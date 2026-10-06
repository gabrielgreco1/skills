"""slowed_reverb.py — the classic edit treatment: slowed (pitch + tempo down together), heavier low end, big dark reverb.

  python3 slowed_reverb.py song.mp3 out.wav                     # 0.85× speed, reverb 0.42
  python3 slowed_reverb.py song.mp3 out.wav --speed .8 --wet .5 # more dragged and wetter
  python3 slowed_reverb.py song.mp3 out.wav --speed 1.15 --wet 0  # "sped up" / nightcore instead
  python3 slowed_reverb.py song.mp3 out.wav --start 30 --dur 40  # only a section of the song

Run beat_map.py on the OUTPUT (the slowed file) — all timings change with the speed.
"""
import argparse, subprocess, tempfile, os, wave
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('src'); ap.add_argument('out')
ap.add_argument('--speed', type=float, default=.85); ap.add_argument('--wet', type=float, default=.42)
ap.add_argument('--bass', type=float, default=5, help='low-shelf boost in dB at 70 Hz')
ap.add_argument('--start', type=float, default=0); ap.add_argument('--dur', type=float)
ap.add_argument('--decay', type=float, default=.9, help='reverb decay (s); bigger = longer tail')
a = ap.parse_args(); SR = 48000
tmp = tempfile.mktemp(suffix='.wav')
af = f'asetrate={SR}*{a.speed},aresample={SR},bass=g={a.bass}:f=70' + (',lowpass=f=9000' if a.speed < 1 else '')
cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(a.start), '-i', a.src] + (['-t', str(a.dur / a.speed if a.speed else a.dur)] if a.dur else []) + ['-af', af, '-ac', '2', '-ar', str(SR), tmp]
subprocess.run(cmd, check=True)
w = wave.open(tmp); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float).reshape(-1, 2) / 32768; w.close(); os.remove(tmp)
out = x
if a.wet > 0:
    rng = np.random.default_rng(3)
    def ir():
        t = np.arange(int(3.2 * SR)) / SR; n = rng.standard_normal(len(t)) * np.exp(-t / a.decay)
        X = np.fft.rfft(n); f = np.fft.rfftfreq(len(n), 1 / SR); X *= 1 / (1 + (f / 4000) ** 2); return np.fft.irfft(X, len(n))
    def conv(s, k):
        m = len(s) + len(k); return np.fft.irfft(np.fft.rfft(s, m) * np.fft.rfft(k, m), m)[:len(s)]
    pd = int(.035 * SR)
    wet = np.stack([np.concatenate([np.zeros(pd), conv(x[:, c], ir())])[:len(x)] for c in (0, 1)], 1)
    wet /= np.max(np.abs(wet)) + 1e-9
    out = x * (1 - a.wet * .5) + wet * a.wet * np.max(np.abs(x))
out = np.tanh(out * 1.3); out /= np.max(np.abs(out)) + 1e-9; out *= .92
o = wave.open(a.out, 'wb'); o.setnchannels(2); o.setsampwidth(2); o.setframerate(SR); o.writeframes((out * 32767).astype(np.int16).tobytes()); o.close()
print(f'wrote {a.out} · {len(out) / SR:.2f} s · speed {a.speed} · wet {a.wet}')
