#!/bin/sh
# There is no Linux or macOS build yet. The recomp runs on pcrecomp's native32
# host, which binds AmazingMIDI's imports to the real Windows DLLs, and the
# win32hle path (ra2's native Linux build) doesn't cover MFC's common dialogs
# and MCI yet. A Wine path is untested. ROADMAP.md tracks it.
echo "AmazingMIDI recomp: Windows only for now. Run Setup.cmd on Windows (see README.md)." >&2
exit 1
