# DND#1 — BASIC port experiments

A preservation and restoration project for Richard Garriott's 1977 **DND#1**, including earlier PDP-11-clone experiments and a partial TRS-80 **LDOS/LBASIC** port. Roy remembers the game running from a **Teletype Model 33** connected to a school time-sharing **DEC** system; the exact computer (possibly a PDP-11) and BASIC dialect have **not been confirmed**.

**Status:** incomplete. The original BASIC dialect has not been established, and file I/O in the TRS-80 port remains unfinished. Save-game support is not implemented in that port.

## Restoration project — Phase 1 audit

The first **source and dungeon-data audit** is complete. The two historical BASIC files and the original dungeon files have **not been modified**.

- [**Source and data audit**](docs/SOURCE_AUDIT.md): the original listing has 1,215 numbered lines, the TRS-80 attempt has 1,292, six external maps contain complete **26×26** numeric grids, and the 26×26 map embedded in the TRS-80 code is **different from all six**.
- [**TRS80gp testing plan**](docs/TRS80GP_TESTING.md): reproducible Model III/LDOS/LBASIC testing using [George Phillips' emulator](https://48k.ca/trs80gp.html).
- [**Read-only source checker**](tools/audit_sources.py): run `python3 tools/audit_sources.py` from a local checkout to repeat the source/map structural checks.

**Known issues:** the existing port has an unclosed string at line `00404`, lacks completed save/load support, and doesn't yet select between the surviving dungeon maps. The original asks for `DNG3` but the repository has `DND3`. Details, including uncertainty about map provenance, are recorded in the audit.

**Restoration goal:** build a **new, self-contained BASIC edition** (maps and game data embedded) with a text-first, Teletype-inspired interface. The physical 48 KB Model III version can be tackled separately if necessary. Original files remain as historical references.

**Testing status:** static inspection only. The game has **not yet been run successfully in TRS80gp as part of this audit**.

## Repository contents

| File | Purpose |
| --- | --- |
| [DND.BAS](DND.BAS) | Original-version BASIC listing supplied with this project |
| [DND1TRS.BAS](DND1TRS.BAS) | Partial TRS-80 LBASIC port |
| `DNG1`, `DNG2`, `DND3`, `DNG4`, `DNG5`, `DNG6`, `GMSTR` | Supplied game data and supporting files; retain their original names |
| [DND1_source.pdf](DND1_source.pdf) | Reference source listing |
| [LICENSE](LICENSE) | Repository licence text |

## Trying the port

Use a TRS-80 system or emulator with LDOS 5.x and LBASIC. Start with `DND1TRS.BAS`; transfer/import it using the method supported by your system. The port currently embeds external data in its code while file I/O is being worked on. Modern BASIC interpreters should not be assumed compatible.

## Commands

| Command | Action |
| --- | --- |
| `1` | Move |
| `2` | Open door |
| `3` | Search for traps and secret doors |
| `4` | Switch weapon hand |
| `5` | Fight |
| `6` | Look around |
| `7` | Save game — not implemented in the port |
| `8` | Use magic |
| `9` | Buy magic |
| `0` | Pass |
| `11` | Buy hit points |

## Remaining work

- Identify the original BASIC interpreter and its file-handling behaviour.
- Complete file I/O and save-game support in the TRS-80 version.
- Record a repeatable load/run procedure and known failures for each target.

The historical files remain at the repository root; new audit documents live in `docs/` and analysis utilities in `tools/`. Keep original data filenames intact when transferring files. Suggestions and test results are welcome through [repository issues](https://github.com/royedmund/dnd-1/issues).
