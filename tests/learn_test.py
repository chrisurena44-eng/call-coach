import sys, asyncio, json
from playwright.async_api import async_playwright
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path=os.path.join(ROOT,'index.html'); S=os.path.join(ROOT,'tests','samples')+'/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':1300,'height':950}, accept_downloads=True)
        pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto('file://'+path)
        await pg.click('#learnBtn')
        await pg.fill('#myName','Chris Urena'); await pg.dispatch_event('#myName','change')
        await pg.set_input_files('#lFiles',[S+'call1_headers.txt',S+'call2_colon.txt',S+'call3.srt',S+'call4.docx'])
        await pg.wait_for_timeout(600)
        info=await pg.evaluate("""()=>[...document.querySelectorAll('.lcall')].map(a=>({
            name:a.querySelector('h3').textContent,
            me:a.querySelector('select[data-k=me]').value,
            speakers:[...a.querySelector('select[data-k=me]').options].map(o=>o.value),
            stats:a.querySelector('p.small').textContent,
            objections:[...a.querySelectorAll('ul li b')].map(x=>x.textContent),
            missed:[...a.querySelectorAll('.teach input:first-child')].map(i=>i.value)}))""")
        for c in info: print(json.dumps(c))
        print('MSG:', await pg.text_content('#lMsg'))
        # teach a new objection from call1 missed line
        await pg.evaluate("""()=>{const row=[...document.querySelectorAll('.teach')].find(r=>r.querySelector('input').value.includes('locked into'));
            row.querySelector('input').value='locked into a three year';
            row.querySelector('.newtitle').value='Locked into a multi-year policy';}""")
        await pg.evaluate("""()=>[...document.querySelectorAll('.teach')].find(r=>r.querySelector('input').value.includes('locked into')).querySelector('button').click()""")
        await pg.wait_for_timeout(200)
        print('AFTER TEACH MSG:', await pg.text_content('#lMsg'))
        # set outcome of first call to won, save all
        await pg.select_option('.lcall[data-c="0"] select[data-k=outcome]','won')
        for _ in range(4):
            await pg.click('.lcall[data-c="0"] button[data-act=save]'); await pg.wait_for_timeout(150)
        print('LIB:', await pg.text_content('#lLib'))
        await pg.screenshot(path='/tmp/learn_dialog.png')
        # export
        async with pg.expect_download() as d: await pg.click('#lExport')
        dl=await d.value; print('EXPORT:', dl.suggested_filename)
        await pg.click('#learnClose')
        # live: taught phrase + example reply on price card
        await pg.fill('#pText','Honestly we are locked into a three year contract with them'); await pg.click('#practice button'); await pg.wait_for_timeout(200)
        print('CUE1:', await pg.text_content('#cueTitle'))
        await pg.fill('#pText','The premium went up again, it is too expensive'); await pg.click('#practice button'); await pg.wait_for_timeout(200)
        print('CUE2:', await pg.text_content('#cueTitle'), '|', await pg.text_content('#youLabel'), '|', await pg.text_content('#cueYou'))
        await pg.screenshot(path='/tmp/learned_cue.png')
        # persistence after reload
        await pg.reload(); await pg.wait_for_timeout(300)
        await pg.fill('#pText','we are locked into a three year deal'); await pg.click('#practice button'); await pg.wait_for_timeout(200)
        print('AFTER RELOAD CUE:', await pg.text_content('#cueTitle'))
        print('ERRORS:', [e for e in errs])
        await b.close()
asyncio.run(main())
