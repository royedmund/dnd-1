# Comparison: Richard Garriott Simulator 1977 vs DND#1 restoration

**Reference:** https://toqc.com/rgsim1977.html (provided by the project maintainer)

**Assessment date:** 25 November 2026

## Verification scope and limits

The external simulator page was not available for a direct gameplay comparison through the available web access. Consequently **no side-by-side simulator run, deterministic seed comparison, or gameplay-parity claim is made**. The supplied site notes identify the browser edition as a JavaScript interpreter running an adapted copy of this project's PDP-11 listing, rather than a separately authored historical game. The page itself has not been independently executed here.

A static review of repository source files **DND.BAS** (historical transcription), **cdc/DND1CDC.BAS** (repaired CDC source), and **DND1PLAY.BAS** (Model III reconstruction) was completed. Its confirmed findings are as follows:

| Area | Our TRS-80 playable adaptation | Historical CDC edition | External simulator |
| --- | --- | --- | --- |
| Source scope | Self-contained reconstructed game, not line-for-line historical original | Repaired source derived from historical listing | Maintainer-supplied listing describes a browser-adapted version of this project's PDP-11 BASIC-PLUS port |
| Dungeon content | Seven embedded maps (six surviving external grids plus seventh from older TRS port) | Six historical external dungeon files | Seven maps in supplied BASIC listing |
| Classes | Fighter, Cleric and Wizard | Historical class mechanics retained in source restoration | Fighter, Cleric and Wizard in supplied source/notes |
| Movement and view | Numbered commands, 11×11 numeric dungeon view | Historical teletype interaction | Command 1 movement / command 6 numeric local map, per supplied notes |
| Doors, search, traps, combat and magic | Included in reconstructed command set | Historical implementations in CDC source | Included in supplied BASIC listing; runtime unverified |
| Save/restore | Printed paper-tape-style record entered manually | CDC numbered-file / GMSTR mechanisms | Paper-tape transcript with browser **Save transcript** facility, according to supplied notes |
| Runtime testing | Model III ROM BASIC tests documented in README | Static checks only; CDC runtime untested | Not run |

## Uploaded listing review — 25 November 2026

The maintainer supplied a 655-line BASIC listing labelled as the simulator's source. **The listing itself identifies as the project's PDP-11/RSTS/E BASIC-PLUS adaptation**, including `REM RECREATION PORTED FROM THE MODEL III EDITION` and `REM RESTORATION BY ROY ANTAW + CHATGPT OPENAI`. It closely follows `pdp11/DND11.BAS` in this repository, with additional browser-edition repair notes and input checks. The subsequently supplied notes explicitly describe this as a browser-interpreted, repaired edition of our PDP-11 listing; page authorship and live runtime remain unverified independently. Treat it as a derivative port, not an independent source against which historical fidelity can be established.

### Static checks completed on the supplied listing

- 655 numbered lines, no duplicate line numbers.
- 182 quoted DATA rows grouped into 7 maps of 26 rows × 26 digits; all map rows have the expected 26-digit shape.
- Map codes span 0–8. Map 7's preferred entrance at row 1, column 12 is a wall and requires the program's fallback scan.
- The code contains fighter/cleric/wizard character creation, seeded random rolls, equipment purchasing, map movement, doors, traps, combat, healing/bolt/reveal magic, printed save/restore and monster encounters.
- Compared with the repository PDP-11 version, visible additions include `REM BROWSER EDITION` and stronger validation for restored inventory, map rows and active-monster position.
- **Not executed:** no DEC BASIC-PLUS interpreter or external simulator runtime was available. These are structural/source inspections, **not passed gameplay tests**.

### Source-level concern: dungeon entrance fallback order

In the supplied listing, `7100` establishes `GY=1`, `GX=12`; `7120` returns if that tile is floor (`0`). If it is not, lines `7130`–`7160` scan for floor tiles. However, line `7145` reads:

```basic
7145 IF GX <> 12 OR GY <> 1 THEN 7160
```

Because `GX` and `GY` are still `12` and `1` throughout that scan, the condition is always false, so line `7150` updates the entrance to **every** floor tile visited rather than the first. The result is the **last floor tile in scan order**, not the nearest or first valid floor. Consequently, the existing report's previous conclusion that this fallback never selects an entrance was incorrect; the more precise finding is that it **chooses the last scanned floor tile**. For maps 2, 3, 5 and 7, this is a valid but unintended entrance position; for maps 1, 4 and 6 the preferred entrance is already open. This is a code-level observation. The supplied publisher's notes say that the fallback search **completes its loops**; that is compatible with choosing the last rather than the first floor. Whether this is regarded as a defect or deliberate behaviour requires confirmation with the edition's author. Runtime behaviour remains untested here.

Suggested correction if the intention is *first available floor*: immediately `RETURN` upon finding a floor, instead of continuing the scan:

```basic
7130 FOR YY = 1 TO 24 \ FOR XX = 1 TO 24
7140 IF VAL(MID(D$(YY), XX + 1, 1)) <> 0 THEN 7160
7150 GY = YY \ GX = XX \ RETURN
7160 NEXT XX \ NEXT YY
7170 PRINT "THIS DUNGEON HAS NO ENTRANCE" \ END
```

This correction has **not been applied** to either executable BASIC version; it needs interpreter testing and a design decision about desired entrance selection.

### Provenance and gameplay comparison limitations

The uploaded listing retains the project's own title, author credits, seven maps and PDP-11 BASIC-PLUS structure. Its accompanying publisher notes expressly say the webpage runs the editable listing under a purpose-built JavaScript interpreter. This is **publisher-provided implementation information, not an independently observed browser runtime test**. It does not establish independent historical fidelity. It cannot substantiate an independent head-to-head parity claim.

Other source-level checks to run before importing repairs: confirm the typed `RUN` restart behaviour in BASIC-PLUS, exercise all old-tape validation paths, and compare encounter timing and character progression against the historical CDC source. The supplied port's combat and item formulas should not be assumed historically exact.

### Follow-up engineering checks

- Compare the uploaded browser-edition modifications with the repository's PDP-11 source line by line before merging any fixes.
- Test preferred and fallback entrance selection for **all seven** maps (especially maps **2, 3, 5 and 7**) under a real interpreter; decide whether the first or last passable floor should be selected.
- Exercise all restore validation branches, especially inventory/weapon consistency and saved active-monster coordinates.
- Resolve whether the actual TOQC site hosts this derivative or another implementation, then conduct a genuine independent comparison.

## Publisher-supplied notes and credit (25 November 2026)

**Source of this section:** the project maintainer supplied the `Playing DND #1`, `Repairs in this edition`, `Console photograph` and `Interpreter scope` notes attributed to [Richard Garriott Simulator 1977 (toqc.com)](https://toqc.com/rgsim1977.html). These are **publisher claims transcribed/summarised from supplied notes**, not results of our own browser execution.

### Playing the TOQC browser edition

Choose **N** for a new game, **0** for the standard random seed, a dungeon **1–7**, a character name and a class. Fighter has the greatest potential hit points; wizard starts with five magic points. Choose **0** in the equipment shop to enter the dungeon. Command **6** displays the local numeric map (`9` marks the player), command **1** then U/D/L/R moves, command **3** searches, and **99** lists commands.

Command **7** produces a printed paper-tape-style save. The browser's **Session → Save transcript** stores a transcript. To restore, restart, select **O** and re-enter character fields, the six separate attributes, pack contents, monster state and each saved map row. **Save transcript is a feature of TOQC's browser Session panel, not a command supported by the standalone Model III/PDP-11 BASIC programs.**

### Repairs reported by the publisher

- Paper-tape restore retains a random seed/state of **zero**; validates inventory digits, tile codes, coordinates, equipped weapon and active monster information.
- Fractional dungeon numbers and item selections are rejected before array access; lowercase class letters and lowercase movement direction words are accepted.
- Dungeon entrance fallback loops complete; **Y** after death restarts a fresh game; equipment prices are initialised once.
- These are *reported repairs in the browser edition*. We have not established that all were defects in the repository versions or rerun the publisher's tests.

### JavaScript interpreter scope

According to the supplied notes, the browser executes the numbered BASIC listing with a **program counter, subroutine stack, loop stack and DATA cursor**. It implements the statements, one-dimensional arrays, functions and `RUN` replay behaviour used by `DND11`. It uses **JavaScript numeric values and browser keyboard input**, functions offline and does not require an emulated PDP-11 or disk image. A successful browser run would therefore **not** be proof of DEC RSTS/E BASIC-PLUS interpreter compatibility.

### Attribution and rights

- **Richard Garriott** — original DND#1 game (1977).
- **Roy Antaw and ChatGPT (OpenAI)** — TRS-80 restoration and derived PDP-11 BASIC-PLUS listing, as acknowledged by the publisher.
- **Richard Garriott Simulator 1977 at toqc.com** — browser interpreter/adaptation, edition repairs, instructions and Session transcript functionality, as described in the supplied notes. The publisher's individual name was **not supplied**; do not invent one.
- **TedColes** — publisher-credited photographer of the adapted Teletype console image, based on [the original Wikimedia Commons Teletype 33 ASR photograph](https://commons.wikimedia.org/wiki/File:Teletype_33_ASR.jpg). The publisher describes its console image as **cropped and masked**, with **[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)** attribution/share-alike licensing. This credit applies to **their adapted console photograph**, not automatically to the separate ASR 33 photograph currently present in this repository.
- The supplied notes end with the incomplete text `Source archive lice`. No complete archive licence statement was provided; **no conclusion is made about the simulator source archive's licence**.

## Repeatable side-by-side test protocol (pending)

1. Record external simulator version/date, platform, instructions and any available source or downloadable package.
2. Start a new character in both programs. Capture the six attributes, class choices, starting resources, shop inventory and initial map.
3. Choose the same dungeon number (1–6) and seed *only if* both implementations expose equivalent seed handling; otherwise use comparable test scenarios rather than expecting exact random sequences.
4. Compare the player's starting position and initial printed view, then perform controlled sequences: move into wall, move along corridor, open a door, search for a secret door/trap, encounter enemy, fight, cast spell, consume food, buy points, die and quit.
5. Check gold, experience, food, magic points, hit points and character progression after each step. Record first divergence with screenshots/printed transcript.
6. Exercise save/restore (if external version supports it), and compare terminal text layout, turn order, timing, randomness and game-over handling.
7. Categorize differences as **historical fidelity**, **intentional Model III adaptation**, **bug**, or **unverified due to missing simulator details**.

## Next action

Use the publisher's interpreter and provided listing to execute repeatable browser gameplay scenarios, then compare the transcripts and results with our Model III and original CDC versions. The developer notes provide the interpreter design, but not an independent full browser run or historical rules verification. Until then there is **no verified head-to-head result**.
