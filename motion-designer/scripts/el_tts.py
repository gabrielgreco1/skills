"""el_tts.py — ElevenLabs narration with word timings, cache and a hard credit budget.

  python3 el_tts.py vo/script.txt --voice <voice_id> --budget 1500                 # -> vo/el/c0.mp3 ... + vo/words.json
  python3 el_tts.py vo/script.txt --voice <id> --model eleven_multilingual_v2 --stability .45 --style .25

script.txt: one paragraph per act (blank line between).
DEFAULT = ONE TAKE: the whole script goes in ONE request (v3 ≤ 5,000 chars) → one continuous performance, no energy/pitch
jump between acts; words.json gets an "act" index per word (paragraph). --per-act = one request per paragraph (only
when the script is too long, or to regenerate a single act: --per-act --only N).
Lead 0.20 s of silence is added in front (LEAD) so the first word never starts on frame 0. Audio tags like [curious] are allowed on v3/v4 and are stripped
from the word timings. Chunks are joined with --gap seconds of silence into vo/narration.wav.

Key: $ELEVENLABS_API_KEY or ~/.config/elevenlabs/api_key (never write it into the project).
Cost ≈ 1 credit per character (tags included). Every response is cached in vo/el/ — a chunk is regenerated only if
its text changed (or you delete its files). Each request is logged in vo/el/credits.log; the run stops before
exceeding --budget. Test ONE short chunk first (--only 0), listen, then run the rest.
Writing rules (craft.md §7): no "..." or commas in the middle of a sentence; pauses only between sentences;
CAPS on one word for emphasis; numbers/acronyms spelled as spoken; tags only at 3–5 turning points.
"""
import argparse, base64, hashlib, json, os, re, subprocess, sys, wave

ap = argparse.ArgumentParser()
ap.add_argument('script'); ap.add_argument('--voice', required=True)
ap.add_argument('--model', default='eleven_v3'); ap.add_argument('--stability', type=float, default=0.3)
ap.add_argument('--similarity', type=float, default=0.8); ap.add_argument('--style', type=float)
ap.add_argument('--speed', type=float); ap.add_argument('--seed', type=int, default=7)
ap.add_argument('--pvc-as-ivc', action='store_true', help='use for professional (PVC) voices on eleven_v3/v4')
ap.add_argument('--budget', type=int, required=True, help='max credits (characters) this run may spend')
ap.add_argument('--gap', type=float, default=0.35); ap.add_argument('--only', type=int)
ap.add_argument('--per-act', action='store_true', help='one request per paragraph instead of one take')
a = ap.parse_args()

key = os.environ.get('ELEVENLABS_API_KEY') or open(os.path.expanduser('~/.config/elevenlabs/api_key')).read().strip()
d = os.path.dirname(os.path.abspath(a.script)); out = os.path.join(d, 'el'); os.makedirs(out, exist_ok=True)
acts = [c.strip() for c in re.split(r'\n\s*\n', open(a.script).read()) if c.strip()]
chunks = acts if a.per_act else ['\n\n'.join(acts)]
LEAD = .20
log = open(os.path.join(out, 'credits.log'), 'a'); spent = 0

def gen(i, text):
    global spent
    h = hashlib.sha1(f'{a.voice}|{a.model}|{a.stability}|{a.similarity}|{a.style}|{a.speed}|{a.seed}|{text}'.encode()).hexdigest()[:10]
    mp3, js = f'{out}/c{i}_{h}.mp3', f'{out}/c{i}_{h}.json'
    if os.path.exists(js): return mp3, json.load(open(js))
    if spent + len(text) > a.budget: sys.exit(f'STOP: chunk {i} ({len(text)} chars) would exceed the budget ({spent}/{a.budget})')
    vs = {'stability': a.stability, 'similarity_boost': a.similarity}
    if a.style is not None: vs['style'] = a.style
    if a.speed is not None: vs['speed'] = a.speed
    body = {'text': text, 'model_id': a.model, 'voice_settings': vs, 'seed': a.seed}
    if a.pvc_as_ivc: body['use_pvc_as_ivc'] = True
    r = subprocess.run(['curl', '-s', '-w', '\n%{http_code}', '-X', 'POST',
                        f'https://api.elevenlabs.io/v1/text-to-speech/{a.voice}/with-timestamps?output_format=mp3_44100_128',
                        '-H', 'xi-api-key: ' + key, '-H', 'Content-Type: application/json', '-d', json.dumps(body)],
                       capture_output=True, text=True)
    res, code = r.stdout.rsplit('\n', 1)
    if code != '200': sys.exit(f'chunk {i}: HTTP {code} {res[:300]}  (refused requests are not billed)')
    j = json.loads(res); open(mp3, 'wb').write(base64.b64decode(j.pop('audio_base64'))); json.dump(j, open(js, 'w'))
    spent += len(text); log.write(f'c{i}\t{a.model}\t{len(text)} chars\n'); log.flush()
    return mp3, j

def words(al, off, act0=0):
    """character alignment -> [{w,s,e,act}], audio tags removed; a blank line in the text = next act."""
    ch, st, en = al['characters'], al['character_start_times_seconds'], al['character_end_times_seconds']
    res, cur, tag, act, nl = [], None, False, act0, 0
    for c, s, e in zip(ch, st, en):
        if c == '\n':
            nl += 1
            if nl == 2: act += 1
        elif not c.isspace(): nl = 0
        if c == '[': tag = True; continue
        if tag: tag = c != ']'; continue
        if c.isspace():
            if cur: res.append(cur); cur = None
            continue
        if cur is None: cur = {'w': '', 's': round(s + off, 3), 'e': 0, 'act': act}
        cur['w'] += c; cur['e'] = round(e + off, 3)
    if cur: res.append(cur)
    return res

W, wavs, t = [], [], LEAD
for i, text in enumerate(chunks):
    if a.only is not None and i != a.only: continue
    mp3, j = gen(i, text)
    wav = mp3[:-4] + '.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ar', '48000', '-ac', '1', wav], check=True)
    w = wave.open(wav); dur = w.getnframes() / w.getframerate(); w.close()
    W += words(j['alignment'], t, i if a.per_act else 0); wavs.append((wav, t)); t += dur + a.gap
    print(f'c{i}  {dur:5.2f}s  "{text[:60]}"')
json.dump({'words': W, 'chunks': [{'wav': os.path.basename(p), 'start': s} for p, s in wavs], 'dur': round(t, 3)},
          open(os.path.join(d, 'words.json'), 'w'), ensure_ascii=False, indent=0)
inp = sum([['-i', p] for p, _ in wavs], [])
mix = ''.join(f'[{k}]adelay={int(s * 1000)}|{int(s * 1000)}[a{k}];' for k, (_, s) in enumerate(wavs))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *inp, '-filter_complex',
                mix + ''.join(f'[a{k}]' for k in range(len(wavs))) + f'amix=inputs={len(wavs)}:normalize=0',
                os.path.join(d, 'narration.wav')], check=True)
print(f'credits spent this run: {spent} (budget {a.budget}) · narration {t:.2f}s · {len(W)} words -> words.json')
