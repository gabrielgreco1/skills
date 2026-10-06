"""beat_map.py — map a song for a beat edit: tempo, bass hits, the drop and the silences.

  python3 beat_map.py song.wav --out beats.json            # analyse
  python3 beat_map.py song.wav --out beats.json --start 12.5 --dur 35   # analyse a section only

Writes beats.json (and beats.js for the timeline) = {dur, bpm, beat, hits:[…], drop, quiet:[[a,b],…], energy:[…]} with every time snapped to 1/60 s,
so every cut lands on a 60 fps frame (tmix motion blur never mixes two shots). Prints a readable map:
  hits  = bass-band onsets (kick / 808): put a cut, a word slam, a zoom punch or a shake on each one
  drop  = the biggest jump in low-end energy: the hero reveal goes exactly here
  quiet = stretches where the bass drops out (pre-drop gap, music cut): the punchline / silence moments
"""
import argparse, json, subprocess, tempfile, os, wave
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--out', default='beats.json')
ap.add_argument('--start', type=float, default=0); ap.add_argument('--dur', type=float)
ap.add_argument('--sens', type=float, default=2.2, help='onset threshold in std devs (lower = more hits)')
a = ap.parse_args()
SR = 48000
tmp = tempfile.mktemp(suffix='.wav')
cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(a.start), '-i', a.audio] + (['-t', str(a.dur)] if a.dur else []) + ['-ac', '1', '-ar', str(SR), tmp]
subprocess.run(cmd, check=True)
w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768; w.close(); os.remove(tmp)
q = lambda v: round(round(v * 60) / 60, 4)
n, h = 1024, 512
F = np.array([np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n))) for i in range(0, len(x) - n, h)])
freqs = np.fft.rfftfreq(n, 1 / SR); lowband = freqs < 200
flux = np.maximum(F[1:] - F[:-1], 0)[:, lowband].sum(1); flux = (flux - flux.mean()) / (flux.std() + 1e-9)
hits = []
for i in range(1, len(flux) - 1):
    if flux[i] > a.sens and flux[i] >= flux[i - 1] and flux[i] >= flux[i + 1]:
        t = (i + 1) * h / SR
        if not hits or t - hits[-1] > .15: hits.append(t)
# tempo from the median inter-hit interval (folded into 70–180 BPM)
iv = np.diff(hits); beat = float(np.median(iv)) if len(iv) else .5
while beat < 60 / 180: beat *= 2
while beat > 60 / 70: beat /= 2
# low-end energy per 0.25 s, drop = biggest rise, quiet = bass below 35% of median
step = int(.25 * SR); en = []
for i in range(0, len(x) - step, step):
    S = np.abs(np.fft.rfft(x[i:i + step])); f = np.fft.rfftfreq(step, 1 / SR); en.append(float(S[f < 150].sum()))
en = np.array(en); med = np.median(en) + 1e-9
rise = [en[i + 2:i + 6].mean() - en[max(0, i - 4):i].mean() for i in range(4, len(en) - 6)]
drop_i = int(np.argmax(rise)) + 4 if rise else 0
drop = q(min(hits, key=lambda t: abs(t - drop_i * .25)) if hits else drop_i * .25)
quiet, run = [], None
for i, e in enumerate(en):
    if e < .35 * med: run = run if run is not None else i
    elif run is not None:
        if i - run >= 2: quiet.append([q(run * .25), q(i * .25)])
        run = None
if run is not None and len(en) - run >= 2: quiet.append([q(run * .25), q(len(en) * .25)])
out = {'dur': q(len(x) / SR), 'bpm': round(60 / beat, 1), 'beat': round(beat, 4), 'hits': [q(t) for t in hits],
       'drop': drop, 'quiet': quiet, 'energy': [round(float(e / med), 2) for e in en]}
json.dump(out, open(a.out, 'w'), indent=1)
open(os.path.splitext(a.out)[0] + '.js', 'w').write('window.BEATS=' + json.dumps(out) + ';\n')   # <script src="beats.js"> for the timeline
print(f"dur {out['dur']} s · ~{out['bpm']} BPM (beat {out['beat']} s) · {len(hits)} bass hits · DROP at {drop} s")
print('quiet (no bass):', quiet)
print('hits:', ' '.join(f'{t:.2f}' for t in out['hits']))
