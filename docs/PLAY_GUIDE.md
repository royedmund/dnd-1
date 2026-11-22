# Playing the new DND#1 BASIC restoration

## Requirements

- Recommended: **trs80gp 2.5.8** (or a compatible version) in **TRS-80 Model III** mode.
- The game is one plain-text, numbered BASIC listing: [`DND1PLAY.BAS`](../DND1PLAY.BAS).
- Model III ROM BASIC was used for successful emulator tests. **LDOS LBASIC 5.1 and real Model III hardware remain untested**; importing a text file as a native BASIC file may require a transfer utility or program entry.

### Starting the game in trs80gp

Use **File → Run** and select `DND1PLAY.BAS`, or launch from a terminal with:

```text
trs80gp -m3 DND1PLAY.BAS
```

The emulator's direct `.BAS` loader starts the program in ROM BASIC. No separate map disk or external data files are required.

Enter `N` for a new game. Use seed `0` for the repeatable default or a whole number from `1` to `65520` for a different adventure. Select a dungeon from `1` to `7`. Dungeons 1–6 reproduce the six surviving external map grids; dungeon 7 reproduces the different map embedded in the 2021 TRS-80 port. Then type your name, select `F`, `C`, or `W`, buy equipment by number, and enter `0` to finish shopping.

## Commands

All commands are numbers. Enter `99` at the command prompt to see the whole list.

| Command | Action |
| --- | --- |
| `1` | Move (U=up, D=down, L=left, R=right) |
| `2` | Try to open a door in an adjacent square |
| `3` | Search adjacent squares for traps and secret doors |
| `4` | Equip a weapon owned in your inventory |
| `5` | Attack a monster you are facing |
| `6` | Look: print an 11×11 area of numbers |
| `7` | Print the **paper tape** save record |
| `8` | Use a class-appropriate spell |
| `9` | Buy one magic point for 50 gold |
| `0` | Wait; enemies may attack |
| `10` | See your statistics and equipment |
| `11` | Buy an extra hit point for 200 gold |
| `12` | Eat spare food to heal |
| `98` | Quit to BASIC |
| `99` | Help |

In the numeric look view: **9** is you, **0** floor, **1** wall (and unrevealed secret door), **4** closed door, **5** monster, **6** gold, **7** a strength bonus and **8** a constitution bonus. Traps are **2** in the data but look like floor (**0**) until encountered or searched.

The game uses restored and simplified turn-based rules; combat, spells and equipment should **not** be assumed identical to the entire unfinished 1977 program.

## Saving and restoring

There is deliberately **no machine-specific disk save command**. Choose `7` to print a record with your character, random seed, coordinates, inventory, active monster and all 26 map rows. Save this output in a text file or copy it to paper. For later play, start the program and answer `O` at the first prompt, then enter the printed values, including **all 26 rows** of **26 digits** each. This has been tested with a stored sample record in trs80gp.

This is a small tribute to paper-tape workflows and a portable fall-back; it is intentionally more manual than saving to a TRS-80 disk. A separate optional, platform-specific disk save may be added later without removing this text-only approach.

## Memory and BASIC dialect notes

- Program file has 8.3-compatible name `DND1PLAY.BAS` and includes `REM` comments throughout.
- The game uses ordinary BASIC `DATA`, `READ`, `RESTORE`, `PRINT`, `INPUT`, string functions, arrays and subroutines. No `POKE`, `PEEK`, direct screen addresses or character ROM are required.
- The one Model III-oriented initialisation is `CLEAR 3000`, reserving BASIC string space for the stored dungeon rows. Other BASIC dialects may use a different way of assigning string space.
- Map strings are stored in five `DATA` chunks of at most **156 characters per dungeon**. Model III BASIC's rejection of `RESTORE <line number>` was confirmed during testing, so the loader relies on portable sequential `RESTORE` and `READ` instead.
- The original external files and Roy's earlier port remain untouched. The newer game is a **reconstruction**, not a byte-for-byte or rules-exact repair.
