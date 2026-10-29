import asyncio, sys
from playwright.async_api import async_playwright
url, outdir = sys.argv[1], sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1280,'height':900})
        await pg.goto(url, wait_until='networkidle')
        await pg.emulate_media(media='screen')
        names=await pg.evaluate("[...document.querySelectorAll('[data-page]')].map(e=>e.dataset.page)")
        for i,n in enumerate(names):
            await pg.evaluate("""(i)=>{
              const ps=[...document.querySelectorAll('[data-page]')];
              ps.forEach((e,k)=>e.style.display=(k===i)?'':'none');
              document.querySelector('header').style.display=(i===0)?'':'none';
              document.querySelector('header').style.position='static';
              document.querySelector('footer').style.display=(i===ps.length-1)?'':'none';
              const sc=document.querySelector('.sticky-cta'); if(sc){sc.style.position='static';sc.style.display=(i===ps.length-1)?'':'none';}
              document.body.style.paddingBottom='0';
              window.scrollTo(0,0);
            }""", i)
            await pg.wait_for_timeout(300)
            h=await pg.evaluate("Math.ceil(document.body.getBoundingClientRect().height)")
            await pg.pdf(path=f"{outdir}/{n}.pdf", width='1280px', height=f'{h+2}px', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
            print(n,h)
        await b.close()
asyncio.run(main())
