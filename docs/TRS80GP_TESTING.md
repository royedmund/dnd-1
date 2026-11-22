# Tested playable edition — 22 November 2026

**Emulator:** George Phillips' **trs80gp 2.5.8**, **TRS-80 Model III ROM BASIC**, automatic `.BAS` loading. Unlike the historical LDOS LBASIC port, the **new** [`DND1PLAY.BAS`](../DND1PLAY.BAS) was exercised and produced actual screen output. **LDOS 5.1 LBASIC and physical hardware are still untested.**

Observed passing scenarios:

1. **Dungeon 1 Fighter:** character creation, 3d6 rolls, equipment shopping, the command prompt, numeric `6=LOOK` map, `99=HELP` and `98=QUIT` (clean return to BASIC).
2. **Movement/save:** movement to another square, search, player status, `7=SAVE` printing all 26 mutated map rows, then clean exit.
3. **Dungeon 2 Wizard:** monster encountered by moving left, `8=USE MAGIC` attacks, monster counterattack and a game-over path.
4. **Dungeon 7:** the distinct `DND1TRS.BAS` embedded map loaded into the reconstructed program and reached its command prompt.
5. **Old-tape restore:** chose `O`, entered hero data, seed, inventory and all 26 complete dungeon rows; the map and player position were restored, `99=HELP` worked and quit returned to BASIC.
6. **Compatibility:** `RESTORE 20` produced `?SN Error` in Model III ROM BASIC; the new loader uses only `RESTORE` and `READ`. String-space allocation and loading were also verified after adding `CLEAR 3000`.

Static tests: run `python3 tests/check_playable.py` in a checkout. It verifies BASIC line numbers/branches, the 35 embedded map chunks, map contents and the preserved source files.

**Scope limitation:** These are representative scenarios, not full dungeon completions or a test of every original historical feature. The new source is a playable, independently reconstructed game, not a verified rules-identical original.

---

# Testing DND#1 with George Phillips' trs80gp

Primary reference: https://48k.ca/trs80gp.html

This protocol began as a plan for the archival port. The new standalone reconstruction has since been run in Model III ROM BASIC; see the verified results above. The historical `DND1TRS.BAS` remains untested as a fully working game.

## Recommended baseline

- Platform: **TRS-80 Model III**, 48 KB initially.
- Operating system: use TRS80gp's included **LDOS 5.3.1** to establish a repeatable baseline, then compare against **LDOS 5.1** when an appropriate boot image is available.
- BASIC: **LBASIC** under LDOS. Do not mistake ROM BASIC execution for a valid LBASIC compatibility test.
- Display: keep the game text-only and avoid machine-specific full-screen display effects in the eventual common edition.
- Historical terminal target: the Teletype Model 33 experience should be treated as a separate text/serial-output compatibility test; the DEC host is not confirmed.

The current TRS80gp documentation describes Model III/48K as the default model and offers a bundled LDOS 5.3.1 disk.

### Boot the emulator

```text
trs80gp -m3 -ld
```

At the LDOS prompt, start LBASIC using the version's documented invocation. The current `DND1TRS.BAS` is an **unfinished archival port**; it is expected to fail until repaired in a separate working copy.

### Transfer BASIC listings

For small experiments, TRS80gp documents **Edit → Paste** and saving a BASIC program from the emulator. For the 1,292-line / roughly 32 KB legacy listing, prefer a tested file-import workflow to avoid keyboard-buffer or timing problems.

The emulator's built-in utilities floppy has `IMPORT2` / `EXPORT2`; they require **FreHD emulation** to be enabled. One useful configuration is:

```text
trs80gp -m3 -ld -d1 :lu3 -frehd
```

`IMPORT2 -n` translates host line feeds to TRS-80 carriage returns when needed. Confirm the resulting file format before trying to `LOAD` or `MERGE` it in LBASIC; plain ASCII and tokenised LBASIC are not interchangeable. If needed, use the emulator's Edit → Paste facility to enter the source as BASIC program lines.

TRS80gp supports scripted input (`-i`, `-ib`, `-cmd`), batch mode, screen copying, memory dumps and debugging. These can underpin automated acceptance tests once we have a loadable program.

## First interactive test cases

| Test | Action | Expected / issue to verify |
| --- | --- | --- |
| T01 | Boot Model III with LDOS and start LBASIC | Emulator boots consistently |
| T02 | Import a new *working copy* with only known parse fixes | Listing imports without a syntax error at 00404 |
| T03 | `RUN`; answer instructions question and select `NEW` | Startup advances to character creation |
| T04 | Enter `SHAVS` for the archival player-name gate | Character creation progresses; later remove gate from normal mode |
| T05 | Choose Fighter, Cleric or Wizard | Attributes and equipment rules function for each |
| T06 | Select each of six preserved external maps and the seventh embedded map | Correct 26×26 map appears for each selection |
| T07 | Issue movement, look, search and door commands | Coordinates remain valid; walls and doors behave consistently |
| T08 | Exercise combat and magic | No missing variables, arrays or invalid branches |
| T09 | Save; restart; load | Whole player and dungeon state restored accurately; **not implemented yet** |
| T10 | Replay a fixed transcript via scripted input | Repeatable output except deliberately random rolls |

## What to capture

For each test save: TRS80gp version, ROM, OS/BASIC versions, RAM size, exact source commit, command/input sequence, observed screen or transcript, and any error with BASIC line number.

Avoid editing archival `DND.BAS`, `DND1TRS.BAS` or dungeon files during tests.

## Emulator limitations / interpretation

An emulator may accept some code which a physical Model III cannot fit in 48 KB. We should also validate RAM use and compatibility separately. The development source may target a less constrained environment first, while a 48K edition remains an optional later goal.

See `docs/SOURCE_AUDIT.md` for initial static results.
