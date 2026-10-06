"""sheet.py DIR — tile DIR/t*.png into DIR/sheet.png with timestamps (for reviewing test stills yourself)."""
import glob, sys
from PIL import Image, ImageDraw
d = sys.argv[1]; fs = sorted(glob.glob(f'{d}/t*.png'))
if not fs: sys.exit('no t*.png in ' + d)
im0 = Image.open(fs[0]); r = im0.height / im0.width
W = 640; H = int(W * r); cols = 3 if r < 1.2 else 4
rows = (len(fs) + cols - 1) // cols
c = Image.new('RGB', (W * cols, H * rows), 'white'); dr = ImageDraw.Draw(c)
for i, f in enumerate(fs):
    x, y = (i % cols) * W, (i // cols) * H
    c.paste(Image.open(f).convert('RGB').resize((W, H)), (x, y))
    dr.rectangle([x, y, x + 84, y + 20], fill='black'); dr.text((x + 4, y + 4), f.split('/t')[-1][:-4] + 's', fill='yellow')
c.save(f'{d}/sheet.png'); print('sheet ->', f'{d}/sheet.png')
