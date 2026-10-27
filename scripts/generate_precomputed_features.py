#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate precomputed visual features (colorSignature and bandProfile) for all cars in CARS_DATABASE.
Embedded directly into index.html so visual recognition runs instantly with zero network requests.
"""

import os
import re
import json
import numpy as np
from PIL import Image

def hue_of(r, g, b):
    r, g, b = float(r), float(g), float(b)
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx - mn
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    if diff <= 1e-6 or mx <= 1e-4:
        return 0.0, 0.0, luma
    if mx == r:
        hue = ((g - b) / diff) % 6.0
        if hue < 0:
            hue += 6.0
    elif mx == g:
        hue = (b - r) / diff + 2.0
    else:
        hue = (r - g) / diff + 4.0
    return hue / 6.0, diff / mx, luma

def smooth_hist(hist):
    out = [0.0] * 12
    for i in range(12):
        out[i] = 0.70 * hist[i] + 0.15 * hist[(i + 11) % 12] + 0.15 * hist[(i + 1) % 12]
    return [round(float(x), 4) for x in out]

def pack_hue(s, count):
    if count < 40:
        return None
    hist = [float(s[i]) / count for i in range(12)]
    smoothed = smooth_hist(hist)
    peak = 0
    for i in range(1, 12):
        if smoothed[i] > smoothed[peak]:
            peak = i
    return {
        'hist': smoothed,
        'sat': round(float(s[12]) / count, 4),
        'peak': peak,
        'pm': round(float(smoothed[peak]), 4)
    }

def color_signature(img_path):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert('RGB')
    nw, nh = im.size
    long_edge = max(nw, nh)
    scale = 180.0 / long_edge
    if scale > 1.0:
        scale = 1.0
    out_w = max(1, int(round(nw * scale)))
    out_h = max(1, int(round(nh * scale)))
    resized = im.resize((out_w, out_h), Image.Resampling.BILINEAR)
    arr = np.array(resized, dtype=np.float32) / 255.0

    open_sum = [0.0] * 13
    nored_sum = [0.0] * 13
    open_n = 0
    nored_n = 0
    red_count = 0
    yellow_count = 0
    dark_count = 0
    blue_count = 0
    total_non_bg = 0
    lower_start_y = int(out_h * 0.65)
    lower_non_bg = 0
    lower_whitewall = 0
    lower_red = 0

    for y in range(out_h):
        for x in range(out_w):
            r, g, b = arr[y, x]
            is_bg = (r > 0.95 and g > 0.95 and b > 0.95)
            if not is_bg:
                total_non_bg += 1

            hue, sat, luma = hue_of(r, g, b)

            if luma < 0.22 and sat < 0.40 and not is_bg:
                dark_count += 1
            if b > r + 0.08 and b > g + 0.03 and sat > 0.20 and 0.12 < luma < 0.88 and not is_bg:
                blue_count += 1
            is_red = (r > g + 0.15 and r > b + 0.15 and sat > 0.35 and r > 0.35)
            if is_red:
                red_count += 1
            is_yellow = (r > 0.45 and g > 0.38 and b < min(r, g) - 0.15 and sat > 0.35)
            if is_yellow:
                yellow_count += 1

            if y >= lower_start_y and not is_bg:
                lower_non_bg += 1
                if 0.55 < luma < 0.92 and sat < 0.20:
                    lower_whitewall += 1
                if is_red:
                    lower_red += 1

            if sat < 0.28 or luma <= 0.18 or luma >= 0.90:
                continue

            bin_idx = min(11, int(hue * 12))
            open_sum[bin_idx] += 1
            open_sum[12] += sat
            open_n += 1
            if is_red:
                continue
            nored_sum[bin_idx] += 1
            nored_sum[12] += sat
            nored_n += 1

    denom = max(1, total_non_bg)
    lower_denom = max(1, lower_non_bg)

    return {
        'open': pack_hue(open_sum, open_n),
        'nored': pack_hue(nored_sum, nored_n),
        'blueRatio': round(float(blue_count) / denom, 4),
        'redRatio': round(float(red_count) / denom, 4),
        'yellowRatio': round(float(yellow_count) / denom, 4),
        'darkRatio': round(float(dark_count) / denom, 4),
        'whitewallRatio': round(float(lower_whitewall) / lower_denom, 4),
        'lowerRedRatio': round(float(lower_red) / lower_denom, 4)
    }

def band_profile(img_path):
    if not os.path.exists(img_path):
        return None
    im = Image.open(img_path).convert('RGB')
    nw, nh = im.size
    scale = 180.0 / max(nw, nh)
    if scale > 1.0:
        scale = 1.0
    out_w = max(1, int(round(nw * scale)))
    out_h = max(1, int(round(nh * scale)))
    resized = im.resize((out_w, out_h), Image.Resampling.BILINEAR)
    arr = np.array(resized, dtype=np.float32) / 255.0

    min_x, min_y = out_w, out_h
    max_x, max_y = -1, -1
    count = 0

    for y in range(out_h):
        for x in range(out_w):
            r, g, b = arr[y, x]
            hue, sat, luma = hue_of(r, g, b)
            if sat < 0.28 or luma <= 0.20 or luma >= 0.88:
                continue
            count += 1
            if x < min_x: min_x = x
            if y < min_y: min_y = y
            if x > max_x: max_x = x
            if y > max_y: max_y = y

    if count < 20 or max_x < min_x:
        return None

    bh = max_y - min_y + 1
    bw = max_x - min_x + 1
    yA = max(0, min_y - int(bh * 0.15))
    yB = min(out_h, max_y + int(bh * 0.15) + 1)
    xA = max(0, min_x - int(bw * 0.10))
    xB = min(out_w, max_x + int(bw * 0.10) + 1)
    span = max(1, yB - yA)
    profile = []

    for band in range(3):
        ya = yA + int(band * span / 3)
        yb = yA + int((band + 1) * span / 3)
        bins = [0] * 6
        dark_n = 0
        area = max(1, (yb - ya) * (xB - xA))
        for y in range(ya, yb):
            for x in range(xA, xB):
                r, g, b = arr[y, x]
                hue, sat, luma = hue_of(r, g, b)
                dark = (luma < 0.32 and sat < 0.50)
                if dark:
                    dark_n += 1
                if not dark and sat >= 0.22 and 0.16 < luma < 0.92:
                    bins[min(5, int(hue * 6))] += 1
        peak = 0
        for b in range(1, 6):
            if bins[b] > bins[peak]:
                peak = b
        profile.extend([
            round(float(bins[peak]) / area, 4),
            round(float(dark_n) / area, 4),
            int(peak) if bins[peak] > 0 else -1
        ])
    return profile

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(root, 'index.html')
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract CARS_DATABASE
    lines = content.splitlines()
    chunk = '\n'.join(lines[1465:7291])
    start = chunk.find('[')
    json_part = chunk[start:].strip()
    if json_part.endswith(';'):
        json_part = json_part[:-1].strip()
    cars = json.loads(json_part)
    print(f"Loaded {len(cars)} cars from CARS_DATABASE.")

    features = {}
    missing = 0
    processed = 0

    for car in cars:
        car_id = car.get('id')
        reg_key = car.get('registryKey')
        imgs = car.get('images', [])
        local_url = None
        for im in imgs:
            url = im.get('url', '')
            if url and not url.startswith(('http:', 'https:', '//')):
                local_url = url
                break

        if not local_url:
            continue

        full_img_path = os.path.join(root, local_url)
        if not os.path.exists(full_img_path):
            print(f"Image not found: {full_img_path} for {car_id}")
            missing += 1
            continue

        sig = color_signature(full_img_path)
        band = band_profile(full_img_path)

        feat_entry = { 'sig': sig, 'band': band }
        features[car_id] = feat_entry
        if reg_key and reg_key != car_id:
            features[reg_key] = feat_entry
        processed += 1

    print(f"Successfully processed {processed} cars (features keys: {len(features)}, missing images: {missing}).")

    out_json = os.path.join(root, 'data', 'precomputed_catalog_features.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(features, f, ensure_ascii=False, indent=None, separators=(',', ':'))

    print(f"Wrote precomputed features to {out_json} (size: {os.path.getsize(out_json)} bytes)")

if __name__ == '__main__':
    main()
