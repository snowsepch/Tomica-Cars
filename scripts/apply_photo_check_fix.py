#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applies photo check fixes to index.html and tomica_cars_collection.html:
1. Inlines PRECOMPUTED_CATALOG_FEATURES (100% offline, zero network requests, solves raw.githack 403 on images).
2. Updates ensureCatalogFeatures() to use PRECOMPUTED_CATALOG_FEATURES.
3. Adds flattenOcrData() in recognizeRaw() to unpack Tesseract.js v5 block hierarchy into lines and words.
4. Adds SP support and i/a character normalization in extractNumbers() and tokenNumber().
5. Relaxes numbersFromRecognition() so multiple detected candidate numbers do not discard the valid number.
6. Ensures carNumbers() and C-38 Hamm recognize SP.
7. Syncs index.html to tomica_cars_collection.html.
"""

import os
import json
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, 'index.html')
MIRROR_PATH = os.path.join(ROOT, 'tomica_cars_collection.html')
FEATURES_JSON = os.path.join(ROOT, 'data', 'precomputed_catalog_features.json')

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

with open(FEATURES_JSON, 'r', encoding='utf-8') as f:
    features_data = json.load(f)

features_min_str = json.dumps(features_data, ensure_ascii=False, separators=(',', ':'))

# 1. Update Hamm keywords
old_hamm_kw = '"keywords": "C 38 ham standard C-38 C-38_ham_standard C38 ハム(スタンダードタイプ)",'
new_hamm_kw = '"keywords": "C 38 ham standard C-38 C-38_ham_standard C38 SP ハム(スタンダードタイプ)",'
if old_hamm_kw in html:
    html = html.replace(old_hamm_kw, new_hamm_kw)
    print("Updated Hamm keywords with SP.")

# 2. Update extractNumbers()
old_extract_numbers = """      function extractNumbers(text) {
        var source = normalizeDigits(text);
        var out = [];
        var re = /C\\s*[-]?\\s*([0-9Il|OoQZzSs]{1,3})(?![0-9A-Za-z])/gi;
        var match;
        while ((match = re.exec(source))) {
          var digits = match[1]
            .replace(/[Il|]/g, '1')
            .replace(/[OoQ]/g, '0')
            .replace(/[Zz]/g, '2')
            .replace(/[Ss]/g, '5');
          if (!/^\\d{1,3}$/.test(digits)) continue;
          var n = parseInt(digits, 10);
          if (n < 1 || n > 50) continue;
          out.push('C-' + n);
        }
        return unique(out);
      }"""

new_extract_numbers = """      function extractNumbers(text) {
        var source = normalizeDigits(text);
        var out = [];
        var re = /C\\s*[-]?\\s*([0-9Il|iOoQZzSsAa]{1,3})(?![0-9A-Za-z])/gi;
        var match;
        while ((match = re.exec(source))) {
          var digits = match[1]
            .replace(/[Il|i]/g, '1')
            .replace(/[OoQ]/g, '0')
            .replace(/[Zz]/g, '2')
            .replace(/[Ss]/g, '5')
            .replace(/[Aa]/g, '4');
          if (!/^\\d{1,3}$/.test(digits)) continue;
          var n = parseInt(digits, 10);
          if (n < 1 || n > 50) continue;
          out.push('C-' + n);
        }
        if (!out.length) {
          if (/(^|[^A-Za-z0-9])SP(?![A-Za-z0-9])/i.test(source)) {
            out.push('SP');
          }
        }
        return unique(out);
      }"""

if old_extract_numbers in html:
    html = html.replace(old_extract_numbers, new_extract_numbers)
    print("Updated extractNumbers() with SP and i/a tolerance.")
else:
    print("Warning: old extractNumbers() not matched exactly.")

# 3. Update carNumbers()
old_car_numbers = """      function carNumbers(car) {
        var set = {};
        [car.displayNumber, car.id, car.registryKey].forEach(function (value) {
          extractNumbers(value).forEach(function (num) { set[num] = true; });
        });
        if (normText(car.displayNumber) === 'sp') set.SP = true;
        return set;
      }"""

new_car_numbers = """      function carNumbers(car) {
        var set = {};
        [car.displayNumber, car.id, car.registryKey].forEach(function (value) {
          extractNumbers(value).forEach(function (num) { set[num] = true; });
        });
        if (normText(car.displayNumber) === 'sp' || (car.keywords && /\\bSP\\b/i.test(car.keywords))) set.SP = true;
        return set;
      }"""

if old_car_numbers in html:
    html = html.replace(old_car_numbers, new_car_numbers)
    print("Updated carNumbers().")
else:
    print("Warning: old carNumbers() not matched exactly.")

# 4. Update tokenNumber()
old_token_number = """      function tokenNumber(text) {
        var flat = normalizeDigits(String(text || ''))
          .replace(/\\s+/g, '')
          .replace(/^[^A-Za-z0-9]+|[^A-Za-z0-9]+$/g, '');
        if (!flat || flat.length > 6) return [];
        var nums = extractNumbers(flat);
        if (nums.length !== 1) return [];
        var folded = flat.toUpperCase()
          .replace(/[IL|]/g, '1')
          .replace(/[OQ]/g, '0')
          .replace(/Z/g, '2')
          .replace(/S/g, '5');
        if (!/^C-?\\d{1,2}$/.test(folded)) return [];
        return nums;
      }"""

new_token_number = """      function tokenNumber(text) {
        var flat = normalizeDigits(String(text || ''))
          .replace(/\\s+/g, '')
          .replace(/^[^A-Za-z0-9]+|[^A-Za-z0-9]+$/g, '');
        if (!flat || flat.length > 6) return [];
        if (flat.toUpperCase() === 'SP') return ['SP'];
        var nums = extractNumbers(flat);
        if (nums.length !== 1) return [];
        var folded = flat.toUpperCase()
          .replace(/[IL|i]/gi, '1')
          .replace(/[OQ]/g, '0')
          .replace(/Z/g, '2')
          .replace(/S/g, '5')
          .replace(/A/g, '4');
        if (!/^C-?\\d{1,2}$/.test(folded)) return [];
        return nums;
      }"""

if old_token_number in html:
    html = html.replace(old_token_number, new_token_number)
    print("Updated tokenNumber().")
else:
    print("Warning: old tokenNumber() not matched exactly.")

# 5. Update numbersFromRecognition()
old_numbers_from_rec = "return kept.length === 1 ? kept : [];"
new_numbers_from_rec = "return kept.length ? kept : [];"

if old_numbers_from_rec in html:
    html = html.replace(old_numbers_from_rec, new_numbers_from_rec, 1)
    print("Updated numbersFromRecognition() kept length.")
else:
    print("Warning: old numbersFromRecognition kept length not matched.")

# 6. Update recognizeRaw() with flattenOcrData()
old_recognize_raw = """      function recognizeRaw(worker, img, pass, id) {
        if (id !== runId) return Promise.resolve(null);
        var canvas = paintVariant(img, pass.crop, pass.edge, pass.color);
        return worker.setParameters({
          tessedit_pageseg_mode: pass.psm,
          user_defined_dpi: '300'
        }).then(function () {
          if (id !== runId) return null;
          return worker.recognize(canvas, {}, { text: true, blocks: true });
        }).then(function (res) {
          if (!res || id !== runId) return null;
          return res.data || null;
        });
      }"""

new_recognize_raw = """      function flattenOcrData(data) {
        if (!data) return data;
        var words = [];
        var lines = [];
        if (Array.isArray(data.blocks)) {
          data.blocks.forEach(function (b) {
            if (Array.isArray(b.paragraphs)) {
              b.paragraphs.forEach(function (p) {
                if (Array.isArray(p.lines)) {
                  p.lines.forEach(function (l) {
                    lines.push(l);
                    if (Array.isArray(l.words)) {
                      l.words.forEach(function (w) {
                        words.push(w);
                      });
                    }
                  });
                }
              });
            }
          });
        }
        if (!data.lines || !data.lines.length) data.lines = lines;
        if (!data.words || !data.words.length) data.words = words;
        return data;
      }

      function recognizeRaw(worker, img, pass, id) {
        if (id !== runId) return Promise.resolve(null);
        var canvas = paintVariant(img, pass.crop, pass.edge, pass.color);
        return worker.setParameters({
          tessedit_pageseg_mode: pass.psm,
          user_defined_dpi: '300'
        }).then(function () {
          if (id !== runId) return null;
          return worker.recognize(canvas, {}, { text: true, blocks: true });
        }).then(function (res) {
          if (!res || id !== runId) return null;
          return flattenOcrData(res.data) || null;
        });
      }"""

if old_recognize_raw in html:
    html = html.replace(old_recognize_raw, new_recognize_raw)
    print("Updated recognizeRaw() with flattenOcrData().")
else:
    print("Warning: old recognizeRaw() not matched exactly.")

# 7. Insert PRECOMPUTED_CATALOG_FEATURES and update ensureCatalogFeatures()
old_ensure_cat = """      var catalogFeaturePromise = null;

      function localImageEntries() {
        var out = [];
        catalogCars().forEach(function (car) {
          var images = car.images || [];
          var url = '';
          for (var i = 0; i < images.length; i++) {
            var candidate = images[i] && images[i].url;
            if (!candidate) continue;
            if (candidate.indexOf('http:') === 0 || candidate.indexOf('https:') === 0 || candidate.indexOf('//') === 0) continue;
            url = candidate;
            break;
          }
          if (url) out.push({ car: car, url: url });
        });
        return out;
      }

      function loadHtmlImage(url) {
        return new Promise(function (resolve) {
          var img = new Image();
          img.onload = function () { resolve(img); };
          img.onerror = function () { resolve(null); };
          img.src = url;
        });
      }"""

new_ensure_cat = f"""      var PRECOMPUTED_CATALOG_FEATURES = {features_min_str};

      var catalogFeaturePromise = null;

      function localImageEntries() {{
        var out = [];
        catalogCars().forEach(function (car) {{
          var images = car.images || [];
          var url = '';
          for (var i = 0; i < images.length; i++) {{
            var candidate = images[i] && images[i].url;
            if (!candidate) continue;
            if (candidate.indexOf('http:') === 0 || candidate.indexOf('https:') === 0 || candidate.indexOf('//') === 0) continue;
            url = candidate;
            break;
          }}
          if (url) out.push({{ car: car, url: url }});
        }});
        return out;
      }}

      function loadHtmlImage(url) {{
        return new Promise(function (resolve) {{
          var img = new Image();
          img.onload = function () {{ resolve(img); }};
          img.onerror = function () {{ resolve(null); }};
          img.src = url;
        }});
      }}"""

if old_ensure_cat in html:
    html = html.replace(old_ensure_cat, new_ensure_cat)
    print("Inserted PRECOMPUTED_CATALOG_FEATURES.")
else:
    print("Warning: old_ensure_cat not matched exactly.")

old_ensure_fn = """      function ensureCatalogFeatures() {
        if (catalogFeaturePromise) return catalogFeaturePromise;
        catalogFeaturePromise = mapPool(localImageEntries(), 4, function (entry) {
          return loadHtmlImage(entry.url).then(function (img) {
            if (!img) return null;
            return { car: entry.car, sig: colorSignature(img), band: bandProfile(img) };
          });
        }).then(function (rows) {
          return rows.filter(Boolean);
        }).catch(function (err) {
          catalogFeaturePromise = null;
          throw err;
        });
        return catalogFeaturePromise;
      }"""

new_ensure_fn = """      function ensureCatalogFeatures() {
        if (catalogFeaturePromise) return catalogFeaturePromise;
        var cars = catalogCars();
        var rows = [];
        var featMap = (typeof PRECOMPUTED_CATALOG_FEATURES !== 'undefined' && PRECOMPUTED_CATALOG_FEATURES) || {};
        cars.forEach(function (car) {
          var feat = featMap[car.id] || (car.registryKey && featMap[car.registryKey]);
          if (feat && feat.sig) {
            rows.push({ car: car, sig: feat.sig, band: feat.band });
          }
        });
        if (rows.length > 0) {
          catalogFeaturePromise = Promise.resolve(rows);
          return catalogFeaturePromise;
        }
        catalogFeaturePromise = mapPool(localImageEntries(), 4, function (entry) {
          return loadHtmlImage(entry.url).then(function (img) {
            if (!img) return null;
            return { car: entry.car, sig: colorSignature(img), band: bandProfile(img) };
          });
        }).then(function (res) {
          return res.filter(Boolean);
        }).catch(function (err) {
          catalogFeaturePromise = null;
          throw err;
        });
        return catalogFeaturePromise;
      }"""

if old_ensure_fn in html:
    html = html.replace(old_ensure_fn, new_ensure_fn)
    print("Updated ensureCatalogFeatures() implementation.")
else:
    print("Warning: old ensureCatalogFeatures() not matched exactly.")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {INDEX_PATH} ({len(html)} bytes).")

with open(MIRROR_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {MIRROR_PATH} ({len(html)} bytes).")
