# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-20

### Added
- `CONTRIBUTING.md`, `CONTRIBUTORS.md`, `docs/building.md`, `docs/testing.md`,
  and a `setup.sh` that says the build is Windows-only for now.
- `Setup.cmd` (`tools/setup.ps1`): one-click setup from your installed copy;
  checks and offers to install the prerequisites, resumes after a failure,
  ends with an `AmazingMIDI` shortcut.
- `launcher/launcher.json` and a hand-run installer workflow for
  recomp-launcher.
- `docs/architecture.md`.
- A netlab recipe (`projects/amazingmidi-recomp.env` in recomp-netlab), with
  `tools/midi_diff.py` as its QA.

### Changed
- README in the ra2 layout; the step-by-step build and the harness moved to
  `docs/`. `NOTICE` is now `NOTICE.md` and says what MIT does and doesn't cover.
- `tools/midi_diff.py` prints `midi_diff: skipped` and exits 0 when there is
  no `gamemazingmidi.exe`, so a machine without the program reports SKIP.
- README rewritten in the pcrecomp house style, with the real catalog and lift
  figures (3,232 catalogued, 3,233 lifted).

## [0.1.0] - 2026-11-10

### Added
- `amazingmidi.exe` 1.70 lifted to C (3,230 functions, 0 errors) on
  pcrecomp's native32 host. The main window, menus, toolbar, the file
  open/save dialogs and the Transcribe dialog work.
- `tools/midi_diff.py`: a generated sine scale transcribed by the original and
  by the recomp; the two .mid files are byte-identical.
- `seeds/run_seeds.json`: 0x0041D5F1, called only through a pointer.
