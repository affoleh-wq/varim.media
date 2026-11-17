"""Саунд-дизайн для ролика: бит 120 BPM + SFX под монтаж. Пишет out/sound.wav"""
import numpy as np, os
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
DUR = 21.0
N = int(SR * DUR)
rng = np.random.default_rng(3)
CUTS = [3.5, 8.5, 13.0, 17.5]


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, kind, fs=SR, output="sos"), x)


def add(buf, t, s, g=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    s = s[: len(buf) - i]
    buf[i:i + len(s)] += s * g


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1) * np.exp(-np.maximum(t - a, 0) / d)


def kick(g=1.0):
    n = int(.35 * SR); t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / .03)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .11) * g


def hat(d=.03):
    n = int(.12 * SR)
    return filt(rng.standard_normal(n), "high", 7000) * env(n, .001, d)


def clap():
    n = int(.25 * SR)
    x = filt(rng.standard_normal(n), "band", [900, 3500]) * env(n, .002, .07)
    return x + np.roll(x, int(.012 * SR)) * .6


def saw(f, n, det=0.0):
    t = np.arange(n) / SR
    return sum(2 * ((t * f * (1 + d)) % 1) - 1 for d in (-det, 0, det)) / 3


def pad(freqs, dur):
    n = int(dur * SR)
    x = sum(saw(f, n, .004) for f in freqs) / len(freqs)
    x = filt(x, "low", 900, 2)
    t = np.arange(n) / SR
    return x * np.minimum(t / .4, 1) * np.minimum((dur - t) / .5, 1).clip(0)


def bass(f, dur=.22):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + .35 * filt(saw(f, n), "low", 500)
    return x * env(n, .005, .12)


def pluck(f):
    n = int(.25 * SR)
    return filt(saw(f, n, .003), "low", 3200) * env(n, .002, .06)


def whoosh(dur=.9, peak=.55):
    n = int(dur * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n); step = 2048
    for i in range(0, n, step):                      # плавающий полосовой фильтр
        c = 400 + 5200 * np.exp(-((t[i] - dur * peak) / (dur * .25)) ** 2)
        out[i:i + step] = filt(x[i:i + step + 0], "band", [c * .6, c * 1.6])[:step]
    return out * np.exp(-((t - dur * peak) / (dur * .22)) ** 2)


def impact():
    n = int(1.4 * SR); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t / .06)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .35)
    crack = filt(rng.standard_normal(n), "band", [300, 5000]) * np.exp(-t / .05) * .6
    tail = filt(rng.standard_normal(n), "low", 700) * np.exp(-t / .5) * .25
    return boom + crack + tail


def riser(dur=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 300 * (2 ** (t / dur * 2.2))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * .35
    noise = filt(rng.standard_normal(n), "high", 2500) * .5
    return (tone + noise) * (t / dur) ** 2


def blip(f, d=.04):
    n = int(.1 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t) * env(n, .001, d)


def ding():
    n = int(1.2 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * a for f, a in ((880, 1), (1320, .5), (1760, .3))) * np.exp(-t / .3)


music = np.zeros(N); drums = np.zeros(N); sfx = np.zeros(N)

def stac(f):
    n = int(.12 * SR)
    x = saw(f, n, .006) + .5 * saw(f * 2, n, .006)
    return filt(x, "low", 2600) * env(n, .004, .045)

def stab(freqs, dur=.55):
    n = int(dur * SR)
    x = sum(saw(f, n, .005) for f in freqs) / len(freqs) + .6 * saw(freqs[0] / 2, n, .004)
    return filt(x, "low", 2100) * env(n, .015, dur * .45)

def timp(g=1.0):
    n = int(.8 * SR); t = np.arange(n) / SR
    f = 62 + 40 * np.exp(-t / .04)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .28) + filt(rng.standard_normal(n), "low", 400) * np.exp(-t / .03) * .5) * g

def bell(f, d=.35):
    n = int(1.0 * SR); t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * h * t) * a for h, a in ((1, 1), (2, .4), (3, .15))) * np.exp(-t / d) * np.minimum(t / .003, 1)

# i – VI – iv – V, смена каждые 4 с; с 16.0 снова Am, с 17.5 финальный аккорд
CH = [(110.0, [220, 261.63, 329.63]), (87.31, [174.61, 220, 261.63]), (73.42, [146.83, 174.61, 220]), (82.41, [164.81, 207.65, 246.94]), (110.0, [220, 261.63, 329.63])]
PAT = [1, 1, 1, 1.5, 1, 1, 2, 1.5]           # остинато «струнных» шестнадцатыми
for k in range(int(19.0 / .125)):
    t = k * .125
    root, tones = CH[min(int(t // 4), 4)]
    build = min(1, .45 + t / 6) if t < 17.5 else max(0, 1 - (t - 17.5) / 1.5) * .6
    acc = 1.0 if k % 4 == 0 else .55
    add(music, t, stac(root * 2 * PAT[k % 8]), .5 * acc * build)
    add(music, t, stac(root * PAT[k % 8]), .35 * acc * build)
    if k % 2 == 0 and t < 19.6:                # тиканье часов
        add(drums, t, blip(2600 if k % 4 == 0 else 2050, .008), .09)
    if 8.5 <= t < 17.5:
        add(drums, t, hat(.012), .05)
for bar in range(9):                           # духовые акценты 3-3-2 и литавры
    t0 = bar * 2.0
    root, tones = CH[min(int(t0 // 4), 4)]
    for off, g in ((0, 1.0), (.75, .55), (1.5, .7)):
        if t0 + off < 17.4:
            add(music, t0 + off, stab(tones), .55 * g * (0.7 if t0 < 3.5 else 1))
    add(drums, t0, timp(), .8)
    if t0 + 1.5 < 17.4: add(drums, t0 + 1.5, timp(.6), .8)
for b in range(7, 35):                         # бочка с 3.5 до 17.5
    add(drums, b * .5, kick(.75))
for k in range(8):                             # дробь литавр перед финалом
    add(drums, 16.5 + k * .125, timp(.25 + k * .09), .8)
add(music, 17.5, stab([220, 329.63, 440, 554.37], 2.6), .9); add(drums, 17.5, timp(1.2), 1.0)
add(music, 17.5, pad([110, 164.81, 220], 3.5), .45)
for t0, g in ((3.75, .16), (8.75, .12), (13.25, .16)):   # позывной
    for j, f in enumerate((659.25, 659.25, 880)):
        add(music, t0 + j * .25, bell(f), g)
for j, f in enumerate((659.25, 880, 1108.73, 1318.5)):
    add(music, 18.1 + j * .2, bell(f, .6), .2)

# SFX
add(sfx, 0.0, whoosh(.6), .5)
for c in CUTS:
    w = whoosh(.95)
    add(sfx, c - .52, w, .95)
add(sfx, 2.5, riser(1.0), .3); add(sfx, 16.5, riser(1.0), .42); add(sfx, 7.7, riser(.8), .22); add(sfx, 12.2, riser(.8), .22)
for t in (0.62, 9.28, 18.05):
    add(sfx, t, impact(), 1.0)
add(sfx, 5.9, ding(), .25)
for t0, dur in ((4.1, 1.1), (4.35, 1.1), (4.6, 1.1), (10.8, 1.1)):          # счётчики
    for k in range(int(dur / .07)):
        add(sfx, t0 + k * .07, blip(900 + k * 35), .05)
for t0 in (14.2, 14.95):                                                       # плитки формы
    for k in range(5):
        add(sfx, t0 + k * .08, blip(1400 + k * 120, .02), .12)
for k in range(4):
    add(sfx, 10.0 + k * .1, blip(1200 + k * 100, .02), .1)

mix = music * .6 + drums * .7 + sfx * .7
mix = filt(mix, "high", 28)
t = np.arange(N) / SR
mix *= np.minimum(t / .05, 1) * np.clip((DUR - t) / 1.6, 0, 1) ** 1.2
mix = np.tanh(mix * 1.6)
mix = mix / np.abs(mix).max() * .89
# лёгкая стереобаза
d = int(.011 * SR)
side = filt(np.roll(mix, d), "high", 600) * .22
st = np.stack([mix + side, mix - side], 1)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"), exist_ok=True)
wavfile.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "sound.wav"), SR, (st / np.abs(st).max() * .89 * 32767).astype(np.int16))
print("sound ok")
