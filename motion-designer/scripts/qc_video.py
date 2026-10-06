"""qc_video.py — independent QC of a finished MP4 (run it on EVERY final render, then look at the sheets yourself).

  python3 qc_video.py final.mp4 --vo source/vo/narration.wav --words source/vo/words.json --script source/vo/script.txt

1. AUDIO OFFSET  — cross-correlates the MP4 audio with the narration master (must be ~0 ms)
2. WHAT IS SAID  — transcribes the MP4 with Whisper (mlx-whisper, local) and diffs it against the script: catches
                   misreadings that change the meaning (a word read as a different word), doubled or
                   swallowed words, a keyword pronounced wrong
3. PAUSES        — gaps > 0.35 s inside a sentence in the TTS word timings (an unnatural "this whole, .., room")
4. PICTURE       — near-black/near-white flashes, frozen runs > 1.5 s, the biggest frame jumps (check those cuts)
5. LOUDNESS      — integrated LUFS / true peak (target −14.5 LUFS, TP ≤ −1)
6. SHEETS        — 4 fps contact sheets → qc_out/sheets/sNN.png  (Read EVERY sheet: overlaps, cut objects, empty
                   frames, grey frames, unreadable text, captions over images)
pip install mlx-whisper (Apple Silicon) — first run downloads whisper-large-v3-turbo (~1.6 GB).
"""
import argparse, json, os, re, subprocess, unicodedata, wave, difflib
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('video'); ap.add_argument('--vo'); ap.add_argument('--words'); ap.add_argument('--script')
ap.add_argument('--lang', default='pt'); ap.add_argument('--out', default='qc_out')
a = ap.parse_args(); O = a.out; os.makedirs(f'{O}/sheets', exist_ok=True)
norm = lambda w: re.sub(r'[^a-z0-9%]', '', unicodedata.normalize('NFKD', w.lower()).encode('ascii', 'ignore').decode())
ff = lambda *x: subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *x], check=True)
rd = lambda p: (lambda w: np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32))(wave.open(p))
if a.vo:
    ff('-i', a.video, '-vn', '-ac', '1', '-ar', '8000', f'{O}/a8.wav'); ff('-i', a.vo, '-ac', '1', '-ar', '8000', f'{O}/v8.wav')
    x, y = rd(f'{O}/a8.wav'), rd(f'{O}/v8.wav'); n = min(len(x), len(y), 8000 * 30)
    cc = np.fft.irfft(np.fft.rfft(x[:n], 2 * n) * np.conj(np.fft.rfft(y[:n], 2 * n))); lag = (int(np.argmax(np.r_[cc[-800:], cc[:800]])) - 800) / 8000
    print(f'1 AUDIO OFFSET  {lag * 1000:+.1f} ms', 'OK' if abs(lag) < .02 else '!! FIX')
try:
    import mlx_whisper
    ff('-i', a.video, '-vn', '-ac', '1', '-ar', '16000', f'{O}/a16.wav')
    r = mlx_whisper.transcribe(f'{O}/a16.wav', path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language=a.lang)
    said = r['text'].strip(); open(f'{O}/spoken.txt', 'w').write(said); print('2 SPOKEN:', said)
    if a.script:
        ref = re.sub(r'\[[^\]]*\]', '', open(a.script).read())
        A, B = [norm(w) for w in ref.split() if norm(w)], [norm(w) for w in said.split() if norm(w)]
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
            if tag != 'equal': print(f'   DIFF {tag:7s} script[{" ".join(A[i1:i2])}]  heard[{" ".join(B[j1:j2])}]')
        print('   (numbers come back as digits and "pra"→"para" — ignore those; look for changed meaning, doubled/missing words)')
except ImportError: print('2 SKIPPED — pip install mlx-whisper')
if a.words:
    W = json.load(open(a.words)); W = W['words'] if isinstance(W, dict) else W
    bad = [(p_['e'], b_['s'] - p_['e'], p_['w'], b_['w']) for p_, b_ in zip(W, W[1:]) if b_['s'] - p_['e'] > .35 and not re.search(r'[.?!:]$', p_['w'])]
    print(f'3 PAUSES inside sentences: {len(bad)}'); [print(f'   {t:6.2f}s {g:.2f}s  "{x}" → "{z}"') for t, g, x, z in bad]
raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', a.video, '-vf', 'scale=135:240,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 240, 135).astype(np.float32); fps = 60
L = F.mean((1, 2)); D = np.r_[0, np.abs(np.diff(F, axis=0)).mean((1, 2))]
print(f'4 PICTURE {len(F)} frames · near-black {int((L < 4).sum())} · near-white {int((L > 235).sum())}')
run = 0
for i, d in enumerate(D):
    run = run + 1 if d < .05 else 0
    if run == int(1.5 * fps): print(f'   frozen from {(i - run) / fps:.2f}s')
print('   biggest jumps (check these cuts):', ', '.join(f'{i / fps:.2f}s' for i in np.argsort(D)[-10:][::-1]))
lo = subprocess.run(['ffmpeg', '-hide_banner', '-i', a.video, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
k = lo.index('{', lo.index('Parsed_loudnorm')); j = json.loads(lo[k:lo.index('}', k) + 1])
print(f"5 LOUDNESS {j['input_i']} LUFS · true peak {j['input_tp']} dBTP")
ff('-i', a.video, '-vf', 'fps=4,scale=216:-1,tile=8x6', f'{O}/sheets/s%02d.png')
print(f'6 SHEETS → {O}/sheets/ — Read every one before calling it done')
