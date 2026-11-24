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
