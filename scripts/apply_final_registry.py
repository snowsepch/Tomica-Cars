import json
import re
import subprocess

def apply_registry_update():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Locate CARS_DATABASE
    start_marker = '    const CARS_DATABASE = '
    end_marker = ';\n\n    // 狀態變數：支援多選系列與重複獨立過濾'
    
    start_idx = html.find(start_marker)
    if start_idx == -1:
        raise ValueError('Could not find start of CARS_DATABASE')
    
    end_idx = html.find(end_marker, start_idx)
    if end_idx == -1:
        raise ValueError('Could not find end of CARS_DATABASE')

    cars_json_str = html[start_idx + len(start_marker):end_idx]
    cars = json.loads(cars_json_str)
    print(f'Parsed {len(cars)} cars from CARS_DATABASE')

    with open('data/registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)

    reg_entries = {e['number']: e for e in registry['entries']}
    print(f'Loaded {len(reg_entries)} entries from data/registry.json')

    date_changes = 0
    updated_cars = 0

    for car in cars:
        k = car.get('registryKey')
        if k in reg_entries:
            updated_cars += 1
            e = reg_entries[k]
            
            # Record release date change
            if car.get('releaseDate') != e.get('releaseDate'):
                date_changes += 1

            # Update official fields
            car['officialNameJp'] = e['officialNameJp']
            car['jpName'] = e['officialNameJp']
            car['nameZh'] = e['nameZh']
            car['name'] = e['nameZh']
            car['releaseDate'] = e['releaseDate']
            
            if 'notes' in e:
                car['notes'] = e['notes']
            if 'sourceTier' in e:
                car['sourceTier'] = e['sourceTier']
            if 'confidence' in e:
                car['confidence'] = e['confidence']
            if 'verifiedAt' in e:
                car['verifiedAt'] = e['verifiedAt']
            if 'releaseDatePrecision' in e:
                car['releaseDatePrecision'] = e['releaseDatePrecision']
            if 'evidenceUrls' in e:
                car['evidenceUrls'] = e['evidenceUrls']

    print(f'Updated {updated_cars} cars, {date_changes} release dates updated')

    # Verification of key constraints
    assert len(cars) == 178, f'Expected 178 cars, got {len(cars)}'
    
    # NTC check
    ntc_cars = [c for c in cars if c.get('category') == 'cars_non_tomica']
    assert len(ntc_cars) == 6, f'Expected 6 non-tomica cars, got {len(ntc_cars)}'
    for nc in ntc_cars:
        cid = nc.get('id')
        assert len(nc.get('images', [])) == 1, f'{cid} must have 1 sanitized image'
        assert nc['images'][0]['label'] == '📷 藏品實拍'

    # Ownership checks
    sp_mater = next(c for c in cars if c.get('registryKey') == 'SP_mater_mcqueen_2023_special')
    assert sp_mater['boxed'] == 0 and sp_mater['loose'] == 0 and sp_mater['owned'] is False
    assert sp_mater['releaseDate'] == '2023-09'

    c21_jp = next(c for c in cars if c.get('registryKey') == 'C-21_j_p_standard')
    assert c21_jp['releaseDate'] == '2018-10'
    assert 'Apple' in c21_jp.get('characterEasterEggZh', '')

    c34_grc = next(c for c in cars if c.get('registryKey') == 'C-34_mcqueen_grc')
    assert c34_grc['releaseDate'] == '2025-10-18'

    c06_doc = next(c for c in cars if c.get('registryKey') == 'C-06_doc_standard')
    assert c06_doc['boxed'] == 0 and c06_doc['loose'] == 0 and c06_doc['owned'] is False

    # Serialize CARS_DATABASE back with neat indentation
    new_cars_json = json.dumps(cars, ensure_ascii=False, indent=2)
    new_html = html[:start_idx + len(start_marker)] + new_cars_json + html[end_idx:]

    # Update modal to show sourceTier / confidence if available
    old_modal_row = '''          <div class="flex items-center justify-between">
            <span class="text-zinc-500">官方發售日期</span>
            <span class="font-semibold text-zinc-800 font-mono">${releaseText}</span>
          </div>'''

    new_modal_row = '''          <div class="flex items-center justify-between">
            <span class="text-zinc-500">官方發售日期</span>
            <div class="text-right">
              <span class="font-semibold text-zinc-800 font-mono">${releaseText}</span>
              ${car.sourceTier ? `<span class="ml-1.5 text-[10px] px-1.5 py-0.5 rounded bg-zinc-200/80 text-zinc-700 font-medium">${car.sourceTier}${car.confidence ? ' (' + car.confidence + ')' : ''}</span>` : ''}
            </div>
          </div>'''

    if old_modal_row in new_html:
        new_html = new_html.replace(old_modal_row, new_modal_row, 1)
        print('Updated modal detail to show sourceTier and confidence')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    with open('tomica_cars_collection.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print('Successfully written updated index.html and tomica_cars_collection.html!')

if __name__ == '__main__':
    apply_registry_update()
