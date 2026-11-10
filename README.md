# AmazingMIDI, recompiled

Static recompilation of **AmazingMIDI** 1.70 (arakisoftware, 2003), the
WAV-to-MIDI transcriber, from its shipping Win32 executable to native C. No
emulator, no wrapper DLLs. It is the first pcrecomp project that ran with no
changes at all: no toolkit fixes and no fixes to the program, just lift and
build (plus one seeded function address, below).

Built on the [pcrecomp](https://github.com/sp00nznet/pcrecomp) toolchain and
following its shared house style (layout, CLI, conformance harness), like the
other [pcrecomp projects](https://github.com/sp00nznet/pcrecomp#the-projects-that-built-this).

## What it is

A static recompilation of `amazingmidi.exe` (Visual C++ 6, MFC 4.2 and the C
runtime linked in, PE stamp `0x3F5249AC`). Its 3,232 catalogued functions are
lifted to C by pcrecomp, compiled with MSVC, and run on pcrecomp's `native32`
host, which calls the real user32, gdi32, comdlg32 and winmm. It runs Araki's
own code; it is not a rewrite.

## Status: v0.1.0, alpha. It transcribes, and its output matches the original byte for byte

| Stage | State |
|---|---|
| Version recompiled | AmazingMIDI 1.70 (`azmid170.exe`, 2003-08-31), the last release, freeware |
| Function catalog (`disasm32`) | 3,232 functions |
| Lift (`run_lift.py`) | 3,233 functions, 0 errors (57 with no terminator found, unchecked) |
| Host (`build/amazingmidirecomp.exe`, 32-bit, pcrecomp `native32`) | 365 imports bound to real Windows, 7 shimmed, 0 unresolved |
| Main window, menus, toolbar, piano roll | works, matches the original |
| File > Specify ... (open/save dialogs) | works |
| Transcribe dialog, transcription | works |
| .mid output vs the original | **byte-identical** on the harness's generated scale and on the bundled `sample.wav` |
| Play (MCIWnd), Help (WinHelp) | not yet checked |
| Headless mode (`--headless --record`) | not yet ([ROADMAP.md](ROADMAP.md)) |
| Conformance harness | `tools/midi_diff.py`: **1/1** (IDENTICAL) on a machine with the program; SKIP without it |

Built and tested against pcrecomp `main` at `2adc02f`.

## Screenshots

The main window, running as recompiled native code:

![The main window, running as recompiled native code](docs/screenshots/main.png)

## What is not in this repo

Nothing of AmazingMIDI: no executable, help file, tone file, and **no
generated source**. The recompiled C is produced on your machine from your own
copy by `run_lift.py`, into `src/recomp/gen/`, which is gitignored.

## Getting Started

You need **your own copy of AmazingMIDI 1.70**. The 1.70 installer
(`azmid170.exe`) is on the Internet Archive in the Tucows collection (item
`tucows_327319_AmazingMIDI`). It is a Wise installer: run it, and use the
folder it installs to (by default `C:\Program Files (x86)\AmazingMIDI`).
Nothing is downloaded for you.

### Quick start: Setup.cmd

1. Download this repository (the green **Code** button, then **Download ZIP**)
   and unzip it somewhere with 300 MB free.
2. Double-click **`Setup.cmd`**.

It checks for Python 3.10+, the `pefile` and `capstone` packages, the pcrecomp
toolkit and the Visual Studio 2022 C++ compiler, and **asks** before
installing any of them, saying what and how big. It finds AmazingMIDI in its
default install folder, or asks where it is (`Setup.cmd -GameDir <folder>`
skips the question, `-Yes` answers yes to every install). Then it copies the
program into `game\` (and `amazingmidi.exe` into `work\`), finds every
function, recompiles it and builds `build\amazingmidirecomp.exe`. A rerun skips
the finished steps. If it stops, it says why in one sentence, and the details
are in `setup.log`.

It ends with an **`AmazingMIDI`** shortcut in the folder. Double-click it to
run the recompiled program.

The [recomp-launcher](https://github.com/sp00nznet/recomp-launcher) installer
uses `launcher/launcher.json` to do the same; this repo builds it by hand only
(`.github/workflows/installer.yml`, run from the Actions tab).

### Step by step

Prerequisites: Windows 10/11, **Python 3.10+** (`py -3 --version`), **git**,
**Visual Studio 2022** (or its Build Tools) with *Desktop development with
C++*, and the pcrecomp toolkit cloned **beside** this repository as
`pcrecomp`, on `main`:

```
some-folder\
  pcrecomp\                     <- git clone https://github.com/sp00nznet/pcrecomp
  amazingmidi\                  <- this repository
```

1. Python packages:
   ```
   py -3 -m pip install --user pefile capstone
   ```
2. Copy the installed files (`amazingmidi.exe`, `sine.wav`, `piano0.wav`, ...)
   into `game\`, and `amazingmidi.exe` into `work\` too:
   ```
   mkdir game work
   xcopy /e /y "C:\Program Files (x86)\AmazingMIDI" game\
   copy game\amazingmidi.exe work\
   ```
3. The function catalog (seconds):
   ```
   py -3 ..\pcrecomp\tools\disasm\disasm32.py work\amazingmidi.exe -o work\functions.json
   ```
   Expected, at the end: `[*] Functions: 3232  (thunks=13, leaves=886)`.
4. Recompile to C:
   ```
   py -3 run_lift.py
   ```
   Expected, at the end:
   `lifted 3233 (+1 outside the catalog)   errors 0   no terminator 57   catch 0`.
5. Build (a minute or two):
   ```
   build.cmd
   ```
   Expected: `Linking C executable amazingmidirecomp.exe`.
6. Check it without opening a window:
   ```
   build\amazingmidirecomp.exe
   ```
   Expected: `[bind] 0x00400000: 365 native, 0 guest, 7 shimmed, 0 unresolved`
   and `(dry run: image mapped and bound; --run enters 0x0040CAB3)`.
7. Run it: `build\amazingmidirecomp.exe --run`.

The usual trip-ups: `python` opening the Microsoft Store (that is Windows'
alias placeholder; use `py -3`, or turn the alias off in *Settings > Apps >
Advanced app settings > App execution aliases*); a freshly installed Python
not being on `PATH` until you open a new window; and `run_lift.py` refusing a
different version (it checks the 1.70 PE stamp).

## Usage

```
build\amazingmidirecomp.exe --run                      # run it
build\amazingmidirecomp.exe --run --watchdog 60        # stop after 60 s, saying where every thread was
build\amazingmidirecomp.exe --run --native-trace       # one line per call into Windows
py -3 tools\midi_diff.py                               # the conformance check, below
```

| Flag | |
|---|---|
| `--run` | enter the program (without it: map, bind and stop, no window) |
| `--game DIR` | the program folder (default `game`) |
| `--args "..."` | the guest's command line |
| `--watchdog S` | stop after S seconds and say where every thread was |
| `--native-trace`, `--callbacks` | one line per call into Windows, or back from it |

### The conformance check

```
py -3 tools\midi_diff.py
```

writes a C major scale of sine tones with Python's `wave` module, has the
original `game\amazingmidi.exe` and the recomp each transcribe it (tone file
`sine.wav`), driving them through their own File and Transcribe dialogs, and
compares the two .mid files. It prints `IDENTICAL` and exits 0 when they match.
Without `game\amazingmidi.exe` it prints `midi_diff: skipped` and exits 0. It
opens both programs' windows, so run it at the console (or under offstage),
not over RDP. AmazingMIDI runs one instance at a time: close any open copy
first.

On [netlab](https://github.com/sp00nznet/recomp-netlab) the recipe is
`projects/amazingmidi-recomp.env`: `netlab build amazingmidi-recomp`, and
`netlab check amazingmidi-recomp` runs this check (SKIP on the test VMs, which
have no copy of the program).

## Building from source

Steps 3 to 5 above. `PCRECOMP` (Python) and `-DPCRECOMP=` (CMake, through
`set CMAKE_ARGS=...` for `build.cmd`) point at a toolkit checkout other than
`..\pcrecomp`; the lifter and the runtime must come from the same tree.

Nothing in the program needed a fix. The host (`src/runtime/host.c`) only
tells the guest it is `amazingmidi.exe` (`GetModuleHandleA(NULL)`,
`GetModuleFileNameA`, `GetCommandLineA`), so MFC finds its menus, dialogs and
icons in the mapped image. One function reached only through a pointer,
`0x0041D5F1`, was missing from the catalog and is seeded
(`seeds/run_seeds.json`). More in [docs/architecture.md](docs/architecture.md).

## License

MIT, for the code in this repository ([LICENSE](LICENSE); attribution in
[NOTICE](NOTICE)). AmazingMIDI is (c) 1998-2003 arakisoftware; none of it is
here.
