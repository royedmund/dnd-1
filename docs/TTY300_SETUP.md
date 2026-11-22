# TTY300 — Model III LDOS BASIC terminal for PiDP-11/70 RSTS/E

**Status:** First BASIC-only experimental version. Source has been checked and a standalone screen-startup smoke test completed in trs80gp 2.5.8 (Model III ROM BASIC, not LBASIC); physical RS-232 transfer **has not yet been tested on Roy's hardware**. It must not be described as guaranteed loss-free at 300 baud.

## Intended connection

The user's real **48 KB TRS-80 Model III** runs **LDOS 5.1** and **LBASIC**, using the built-in RS-232 interface to act as a simple printing terminal. The remote endpoint is a **PiDP-11/70 (SIMH emulated PDP-11)** running **RSTS/E**, with a **USB-to-RS-232 adapter** attached to an emulated terminal line. DND runs on RSTS/E (use this repository's *experimental* [BASIC-PLUS port](../pdp11/DND11.BAS)), not on the Model III during the terminal session.

This is a text-only *Teletype-inspired* terminal, not exact electromechanical ASR-33 simulation. A physical ASR-33 typically ran at 110 baud (10 cps); the **300 baud** speed here is intentionally higher. It uses standard ASCII, not VT52/VT100 escape-sequence emulation, and shows 64 columns by 16 lines with scrolling (the Model III display). It does not simulate paper tape or an actual local printer.

## Model III connection and wiring

**Use real RS-232 electrical signalling**, not a Raspberry Pi GPIO header or USB-to-TTL cable (which use 3.3V/5V logic). Most USB-to-RS-232 serial adapters with a DB9 male connector behave as DTE devices. The Model III DB25 serial port is DTE, so a **null-modem/crossover cable** is required. A minimal 3-wire connection (with hardware flow control disabled) for a conventional DTE USB DB9 is:

| Model III DB25 | Direction | USB RS-232 DB9 DTE |
| --- | --- | --- |
| Pin 2 — TxD (output) | → | Pin 2 — RxD (input) |
| Pin 3 — RxD (input) | ← | Pin 3 — TxD (output) |
| Pin 7 — Signal ground | ↔ | Pin 5 — Signal ground |

**Check the actual pinouts and connector gender of your adapter**, which may vary. This is a *crossed-signal* cable even though the two data pins happen to have the same numerical labels on DB25 and DB9. Do not connect two outputs together. With no flow control, don't require CTS/DSR/DCD at the Pi end; RTS/DTR are asserted by the Model III. If SIMH / USB adapter insists on modem-control leads, use a properly wired hardware-handshake null-modem cable instead of forcing the program to wait forever.

## Run on the Model III

1. Boot the Model III under **LDOS 5.1**. **Do not** first run ``SET *CL TO RS232T/DVR`` or LCOMM; this program **directly accesses** the UART hardware ports and must not compete with the LDOS interrupt-driven serial driver.
2. Transfer/import the plain-text listing [``basic/TTY300.BAS``](../basic/TTY300.BAS) into **LBASIC**. Note that a plain ASCII file is not necessarily a tokenised ``/BAS`` disk file. Type the numbered lines manually or use a verified file import tool.
3. Save it with ``SAVE "TTY300/BAS"`` once it is in BASIC memory.
4. Connect the null-modem cable to the Raspberry Pi's USB-RS232 adapter, with RSTS/E already booted and a working serial terminal line configured.
5. Type ``RUN``. Text coming from the PiDP-11 appears on the Model III; keys typed on the Model III go to the emulated PDP-11.
6. Press **BREAK** to stop (the normal BASIC break may interrupt the program before it sees the ASCII break code). ``RUN`` restarts, resetting the UART. If the port will later be used with LDOS `RS232T/DVR`, reload/reinitialise the driver after finishing this direct-I/O program.

**Serial settings:** 300 baud / 8 data bits / no parity / 1 stop bit (**300 8N1**), full duplex with remote echo, **no XON/XOFF and no CTS/RTS flow control**. The host is responsible for echo. If no characters appear as you type, investigate whether RSTS/E is configured to echo input; the program deliberately does not locally echo keys to avoid doubled text.

## Port operations

| Decimal I/O port | Operation |
| --- | --- |
| 232 / E8h | UART master reset: ``OUT 232,0`` |
| 233 / E9h | Baud select: ``OUT 233,85`` (55h = 300 bps both directions) |
| 234 / EAh (output) | UART control: ``OUT 234,104`` (68h: 8-bit, no parity, 1 stop, DTR/RTS asserted) |
| 234 / EAh (input) | Receive data-ready bit 7 (128); transmitter-ready bit 6 (64) |
| 235 / EBh | UART received byte via ``INP(235)``, transmit via ``OUT 235,B`` |

The program polls receive before checking the keyboard on each loop, checks transmit readiness, ignores incoming LF (to avoid double-spaced CR+LF output), translates CR to a BASIC newline, handles simple backspace/tab, and filters unprintable controls. The Model III left arrow/backspace transmits ASCII DEL (127), commonly suitable for RSTS/E editing. For other RSTS terminal editing settings it may be necessary to send ASCII BS (8) instead: change line 280 to ``IF B=8 THEN B=8`` or simply delete line 280.

**Limits:** BASIC is slow and the hardware UART has limited character buffering. A vintage LDOS Quarterly article explicitly reports losing characters at **300 baud** with a similar BASIC polling terminal. This is an **experiment**, especially when DND emits long map displays. If received text is damaged, use the supplied LDOS **LCOMM/CMD** with the buffered **RS232T/DVR** driver, or a small Z80 interrupt-driven terminal executable (future project) instead. Do not mix direct port polling with the active buffered driver.

## PiDP-11/70 and SIMH side

The Pi must use a real ``/dev/ttyUSB0`` (or another detected USB serial port). Verify the device name:

```sh
ls -l /dev/serial/by-id/
ls -l /dev/ttyUSB*
```

Before SIMH owns the port, configure/test the adapter with Linux (replace the device name appropriately):

```sh
sudo stty -F /dev/ttyUSB0 300 cs8 -parenb -cstopb -ixon -ixoff -crtscts raw -echo
```

The *actual* serial settings when attached may be controlled by SIMH; check them with ``SHOW SERIAL``. When RSTS/E is running, connect the USB adapter to an **enabled emulated DZ11/VH11 terminal line** using the syntax supported by your particular SIMH build, e.g. from the simulator prompt or its ``boot.ini``:

```text
SET DZ 8B
ATTACH DZ LINE=0,CONNECT=/dev/ttyUSB0
SHOW SERIAL
```

This is an **illustrative** DZ line-0 configuration, not a universally supported PiDP boot.ini. **Do not attach the USB adapter to a console or terminal device already in use.** Some versions of RSTS/E are not configured to support all of the SIMH multiplexer lines; the stock PiDP-11 RSTS/E V7 image has been reported to lack the necessary DZ remote terminal system generation. Confirm that your chosen RSTS/E image actually has an enabled terminal port. Choose 300 8N1 on both sides, and disable any Linux ``serial-getty`` service that owns the same device. Connecting to a Linux login on ``/dev/ttyUSB0`` would not reach the emulated RSTS/E computer.

After RSTS/E logs you in over that serial terminal, start BASIC-PLUS and load/run **DND11.BAS** using the procedures for your installed RSTS/E release. This repo's PDP-11 source remains **experimental**, pending successful real RSTS/E gameplay testing. The CDC BASIC source **does not run directly under RSTS/E**.

## Checks and incremental troubleshooting

1. **Cable loopback first:** with the Model III disconnected from the Pi, temporarily loop **pins 2 and 3** on the Model III's own DB25 serial port (not the Raspberry Pi GPIO). Start TTY300, type characters, and see whether they return to the Model III display; this checks transmit and receive locally. Remove the loopback before connecting the Pi.
2. **USB adapter first:** use an ordinary Linux terminal program on the Pi to test its serial device at 300 8N1; do not have SIMH and Linux terminal software using the port simultaneously.
3. **SIMH line:** confirm ``SHOW SERIAL`` reports the expected serial USB adapter attached to the terminal line; check your RSTS/E terminal device and terminal speed settings.
4. **Echo:** if typed keys aren't displayed, the remote RSTS/E may not be echoing. Do not enable simultaneous local and remote echo as it produces doubled text.
5. **Garbage text:** check baud, 8N1, null-modem wiring and serial-to-RS232 electrical levels.
6. **Missing text:** this BASIC implementation is receive-polling and might overrun at even 300 baud. Prefer the LDOS buffered LCOMM path for full dungeon listings.

### Emulator and static tests

The source loads and reaches its terminal banner without a BASIC syntax error under **trs80gp 2.5.8 emulating a Model III ROM BASIC**. No serial peer was connected, so actual transmit/receive and any possible dropped characters have **not** been tested. No run under **LDOS 5.1 LBASIC** has yet been completed. Run `python3 tests/check_tty300.py` to repeat the static source/profile checks.

### Sources

- **User-provided LDOS 5.1 operating system manual**, Model III ``RS232T/DVR`` section (driver defaults 300/7/E/1 and 128-byte interrupt receive buffering), and LBASIC ``CMD "R"``/``CMD "T"`` section (Model III clock display toggles; they do **not** disable interrupts as on Model I).
- [Model III I/O ports and UART status bits](https://www.trs-80.com/main-internal-ports-and-i-o.htm).
- [LDOS Quarterly issue 1–6](https://www.tim-mann.org/trs80/doc/ldosq1-6.pdf), p. 50–51, contemporary BASIC 300-baud terminal example, warning that BASIC sometimes drops incoming chars.
- [PiDP-11 forum: serial ports and SIMH ``SHOW SERIAL`` / ``ATTACH``](https://groups.google.com/g/pidp-11/c/NmQ65FjxjkA).
- [PiDP-11 forum: RSTS/E and SIMH character mode](https://groups.google.com/g/pidp-11/c/SvMMtfYZ_V4).
