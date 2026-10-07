# DND#1 — BASIC port experiments

An attempt to run Richard Garriott's 1977 DND#1 on a PDP-11 clone, with a partial port to TRS-80 LBASIC under LDOS 5.x.

**Status:** incomplete. The original BASIC dialect has not been established, and file I/O in the TRS-80 port remains unfinished. Save-game support is not implemented in that port.

## Repository contents

| File | Purpose |
| --- | --- |
| [DND.BAS](DND.BAS) | Original-version BASIC listing supplied with this project |
| [DND1TRS.BAS](DND1TRS.BAS) | Partial TRS-80 LBASIC port |
| `DNG1`–`DNG6`, `DND3`, `DNG4`, `DNG5`, `GMSTR` | Supplied game data and supporting files; retain their original names |
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

The flat layout is appropriate for this small source-and-data collection. Keep data filenames intact when transferring files. Suggestions and test results are welcome through [repository issues](https://github.com/royedmund/dnd-1/issues).
