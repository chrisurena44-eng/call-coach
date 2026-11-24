import sys, asyncio
from playwright.async_api import async_playwright
import os
path = os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','index.html'))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        errs = []
        for w, h, scheme, tag in [(1400, 900, 'light', 'wide'), (420, 900, 'dark', 'narrow')]:
            pg = await b.new_page(viewport={'width': w, 'height': h}, color_scheme=scheme)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' and 'fonts' not in m.text else None)
            await pg.goto('file://' + path)
            await pg.screenshot(path=f'/tmp/idle_{tag}.png', full_page=False)
            # speed the demo: patch setTimeout delays
            await pg.evaluate("""() => { const st = window.setTimeout; window.setTimeout = (f, d, ...a) => st(f, Math.min(d || 0, 60), ...a); }""")
            await pg.click('#demoBtn')
            await pg.wait_for_timeout(3500)
            # practice line from agent to trigger caution check
            await pg.fill('#pText', 'Our last audit was brutal and the deductible is too high')
            await pg.click('#practice button')
            await pg.wait_for_timeout(300)
            info = await pg.evaluate("""() => ({
              title: document.querySelector('#cueTitle').textContent,
              kind: document.querySelector('#cue').dataset.kind,
              history: [...document.querySelectorAll('#history button')].map(b => b.textContent),
              checks: [...document.querySelectorAll('#checklist li.done')].map(li => li.textContent),
              lines: document.querySelectorAll('#tx .u:not(.interim)').length,
              marks: [...document.querySelectorAll('#tx mark')].map(m => m.textContent),
              meters: document.querySelector('#meters').innerText.replace(/\\n/g,' | '),
              ratio: document.querySelector('#ratioMe').textContent,
              overflow: document.documentElement.scrollWidth > window.innerWidth
            })""")
            print(tag, info)
            await pg.click('#history button')  # re-show top pointer
            await pg.evaluate("window.scrollTo(0,0)")
            await pg.screenshot(path=f'/tmp/demo_{tag}.png', full_page=(tag=='narrow'))
            await pg.click('#endBtn'); await pg.wait_for_timeout(200)
            summ = await pg.input_value('#sumText')
            print('SUMMARY HEAD:\n' + '\n'.join(summ.split('\n')[:12]))
            await pg.screenshot(path=f'/tmp/summary_{tag}.png')
            await pg.click('#sumClose')
            await pg.click('#settingsBtn'); await pg.wait_for_timeout(200)
            await pg.screenshot(path=f'/tmp/settings_{tag}.png')
            await pg.close()
        print('ERRORS:', errs)
        await b.close()
asyncio.run(main())
