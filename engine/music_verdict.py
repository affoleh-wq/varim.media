"""Phonk/drill-бит 140 BPM для формата Verdict 12 (12.0 с). Пишет sound_verdict.wav рядом со скриптом.
Склейки сцен на долях 6, 12, 20 (2.571 / 5.143 / 8.571 с), удары — через долю после склейки."""
import numpy as np, os
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
BPM = 140
B = 60 / BPM                     # 0.4286 с
DUR = 12.0
N = int(SR * DUR)
rng = np.random.default_rng(11)
CUTS = [6 * B, 12 * B, 20 * B]
HITS = [1 * B, 6 * B + B, 12 * B + B, 20 * B + B]


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, kind, fs=SR, output="sos"), x)


def add(buf, t, s, g=1.0):
    i = int(round(t * SR))
    if i >= len(buf) or i < 0:
        return
    s = s[: len(buf) - i]
    buf[i:i + len(s)] += s * g


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / max(a, 1e-4), 1) * np.exp(-np.maximum(t - a, 0) / d)


def bass808(f0, dur, glide_to=None):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.full(n, f0)
    if glide_to:
        k = int(n * .55)
        f[k:] = f0 + (glide_to - f0) * np.clip((t[k:] - t[k]) / .09, 0, 1)
    click = 40 * np.exp(-t / .012)
    ph = 2 * np.pi * np.cumsum(f + click) / SR
    x = np.sin(ph) + .25 * np.sin(2 * ph)
    x = np.tanh(x * 2.2) * np.minimum(t / .004, 1) * np.exp(-t / (dur * .9))
    return x


def kick():
    n = int(.22 * SR); t = np.arange(n) / SR
    f = 50 + 140 * np.exp(-t / .02)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .07)


def clap():
    n = int(.3 * SR)
    x = filt(rng.standard_normal(n), "band", [1000, 4500]) * env(n, .001, .08)
    return x + np.roll(x, int(.011 * SR)) * .7 + np.roll(x, int(.022 * SR)) * .45


def hat(d=.025):
    n = int(.08 * SR)
    return filt(rng.standard_normal(n), "high", 8000) * env(n, .0005, d)


def cowbell(f):
    n = int(.35 * SR); t = np.arange(n) / SR
    sq = lambda fr: np.sign(np.sin(2 * np.pi * fr * t))
    x = (sq(f) + sq(f * 1.48)) * .5
    x = filt(x, "band", [500, 4000])
    return x * env(n, .001, .09)


def impact():
    n = int(1.1 * SR); t = np.arange(n) / SR
    f = 36 + 80 * np.exp(-t / .05)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .3)
    crack = filt(rng.standard_normal(n), "band", [400, 6000]) * np.exp(-t / .04) * .7
    return np.tanh((boom + crack) * 1.5)


def whoosh(dur=.5):
    n = int(dur * SR); t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), "band", [700, 7000])
    return x * (t / dur) ** 2.2


def riser(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), "high", 3000) * .6
    f = 400 * 2 ** (t / dur * 2)
    x += np.sin(2 * np.pi * np.cumsum(f) / SR) * .25
    return x * (t / dur) ** 2


drums = np.zeros(N); bass = np.zeros(N); mel = np.zeros(N); sfx = np.zeros(N)
beats = int(DUR / B) + 1
# F# minor: F#1 46.25, A1 55, B1 61.74, D2 73.42, E2 82.41, C#2 69.3
ROOTS = [46.25, 46.25, 55.0, 41.2]           # на каждый такт (4 доли)
for b in range(beats):
    t = b * B
    bar, pos = divmod(b, 4)
    intro = b < 1
    if pos == 0 and not intro:
        add(drums, t, kick(), .9)
    if pos == 2:
        add(drums, t, clap(), .55)
    # хэты восьмыми, в конце каждого второго такта — дробь
    if bar % 2 == 1 and pos == 3:
        for k in range(6):
            add(drums, t + k * B / 6, hat(.012), .22)
    else:
        add(drums, t, hat(), .2); add(drums, t + B / 2, hat(.015), .13)
    # 808: на 1-ю долю и с синкопой
    r = ROOTS[bar % 4]
    if pos == 0:
        add(bass, t, bass808(r, B * 1.4), .75)
    if pos == 2 and bar % 2 == 0:
        add(bass, t + B * .5, bass808(r, B * 1.2, glide_to=r * 1.5), .6)
    if pos == 3 and bar % 2 == 1:
        add(bass, t + B * .5, bass808(r * 1.335, B * .9, glide_to=r), .55)
# коубелл-мелодия шестнадцатыми-восьмыми (фригийский оттенок)
PAT = [(0, 739.99), (0.75, 739.99), (1.5, 783.99), (2, 739.99), (2.75, 659.25), (3.5, 587.33)]
for bar in range(beats // 4 + 1):
    for off, f in PAT:
        t = (bar * 4 + off) * B
        if t >= B * 1:
            add(mel, t, cowbell(f), .32 if bar % 2 == 0 else .26)
# эффекты
add(sfx, 0.0, impact(), .55)
for h in HITS:
    add(sfx, h, impact(), .7)
for c in CUTS:
    add(sfx, c - .5, whoosh(.5), .55)
add(sfx, CUTS[2] - 1.6, riser(1.6), .3)

mix = drums * .9 + bass * .8 + mel * .55 + sfx * .75
mix = filt(mix, "high", 25)
t = np.arange(N) / SR
mix *= np.clip((DUR - t) / .08, 0, 1)          # резкий конец под петлю
mix = np.tanh(mix * 1.4)
mix = mix / np.abs(mix).max() * .9
d = int(.009 * SR)
side = filt(np.roll(mel + drums * .3, d), "high", 800) * .18
st = np.stack([mix + side, mix - side], 1)
st = st / np.abs(st).max() * .9
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound_verdict.wav")
wavfile.write(out, SR, (st * 32767).astype(np.int16))
print("ok", out)
