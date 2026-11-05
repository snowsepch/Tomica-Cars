import os
import re

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(root, 'index.html')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        orig = f.read()

    # Extract WEEKLY_PICKS_DATA and CARS_DATABASE
    w_start = orig.find('const WEEKLY_PICKS_DATA')
    c_start = orig.find('const CARS_DATABASE')
    c_end = orig.find('];', c_start) + 2

    weekly_picks_str = orig[w_start:c_start].strip()
    weekly_picks_str = weekly_picks_str.replace('"site": "https://snowsepch.github.io/Tomica-Cars/",', '"site": "",')

    cars_database_str = orig[c_start:c_end].strip()

    # Extract Script #3 (Photo check logic)
    s3_start = orig.find('<script>', c_end)
    s3_end = orig.rfind('</script>') + len('</script>')
    s3_str = orig[s3_start:s3_end]

    head_and_styles = '''<!DOCTYPE html>
<html lang="zh-Hant-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Tomica 小車圖鑑</title>
  <meta name="description" content="Tomica 小車圖鑑・個人隨身典藏型錄">
  <meta property="og:title" content="Tomica 小車圖鑑">
  <meta property="og:description" content="Tomica 小車圖鑑・個人隨身典藏型錄">
  <meta property="og:type" content="website">
  <link rel="preload" href="fonts/jf-openhuninn.woff2" as="font" type="font/woff2" crossorigin>
  <style>
    @font-face {
      font-family: "jf-openhuninn";
      src: url("fonts/jf-openhuninn.woff2") format("woff2");
      font-weight: normal;
      font-style: normal;
      font-display: swap;
    }
    :root {
      --bg: #FBFAF7;
      --ink: #1C1B19;
      --mut: #8A8578;
      --line: rgba(28, 27, 25, 0.12);
      --grn: #1E6B4F;
      --red: #B3261E;
      --round: "jf-openhuninn", "Yuanti TC", "Hiragino Maru Gothic ProN", "PingFang TC", "Noto Sans TC", sans-serif;
      --serif: var(--round);
      --latin: var(--round);
      --sans: var(--round);
    }
    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }
    html {
      scroll-behavior: smooth;
      background-color: var(--bg);
    }
    body {
      font-variant-numeric: lining-nums;
      margin: 0;
      padding: 0;
      background-color: var(--bg);
      color: var(--ink);
      font-family: var(--sans);
      font-size: 15px;
      line-height: 1.75;
      letter-spacing: 0.015em;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    button, input, select, textarea {
      font-family: inherit;
    }
    button {
      font: inherit;
      color: inherit;
      background: none;
      border: 0;
      cursor: pointer;
      touch-action: manipulation;
    }
    a {
      color: inherit;
      text-decoration: none;
    }
    .cap {
      font-size: 11px;
      letter-spacing: 0.18em;
      color: var(--mut);
      text-transform: uppercase;
    }
    .lat {
      font-family: var(--latin);
    }
    .ser {
      font-family: var(--serif);
      font-weight: 500;
    }
    @keyframes up {
      from { opacity: 0; transform: translateY(12px); }
      to { opacity: 1; transform: none; }
    }
    @keyframes car {
      from { opacity: 0; transform: translateX(36px); }
      to { opacity: 1; transform: none; }
    }
    @keyframes stamp {
      0% { opacity: 0; transform: scale(1.8) rotate(-18deg); }
      60% { opacity: 1; transform: scale(0.94) rotate(-8deg); }
      100% { opacity: 1; transform: scale(1) rotate(-10deg); }
    }

    /* Cover (P.01) */
    .cover {
      height: 76svh;
      min-height: 560px;
      max-width: 600px;
      margin: 0 auto;
      padding: 22px 22px 0;
      display: flex;
      flex-direction: column;
      position: relative;
      overflow: hidden;
    }
    .cover .eb {
      display: flex;
      justify-content: space-between;
      animation: up 0.8s both;
    }
    .cover h1 {
      font-family: var(--serif);
      font-weight: 500;
      font-size: 38px;
      line-height: 1.25;
      margin: 20px 0 0;
      letter-spacing: 0.04em;
      animation: up 0.9s 0.1s both;
    }
    .cover h1 small {
      display: block;
      font-family: var(--latin);
      font-size: 16px;
      letter-spacing: 0.02em;
      color: var(--mut);
      margin-top: 6px;
    }
    .hero {
      flex: 1;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: flex-end;
      min-height: 0;
      cursor: pointer;
    }
    .hero:before {
      content: "";
      position: absolute;
      right: -30px;
      top: 50%;
      width: 78%;
      aspect-ratio: 1;
      transform: translateY(-50%);
      border-radius: 50%;
      background: #F2EEE5;
    }
    .hero img {
      position: relative;
      width: 88%;
      max-height: 100%;
      object-fit: contain;
      mix-blend-mode: multiply;
      animation: car 1.2s 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) both;
    }
    .hero .lab {
      position: absolute;
      left: 0;
      bottom: 8%;
      animation: up 1s 0.7s both;
    }
    .hero .lab b {
      display: block;
      font-family: var(--latin);
      font-weight: 500;
      font-size: 40px;
      line-height: 1;
      color: var(--red);
    }
    .hero .lab span {
      font-size: 12px;
      color: var(--mut);
    }
    .stat {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      border-top: 1px solid var(--line);
      padding: 10px 0;
      animation: up 1s 0.9s both;
    }
    .stat div {
      text-align: center;
    }
    .stat b {
      display: block;
      font-family: var(--latin);
      font-weight: 500;
      font-size: 26px;
      line-height: 1.1;
    }
    .stat b small {
      font-size: 13px;
      color: var(--mut);
    }
    .stat span {
      font-size: 11px;
      color: var(--mut);
      letter-spacing: 0.14em;
    }
    .peek {
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      min-height: 48px;
      font-size: 12px;
      color: var(--mut);
      letter-spacing: 0.1em;
    }
    .peek a {
      color: var(--ink);
      min-height: 44px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Sticky Toolbar */
    .tb {
      position: fixed;
      left: 0;
      right: 0;
      top: 0;
      height: 46px;
      z-index: 100;
      background: #FBFAF7;
      border-bottom: 1px solid var(--line);
      display: flex;
      align-items: center;
      padding: 0 10px 0 16px;
      gap: 4px;
      transform: translateY(-100%);
      transition: transform 0.3s;
    }
    .tb.show {
      transform: none;
    }
    .tb .tt {
      flex: 1;
      font-family: var(--serif);
      font-size: 14px;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .tb .tt i {
      font-style: normal;
      font-family: var(--latin);
      color: var(--mut);
      margin-left: 6px;
      font-size: 13px;
    }
    .tb button {
      min-width: 44px;
      height: 44px;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 8px;
      color: var(--ink);
    }

    /* Sections */
    .sec {
      max-width: 680px;
      margin: 0 auto;
      padding: 26px 20px 8px;
      scroll-margin-top: 52px;
    }
    .sh {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1px solid var(--ink);
      padding-bottom: 8px;
      margin-bottom: 14px;
    }
    .sh h2 {
      margin: 0;
      font-family: var(--serif);
      font-weight: 500;
      font-size: 22px;
      letter-spacing: 0.04em;
    }
    .seg {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      background: #F1EEE7;
      border-radius: 14px;
      padding: 4px;
      gap: 4px;
    }
    .seg button {
      min-height: 44px;
      border-radius: 11px;
      font-size: 15px;
      color: #6b665c;
      border: 0;
      margin: 0;
      font-weight: 500;
      transition: background 0.15s, color 0.15s;
    }
    .seg button.on {
      background: #fff;
      color: var(--ink);
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      font-weight: 700;
    }
    .sbox {
      display: flex;
      gap: 8px;
      margin-top: 16px;
      align-items: center;
    }
    .sfield {
      flex: 1;
      min-width: 0;
      display: flex;
      align-items: center;
      gap: 8px;
      height: 46px;
      border: 1px solid rgba(0,0,0,0.16);
      border-radius: 23px;
      background: #fff;
      padding: 0 14px;
    }
    .sfield svg {
      flex: none;
    }
    .sfield input {
      flex: 1;
      min-width: 0;
      border: 0;
      outline: none;
      background: none;
      font: inherit;
      font-size: 15px;
      color: var(--ink);
    }
    .camb {
      width: 46px;
      height: 46px;
      flex: none;
      border: 1px solid rgba(0,0,0,0.16);
      border-radius: 50%;
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    .flab {
      font-size: 11px;
      color: var(--mut);
      letter-spacing: 0.12em;
      margin: 18px 0 0;
    }
    .chips {
      display: flex;
      gap: 6px;
      overflow-x: auto;
      margin-top: 8px;
      padding: 2px 2px 4px;
      scrollbar-width: none;
      -webkit-overflow-scrolling: touch;
    }
    .chips::-webkit-scrollbar {
      display: none;
    }
    .chip {
      flex: none;
      min-height: 36px;
      padding: 0 13px;
      border: 1px solid var(--line);
      border-radius: 99px;
      font-size: 13px;
      color: #57534E;
      background: none;
      display: inline-flex;
      align-items: center;
      cursor: pointer;
      white-space: nowrap;
    }
    .chip i {
      font-style: normal;
      opacity: 0.6;
      margin-left: 4px;
      font-family: var(--latin);
    }
    .chip.on {
      background: #fff;
      border-color: var(--ink);
      color: var(--ink);
      font-weight: 600;
    }
    .chip.own {
      color: var(--grn);
    }
    .chip.own.on {
      background: #EEF6F1;
      border-color: var(--grn);
    }
    .chip.un {
      color: var(--red);
    }
    .chip.un.on {
      background: #FBEFEE;
      border-color: var(--red);
    }
    .pg {
      margin-top: 16px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
      font-size: 12px;
      color: var(--mut);
      line-height: 1.6;
    }
    .pg .bar {
      height: 1px;
      background: var(--line);
      margin: 8px 0;
    }
    .pg .bar i {
      display: block;
      height: 1px;
      background: var(--grn);
    }
    .pg b {
      color: var(--ink);
      font-weight: 600;
    }

    /* TOC (P.03) */
    .toc a {
      display: grid;
      grid-template-columns: 52px 1fr auto;
      align-items: center;
      min-height: 60px;
      border-bottom: 1px solid var(--line);
      gap: 8px;
    }
    .toc .no {
      font-family: var(--latin);
      font-size: 13px;
      color: var(--mut);
      letter-spacing: 0.08em;
    }
    .toc .nm {
      font-family: var(--serif);
      font-size: 16px;
      color: var(--ink);
    }
    .toc .en {
      display: block;
      font-size: 10px;
      letter-spacing: 0.16em;
      color: var(--mut);
      margin-top: 2px;
    }
    .toc .pr {
      text-align: right;
      font-family: var(--latin);
      font-size: 18px;
      color: var(--ink);
    }
    .toc .pr small {
      color: var(--mut);
      font-size: 12px;
    }
    .toc .mini {
      display: block;
      width: 64px;
      height: 1px;
      background: var(--line);
      margin-top: 5px;
      margin-left: auto;
    }
    .toc .mini i {
      display: block;
      height: 1px;
      background: var(--grn);
    }

    /* Chapter Spread */
    .ch {
      max-width: 680px;
      margin: 0 auto;
      padding: 36px 0 10px;
      scroll-margin-top: 52px;
    }
    @media (min-width: 768px) {
      .sec, .ch {
        max-width: 1080px;
      }
    }
    .sp {
      padding: 0 20px;
      display: grid;
      grid-template-columns: 1fr;
      position: relative;
      overflow: hidden;
    }
    .sp .num {
      display: flex;
      justify-content: space-between;
    }
    .sp h3 {
      font-family: var(--serif);
      font-weight: 500;
      font-size: 28px;
      line-height: 1.25;
      margin: 14px 0 4px;
      letter-spacing: 0.04em;
    }
    .sp .en {
      font-family: var(--latin);
      color: var(--mut);
      font-size: 16px;
    }
    .fig {
      margin: 18px -20px 0 32px;
      background: #F2EEE5;
      aspect-ratio: 4/3;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      cursor: pointer;
      border-radius: 4px;
    }
    @media (min-width: 768px) {
      .fig {
        margin: 18px 0 0 auto;
        max-width: 520px;
      }
    }
    .fig img {
      width: 86%;
      max-height: 84%;
      object-fit: contain;
      mix-blend-mode: multiply;
    }
    .figcap {
      display: flex;
      justify-content: space-between;
      margin: 8px 0 0 32px;
      font-size: 11px;
      color: var(--mut);
    }
    @media (min-width: 768px) {
      .figcap {
        margin: 8px 0 0 auto;
        max-width: 520px;
      }
    }
    .quote {
      margin: 18px 40px 0 0;
      font-family: var(--serif);
      font-size: 14px;
      line-height: 1.8;
      color: #3f3c37;
      border-left: 1px solid var(--ink);
      padding-left: 12px;
    }
    .chp {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin: 18px 20px 12px;
      font-size: 12px;
      color: var(--mut);
      border-top: 1px solid var(--line);
      padding-top: 8px;
    }
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 22px 12px;
      padding: 0 20px;
    }
    @media (min-width: 768px) {
      .grid {
        grid-template-columns: repeat(4, 1fr);
        gap: 24px 16px;
        padding: 0 20px;
      }
    }

    /* Cards */
    .card {
      cursor: pointer;
      min-height: 44px;
      display: flex;
      flex-direction: column;
    }
    .card .fr {
      position: relative;
      aspect-ratio: 1/1;
      background: #fff;
      border-radius: 3px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .card .fr img {
      width: 84%;
      max-height: 70%;
      object-fit: contain;
      margin-top: 10px;
    }
    .card.o .fr {
      box-shadow: 0 0 0 1px var(--grn);
    }
    .card.u .fr {
      box-shadow: 0 0 0 1px rgba(0,0,0,0.1);
    }
    .card .id {
      position: absolute;
      top: 8px;
      left: 9px;
      font-family: var(--latin);
      font-size: 14px;
      color: #57534E;
      max-width: 60%;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }
    .seal {
      position: absolute;
      top: 6px;
      right: 6px;
      width: 28px;
      height: 28px;
    }
    .tag {
      position: absolute;
      top: 8px;
      right: 8px;
      font-size: 10px;
      letter-spacing: 0.08em;
      color: var(--red);
      border: 1px solid rgba(179,38,30,0.55);
      border-radius: 99px;
      padding: 1px 7px;
      background: #fff;
    }
    .card .nm {
      font-family: var(--serif);
      font-size: 15px;
      line-height: 1.4;
      margin-top: 8px;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      color: var(--ink);
    }
    .card .m {
      display: flex;
      justify-content: space-between;
      gap: 4px;
      font-size: 11px;
      color: #A8A29E;
      margin-top: 3px;
    }
    .card.o .s {
      color: var(--grn);
    }
    .card.u .s {
      color: var(--red);
    }
    .dupt {
      color: #A8A29E;
      font-size: 10.5px;
    }
    .empty {
      padding: 30px 20px;
      color: var(--mut);
      font-size: 14px;
      text-align: center;
    }
    .foot {
      text-align: center;
      padding: 40px 20px 60px;
      font-size: 11px;
      color: var(--mut);
      letter-spacing: 0.2em;
    }

    /* Detail Modal */
    .dt {
      position: fixed;
      inset: 0;
      z-index: 1000;
      background: var(--bg);
      transform: translateY(100%);
      transition: transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
    }
    .dt.open {
      transform: none;
    }
    .dt .bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      height: 52px;
      padding: 0 10px 0 20px;
      border-bottom: 1px solid var(--line);
      position: sticky;
      top: 0;
      background: var(--bg);
      z-index: 2;
    }
    .dt .bar button {
      width: 44px;
      height: 44px;
      font-size: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .dt .stg {
      position: relative;
      margin: 18px 20px 0;
      max-width: 500px;
      width: calc(100% - 40px);
      margin-left: auto;
      margin-right: auto;
      aspect-ratio: 4/3.2;
      background: #fff;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .dt.o .stg {
      box-shadow: 0 0 0 1px var(--grn);
    }
    .dt.u .stg {
      box-shadow: 0 0 0 1px rgba(0,0,0,0.1);
    }
    .dt .stg img {
      width: 86%;
      max-height: 80%;
      object-fit: contain;
    }
    .bigseal {
      position: absolute;
      right: 12px;
      bottom: 12px;
      width: 76px;
      height: 76px;
    }
    .dt.o .bigseal {
      animation: stamp 0.6s 0.25s both;
    }
    .dt .body {
      padding: 18px 20px 40px;
      max-width: 500px;
      width: 100%;
      margin: 0 auto;
    }
    .dt h4 {
      font-family: var(--serif);
      font-weight: 500;
      font-size: 22px;
      line-height: 1.35;
      margin: 6px 0 2px;
    }
    .dt .jp {
      font-size: 13px;
      color: var(--mut);
    }
    .dl {
      margin-top: 16px;
      border-top: 1px solid var(--line);
    }
    .dl div {
      display: flex;
      justify-content: space-between;
      min-height: 44px;
      align-items: center;
      border-bottom: 1px solid var(--line);
      font-size: 14px;
    }
    .dl dt {
      color: var(--mut);
      font-size: 12px;
      letter-spacing: 0.1em;
    }
    .pn {
      display: flex;
      gap: 10px;
      margin-top: 24px;
    }
    .pn button {
      flex: 1;
      height: 48px;
      border: 1px solid var(--line);
      border-radius: 99px;
      font-size: 14px;
      background: #fff;
      font-weight: 500;
    }

    /* Weekly Picks */
    .wk {
      display: grid;
      grid-template-columns: 96px 1fr;
      gap: 14px;
      padding: 14px 0;
      border-bottom: 1px solid var(--line);
      align-items: center;
    }
    .wk .fr {
      aspect-ratio: 1;
      background: #fff;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 0 1px var(--line);
      overflow: hidden;
    }
    .wk .fr img {
      width: 86%;
      max-height: 80%;
      object-fit: contain;
    }
    .wk h5 {
      margin: 3px 0 4px;
      font-size: 15px;
      font-weight: 500;
      line-height: 1.4;
    }
    .wk .m {
      font-size: 12px;
      color: var(--mut);
      line-height: 1.6;
    }
    .wk a {
      color: var(--grn);
      font-size: 12px;
      font-weight: 500;
      display: inline-block;
      margin-top: 4px;
    }

    /* Photo Check Sheet & AI Modal */
    .photo-check-overlay {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      height: 100dvh;
      z-index: 1200;
      display: flex;
      align-items: flex-end;
      justify-content: center;
      background: rgba(9, 9, 11, 0.65);
      padding: 0;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .photo-check-overlay[hidden] {
      display: none;
    }
    .photo-check-overlay.active {
      opacity: 1;
      pointer-events: auto;
    }
    @media (min-width: 640px) {
      .photo-check-overlay {
        align-items: center;
        padding: 1.25rem;
      }
    }
    .photo-check-sheet {
      background: #FBFAF7;
      color: var(--ink);
      border: 1px solid var(--line);
      border-radius: 24px 24px 0 0;
      width: 100%;
      max-width: 480px;
      max-height: min(92dvh, 760px);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.16);
      transform: translateY(100%);
      transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      outline: none;
    }
    @media (min-width: 640px) {
      .photo-check-sheet {
        border-radius: 20px;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.2);
        transform: translateY(16px) scale(0.98);
      }
    }
    .photo-check-overlay.active .photo-check-sheet {
      transform: translateY(0);
    }
    @media (min-width: 640px) {
      .photo-check-overlay.active .photo-check-sheet {
        transform: translateY(0) scale(1);
      }
    }
    .photo-check-handle {
      width: 3rem;
      height: 0.35rem;
      border-radius: 999px;
      background: rgba(161, 161, 170, 0.6);
      margin: 0.7rem auto 0;
      flex-shrink: 0;
    }
    @media (min-width: 640px) {
      .photo-check-handle { display: none; }
    }
    .photo-check-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 0.75rem;
      padding: 0.85rem 1.15rem 0.35rem;
      flex-shrink: 0;
    }
    .photo-check-head h2 {
      margin: 0;
      font-size: 1.1rem;
      line-height: 1.4;
      font-weight: 700;
      font-family: var(--serif);
    }
    .photo-check-head p {
      margin: 0.15rem 0 0;
      font-size: 0.75rem;
      line-height: 1.55;
      color: var(--mut);
    }
    .photo-check-close {
      width: 2rem;
      height: 2rem;
      border-radius: 999px;
      border: 0;
      background: #f4f4f5;
      color: var(--ink);
      font-weight: 700;
      cursor: pointer;
      flex-shrink: 0;
    }
    .photo-check-body {
      flex: 1 1 auto;
      min-height: 0;
      overflow-y: auto;
      overscroll-behavior: contain;
      -webkit-overflow-scrolling: touch;
      padding: 0.35rem 1.15rem 0.75rem;
    }
    .photo-check-tip {
      margin: 0 0 0.65rem;
      font-size: 0.78rem;
      line-height: 1.65;
      color: var(--mut);
    }
    .photo-check-preview-wrap {
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 12px;
      min-height: 140px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }
    .photo-check-preview-wrap img {
      display: block;
      width: 100%;
      max-height: min(32vh, 220px);
      object-fit: contain;
    }
    .photo-check-query {
      margin-top: 0.75rem;
    }
    .photo-check-query-label {
      margin: 0 0 0.35rem;
      font-size: 0.7rem;
      font-weight: 700;
      color: var(--mut);
    }
    .photo-check-query-row {
      display: flex;
      gap: 0.4rem;
    }
    .photo-check-query-row input {
      flex: 1;
      min-width: 0;
      min-height: 44px;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 0.4rem 0.65rem;
      font: inherit;
      font-size: 0.88rem;
      background: #ffffff;
      color: var(--ink);
    }
    .photo-check-query-row button {
      min-height: 44px;
      padding: 0 0.85rem;
      border-radius: 10px;
      border: 1px solid var(--ink);
      background: var(--ink);
      color: #ffffff;
      font-weight: 700;
      font-size: 0.82rem;
      white-space: nowrap;
      cursor: pointer;
    }
    .photo-check-heard {
      margin: 0.55rem 0 0;
      font-size: 0.75rem;
      line-height: 1.55;
      color: var(--mut);
      user-select: text;
      -webkit-user-select: text;
    }
    .photo-check-results {
      margin-top: 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .photo-check-result {
      width: 100%;
      text-align: left;
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 0.7rem 0.75rem;
      cursor: pointer;
      color: var(--ink);
      font: inherit;
    }
    .photo-check-result.is-selected {
      border-color: var(--ink);
    }
    .photo-check-result-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
    }
    .compendium-badge {
      font-family: var(--latin);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      background: #f4f4f5;
      color: var(--ink);
    }
    .photo-check-result-name {
      margin: 0.35rem 0 0;
      font-size: 0.92rem;
      font-weight: 700;
      line-height: 1.45;
    }
    .photo-check-result-jp {
      margin: 0.15rem 0 0;
      font-size: 0.78rem;
      line-height: 1.5;
      color: var(--mut);
    }
    .photo-check-result-counts {
      margin: 0.25rem 0 0;
      font-size: 0.78rem;
      line-height: 1.45;
      color: var(--ink);
    }
    .photo-check-owned { color: var(--grn); font-weight: 700; font-size: 0.78rem; }
    .photo-check-unowned { color: var(--mut); font-weight: 700; font-size: 0.78rem; }
    .photo-check-footer {
      padding: 0.65rem 1.15rem 0.9rem;
      background: #FBFAF7;
      border-top: 1px solid var(--line);
      flex-shrink: 0;
    }
    .photo-check-status {
      font-size: 0.78rem;
      color: var(--mut);
      margin: 0 0 0.5rem;
    }
    .photo-check-secondary {
      width: 100%;
      min-height: 44px;
      border-radius: 10px;
      border: 1px solid var(--line);
      background: #ffffff;
      color: var(--ink);
      font-weight: 700;
      font-size: 0.85rem;
      margin-bottom: 0.4rem;
      cursor: pointer;
    }
    .photo-check-row {
      display: flex;
      justify-content: space-between;
      gap: 0.5rem;
    }
    .photo-check-textbtn {
      background: transparent;
      border: 0;
      padding: 0.35rem 0.25rem;
      min-height: 44px;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--mut);
      cursor: pointer;
    }
    .photo-check-file {
      position: fixed;
      left: -9999px;
      top: 0;
      width: 1px;
      height: 1px;
      opacity: 0;
      overflow: hidden;
    }
    .ai-mode-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      padding: 0.55rem 0.75rem;
      border-radius: 10px;
      font-size: 0.78rem;
      margin-bottom: 0.65rem;
      border: 1px solid var(--line);
      background: #ffffff;
    }
    .ai-mode-bar.is-active {
      background: #EEF6F1;
      border-color: var(--grn);
      color: var(--grn);
    }
    .ai-mode-bar.is-idle {
      background: #f4f4f5;
      color: #52525B;
    }
    .ai-config-btn {
      padding: 0.25rem 0.65rem;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #ffffff;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
    }
    #aiKeyModalOverlay {
      position: fixed;
      inset: 0;
      z-index: 1300;
      background: rgba(9, 9, 11, 0.65);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }
    #aiKeyModalOverlay[hidden] {
      display: none;
    }
    .ai-key-card {
      background: #ffffff;
      border-radius: 18px;
      max-width: 440px;
      width: 100%;
      padding: 1.25rem;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.2);
      border: 1px solid var(--line);
      color: var(--ink);
    }

    @media (prefers-reduced-motion: reduce) {
      *, *:before, *:after {
        animation: none !important;
        transition: none !important;
      }
      html {
        scroll-behavior: auto !important;
      }
    }
  </style>
</head>
<body>
  <!-- 頂部吸頂工具列 (捲動過封面約 80% 後浮現) -->
  <header class="tb" id="tb">
    <div class="tt">Tomica 小車圖鑑<i id="tbp">90/187</i></div>
    <button id="tbSearchBtn" onclick="goSearch()" aria-label="搜尋">🔍 搜尋</button>
    <button id="tbFilterBtn" onclick="goSearch(1)" aria-label="篩選">篩選</button>
    <button id="tbCamBtn" aria-label="拍照對照" onclick="document.getElementById('photoCheckOpenBtn').click()">📷</button>
  </header>

  <!-- P.01 封面 (約 76svh) -->
  <section class="cover" id="cover">
    <div class="eb">
      <span class="cap">TOMICA FIELD GUIDE</span>
      <span class="cap">VOL. 2026・P.01</span>
    </div>
    <h1>Tomica<br>小車圖鑑<small>A catalogue of little cars</small></h1>
    <div class="hero" id="heroCard" onclick="openCarDetail(HERO.id)" title="查看主角車小檔案">
      <img id="heroImg" alt="閃電麥坤（標準型）">
      <div class="lab">
        <b id="heroNo">No.C-1</b>
        <span id="heroNm">閃電麥坤（標準型）</span>
      </div>
    </div>
    <div class="stat">
      <div><b id="s1">90<small>/187</small></b><span>已入手</span></div>
      <div><b id="s2">67</b><span>盒裝</span></div>
      <div><b id="s3">51</b><span>散車</span></div>
    </div>
    <div class="peek">
      <a href="#toc">目錄 CONTENTS ↓</a>
      <a href="#findSec">🔍 搜尋・篩選</a>
    </div>
  </section>

  <!-- P.02 查詢區 -->
  <section class="sec" id="findSec">
    <div class="sh">
      <h2>查詢</h2>
      <span class="cap">P.02 INDEX</span>
    </div>
    <nav class="seg" id="seg">
      <button id="mainTabOfficial" data-t="all" class="on">全部車款</button>
      <button id="mainTabOwned" data-t="mine">我的收藏</button>
      <button id="mainTabWeekly" data-t="week">每週新品</button>
    </nav>
    <div class="sbox">
      <label class="sfield">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8A8578" stroke-width="2">
          <circle cx="11" cy="11" r="7"/>
          <path d="m20 20-3.5-3.5"/>
        </svg>
        <input id="searchInput" type="search" placeholder="搜尋編號或車名" aria-label="搜尋編號或車名">
      </label>
      <button class="camb" id="photoCheckOpenBtn" aria-label="拍照對照" title="拍照對照">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1C1B19" stroke-width="1.6">
          <path d="M4 8h3l2-3h6l2 3h3v11H4z"/>
          <circle cx="12" cy="13" r="3.5"/>
        </svg>
      </button>
      <button id="photoCheckLibraryBtn" style="display:none" aria-label="從相簿選">相簿</button>
    </div>
    <div class="flab" id="flab1">購入狀態</div>
    <div class="chips" id="sf"></div>
    <div class="flab" id="flab2">系列</div>
    <div class="chips" id="cf"></div>
    <div class="pg" id="pg"></div>
  </section>

  <!-- P.03 目錄區 -->
  <section class="sec" id="toc">
    <div class="sh">
      <h2>目錄</h2>
      <span class="cap">P.03 Contents</span>
    </div>
    <div class="toc" id="tocL"></div>
  </section>

  <!-- 主車款清單 (依章節陳列) -->
  <main id="chs"></main>

  <!-- 每週新品區 -->
  <section class="sec" id="weekSec" hidden>
    <div class="sh">
      <h2>每週新品</h2>
      <span class="cap">WEEKLY PICKS</span>
    </div>
    <div id="wkL"></div>
  </section>

  <div class="foot">TOMICA FIELD GUIDE・END</div>

  <!-- 全螢幕車款小檔案彈窗 -->
  <div class="dt" id="dt" aria-modal="true" role="dialog" aria-label="車款小檔案">
    <div class="bar">
      <span class="cap" id="dPos"></span>
      <button onclick="closeCarDetail()" aria-label="關閉">✕</button>
    </div>
    <div class="stg" id="dStg"></div>
    <div class="body" id="dBody"></div>
  </div>

  <!-- 拍照對照輸入與面板 (保有完整 OCR / Tesseract / 散車比對 / Gemini 邏輯) -->
  <div id="photoCheckInputs">
    <input id="photoCheckCameraInput" class="photo-check-file" type="file" accept="image/*" capture="environment" tabindex="-1" aria-hidden="true">
    <input id="photoCheckLibraryInput" class="photo-check-file" type="file" accept="image/*" tabindex="-1" aria-hidden="true">
  </div>

  <div id="photoCheckOverlay" class="photo-check-overlay" hidden>
    <div
      id="photoCheckSheet"
      class="photo-check-sheet"
      role="dialog"
      aria-modal="true"
      aria-labelledby="photoCheckTitle"
      aria-describedby="photoCheckTip"
      tabindex="-1"
    >
      <div class="photo-check-handle" aria-hidden="true"></div>
      <div class="photo-check-head">
        <div>
          <h2 id="photoCheckTitle">拍照對照</h2>
          <p>Cars、迪士尼、Dream，整本圖鑑都能對</p>
        </div>
        <button id="photoCheckCloseBtn" type="button" class="photo-check-close" aria-label="關閉拍照對照">✕</button>
      </div>

      <div class="photo-check-body">
        <!-- Gemini AI 模式狀態與快速設定列 -->
        <div id="aiModeBar" class="ai-mode-bar is-idle">
          <div style="display:flex;align-items:center;gap:6px;min-width:0">
            <span style="font-size:14px;flex-shrink:0">✨</span>
            <span id="aiModeStatusText" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:500">離線比對中（點右側開啟 AI 99% 精準辨識）</span>
          </div>
          <button id="aiConfigBtn" type="button" class="ai-config-btn" style="flex-shrink:0">免費開啟</button>
        </div>
        <p id="photoCheckTip" class="photo-check-tip">整本口袋圖鑑都會對，包含 Cars、迪士尼和 Dream。先讀編號或品名，讀不到再看外形與配色。預設不上傳照片，僅在手機本機比對；開啟 AI 模式才會將照片傳送至 Google API 辨識。</p>
        <div class="photo-check-preview-wrap">
          <img id="photoCheckPreview" alt="">
        </div>
        <p id="photoCheckOcrNote" class="photo-check-heard" role="status" aria-live="polite"></p>
        <form id="photoCheckQueryForm" class="photo-check-query" autocomplete="off">
          <label id="photoCheckQueryLabel" class="photo-check-query-label" for="photoCheckQuery">改查編號或品名</label>
          <div class="photo-check-query-row">
            <input id="photoCheckQuery" type="text" inputmode="text" enterkeyhint="search" placeholder="例如 C-14、No.179、メーター" aria-describedby="photoCheckTip">
            <button type="submit">對照圖鑑</button>
          </div>
        </form>
        <div id="photoCheckResults" class="photo-check-results"></div>
      </div>

      <div class="photo-check-footer">
        <p id="photoCheckStatus" class="photo-check-status" role="status" aria-live="polite"></p>
        <button id="photoCheckShareBtn" type="button" class="photo-check-secondary" hidden>系統分享</button>
        <button id="photoCheckSaveBtn" type="button" class="photo-check-secondary">儲存照片</button>
        <div class="photo-check-row">
          <button id="photoCheckRetakeBtn" type="button" class="photo-check-textbtn">重拍</button>
          <button id="photoCheckSheetLibraryBtn" type="button" class="photo-check-textbtn">從相簿選</button>
          <button id="photoCheckDismissBtn" type="button" class="photo-check-textbtn">關閉</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Gemini AI 金鑰設定視窗 -->
  <div id="aiKeyModalOverlay" hidden>
    <div
      id="aiKeyModalCard"
      class="ai-key-card"
      role="dialog"
      aria-modal="true"
      aria-labelledby="aiKeyModalTitle"
    >
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
        <div style="display:flex;align-items:center;gap:8px">
          <span style="font-size:20px">✨</span>
          <h3 id="aiKeyModalTitle" style="font-size:16px;font-weight:700;margin:0;letter-spacing:0.02em">Google Gemini 視覺 AI 設定</h3>
        </div>
        <button id="aiKeyModalCloseBtn" type="button" style="width:32px;height:32px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#f4f4f5;border:0;cursor:pointer" aria-label="關閉設定">✕</button>
      </div>

      <div style="font-size:13px;color:#52525B;line-height:1.6;margin-bottom:14px">
        本功能完全免費且安全，API Key 僅保存在您的手機瀏覽器中，不經過任何第三方伺服器。<br>
        前往 <a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener noreferrer" style="color:#1E6B4F;font-weight:700;text-decoration:underline">Google AI Studio</a> 即可一鍵免費獲取。
      </div>

      <div style="margin-bottom:14px">
        <label for="geminiApiKeyInput" style="display:block;font-size:12px;font-weight:700;color:#18181B;margin-bottom:6px">輸入 Gemini API 金鑰 (Key)</label>
        <div style="position:relative">
          <input
            id="geminiApiKeyInput"
            type="password"
            placeholder="AIzaSy..."
            autocomplete="off"
            spellcheck="false"
            style="width:100%;height:44px;padding:0 38px 0 12px;border:1px solid #D8D8D4;border-radius:10px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;outline:none"
          >
          <button id="toggleApiKeyVisibilityBtn" type="button" style="position:absolute;right:10px;top:50%;transform:translateY(-50%);border:0;background:none;cursor:pointer;font-size:14px" aria-label="切換密碼顯示">👁️</button>
        </div>
      </div>

      <div style="display:flex;gap:8px">
        <button id="saveApiKeyBtn" type="button" style="flex:1;height:44px;background:#1C1B19;color:#fff;border-radius:10px;font-size:14px;font-weight:700;border:0;cursor:pointer">儲存並啟用 AI 視覺</button>
        <button id="clearApiKeyBtn" type="button" style="height:44px;padding:0 14px;background:#f4f4f5;color:#52525B;border-radius:10px;font-size:13px;border:1px solid #D8D8D4;cursor:pointer">清除</button>
      </div>
    </div>
  </div>

  <script>
'''

    script_2_logic = '''
// ==========================================
// K3 粉圓雜誌版 核心渲染與互動邏輯
// ==========================================
const isOwned = c => c.owned !== false && ((c.boxed || 0) + (c.loose || 0)) > 0;
const D = CARS_DATABASE;
const OWN = D.filter(isOwned);
const title = c => (c.name && c.name !== '官方未載明' && c.name !== c.jpName) ? c.name : (c.jpName || c.name || c.id);
const has = v => v != null && v !== '' && v !== '官方未載明';
const getCarImg = c => c.img || (c.images && c.images.length > 0 ? c.images[0].url : '');
const im = c => {
  const url = getCarImg(c);
  return url ? `<img src="${url}" loading="lazy" alt="${title(c)}">` : `<span class="noimg" style="font-size:12px;color:#a8a29e">暫無官方圖</span>`;
};

const CH = [
  ['cars_tomica', 'Cars 汽車總動員', 'Cars・Tomica', '從 Radiator Springs 出發，每一台都是 66 號公路上的老朋友。'],
  ['cars_non_tomica', 'Cars 非 Tomica 系列', 'Cars・Other Makers', '不是 Tomica，卻同樣屬於這座小鎮的收藏。'],
  ['other_disney', '迪士尼與夢幻系列', 'Disney & Dreams', '把喜歡的角色，縮成掌心大小。'],
  ['toystory', '玩具總動員', 'Toy Story', '到無限，再超越——裝進小小的車殼裡。'],
  ['general', '一般車輛與其他', 'General & Others', '街上看得見的車，也值得一頁。']
].filter(c => D.some(x => x.category === c[0]));

const TB = OWN.reduce((a, c) => a + (c.boxed || 0), 0);
const TL = OWN.reduce((a, c) => a + (c.loose || 0), 0);
const HERO = D.find(c => c.id === 'C-01') || OWN[0];

if (HERO) {
  const hImg = document.getElementById('heroImg');
  const hNo = document.getElementById('heroNo');
  const hNm = document.getElementById('heroNm');
  if (hImg) {
    const u = getCarImg(HERO);
    if (u) hImg.src = u;
    hImg.alt = title(HERO);
  }
  if (hNo) hNo.textContent = 'No.' + (HERO.displayNumber || HERO.id);
  if (hNm) hNm.textContent = title(HERO);
}

const s1 = document.getElementById('s1');
const s2 = document.getElementById('s2');
const s3 = document.getElementById('s3');
const tbp = document.getElementById('tbp');
const pg = document.getElementById('pg');
const tocL = document.getElementById('tocL');
const sf = document.getElementById('sf');
const cf = document.getElementById('cf');
const seg = document.getElementById('seg');
const q = document.getElementById('searchInput');
const tb = document.getElementById('tb');
const chs = document.getElementById('chs');
const weekSec = document.getElementById('weekSec');
const wkL = document.getElementById('wkL');
const tocSec = document.getElementById('toc');
const findSec = document.getElementById('findSec');
const coverSec = document.getElementById('cover');

if (s1) s1.innerHTML = `${OWN.length}<small>/${D.length}</small>`;
if (s2) s2.textContent = TB;
if (s3) s3.textContent = TL;
if (tbp) tbp.textContent = `${OWN.length}/${D.length}`;

if (pg) {
  const pct = Math.round((OWN.length / D.length) * 100);
  pg.innerHTML = `總收藏進度 <b>${OWN.length} / ${D.length}</b>・${pct}%<div class="bar"><i style="width:${(OWN.length / D.length) * 100}%"></i></div>盒裝 ${TB} 台・散車 ${TL} 台・待入手 ${D.length - OWN.length} 款`;
}

const pad = n => String(n).padStart(2, '0');

if (tocL) {
  tocL.innerHTML = CH.map((c, i) => {
    const L = D.filter(x => x.category === c[0]);
    const o = L.filter(isOwned).length;
    const pct = L.length ? (o / L.length) * 100 : 0;
    return `
      <a href="#ch-${c[0]}">
        <span class="no">CH.${pad(i + 1)}</span>
        <span>
          <span class="nm">${c[1]}</span>
          <span class="en">${c[2]}</span>
        </span>
        <span class="pr">
          ${o}<small>/${L.length}</small>
          <span class="mini"><i style="width:${pct}%"></i></span>
        </span>
      </a>
    `;
  }).join('');
}

const st = { s: 'all', c: 'all', q: '', t: 'all' };

if (sf) {
  sf.innerHTML = [
    ['all', '全部', D.length],
    ['own', '已入手', OWN.length],
    ['un', '待入手', D.length - OWN.length]
  ].map(s => `<button class="chip ${s[0]}" data-v="${s[0]}">${s[1]}<i>${s[2]}</i></button>`).join('');
}

if (cf) {
  cf.innerHTML = [
    ['all', '全部系列'],
    ...CH.map(c => [c[0], c[1]])
  ].map(s => `<button class="chip" data-v="${s[0]}">${s[1]}</button>`).join('');
}

if (sf) {
  sf.onclick = e => {
    const b = e.target.closest('button');
    if (b) {
      st.s = b.dataset.v;
      render();
    }
  };
}

if (cf) {
  cf.onclick = e => {
    const b = e.target.closest('button');
    if (b) {
      st.c = b.dataset.v;
      render();
    }
  };
}

if (q) {
  q.oninput = () => {
    st.q = q.value.trim();
    render();
    if (st.t === 'week') renderWk();
  };
}

function setTab(tab, updateHash) {
  st.t = tab;
  if (seg) {
    seg.querySelectorAll('button').forEach(x => {
      x.classList.toggle('on', x.dataset.t === tab);
    });
  }
  const isWeek = st.t === 'week';
  if (weekSec) weekSec.hidden = !isWeek;
  if (chs) chs.hidden = isWeek;
  if (tocSec) tocSec.hidden = isWeek;

  const flab1 = document.getElementById('flab1');
  const flab2 = document.getElementById('flab2');
  if (sf) sf.style.display = isWeek ? 'none' : '';
  if (cf) cf.style.display = isWeek ? 'none' : '';
  if (flab1) flab1.style.display = isWeek ? 'none' : '';
  if (flab2) flab2.style.display = isWeek ? 'none' : '';

  if (st.t === 'mine') {
    st.s = 'own';
    if (updateHash) window.location.hash = 'collection';
  } else if (st.t === 'all') {
    st.s = 'all';
    if (updateHash) window.location.hash = 'official';
  } else if (st.t === 'week') {
    if (updateHash) window.location.hash = 'weekly';
  }
  render();
  if (isWeek) renderWk();
}

if (seg) {
  seg.onclick = e => {
    const b = e.target.closest('button');
    if (!b) return;
    setTab(b.dataset.t, true);
  };
}

function syncFromHash() {
  const hash = window.location.hash.replace(/^#/, '');
  if (hash === 'weekly') {
    setTab('week', false);
  } else if (hash === 'collection') {
    setTab('mine', false);
  } else if (hash === 'official') {
    setTab('all', false);
  }
}
window.addEventListener('hashchange', syncFromHash);
syncFromHash();

function renderWk() {
  if (!wkL) return;
  const E = (window.WEEKLY_PICKS_DATA && window.WEEKLY_PICKS_DATA.entries) || (window.WEEKLY && window.WEEKLY.entries) || [];
  const qq = (st.q || '').toLowerCase();
  const L = E.filter(e => !qq || ((e.displayNumber || '') + (e.nameZh || '') + (e.nameJp || '')).toLowerCase().includes(qq));
  if (!L.length) {
    wkL.innerHTML = '<p class="empty" style="padding:20px 0">目前沒有每週新品資料。</p>';
    return;
  }
  wkL.innerHTML = L.map(e => {
    const c = D.find(x => x.name === e.nameZh && getCarImg(x));
    const imgHtml = c ? im(c) : '<span style="font-size:11px;color:#a8a29e">暫無圖</span>';
    return `
      <div class="wk">
        <div class="fr">${imgHtml}</div>
        <div>
          <span class="cap">${e.weekOf || ''} 週報</span>
          <h5>${e.nameZh || ''}</h5>
          <div class="m">
            ${e.releaseOrPeriod || ''}${e.priceJpy ? '・¥' + e.priceJpy : ''}${e.owned === true ? '・<span style="color:#1E6B4F">✓ 已入手</span>' : (e.owned === false ? '・<span style="color:#B3261E">待入手</span>' : '')}
            <br>${e.place || ''}
          </div>
          ${e.sourceUrl ? `<a href="${e.sourceUrl}" target="_blank" rel="noopener">官方來源 ↗</a>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

const SEAL = (cls, big) => `
  <svg class="${cls}" viewBox="0 0 40 40" aria-label="已入手印章">
    <circle cx="20" cy="20" r="18" fill="rgba(255,255,255,.9)" stroke="#1E6B4F" stroke-width="${big ? 0.7 : 1}"/>
    <circle cx="20" cy="20" r="14.5" fill="none" stroke="#1E6B4F" stroke-width="0.5" stroke-dasharray="1.2 1.4"/>
    <text x="20" y="18.5" text-anchor="middle" font-size="7" fill="#1E6B4F" font-family="var(--sans)">又入手</text>
    <text x="20" y="28.5" text-anchor="middle" font-size="9" fill="#1E6B4F" font-family="var(--sans)">✓</text>
  </svg>
`;

const EMPTY = `
  <svg class="bigseal" viewBox="0 0 40 40" aria-label="待入手空印章">
    <circle cx="20" cy="20" r="18" fill="none" stroke="#B3261E" stroke-width="0.6" stroke-dasharray="2 2"/>
    <text x="20" y="23" text-anchor="middle" font-size="6.5" fill="#B3261E" font-family="var(--sans)">待入手</text>
  </svg>
`;

let LIST = [];

function card(c) {
  const o = isOwned(c);
  const dup = Boolean(c.isDuplicate);
  const total = (c.boxed || 0) + (c.loose || 0);
  const num = c.displayNumber || c.id;
  return `
    <div class="card ${o ? 'o' : 'u'}" onclick="openCarDetail('${c.id}')">
      <div class="fr">
        <span class="id">${num}</span>
        ${o ? SEAL('seal') : '<span class="tag">待入手</span>'}
        ${im(c)}
      </div>
      <div class="nm">${title(c)}</div>
      <div class="m">
        ${o ? `<span class="s">✓ 盒 ${c.boxed || 0}・散 ${c.loose || 0}</span>${dup ? `<span class="dupt">重複 ×${total}</span>` : ''}` : `<span class="s">待入手</span><span>${has(c.releaseDate) ? c.releaseDate : ''}</span>`}
      </div>
    </div>
  `;
}

function render() {
  if (sf) {
    sf.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.v === st.s));
  }
  if (cf) {
    cf.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.v === st.c));
  }
  LIST = [];
  let page = 4;
  if (!chs) return;
  const html = CH.map((c, i) => {
    if (st.c !== 'all' && st.c !== c[0]) return '';
    const all = D.filter(x => x.category === c[0]);
    const L = all.filter(x => (st.s === 'all' || (st.s === 'own') === isOwned(x)) && (!st.q || (x.id + (x.displayNumber || '') + (x.name || '') + (x.jpName || '')).toLowerCase().includes(st.q.toLowerCase())));
    if (!L.length && (st.q || st.s !== 'all')) return '';
    LIST.push(...L);
    const pick = all.find(x => isOwned(x) && getCarImg(x) && x.id !== (HERO ? HERO.id : '')) || all.find(x => getCarImg(x)) || all[0];
    const o = all.filter(isOwned).length;
    const p = page;
    page += 2;
    return `
      <section class="ch" id="ch-${c[0]}">
        <div class="sp">
          <div class="num">
            <span class="cap">CH.${pad(i + 1)}</span>
            <span class="cap">P.${pad(p)}</span>
          </div>
          <h3>${c[1]}</h3>
          <div class="en">${c[2]}</div>
          <div class="fig" onclick="openCarDetail('${pick.id}')">
            ${im(pick)}
          </div>
          <div class="figcap">
            <span>${pick.displayNumber || pick.id}・${title(pick)}</span>
            <span>本章精選</span>
          </div>
          <p class="quote">${c[3]}</p>
        </div>
        <div class="chp">
          <span>本章收藏 ${o} / ${all.length}</span>
          <span>${L.length} 款</span>
        </div>
        <div class="grid">${L.map(card).join('')}</div>
      </section>
    `;
  }).join('');

  chs.innerHTML = html || '<p class="empty">找不到符合的車款。</p>';
}
render();

const tbu = () => {
  if (tb && coverSec) {
    tb.classList.toggle('show', window.scrollY > coverSec.offsetHeight * 0.8);
  }
};
window.addEventListener('scroll', tbu, { passive: true });
tbu();

function goSearch(focusFilter) {
  if (findSec) {
    findSec.scrollIntoView({ behavior: 'smooth' });
    if (!focusFilter && q) {
      setTimeout(() => q.focus({ preventScroll: true }), 350);
    }
  }
}

let cur = -1, retY = 0;
const dt = document.getElementById('dt');
const dPos = document.getElementById('dPos');
const dStg = document.getElementById('dStg');
const dBody = document.getElementById('dBody');

function openCarDetail(id) {
  let i = LIST.findIndex(c => c.id === id);
  if (i < 0) {
    LIST = D.slice();
    i = D.findIndex(c => c.id === id);
  }
  cur = i;
  retY = window.scrollY;
  fillDetail();
  if (dt) dt.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeCarDetail() {
  if (dt) dt.classList.remove('open');
  document.body.style.overflow = '';
  window.scrollTo(0, retY);
}

function stepDetail(d) {
  if (!LIST.length) return;
  cur = (cur + d + LIST.length) % LIST.length;
  fillDetail();
}

function fillDetail() {
  if (!dt || cur < 0 || cur >= LIST.length) return;
  const c = LIST[cur];
  const o = isOwned(c);
  dt.className = 'dt open ' + (o ? 'o' : 'u');
  if (dPos) dPos.textContent = `${pad(cur + 1)} / ${LIST.length}`;
  if (dStg) dStg.innerHTML = im(c) + (o ? SEAL('bigseal', true) : EMPTY);

  const rows = [
    ['編號', c.displayNumber || c.id],
    ['發售日', has(c.releaseDate) ? c.releaseDate : null],
    ['系列', c.categoryName],
    ['盒裝', (o || c.boxed) ? (c.boxed || 0) + ' 台' : null],
    ['散車', (o || c.loose) ? (c.loose || 0) + ' 台' : null],
    ['狀態', o ? '<span style="color:#1E6B4F">✓ 已入手</span>' : '<span style="color:#B3261E">待入手</span>']
  ].filter(r => r[1] != null);

  if (dBody) {
    dBody.innerHTML = `
      <span class="cap">${c.displayNumber || c.id}</span>
      <h4>${title(c)}</h4>
      ${has(c.jpName) && c.jpName !== title(c) ? `<div class="jp">${c.jpName}</div>` : ''}
      ${c.isDuplicate ? '<div class="dupt" style="margin-top:4px">重複收藏 ×' + ((c.boxed || 0) + (c.loose || 0)) + '</div>' : ''}
      <dl class="dl">
        ${rows.map(r => `<div><dt>${r[0]}</dt><dd style="margin:0">${r[1]}</dd></div>`).join('')}
      </dl>
      <div class="pn">
        <button onclick="stepDetail(-1)">← 上一台</button>
        <button onclick="stepDetail(1)">下一台 →</button>
      </div>
    `;
  }
  const s = dStg ? dStg.querySelector('.bigseal') : null;
  if (s && o) {
    s.style.animation = 'none';
    s.offsetWidth;
    s.style.animation = '';
  }
}

let touchStartX = null;
if (dt) {
  dt.addEventListener('touchstart', e => {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });

  dt.addEventListener('touchend', e => {
    if (touchStartX === null) return;
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 60) {
      stepDetail(dx < 0 ? 1 : -1);
    }
    touchStartX = null;
  });
}

window.addEventListener('keydown', e => {
  if (!dt || !dt.classList.contains('open')) return;
  if (e.key === 'Escape') closeCarDetail();
  if (e.key === 'ArrowRight') stepDetail(1);
  if (e.key === 'ArrowLeft') stepDetail(-1);
});

window.openCarDetail = openCarDetail;
window.closeCarDetail = closeCarDetail;
window.openD = openCarDetail;
window.closeD = closeCarDetail;
window.step = stepDetail;
window.stepDetail = stepDetail;
window.goSearch = goSearch;
window.switchMainTab = setTab;
window.renderCompendium = render;
window.renderWeeklyTracker = renderWk;
window.CARS_DATABASE = CARS_DATABASE;
window.WEEKLY_PICKS_DATA = WEEKLY_PICKS_DATA;
</script>
'''

    new_html = head_and_styles + '\n' + weekly_picks_str + '\n\n' + cars_database_str + '\n' + script_2_logic + '\n\n' + s3_str + '\n</body>\n</html>\n'

    out_path = os.path.join(root, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f'Successfully generated {out_path}, size: {len(new_html)} bytes')

if __name__ == '__main__':
    main()
