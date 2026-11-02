#!/usr/bin/env python3
"""Monta o A-roll a partir de takes de câmera cortados por palavra.

Entrada: uma EDL em JSON, escrita depois de ler as transcrições do transcribe.py:
{
  "takes": "~/videos/meu-video/takes",          # saída do transcribe.py: link do vídeo + .wav + .words.json
  "out":   "~/videos/meu-video/source",
  "items": [ {"take": "take_01", "ranges": [[0, 14]]},           # índices de palavra, inclusivos
             {"take": "take_02", "ranges": [[0, 28], [30, 39]]} ],
  "punch_in": 1.08,       # jump cut: cortes seguidos do mesmo take alternam 1.0 / punch_in
  "crop_y": 0.62,         # onde o crop vertical cai quando há zoom (0 = topo, 1 = base)
  "max_gap": 0.30,        # silêncio interno maior que isso é encurtado...
  "keep_gap": 0.14,       # ...para isso
  "grade": "eq=saturation=1.12:contrast=1.04"
}
As bordas de cada trecho vêm da energia do áudio, não do Whisper (a transcrição corta números longos no meio):
o trecho começa onde a voz começa e termina onde ela realmente para. Corte nunca na respiração.

Saída em <out>: aroll.mov (1080×1920, 60 fps, PCM), aroll_words.json (palavras no tempo do A-roll, com take e índice
de origem — a legenda usa isso e nunca junta palavras de takes diferentes num bloco), segments.json, clips/.
uso: cut_aroll.py edl.json
"""
import glob, json, os, subprocess, sys, wave
import numpy as np

HOP = .01


def load_voiced(wav):
    w = wave.open(wav); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    n = len(a) // 160; r = np.sqrt((a[:n * 160].reshape(n, 160) ** 2).mean(1))
    r = np.convolve(r, np.ones(3) / 3, 'same'); thr = max(np.percentile(r, 10) * 3.0, np.percentile(r, 99) * .045)
    return r > thr, len(a) / 16000


def voiced_bounds(v, s, e, lo, hi):
    i, j = int(s / HOP), min(len(v) - 1, int(e / HOP))
    while i > 0 and v[i - 1] and s / HOP - i < 40 and (i - 1) * HOP > lo: i -= 1
    while (j < len(v) - 1 and (v[j + 1] or v[min(len(v) - 1, j + 2)] or v[min(len(v) - 1, j + 3)])
           and j - e / HOP < 80 and (j + 2) * HOP < hi): j += 1
    return i * HOP, (j + 1) * HOP


def media(T, take):
    for ext in ('MOV', 'mov', 'mp4', 'MP4', 'm4v'):
        p = f'{T}/{take}.{ext}'
        if os.path.exists(p): return p
    hits = glob.glob(f'{T}/{take}.*'); hits = [h for h in hits if not h.endswith(('.wav', '.json', '.jpg'))]
    if hits: return hits[0]
    sys.exit(f'take não encontrado: {take} em {T}')


def main():
    E = json.load(open(sys.argv[1])); T = os.path.expanduser(E['takes']); OUT = os.path.expanduser(E['out'])
    pin, cy = E.get('punch_in', 1.08), E.get('crop_y', .62); max_gap, keep = E.get('max_gap', .30), E.get('keep_gap', .14)
    grade = E.get('grade', 'eq=saturation=1.12:contrast=1.04')
    pieces = []
    for it in E['items']:
        take = it['take']; W = json.load(open(f'{T}/{take}.words.json')); v, dur = load_voiced(f'{T}/{take}.wav')
        for a, b in it['ranges']:
            s0 = W[a]['s'] if a else max(W[0]['s'], np.argmax(v) * HOP)
            lo = W[a - 1]['e'] + .02 if a else 0; hi = W[b + 1]['s'] - .02 if b + 1 < len(W) else 1e9
            s, e = voiced_bounds(v, s0, W[b]['e'], lo, hi); s = max(lo, s - .06); e = min(dur, hi, e + .08)
            cur, run = s, None
            for k in range(int(s / HOP), int(e / HOP)):
                if not v[k]: run = k if run is None else run
                else:
                    if run is not None and (k - run) * HOP > max_gap:
                        pieces.append((take, cur, run * HOP + keep / 2)); cur = k * HOP - keep / 2
                    run = None
            pieces.append((take, cur, e))
    merged = []
    for p in pieces:
        if merged and merged[-1][0] == p[0] and p[1] <= merged[-1][2]: merged[-1] = (p[0], merged[-1][1], max(merged[-1][2], p[2]))
        else: merged.append(p)
    spans, t, prev, z = [], 0.0, None, 1.0
    for take, s, e in merged:
        z = (pin if z == 1.0 else 1.0) if take == prev else 1.0; prev = take
        spans.append(dict(take=take, s=round(s, 3), e=round(e, 3), t0=round(t, 3), zoom=z)); t += e - s
    words = []
    for it in E['items']:
        take = it['take']; W = json.load(open(f'{T}/{take}.words.json'))
        for a, b in it['ranges']:
            for i in range(a, b + 1):
                m = (W[i]['s'] + W[i]['e']) / 2
                for sp in spans:
                    if sp['take'] == take and sp['s'] <= m <= sp['e']:
                        words.append(dict(w=W[i]['w'], take=take, i=i,
                                          s=round(sp['t0'] + max(W[i]['s'], sp['s']) - sp['s'], 3),
                                          e=round(sp['t0'] + min(W[i]['e'], sp['e']) - sp['s'], 3))); break
    os.makedirs(f'{OUT}/clips', exist_ok=True)
    for f in glob.glob(f'{OUT}/clips/*'): os.remove(f)
    with open(f'{OUT}/clips/list.txt', 'w') as lst:
        for k, sp in enumerate(spans):
            d, z = sp['e'] - sp['s'], sp['zoom']
            vf = (f"scale={round(1080*z/2)*2}:{round(1920*z/2)*2}:flags=lanczos,crop=1080:1920:(iw-1080)/2:(ih-1920)*{cy},"
                  f"fps=60,{grade},format=yuv420p")
            subprocess.run(['nice', '-n', '15', 'ffmpeg', '-v', 'error', '-y', '-ss', f"{sp['s']:.3f}", '-i', media(T, sp['take']),
                            '-t', f'{d:.3f}', '-vf', vf,
                            '-af', f'aresample=48000,afade=t=in:d=0.006,afade=t=out:st={max(0, d - .006):.3f}:d=0.006',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-c:a', 'pcm_s16le', f'{OUT}/clips/c{k:02d}.mov'],
                           check=True)
            lst.write(f"file 'c{k:02d}.mov'\n")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', f'{OUT}/clips/list.txt', '-c', 'copy',
                    f'{OUT}/aroll.mov'], check=True)
    json.dump(words, open(f'{OUT}/aroll_words.json', 'w'), ensure_ascii=False, indent=0)
    json.dump(spans, open(f'{OUT}/segments.json', 'w'), indent=1)
    print(f'A-roll: {t:.2f} s em {len(spans)} trechos → {OUT}/aroll.mov')


if __name__ == '__main__':
    main()
