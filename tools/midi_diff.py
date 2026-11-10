#!/usr/bin/env python3
"""Done check: the same WAV through the original exe and the recomp, .mid compared.

    py -3 tools/midi_diff.py [--game game] [--recomp build/amazingmidirecomp.exe]

The input is generated here (a C major scale of sine tones, made with the
stdlib `wave` module), so no recorded audio is involved. The tone file is the
sine.wav AmazingMIDI ships with. Each program is driven the same way, through
window messages: the three file boxes are filled in, Transcribe... is sent,
and Start is pressed in its dialog. The two .mid files must be byte-identical.
Exit 0 if they are.
"""
import argparse
import ctypes
import ctypes.wintypes as W
import math
import os
import struct
import subprocess
import sys
import tempfile
import time
import wave

u = ctypes.windll.user32
u.SendMessageW.argtypes = [W.HWND, W.UINT, W.WPARAM, W.LPARAM]
u.SendMessageW.restype = W.LPARAM
u.PostMessageW.argtypes = [W.HWND, W.UINT, W.WPARAM, W.LPARAM]
WM_SETTEXT, WM_COMMAND, BM_CLICK, BM_SETCHECK = 0x000C, 0x0111, 0x00F5, 0x00F1
# Menu resource 128: File > Specify Tone / Input / Output File..., Transcribe...
ID_TONE, ID_INPUT, ID_OUTPUT, ID_TRANSCRIBE = 32772, 32771, 32773, 32777
EnumProc = ctypes.WINFUNCTYPE(W.BOOL, W.HWND, W.LPARAM)


def make_wav(path, rate=44100):
    """C4..C5, half a second a note, a short fade at each end."""
    notes = [60, 62, 64, 65, 67, 69, 71, 72]
    n, fade = rate // 2, rate // 100
    frames = bytearray()
    for m in notes:
        f = 440.0 * 2 ** ((m - 69) / 12)
        for i in range(n):
            env = min(1.0, i / fade, (n - i) / fade)
            frames += struct.pack('<h', int(12000 * env * math.sin(2 * math.pi * f * i / rate)))
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(bytes(frames))


def windows(pid=None, parent=None):
    out = []

    def cb(h, _):
        p = W.DWORD()
        u.GetWindowThreadProcessId(h, ctypes.byref(p))
        if pid is None or p.value == pid:
            t = ctypes.create_unicode_buffer(256)
            c = ctypes.create_unicode_buffer(256)
            u.GetWindowTextW(h, t, 256)
            u.GetClassNameW(h, c, 256)
            out.append((h, t.value, c.value))
        return True
    if parent:
        u.EnumChildWindows(parent, EnumProc(cb), 0)
    else:
        u.EnumWindows(EnumProc(cb), 0)
    return out


def wait_for(fn, what, timeout=30):
    t = time.time() + timeout
    while time.time() < t:
        r = fn()
        if r:
            return r
        time.sleep(0.2)
    raise TimeoutError(what)


def pick_file(pid, main, cmd_id, path):
    """Open a File > Specify ... box and type the path into the common dialog."""
    u.PostMessageW(main, WM_COMMAND, cmd_id, 0)
    dlg = wait_for(lambda: [h for h, t, c in windows(pid) if c == '#32770' and u.IsWindowVisible(h)],
                   'file dialog')[0]
    time.sleep(0.5)
    # The file name box: an Edit inside ComboBoxEx 0x47C (Explorer style) or
    # Edit 0x480 (old style).
    name = wait_for(lambda: [h for h, t, c in windows(parent=dlg) if c == 'Edit'
                             and u.GetDlgCtrlID(u.GetParent(h)) in (0x47C, 0x480) or
                             c == 'Edit' and u.GetDlgCtrlID(h) in (0x47C, 0x480)], 'file name box')[0]
    buf = ctypes.create_unicode_buffer(path)
    u.SendMessageW(name, WM_SETTEXT, 0, ctypes.addressof(buf))
    u.PostMessageW(dlg, WM_COMMAND, 1, 0)          # IDOK
    wait_for(lambda: not u.IsWindow(dlg), 'file dialog to close')
    time.sleep(0.3)


def convert(cmd, tone, wav, mid):
    """Run one AmazingMIDI, transcribe wav into mid, return mid's bytes."""
    if os.path.exists(mid):
        os.remove(mid)
    p = subprocess.Popen(cmd)
    try:
        main = wait_for(lambda: [h for h, t, c in windows(p.pid)
                                 if t.startswith('AmazingMIDI') and u.IsWindowVisible(h)], 'main window')[0]
        for cmd_id, path in ((ID_TONE, tone), (ID_INPUT, wav), (ID_OUTPUT, mid)):
            pick_file(p.pid, main, cmd_id, path)
        u.PostMessageW(main, WM_COMMAND, ID_TRANSCRIBE, 0)
        dlg = wait_for(lambda: [h for h, t, c in windows(p.pid) if t == 'Transcribe'], 'Transcribe dialog')[0]
        kids = windows(parent=dlg)
        for h, t, c in kids:                 # don't play the result
            if t == 'Play Output File':
                u.SendMessageW(h, BM_SETCHECK, 0, 0)
        start = [h for h, t, c in kids if t == 'Start'][0]
        u.PostMessageW(start, BM_CLICK, 0, 0)

        def done():
            if not os.path.exists(mid):
                return None
            a = os.path.getsize(mid)
            time.sleep(1)
            return a and a == os.path.getsize(mid)
        wait_for(done, 'output .mid', timeout=120)
        return open(mid, 'rb').read()
    finally:
        p.kill()


def main():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default=os.path.join(here, 'game'))
    ap.add_argument('--recomp', default=os.path.join(here, 'build', 'amazingmidirecomp.exe'))
    ap.add_argument('--keep', help='folder to keep the .wav and both .mid in')
    a = ap.parse_args()
    game = os.path.abspath(a.game)
    work = os.path.abspath(a.keep) if a.keep else tempfile.mkdtemp(prefix='amidi_')
    os.makedirs(work, exist_ok=True)
    wav = os.path.join(work, 'scale.wav')
    make_wav(wav)
    tone = os.path.join(game, 'sine.wav')
    orig = convert([os.path.join(game, 'amazingmidi.exe')], tone, wav, os.path.join(work, 'original.mid'))
    rec = convert([os.path.abspath(a.recomp), '--run', '--game', game], tone, wav,
                  os.path.join(work, 'recomp.mid'))
    print('original %d bytes, recomp %d bytes (%s)' % (len(orig), len(rec), work))
    if orig == rec:
        print('IDENTICAL')
        return 0
    k = next(i for i in range(min(len(orig), len(rec)) + 1)
             if i == min(len(orig), len(rec)) or orig[i] != rec[i])
    print('DIFFER at byte %d' % k)
    return 1


if __name__ == '__main__':
    sys.exit(main())
