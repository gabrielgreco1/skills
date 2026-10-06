"""export_marks.py timeline.html [--ar 16x9] > marks.json — dump window.MARK (+DUR) so audio/VO lock to visual events."""
import asyncio, json, os, sys
from playwright.async_api import async_playwright
html = sys.argv[1]; ar = sys.argv[sys.argv.index('--ar') + 1] if '--ar' in sys.argv else '16x9'
async def m():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto('file://' + os.path.abspath(html) + f'?ar={ar}'); await pg.wait_for_function('window.ready===true')
        print(json.dumps(await pg.evaluate('({...(window.MARK||{}), DUR: window.DUR})'), indent=1)); await b.close()
asyncio.run(m())
