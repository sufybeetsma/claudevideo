"""Synthesises an original, royalty-free background music bed (warm lo-fi / inspirational, 96 BPM)
into public/music/bed.mp3. Replace that file with any licensed track to change the music."""
import numpy as np, os, subprocess, wave
from scipy.signal import butter, lfilter

SR = 44100
BPM = 96
BEAT = 60 / BPM
DUR = 66.0
N = int(SR * DUR)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(3)
mix = np.zeros((N, 2))

def lp(x, fc, order=2): b, a = butter(order, fc / (SR / 2)); return lfilter(b, a, x)
def hp(x, fc, order=2): b, a = butter(order, fc / (SR / 2), 'high'); return lfilter(b, a, x)
def midi(m): return 440 * 2 ** ((m - 69) / 12)

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    sig = sig[: N - i]
    mix[i:i + len(sig), 0] += sig * gain * (1 - pan) / 1.0
    mix[i:i + len(sig), 1] += sig * gain * (1 + pan) / 1.0

# Progression (one chord per bar): Fmaj7 - Am7 - Cmaj7 - G6  (bright, hopeful, "property / lifestyle" feel)
CHORDS = [[53, 57, 60, 64], [57, 60, 64, 67], [48, 52, 55, 59], [55, 59, 62, 64]]
BASS = [41, 45, 48, 43]
bar = 4 * BEAT
nbars = int(DUR / bar) + 1

for b in range(nbars):
    t0 = b * bar
    ch = CHORDS[b % 4]
    # warm pad: detuned saws, low-passed, slow attack
    t = np.arange(int(bar * SR * 1.05)) / SR
    pad = sum(((t * midi(m) * d) % 1 * 2 - 1) for m in ch for d in (0.997, 1.003))
    env = np.minimum(1, t / 0.6) * np.minimum(1, (bar * 1.05 - t) / 0.4)
    add(lp(pad, 1400) * env, t0, 0.035)
    # sub bass on beats 1 and 3
    for k in (0, 2):
        tb = np.arange(int(BEAT * 1.8 * SR)) / SR
        add(np.sin(2 * np.pi * midi(BASS[b % 4] - 12) * tb) * np.exp(-tb * 1.6), t0 + k * BEAT, 0.28)
    # pluck arpeggio in 8ths (enters after 2 bars)
    if b >= 2:
        pattern = [0, 2, 1, 3, 2, 1, 3, 2]
        for k, p in enumerate(pattern):
            tp = np.arange(int(0.5 * SR)) / SR
            f = midi(ch[p] + 12)
            pl = (np.sin(2 * np.pi * f * tp) + 0.3 * np.sin(4 * np.pi * f * tp)) * np.exp(-tp * 9)
            add(pl, t0 + k * BEAT / 2, 0.06, pan=0.35 if k % 2 else -0.35)
    # drums (enter after 1 bar)
    if b >= 1:
        for k in range(4):
            tk = np.arange(int(0.35 * SR)) / SR
            if k in (0, 2):  # soft kick
                f = 50 + 70 * np.exp(-tk * 30)
                add(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 9), t0 + k * BEAT, 0.42)
            else:  # rimshot-ish snap
                n = hp(rng.standard_normal(len(tk)), 1800) * np.exp(-tk * 28)
                add(n, t0 + k * BEAT, 0.07)
        for k in range(8):  # hats
            th = np.arange(int(0.08 * SR)) / SR
            add(hp(rng.standard_normal(len(th)), 7000) * np.exp(-th * 60), t0 + k * BEAT / 2 + (0.012 if k % 2 else 0),
                0.035 if k % 2 else 0.05, pan=0.2)

# fades + gentle bus compression / limiting
fade = np.ones(N)
fi, fo = int(1.0 * SR), int(3.0 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
mix *= fade[:, None]
mix = np.tanh(mix * 1.6) / 1.6
mix /= np.max(np.abs(mix)) / 0.89
tmp = os.path.join(ROOT, 'public', 'music', '_bed.wav')
with wave.open(tmp, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-b:a', '192k', os.path.join(ROOT, 'public', 'music', 'bed.mp3')], check=True)
os.remove(tmp)
print('wrote public/music/bed.mp3')
