"""Снимает сцены video.html в mp4.  python3 film.py check | python3 film.py render [s1 s2 ...]"""
import asyncio, subprocess, sys, os
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
import base64, json
DATA = json.load(open(sys.argv[2]))
_h = open(HERE + "/" + DATA.get("template", "video.html")).read().replace("/*ENGINE_CSS*/", open(HERE + "/engine.css").read()).replace("/*ENGINE_JS*/", open(HERE + "/engine.js").read()).replace("__DATA__", json.dumps(DATA)).replace("__LOGO__", "data:image/png;base64," + base64.b64encode(open(HERE + "/logo.png", "rb").read()).decode())
open(HERE + "/build_" + DATA["slug"] + ".html", "w").write(_h)
OUT = HERE + "/out/" + DATA["slug"]
URL = "file://" + HERE + "/build_" + DATA["slug"] + ".html"
FPS = 30
SCENES = DATA.get("scenes") or {"s1": 3.5, "s2": 5.0, "s3": 4.5, "s4": 4.5, "s5": 3.5}
CHECK = {"s1a": 0.0, "s1": 2.8, "s2": 3.3, "s3": 3.2, "s4": 3.2, "s5": 2.6, "s1b": 0.62, "s2b": 0.2, "s3b": 0.7, "s4b": 4.3}
CHECK = DATA.get("checks") or CHECK


async def open_scene(browser, sid):
    page = await browser.new_page(viewport={"width": 1080, "height": 1920})
    page.on("pageerror", lambda e: print("JS ERROR", sid, e, flush=True))
    await page.goto(URL + "#" + sid)
    await page.evaluate("document.fonts.ready")
    return page


async def check(browser):
    for sid, t in CHECK.items():
        page = await open_scene(browser, sid[:2])
        await page.evaluate(f"seek({t*1000})")
        await page.screenshot(path=f"{OUT}/check_{sid}.jpg", type="jpeg", quality=85)
        await page.close()


async def render(browser, sid):
    page = await open_scene(browser, sid)
    tmp, final = f"{OUT}/{sid}.tmp.mp4", f"{OUT}/{sid}.mp4"
    ff = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-c:v", "mjpeg", "-framerate", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
        stdin=subprocess.PIPE)
    for f in range(round(SCENES[sid] * FPS)):
        await page.evaluate(f"seek({f*1000/FPS})")
        ff.stdin.write(await page.screenshot(type="jpeg", quality=92))
    ff.stdin.close()
    if ff.wait() == 0:
        os.rename(tmp, final)
        print("ok", sid, flush=True)
    await page.close()


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        if sys.argv[1] == "check":
            await check(browser)
        else:
            for sid in (sys.argv[3:] or SCENES):
                await render(browser, sid)
        await browser.close()

asyncio.run(main())
