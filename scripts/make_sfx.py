"""Synthesises the sound-effect library into public/sfx (no third-party samples / licensing issues)."""
import numpy as np, wave, os
SR = 48000
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "sfx")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

def save(name, x):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.9
    x = np.stack([x, x], 1)
    with wave.open(f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

def t(d): return np.arange(int(SR * d)) / SR

def sweep_noise(d, f0, f1, env):
    n = rng.standard_normal(len(t(d)))
    fc = np.geomspace(f0, f1, len(n))
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.zeros_like(n); lp = 0; lp2 = 0
    for i in range(len(n)):  # two cascaded one-pole low-pass with moving cutoff
        lp = (1 - a[i]) * n[i] + a[i] * lp
        lp2 = (1 - a[i]) * lp + a[i] * lp2
        y[i] = lp - 0.6 * lp2  # crude band-pass
    return y * env

# whoosh: noise swept up then down
d = 0.5; x = t(d); env = np.sin(np.pi * x / d) ** 2
save("whoosh", sweep_noise(d, 300, 6000, env))
# swoosh up (riser) for CTA
d = 0.9; x = t(d); env = (x / d) ** 2 * np.exp(-((x - d) * 25) ** 2 * 0.0 + 0) * np.clip((d - x) / 0.06, 0, 1)
save("riser", sweep_noise(d, 200, 9000, env))
# pop: fast pitch-dropping sine
d = 0.14; x = t(d); f = 900 * np.exp(-x * 30) + 250
save("pop", np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 35))
# ding: bell partials
d = 1.0; x = t(d)
save("ding", sum(a * np.sin(2 * np.pi * f * x) * np.exp(-x * k) for f, a, k in
                 [(1568, 1, 5), (3136, .4, 8), (4704, .2, 12), (2350, .15, 9)]))
# tick: short click
d = 0.05; x = t(d)
save("tick", (np.sin(2 * np.pi * 2800 * x) + .5 * rng.standard_normal(len(x))) * np.exp(-x * 120))
# boom: sub hit for the hook
d = 0.9; x = t(d); f = 110 * np.exp(-x * 6) + 42
save("boom", np.tanh(2.5 * np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-x * 5) +
     0.3 * sweep_noise(d, 2000, 200, np.exp(-x * 20)))
# error buzz (for the "wrong question")
d = 0.35; x = t(d)
sq = np.sign(np.sin(2 * np.pi * 140 * x)) + .6 * np.sign(np.sin(2 * np.pi * 147 * x))
save("buzz", sq * np.clip(x / .01, 0, 1) * np.clip((d - x) / .08, 0, 1) * 0.6)
# cash/coin chime for equity
d = 0.6; x = t(d)
c = np.sin(2*np.pi*2093*x)*np.exp(-x*9) + np.where(x > .08, np.sin(2*np.pi*2637*(x-.08))*np.exp(-(x-.08)*9), 0)
save("coin", c)
print(sorted(os.listdir(OUT)))
