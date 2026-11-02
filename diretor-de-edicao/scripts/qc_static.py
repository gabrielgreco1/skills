#!/usr/bin/env python3
"""Acha trechos de tela parada num vídeo (o sinal que derrubava a retenção entre 8 e 25 s).

Lê o vídeo em cinza a 5 fps em 270×480, mede a diferença média entre quadros seguidos e lista todo trecho em que a
imagem quase não muda por mais de --min segundos. Também imprime, de 8 a 25 s, quantos segundos ficaram parados.

uso: qc_static.py video.mp4 [--min 1.5] [--thr 0.6] [--from 0] [--to 0]
"""
import argparse, subprocess, sys
import numpy as np

W, H, FPS = 270, 480, 5


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--min', type=float, default=1.5)
    ap.add_argument('--thr', type=float, default=.6, help='diferença média (0–255) abaixo da qual o quadro conta como parado')
    ap.add_argument('--from', dest='t0', type=float, default=0); ap.add_argument('--to', dest='t1', type=float, default=0)
    a = ap.parse_args()
    cmd = ['ffmpeg', '-v', 'error', '-ss', str(a.t0), '-i', a.video] + (['-t', str(a.t1 - a.t0)] if a.t1 else []) + \
          ['-vf', f'fps={FPS},scale={W}:{H},format=gray', '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.int16)
    if len(fr) < 2: sys.exit('vídeo curto demais')
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    still = d < a.thr
    runs, i = [], 0
    while i < len(still):
        if still[i]:
            j = i
            while j < len(still) and still[j]: j += 1
            s, e = a.t0 + i / FPS, a.t0 + (j + 1) / FPS
            if e - s >= a.min: runs.append((s, e))
            i = j
        else: i += 1
    print(f'{len(runs)} trecho(s) parado(s) ≥ {a.min} s')
    for s, e in runs: print(f'  {s:6.1f}–{e:6.1f} s  ({e - s:.1f} s)')
    win = sum(max(0, min(e, 25) - max(s, 8)) for s, e in runs)
    print(f'parado entre 8 e 25 s: {win:.1f} s')


if __name__ == '__main__':
    main()
