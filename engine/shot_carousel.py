"""python3 shot_carousel.py data/<slug>.json -> out/<slug>/slide_N.jpg (1080x1350)"""
import asyncio,base64,json,sys,os
from playwright.async_api import async_playwright
H=os.path.dirname(os.path.abspath(__file__)); d=json.load(open(sys.argv[1])); o=f"{H}/out/{d['slug']}"; os.makedirs(o,exist_ok=True)
h=open(H+'/carousel.html').read().replace('__DATA__',json.dumps(d)).replace('__FONT__','data:font/ttf;base64,'+base64.b64encode(open(H+'/fonts/BigShoulders-Bold.ttf','rb').read()).decode()).replace('__LOGO__','data:image/png;base64,'+base64.b64encode(open(H+'/logo.png','rb').read()).decode())
open(f'/tmp/car_{d["slug"]}.html','w').write(h)
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for i in range(len(d['slides'])):
            pg=await b.new_page(viewport={"width":1080,"height":1350}); pg.on("pageerror",lambda e:print("JS",e))
            await pg.goto(f'file:///tmp/car_{d["slug"]}.html#{i}'); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=f'{o}/slide_{i+1}.jpg',type='jpeg',quality=93); await pg.close()
        await b.close()
asyncio.run(m()); print("ok",o)
