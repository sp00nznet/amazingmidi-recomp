# Contributing

Issues and pull requests are welcome.

## The one rule

**Nothing from the program goes in the repository.** No AmazingMIDI files, no
lifted C (`src/recomp/gen/`), no catalog (`work/`), no disassembly listings,
nothing generated from `amazingmidi.exe`. The tool ships; its output is made
on each person's machine from their own copy. `.gitignore` covers the usual
paths; check `git status` before you commit anyway. Screenshots are fine.

## Before a pull request

1. Build from a clean lift: `py -3 run_lift.py` (expected: `errors 0`), then
   `build.cmd`.
2. Run the conformance harness at the console (it opens windows):
   ```
   py -3 tools\midi_diff.py
   ```
   It must print `IDENTICAL`. A new behaviour comes with a case that shows it
   ([docs/testing.md](docs/testing.md)).

## Where a fix belongs

- A bug in the lifter, the catalog or the native bridge belongs in
  [pcrecomp](https://github.com/sp00nznet/pcrecomp), not here.
- A fix to the program itself is a patch in `run_lift.py` or a seed in
  `seeds/`, with a comment that says what it fixes and why.
- Contributions must be your own or MIT-compatible: nothing ported from GPL
  code (Wine among it).
