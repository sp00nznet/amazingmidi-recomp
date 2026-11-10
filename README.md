<div align="center">

# AmazingMIDI, recompiled

**AmazingMIDI** 1.70 (arakisoftware, 2003), the WAV-to-MIDI transcriber, taken
apart from its shipping Windows executable and rebuilt as a native program.
No emulator, no wrapper DLLs. The first application (not a game) on
[pcrecomp](https://github.com/sp00nznet/pcrecomp).

<img src="docs/screenshots/main.png" width="640" alt="The main window, running as recompiled native code">

</div>

## What it is

A static recompilation of `amazingmidi.exe` (Visual C++ 6, MFC 4.2 and the C
runtime linked in, PE stamp `0x3F5249AC`). Its 3,230 functions are lifted to C
by pcrecomp, compiled with MSVC, and run on pcrecomp's `native32` host, which
calls the real user32, gdi32, comdlg32 and winmm. It runs Araki's own code; it
is not a rewrite.

**Generated source is not distributed.** You supply your own copy, and the
lifted C is generated on your machine. Nothing from the program is in this
repository.

## Status: it transcribes, and its output matches the original byte for byte

| | |
|---|---|
| Version recompiled | AmazingMIDI 1.70 (`azmid170.exe`, 2003-08-31), the last release, freeware |
| Lift | 3,230 functions, 0 errors |
| Main window, menus, toolbar, piano roll | ✅ identical to the original |
| File > Specify ... (open/save dialogs) | ✅ |
| Transcribe dialog, transcription | ✅ |
| .mid output vs the original | ✅ byte-identical (`tools/midi_diff.py`; also on the bundled `sample.wav`) |
| Play (MCIWnd), Help (WinHelp) | not yet checked |

## Getting started

You need Windows 10/11, Python 3 with `capstone` and `pefile`, Visual Studio
2022 with the C++ x86 tools, and a checkout of
[pcrecomp](https://github.com/sp00nznet/pcrecomp) next to this one (built and
tested against main at `2adc02f`).

1. Get `azmid170.exe`. The 1.70 installer is on the Internet Archive in the
   Tucows collection (item `tucows_327319_AmazingMIDI`). It is a Wise
   installer: install it, or unpack it with E_WISE, and copy the installed
   files (`amazingmidi.exe`, `sine.wav`, `piano0.wav`, ...) into `game\`.
   Copy `amazingmidi.exe` into `work\` too.
2. Catalogue and lift:
   ```
   py -3 ..\pcrecomp\tools\disasm\disasm32.py work\amazingmidi.exe -o work\functions.json
   py -3 run_lift.py
   ```
3. Build: `build.cmd` (a minute or two).
4. Run: `build\amazingmidirecomp.exe --run`.

Options: `--game DIR` (default `game`), `--args "..."` (the guest's command
line), `--watchdog S`, `--native-trace`, `--callbacks`.

## The done check

```
py -3 tools\midi_diff.py
```

writes a C major scale of sine tones with Python's `wave` module, has the
original `game\amazingmidi.exe` and the recomp each transcribe it (tone file
`sine.wav`), driving them through their own File and Transcribe dialogs, and
compares the two .mid files. It prints `IDENTICAL` and exits 0 when they match.
AmazingMIDI runs one instance at a time: close any open copy first.

## How it works

Nothing in this program needed a fix. The host (`src/runtime/host.c`) only
tells the guest it is `amazingmidi.exe` (`GetModuleHandleA(NULL)`,
`GetModuleFileNameA`, `GetCommandLineA`), so MFC finds its menus, dialogs and
icons in the mapped image. One function reached only through a pointer,
`0x0041D5F1`, was missing from the catalogue and is seeded
(`seeds/run_seeds.json`).

## License

MIT for the code in this repository; see [LICENSE](LICENSE) and
[NOTICE](NOTICE). AmazingMIDI is (c) arakisoftware and is not included.
