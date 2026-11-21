#!/usr/bin/env python3
"""Read-only structural audit of the historical DND#1 BASIC and map files.

Run: python3 tools/audit_sources.py
Never modifies a source or data file.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DIM = 26
MAP_NAMES = ("DNG1", "DNG2", "DND3", "DNG4", "DNG5", "DNG6")
BASIC_NAMES = ("DND.BAS", "DND1TRS.BAS")


def basic_lines(path):
    result = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^\s*(\d+)\s+(.+)$", raw)
        if match:
            result.append((int(match.group(1)), match.group(2)))
    return result


def external_map(path):
    output = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        fields = raw.split()
        if len(fields) == DIM and all(re.fullmatch(r"\d+", f) for f in fields):
            output.append([int(f) for f in fields])
    return output


def embedded_map(lines):
    output = []
    for number, source in lines:
        if not 1400 <= number <= 1510:
            continue
        match = re.match(r"DATA\s+([\d, ]+)$", source.strip(), re.I)
        if not match:
            continue
        items = [v.strip() for v in match.group(1).split(",")]
        if len(items) == DIM and all(v.isdecimal() for v in items):
            output.append([int(v) for v in items])
    return output


def check_map(label, data):
    shape_ok = len(data) == DIM and all(len(row) == DIM for row in data)
    values = sorted({v for row in data for v in row})
    cells_ok = shape_ok and set(values).issubset(set(range(9)))
    print(f"{label:<16} {len(data):2} rows; shape={'OK' if shape_ok else 'CHECK'};"
          f" codes={values}; codes={'OK' if cells_ok else 'CHECK'}")
    return shape_ok


def check_basic(label, lines):
    numbers = [number for number, _ in lines]
    line_set = set(numbers)
    duplicate = len(numbers) - len(line_set)
    absent = []
    odd_quotes = []
    for number, source in lines:
        if source.lstrip().upper().startswith("REM"):
            continue
        if source.count('"') % 2:
            odd_quotes.append(number)
        for match in re.finditer(r"\b(?:GOTO|GOSUB|THEN)\s+(\d+)\b", source, re.I):
            target = int(match.group(1))
            if target not in line_set:
                absent.append((number, target))
    print(f"{label}: {len(lines)} numbered lines; duplicates={duplicate};"
          f" missing direct targets={len(absent)}; odd-quote lines={odd_quotes}")
    if absent:
        print(f"  missing targets (first 10): {absent[:10]}")
    return duplicate == 0 and not absent


def main():
    print("DND#1 source/data structural audit (not a runtime test)")
    print("=" * 64)
    basics = {}
    for name in BASIC_NAMES:
        basics[name] = basic_lines(ROOT / name)
        check_basic(name, basics[name])
    print()
    maps = {}
    for name in MAP_NAMES:
        maps[name] = external_map(ROOT / name)
        check_map(name, maps[name])
    map_save = external_map(ROOT / "GMSTR")
    check_map("GMSTR map", map_save)
    trsm = embedded_map(basics["DND1TRS.BAS"])
    check_map("Embedded TRS", trsm)
    print()
    if len(trsm) == DIM and all(len(row) == DIM for row in trsm):
        for name, ext in maps.items():
            if len(ext) != DIM or any(len(row) != DIM for row in ext):
                continue
            equal = sum(trsm[row][col] == ext[row][col]
                        for row in range(DIM) for col in range(DIM))
            print(f"Embedded vs {name}: {equal}/{DIM*DIM} identical cells")
    print()
    print("Filename warning: original DND.BAS requests DNG3,")
    print("  but surviving third-map file in repository is DND3.")
    print("Port warning: DND1TRS.BAS line 00404 has an unclosed string.")
    print("Save/load warning: CHR$(4) print control sequences are")
    print("  not LDOS file I/O; runtime paths need rewriting.")
    print("Note: full gameplay and scanned PDF not tested by this script.")


if __name__ == "__main__":
    main()
