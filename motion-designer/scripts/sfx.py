"""sfx.py — tiny numpy synth kit for event-locked soundtracks (no samples, no licensing issues).

Usage (in your project's audio.py):
    import sys; sys.path.insert(0, '<skill>/scripts')
    from sfx import *
    init(dur=24.0)                       # seconds, must match the timeline DUR
    M = marks('marks.json')              # event times exported from the timeline (see export_marks.py)
    put(whoosh(.6), M['T2'] - .3, .45)   # place sounds on timeline events
    put(boom(), M['END'], .8, verb=.4)
    master('sound.wav')                  # reverb + soft-clip + fade + write 48 kHz stereo

Every sound must be tied to a visual event (cut, land, tap, count, stamp). Music bed = simple
groove from kick/hat/bass/marimba/pad helpers; keep it under the visuals, never louder than SFX hits.
"""
import json, wave
import numpy as np

SR = 48000
DUR = 0.0
N = 0
rng = np.random.default_rng(7)
L = R = VL = VR = None


def init(dur):
    global DUR, N, L, R, VL, VR
    DUR = float(dur); N = int(SR * DUR)
    L, R, VL, VR = (np.zeros(N) for _ in range(4))


def marks(path='marks.json'):
    return json.load(open(path))


def put(sig, t, gain=1.0, pan=0.0, verb=0.0):
    """Place a mono signal at time t (s). pan -1..1, verb = reverb send 0..1."""
    i = int(t * SR); n = min(len(sig), N - i)
    if n <= 0 or i < 0: return
    gl, gr = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    L[i:i + n] += sig[:n] * gain * gl; R[i:i + n] += sig[:n] * gain * gr
    if verb:
        VL[i:i + n] += sig[:n] * gain * verb * gl; VR[i:i + n] += sig[:n] * gain * verb * gr


def onepole_lp(x, fc):
    """time-varying one-pole lowpass; fc scalar or array (Hz)."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)):
        s += a[i] * (x[i] - s); y[i] = s
    return y


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if lo: g *= 1 / (1 + (lo / np.maximum(f, 1)) ** 4)
    if hi: g *= 1 / (1 + (f / hi) ** 4)
    return np.fft.irfft(X * g, len(x))




def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=.002, dec=.2):
    t = tt(d); return np.minimum(t / a, 1) * np.exp(-t / dec)


def kick(d=.55, f0=140, f1=42, dec=.28):
    t = tt(d); f = f1 + (f0 - f1) * np.exp(-t / .045)
    ph = 2 * np.pi * np.cumsum(f) / SR
    click = rng.standard_normal(len(t)) * np.exp(-t / .004) * .3
    return (np.sin(ph) * np.exp(-t / dec) + click) * np.minimum(t / .001, 1)


def boom(d=2.4):
    t = tt(d); f = 30 + 110 * np.exp(-t / .12)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .9)
    nz = fft_filter(rng.standard_normal(len(t)), hi=2500) * np.exp(-t / .18) * .5
    return np.tanh((s + nz) * 1.6) * .9


def hat(d=.06, dec=.018):
    t = tt(d); return fft_filter(rng.standard_normal(len(t)), lo=7000) * np.exp(-t / dec)


def clap(d=.3):
    t = tt(d); n = fft_filter(rng.standard_normal(len(t)), lo=900, hi=5000)
    e = np.exp(-t / .07) + .6 * np.exp(-np.maximum(t - .011, 0) / .01) * (t > .011) + .6 * np.exp(-np.maximum(t - .022, 0) / .01) * (t > .022)
    return n * e


def tone(f, d, dec=.3, harm=((1, 1),), a=.004):
    t = tt(d); s = sum(g * np.sin(2 * np.pi * f * h * t) for h, g in harm)
    return s * env(d, a, dec)


def bell(f, d=1.6):
    return tone(f, d, .55, ((1, 1), (2.76, .35), (5.4, .12), (8.93, .05)), .002)


def tick(d=.03, f=3500):
    t = tt(d); return (np.sin(2 * np.pi * f * t) * .6 + rng.standard_normal(len(t)) * .4) * np.exp(-t / .004)


def metal(d=.35):
    t = tt(d); s = sum(np.sin(2 * np.pi * f * t + rng.random() * 6) * g for f, g in ((1830, 1), (2970, .7), (4410, .5), (6230, .3)))
    return (s * .5 + fft_filter(rng.standard_normal(len(t)), lo=2000) * .5) * np.exp(-t / .05)


def whoosh(d, peak=.6, lo=300, hi=5000, rev=False):
    t = tt(d); n = rng.standard_normal(len(t)); x = t / d
    shape = np.exp(-((x - peak) / .22) ** 2)
    fc = lo + (hi - lo) * shape
    s = onepole_lp(n, fc) - onepole_lp(n, fc * .25)
    s *= shape; s /= np.max(np.abs(s)) + 1e-9
    return s[::-1] if rev else s


def riser(d, f0=180, f1=1400):
    t = tt(d); x = t / d
    f = f0 * (f1 / f0) ** (x ** 1.6)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * .35 + np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * .15
    n = rng.standard_normal(len(t)); nz = onepole_lp(n, 300 + 9000 * x ** 2) * .9
    return (s + nz) * x ** 2.2


def saw(f, d, nh=14):
    t = tt(d); return sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, nh + 1) if f * k < 16000)


def blip(f, d=.05):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.exp(-t / .012)


def noteHz(n): return 440 * 2 ** ((n - 69) / 12)


# ---- melodic / texture helpers
def marimba(f, d=.6, g=1):
    t = tt(d); s = np.sin(2*np.pi*f*t)*np.exp(-t/.22) + .35*np.sin(2*np.pi*f*4*t)*np.exp(-t/.03) + .15*np.sin(2*np.pi*f*10*t)*np.exp(-t/.008)
    return s*np.minimum(t/.001, 1)*g


def pluck(f, d=.5):
    t = tt(d); s = saw(f, d, 10); s = onepole_lp(s*np.exp(-t/.12), 900+5000*np.exp(-t/.06)); return s*.5


def bass(f, d=.45):
    t = tt(d); s = np.sin(2*np.pi*f*t) + .3*np.sin(2*np.pi*2*f*t); return np.tanh(s*1.4)*np.exp(-t/.25)*np.minimum(t/.005, 1)


def pad(fs, d, a=.6):
    t = tt(d); s = sum(saw(f*(1+dt), d, 8) for f in fs for dt in (-.003, .003)); s = fft_filter(s, hi=1800)
    return s*np.minimum(t/a, 1)*np.minimum((d-t)/.8, 1)*.12


def coinding(f=1568):
    return bell(f, .9)*.6 + bell(f*1.5, .9)*.35


def shutter():
    t = tt(.12); n = fft_filter(rng.standard_normal(len(t)), lo=1500)
    return n*(np.exp(-t/.008) + .7*np.exp(-np.maximum(t-.05, 0)/.01)*(t > .05))


def pop(f):
    t = tt(.18); fr = f*(1+1.5*np.exp(-t/.01)); return np.sin(2*np.pi*np.cumsum(fr)/SR)*np.exp(-t/.06)


def typing(n=12, start=0.0, rate=.07, gain=.08):
    """Keyboard clicks: call put() for n ticks starting at `start`."""
    for j in range(n): put(tick(.02, 2600 + ((j*7) % 5)*300), start + j*rate, gain, (j/max(n-1, 1)*2-1)*.5)


def groove(t0, t1, bpm=120, chords=((60, 64, 67, 71), (57, 60, 64, 67), (53, 57, 60, 64), (55, 59, 62, 64)),
           roots=(36, 33, 29, 31), level=1.0):
    """Light 4-on-the-floor bed with marimba arps between t0 and t1 (seconds)."""
    B = 60/bpm; k = 0
    while True:
        t = t0 + k*B
        if t >= t1: break
        bar = int((t - t0)//(4*B)) % len(chords)
        put(kick(), t, .9*level)
        if k % 2 == 1: put(clap(), t, .35*level, .1, .25)
        put(hat(), t + B/2, .16*level, .3)
        put(bass(noteHz(roots[bar])), t, .5*level)
        for h in (0, 1):
            nn = chords[bar][(k*2 + h) % 4] + (12 if (k*2 + h) % 8 >= 4 else 0)
            put(marimba(noteHz(nn)), t + h*B/2, .22*level, (-.4 if h else .4), .35)
        if k % 4 == 0: put(pad([noteHz(n) for n in chords[bar]], 4*B + .05), t, level, 0, .4)
        k += 1


def _reverb(x):
    ir_t = tt(2.2); ir = rng.standard_normal(len(ir_t))*np.exp(-ir_t/.55); ir = fft_filter(ir, hi=6000)
    n = len(x) + len(ir); X = np.fft.rfft(x, n); I = np.fft.rfft(ir, n); return np.fft.irfft(X*I, n)[:len(x)]*.05


def master(path='sound.wav', fade_out=.6, drive=1.6, ceiling=.89):
    """Reverb return + soft clip + fade-out; writes 48 kHz 16-bit stereo WAV."""
    L2 = L + _reverb(VL); R2 = R + _reverb(VR)
    fade = np.ones(N); fl = int(fade_out*SR); fade[-fl:] = np.linspace(1, 0, fl)
    mix = np.stack([L2, R2], 1)*fade[:, None]
    mix = np.tanh(mix/(np.max(np.abs(mix)) + 1e-9)*drive)
    mix = mix/np.max(np.abs(mix))*ceiling
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
    print('wrote', path)


def silence(path, dur):
    """Silent track (for the 'no sound' variant — keeps an audio stream so players behave)."""
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(np.zeros(int(dur*SR)*2, np.int16).tobytes())
