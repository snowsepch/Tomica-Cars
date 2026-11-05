import asyncio
import base64
import json
import os
import subprocess
import time
import urllib.request
import websockets

async def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_url = f'file://{os.path.join(root, "index.html")}'
    
    port = 9223
    proc = subprocess.Popen([
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '--headless=new',
        '--disable-gpu',
        f'--remote-debugging-port={port}',
        '--no-first-run',
        '--no-default-browser-check',
        'about:blank'
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(1.2)
    
    try:
        tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json').read().decode('utf-8'))
        page_tab = next(t for t in tabs if t.get('type') == 'page')
        ws_url = page_tab['webSocketDebuggerUrl']
        
        async with websockets.connect(ws_url, max_size=50 * 1024 * 1024) as ws:
            msg_id = 0
            
            async def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                req = {'id': msg_id, 'method': method, 'params': params or {}}
                await ws.send(json.dumps(req))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id:
                        return resp.get('result', {})
            
            # 1. Enable Page and Emulation
            await send('Page.enable')
            await send('Emulation.setDeviceMetricsOverride', {
                'width': 390,
                'height': 844,
                'deviceScaleFactor': 2,
                'mobile': True
            })
            await send('Emulation.setUserAgentOverride', {
                'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
            })
            
            # 2. Navigate
            await send('Page.navigate', {'url': index_url})
            await asyncio.sleep(2.5) # Wait for network, fonts and CSS animations
            
            # 3. Evaluate assertions
            async def evaluate(expr):
                res = await send('Runtime.evaluate', {
                    'expression': expr,
                    'returnByValue': True,
                    'awaitPromise': True
                })
                return res.get('result', {}).get('value')
            
            title = await evaluate('document.title')
            font_loaded = await evaluate("document.fonts.check('16px jf-openhuninn')")
            inner_w = await evaluate('window.innerWidth')
            scroll_w = await evaluate('document.documentElement.scrollWidth')
            s1 = await evaluate("document.getElementById('s1').textContent")
            s2 = await evaluate("document.getElementById('s2').textContent")
            s3 = await evaluate("document.getElementById('s3').textContent")
            hero_no = await evaluate("document.getElementById('heroNo').textContent")
            hero_nm = await evaluate("document.getElementById('heroNm').textContent")
            tbp = await evaluate("document.getElementById('tbp').textContent")
            
            # Check chapter counts sum
            toc_stats = await evaluate("""
                (() => {
                    const links = Array.from(document.querySelectorAll('#tocL a'));
                    let totalOwned = 0, totalCars = 0;
                    links.forEach(a => {
                        const pr = a.querySelector('.pr').textContent.trim();
                        const [o, t] = pr.split('/').map(s => parseInt(s, 10));
                        totalOwned += o;
                        totalCars += t;
                    });
                    return { totalOwned, totalCars, count: links.length };
                })()
            """)
            
            # Check unowned card image filter (should NOT be grayscale or opacity reduced)
            unowned_style = await evaluate("""
                (() => {
                    const uCard = document.querySelector('.card.u');
                    if (!uCard) return null;
                    const img = uCard.querySelector('img');
                    const comp = img ? window.getComputedStyle(img) : null;
                    const cardComp = window.getComputedStyle(uCard);
                    return {
                        filter: comp ? comp.filter : null,
                        opacity: cardComp.opacity,
                        boxShadow: window.getComputedStyle(uCard.querySelector('.fr')).boxShadow
                    };
                })()
            """)
            
            # Check photo check button existence
            cam_btn = await evaluate("Boolean(document.getElementById('photoCheckOpenBtn'))")
            
            print('=== BROWSER VALIDATION REPORT ===')
            print(f'Page Title: {title} (Expected: Tomica 小車圖鑑)')
            print(f'Font jf-openhuninn Loaded: {font_loaded}')
            print(f'Viewport Width: {inner_w}px, Document Scroll Width: {scroll_w}px (Horizontal overflow: {scroll_w > inner_w})')
            print(f'Stats: s1={s1}, s2={s2}, s3={s3}, tbp={tbp}')
            print(f'Hero: {hero_no} - {hero_nm}')
            print(f'TOC Chapters: {toc_stats}')
            print(f'Unowned Card Style: {unowned_style}')
            print(f'Photo Check Open Button in DOM: {cam_btn}')
            
            # 4. Take Screenshots
            cover_shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(root, 'mobile_verified_cover.png'), 'wb') as f:
                f.write(base64.b64decode(cover_shot['data']))
            print('Saved mobile_verified_cover.png (390x844 viewport)')
            
            # Test detail modal opening
            await evaluate("openCarDetail('C-01')")
            await asyncio.sleep(0.8)
            dt_open = await evaluate("document.getElementById('dt').classList.contains('open')")
            dt_pos = await evaluate("document.getElementById('dPos').textContent")
            print(f'Detail Modal Opened: {dt_open}, Position: {dt_pos}')
            
            detail_shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(root, 'mobile_verified_detail.png'), 'wb') as f:
                f.write(base64.b64decode(detail_shot['data']))
            print('Saved mobile_verified_detail.png')
            
            # Close detail modal and check return
            await evaluate("closeCarDetail()")
            await asyncio.sleep(0.3)
            dt_closed = await evaluate("!document.getElementById('dt').classList.contains('open')")
            print(f'Detail Modal Closed: {dt_closed}')
            # Scroll to Chapter 1
            await evaluate("document.getElementById('ch-cars_tomica').scrollIntoView()")
            await asyncio.sleep(0.8)
            grid_shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(root, 'mobile_verified_grid.png'), 'wb') as f:
                f.write(base64.b64decode(grid_shot['data']))
            print('Saved mobile_verified_grid.png')

            # Switch to Weekly tab
            await evaluate("setTab('week', true)")
            await asyncio.sleep(0.8)
            weekly_shot = await send('Page.captureScreenshot', {'format': 'png'})
            with open(os.path.join(root, 'mobile_verified_weekly.png'), 'wb') as f:
                f.write(base64.b64decode(weekly_shot['data']))
            print('Saved mobile_verified_weekly.png')

    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
