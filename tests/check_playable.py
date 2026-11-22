#!/usr/bin/env python3
"""Static checks for the portable BASIC DND#1 reimplementation.

Usage: python3 tests/check_playable.py
Optional: original sources/maps at repo root are compared byte-for-byte
against their embedded data. Never modifies any source file.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "DND1PLAY.BAS"
MAPS = ("DNG1", "DNG2", "DND3", "DNG4", "DNG5", "DNG6", "EMBEDDED-TRS")


def original_map(name: str) -> str | None:
    if name == "EMBEDDED-TRS":
        path = ROOT / "DND1TRS.BAS"
        if not path.is_file():
            return None
        chunks = []
        for raw in path.read_text(encoding="utf-8-sig").splitlines():
            m = re.match(r"^\s*(\d+)\s+DATA\s+((?:\d+,){25}\d+)\s*$", raw, re.I)
            if m and 1400 <= int(m.group(1)) <= 1510:
                chunks.append(m.group(2).replace(",", ""))
        return "".join(chunks)
    path = ROOT / name
    if not path.is_file():
        return None
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        parts = line.split()
        if len(parts) == 26 and all(re.fullmatch(r"[0-8]", p) for p in parts):
            rows.append("".join(parts))
    return "".join(rows)


def check() -> None:
    lines = PROGRAM.read_text(encoding="ascii").splitlines()
    entries = []
    for line in lines:
        m = re.fullmatch(r"(\d+)\s+(.+)", line)
        assert m, f"Missing line number: {line!r}"
        entries.append((int(m.group(1)), m.group(2)))
    nums = [n for n, _ in entries]
    assert nums == sorted(set(nums)), "Line numbers unsorted or repeated"
    assert len(entries) >= 400, "Unexpectedly short playable BASIC source"
    lookup = set(nums)
    bad_quotes = []
    direct_targets = []
    for number, source in entries:
        if source.upper().startswith("REM"):
            continue
        if source.count('"') % 2:
            bad_quotes.append(number)
        for m in re.finditer(r"\b(?:GOTO|GOSUB|THEN)\s+(\d+)\b", source, re.I):
            direct_targets.append((number, int(m.group(1))))
    assert not bad_quotes, f"Unclosed quote(s): {bad_quotes}"
    missing = [(a,b) for a,b in direct_targets if b not in lookup]
    assert not missing, f"Missing branch targets: {missing}"

    data = [re.fullmatch(r'DATA "([0-8]+)"', source) for _, source in entries
            if source.startswith('DATA ')]
    assert len(data) == 35 and all(data), "Expected 35 quoted map DATA records"
    chunks = [m.group(1) for m in data]
    decoded = []
    for index, name in enumerate(MAPS):
        group = chunks[index*5:index*5+5]
        assert list(map(len, group)) == [156, 156, 156, 156, 52], f"Wrong chunk lengths: {name}"
        grid = "".join(group)
        assert len(grid) == 26*26, f"Wrong grid dimensions: {name}"
        assert set(grid) <= set("012345678"), f"Unexpected tile code: {name}"
        original = original_map(name)
        if original is None:
            print(f"{name}: 676 tiles OK (archival comparison not available)")
        else:
            assert grid == original, f"MAP MISMATCH: {name}"
            print(f"{name}: 676 tiles MATCH archival data")
        decoded.append(grid)
    assert len(set(decoded)) == 7, "One or more maps are accidental duplicates"

    program_text = "\n".join(src for _, src in entries if not src.upper().startswith("REM"))
    assert "PEEK(" not in program_text.upper()
    assert "POKE " not in program_text.upper()
    assert "CHR$(4)" not in program_text.upper()
    assert "CLEAR 3000" in program_text, "Model III string memory not reserved"
    assert 'NEXT BK:NEXT MI' in program_text, "Missing embedded map loop"
    assert 'D$(TY)=LEFT$' in program_text, "Portable map update routine missing"
    assert len([1 for n,s in entries if s.startswith('REM ')]) >= 45, "Insufficient explanatory REM statements"
    print(f"BASIC source: {len(entries)} numbered lines; {len(direct_targets)} direct branches; no missing targets")
    print("All seven 26x26 maps verified; source structure OK.")


if __name__ == "__main__":
    try:
        check()
    except AssertionError as exc:
        print("FAIL:", exc, file=sys.stderr)
        sys.exit(1)
