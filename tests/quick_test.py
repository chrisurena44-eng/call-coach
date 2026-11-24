# Quick objection: playbook fallback without a key, and Claude pointers with a mocked API response.
import os, json, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='file://'+os.path.join(ROOT,'index.html')
FAKE={"content":[{"type":"text","text":json.dumps({"pointers":[
  {"title":"Acknowledge the term","say":"Makes sense, a three-year deal is a real commitment. Let's make sure you're set up well for when it ends.","ask":"When does the term end?"},
  {"title":"Find the real concern","say":"Is the contract the only thing holding you back, or is it price too?","ask":"What would you change if you could?"},
  {"title":"Set a next step","say":"Let me put a reminder 90 days before it ends and send you a comparison then.","ask":"Is email or a call better?"}],
  "caution":"Don't advise breaking an existing contract."})}]}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1300,'height':950}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # 1) no key: playbook fallback, keyboard shortcut
        await pg.keyboard.press('/'); await pg.keyboard.type("it's too expensive"); await pg.keyboard.press('Enter')
        await pg.wait_for_timeout(200)
        n=await pg.locator('#qGrid .qp').count(); src=await pg.text_content('#qSrc'); first=await pg.text_content('#qGrid .qp h3')
        print('NO KEY:',n,'pointers |',src,'|',first); assert n>=1 and 'playbook' in src
        await pg.fill('#qText','zebra quantum'); await pg.click('#quick button'); await pg.wait_for_timeout(150)
        print('NO MATCH:', (await pg.text_content('#qGrid'))[:60])
        # 2) with key: mocked Claude
        await pg.evaluate("localStorage.setItem('callcoach.cfg',JSON.stringify({antKey:'test-key',remember:true}))")
        await pg.route('https://api.anthropic.com/**', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(FAKE)))
        await pg.reload(); await pg.fill('#qText',"we're locked into a three year deal"); await pg.click('#quick button')
        await pg.wait_for_timeout(600)
        titles=await pg.locator('#qGrid .qp h3').all_text_contents(); src=await pg.text_content('#qSrc'); cau=await pg.text_content('#qCau')
        print('CLAUDE:',titles,'|',src,'|',cau); assert len(titles)==3 and src=='From Claude'
        hist=await pg.text_content('#history'); assert 'Typed:' in hist
        await pg.screenshot(path='/tmp/quick.png')
        print('ERRORS:',errs); assert not errs
        await b.close()
asyncio.run(main())
