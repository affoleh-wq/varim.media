"""python3 poster.py data/<slug>.json -> out/<slug>/<slug>_pinterest.png, _instagram.png"""
import asyncio, sys, os, json, base64
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
PLATFORMS = {"pinterest": (1000, 1500), "instagram": (1080, 1350)}
FOOT = {
    "pinterest": "Full prediction &amp; match stats at varim.net<br>An estimate, not a guarantee. 18+",
    "instagram": "<b>Comment your score below</b><br>An estimate, not a guarantee. 18+",
}


async def main():
    data = json.load(open(sys.argv[1]))
    out = f"{HERE}/out/{data['slug']}"
    os.makedirs(out, exist_ok=True)
    tpl = open(HERE + "/poster.html").read().replace("/*ENGINE_CSS*/", open(HERE + "/engine.css").read()).replace("/*ENGINE_JS*/", open(HERE + "/engine.js").read())
    logo = "data:image/png;base64," + base64.b64encode(open(HERE + "/logo.png", "rb").read()).decode()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for name, (w, h) in PLATFORMS.items():
            d = dict(data, platform={"name": name, "w": w, "h": h}, footNote=FOOT[name])
            html = tpl.replace("__DATA__", json.dumps(d)).replace("__LOGO__", logo)
            path = f"{out}/poster_{name}.html"
            open(path, "w").write(html)
            page = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            page.on("pageerror", lambda e: print("JS ERROR", e))
            await page.goto("file://" + path)
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(200)
            await page.screenshot(path=f"{out}/varim_{data['slug']}_{name}.png")
            await page.close()
        await b.close()
    print("ok", data["slug"])

asyncio.run(main())
