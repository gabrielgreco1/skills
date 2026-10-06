"""fetch_assets.py — download real images / 3D / HDRIs with their licence logged (assets/catalog.md).

  python3 fetch_assets.py threejs --list                    # three.js examples library (models, HDRIs, textures)
  python3 fetch_assets.py threejs DamagedHelmet earth hdr:royal_esplanade_1k --out assets
  python3 fetch_assets.py commons "lighthouse" --list            # search Wikimedia Commons (shows licence per file)
  python3 fetch_assets.py commons "File:<exact file name>.jpg" --out assets
  python3 fetch_assets.py polyhaven hdris --list --q studio  # Poly Haven (all CC0): hdris | textures | models
  python3 fetch_assets.py polyhaven studio_small_09 --res 2k --out assets
  python3 fetch_assets.py nasa "blue marble" --list         # NASA image library (public domain, check the credit)

Every download appends a row to <out>/catalog.md: file · what · source URL · author · licence · attribution · use.
Licence rules (craft.md §8): PD / CC0 / CC BY / CC BY-SA are fine (credit BY/BY-SA in the post caption); never NC or
ND for promotional videos; "editorial only" press images only in non-promotional content; Mixamo characters are fine
inside a video but not as standalone files. When a licence is unknown, the row says VERIFY — don't ship it unverified.
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request
UA = {'User-Agent': 'motion-designer-skill/1.0 (asset fetcher)'}
import subprocess
def get(u, binary=False):   # curl, not urllib: python.org builds on macOS often lack the system CA certificates
    r = subprocess.run(['curl', '-sfL', '--max-time', '180', '-A', UA['User-Agent'], u], capture_output=True)
    if r.returncode: raise RuntimeError(f'download failed ({r.returncode}): {u}')
    return r.stdout if binary else r.stdout.decode('utf-8', 'replace')
def save(u, path):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True); open(path, 'wb').write(get(u, True)); return path
def catalog(out, f, what, src, author, lic, use=''):
    p = os.path.join(out, 'catalog.md'); new = not os.path.exists(p)
    with open(p, 'a') as c:
        if new: c.write('| file | what | source | author | licence | attribution | use |\n|---|---|---|---|---|---|---|\n')
        attr = '' if lic.upper().startswith(('CC0', 'PUBLIC', 'PD')) else f'"{what}" by {author}, {lic}'
        c.write(f'| {os.path.relpath(f, out)} | {what} | {src} | {author} | {lic} | {attr} | {use} |\n')
    print(f'  ✓ {f}  [{lic}]')

# ---------------------------------------------------------------- three.js examples library (r170)
TJ = 'https://raw.githubusercontent.com/mrdoob/three.js/r170/'
THREEJS = {  # name: (path, what, author, licence)  — licences from the repo READMEs / Khronos sample models
 'DamagedHelmet':   ('examples/models/gltf/DamagedHelmet/glTF/', 'sci-fi helmet (PBR showcase)', 'theblueturtle_ (Khronos sample)', 'CC BY 4.0'),
 'BoomBox':         ('examples/models/gltf/BoomBox.glb', 'retro boombox', 'Microsoft (Khronos sample)', 'CC0'),
 'SheenChair':      ('examples/models/gltf/SheenChair.glb', 'velvet chair', 'Wayfair (Khronos sample)', 'CC BY 4.0'),
 'IridescenceLamp': ('examples/models/gltf/IridescenceLamp.glb', 'iridescent lamp', 'Wayfair (Khronos sample)', 'CC BY 4.0'),
 'AnisotropyBarnLamp': ('examples/models/gltf/AnisotropyBarnLamp.glb', 'brushed-metal barn lamp', 'Wayfair (Khronos sample)', 'CC BY 4.0'),
 'DragonAttenuation': ('examples/models/gltf/DragonAttenuation.glb', 'glass dragon (transmission)', 'Stanford / Khronos sample', 'CC BY 4.0'),
 'IridescentDish':  ('examples/models/gltf/IridescentDishWithOlives.glb', 'iridescent dish', 'Wayfair (Khronos sample)', 'CC BY 4.0'),
 'PrimaryIonDrive': ('examples/models/gltf/PrimaryIonDrive.glb', 'sci-fi ion engine (emissive)', 'Animated Heaven (Khronos sample)', 'CC BY 4.0'),
 'LittlestTokyo':   ('examples/models/gltf/LittlestTokyo.glb', 'animated miniature city', 'Glen Fox (Sketchfab)', 'CC BY 4.0'),
 'Nefertiti':       ('examples/models/gltf/Nefertiti/Nefertiti.glb', 'Nefertiti bust scan', 'see repo README', 'VERIFY (README in folder)'),
 'Flower':          ('examples/models/gltf/Flower/Flower.glb', 'flower', 'see repo README', 'VERIFY (README in folder)'),
 'ShaderBall':      ('examples/models/gltf/ShaderBall.glb', 'material preview ball', 'three.js examples', 'VERIFY'),
 'coffeeMug':       ('examples/models/gltf/coffeeMug.glb', 'coffee mug', 'three.js examples', 'VERIFY'),
 'gears':           ('examples/models/gltf/gears.glb', 'interlocking gears', 'three.js examples', 'VERIFY'),
 'ferrari':         ('examples/models/gltf/ferrari.glb', 'sports car (parts split for materials)', 'three.js examples', 'VERIFY'),
 'Parrot':          ('examples/models/gltf/Parrot.glb', 'animated parrot (morph)', 'ro.me / Mirada', 'VERIFY'),
 'Flamingo':        ('examples/models/gltf/Flamingo.glb', 'animated flamingo (morph)', 'ro.me / Mirada', 'VERIFY'),
 'Stork':           ('examples/models/gltf/Stork.glb', 'animated stork (morph)', 'ro.me / Mirada', 'VERIFY'),
 'Horse':           ('examples/models/gltf/Horse.glb', 'animated horse (morph)', 'ro.me / Mirada', 'VERIFY'),
 'Soldier':         ('examples/models/gltf/Soldier.glb', 'animated soldier (skinned)', 'Mixamo', 'Mixamo terms (in-video use only)'),
 'Xbot':            ('examples/models/gltf/Xbot.glb', 'animated mannequin robot', 'Mixamo', 'Mixamo terms (in-video use only)'),
 'RobotExpressive': ('examples/models/gltf/RobotExpressive/RobotExpressive.glb', 'cartoon robot with emotes', 'Tomás Laulhé (Quaternius)', 'CC0'),
 'space_ship_hallway': ('examples/models/gltf/space_ship_hallway.glb', 'sci-fi corridor', 'three.js examples', 'VERIFY'),
 'earth':           ('examples/textures/land_ocean_ice_cloud_2048.jpg', 'Earth (Blue Marble) equirect texture', 'NASA', 'Public domain (NASA)'),
 'earth_specular':  ('examples/textures/planets/earth_specular_2048.jpg', 'Earth ocean specular mask', 'NASA', 'Public domain (NASA)'),
 'earth_normal':    ('examples/textures/planets/earth_normal_2048.jpg', 'Earth normal map', 'NASA / three.js', 'Public domain (NASA)'),
 'earth_lights':    ('examples/textures/planets/earth_lights_2048.png', 'Earth city lights at night', 'NASA', 'Public domain (NASA)'),
 'moon':            ('examples/textures/planets/moon_1024.jpg', 'Moon texture', 'NASA', 'Public domain (NASA)'),
 'waternormals':    ('examples/textures/waternormals.jpg', 'ocean water normal map', 'three.js examples', 'VERIFY'),
 'hardwood':        ('examples/textures/hardwood2_diffuse.jpg', 'wood floor diffuse', 'three.js examples', 'VERIFY'),
 'helvetiker_bold': ('examples/fonts/helvetiker_bold.typeface.json', '3D text font (TextGeometry)', 'Helvetiker (three.js)', 'see examples/fonts/LICENSE'),
}
THREEJS_HDR = ['royal_esplanade_1k', 'venice_sunset_1k', 'blouberg_sunrise_2_1k', 'moonless_golf_1k', 'pedestrian_overpass_1k',
               'quarry_01_1k', 'san_giuseppe_bridge_2k', 'spruit_sunrise_1k']  # Poly Haven HDRIs (CC0) mirrored in three.js
def threejs(names, out, lst):
    if lst:
        print('three.js examples library (r170) — pass names to download; licences shown:')
        for k, (p, w, a, l) in THREEJS.items(): print(f'  {k:20s} {w:42s} {l}')
        print('  hdr:<name> →', ', '.join(THREEJS_HDR), '(Poly Haven, CC0)')
        print('  More effects to learn from (read their source): https://threejs.org/examples/ — webgl_postprocessing_unreal_bloom,'
              ' webgl_materials_physical_transmission, webgl_geometry_extrude_splines, webgl_lines_fat, webgl_shaders_ocean,'
              ' webgl_postprocessing_dof2, webgl_loader_gltf, webgl_animation_keyframes, webgl_geometry_text, webgl_points_waves')
        return
    tree = None
    for n in names:
        if n.startswith('hdr:'):
            f = save(TJ + f'examples/textures/equirectangular/{n[4:]}.hdr', f'{out}/hdri/{n[4:]}.hdr')
            catalog(out, f, f'HDRI {n[4:]}', 'https://polyhaven.com (via three.js examples)', 'Poly Haven', 'CC0', 'lighting'); continue
        if n not in THREEJS: print('unknown:', n); continue
        p, w, a, l = THREEJS[n]
        if p.endswith('/'):            # multi-file glTF: fetch the whole folder
            tree = tree or json.loads(get('https://api.github.com/repos/mrdoob/three.js/git/trees/r170?recursive=1'))['tree']
            for x in tree:
                if x['type'] == 'blob' and x['path'].startswith(p): save(TJ + x['path'], f'{out}/models/{n}/' + x['path'][len(p):])
            f = f'{out}/models/{n}/'
        else:
            sub = 'models' if p.endswith(('.glb', '.gltf')) else 'fonts' if p.endswith('.json') else 'textures'
            f = save(TJ + p, f'{out}/{sub}/{os.path.basename(p)}')
        catalog(out, f, w, 'https://github.com/mrdoob/three.js/tree/r170/' + p, a, l, '3d')

# ---------------------------------------------------------------- Wikimedia Commons
API = 'https://commons.wikimedia.org/w/api.php?'
def strip(h): return re.sub(r'<[^>]+>', '', h or '').strip()
def commons(q, out, lst, n=20):
    if q.startswith('File:'): titles = [q]
    else:
        r = json.loads(get(API + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': q,
                                                          'srnamespace': 6, 'srlimit': n})))
        titles = [x['title'] for x in r['query']['search']]
    if not titles: print('nothing found'); return
    r = json.loads(get(API + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'imageinfo', 'titles': '|'.join(titles[:50]),
                                                      'iiprop': 'url|size|extmetadata'})))
    for pg in r['query']['pages'].values():
        ii = (pg.get('imageinfo') or [{}])[0]; m = ii.get('extmetadata', {})
        lic = strip(m.get('LicenseShortName', {}).get('value')) or 'VERIFY'; au = strip(m.get('Artist', {}).get('value'))[:80] or 'unknown'
        desc = strip(m.get('ImageDescription', {}).get('value'))[:70]
        if lst: print(f"  {pg['title'][:60]:60s} {ii.get('width')}×{ii.get('height')}  {lic:16s} {au[:30]}"); continue
        if re.search(r'\bNC\b|\bND\b|non-?commercial|no ?deriv', lic, re.I): print('  ✗ skipped (NC/ND):', pg['title'], lic); continue
        f = save(ii['url'], f'{out}/photos/{os.path.basename(urllib.parse.unquote(ii["url"].split("?")[0]))}')
        catalog(out, f, desc or pg['title'], ii.get('descriptionurl', ''), au, lic)

# ---------------------------------------------------------------- Poly Haven (CC0)
def polyhaven(arg, out, lst, q=None, res='2k'):
    if lst:
        d = json.loads(get(f'https://api.polyhaven.com/assets?t={arg}'))
        for k, v in sorted(d.items(), key=lambda kv: -kv[1].get('download_count', 0))[:400]:
            if q and q.lower() not in (k + ' ' + ' '.join(v.get('tags', [])) + ' ' + ' '.join(v.get('categories', []))).lower(): continue
            print(f"  {k:32s} {', '.join(v.get('categories', [])[:4])}")
        return
    files = json.loads(get(f'https://api.polyhaven.com/files/{arg}')); kind = json.loads(get(f'https://api.polyhaven.com/info/{arg}')).get('type')
    if kind == 0:
        f = save(files['hdri'][res]['hdr']['url'], f'{out}/hdri/{arg}_{res}.hdr'); catalog(out, f, f'HDRI {arg}', f'https://polyhaven.com/a/{arg}', 'Poly Haven', 'CC0', 'lighting')
    elif kind == 2:
        g = files['gltf'][res]['gltf']; base = f'{out}/models/{arg}/'
        save(g['url'], base + os.path.basename(g['url']))
        for rel, inc in g.get('include', {}).items(): save(inc['url'], base + rel)
        catalog(out, base, f'model {arg}', f'https://polyhaven.com/a/{arg}', 'Poly Haven', 'CC0', '3d')
    else:
        for mp in ('Diffuse', 'nor_gl', 'Rough', 'Displacement', 'AO', 'arm'):
            if mp in files and res in files[mp]:
                fmt = 'jpg' if 'jpg' in files[mp][res] else 'png'; save(files[mp][res][fmt]['url'], f'{out}/textures/{arg}/{arg}_{mp}_{res}.{fmt}')
        catalog(out, f'{out}/textures/{arg}/', f'PBR texture {arg}', f'https://polyhaven.com/a/{arg}', 'Poly Haven', 'CC0', 'material')

# ---------------------------------------------------------------- NASA image library (public domain; respect the credit line)
def nasa(q, out, lst, pick=None):
    d = json.loads(get('https://images-api.nasa.gov/search?' + urllib.parse.urlencode({'q': q, 'media_type': 'image'})))
    items = d['collection']['items'][:25]
    for i, it in enumerate(items):
        m = it['data'][0]
        if lst: print(f"  [{i}] {m.get('nasa_id', '')[:28]:28s} {m.get('title', '')[:60]}  · {m.get('center', '')}"); continue
        if pick is not None and i != pick: continue
        assets = json.loads(get(it['href'])); big = [u for u in assets if re.search(r'~(orig|large)\.(jpg|png|tif)$', u)]
        if not big: continue
        f = save(big[0].replace('http://', 'https://'), f"{out}/photos/{m['nasa_id']}{os.path.splitext(big[0])[1]}")
        catalog(out, f, m.get('title', '')[:70], f"https://images.nasa.gov/details/{m['nasa_id']}", m.get('photographer') or m.get('center', 'NASA'),
                'Public domain (NASA) — check credit', '');
        if pick is None: break

ap = argparse.ArgumentParser(); ap.add_argument('source', choices=['threejs', 'commons', 'polyhaven', 'nasa'])
ap.add_argument('args', nargs='*'); ap.add_argument('--list', action='store_true'); ap.add_argument('--out', default='assets')
ap.add_argument('--q'); ap.add_argument('--res', default='2k'); ap.add_argument('--pick', type=int)
a = ap.parse_args()
if a.source == 'threejs': threejs(a.args, a.out, a.list)
elif a.source == 'commons': [commons(q, a.out, a.list) for q in (a.args or [''])]
elif a.source == 'polyhaven': [polyhaven(x, a.out, a.list, a.q, a.res) for x in (a.args or ['hdris'])]
else: [nasa(q, a.out, a.list, a.pick) for q in a.args]
