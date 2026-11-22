# Bootable Model III LDOS 5.3 HFE with DND#1 and TTY300

**Image:** [`disks/LDOS53_DND1PLAY_TTY300_ModelIII.hfe`](../disks/LDOS53_DND1PLAY_TTY300_ModelIII.hfe)  
**ZIP containing image and both BASIC sources:** [`disks/LDOS53_DND1PLAY_TTY300_ModelIII.zip`](../disks/LDOS53_DND1PLAY_TTY300_ModelIII.zip)

## What's on the disk?

This is a **40-track, single-sided, double-density LDOS 5.3.0** Model III boot disk, created from a **copy** of the user's original `ldos53_dsk.hfe`. It contains native saved/tokenised LBASIC files:

| LDOS file | Contents | Lines |
| --- | --- | ---: |
| `DND1PLAY/BAS` | Self-contained DND#1 game with all seven dungeons | 449 |
| `TTY300/BAS` | Model III RS-232 300-baud printing terminal for PiDP-11/70 | 42 |

The LDOS bootstrap, system files, `BASIC/CMD`, `BASIC/OV1` through `BASIC/OV4`, and other utility programs are retained. Only two **optional help/reference files** were removed: `DOS/HLP` and `BASIC/HLP`. That recovers **20 granules of 1.5 KiB = 30 KiB** of raw disk allocation. It does not remove the BASIC interpreter.

## Running

Use the HFE directly with **Gotek/FlashFloppy** or a compatible emulator.

At the LDOS command prompt:

```text
BASIC
```

At the LBASIC prompt, for the game:

```text
LOAD "DND1PLAY/BAS"
RUN
```

For the serial terminal instead:

```text
LOAD "TTY300/BAS"
RUN
```

The terminal sets up the Model III UART at **300 baud / 8N1** using direct I/O port access. Do not run the LDOS `RS232T/DVR` on the same port simultaneously. Use a **proper RS-232-voltage USB adapter** and **null-modem wiring**, not a TTL-only adapter. See [TTY300 setup notes](TTY300_SETUP.md).

To switch between programs, return to the BASIC prompt and `LOAD` the other program. Since `DND1PLAY` contains game data inside its BASIC listing, no external dungeon files are needed for the Model III edition.

## Integrity and validation

The source image was copied, and both programs were entered and saved using **George Phillips' trs80gp**. The final file was modified at the disk-sector level to remove the two optional help files.

Validation of the finished HFE:

- 720 sectors decoded successfully; edited directory-sector data and CRCs verified
- The original boot sector and LDOS program sectors were preserved
- Directory and allocation map mark `DOS/HLP` and `BASIC/HLP` as removed, leaving **21 free granules** (31.5 KiB of raw granule space)
- File-stream parsing confirmed a **complete 449-line `DND1PLAY/BAS`**, from source line 10 to line 9430, with valid end marker
- File-stream parsing confirmed a **complete 42-line `TTY300/BAS`**, from source line 10 to line 420, with valid end marker
- The user's original HFE was **not modified**

**Limitations:** the final trimmed HFE has **not been independently booted on physical hardware**. The source LDOS disk was booted in the emulator; boot and file integrity have been checked on the final image, but real hardware execution and RS-232 communication still need verification. The DND program has previously been exercised under Model III ROM BASIC; this does **not** prove every gameplay path under LBASIC 5.3.0 works.

The image contains the LDOS distribution files from the user-supplied boot disk. It is provided as a project copy for that user, and no additional rights to the original operating system are claimed.
