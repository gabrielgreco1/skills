"""el_voices.py — pick an ElevenLabs narrator BY EAR, for free (listing + preview MP3s cost 0 credits).

  python3 el_voices.py --lang pt --accent brazilian --out voice-tests          # top 14 by usage, previews downloaded
  python3 el_voices.py --lang en --accent american --gender male --use narrative_story
  python3 el_voices.py --lang es --n 20

Writes <out>/NN_<G>_<Name>.mp3 + <out>/voices.md (name · style · voice_id) and opens the folder in Finder.
Needs a key with "Voices: Read" (+ "Text to Speech" to generate later). Library (community) voices need a PAID plan
to be used through the API — a free plan returns 402 "Free users cannot use library voices via the API" (no charge).
Professional voices (PVC) run on eleven_v3 with use_pvc_as_ivc (el_tts.py --pvc-as-ivc).
Never pick voices that imitate real celebrities — unauthorized clones are a legal and platform risk.
"""
import argparse, json, os, re, subprocess, urllib.parse
ap = argparse.ArgumentParser(); ap.add_argument('--lang', default='pt'); ap.add_argument('--accent'); ap.add_argument('--gender')
ap.add_argument('--use', help='narrative_story | social_media | informative_educational | advertisement | conversational | entertainment_tv')
ap.add_argument('--n', type=int, default=14); ap.add_argument('--out', default='voice-tests')
a = ap.parse_args()
key = os.environ.get('ELEVENLABS_API_KEY') or open(os.path.expanduser('~/.config/elevenlabs/api_key')).read().strip()
q = {'language': a.lang, 'page_size': 100, 'sort': 'usage_character_count_1y'}
if a.accent: q['accent'] = a.accent
if a.gender: q['gender'] = a.gender
if a.use: q['use_cases'] = a.use
r = subprocess.run(['curl', '-s', 'https://api.elevenlabs.io/v1/shared-voices?' + urllib.parse.urlencode(q), '-H', 'xi-api-key: ' + key], capture_output=True, text=True)
d = json.loads(r.stdout)
if 'voices' not in d: raise SystemExit(f"API error: {d.get('detail', d)} (needs the 'Voices: Read' permission)")
os.makedirs(a.out, exist_ok=True); md = ['| # | name | gender/age | style | use | voice_id |', '|---|---|---|---|---|---|']
for i, v in enumerate(d['voices'][:a.n], 1):
    name = re.sub(r'[^A-Za-z0-9]+', '-', v['name'].split(' - ')[0]).strip('-')
    f = f"{a.out}/{i:02d}_{(v.get('gender') or '?')[0].upper()}_{name}.mp3"
    if v.get('preview_url'): subprocess.run(['curl', '-sfL', v['preview_url'], '-o', f])
    md.append(f"| {i:02d} | {v['name']} | {v.get('gender')}/{v.get('age')} | {v.get('descriptive') or ''} | {v.get('use_case') or ''} | `{v['voice_id']}` |")
    print(f"{i:02d}  {v['name'][:48]:48s} {v.get('gender', ''):6s} {v.get('use_case') or '':24s} {v['voice_id']}")
open(f'{a.out}/voices.md', 'w').write('\n'.join(md) + '\n'); subprocess.run(['open', a.out]) if os.environ.get('NO_OPEN') is None else None
