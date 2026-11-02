#!/usr/bin/env python3
"""Transcreve takes de câmera com tempo por palavra (mlx-whisper, local).

Para cada vídeo: cria um link simbólico dele em --out (se estiver em outra pasta), extrai o áudio em 16 kHz mono (<nome>.wav), transcreve com whisper-large-v3-turbo e grava
<nome>.words.json = [{"i": 0, "w": "Você", "s": 0.48, "e": 0.71}, ...]. Também imprime a transcrição numerada
("[12]palavra"), que é o que se usa para montar a EDL do cut_aroll.py, a duração e o primeiro ataque de voz.

uso: transcribe.py <video ou pasta> [...] [--out DIR] [--lang pt] [--force]
"""
import argparse, glob, json, os, subprocess, sys, wave
import numpy as np

VID = ('.mov', '.mp4', '.m4v', '.MOV', '.MP4')


def onset(wav):
    """Primeiro ataque de voz pela envoltória RMS em janelas de 20 ms (o corte do gancho entra aqui, nunca na respiração)."""
    w = wave.open(wav); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    n = len(a) // 320; r = np.sqrt((a[:n * 320].reshape(n, 320) ** 2).mean(1))
    thr = max(np.percentile(r, 10) * 3, np.percentile(r, 99) * .06)
    k = int(np.argmax(r > thr)); return round(k * .02, 2), round(len(a) / 16000, 2)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('src', nargs='+'); ap.add_argument('--out')
    ap.add_argument('--lang', default='pt'); ap.add_argument('--force', action='store_true'); a = ap.parse_args()
    files = []
    for s in a.src:
        s = os.path.expanduser(s)
        files += sorted(f for f in glob.glob(os.path.join(s, '*')) if f.endswith(VID)) if os.path.isdir(s) else [s]
    if not files: sys.exit('nenhum vídeo encontrado')
    try:
        import mlx_whisper
    except ImportError:
        sys.exit('pip install mlx-whisper (Apple Silicon); o primeiro uso baixa o whisper-large-v3-turbo (~1,6 GB)')
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]; out = os.path.expanduser(a.out) if a.out else os.path.dirname(f)
        os.makedirs(out, exist_ok=True); wav = f'{out}/{base}.wav'; js = f'{out}/{base}.words.json'
        link = os.path.join(out, os.path.basename(f))   # o cut_aroll.py acha o vídeo em takes/ sem mover nada de ~/Downloads
        if os.path.realpath(os.path.dirname(f)) != os.path.realpath(out) and not os.path.lexists(link):
            os.symlink(os.path.abspath(f), link)
        if not os.path.exists(wav) or a.force:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', wav], check=True)
        if not os.path.exists(js) or a.force:
            r = mlx_whisper.transcribe(wav, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language=a.lang,
                                       word_timestamps=True, condition_on_previous_text=False)
            W = [dict(w=x['word'].strip(), s=round(x['start'], 3), e=round(x['end'], 3))
                 for seg in r['segments'] for x in seg.get('words', []) if x['word'].strip()]
            for i, x in enumerate(W): x['i'] = i
            json.dump(W, open(js, 'w'), ensure_ascii=False, indent=0)
        W = json.load(open(js)); on, dur = onset(wav)
        print(f'\n== {base}  ({dur} s, voz começa em {on} s, {len(W)} palavras) → {js}')
        print(' '.join(f"[{x['i']}]{x['w']}" for x in W))


if __name__ == '__main__':
    main()
