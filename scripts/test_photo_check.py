import asyncio
import json
import os
import subprocess
import time
import urllib.request
import websockets

async def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_url = f'file://{os.path.join(root, "index.html")}'
    test_img = os.path.join(root, 'tomica_images', 'C-14_mater_20th_box2.jpg')
    
    port = 9224
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
    
    network_requests = []
    
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
                    if resp.get('method') == 'Network.requestWillBeSent':
                        network_requests.append(resp['params']['request']['url'])
                    if resp.get('id') == msg_id:
                        return resp.get('result', {})
            
            # Listen to network requests
            await send('Network.enable')
            await send('Page.enable')
            await send('DOM.enable')
            
            # Navigate to index.html
            await send('Page.navigate', {'url': index_url})
            await asyncio.sleep(2.0)
            
            # Get node for #photoCheckLibraryInput
            doc = await send('DOM.getDocument')
            node = await send('DOM.querySelector', {
                'nodeId': doc['root']['nodeId'],
                'selector': '#photoCheckLibraryInput'
            })
            
            print(f'Found #photoCheckLibraryInput nodeId: {node.get("nodeId")}')
            
            # Set input files
            await send('DOM.setFileInputFiles', {
                'files': [test_img],
                'nodeId': node['nodeId']
            })
            
            # Wait for OCR and matching to complete (Tesseract worker initialization + OCR)
            print('Waiting for OCR and matching...')
            for wait_sec in range(12):
                await asyncio.sleep(1)
                status_text = await send('Runtime.evaluate', {
                    'expression': 'document.getElementById("photoCheckStatus").textContent',
                    'returnByValue': True
                })
                res_count = await send('Runtime.evaluate', {
                    'expression': 'document.querySelectorAll("#photoCheckResults .photo-check-result").length',
                    'returnByValue': True
                })
                st = status_text.get('result', {}).get('value', '')
                cnt = res_count.get('result', {}).get('value', 0)
                if cnt > 0:
                    print(f'Match found in {wait_sec+1}s! Results count: {cnt}, status: {st}')
                    break
            
            results_text = await send('Runtime.evaluate', {
                'expression': 'Array.from(document.querySelectorAll("#photoCheckResults .photo-check-result")).map(r => r.innerText)',
                'returnByValue': True
            })
            vals = results_text.get('result', {}).get('value', [])
            print('Top results:', vals[:3])
            
            # Check for any external image upload requests
            gemini_uploads = [url for url in network_requests if 'googleapis.com' in url or 'generativelanguage' in url]
            print(f'Gemini/Google API upload requests observed: {len(gemini_uploads)}')
            
            assert len(gemini_uploads) == 0, 'No Google API requests should be sent when no Gemini key is set'
            print('Photo check OCR offline verification PASSED!')
            
    finally:
        proc.terminate()

if __name__ == '__main__':
    asyncio.run(main())
