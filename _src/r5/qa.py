import sys, asyncio
from playwright.async_api import async_playwright
d=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (320,375,414,768,900,1024,1280,1440):
            pg = await b.new_page(viewport={'width':w,'height':900})
            errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(f'file:///home/claude/r5/{d}/index.html'); await pg.wait_for_timeout(400)
            r = await pg.evaluate('''()=>{
              const sw=document.documentElement.scrollWidth, cw=document.documentElement.clientWidth;
              const st=[...document.querySelectorAll('.mt-sticker')].map(e=>{const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.width),Math.round(r.height), e.scrollHeight>e.clientHeight+1]});
              const nums=[...document.querySelectorAll('.mt-plans .mt-num')].map(e=>e.textContent).join(' ');
              const more=document.querySelectorAll('.mt-more').length;
              const bp=document.querySelector('.mt-btns-price').getBoundingClientRect();
              const col=getComputedStyle(document.querySelector('.mt-st-l4')).color+'/'+getComputedStyle(document.querySelector('.mt-st-l2')).color;
              return {sw,cw,st,nums,more,bp:[Math.round(bp.width),Math.round(bp.height)],col}}''')
            print(w, 'HSCROLL' if r['sw']>r['cw'] else 'ok', r, errs)
            for i,sel in enumerate(['.mt-plans-top','#price']):
                el = await pg.query_selector(sel)
                bb = await el.bounding_box()
                await pg.screenshot(path=f'{d}_{w}_{i}.png', clip={'x':0,'y':max(0,bb['y']-20),'width':w,'height':min(bb['height']+(520 if i==0 else 120),1600)}, full_page=True)
            await pg.close()
        await b.close()
asyncio.run(main())
