#!/usr/bin/env python3
"""Build the RSTS/E BASIC-PLUS (EXTEND mode) edition from DND1PLAY.BAS.

This only changes the new restoration, and never edits historical files.  The
long Model III DATA chunks are expanded into one DATA string per dungeon row.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'DND1PLAY.BAS'
TARGET = ROOT / 'pdp11' / 'DND11.BAS'


def split_numbered(line: str) -> tuple[int, str]:
    m = re.fullmatch(r'\s*(\d+)\s+(.+)', line)
    if not m:
        raise ValueError(f'Not a numbered BASIC line: {line!r}')
    return int(m[1]), m[2]


def rewrite_separator(statement: str) -> str:
    """Translate MS/Model-III colon separators to BASIC-PLUS backslash.

    Do not alter quoted literal strings (including prompt messages).
    """
    out = []
    quoted = False
    if statement.lstrip().upper().startswith('REM '):
        return statement
    for ch in statement:
        if ch == '"':
            quoted = not quoted
        out.append('\\' if ch == ':' and not quoted else ch)
    if quoted:
        raise ValueError('Unbalanced quotation mark: ' + statement)
    return ''.join(out)


def port(source: str) -> str:
    original = [split_numbered(s) for s in source.splitlines() if s.strip()]
    src = dict(original)
    if len(src) != len(original):
        raise ValueError('Duplicate line number in TRS source')

    chunks = [m.group(1) for line, text in original
              if line >= 9000 and (m := re.fullmatch(r'DATA "([0-8]+)"', text))]
    if len(chunks) != 35:
        raise ValueError(f'Expected 35 source DATA chunks, found {len(chunks)}')
    maps = [''.join(chunks[i * 5:(i + 1) * 5]) for i in range(7)]
    for m in maps:
        if len(m) != 676 or any(ch not in '012345678' for ch in m):
            raise ValueError('Unexpected dungeon map dimensions or value')

    src[10] = 'EXTEND'
    src[11] = 'REM DND#1 FOR PDP-11 / RSTS/E BASIC-PLUS V7.1'
    src[12] = 'REM RECREATION PORTED FROM THE MODEL III EDITION'
    src[13] = 'REM TEXT-TERMINAL INPUT/OUTPUT; NO DISK FILE I/O'
    src[14] = 'REM DEC BASIC-PLUS DIALECT: EXTEND, MID, LEFT'
    src[15] = 'REM NO PDP-11 OR RSTS/E RUN HAS YET BEEN DONE'
    src[50] = 'REM RSTS/E BASIC-PLUS EXTEND MODE, PDP-11'
    src[95] = 'REM PRINT AND INPUT ONLY; NO MACHINE-SPECIFIC IO'
    src[100] = src[100].replace('CLEAR 3000:', '')
    src[6740] = 'IF Q$="Y" OR Q$="y" THEN PRINT "TYPE RUN TO START AGAIN"'

    # Sequential READ works in Model III and RSTS/E BASIC-PLUS. This avoids
    # line-numbered RESTORE, which the Model III ROM BASIC cannot execute.
    src[7200] = 'REM READ THE CHOSEN MAP FROM SEQUENTIAL DATA ROWS'
    src[7210] = 'RESTORE'
    src[7215] = 'REM EACH MAP IS 26 STRINGS OF 26 DIGITS'
    src[7220] = 'FOR MI=1 TO DN'
    src[7230] = 'FOR BK=0 TO 25'
    src[7240] = 'READ RW$'
    src[7250] = 'IF MI=DN THEN D$(BK)=RW$'
    src[7260] = 'NEXT BK'
    src[7270] = 'NEXT MI'
    for num in (7265,):
        src.pop(num, None)

    # DEC's functions are LEFT(s$,n), MID(s$,start,n) with NO dollar sign,
    # whereas Radio Shack BASIC uses LEFT$, MID$.  DEC MID takes three args.
    src[8180] = 'REM REPLACE ONE MAP CELL WITH DEC LEFT AND MID'
    src[8190] = 'REM TY ROW TX COLUMN TV NEW DIGIT'
    src[8200] = 'IF TX=0 THEN D$(TY)=CHR$(48+TV)+MID(D$(TY),2,25)\\RETURN'
    src[8210] = 'IF TX=25 THEN D$(TY)=LEFT(D$(TY),25)+CHR$(48+TV)\\RETURN'
    src[8220] = 'D$(TY)=LEFT(D$(TY),TX)+CHR$(48+TV)+MID(D$(TY),TX+2,25-TX)'
    src[8230] = 'RETURN'

    # Remove the compact Model III DATA section; expand to one 26-digit row
    # per DATA statement, to suit 80-column and printing terminals.
    for n in list(src):
        if n >= 8990:
            del src[n]
    src[8990] = 'REM SEVEN MAPS, 26 ROWS OF 26 DIGITS EACH'
    src[9000] = 'REM READ BY 7200; DO NOT MOVE DATA AHEAD OF OTHER DATA'
    num = 9010
    tags = ('DNG1', 'DNG2', 'DND3', 'DNG4', 'DNG5', 'DNG6', 'TRS7')
    for name, dungeon in zip(tags, maps):
        src[num] = f'REM MAP {name}, 26 ROWS'
        num += 10
        for i in range(26):
            src[num] = f'DATA "{dungeon[i * 26:(i + 1) * 26]}"'
            num += 10
    if num >= 32767:
        raise ValueError('DATA section exceeds BASIC-PLUS line numbers')
    src[32767] = 'END'

    result = []
    for num, command in sorted(src.items()):
        command = re.sub(r'\bMID\$\s*\(', 'MID(', command, flags=re.I)
        command = re.sub(r'\bLEFT\$\s*\(', 'LEFT(', command, flags=re.I)
        command = rewrite_separator(command)
        line = f'{num} {command}'
        if len(line) > 120:
            raise ValueError(f'Line too long for our teletype profile: {num} ({len(line)})')
        result.append(line)
    return '\n'.join(result) + '\n'


def main():
    result = port(SOURCE.read_text(encoding='ascii'))
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    if '--check' in sys.argv:
        if not TARGET.is_file() or TARGET.read_text(encoding='ascii') != result:
            sys.exit('ERROR: pdp11/DND11.BAS differs from regenerated source')
        print(f'MATCH: {TARGET} ({result.count(chr(10))} BASIC lines)')
    else:
        TARGET.write_text(result, encoding='ascii', newline='\n')
        print(f'Wrote {TARGET} ({result.count(chr(10))} BASIC lines)')


if __name__ == '__main__':
    main()
