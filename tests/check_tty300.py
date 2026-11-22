#!/usr/bin/env python3
"""Basic structural checks for a Model III 300-baud direct-UART program.

Checks the source profile and critical hardware constants. Not a serial loopback
or a real PiDP-11/RSTS/E test.
"""
from pathlib import Path
import re

SRC = Path(__file__).resolve().parent.parent / "basic" / "TTY300.BAS"


def main():
    text = SRC.read_text(encoding="ascii")
    lines = []
    for raw in text.splitlines():
        match = re.fullmatch(r"(\d+)\s+(.+)", raw)
        assert match, f"Invalid BASIC statement: {raw!r}"
        lines.append((int(match[1]), match[2]))
    nums = [n for n, _ in lines]
    assert nums == sorted(set(nums)), "Line numbers must be unique and increasing"
    targets = set(nums)
    for number, statement in lines:
        if statement.startswith("REM"):
            continue
        assert statement.count('"') % 2 == 0, f"Odd quote count in {number}"
        for target in re.findall(r"\b(?:GOSUB|GOTO|THEN)\s+(\d+)\b", statement):
            assert int(target) in targets, f"Undefined branch {number} -> {target}"
    for phrase in (
        "OUT 232,0", "OUT 233,85", "OUT 234,104", "INP(234)",
        "INP(235)", "OUT 235,B", "S AND 128", "AND 64", "INKEY$",
        "IF C=10 THEN RETURN", "IF C=13 THEN PRINT:RETURN",
    ):
        assert phrase in text, f"Missing terminal requirement: {phrase}"
    assert "SET *CL" not in "\n".join(stmt for _, stmt in lines if not stmt.startswith("REM"))
    # 0x68: DTR asserted, RTS asserted, parity disabled, 1 stop, 8 data bits.
    ctl = 104
    assert ctl & 0x60 == 0x60
    assert ctl & 0x08 == 0x08
    assert ctl & 0x10 == 0
    assert ctl & 0x03 == 0
    print(f"PASS: TTY300.BAS {len(lines)} numbered BASIC statements; all branches exist")
    print("PASS: direct UART 300/8N1, receive priority, TX status and CR/LF filtering")
    print("NOT tested: Model III serial hardware, PiDP-11 USB adapter or RSTS/E login")


if __name__ == "__main__":
    main()
