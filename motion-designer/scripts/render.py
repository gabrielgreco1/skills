"""render.py — capture a deterministic HTML timeline (window.seek(t)) into frames with Playwright.

  python3 render.py timeline.html --ar 16x9 --test 0.5,2,4.2,8     # stills → test_16x9/ (+ sheet.png)
  python3 render.py timeline.html --ar 9x16 --fps 240               # full run → frames_9x16/%05d.jpg
  python3 render.py timeline.html --ar 1x1 --fps 240 --range 12.0,14.5   # re-render a slice only
  python3 render.py timeline.html --ar 16x9 --fps 30 --scale .5     # quick low-res animated draft
  python3 render.py timeline.html --ar 9x16 --sweep 10              # layout check only, whole timeline at 10 fps

Layout checks (in --test and --sweep): every visible text must sit inside the platform safe box, must not overlap
another text block, must not sit on top of a [data-role=focal] element (image/3D/chart the viewer must SEE), and focal
elements must not be cut by the frame edge. Opt-outs: [data-bleed] (backgrounds/textures), [data-over] (text that is
deliberately on a scrim over a full-bleed photo), [data-nocheck]. Text blocks = nearest .hl / [data-block] /
[data-role=caption] ancestor (words of one headline don't count as overlapping each other).
3D: expose window.FOCAL_BOXES = () => [{x,y,w,h,name}] with the projected screen boxes of hero objects.

The page must: read ?ar=, set window.DUR, define window.seek(t) (pure function of t) and set
window.ready = true once fonts/assets are loaded. 240 fps capture + tmix=4 in encode.sh gives
real motion blur at 60 fps. Workers default to 3 parallel pages (keeps the machine usable; run under `nice -n 15`).
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright

SIZES = {'16x9': (1920, 1080), '1x1': (1080, 1080), '4x5': (1080, 1350), '9x16': (1080, 1920)}

ap = argparse.ArgumentParser()
ap.add_argument('html'); ap.add_argument('--ar', default='16x9', help='16x9 | 1x1 | 4x5 | 9x16 | custom WxH (e.g. 1200x628)')
ap.add_argument('--fps', type=int, default=240); ap.add_argument('--test')
ap.add_argument('--range'); ap.add_argument('--out'); ap.add_argument('--workers', type=int, default=3)
ap.add_argument('--sweep', type=float, help='check layout over the whole timeline at N fps (no frames saved)')
CHECK_JS = r"""(() => { const B = window.SAFE_BOX, FW = innerWidth, FH = innerHeight, out = [];
  const vis = el => el.checkVisibility({opacityProperty: true, visibilityProperty: true}) && +getComputedStyle(el).opacity > .05;
  const hit = (a, b, m = 2) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > m && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > m;
  const T = [], w = document.createTreeWalker(document.getElementById('stage'), NodeFilter.SHOW_TEXT);
  while (w.nextNode()) { const n = w.currentNode, txt = n.textContent.trim(), el = n.parentElement;
    if (!txt || el.closest('#guides,[data-bleed],[data-nocheck]') || !vis(el)) continue;
    const r = document.createRange(); r.selectNodeContents(n);
    const blk = el.closest('.hl,[data-block],[data-role=caption]') || el;
    for (const q of r.getClientRects()) if (q.width > 1 && q.height > 1) T.push({q, blk, txt: txt.slice(0, 30), over: !!el.closest('[data-over]')}); }
  for (const a of T) if (B && (a.q.left < B.x - 2 || a.q.top < B.y - 2 || a.q.right > B.x + B.w + 2 || a.q.bottom > B.y + B.h + 2)) out.push(`OUTSIDE SAFE ZONE  "${a.txt}"`);
  for (let i = 0; i < T.length; i++) for (let j = i + 1; j < T.length; j++)
    if (T[i].blk !== T[j].blk && hit(T[i].q, T[j].q)) out.push(`TEXT OVERLAP  "${T[i].txt}" x "${T[j].txt}"`);
  const F = [...document.querySelectorAll('[data-role=focal]')].filter(e => vis(e) && !e.closest('[data-nocheck]'))
    .map(e => ({q: e.getBoundingClientRect(), name: e.dataset.name || e.className || e.tagName, bleed: e.hasAttribute('data-bleed')}));
  for (const f of (window.FOCAL_BOXES ? window.FOCAL_BOXES() : [])) F.push({q: {left: f.x, top: f.y, right: f.x + f.w, bottom: f.y + f.h}, name: f.name || '3d'});
  for (const f of F) { if (!f.bleed && (f.q.left < -2 || f.q.top < -2 || f.q.right > FW + 2 || f.q.bottom > FH + 2)) out.push(`CUT OFF BY FRAME  [${f.name}]`);
    for (const a of T) if (!a.over && hit(a.q, f.q, 6)) out.push(`TEXT OVER IMAGE  "${a.txt}" on [${f.name}]`); }
  return [...new Set(out)]; })()"""
unsafe = []
ap.add_argument('--scale', type=float, default=1.0, help='device scale factor (0.5 = half-res draft)')
a = ap.parse_args()
W, H = SIZES[a.ar] if a.ar in SIZES else map(int, a.ar.lower().split('x'))
URL = 'file://' + os.path.abspath(a.html) + f'?ar={a.ar}'


async def worker(b, jobs, out, errs):
    pg = await b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=a.scale)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    await pg.goto(URL); await pg.wait_for_function('window.ready===true', timeout=60000)
    await pg.evaluate('document.fonts.ready')
    for name, t in jobs:
        await pg.evaluate(f'seek({t})')
        if a.test or a.sweep:
            for b_ in await pg.evaluate(CHECK_JS): unsafe.append(f'{t:6.2f}s  {b_}')
            if a.test: await pg.screenshot(path=f'{out}/{name}.png')
        else: await pg.screenshot(path=f'{out}/{name}.jpg', type='jpeg', quality=94)


async def main():
    async with async_playwright() as p:
        # Metal GPU WebGL (Three.js ~20 ms/frame) + file:// textures/GLB/ES modules
        b = await p.chromium.launch(args=['--force-color-profile=srgb', '--font-render-hinting=none', '--allow-file-access-from-files',
                                          '--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
        if a.test:
            out = a.out or f'test_{a.ar}'
            times = [(f't{float(x):06.2f}', float(x)) for x in a.test.split(',')]
        elif a.sweep:
            out = a.out or 'sweep'
            pg = await b.new_page(); await pg.goto(URL); await pg.wait_for_function('window.ready===true', timeout=60000)
            dur = await pg.evaluate('window.DUR'); await pg.close()
            times = [(f's{i:05d}', i / a.sweep) for i in range(int(dur * a.sweep))]
        else:
            out = a.out or f'frames_{a.ar}'
            pg = await b.new_page(); await pg.goto(URL); await pg.wait_for_function('window.ready===true', timeout=60000)
            dur = await pg.evaluate('window.DUR'); await pg.close()
            i0, i1 = 0, int(round(dur * a.fps))
            if a.range:
                r0, r1 = map(float, a.range.split(',')); i0, i1 = int(r0 * a.fps), min(i1, int(r1 * a.fps) + 1)
            times = [(f'{i:05d}', i / a.fps) for i in range(i0, i1)]
        if not a.sweep: os.makedirs(out, exist_ok=True)
        n = max(1, min(a.workers, len(times))); errs = []
        await asyncio.gather(*[worker(b, times[k::n], out, errs) for k in range(n)])
        await b.close()
    if unsafe:
        print(f'LAYOUT PROBLEMS ({len(unsafe)}) — fix every one before encoding:', *sorted(unsafe)[:60], sep='\n  ')
        if len(unsafe) > 60: print(f'  … and {len(unsafe) - 60} more')
    elif a.test or a.sweep: print('layout: OK (safe zone, no text overlap, no text over images, nothing cut)')
    if errs: print('PAGE ERRORS:', *sorted(set(errs))[:8], sep='\n  ')
    if a.sweep: print(f'{len(times)} instants checked'); sys.exit(1 if unsafe else 0)
    print(f'{len(times)} frames -> {out}/')
    if a.test:
        os.system(f'python3 "{os.path.dirname(os.path.abspath(__file__))}/sheet.py" "{out}"')

asyncio.run(main())
