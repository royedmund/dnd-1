# Identifying the BASIC dialect and host behind DND#1

**Research note — 22 November 2026**

## Finding

**High confidence: Control Data Corporation (CDC) BASIC, in the Version 2-compatible language family.**
**Likely host: a CDC CYBER or CDC 6000-series time-sharing system.**

The surviving historical listing is **not consistent with unmodified DEC RSTS/E BASIC-PLUS**. The exact CDC hardware model, operating system (SCOPE, KRONOS, NOS, or other), and the exact BASIC compiler revision **cannot be proved from the code alone**. This identification does **not** diminish the value of a separate PDP-11 RSTS/E BASIC-PLUS port, or the primary TRS-80 Model III recreation.

## Strongest evidence: exact syntax matches to CDC's published manual

The [CDC BASIC Language Version 2 Reference Manual, document 19980300B (October 1974)](https://bitsavers.trailing-edge.com/pdf/cdc/cyber/lang/basic/19980300B_BASIC_Language_Version_2_Reference_Nov74.pdf) explicitly documents **all** the distinctive constructs below, including near-exact working examples.

| Historical DND#1 source | CDC BASIC Version 2 manual explanation |
| --- | --- |
| `00100 BASE 0` | The `BASE` statement declares zero- or one-origin arrays, with a literal example `100 BASE 0`. |
| `00160 LET J9=RND(CLK(J9))` | `CLK(x)` reads clock time; the random-number section even recommends `RND(CLK(0))` to initialise the sequence. |
| `00210 FILE #1="DNG1"` | The documented `FILE #1 = "OLDM"` syntax assigns a file ordinal to a name. |
| `00220 FILE #2="DNG2",#3="DNG3",...` | CDC BASIC allows several numbered file assignments in one `FILE` statement. |
| `00230 RESTORE #4` | `RESTORE #ne` rewinds a numbered file's data pointer. |
| `01440 READ #D,D(M,N)` | The documented `READ #ne, variable` format reads numeric/string data from a file. |
| `06620 WRITE #7,D` and `11080 WRITE #D2,D(M,N)` | The documented `WRITE #ne, expression` format writes a binary-format data item to a file. |

**Why this is compelling:** it is not just a generic `PRINT`/`GOTO` program. The combination of `BASE 0`, numbered `FILE` declarations, numbered `RESTORE` and file `READ`/`WRITE`, plus `RND(CLK(...))`, matches the CDC compiler reference remarkably closely. The CDC manual's preface says this BASIC compiler ran on **CYBER 70, CYBER 170 and CDC 6000-series** machines and was available under **SCOPE, KRONOS and NOS**. (The 1974 edition documents a **BASIC 2.1** compiler derived from **Version 2.0**.)

Roy's supplied **DEC BASIC-PLUS Language Manual for RSTS/E** (December 1981, publication AA-2623D-TC) describes an `OPEN`-based file interface, not the file-ordinal `FILE #1="..."` statement in the original listing. Do not assume this code would run unchanged under RSTS/E.

## Documentary disagreement

- [Richard Garriott's DND #1 Contest announcement (Shroud of the Avatar, 16 April 2014)](https://www.shroudoftheavatar.com/?p=39149) describes a **PDP-11-type minicomputer** accessed from the school over an acoustic modem.
- [The CRPG Addict, Dungeons and Dragons #1 (2021)](https://crpgaddict.blogspot.com/2021/07/game-421-dungeons-and-dragons-1-1977.html) explicitly revises that conventional attribution to a **CDC-6000**, crediting research by El Explorador de RPG.
- [El Explorador de RPG's DND #1 historical entry](https://exploradorrpg.wordpress.com/juegos/dnd-1/) names a **CDC CYBER**.
- The [independent BASIC transcription by Bussiere](https://gist.github.com/bussiere/11137495) retains a printout header: **79/02/28, 19:27:34, PROGRAM DND1**. This is consistent with a surviving **1979 source printout**, not necessarily with the date the program was first written (usually given as 1977).
- [A 2014 classiccmp PDP-11 BASIC investigation](https://classiccmp.org/mailman3/hyperkitty/list/test-drb%40ccmp.vtda.org/latest?count=200&page=62) records a developer unable to run the original `FILE #1="DNG1"` command under a PDP-11 BASIC emulator. The CDC manual explains the discrepancy.

## What can and cannot be named precisely

| Question | Current conclusion | Confidence |
| --- | --- | --- |
| BASIC family | **CDC BASIC** rather than an unmodified DEC RSTS/E BASIC-PLUS | **High** |
| Compatible language version | **CDC BASIC Version 2.0/2.1 syntax**, as documented in 1974 | **High** |
| Exact BASIC compiler revision actually used | **Unknown**; may have been a later backward-compatible release | **Unresolved** |
| Computer family | **CDC CYBER / CDC 6000** more probable than PDP-11 | **High**, but exact model unverified |
| Particular computer, e.g. CDC 6600 versus a CYBER model | **Unknown** | **Unresolved** |
| Operating system | SCOPE, KRONOS, NOS or another supported CDC installation **not distinguishable** | **Unresolved** |
| Input/output equipment | School teletype and acoustic-modem link as reported; precise terminal subtype not source-proven | **Strong historical support** |

**Technical note:** CDC BASIC is documented as a *compiled* language within the operating system's time-sharing environment, even though it was conversationally accessed from a terminal. Calling it a particular ROM BASIC or simply “PDP-11 BASIC-PLUS” would be misleading.

## Implications for this repository

1. **Historical originals:** keep `DND.BAS`, `DND1TRS.BAS`, the PDF and all dungeon files unchanged.
2. **TRS-80 Model III:** `DND1PLAY.BAS` remains the principal tested reconstruction.
3. **PDP-11 / RSTS/E:** `pdp11/DND11.BAS` remains an **experimental modern target port**, not a claim of the original interpreter. It still needs real BASIC-PLUS runtime testing.
4. **Potential later historic target:** consider a **CDC BASIC Version 2-compatible** edition, with matching file syntax, if a suitable CDC CYBER/6000 emulator and BASIC environment can be assembled. Do not label it tested before execution.

*This is a source-based attribution supported by historical documentation, not an identification from an original system banner, binary header, compiler version line, or installation log.*
