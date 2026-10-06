"""mix.py — build the final audio for one variant.

  python3 mix.py --dur 28 --music sound.wav --vo vo/lines.tsv --out narrated.wav   # SFX + narration (ducked)
  python3 mix.py --dur 28 --music sound.wav --out sound.wav                         # SFX only (copy-through)
  python3 mix.py --dur 28 --vo vo/lines.tsv --out vo_only.wav                       # narration only
  python3 mix.py --dur 28 --out silent.wav                                          # no sound

Voice stays DRY (no reverb/echo — echo was explicitly rejected). Music ducks -9 dB under the
voice (≈40 ms attack / 350 ms release).
"""
import argparse, wave
import numpy as np
SR = 48000
ap = argparse.ArgumentParser(); ap.add_argument('--dur', type=float, required=True)
ap.add_argument('--music'); ap.add_argument('--vo'); ap.add_argument('--out', required=True)
ap.add_argument('--duck_db', type=float, default=9.0)
a = ap.parse_args(); N = int(a.dur * SR)


def rd(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    x = x.reshape(-1, w.getnchannels()); w.close()
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    out = np.zeros((N, 2)); n = min(N, len(x)); out[:n] = x[:n]; return out


mus = rd(a.music) if a.music else np.zeros((N, 2))
vo = np.zeros(N)
if a.vo:
    import os
    d = os.path.dirname(os.path.abspath(a.vo))
    rows = [l for l in open(a.vo) if l.strip() and not l.startswith('#')]
    for i, l in enumerate(rows):
        s = int(float(l.split('\t')[0]) * SR); v = rd(f'{d}/l{i}.wav')[:, 0]
        n = min(len(v), N - s); vo[s:s + n] += v[:n]
    vo = vo / (np.max(np.abs(vo)) + 1e-9) * .95
    env = np.convolve(np.abs(vo), np.ones(int(.02 * SR)) / int(.02 * SR), 'same')
    on = (env > .02).astype(float); g = np.zeros(N); s = 0.0
    for i in range(0, N, 48):
        tgt = on[i]; s += (tgt - s) * (.25 if tgt > s else .012); g[i:i + 48] = s
    mus = mus * (10 ** (-a.duck_db * g / 20))[:, None] * .85
out = mus + np.stack([vo, vo], 1) * .9
pk = np.max(np.abs(out))
if pk > 0: out = np.tanh(out * 1.1); out = out / np.max(np.abs(out)) * .9
with wave.open(a.out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype(np.int16).tobytes())
print('wrote', a.out)
