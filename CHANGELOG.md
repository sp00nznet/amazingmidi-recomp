# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.0] - 2026-11-10

### Added
- `amazingmidi.exe` 1.70 lifted to C (3,230 functions, 0 errors) on
  pcrecomp's native32 host. The main window, menus, toolbar, the file
  open/save dialogs and the Transcribe dialog work.
- `tools/midi_diff.py`: a generated sine scale transcribed by the original and
  by the recomp; the two .mid files are byte-identical.
- `seeds/run_seeds.json`: 0x0041D5F1, called only through a pointer.
