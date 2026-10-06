"""prep_image.py — get real photos ready for a 9:16 (or any) frame.

  python3 prep_image.py card  photo.jpg --out img/card.jpg [--crop x,y,w,h] [--grade "#050817"]   # photo + blurred bg version
  python3 prep_image.py cutout object.jpg --out img/object.png          # remove background (rembg) → transparent PNG
  python3 prep_image.py grade  photo.jpg --out img/photo.jpg --tint "#5cadf5" --amount .25   # pull colours toward the palette
  python3 prep_image.py grain  --out img/grain.png                      # tileable film grain overlay (mix-blend: overlay)

card: writes <out> (the photo, cropped, max 2160 px) and <out>_bg.jpg (same photo, heavily blurred and darkened) — put
the photo in a rounded card with ITS OWN aspect ratio over the blurred copy as a full-bleed background (craft.md §8):
never a thin strip with dark padding, never a letterbox. Crop out museum labels / watermarks with --crop.
cutout needs `pip3 install rembg` (downloads a ~170 MB model on first use).
"""
import argparse, os
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
ap = argparse.ArgumentParser(); ap.add_argument('mode', choices=['card', 'cutout', 'grade', 'grain']); ap.add_argument('src', nargs='?')
ap.add_argument('--out', required=True); ap.add_argument('--crop'); ap.add_argument('--tint', default='#5cadf5'); ap.add_argument('--amount', type=float, default=.2)
ap.add_argument('--max', type=int, default=2160)
a = ap.parse_args(); os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
def load(p):
    im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')
    if a.crop: x, y, w, h = map(int, a.crop.split(',')); im = im.crop((x, y, x + w, y + h))
    im.thumbnail((a.max, a.max), Image.LANCZOS); return im
def tint(im, hexc, k):
    c = tuple(int(hexc[i:i + 2], 16) for i in (1, 3, 5)); g = ImageOps.grayscale(im); col = ImageOps.colorize(g, (5, 8, 23), c)
    return Image.blend(im, col, k)
if a.mode == 'card':
    im = load(a.src); im.save(a.out, quality=92)
    bg = im.copy(); bg.thumbnail((540, 540)); bg = bg.filter(ImageFilter.GaussianBlur(28)); bg = ImageEnhance.Brightness(bg).enhance(.45)
    bg = tint(bg, a.tint, .25); bg.save(os.path.splitext(a.out)[0] + '_bg.jpg', quality=88); print('card', im.size, '+ bg')
elif a.mode == 'cutout':
    from rembg import remove
    out = remove(Image.open(a.src)); bb = out.getbbox(); out = out.crop(bb) if bb else out; out.save(a.out); print('cutout', out.size)
elif a.mode == 'grade':
    tint(load(a.src), a.tint, a.amount).save(a.out, quality=92); print('graded')
else:
    import random; random.seed(7); im = Image.new('L', (512, 512))
    im.putdata([max(0, min(255, int(random.gauss(128, 38)))) for _ in range(512 * 512)]); im.save(a.out); print('grain 512²')
