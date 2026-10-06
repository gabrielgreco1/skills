"""vo.py — synthesize narration lines with edge-tts (the approved default), trimmed and timed.

  python3 vo.py vo/lines.tsv --voice male-us                          # -> vo/l0.wav, vo/l1.wav ...
  python3 vo.py vo/lines.tsv --voice en-US-AndrewMultilingualNeural --rate +8%

lines.tsv: one line per VO cue, TAB-separated:  start_s <TAB> end_s <TAB> text [<TAB> voice override]
  start/end = the visual window the line must fit in (use timeline MARK times).
The script warns when a line is longer than its window or overlaps the next cue — fix the SCRIPT
(shorter words) or the TIMELINE (hold longer), never speed the voice past +15%.

Approved recipe (2026-10): American Multilingual neural voice, rate +8%, no pitch shift, DRY
(no reverb/echo), silences trimmed. Rejected: British voice, slow rate (-14%), pitch -8 Hz, room reverb.
"""
import argparse, os, subprocess, sys, wave

VOICES = {  # friendly name -> edge-tts voice
    'female-us': 'en-US-AvaMultilingualNeural', 'male-us': 'en-US-AndrewMultilingualNeural',
    'male-us-2': 'en-US-BrianMultilingualNeural', 'female-us-2': 'en-US-EmmaMultilingualNeural',
    'female-ptbr': 'pt-BR-ThalitaMultilingualNeural', 'male-ptbr': 'pt-BR-AntonioNeural',
}
ap = argparse.ArgumentParser(); ap.add_argument('tsv')
ap.add_argument('--voice', required=True, help='the voice the user picked: ' + ', '.join(VOICES)); ap.add_argument('--rate', default='+8%')
a = ap.parse_args()
d = os.path.dirname(os.path.abspath(a.tsv))
rows = [l.rstrip('\n').split('\t') for l in open(a.tsv) if l.strip() and not l.startswith('#')]
ok = True
for i, r in enumerate(rows):
    s, e, text = float(r[0]), float(r[1]), r[2]
    voice = VOICES.get(r[3] if len(r) > 3 and r[3] else a.voice, r[3] if len(r) > 3 and r[3] else VOICES.get(a.voice, a.voice))
    mp3, wav = f'{d}/l{i}.mp3', f'{d}/l{i}.wav'
    subprocess.run(['edge-tts', '--voice', voice, f'--rate={a.rate}', '--text', text, '--write-media', mp3],
                   check=True, capture_output=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-af',
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                    '-ar', '48000', '-ac', '1', wav], check=True)
    w = wave.open(wav); dur = w.getnframes() / w.getframerate(); w.close()
    nxt = float(rows[i + 1][0]) if i + 1 < len(rows) else 1e9
    flag = ''
    if s + dur > e + .15: flag += f'  !! overruns window by {s + dur - e:.2f}s'; ok = False
    if s + dur > nxt - .1: flag += f'  !! collides with next cue'; ok = False
    print(f'l{i}  {s:6.2f}-{e:6.2f}  {dur:5.2f}s  {voice}  "{text[:60]}"{flag}')
print('all lines fit' if ok else 'FIX the flagged lines before mixing')
