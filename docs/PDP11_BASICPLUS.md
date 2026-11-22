# PDP-11 / RSTS/E BASIC-PLUS edition

**Status:** first BASIC-PLUS **source port**, 22 November 2026. **Static checks pass; NOT yet run under an actual RSTS/E BASIC-PLUS interpreter.** The tested playable edition remains the TRS-80 Model III ROM BASIC source at [`../DND1PLAY.BAS`](../DND1PLAY.BAS).

The additional PDP-11 target is a celebration of the Teletype-and-timesharing experience Roy recalls, **not proof** that the original 1977 game ran on a PDP-11. The historical machine and BASIC dialect remain uncertain.

## Files

- [`../pdp11/DND11.BAS`](../pdp11/DND11.BAS) — **602 numbered lines** of ASCII BASIC-PLUS source for RSTS/E, with embedded maps, commands and `REM` explanations. `DND11` is deliberately a short, RSTS-friendly basename.
- [`../tools/build_pdp11.py`](../tools/build_pdp11.py) — deterministic conversion from the restored TRS edition. Does not modify the historical source files.
- [`../tests/check_pdp11.py`](../tests/check_pdp11.py) — verifies syntax profile, branch targets, all dungeon cells, map-edit boundary logic and rebuild reproducibility. It is **not** a BASIC-PLUS interpreter.

## Reference manual supplied for this port

Digital Equipment Corporation, **_BASIC-PLUS Language Manual_**, order **AA-2623D-TC**, **December 1981**; the scanned cover specifies **RSTS/E V7.1** and **BASIC-PLUS V7.1**. The uploaded copyrighted manual is a development reference and is **not redistributed by this repository**.

Relevant sections in that manual:

| Section | Rule used in this port |
| --- | --- |
| 4.1, 4.4, 4.5 (pp. 4-1, 4-6, 4-7) | `NEW`, `RUN`, and `SAVE` workflow in the BASIC-PLUS environment |
| 7.3, 7.5 (pp. 7-4, 7-9 to 7-12) | Backslash `\` for multiple statements and `EXTEND` for longer variable names |
| 7.4 (pp. 7-6 to 7-8) | `REM` comments; preserve historical notes and portability explanations |
| 9.2, 9.3, 9.4 (pp. 9-3 to 9-15) | `PRINT`, `INPUT`, `READ` / `DATA`, `RESTORE`, `GOTO`, `IF` |
| 10.5 (pp. 10-9 to 10-11) | `LEFT(A$,N)`, `MID(A$,N1,N2)`, `CHR$(N)`, `LEN(A$)`, and `VAL(A$)` |

**Important:** The name of the downloaded document may contain other version numbers; the **manual's own cover identifies V7.1**. We target that documented syntax as a starting baseline; other RSTS/E versions require their own testing.

## Adaptations from the Model III edition

1. **Line `10 EXTEND`** enables the naming/syntax rules used by the source; the Model III source has no such command.
2. BASIC-PLUS joins statements with **backslash `\`**, not the Model III colon `:`. Colons inside quoted strings and `REM` text are preserved.
3. BASIC-PLUS calls the string functions **`MID(...)` and `LEFT(...)` without trailing `$`**, even though the return value is a string. `CHR$`, `VAL`, `LEN`, `DIM`, `READ`, `RESTORE`, `PRINT`, `INPUT`, `GOTO`, and `GOSUB` are retained.
4. The Model III-specific `CLEAR 3000` string-space allocation is removed. RSTS/E manages storage differently; **actual per-job memory requirements are not yet verified**.
5. The **seven 26×26 maps remain completely embedded**, but each source `DATA` line now contains exactly **one 26-digit row** rather than an up-to-156-digit chunk. This makes a 26-column row recognisable in an 80-column terminal listing and avoids long physical source lines. All **182 DATA rows** were compared byte-for-byte to the seven preserved maps in `DND1PLAY.BAS`.
6. Map mutation is written as string concatenation with `LEFT(...)` and `MID(...)`, with separate cases for the first and last column. There is **no** `PEEK`, `POKE`, terminal-control escape code, or disk file API.
7. The original TRS edition's in-program `RUN` replay shortcut is replaced by a message telling the user to issue `RUN` again at the BASIC-PLUS prompt. It is safer than assuming an in-program `RUN` statement works under RSTS/E.
8. A `32767 END` is placed after the final embedded `DATA` row, matching the numbered-program style shown in the DEC manual.

**Gameplay design:** both restored editions deliberately use the *same reconstructed* rules, command numbers, map codes, character classes, shop and paper-tape save/restore scheme. This is **not** a line-for-line recovery of the historical DND#1 code.

## Planned RSTS/E session

Once an RSTS/E PDP-11 or compatible emulator is available, enter the BASIC-PLUS environment. A typical manual-based workflow is:

```text
Ready
NEW DND11
[enter or transfer the numbered text in pdp11/DND11.BAS]
SAVE
RUN
```

`NEW`, `SAVE`, and `RUN` are **BASIC-PLUS environment commands**, not operating-system shell commands. Your actual login prompt and how a large ASCII listing is imported depend on the RSTS/E installation, DEC terminal settings and available transfer utilities. **The transcript above is a proposed workflow, not a tested session.** Save the source in a file accessible to the account before relying on it.

When the game starts, choose `N` for a new game, choose dungeon `1`–`7`, enter your character and use command `99` for help. Command `7` prints a paper-tape-style save record; choosing `O` at the next run accepts the same data. There is **no automatic disk-save implementation** in either current edition.

## Test plan for a real PDP-11 / RSTS/E environment

1. Confirm a BASIC-PLUS runtime and version: preferably V7.1, then later versions.
2. Transfer the 602 numbered lines as ASCII without converting `\` to `:`. Check `LIST` for rejected lines or syntax warnings.
3. Run a Fighter in Dungeon 1 through name, class, characteristics and equipment shop.
4. Use `99` help and `6` look; confirm exactly 11 printable map rows with `9` at the player.
5. Test movement, doors, traps, treasure, and combat for runtime or subscript errors.
6. Test dungeon 7 (the map preserved from Roy's earlier TRS-80 conversion).
7. Print a save with command `7`, restart and restore from the printed record with `O`.
8. Measure memory usage and test behavior on RSTS/E systems with different job quotas or BASIC-PLUS revisions.
9. Capture a transcript and any failing BASIC line number, then correct only the **new port**, not archival programs.

### Reproduce the static validation now

```sh
python3 tools/build_pdp11.py --check
python3 tests/check_pdp11.py
```

**Current verified result:** the source is reproducible, basic program structure and direct branch targets are valid, and all seven map grids match the restored TRS-80 edition. **Current unverified result:** translating/executing `DND11.BAS` on the actual BASIC-PLUS runtime and completing gameplay.
