# Roadmap

## Next
- Play Tone / Input / Output File (MCIWnd): untested.
- Help > Contents opens amazingmidi.hlp through WinHelp, which Windows 10/11
  no longer ships: needs a fallback (or a .chm conversion) to be useful.
- A longer, polyphonic generated test (chords) in `tools/midi_diff.py`, and
  each of the shipped tone files, so the harness reports a count over a
  corpus rather than one case.
- Track the harness figure over time and fail on regression (REPO_RULES
  section 9): a `conformance.json` baseline, like hover's.

## Then
- Headless mode, `--headless --record out.mp4` (REPO_RULES section 10), so the
  harness and screenshots can run over RDP and on the netlab test VMs. Today
  `midi_diff.py` needs a visible desktop.
- Let Setup.cmd take `azmid170.exe` (the Wise installer) directly instead of
  an installed folder.
- The 57 functions whose extent walk found no terminator: check none of them
  is reached.

## Out of scope
- Rewriting or changing how AmazingMIDI transcribes. The point is the
  original's output, byte for byte.
