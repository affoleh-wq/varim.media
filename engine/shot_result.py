"""python3 shot_result.py data/<slug>.json -> out/<slug>/result_feed.jpg (1080x1350), result_story.jpg (1080x1920)"""
import asyncio,base64,json,sys,os
from playwright.async_api import async_playwright
H=os.path.dirname(os.path.abspath(__file__)); d=json.load(open(sys.argv[1])); o=f"{H}/out/{d['slug']}"; os.makedirs(o,exist_ok=True)
h=open(H+'/poster_result.html').read().replace('__DATA__',json.dumps(d)).replace('__FONT__','data:font/ttf;base64,'+base64.b64encode(open(H+'/fonts/BigShoulders-Bold.ttf','rb').read()).decode()).replace('__LOGO__','data:image/png;base64,'+base64.b64encode(open(H+'/logo.png','rb').read()).decode())
open(f'/tmp/r_{d["slug"]}.html','w').write(h)
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for n,(w,hh) in {'feed':(1080,1350),'story':(1080,1920)}.items():
            pg=await b.new_page(viewport={"width":w,"height":hh}); pg.on("pageerror",lambda e:print("JS",e))
            await pg.goto(f'file:///tmp/r_{d["slug"]}.html'); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'{o}/result_{n}.jpg',type='jpeg',quality=93); await pg.close()
        await b.close()
asyncio.run(m()); print("ok",o)
