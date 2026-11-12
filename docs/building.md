# Building

What `Setup.cmd` does, by hand. `tools/setup.ps1` runs exactly these steps.

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


## Command line

```
build\amazingmidirecomp.exe --run                      # run it
build\amazingmidirecomp.exe --run --watchdog 60        # stop after 60 s, saying where every thread was
build\amazingmidirecomp.exe --run --native-trace       # one line per call into Windows
py -3 tools\midi_diff.py                               # the conformance check (docs/testing.md)
```

| Flag | |
|---|---|
| `--run` | enter the program (without it: map, bind and stop, no window) |
| `--game DIR` | the program folder (default `game`) |
| `--args "..."` | the guest's command line |
| `--watchdog S` | stop after S seconds and say where every thread was |
| `--native-trace`, `--callbacks` | one line per call into Windows, or back from it |


## Toolkit and fixes

`PCRECOMP` (Python) and `-DPCRECOMP=` (CMake, through
`set CMAKE_ARGS=...` for `build.cmd`) point at a toolkit checkout other than
`..\pcrecomp`; the lifter and the runtime must come from the same tree.

Nothing in the program needed a fix. The host (`src/runtime/host.c`) only
tells the guest it is `amazingmidi.exe` (`GetModuleHandleA(NULL)`,
`GetModuleFileNameA`, `GetCommandLineA`), so MFC finds its menus, dialogs and
icons in the mapped image. One function reached only through a pointer,
`0x0041D5F1`, was missing from the catalog and is seeded
(`seeds/run_seeds.json`). More in [docs/architecture.md](docs/architecture.md).

