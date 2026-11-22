#!/usr/bin/env python3
"""Static CDC BASIC Version 2 source and dungeon-data checker.

This is NOT a CDC compiler or an emulator. Run from any repository directory:
    python3 tests/check_cdc.py
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
N = 26
FILENAMES = ("DNG1", "DNG2", "DND3", "DNG4", "DNG5", "DNG6")


def numbered(path):
    result = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"(\d+)\s+(.+)", line)
        assert match, f"{path}: malformed line {line!r}"
        assert len(line) <= 72, f"{path}: exceeds 72: {line!r}"
        result.append((int(match[1]), match[2]))
    numbers = [n for n, _ in result]
    assert numbers == sorted(set(numbers)), f"{path}: duplicate or unordered lines"
    defined = set(numbers)
    for number, statement in result:
        if statement.startswith("REM"):
            continue
        assert statement.count('"') % 2 == 0, (path, number, "odd quotes")
        for t in re.findall(r"\b(?:GOTO|GOSUB|THEN)\s+(\d+)\b", statement):
            assert int(t) in defined, (path, number, t, "missing target")
    return result


def text_map(path):
    data = [line.split() for line in path.read_text().splitlines() if line.strip()]
    assert len(data) == N and all(len(row) == N for row in data), (path, "shape")
    assert all(x.isdecimal() and 0 <= int(x) <= 8
               for row in data for x in row), (path, "invalid cell")
    return [[int(x) for x in row] for row in data]


def main():
    original = numbered(ROOT / "DND.BAS")
    game = numbered(ROOT / "cdc/DND1CDC.BAS")
    loader = numbered(ROOT / "cdc/MAKEFILE.BAS")
    old = dict(original)
    new = dict(game)
    assert set(old).issubset(set(new)), "lost original line numbers"
    assert len(game) > len(original), "source repairs missing"
    assert "uprintf" not in (ROOT / "cdc/DND1CDC.BAS").read_text()
    assert 'FILE #1="DNG1"' in (ROOT / "cdc/DND1CDC.BAS").read_text()
    assert 'WRITE #F,V' in (ROOT / "cdc/MAKEFILE.BAS").read_text()
    dataset = []
    for name in FILENAMES:
        canonical = text_map(ROOT / name)
        out_name = name if name != "DND3" else "DNG3"
        repack = text_map(ROOT / "cdc/data" / f"{out_name}.txt")
        assert repack == canonical, f"repack mismatch: {name}"
        dataset.extend(canonical)
    rows = []
    for _, stmt in loader:
        m = re.fullmatch(r"DATA\s+(\d+(?:,\d+)*)", stmt)
        if m:
            row = [int(s) for s in m[1].split(",")]
            assert len(row) == N, "loader row length incorrect"
            rows.append(row)
    assert len(rows) == 156, ("loader rows", len(rows))
    assert rows == dataset, "loader DATA does not match original maps"
    changed = [(n, old[n], new[n]) for n in old if old[n] != new[n]]
    assert changed, "no source changes found"
    print("PASS: historic source preserved, CDC derivative checked")
    print(f"      {len(original)} original lines, {len(game)} CDC lines, {len(changed)} modified source lines")
    print("      all source statements <=72 characters and branch targets present")
    print("      six 26x26 maps, 4056 binary initializer values, all match originals")
    print("      NOTE: this does not test CDC compilation or gameplay")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
