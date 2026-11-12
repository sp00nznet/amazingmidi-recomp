# Testing

## The conformance check: `tools/midi_diff.py`

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


Today the corpus is one case, so the figure is **1/1**. `sample.wav` (shipped
with AmazingMIDI) was also transcribed by both and compared byte for byte by
hand; it is not in the harness yet ([ROADMAP.md](../ROADMAP.md)).

`--keep DIR` keeps the generated .wav and both .mid files; `--game` and
`--recomp` point at another program folder or build.

## The dry run

`buildmazingmidirecomp.exe` with no `--run` maps and binds the image and
stops, with no window, so it works over RDP and on any test VM:

```
[bind] 0x00400000: 365 native, 0 guest, 7 shimmed, 0 unresolved
```
