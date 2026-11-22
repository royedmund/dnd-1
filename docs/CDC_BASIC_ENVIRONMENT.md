# CDC CYBER / CDC 6000 BASIC Version 2 restoration

**Status: complete first-pass CDC BASIC source and dungeon-data initializer; static checks passed; no actual CDC runtime test yet.** This is a source-faithful repair of the surviving historical program, distinct from the redesigned and emulator-tested TRS-80 Model III game.

## Project files

| File | Purpose |
| --- | --- |
| [`DND1CDC.BAS`](../cdc/DND1CDC.BAS) | Full repaired, **1,233-line** CDC BASIC Version 2-style historical game, keeping original line numbers and gameplay systems |
| [`MAKEFILE.BAS`](../cdc/MAKEFILE.BAS) | Converts the six historic 26×26 dungeon grids to CDC **binary numbered files** using native `FILE` / `READ` / `WRITE` |
| [`cdc/data/DNG1.txt` through `DNG6.txt`](../cdc/data/DNG1.txt) | Six archival-format text matrices retained for inspection and reproducibility; **not** directly loadable with `READ #` |
| [`tests/check_cdc.py`](../tests/check_cdc.py) | Source/line-limit/reference checker and data identity test |
| [`CDC_REPAIRS.md`](CDC_REPAIRS.md) | Line-by-line restoration changes, remaining bugs, known unverified behaviour |
| [`ORIGINAL_PLATFORM.md`](ORIGINAL_PLATFORM.md) | Research behind the CDC identification |
| [`DND.BAS`](../DND.BAS) | **Unmodified** original-version transcription |

**Important:** the original `DND3` is copied as **`DNG3`** in the new CDC data folder. The original file name is left as received. The seventh, distinct dungeon from Roy's earlier TRS-80 conversion is intentionally **not** presented as part of Garriott's six-dungeon source; that map remains in the TRS-80 restoration.

## Real CDC time-sharing environment

The [CDC BASIC Language Version 2 Reference Manual (document 19980300 B, October 1974)](https://bitsavers.trailing-edge.com/pdf/cdc/cyber/lang/basic/19980300B_BASIC_Language_Version_2_Reference_Nov74.pdf) applies to the **CYBER 70 models 72–74, CYBER 170 models 172–175, and 6000-series systems**. The language could be used under contemporary CDC software environments including **SCOPE/INTERCOM, KRONOS and NOS**. CDC BASIC V2 was a compiler with a conversational terminal workflow; it was not the DEC RSTS/E BASIC-PLUS interpreter or the microcomputer ROM BASIC used in the separate ports.

A school or other remote user could connect over a telephone/acoustic modem to a terminal multiplexer, enter a user ID, and operate an interactive CDC session through a **printing TTY** or compatible CRT. One example in the official manual explicitly identifies **Model 33 or Model 35 teletypewriters**. On KRONOS/NOS, the example log-in transcript includes `RECOVER /SYSTEM:BASIC`, prompts for `OLD, NEW, OR LIB FILE`, a `READY.` prompt, and BASIC commands such as `LIST` and `RUN`. Under SCOPE, **INTERCOM** provides interactive log-in and an `EDITOR` / `FORMAT,BASIC` / compile-run workflow. These are **documented examples**, not verified transcripts from Garriott's original school installation.

The **CDC 6600**, a member of the 6000 series, is a representative photograph for the README; **there is no evidence that DND#1 ran specifically on a 6600**. Also, seeing an ASR 33 image does not establish the exact terminal used in this installation.

### CDC BASIC Version 2 source considerations

- **One line-numbered statement per source line**, with the manual's **72-character statement maximum**. Both new CDC programs have been checked against a conservative 72-character **whole line** limit.
- `BASE 0` gives the original zero-based numeric arrays.
- `FILE #1="DNG1"` and `FILE #7="GMSTR"` associate numbered file ordinals with host files. File names are at most seven alphanumeric characters in this language.
- `READ #D,D(M,N)` **reads CDC binary data**. Merely copying a modern text file with rows of digit tokens into the user account will **not** satisfy this requirement.
- `WRITE #F,V` creates CDC-native binary sequential records/data. The accompanying initializer writes 26 × 26 = 676 values for **each** of six dungeons.
- `RESTORE #F` rewinds a numbered binary file; `RESTORE` without `#` rewinds internal `DATA` statements.
- `RND(CLK(0))` follows the manual's documented clock-based random seed example.
- `GMSTR` is a **writable game save file**, distinct from the archival text-format `GMSTR` in the repository.

## First-time installation / setup on a CDC system

The exact host command sequence depends on your CDC **OS, site procedures and terminal connection**. This is a conceptual runbook; the CDC language and file commands are documented, but these steps have **not yet been performed on a CDC machine or emulator**:

1. Transfer **`cdc/MAKEFILE.BAS`** and **`cdc/DND1CDC.BAS`** to your CDC user area as BASIC source, using your installation's text editor, terminal/paper-tape reader or file-transfer process.
2. Enter the BASIC facility appropriate to the installation. For a **KRONOS/NOS** system, see the manual's sample `RECOVER /SYSTEM:BASIC` terminal session. A **SCOPE/INTERCOM** system uses different editor and run commands.
3. Before starting the main game, compile/run **`MAKEFILE.BAS`**. **It will overwrite/reset DNG1–DNG6 and GMSTR.** Only enter **YES** when you are happy to initialise fresh game data.
4. The initializer uses `WRITE #1` through `WRITE #6` to create the six binary dungeon files in the native format expected by `DND1CDC.BAS`. It also starts a new `GMSTR` save file.
5. Run **`DND1CDC.BAS`**, choose **NEW** the first time, select dungeon **1–6**, generate a character and play.
6. To save, select the original game's **command 7**. This writes the game state to `GMSTR`. **Only choose OLD after a complete saved state exists.** The initializer's `GMSTR` header alone is not a usable saved game.
7. Record actual compile/run diagnostics (including source line number). Investigate any interpreter/compiler differences before claiming hardware compatibility.

**Data safety:** `MAKEFILE.BAS` is deliberately destructive with respect to seven named CDC user files; do not run it over a valuable pre-existing game. Copy the originals or use a temporary user account.

## What's verified

- All six source grids have exactly **676** cell values in 26 rows, with codes **0–8**.
- The seven new `cdc/` text assets (source plus six matrices) and initializer are internally consistent.
- Every numeric direct `GOTO`, `GOSUB` and `THEN` target in the main CDC program exists.
- No duplicate or out-of-order BASIC statement numbers; no non-`REM` unmatched quotation marks.
- No BASIC source lines longer than 72 characters.
- The new source keeps the original six dungeon choices, classes, original shop, monster data, equipment, spells, fighting, saving and loading logic (with documented source repairs).
- It has **not** been compiled by a CDC BASIC 2.0/2.1 compiler. Therefore it is a **complete first-pass code and data restoration**, **not a proven finished playable CDC binary**.

For reproducing the checks: `python3 tests/check_cdc.py` in a cloned repository.

## References

- [CDC BASIC Language Version 2 Reference Manual (1974)](https://bitsavers.trailing-edge.com/pdf/cdc/cyber/lang/basic/19980300B_BASIC_Language_Version_2_Reference_Nov74.pdf)
- [CDC 6000-series computer family](https://en.wikipedia.org/wiki/CDC_6000_series)
- [Richard Garriott's original DND #1 recollection (2014)](https://www.shroudoftheavatar.com/?p=39149)
- [Source-based BASIC and machine identification](ORIGINAL_PLATFORM.md)
