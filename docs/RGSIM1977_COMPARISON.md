# Comparison: Richard Garriott Simulator 1977 vs DND#1 restoration

**Reference:** https://toqc.com/rgsim1977.html (provided by the project maintainer)

**Assessment date:** 25 November 2026

## Verification scope and limits

The external simulator page could not be loaded by the available web access (fetch disabled); a search for its exact title and URL did not produce source code or dependable mechanics documentation. Consequently **no side-by-side simulator run, deterministic seed comparison, or gameplay-parity claim is made**. Do not treat the external simulator as the historical original by default: it is a separate implementation until its provenance and code are checked.

A static review of repository source files **DND.BAS** (historical transcription), **cdc/DND1CDC.BAS** (repaired CDC source), and **DND1PLAY.BAS** (Model III reconstruction) was completed. Its confirmed findings are as follows:

| Area | Our TRS-80 playable adaptation | Historical CDC edition | External simulator |
| --- | --- | --- | --- |
| Source scope | Self-contained reconstructed game, not line-for-line historical original | Repaired source derived from historical listing | Not inspected |
| Dungeon content | Seven embedded maps (six surviving external grids plus seventh from older TRS port) | Six historical external dungeon files | Unknown |
| Classes | Fighter, Cleric and Wizard | Historical class mechanics retained in source restoration | Unknown |
| Movement and view | Numbered commands, 11×11 numeric dungeon view | Historical teletype interaction | Unknown |
| Doors, search, traps, combat and magic | Included in reconstructed command set | Historical implementations in CDC source | Unknown |
| Save/restore | Printed paper-tape-style record entered manually | CDC numbered-file / GMSTR mechanisms | Unknown |
| Runtime testing | Model III ROM BASIC tests documented in README | Static checks only; CDC runtime untested | Not run |

## Uploaded listing review — 25 November 2026

The maintainer supplied a 655-line BASIC listing labelled as the simulator's source. **The listing itself identifies as the project's PDP-11/RSTS/E BASIC-PLUS adaptation**, including `REM RECREATION PORTED FROM THE MODEL III EDITION` and `REM RESTORATION BY ROY ANTAW + CHATGPT OPENAI`. It closely follows `pdp11/DND11.BAS` in this repository, with additional browser-edition repair notes and input checks. Its origin as the independent TOQC simulator's source is **not established**. Treat it as an enhanced derivative of our PDP-11 port unless independent provenance is provided.

### Static checks completed on the supplied listing

- 655 numbered lines, no duplicate line numbers.
- 182 quoted DATA rows grouped into 7 maps of 26 rows × 26 digits; all map rows have the expected 26-digit shape.
- Map codes span 0–8. Map 7's preferred entrance at row 1, column 12 is a wall and requires the program's fallback scan.
- The code contains fighter/cleric/wizard character creation, seeded random rolls, equipment purchasing, map movement, doors, traps, combat, healing/bolt/reveal magic, printed save/restore and monster encounters.
- Compared with the repository PDP-11 version, visible additions include `REM BROWSER EDITION` and stronger validation for restored inventory, map rows and active-monster position.
- **Not executed:** no DEC BASIC-PLUS interpreter or external simulator runtime was available. These are structural/source inspections, **not passed gameplay tests**.

### Follow-up engineering checks

- Compare the uploaded browser-edition modifications with the repository's PDP-11 source line by line before merging any fixes.
- Test all seven entrance placements, particularly the fallback for dungeon 7, under a real interpreter.
- Exercise all restore validation branches, especially inventory/weapon consistency and saved active-monster coordinates.
- Resolve whether the actual TOQC site hosts this derivative or another implementation, then conduct a genuine independent comparison.

## Repeatable side-by-side test protocol (pending)

1. Record external simulator version/date, platform, instructions and any available source or downloadable package.
2. Start a new character in both programs. Capture the six attributes, class choices, starting resources, shop inventory and initial map.
3. Choose the same dungeon number (1–6) and seed *only if* both implementations expose equivalent seed handling; otherwise use comparable test scenarios rather than expecting exact random sequences.
4. Compare the player's starting position and initial printed view, then perform controlled sequences: move into wall, move along corridor, open a door, search for a secret door/trap, encounter enemy, fight, cast spell, consume food, buy points, die and quit.
5. Check gold, experience, food, magic points, hit points and character progression after each step. Record first divergence with screenshots/printed transcript.
6. Exercise save/restore (if external version supports it), and compare terminal text layout, turn order, timing, randomness and game-over handling.
7. Categorize differences as **historical fidelity**, **intentional Model III adaptation**, **bug**, or **unverified due to missing simulator details**.

## Next action

Obtain direct access to the external simulator or a capture of its complete gameplay, source files, or screenshots/transcripts; then execute the protocol and document observed mismatches. Until then there is **no verified head-to-head result**.
