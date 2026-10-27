import json
import re
import os

def update_catalog():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract CARS_DATABASE
    start_marker = '    const CARS_DATABASE = '
    end_marker = ';\n\n    // 狀態變數：支援多選系列與重複獨立過濾'

    start_idx = html.find(start_marker)
    if start_idx == -1:
        raise ValueError('Could not find start of CARS_DATABASE')

    end_idx = html.find(end_marker, start_idx)
    if end_idx == -1:
        raise ValueError('Could not find end of CARS_DATABASE')

    cars = json.loads(html[start_idx + len(start_marker):end_idx])
    print(f'Parsed {len(cars)} cars from index.html')

    remote_updated = 0
    for car in cars:
        # Check C-06_doc_standard
        if car.get('id') == 'C-06_doc_standard' or car.get('registryKey') == 'C-06_doc_standard':
            car['owned'] = True
            car['boxed'] = 0
            car['loose'] = 1
            car['description'] = "【經典已購入】ドック・ハドソン(スタンダードタイプ)。官方編號：C-6。深藍色 1951 Hudson Hornet 經典豪華轎跑車型，搭配招牌白牆輪胎與精緻水箱罩電鍍細節。"
            car['relatedOwnedNote'] = "同號已購入：C-6 克魯茲·拉米雷斯（Dinoco 盒裝）。相關已購入：C-8 韓大夫（ファビュラス）、C-27 韓大夫（パトカー）、SP 韓大夫附活塞盃。"
            print('Updated C-06_doc_standard to owned=true, boxed=0, loose=1')

        # Update remote image URLs to local tomica_official_images
        imgs = car.get('images', [])
        for idx, img in enumerate(imgs):
            u = img.get('url', '')
            if u.startswith('http:') or u.startswith('https:'):
                slug = car['id'].replace('/', '_')
                filename = f'{slug}_{idx}_official.jpg' if len(imgs) > 1 else f'{slug}_official.jpg'
                local_path = f'tomica_official_images/{filename}'
                if os.path.isfile(local_path):
                    img['url'] = local_path
                    remote_updated += 1
                else:
                    print(f'Warning: local image not found: {local_path}')

    print(f'Replaced {remote_updated} remote image URLs with local tomica_official_images/ paths')

    # Re-serialize CARS_DATABASE
    new_cars_json = json.dumps(cars, ensure_ascii=False, indent=2)
    new_html = html[:start_idx + len(start_marker)] + new_cars_json + html[end_idx:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    with open('tomica_cars_collection.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print('Saved updated index.html and tomica_cars_collection.html')

if __name__ == '__main__':
    update_catalog()
