# Quick objection section: tabs, inline key setup, Claude request contents, 3 more ideas,
# recent list, playbook fallback. The Anthropic API is mocked.
import os, json, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='file://'+os.path.join(ROOT,'index.html')
def fake(tag):
    return {"content":[{"type":"text","text":json.dumps({"read":"They see the 3-year term as a reason not to look, not as a price problem.",
      "pointers":[{"title":f"Respect the term {tag}","say":"A three-year deal makes sense. Let's make sure you're ready before it ends so you're not rushed.","ask":"When exactly does the term end?"},
                  {"title":f"Find the real lock {tag}","say":"Is it the contract itself, or is there a penalty for leaving early?","ask":"Did they mention any cancellation fees?"},
                  {"title":f"Calendar the review {tag}","say":"I'll set a reminder 90 days out and send a side-by-side then.","ask":"Email or a call better?"}],
      "caution":"Don't advise cancelling mid-term without checking short-rate penalties."})}]}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1300,'height':950}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto(URL)
        # Live call is the default view; "/" jumps to the Quick objection section
        assert await pg.is_visible('#viewLive') and not await pg.is_visible('#viewQuick')
        await pg.keyboard.press('/'); await pg.wait_for_timeout(150)
        assert await pg.is_visible('#viewQuick') and not await pg.is_visible('#viewLive')
        assert await pg.evaluate("document.activeElement.id")=='qText'
        print('TABS OK')
        # No key: key setup shows, playbook fallback for a known objection
        await pg.keyboard.type("it's too expensive"); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        assert await pg.is_visible('#qKey'); src=await pg.text_content('#qSrc')
        print('NO KEY:',src,'|',await pg.locator('#qGrid h3').all_text_contents())
        # Save key inline -> Claude (mocked) answers with context in the request
        sent=[]
        async def handler(route):
            body=json.loads(route.request.post_data); sent.append(body)
            await route.fulfill(status=200,content_type='application/json',body=json.dumps(fake(len(sent))))
        await pg.route('https://api.anthropic.com/**',handler)
        await pg.fill('#qText',"we're locked into a 3-year deal with our carrier")
        await pg.click('#qCtx summary'); await pg.fill('#qBiz','used car dealer'); await pg.select_option('#qCov','Surety / dealer bond')
        await pg.fill('#qDet','renews in March')
        await pg.fill('#qKeyIn','test-key'); await pg.click('#qKeySave'); await pg.wait_for_timeout(500)
        titles=await pg.locator('#qGrid h3').all_text_contents(); read=await pg.text_content('#qRead')
        assert len(titles)==3 and titles[0].endswith('1'), titles
        msg=sent[0]['messages'][0]['content']; sys_=sent[0]['system']
        assert 'exactly as typed: "we\'re locked into a 3-year deal with our carrier"' in msg
        assert 'Type of business: used car dealer' in msg and 'Surety / dealer bond' in msg and 'renews in March' in msg
        assert 'All three pointers must address this objection' in sys_ and sent[0]['temperature']==0.4
        print('CLAUDE OK:',titles,'|',read[:60])
        # 3 more ideas: different temperature and previous pointers sent
        await pg.click('#qMore'); await pg.wait_for_timeout(500)
        msg2=sent[1]['messages'][0]['content']
        assert 'give three clearly different pointers' in msg2 and sent[1]['temperature']==0.8
        assert (await pg.locator('#qGrid h3').all_text_contents())[0].endswith('2')
        print('MORE OK')
        # Recent list persists across reload; clicking shows the saved answer without a new request
        n=len(sent); await pg.reload(); await pg.wait_for_timeout(300)
        assert await pg.is_visible('#viewQuick')  # still on #quick
        await pg.click('#qRecent button'); await pg.wait_for_timeout(150)
        assert len(sent)==n and len(await pg.locator('#qGrid h3').all_text_contents())==3
        print('RECENT OK:', await pg.text_content('#qSrc'))
        # Context remembered
        assert await pg.input_value('#qBiz')=='used car dealer'
        await pg.screenshot(path='/tmp/quick.png')
        # Back to live view via tab
        await pg.click('#tabLive'); await pg.wait_for_timeout(150)
        assert await pg.is_visible('#viewLive')
        print('ERRORS:',errs); assert not errs
        await b.close()
asyncio.run(main())
