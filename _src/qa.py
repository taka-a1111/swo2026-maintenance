import asyncio, re, html, sys
from playwright.async_api import async_playwright
url=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); errs=[]
        for w in [320,375,414,768,900,1024,1280,1440]:
            pg=await b.new_page(viewport={'width':w,'height':900})
            pg.on('pageerror',lambda e: errs.append(str(e)))
            await pg.goto(url, wait_until='load')
            ov=await pg.evaluate("document.documentElement.scrollWidth-document.documentElement.clientWidth")
            nav=await pg.evaluate("getComputedStyle(document.getElementById('navToggle')).display")
            print(w,'overflow',ov,'toggle',nav)
            await pg.close()
        print('pageerrors',errs)
        await b.close()
asyncio.run(main())
