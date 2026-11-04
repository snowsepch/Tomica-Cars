#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrades Japanese OCR and Visual Matching pipeline in index.html:
1. Fixes startOcr pipeline order: readEngSignals -> readJapaneseName -> showVisual -> showManualPrompt.
2. Enhances readJapaneseName passes: targets lower 65% of the box with PSM 11, and checks for box numbers as fallback.
3. Enhances buildExtraIndex & phrasesFromRecognition: indexes character name prefixes (e.g. バズ・ライトイヤー, ドック・ハドソン, メーター, ハム, etc.) and allows multi-car matches up to 5 cars.
4. Enhances rankVisual / rankChannel: returns top 4 candidates (pool.slice(0, 4)) instead of forcing picked = [hueLeader], giving users genuine choice as promised by "這些可能是，請點選".
5. Synchronizes index.html to tomica_cars_collection.html.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, 'index.html')
MIRROR_PATH = os.path.join(ROOT, 'tomica_cars_collection.html')

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update rankChannel in rankVisual to return top 4 candidate cars instead of picked = [hueLeader]
old_rank_channel_pick = """          if (hueLeader.band - bandLeader.band >= 0.08 && bandLeader.band <= 0.70) {
            picked = pool.filter(function (item) {
              return item.band <= bandLeader.band + 0.04;
            }).slice(0, 3);
          } else {
            picked = [hueLeader];
          }
        } else {
          picked = pool.slice(0, 3);
        }"""

new_rank_channel_pick = """          if (hueLeader && hueLeader.band - bandLeader.band >= 0.08 && bandLeader.band <= 0.70) {
            picked = pool.filter(function (item) {
              return item.band <= bandLeader.band + 0.05;
            }).slice(0, 4);
          } else {
            picked = pool.slice(0, 4);
          }
        } else {
          picked = pool.slice(0, 4);
        }"""

if old_rank_channel_pick in html:
    html = html.replace(old_rank_channel_pick, new_rank_channel_pick)
    print("Updated rankChannel multi-car candidate selection.")
else:
    print("Warning: old_rank_channel_pick not matched.")

# 2. Update showVisual note text
old_show_visual_note = "setOcrNote('依外形、配色推測，不是讀到編號。');"
new_show_visual_note = "setOcrNote('依外形、配色推測，請在下方候選車款中點選：');"
if old_show_visual_note in html:
    html = html.replace(old_show_visual_note, new_show_visual_note)
    print("Updated showVisual note text.")

# 3. Update buildExtraIndex phrase indexing & character prefixes
old_build_extra = """          var phraseBlob = [car.jpName, car.officialNameJp, car.keywords, car.description].filter(Boolean).join('\\n');
          var phraseRe = /[\\u30A0-\\u30FF\\u30FC]{8,}/g;
          var phraseMatch;
          var seenPhrase = {};
          while ((phraseMatch = phraseRe.exec(phraseBlob))) {
            var phraseRaw = phraseMatch[0];
            var phraseKey = foldKana(phraseRaw);
            if (phraseKey.length < 7 || seenPhrase[phraseKey]) continue;
            seenPhrase[phraseKey] = true;
            if (!phrases[phraseKey]) phrases[phraseKey] = { raw: phraseRaw, cars: [] };
            else if (phraseRaw.length > phrases[phraseKey].raw.length) phrases[phraseKey].raw = phraseRaw;
            pushUnique(phrases[phraseKey].cars, car);
          }
        });
        Object.keys(dream).forEach(function (key) { if (dream[key].length > 4) delete dream[key]; });
        Object.keys(dm).forEach(function (key) { if (dm[key].length > 4) delete dm[key]; });
        Object.keys(names).forEach(function (key) { if (names[key].cars.length > 4) delete names[key]; });
        Object.keys(phrases).forEach(function (key) { if (phrases[key].cars.length !== 1) delete phrases[key]; });"""

new_build_extra = """          var phraseBlob = [car.jpName, car.officialNameJp, car.keywords, car.description].filter(Boolean).join('\\n');
          var phraseRe = /[\\u30A0-\\u30FF\\u30FC]{4,}/g;
          var phraseMatch;
          var seenPhrase = {};
          while ((phraseMatch = phraseRe.exec(phraseBlob))) {
            var phraseRaw = phraseMatch[0];
            var phraseKey = foldKana(phraseRaw);
            if (phraseKey.length < 4 || seenPhrase[phraseKey]) continue;
            seenPhrase[phraseKey] = true;
            if (!phrases[phraseKey]) phrases[phraseKey] = { raw: phraseRaw, cars: [] };
            else if (phraseRaw.length > phrases[phraseKey].raw.length) phrases[phraseKey].raw = phraseRaw;
            pushUnique(phrases[phraseKey].cars, car);
          }
          var charM = (car.jpName || car.officialNameJp || '').match(/^([^(（]+)/);
          if (charM) {
            var charRaw = charM[1].trim();
            var charKey = foldKana(charRaw);
            if (charKey.length >= 2) {
              if (!phrases[charKey]) phrases[charKey] = { raw: charRaw, cars: [] };
              pushUnique(phrases[charKey].cars, car);
            }
          }
        });
        Object.keys(dream).forEach(function (key) { if (dream[key].length > 4) delete dream[key]; });
        Object.keys(dm).forEach(function (key) { if (dm[key].length > 4) delete dm[key]; });
        Object.keys(names).forEach(function (key) { if (names[key].cars.length > 5) delete names[key]; });
        Object.keys(phrases).forEach(function (key) {
          if (phrases[key].cars.length > 5 && !['ライトニングマックィン', 'メタ'].includes(key)) {
            delete phrases[key];
          }
        });"""

if old_build_extra in html:
    html = html.replace(old_build_extra, new_build_extra)
    print("Updated buildExtraIndex phrase & character extraction.")
else:
    print("Warning: old_build_extra not matched.")

# 4. Update phrasesFromRecognition
old_phrases_from_rec = """      function phrasesFromRecognition(data) {
        var index = buildExtraIndex();
        if (!index.phraseKeys.length) return null;
        var lines = (data && data.lines) || [];
        var cars = [];
        var label = '';
        lines.forEach(function (line) {
          if (!line || !line.text) return;
          if (typeof line.confidence === 'number' && line.confidence < 45) return;
          var folded = foldKana(line.text);
          if (folded.length < 7) return;
          index.phraseKeys.forEach(function (key) {
            if (folded.indexOf(key) === -1) return;
            if (!label) label = index.phrases[key].raw;
            pushUnique(cars, index.phrases[key].cars[0]);
          });
        });
        if (cars.length !== 1) return null;
        return { kind: 'name', label: label, cars: cars };
      }"""

new_phrases_from_rec = """      function phrasesFromRecognition(data) {
        var index = buildExtraIndex();
        if (!index.phraseKeys.length) return null;
        var lines = (data && data.lines) || [];
        var cars = [];
        var label = '';
        var searchTexts = [];
        lines.forEach(function (line) {
          if (line && line.text) searchTexts.push(line.text);
        });
        if (data && data.text) searchTexts.push(data.text);
        searchTexts.forEach(function (text) {
          var folded = foldKana(text);
          if (folded.length < 2) return;
          index.phraseKeys.forEach(function (key) {
            if (folded.indexOf(key) === -1) return;
            var hit = index.phrases[key];
            if (!label || key.length > label.length) label = hit.raw;
            hit.cars.forEach(function (c) { pushUnique(cars, c); });
          });
        });
        if (!cars.length || cars.length > 5) return null;
        return { kind: 'name', label: label, cars: cars };
      }"""

if old_phrases_from_rec in html:
    html = html.replace(old_phrases_from_rec, new_phrases_from_rec)
    print("Updated phrasesFromRecognition.")
else:
    print("Warning: old_phrases_from_rec not matched.")

# 5. Update readJapaneseName passes & fallback
old_read_jp = """      function readJapaneseName(img, id) {
        setOcrNote('外形對不上，正在讀盒上的日文品名。照片不會上傳。');
        var passes = [
          { crop: { x: 0.04, y: 0.16, w: 0.92, h: 0.48 }, edge: 1700, psm: '6', color: true },
          { crop: { x: 0.02, y: 0.02, w: 0.96, h: 0.96 }, edge: 1700, psm: '6', color: true }
        ];
        return ensureWorker('jpn').then(function (worker) {
          var chain = Promise.resolve(null);
          passes.forEach(function (pass) {
            chain = chain.then(function (hit) {
              if (hit || id !== runId || userLocked) return hit;
              return recognizeRaw(worker, img, pass, id).then(function (data) {
                if (!data || id !== runId || userLocked) return null;
                return phrasesFromRecognition(data) || namesFromRecognition(data);
              });
            });
          });
          return chain;
        }).catch(function () {
          return null;
        });
      }"""

new_read_jp = """      function readJapaneseName(img, id) {
        setOcrNote('正在比對盒上日文品名…照片不會上傳。');
        var content = contentCrop(img);
        var passes = [
          { crop: { x: 0.02, y: 0.35, w: 0.96, h: 0.63 }, edge: 2000, psm: '11', color: true },
          { crop: content, edge: 2000, psm: '11', color: true },
          { crop: { x: 0.02, y: 0.35, w: 0.96, h: 0.63 }, edge: 2000, psm: '6', color: false },
          { crop: { x: 0.02, y: 0.02, w: 0.96, h: 0.96 }, edge: 1800, psm: '11', color: true }
        ];
        return ensureWorker('jpn').then(function (worker) {
          var chain = Promise.resolve(null);
          passes.forEach(function (pass) {
            chain = chain.then(function (hit) {
              if (hit || id !== runId || userLocked) return hit;
              return recognizeRaw(worker, img, pass, id).then(function (data) {
                if (!data || id !== runId || userLocked) return null;
                var hitSignal = phrasesFromRecognition(data) || namesFromRecognition(data);
                if (hitSignal) return hitSignal;
                var nums = numbersFromRecognition(data, true);
                if (nums.length) return { kind: 'c', numbers: nums };
                return null;
              });
            });
          });
          return chain;
        }).catch(function () {
          return null;
        });
      }"""

if old_read_jp in html:
    html = html.replace(old_read_jp, new_read_jp)
    print("Updated readJapaneseName passes and fallback.")
else:
    print("Warning: old_read_jp not matched.")

# 6. Update startOcr pipeline order
old_start_ocr_order = """          return showVisual(readyImg, id).then(function (shown) {
            if (shown || id !== runId || userLocked) return null;
            return readJapaneseName(readyImg, id).then(function (nameHit) {
              if (id !== runId || userLocked) return null;
              if (nameHit) showSignal(nameHit);
              else showManualPrompt();
              return null;
            });
          });"""

new_start_ocr_order = """          return readJapaneseName(readyImg, id).then(function (nameHit) {
            if (id !== runId || userLocked) return null;
            if (nameHit) {
              showSignal(nameHit);
              return null;
            }
            return showVisual(readyImg, id).then(function (shown) {
              if (shown || id !== runId || userLocked) return null;
              showManualPrompt();
              return null;
            });
          });"""

if old_start_ocr_order in html:
    html = html.replace(old_start_ocr_order, new_start_ocr_order)
    print("Updated startOcr pipeline order (readJapaneseName -> showVisual).")
else:
    print("Warning: old_start_ocr_order not matched.")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {INDEX_PATH} ({len(html)} bytes).")

with open(MIRROR_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {MIRROR_PATH} ({len(html)} bytes).")
