import re

def update_files():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    ntc_images = {
        'NTC-MATTEL-F1-SET': 'tomica_official_images/NTC-MATTEL-F1-SET.jpg',
        'NTC-PULLBACK-3PACK': 'tomica_official_images/NTC-PULLBACK-3PACK.jpg',
        'NTC-LARGE-PLASTIC-MCQUEEN': 'tomica_official_images/NTC-LARGE-PLASTIC-MCQUEEN.jpg',
        'NTC-CHOROQ-STYLE-MCQUEEN': 'tomica_official_images/NTC-CHOROQ-STYLE-MCQUEEN.jpg',
        'NTC-LARGE-PLASTIC-MATER': 'tomica_official_images/NTC-LARGE-PLASTIC-MATER.jpg',
        'NTC-LARGE-PLASTIC-MACK': 'tomica_official_images/NTC-LARGE-PLASTIC-MACK.jpg'
    }

    for ntc_id, img_url in ntc_images.items():
        pattern = rf'("id":\s*"{ntc_id}".*?"images":\s*)\[\]'
        replacement = rf'\g<1>[\n              {{\n                "url": "{img_url}",\n                "label": "📷 藏品實拍"\n              }}\n            ]'
        content, count = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
        if count != 1:
            raise ValueError(f'Failed to replace {ntc_id}')

    # Update imageTagLabel in generateGridCardHtml
    old_tag = '''      if (hasImages) {
        stageContentHtml = `
            <img 
              src="${displayImg}" 
              referrerpolicy="no-referrer"
              alt="${car.name}" 
              loading="lazy"
              onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\\'w-full h-full flex flex-col items-center justify-center bg-zinc-100 text-zinc-400 gap-1 select-none\\'><span class=\\'text-2xl\\'>📷</span><span class=\\'text-xs font-bold tracking-wider\\'>暫無官方圖</span></div>';"
            >
            <span class="absolute bottom-1.5 right-1.5 bg-black/60 text-white text-[9px] px-1.5 py-0.5 rounded backdrop-blur-xs pointer-events-none">
              🌟 官方圖
            </span>
        `;
      }'''

    new_tag = '''      if (hasImages) {
        const imageTagLabel = (car.category === 'cars_non_tomica') ? '📷 藏品實拍' : '🌟 官方圖';
        stageContentHtml = `
            <img 
              src="${displayImg}" 
              referrerpolicy="no-referrer"
              alt="${car.name}" 
              loading="lazy"
              onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\\'w-full h-full flex flex-col items-center justify-center bg-zinc-100 text-zinc-400 gap-1 select-none\\'><span class=\\'text-2xl\\'>📷</span><span class=\\'text-xs font-bold tracking-wider\\'>暫無官方圖</span></div>';"
            >
            <span class="absolute bottom-1.5 right-1.5 bg-black/60 text-white text-[9px] px-1.5 py-0.5 rounded backdrop-blur-xs pointer-events-none">
              ${imageTagLabel}
            </span>
        `;
      }'''

    if old_tag not in content:
        raise ValueError('old_tag not found in content!')

    content = content.replace(old_tag, new_tag, 1)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

    with open('tomica_cars_collection.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print('Successfully updated index.html and tomica_cars_collection.html!')

if __name__ == '__main__':
    update_files()
