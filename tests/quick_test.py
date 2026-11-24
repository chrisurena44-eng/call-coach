# Quick objection: all 3 pointers must be about the typed objection.
# Covers the playbook-only path (no key) and the Claude path (API mocked, request checked).
import os, json, asyncio
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='file://'+os.path.join(ROOT,'index.html')
FAKE={"content":[{"type":"text","text":json.dumps({"pointers":[
  {"title":"Acknowledge the price","say":"I hear you, nobody wants to overpay. Let's see what's driving the number.","ask":"What did you expect it to be?"},
  {"title":"Find what's behind it","say":"Is it the total, or the down payment that's the problem?","ask":"What monthly amount works?"},
  {"title":"Next step on price","say":"I'll shop it with two more carriers using your real payroll and call you Thursday.","ask":"Does Thursday morning work?"}],
  "caution":"Don't promise a lower premium before underwriting."})}]}
async def quick(pg,text):
    await pg.fill('#qText',text); await pg.click('#quick button'); await pg.wait_for_timeout(250)
    return {'match':await pg.text_content('#qMatch'),'src':await pg.text_content('#qSrc'),
            'titles':await pg.locator('#qGrid .qp h3').all_text_contents(),
            'says':await pg.locator('#qGrid .qp p:not(.qask)').all_text_contents(),
            'grid':(await pg.text_content('#qGrid'))[:90],'caution':await pg.text_content('#qCau')}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':1300,'height':950}); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.goto(URL)
        data=await pg.evaluate("Object.fromEntries([...PLAYBOOK,...SIGNALS].map(c=>[c.id,{title:c.title,say:c.say,ask:c.ask,next:c.next}]))")
        # 1) no key: every pointer comes from the one matched card
        cases={"it's too expensive":'price',"just email me something":'send',"I need to talk to my partner first":'decider',
               "my buddy pays less than me":'friendprice',"we don't need garagekeepers":'garage',"how far out can I date it if I lock it in":'startdate'}
        await pg.keyboard.press('/')
        for text,cid in cases.items():
            r=await quick(pg,text); c=data[cid]
            assert c['title'].replace('Buying signal: ','') in r['match'], (text,r['match'])
            assert r['says']==[c['say'],c['ask'],c['next']], (text,r['says'])
            print('OK  ',text,'->',r['match'],'|',r['titles'])
        r=await quick(pg,'zebra quantum'); print('NO MATCH:',r['match'],'|',r['grid']); assert 'No playbook card' in r['match']
        # 2) with key: Claude gets only the matched card's notes and the exact objection
        sent=[]
        async def handler(route):
            sent.append(json.loads(route.request.post_data)); await route.fulfill(status=200,content_type='application/json',body=json.dumps(FAKE))
        await pg.evaluate("localStorage.setItem('callcoach.cfg',JSON.stringify({antKey:'test-key',remember:true}))")
        await pg.route('https://api.anthropic.com/**',handler)
        await pg.reload(); r=await quick(pg,"it's too expensive"); await pg.wait_for_timeout(400)
        r=await quick(pg,"it's too expensive") if not sent else r
        await pg.wait_for_timeout(400)
        titles=await pg.locator('#qGrid .qp h3').all_text_contents(); src=await pg.text_content('#qSrc')
        body=sent[-1]; msg=body['messages'][0]['content']
        assert 'exactly as the agent typed it: "it\'s too expensive"' in msg and 'Playbook notes for this objection (Price' in msg
        assert 'Deductible' not in msg and 'partner' not in msg, msg
        assert body.get('temperature')==0.3 and 'All three pointers must answer that exact objection' in body['system']
        assert titles==['Acknowledge the price',"Find what's behind it",'Next step on price'] and src=='From Claude', (titles,src)
        print('CLAUDE OK:',titles)
        await pg.screenshot(path='/tmp/quick.png')
        print('ERRORS:',errs); assert not errs
        await b.close()
asyncio.run(main())
