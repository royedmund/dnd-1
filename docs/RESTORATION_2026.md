# DND#1 portable BASIC reconstruction — development record

**22 November 2026.** The restoration is aimed at a TRS-80 Model III, while keeping the game terminal-based and the BASIC as widely reusable as practical.

## Preservation rules

The surviving source files `DND.BAS` and `DND1TRS.BAS`, the scan `DND1_source.pdf`, and the seven external/supporting files (six dungeon grids plus `GMSTR`) are **archival materials**: do not overwrite them to fix the new build. They may be incomplete, and the original DEC/BASIC environment is uncertain. The 2021 port is preserved as Roy's earlier attempt.

The restoration is in the new root file `DND1PLAY.BAS`. This file is intentionally a **playable reimplementation** of the early game, rather than a claim that all original routines have been reproduced faithfully. No source outside the repository is imported verbatim.

## First working edition

- Added descriptive `REM` headings to the numbered BASIC listing, describing user prompts, state, map format, combat, magic, equipment, dice and printed saves.
- Recreated fighter, cleric and wizard character creation, 3d6 attributes, hit points, gold and equipment shopping.
- Added deterministic portable dice using explicit arithmetic instead of interpreter-specific `RND` seeding.
- Preserved the numbered commands and **numeric 11×11 look map** (`9` for the player) to reflect the early Teletype interface rather than a colour/graphics interface.
- Restored movement, walls, doors, traps, secret doors, gold, character bonuses, monster encounters, combat/retaliation, spells, weapon switching, equipment, death and a new-game option.
- Preserved the **six complete external 26×26 dungeon grids** inside the standalone program; the seventh selection contains the **distinct 26×26 map** found in the old `DND1TRS.BAS` port. Runtime files `DNG1`–`DNG6`/`DND3` are no longer required.
- Added a portable **printed paper-tape save/restore** feature. This is not a genuine DEC or LDOS disk-save implementation. A full hero state and the mutated dungeon map are printed, then can be re-entered for an old game.
- Removed the archival `SHAVS` player-name lock in the **new** program. It remains intact in the preserved historical code.
- Added help, status, eating spare food and a clean quit, clearly marked as adaptation conveniences.

## Compatibility problems found and solved

1. Model III ROM BASIC reports `?SN Error` for `RESTORE <line number>`. The loader instead uses plain `RESTORE` and sequential data reads.
2. Storing 7×676 individual numeric `DATA` cells caused long load delays. We now encode each dungeon as **five quoted strings** (6,6,6,6,2 rows), all at most 156 characters each, and split the chosen data into 26 rows.
3. To avoid a 26×26 numeric allocation and its slow initialisation, each dungeon row is a string in `D$(0..25)`. The map-update routine uses `LEFT$`, `CHR$` and `MID$` to change one cell.
4. Model III ROM BASIC's small default string-space allocation produced `?OS Error` on map load. `CLEAR 3000` reserves sufficient string storage; this may need adaptation in other BASIC dialects.
5. Save-state restoration does not call the new-game map loader; doing so would overwrite the saved coordinates, monster state and dungeon map.
6. Model III ROM BASIC was tested via the 2.5.8 emulator. This is **not** equivalent to testing LDOS 5.1 LBASIC or physical equipment.

## What differs from the historical program

- Combat and spell outcomes are intentionally reconstructed and simplified for a dependable minimum playable game; not every original equipment/stat/class rule is carried over.
- The archival gate `SHAVS` is removed in normal play.
- Save/load uses a portable **human-readable text transcript**, not `FILE #`, `READ #`, `WRITE #`, LDOS file I/O or an equivalent of the historical `GMSTR` format.
- The dungeon descriptions, gold, monster stats and encounters may differ from the original, although **all seven map layouts are kept unchanged**.
- The new `98` exit and `99` help commands, `10` status and `12` food are restoration conveniences.
- Some BASIC dialects may need small adjustments to `CLEAR` and `INPUT` syntax. Hardware limits still matter on a physical Model III.

## Test status

Under **trs80gp 2.5.8**, emulating Model III **ROM BASIC**, the following have been run successfully: fighter/wizard setup and shop, Dungeons 1, 2 and 7 loading, numeric look, help and quit, moving/search/status, paper-tape save printout, manual paper-tape restore of all 26 map rows, monster combat, offensive magic, retaliation and death. Python static tests verify all seven map grids match the source data and all explicit BASIC jump targets exist.

Not yet guaranteed: full completion of every dungeon, balanced monster encounters, all class/weapon edge cases, true historical game-rule equivalence, the untouched earlier TRS port, physical 48K hardware or LDOS 5.1 LBASIC.

See `docs/TRS80GP_TESTING.md` for test instructions and `tests/check_playable.py` for source/data checking.
