import copy
import json

def insert_after(row, after_key, key, value):
    out = {}
    for k, v in row.items():
        if k == key:
            continue
        out[k] = v
        if k == after_key:
            out[key] = value
    if key not in out:
        out[key] = value
    return out

def align_weekly_payload(payload, reg_entries):
    """Align Cars weekly names and official release dates to registry.

    releaseOrPeriod stays (銷售期間／「發售中」). displayNumber is not
    overwritten when registry uses 「官方未載明」 as a non-number label.
    owned is left as the site's collection flag.
    """
    name_zh = 0
    name_jp = 0
    dates = 0
    aligned = []
    for row in payload['entries']:
        key = row.get('registryNumber')
        if not key or key not in reg_entries:
            aligned.append(row)
            continue
        reg = reg_entries[key]
        if row.get('nameZh') != reg['nameZh']:
            row['nameZh'] = reg['nameZh']
            name_zh += 1
        if row.get('nameJp') != reg['officialNameJp']:
            row['nameJp'] = reg['officialNameJp']
            name_jp += 1
        if row.get('releaseDate') != reg['releaseDate']:
            dates += 1
        row = insert_after(row, 'releaseOrPeriod', 'releaseDate', reg['releaseDate'])
        aligned.append(row)
    payload['entries'] = aligned
    return {'nameZh': name_zh, 'nameJp': name_jp, 'releaseDate': dates}

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
    with open('data/corrections.json', 'r', encoding='utf-8') as f:
        corrections = json.load(f)
    with open('data/character_easter_eggs.json', 'r', encoding='utf-8') as f:
        eggs = json.load(f)

    reg_entries = {e['number']: e for e in registry['entries']}
    corr_entries = {e['number']: e for e in corrections}
    print(f'Loaded {len(reg_entries)} entries from data/registry.json')

    egg_text = eggs[0]['easterEggZh']
    ownership_before = {
        car['id']: {
            'boxed': car.get('boxed'),
            'loose': car.get('loose'),
            'owned': car.get('owned'),
            'catalogId': car.get('catalogId', None),
            'images': copy.deepcopy(car.get('images')),
        }
        for car in cars
    }

    date_changes = 0
    name_zh_changes = 0
    name_jp_changes = 0
    evidence_changes = 0
    updated_cars = 0

    for car in cars:
        k = car.get('registryKey')
        if k not in reg_entries:
            continue
        updated_cars += 1
        e = reg_entries[k]
        c = corr_entries[k]

        if car.get('releaseDate') != e.get('releaseDate'):
            date_changes += 1
            car['releaseDate'] = e['releaseDate']
        if car.get('nameZh') != e['nameZh'] or car.get('name') != e['nameZh']:
            name_zh_changes += 1
        if car.get('officialNameJp') != e['officialNameJp'] or car.get('jpName') != e['officialNameJp']:
            name_jp_changes += 1

        car['officialNameJp'] = e['officialNameJp']
        car['jpName'] = e['officialNameJp']
        car['nameZh'] = e['nameZh']
        car['name'] = e['nameZh']
        for field in ('notes', 'sourceTier', 'confidence', 'verifiedAt', 'releaseDatePrecision'):
            if field in e:
                car[field] = e[field]
        # 來源連結在 corrections；registry 本包沒有 evidenceUrls。
        if car.get('evidenceUrls') != c.get('evidenceUrls'):
            evidence_changes += 1
            car['evidenceUrls'] = c['evidenceUrls']

    c21_jp = next(c for c in cars if c.get('registryKey') == 'C-21_j_p_standard')
    # 彩蛋正文只允許與 character_easter_eggs.json 逐字相同，不改寫。
    if c21_jp.get('handbookBlurbZh') != egg_text:
        c21_jp['handbookBlurbZh'] = egg_text
    if c21_jp.get('characterEasterEggZh') != egg_text:
        c21_jp['characterEasterEggZh'] = egg_text

    for car in cars:
        before = ownership_before[car['id']]
        assert car.get('boxed') == before['boxed'], car['id']
        assert car.get('loose') == before['loose'], car['id']
        assert car.get('owned') == before['owned'], car['id']
        assert car.get('catalogId', None) == before['catalogId'], car['id']
        assert car.get('images') == before['images'], car['id']

    print(
        f'Catalog touched {updated_cars}; nameZh {name_zh_changes}; '
        f'officialNameJp {name_jp_changes}; releaseDate {date_changes}; '
        f'evidenceUrls {evidence_changes}'
    )

    weekly_marker = '    const WEEKLY_PICKS_DATA = '
    weekly_end = ';\n\n    // 核心車輛資料庫'
    weekly_start = html.find(weekly_marker)
    weekly_stop = html.find(weekly_end, weekly_start)
    if weekly_start == -1 or weekly_stop == -1:
        raise ValueError('Could not find WEEKLY_PICKS_DATA')
    weekly = json.loads(html[weekly_start + len(weekly_marker):weekly_stop])
    weekly_stats = align_weekly_payload(weekly, reg_entries)
    print(f'Weekly embed nameZh {weekly_stats["nameZh"]} nameJp {weekly_stats["nameJp"]} releaseDate {weekly_stats["releaseDate"]}')
    html = (
        html[:weekly_start + len(weekly_marker)]
        + json.dumps(weekly, ensure_ascii=False, indent=6)
        + html[weekly_stop:]
    )

    for weekly_path in ('data/weekly_picks.json', 'weekly_picks.json'):
        with open(weekly_path, 'r', encoding='utf-8') as f:
            file_weekly = json.load(f)
        file_stats = align_weekly_payload(file_weekly, reg_entries)
        print(f'{weekly_path} nameZh {file_stats["nameZh"]} nameJp {file_stats["nameJp"]} releaseDate {file_stats["releaseDate"]}')
        with open(weekly_path, 'w', encoding='utf-8') as f:
            json.dump(file_weekly, f, ensure_ascii=False, indent=2)
            f.write('\n')

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
    assert c21_jp.get('characterEasterEggZh') == egg_text
    assert c21_jp.get('handbookBlurbZh') == egg_text
    c21_ids = [c['id'] for c in cars if c.get('displayNumber') == 'C-21']
    assert c21_ids == [
        'C-21_j_p_standard',
        'C-21_holly_standard',
        'C-21_mcqueen_cars3_standard',
    ], c21_ids

    c34_grc = next(c for c in cars if c.get('registryKey') == 'C-34_mcqueen_grc')
    assert c34_grc['releaseDate'] == '2025-10-18'
    assert c34_grc['nameZh'] == '閃電麥坤（GRC 版）'

    c06_doc = next(c for c in cars if c.get('registryKey') == 'C-06_doc_standard')
    assert c06_doc['boxed'] == 0 and c06_doc['loose'] == 0 and c06_doc['owned'] is False

    unknown = [c for c in cars if c.get('registryKey') in reg_entries and c.get('releaseDate') == '官方未載明']
    assert len(unknown) == 3, [c['registryKey'] for c in unknown]
    with_evidence = [c for c in cars if c.get('registryKey') in reg_entries and c.get('evidenceUrls')]
    assert len(with_evidence) == 152

    # Weekly block sits above CARS_DATABASE, so re-find offsets after that edit.
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker, start_idx)
    if start_idx == -1 or end_idx == -1:
        raise ValueError('Could not re-find CARS_DATABASE after weekly update')

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
