import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (320,375,414,768,900,1024,1280,1440):
            pg = await b.new_page(viewport={'width':w,'height':900})
            errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto('file:///home/claude/swo_r3/out/index.html'); await pg.wait_for_timeout(400)
            r = await pg.evaluate('''()=>{
              const sw=document.documentElement.scrollWidth, cw=document.documentElement.clientWidth;
              const lines=[...document.querySelectorAll('.mt-h1-big .mt-line')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.width),Math.round(r.height),Math.round(parseFloat(getComputedStyle(e).fontSize)), e.scrollWidth>e.clientWidth]});
              const h1=document.querySelector('.mt-h1-big').getBoundingClientRect();
              const sl=document.querySelector('.mt-wide').getBoundingClientRect();
              const pl=[...document.querySelectorAll('.mt-plans-top .mt-plan')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height), e.scrollWidth>e.clientWidth+1]});
              const over=[...document.querySelectorAll('.mt-plans-top *')].filter(e=>e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!='inline').length;
              const m=document.querySelector('.mt-mail-a img').getBoundingClientRect();
              return {sw,cw,lines,h1w:Math.round(h1.width),slide:[Math.round(sl.left),Math.round(sl.width),Math.round(sl.height),Math.round(sl.top)],pl,over,mail:[Math.round(m.width),Math.round(m.height)]}}''')
            print(w, 'hscroll' if r['sw']>r['cw'] else 'ok', r, errs)
            if w in (320,375,768,1024,1280):
                await pg.screenshot(path=f'qa_{w}.png', clip={'x':0,'y':0,'width':w,'height':min(1500, 1500)}, full_page=True)
            await pg.close()
        await b.close()
asyncio.run(main())
