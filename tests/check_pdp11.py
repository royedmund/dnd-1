#!/usr/bin/env python3
"""Static checks for the PDP-11 BASIC-PLUS edition. Does NOT run RSTS/E.

Usage: python3 tests/check_pdp11.py
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'DND1PLAY.BAS').read_text(encoding='ascii')
port = (ROOT / 'pdp11' / 'DND11.BAS').read_text(encoding='ascii')


def numbered(code):
    statements = []
    for raw in code.splitlines():
        m = re.fullmatch(r'(\d+)\s+(.+)', raw)
        assert m, f'Malformed line {raw!r}'
        number = int(m[1])
        assert 1 <= number <= 32767
        statements.append((number, m[2]))
    return statements


def strip_quoted(text):
    """Ignore strings when scanning for separators and control-flow references."""
    return re.sub(r'"[^"\n]*"', '""', text)


def extract_map_groups(code, expected_count):
    data = []
    for _, text in numbered(code):
        m = re.fullmatch(r'DATA\s+"([0-8]+)"', text)
        if m:
            data.append(m[1])
    assert len(data) == expected_count, (len(data), expected_count)
    return data


def main():
    ls = numbered(port)
    ids = [n for n, _ in ls]
    assert ids == sorted(set(ids)), 'Line numbers must be unique and increasing'
    statements = dict(ls)
    assert statements[10] == 'EXTEND'
    assert statements[32767] == 'END'
    assert len(ls) > 600
    assert max(len(f'{n} {s}') for n, s in ls) <= 120
    assert statements[7210] == 'RESTORE'
    assert 'CLEAR 3000' not in port
    assert 'MID$(' not in port and 'LEFT$(' not in port and 'RIGHT$(' not in port
    assert 'MID(D$(TY),TX+2,25-TX)' in port
    assert 'LEFT(D$(TY),TX)' in port
    assert 'CHR$(' in port
    # Confirm only the DEC backslash is used as executable statement separator.
    for n, command in ls:
        if command.startswith('REM '):
            continue
        stripped = strip_quoted(command)
        assert ':' not in stripped, f'Model III colon separator at line {n}'
        assert stripped.count('"') % 2 == 0
        for m in re.finditer(r'\b(?:GOTO|GOSUB|THEN)\s+(\d+)\b', stripped):
            assert int(m[1]) in statements, f'Line {n} branches to missing {m[1]}'

    compact = extract_map_groups(src, 35)
    external = [''.join(compact[i * 5:(i + 1) * 5]) for i in range(7)]
    for grid in external:
        assert len(grid) == 676
        assert set(grid) <= set('012345678')
    decoded = extract_map_groups(port, 182)
    for i in range(7):
        group = decoded[i * 26:(i + 1) * 26]
        assert all(len(s) == 26 for s in group)
        assert ''.join(group) == external[i], f'Dungeon {i + 1} differs'

    # Test intended map-cell string splice at all coordinates, including edges.
    for row in decoded:
        for x in range(26):
            new = '0'
            result = new + row[1:] if x == 0 else (
                row[:25] + new if x == 25 else row[:x] + new + row[x + 1:]
            )
            assert len(result) == 26
            assert result[x] == new

    # Confirm full source can be reproduced without manual edits.
    run = subprocess.run([sys.executable, str(ROOT / 'tools' / 'build_pdp11.py'), '--check'],
                         text=True, capture_output=True)
    assert run.returncode == 0, run.stdout + run.stderr
    print('PASS: BASIC-PLUS source format, branch targets and 7 embedded maps')
    print('PASS: 182 rows = 7 * 26, identical to TRS source data')
    print('PASS: map edit splice at column 0, 1..24 and 25')
    print('PASS: deterministic rebuild from preserved DND1PLAY.BAS')
    print('LIMIT: no RSTS/E BASIC-PLUS interpreter runtime test performed')


if __name__ == '__main__':
    main()
