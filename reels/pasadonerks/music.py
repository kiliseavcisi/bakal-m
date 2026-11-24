"""Synthesize a 20s, 120 BPM beat for the reel (royalty-free, generated)."""
import numpy as np, wave, sys
SR = 44100; DUR = 20.0; BPM = 120; BEAT = 60 / BPM
N = int(SR * DUR); out = np.zeros(N)
rng = np.random.default_rng(7)
def add(sig, t, gain=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: out[i:j] += sig[: j - i] * gain
def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)
def kick():
    n = int(.4 * SR); t = np.arange(n) / SR
    f = 50 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .001, .16)
def snare():
    n = int(.25 * SR); t = np.arange(n) / SR
    return (rng.standard_normal(n) * .7 + np.sin(2 * np.pi * 190 * t) * .5) * env(n, .001, .07)
def hat(open_=False):
    n = int((.18 if open_ else .05) * SR)
    x = rng.standard_normal(n); x = np.diff(x, prepend=0)  # crude high-pass
    return x * env(n, .0005, .06 if open_ else .015)
def bass(freq, length):
    n = int(length * SR); t = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * freq * t)) * .5 + np.sin(2 * np.pi * freq * t)
    return np.tanh(s * 1.5) * env(n, .005, length * .7)
def pluck(freq, length=.3):
    n = int(length * SR); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * freq * k * t) / k for k in (1, 2, 3))
    return s * env(n, .003, .12)
def riser(t0, t1):
    n = int((t1 - t0) * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); x = np.diff(x, prepend=0)
    sweep = np.sin(2 * np.pi * np.cumsum(300 + 2000 * (t / t[-1]) ** 2) / SR)
    add((x * .5 + sweep * .3) * (t / t[-1]) ** 2, t0, .5)
def impact(t0):
    n = int(1.2 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(80 * np.exp(-t * 3) + 30) / SR) + rng.standard_normal(n) * np.exp(-t * 20) * .6
    add(s * env(n, .001, .35), t0, .9)

# Hook (0-2): sparse hits on the word slams
add(kick(), 0.05, 1); add(kick(), 0.55, 1); add(snare(), 1.05, .6); add(kick(), 1.05, 1)
riser(1.5, 2.5)
# Main groove 2-12.5, break 12.5 with impact, outro groove
A, C, D, E, G = 55.0, 65.41, 73.42, 82.41, 98.0
bassline = [A, A, C, A, D, D, E, G]
melody = [440, 523.25, 587.33, 659.25, 587.33, 523.25, 440, 392]
t = 2.5; step = 0
while t < DUR - 1e-6:
    beat_in_bar = step % 4
    if not (16.0 <= t < 16.5):
        add(kick(), t, 1.0)
        if beat_in_bar in (1, 3): add(snare(), t, .55)
        add(hat(), t + BEAT / 2, .25); add(hat(beat_in_bar == 3), t, .15)
        add(bass(bassline[step % 8], BEAT * .9), t, .35)
        if t >= 7.0 and step % 2 == 0: add(pluck(melody[(step // 2) % 8]), t + BEAT / 2, .18)
    t += BEAT; step += 1
riser(6.0, 7.0); riser(15.5, 16.5)
for c in (2.5, 7.0, 14.0, 16.5): impact(c)
# Sizzle under the product scene
n = int(4.5 * SR); sz = np.diff(rng.standard_normal(n), prepend=0) * (0.6 + 0.4 * rng.random(n) ** 8)
add(sz * np.minimum(1, np.arange(n) / (SR * .3)) * np.minimum(1, (n - np.arange(n)) / (SR * .3)), 2.5, .08)
# Fade out last 0.6s
f = int(.6 * SR); out[-f:] *= np.linspace(1, 0, f)
out = np.tanh(out * 1.2); out /= np.abs(out).max() / 0.9
pcm = (out * 32767).astype(np.int16)
st = np.repeat(pcm[:, None], 2, axis=1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
