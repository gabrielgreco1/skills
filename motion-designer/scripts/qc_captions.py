"""qc_captions.py — frame-by-frame caption QC on the real timeline (catches what timing checks miss).

  python3 qc_captions.py source/timeline.html --ar 9x16 [--fps 60]

Needs: window.WORDS = [{w,s,e}] (spoken words, Captions() sets it) and one caption container [data-role=caption] whose
children are the word spans. Checks, at every frame:
  1. STABILITY  — a caption word never moves (x/y layout offset) while its chunk is on screen (jumping/ghosting bug)
  2. HARD SWAP  — the word set of the caption box never changes mid-chunk (rebuilt chunk)
  3. HOLD       — every caption word is readable (opacity > .5) for ≥ 0.2 s
  4. ON TIME    — every spoken word not printed elsewhere becomes visible within 0.08 s of being spoken and never
                  more than 0.15 s before
Exit code 1 if anything fails.
"""
import argparse, asyncio, os, re, sys, unicodedata
from playwright.async_api import async_playwright
ap = argparse.ArgumentParser(); ap.add_argument('html'); ap.add_argument('--ar', default='9x16'); ap.add_argument('--fps', type=float, default=60)
a = ap.parse_args()
SIZES = {'16x9': (1920, 1080), '1x1': (1080, 1080), '4x5': (1080, 1350), '9x16': (1080, 1920)}
W, H = SIZES.get(a.ar, (1080, 1920))
norm = lambda w: re.sub(r'[^a-z0-9%]', '', unicodedata.normalize('NFKD', w.lower()).encode('ascii', 'ignore').decode())
JS = r"""(()=>{const c=document.querySelector('[data-role=caption]');if(!c)return null;
  return [...c.children].map(s=>({t:s.textContent,x:s.offsetLeft,y:s.offsetTop,o:+getComputedStyle(s).opacity}));})()"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files', '--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width': W, 'height': H})
        await pg.goto('file://' + os.path.abspath(a.html) + f'?ar={a.ar}'); await pg.wait_for_function('window.ready===true', timeout=300000)
        dur = await pg.evaluate('window.DUR'); words = await pg.evaluate('window.WORDS||[]')
        if not words: sys.exit('window.WORDS missing — expose the spoken word timings (Captions() does it)')
        bad, prev, chunk, seen = [], None, 0, {}
        for i in range(int(dur * a.fps)):
            t = i / a.fps; await pg.evaluate(f'seek({t})'); cur = await pg.evaluate(JS) or []
            sig = '|'.join(x['t'] for x in cur)
            if prev is not None and sig != prev['sig']:
                if any(x['o'] > .3 for x in prev['w']) and any(x['o'] > .3 for x in cur) and set(sig.split('|')) & set(prev['sig'].split('|')):
                    bad.append(f'{t:6.2f}s HARD SWAP  "{prev["sig"]}" -> "{sig}"')
                chunk += 1
            elif prev is not None:
                for u, v in zip(prev['w'], cur):
                    if u['o'] > .02 and v['o'] > .02 and (abs(u['x'] - v['x']) > 1.5 or abs(u['y'] - v['y']) > 1.5):
                        bad.append(f"{t:6.2f}s MOVED  '{v['t']}' {u['x']},{u['y']} -> {v['x']},{v['y']}")
            for j, x in enumerate(cur):
                if x['o'] > .5: seen.setdefault((chunk, j, x['t']), []).append(t)
            prev = {'sig': sig, 'w': cur}
        for (c, j, w), ts in seen.items():
            if len(ts) / a.fps < .2: bad.append(f'{ts[0]:6.2f}s SHORT HOLD  \'{w}\' visible {len(ts) / a.fps:.2f}s')
        # on-time: first frame each caption word instance is readable vs its spoken time (match in order)
        firsts = sorted((ts[0], norm(w)) for (c, j, w), ts in seen.items())
        k = 0
        for wd in words:
            n = norm(wd['w']); m = next((f for f in firsts[k:k + 12] if f[1] == n), None)
            if m is None: continue                       # printed by a headline/end card instead
            k = firsts.index(m) + 1; d = m[0] - wd['s']
            if d > .08 or d < -.15: bad.append(f"{wd['s']:6.2f}s LATE/EARLY '{wd['w']}' shown {d:+.2f}s")
        print(f'{int(dur * a.fps)} frames, {len(seen)} caption word instances, {len(bad)} problems')
        for x in sorted(bad)[:80]: print('  ', x)
        await b.close(); sys.exit(1 if bad else 0)
asyncio.run(main())
