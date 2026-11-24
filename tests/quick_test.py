# Quick objection section: tabs, AI setup (Manus passcode or Anthropic key), request contents,
# 3 more ideas, recent list, wrong-passcode handling, playbook fallback. All AI calls are mocked.
import os, json, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='file://'+os.path.join(ROOT,'index.html')
SVC='https://callcoachai-jwnbgrgv.manus.space'  # built-in address; every request to it is mocked here
def answer(tag):
    return json.dumps({"read":"They see the 3-year term as a reason not to look, not as a price problem.",
      "pointers":[{"title":f"Respect the term {tag}","say":"A three-year deal makes sense. Let's make sure you're ready before it ends.","ask":"When does the term end?"},
                  {"title":f"Find the real lock {tag}","say":"Is it the contract itself, or a penalty for leaving early?","ask":"Any cancellation fees?"},
                  {"title":f"Calendar the review {tag}","say":"I'll set a reminder 90 days out and send a side-by-side then.","ask":"Email or a call?"}],
      "caution":"Don't advise cancelling mid-term without checking short-rate penalties."})
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1300,'height':950}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto(URL)
        assert await pg.is_visible('#viewLive') and not await pg.is_visible('#viewQuick')
        await pg.keyboard.press('/'); await pg.wait_for_timeout(150)
        assert await pg.is_visible('#viewQuick') and await pg.evaluate("document.activeElement.id")=='qText'
        print('TABS OK')
        # No AI connected: setup box + playbook fallback
        await pg.keyboard.type("it's too expensive"); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        assert await pg.is_visible('#qKey') and await pg.is_visible('#qPassIn')
        print('NO AI:',await pg.text_content('#qSrc'),'|',await pg.locator('#qGrid h3').all_text_contents())
        # Manus service (mocked)
        sent=[]; mode={'status':200}
        async def manus(route):
            sent.append({'url':route.request.url,'headers':route.request.headers,'body':json.loads(route.request.post_data)})
            if mode['status']!=200: return await route.fulfill(status=mode['status'],content_type='application/json',body=json.dumps({"error":"bad passcode"}))
            await route.fulfill(status=200,content_type='application/json',body=json.dumps({"text":answer(len(sent))}))
        await pg.route(SVC+'/api/complete',manus)
        await pg.fill('#qText',"we're locked into a 3-year deal with our carrier")
        await pg.click('#qCtx summary'); await pg.fill('#qBiz','used car dealer'); await pg.select_option('#qCov','Surety / dealer bond'); await pg.fill('#qDet','renews in March')
        assert not await pg.is_visible('#qUrlIn')  # address is built in
        await pg.fill('#qPassIn','test-passcode'); await pg.click('#qKeySave'); await pg.wait_for_timeout(500)
        req=sent[0]; body=req['body']
        assert req['url']==SVC+'/api/complete' and 'x-api-key' not in req['headers']
        assert body['passcode']=='test-passcode' and body['temperature']==0.4 and body['model']=='haiku' and body['max_tokens']==700
        assert 'exactly as typed: "we\'re locked into a 3-year deal with our carrier"' in body['user']
        assert 'used car dealer' in body['user'] and 'Surety / dealer bond' in body['user'] and 'renews in March' in body['user']
        assert 'All three pointers must address this objection' in body['system']
        titles=await pg.locator('#qGrid h3').all_text_contents(); assert len(titles)==3 and titles[0].endswith('1'), titles
        print('MANUS OK:',titles,'|',await pg.text_content('#qSrc'))
        await pg.click('#qMore'); await pg.wait_for_timeout(500)
        assert sent[1]['body']['temperature']==0.8 and 'give three clearly different pointers' in sent[1]['body']['user']
        print('MORE OK')
        n=len(sent); await pg.reload(); await pg.wait_for_timeout(300)
        await pg.click('#qRecent button'); await pg.wait_for_timeout(150)
        assert len(sent)==n and len(await pg.locator('#qGrid h3').all_text_contents())==3 and await pg.input_value('#qBiz')=='used car dealer'
        print('RECENT OK')
        # Wrong passcode -> clear message, setup box shown again
        mode['status']=401; await pg.fill('#qText','we already have an agent'); await pg.click('#qGo'); await pg.wait_for_timeout(400)
        src=await pg.text_content('#qSrc'); assert 'rejected the passcode' in src and await pg.is_visible('#qKey'), src
        print('BAD PASSCODE OK:',src)
        # Anthropic key fallback when no Manus passcode is saved
        await pg.evaluate("localStorage.setItem('callcoach.cfg',JSON.stringify({antKey:'test-key',mPass:'',remember:true}))")
        async def anth(route):
            sent.append({'url':route.request.url,'headers':route.request.headers})
            await route.fulfill(status=200,content_type='application/json',body=json.dumps({"content":[{"type":"text","text":answer('A')}]}))
        await pg.route('https://api.anthropic.com/**',anth)
        await pg.reload(); await pg.fill('#qText','just email me something'); await pg.click('#qGo'); await pg.wait_for_timeout(500)
        assert sent[-1]['url'].startswith('https://api.anthropic.com') and sent[-1]['headers'].get('x-api-key')=='test-key'
        print('ANTHROPIC FALLBACK OK:',(await pg.locator('#qGrid h3').all_text_contents())[0])
        await pg.click('#tabLive'); await pg.wait_for_timeout(150); assert await pg.is_visible('#viewLive')
        print('ERRORS:',errs); assert not errs
        # Phone: no screen sharing -> opens on Quick objection, live buttons hidden there, clear message on Start listening
        ph=await b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
        await ph.add_init_script("Object.defineProperty(MediaDevices.prototype,'getDisplayMedia',{value:undefined,configurable:true})")
        pp=await ph.new_page(); await pp.goto(URL); await pp.wait_for_timeout(200)
        assert await pp.is_visible('#viewQuick') and not await pp.is_visible('#startBtn') and await pp.is_visible('#settingsBtn')
        await pp.click('#tabLive'); await pp.wait_for_timeout(150); assert await pp.is_visible('#startBtn')
        await pp.click('#startBtn'); await pp.wait_for_timeout(200)
        msg=await pp.text_content('#noticeText'); assert 'Chrome on a computer' in msg, msg
        print('PHONE OK:',msg)
        await b.close()
asyncio.run(main())
