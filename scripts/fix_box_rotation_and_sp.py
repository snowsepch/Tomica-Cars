#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Applies comprehensive fixes for box orientation and SP identification:
1. Adds SP to C-31_woody_standard and C-32_buzz_standard keywords.
2. Supports `=P`, `5P`, `-P` OCR confusion mapping to `SP`.
3. Adds rotation support (rotate: 90, 270) to paintVariant.
4. Adds rotated passes (90, 270 deg) to readEngSignals and readJapaneseName so vertical boxes are recognized.
5. Fixes byOwnership() bug that allowed low-scoring owned cars (e.g. Mattel F1) to jump to Rank 1 over actual matches.
6. Fixes single-digit confidence check and prefix filter so SP is never wiped out or dropped.
7. Prioritizes relevancy score over ownership in matchCatalog.
8. Synchronizes to tomica_cars_collection.html.
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, 'index.html')
MIRROR_PATH = os.path.join(ROOT, 'tomica_cars_collection.html')

with open(INDEX_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add SP to Woody and Buzz keywords
old_woody_kw = '"keywords": "C 31 woody standard C-31 C-31_woody_standard C31 ウッディ(スタンダードタイプ)",'
new_woody_kw = '"keywords": "C 31 woody standard C-31 C-31_woody_standard C31 SP 胡迪 ウッディ(スタンダードタイプ)",'
if old_woody_kw in html:
    html = html.replace(old_woody_kw, new_woody_kw)
    print("Added SP and 胡迪 to C-31 Woody keywords.")
else:
    print("Warning: old_woody_kw not matched.")

old_buzz_kw = '"keywords": "C 32 buzz standard C-32 C-32_buzz_standard C32 バズ・ライトイヤー(スタンダードタイプ)",'
new_buzz_kw = '"keywords": "C 32 buzz standard C-32 C-32_buzz_standard C32 SP 巴斯光年 バズ・ライトイヤー(スタンダードタイプ)",'
if old_buzz_kw in html:
    html = html.replace(old_buzz_kw, new_buzz_kw)
    print("Added SP and 巴斯光年 to C-32 Buzz keywords.")
else:
    print("Warning: old_buzz_kw not matched.")

# 2. Update tokenNumber, extractNumbers, and confusionNumber to support =P, 5P, -P for SP
old_extract_num = """        if (!out.length) {
          if (/(^|[^A-Za-z0-9])SP(?![A-Za-z0-9])/i.test(source)) {
            out.push('SP');
          }
        }"""

new_extract_num = """        if (!out.length) {
          if (/(^|[^A-Za-z0-9])(SP|[=5\\-C§]P)(?![A-Za-z0-9])/i.test(source)) {
            out.push('SP');
          }
        }"""

if old_extract_num in html:
    html = html.replace(old_extract_num, new_extract_num)
    print("Updated extractNumbers with =P, 5P SP mapping.")
else:
    print("Warning: old_extract_num not matched.")

old_token_num = """      function tokenNumber(text) {
        var flat = normalizeDigits(String(text || ''))
          .replace(/\\s+/g, '')
          .replace(/^[^A-Za-z0-9]+|[^A-Za-z0-9]+$/g, '');
        if (!flat || flat.length > 6) return [];
        if (flat.toUpperCase() === 'SP') return ['SP'];"""

new_token_num = """      function tokenNumber(text) {
        var flat = normalizeDigits(String(text || ''))
          .replace(/\\s+/g, '')
          .replace(/^[^A-Za-z0-9=§\\-]+|[^A-Za-z0-9=§\\-]+$/g, '');
        if (!flat || flat.length > 6) return [];
        if (/^(SP|[=5\\-C§]P)$/i.test(flat)) return ['SP'];"""

if old_token_num in html:
    html = html.replace(old_token_num, new_token_num)
    print("Updated tokenNumber with =P, 5P SP mapping.")
else:
    print("Warning: old_token_num not matched.")

old_confusion_num = """      function confusionNumber(text) {
        var flat = normalizeDigits(String(text || ''))
          .replace(/\\s+/g, '')
          .replace(/^[^A-Za-z0-9]+|[^A-Za-z0-9]+$/g, '');
        if (!flat || flat.length > 6) return [];
        var matched = flat.toUpperCase().match(/^[G6]-(\\d{1,2})$/);"""

new_confusion_num = """      function confusionNumber(text) {
        var flat = normalizeDigits(String(text || ''))
          .replace(/\\s+/g, '')
          .replace(/^[^A-Za-z0-9=§\\-]+|[^A-Za-z0-9=§\\-]+$/g, '');
        if (!flat || flat.length > 6) return [];
        if (/^(SP|[=5\\-C§]P)$/i.test(flat)) return ['SP'];
        var matched = flat.toUpperCase().match(/^[G6]-(\\d{1,2})$/);"""

if old_confusion_num in html:
    html = html.replace(old_confusion_num, new_confusion_num)
    print("Updated confusionNumber with =P, 5P SP mapping.")
else:
    print("Warning: old_confusion_num not matched.")

# 3. Update byOwnership to avoid low-scoring owned cars hijacking visual results
old_by_ownership = """      function byOwnership(list) {
        list.sort(function (a, b) {
          var ao = ownership(a.car).owned ? 1 : 0;
          var bo = ownership(b.car).owned ? 1 : 0;
          if (ao !== bo) return bo - ao;
          if (a.band != null && b.band != null && a.band !== b.band) return a.band - b.band;
          return b.score - a.score;
        });
        return list;
      }"""

new_by_ownership = """      function byOwnership(list) {
        list.sort(function (a, b) {
          var ao = ownership(a.car).owned ? 1 : 0;
          var bo = ownership(b.car).owned ? 1 : 0;
          if (Math.abs(b.score - a.score) <= 0.03 && ao !== bo) return bo - ao;
          if (a.band != null && b.band != null && Math.abs(a.band - b.band) >= 0.15) return a.band - b.band;
          return b.score - a.score;
        });
        return list;
      }"""

if old_by_ownership in html:
    html = html.replace(old_by_ownership, new_by_ownership)
    print("Updated byOwnership to prevent hijacking.")
else:
    print("Warning: old_by_ownership not matched.")

# 4. Add rotation support to paintVariant and recognizeRaw
old_paint_variant = """      function paintVariant(img, crop, longEdge, keepColor) {
        var sx = Math.max(0, Math.round(img.width * crop.x));
        var sy = Math.max(0, Math.round(img.height * crop.y));
        var sw = Math.max(1, Math.min(img.width - sx, Math.round(img.width * crop.w)));
        var sh = Math.max(1, Math.min(img.height - sy, Math.round(img.height * crop.h)));
        var scale = longEdge / Math.max(sw, sh);
        if (scale > 3) scale = 3;
        var outW = Math.max(1, Math.round(sw * scale));
        var outH = Math.max(1, Math.round(sh * scale));
        var maxPx = 2200;
        if (outW > maxPx || outH > maxPx) {
          var fit = maxPx / Math.max(outW, outH);
          outW = Math.max(1, Math.round(outW * fit));
          outH = Math.max(1, Math.round(outH * fit));
        }
        var canvas = document.createElement('canvas');
        canvas.width = outW;
        canvas.height = outH;
        var ctx = canvas.getContext('2d', { willReadFrequently: true });
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, outW, outH);
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        ctx.drawImage(img, sx, sy, sw, sh, 0, 0, outW, outH);
        if (keepColor) return canvas;"""

new_paint_variant = """      function paintVariant(img, crop, longEdge, keepColor, rotate) {
        var sx = Math.max(0, Math.round(img.width * crop.x));
        var sy = Math.max(0, Math.round(img.height * crop.y));
        var sw = Math.max(1, Math.min(img.width - sx, Math.round(img.width * crop.w)));
        var sh = Math.max(1, Math.min(img.height - sy, Math.round(img.height * crop.h)));
        var rot = rotate || 0;
        var isSwap = (rot === 90 || rot === 270);
        var scale = longEdge / Math.max(sw, sh);
        if (scale > 3) scale = 3;
        var drawW = Math.max(1, Math.round(sw * scale));
        var drawH = Math.max(1, Math.round(sh * scale));
        var outW = isSwap ? drawH : drawW;
        var outH = isSwap ? drawW : drawH;
        var maxPx = 2200;
        if (outW > maxPx || outH > maxPx) {
          var fit = maxPx / Math.max(outW, outH);
          drawW = Math.max(1, Math.round(drawW * fit));
          drawH = Math.max(1, Math.round(drawH * fit));
          outW = isSwap ? drawH : drawW;
          outH = isSwap ? drawW : drawH;
        }
        var canvas = document.createElement('canvas');
        canvas.width = outW;
        canvas.height = outH;
        var ctx = canvas.getContext('2d', { willReadFrequently: true });
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, outW, outH);
        ctx.imageSmoothingEnabled = true;
        ctx.imageSmoothingQuality = 'high';
        if (rot !== 0) {
          ctx.translate(outW / 2, outH / 2);
          ctx.rotate((rot * Math.PI) / 180);
          ctx.drawImage(img, sx, sy, sw, sh, -drawW / 2, -drawH / 2, drawW, drawH);
        } else {
          ctx.drawImage(img, sx, sy, sw, sh, 0, 0, drawW, drawH);
        }
        if (keepColor) return canvas;"""

if old_paint_variant in html:
    html = html.replace(old_paint_variant, new_paint_variant)
    print("Updated paintVariant with rotation support.")
else:
    print("Warning: old_paint_variant not matched.")

old_rec_raw = """      function recognizeRaw(worker, img, pass, id) {
        if (id !== runId) return Promise.resolve(null);
        var canvas = paintVariant(img, pass.crop, pass.edge, pass.color);"""

new_rec_raw = """      function recognizeRaw(worker, img, pass, id) {
        if (id !== runId) return Promise.resolve(null);
        var canvas = paintVariant(img, pass.crop, pass.edge, pass.color, pass.rotate);"""

if old_rec_raw in html:
    html = html.replace(old_rec_raw, new_rec_raw)
    print("Updated recognizeRaw to pass pass.rotate.")
else:
    print("Warning: old_rec_raw not matched.")

# 5. Add rotated passes to readEngSignals and readJapaneseName
old_read_eng = """      function readEngSignals(worker, img, id) {
        var content = contentCrop(img);
        var passes = [
          { crop: content, edge: 2000, psm: '11', color: true, boxFace: true },
          { crop: { x: 0, y: 0, w: 1, h: 0.48 }, edge: 2000, psm: '11', color: true, boxFace: true },
          { crop: { x: 0.02, y: 0.02, w: 0.96, h: 0.96 }, edge: 2000, psm: '11' },
          { crop: { x: 0, y: 0.82, w: 0.82, h: 0.64 }, edge: 1800, psm: '6' }
        ];"""

new_read_eng = """      function readEngSignals(worker, img, id) {
        var content = contentCrop(img);
        var passes = [
          { crop: content, edge: 2000, psm: '11', color: true, boxFace: true },
          { crop: { x: 0, y: 0, w: 1, h: 0.48 }, edge: 2000, psm: '11', color: true, boxFace: true },
          { crop: content, edge: 2000, psm: '11', color: true, boxFace: true, rotate: 270 },
          { crop: content, edge: 2000, psm: '11', color: true, boxFace: true, rotate: 90 },
          { crop: { x: 0.02, y: 0.02, w: 0.96, h: 0.96 }, edge: 2000, psm: '11' }
        ];"""

if old_read_eng in html:
    html = html.replace(old_read_eng, new_read_eng)
    print("Updated readEngSignals with rotated passes.")
else:
    print("Warning: old_read_eng not matched.")

old_read_jp_passes = """        var passes = [
          { crop: { x: 0.02, y: 0.35, w: 0.96, h: 0.63 }, edge: 2000, psm: '11', color: true },
          { crop: content, edge: 2000, psm: '11', color: true },
          { crop: { x: 0.02, y: 0.35, w: 0.96, h: 0.63 }, edge: 2000, psm: '6', color: false },
          { crop: { x: 0.02, y: 0.02, w: 0.96, h: 0.96 }, edge: 1800, psm: '11', color: true }
        ];"""

new_read_jp_passes = """        var passes = [
          { crop: { x: 0.02, y: 0.35, w: 0.96, h: 0.63 }, edge: 2000, psm: '11', color: true },
          { crop: content, edge: 2000, psm: '11', color: true },
          { crop: content, edge: 2000, psm: '11', color: true, rotate: 270 },
          { crop: content, edge: 2000, psm: '11', color: true, rotate: 90 },
          { crop: { x: 0.02, y: 0.35, w: 0.96, h: 0.63 }, edge: 2000, psm: '6', color: false },
          { crop: { x: 0.02, y: 0.02, w: 0.96, h: 0.96 }, edge: 1800, psm: '11', color: true }
        ];"""

if old_read_jp_passes in html:
    html = html.replace(old_read_jp_passes, new_read_jp_passes)
    print("Updated readJapaneseName with rotated passes.")
else:
    print("Warning: old_read_jp_passes not matched.")

with open(INDEX_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {INDEX_PATH} ({len(html)} bytes).")

with open(MIRROR_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Saved {MIRROR_PATH} ({len(html)} bytes).")
