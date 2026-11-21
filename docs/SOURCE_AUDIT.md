# DND#1 restoration — initial source and data audit

**Date:** 21 November 2026  
**Scope:** Text BASIC listings, six external dungeon grids, embedded TRS-80 map, and `GMSTR` text. This is a **static source audit**, not evidence that the program runs. The scanned `DND1_source.pdf` has **not yet been compared page by page**.

## Historical context and goals

The game is described in the surviving repository as Richard Garriott's 1977 **DND#1**. Roy recalls using a Teletype Model 33 connected to a school time-sharing DEC system, **possibly a PDP-11**. The host model and original BASIC dialect remain unconfirmed; do not present them as established facts.

The restoration goal is a **single, self-contained BASIC program** faithful to the text-terminal experience. This can be developed and tested without making the original 48 KB Model III memory ceiling a design requirement. A separate, smaller hardware-compatible build can follow.

## Source inventory

| File | Static finding | Preservation decision |
| --- | --- | --- |
| `DND.BAS` | 1,215 numbered BASIC lines; original-version listing uses `BASE 0`, `FILE #`, `READ #`, `WRITE #`, `RESTORE #` and `CLK` | **Preserve unchanged** |
| `DND1TRS.BAS` | 1,292 numbered lines; earlier TRS-80 LBASIC port, including one embedded 26×26 map | **Preserve unchanged** |
| `DNG1`, `DNG2`, `DND3`, `DNG4`, `DNG5`, `DNG6` | Six surviving 26×26 numeric grids; each has 676 cells; codes observed: 0–8 | **Preserve unchanged** |
| `GMSTR` | Includes another 26×26 grid plus metadata, gear and monster records | **Preserve unchanged** |
| `DND1_source.pdf` | Historical scanned reference, about 9.25 MB | **Preserve; scan comparison still pending** |

### Embedded dungeon is not a copy of the surviving external maps

The TRS-80 port contains **26 DATA statements** each with **26 values**, read into `D(0..25,0..25)`.

| External grid compared with embedded grid | Identical cells | Different cells |
| --- | ---: | ---: |
| `DNG1` | 354 / 676 | 322 |
| `DNG2` | 340 / 676 | 336 |
| `DND3` | 334 / 676 | 342 |
| `DNG4` | 343 / 676 | 333 |
| `DNG5` | 351 / 676 | 325 |
| `DNG6` | 355 / 676 | 321 |
| `GMSTR` grid | 343 / 676 | 333 |

The embedded map is **distinct from all six surviving external dungeon maps**. We cannot determine from this alone whether it was hand-edited, generated, or copied from a missing source. Treat it as a **seventh map**, not a replacement for a known numbered dungeon.

The maps pass shape checks but **that does not prove their contents are historically complete or correct**.

## Concrete issues to investigate

1. **Startup BASIC syntax:** `DND1TRS.BAS` line `00404` lacks the closing quotation mark in a `PRINT` statement. A new working copy should correct it; leave the archival file unchanged.
2. **External map name:** original `DND.BAS` uses `DNG3`; the third grid is currently named `DND3`. We should create an alias during import or in the build process rather than renaming the archival file.
3. **Dungeon selector:** `DND1TRS.BAS` accepts a dungeon number at line `00420`, but its `01400` block reads one fixed embedded map for all choices. A self-contained edition should select among all verified maps, including the seventh as a separately identified option.
4. **Save/load:** original `DND.BAS` uses external file operations and `GMSTR`; the TRS-80 port has no complete LDOS load/save implementation. Its `PRINT CHR$(4)` sequences resemble another system's DOS command convention, **not a working LBASIC file-I/O implementation**. Do not assume `GMSTR` can be loaded as-is.
5. **Old game:** `DND1TRS.BAS` explicitly reports that loading an old game is unsupported; another save path emits data as printed output. Both require redesign and runtime tests.
6. **Access gate:** the original and the TRS-80 port require the name `SHAVS` at line `00460`. It is part of the historical program but prevents ordinary player names; preserve it as an optional historical mode.
7. **BASIC dialect:** commands in the original listing are not standard LDOS LBASIC. Establish semantics against the original printed listing and interpreter reference before rewriting `RND`, `READ`, and file I/O.
8. **Memory:** the existing port is roughly 32 KB as ASCII text. Tokenised BASIC code plus arrays, strings and data may be tight on a physical 48 KB system. Do not assume the complete single-file edition fits on original hardware.

## Checks completed

- Both BASIC source files have unique numbered lines.
- A static scan found **no missing literal GOTO/GOSUB/THEN line-number targets**. Dynamic targets and runtime control-flow errors have not been checked.
- The only unmatched quoted string found outside `REM` statements in the current TRS port is **line 00404**.
- Six external map files, one embedded map, and the 26×26 grid inside `GMSTR` were inspected for row and column counts.

Run `python3 tools/audit_sources.py` to reproduce the structural and map checks.

## Proposed development layout (not yet implemented)

- `DND.BAS`, `DND1TRS.BAS`, all data files and the scanned PDF remain **historical artifacts**.
- `src/DND1_ALL.BAS` — new self-contained development source; name to be confirmed before building.
- `tests/` — scripted input, expected output and map/inventory assertions.
- `docs/` — audit notes, verified behaviour, the emulator test protocol and provenance.

## First executable milestone

1. Create a new working copy, repair the first parsing errors, and load it under TRS80gp.
2. Complete character creation through the start of a dungeon.
3. Replace hard-coded one-map loading with selectable embedded maps, keeping original map identities and preserving all original files.
4. Verify movement, look and map boundaries before enabling combat or save/load.
5. Record emulator configuration, actual output, failures and limitations.

**Status:** Phase 1 source/data inventory completed. No original files modified; no emulator execution performed yet.
