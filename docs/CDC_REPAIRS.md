# DND1CDC source repair log

**Approach:** We preserved the archival [`DND.BAS`](../DND.BAS) **byte-for-byte**, copied its full logic into [`DND1CDC.BAS`](../cdc/DND1CDC.BAS), made explicitly logged repairs and did not remove original subsystems wholesale. Original line numbers are maintained so a researcher can compare the two versions.

## Changes to the historical source

| Original line(s) | Repair | Rationale |
| --- | --- | --- |
| 1–2, 30 | New port / preservation attribution and explanatory `REM` | Clearly identify the derivative, preserve original elsewhere |
| 160 | `RND(CLK(0))` | Use CDC BASIC V2's documented clock seed convention |
| 422–423 | Validate dungeon choice **1 through 6** | Avoid invalid file ordinal access |
| 459–460 | Preserve original `SHAVS`-only gate in a remark, allow other player names | Enable ordinary players to start without losing the historical quirk |
| 881 | Remove comparison of numeric `Y` with empty string | Avoid a possible CDC numeric/string type error |
| 1461–1469 | Search for a passable start floor when random spawn is blocked | Avoid starting trapped inside a wall |
| 1601, 1606 | Replace invalid numeric/string comparison and unsafe dungeon editor shortcut with command help | Make numeric command input coherent |
| 1730–1760 | Replace historical prank `STOP` gate with explanatory help | Keep game start accessible |
| 2365–2366, 3307–3308, 7385–7386 | Check map boundaries before adjacent or two-step accesses | Prevent out-of-bounds array subscripts |
| 2416 | Add **G9** rather than constant 69 to gold balance | Correct mismatched printed and awarded loot |
| 3310 | Fix `D(G+S,T+T)` to `D(G+S,H+T)` | Adjacent door location must use the current horizontal position |
| 4650 | Fix chained `=` into a hit-point subtraction | Make fist damage numeric |
| 5290 | Correct mace range branch | Previous route jumped to the wrong case |
| 6180 | Use hit result `R2=1` rather than uninitialized `T2` | Repair combat damage decision |
| 6300 | Test actual weapon number `J`, not inventory subscript `W(J)` | Correct item selection |
| 6411 | Replace the spurious `uprintf(...)` C-language debugging command with `REM` | Invalid syntax for CDC BASIC |
| 7230 | Test actual monster horizontal displacement `R9` | Avoid stale loop index `M` |
| 8420–8560 | Replace broken monster scan / bad `GOTO 8250` with `F1,F2`-based range calculation | Prevent accidental jump into death logic and restore enemy distance calculation |

The repairs are **not** a proof that all historical mechanics work. In particular, the original program has complex and sometimes inconsistent item consumption, attack, magic and save logic. We have **not yet run it** under CDC V2 nor replayed a full game. Further repairs must be documented as their behaviour is verified.

## Dungeon files

The historical text files are at repository root, with the third named `DND3`. The CDC version requires numbered files `DNG1`–`DNG6` containing **CDC binary numbers**, not text lines. The companion `MAKEFILE.BAS` embeds the exact contents of the six original maps as 156 `DATA` statements and writes the correct binary record sequence; the new `cdc/data/DNG3.txt` is derived from historical `DND3`.

The `GMSTR` file is written by the original game as binary saved state. Do not confuse it with the archival textual `GMSTR` file; the new initializer resets the game-save file, and OLD only works after an actual SAVE.

See [CDC platform and setup](CDC_BASIC_ENVIRONMENT.md) and [original platform identification](ORIGINAL_PLATFORM.md).
