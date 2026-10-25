# Tomica Cars 來源等級／信心再校正（SOURCE AUDIT）

**執行時間（Asia/Taipei）：** 2026-10-25（verifiedAt 全數同日）
**範圍：** Cars／カーズトミカ registry 152 筆；重點＝官方發售資料可信度（非二手賣場品相）。
**台灣代理用語：** 卡布

## 方法

1. 來源等級：`Official`／`Primary retail`／`Secondary`／`Community`／`Unverified`。
2. 本回合實際打開（WebFetch）的活頁才可當 `evidenceUrls`；失效或衝突 → 降級或維持「官方未載明」。
3. `high` 僅 Official 或 Primary retail（或兩者交叉）；禁止猜填日期。
4. tomicadas 本回合 curl／fetch 失敗 → **不**單獨升級；HobbySearch／Takara 活頁為準。
5. 品相摘要預設：`新品／官方商品頁（無品相欄）`（本輪非二手狀態欄）。

## 本回合打開的活頁

- https://www.takaratomy.co.jp/products/disney/cars/
- https://www.takaratomy.co.jp/products/disney/cars/archive.html
- https://www.takaratomy.co.jp/products/disney/cars/20th/
- https://takaratomymall.jp/shop/g/g4904810981015/
- https://www.takaratomy.co.jp/products/tomica/new/2002.htm
- https://www.takaratomy.co.jp/products/tomica/new/2507.htm
- https://www.takaratomy.co.jp/products/tomica/new/2510.htm
- https://www.takaratomy.co.jp/products/tomica/new/2606.htm
- https://www.takaratomy.co.jp/products/tomica/new/2608.htm
- https://www.takaratomy.co.jp/products/tomica/new/2609.htm
- https://www.takaratomy.co.jp/products/tomica/new/2611.htm
- https://www.1999.co.jp/list/2547/7/1
- https://www.1999.co.jp/list/2547/7/2
- https://www.1999.co.jp/list/2547/7/3
- https://www.1999.co.jp/list/2547/7/4

## 統計

| 項目 | 數值 |
|---|---:|
| 有可讀發售日（前→後） | 127 → **149**（+22） |
| 仍「官方未載明」 | **3** |
| confidence high / medium / low | 147 / 2 / 3 |
| sourceTier Official / Primary retail / Unverified | 128 / 23 / 1 |
| 本回合欄位改動列 | 24 |

## confidence 分布說明

- **high（147）**：發售日有 Official（Takara new／mall／20th）或 Primary retail（HobbySearch 列表活頁）依據。
- **medium（2）**：`C-01_mcqueen_standard`、`C-04_mater_standard` — HobbySearch 載 2011-06，但初代 2008 説無 Official 活頁可鎖（可能改模／再掲載）。
- **low（3）**：仍未載明或非 Tomica／系列見出し（見下表）。

## 仍「官方未載明」（3）

| number | display | officialNameJp | sourceTier | confidence | 原因 |
|---|---|---|---|---|---|
| `C-02_mcqueen_dinoco` | C-2 | ライトニング・マックィーン(DINOCOタイプ) | Primary retail | low | HobbySearch 日期衝突（2011-06 vs 2020-12） |
| `SP_lightning_mcqueen_cars_3_metallic_rust_eze_racing_center` | SP | Lightning McQueen (Cars 3 Metallic Rust- | Unverified | low | 非 Tomica（Mattel） |
| `SET_mcqueen_2026special` | 官方未載明 | ライトニング・マックィーンデイ2026特別仕様のカーズ トミカが登場! 作品と一 | Official | low | 公式系列見出し，非單一 SKU |

## 本回合發售日升級（22）

| number | 新 releaseDate | sourceTier | confidence |
|---|---|---|---|
| `SET_carwash` | 2026-11 | Official | high |
| `SET_mcqueen_deruderu_bucket` | 2026-08 | Official | high |
| `マック_cars3_transporter` | 2018-11 | Primary retail | high |
| `SP_mater_mcqueen_2023_special` | 2023-09 | Primary retail | high |
| `C-39_cruz_silver` | 2020-03 | Primary retail | high |
| `C-40_doc_silver` | 2020-03 | Primary retail | high |
| `C-31_mcqueen_silver` | 2020-03 | Primary retail | high |
| `C-38_storm_silver` | 2020-03 | Primary retail | high |
| `C-39_topper3_standard` | 2015-10 | Primary retail | high |
| `C-25_mcqueen_hotrod` | 2019-12 | Primary retail | high |
| `C-08_doc_fabulous` | 2017-12 | Primary retail | high |
| `C-37_storm_thomasville` | 2019-03 | Primary retail | high |
| `C-22_luigi_rrc` | 2019-03 | Primary retail | high |
| `C-18_shu_standard` | 2011-06 | Primary retail | high |
| `C-21_j_p_standard` | 2018-10 | Primary retail | high |
| `C-06_doc_standard` | 2008-03 | Primary retail | high |
| `C-08_ramone_standard` | 2008-07 | Primary retail | high |
| `C-20_sarge_standard` | 2020-10 | Primary retail | high |
| `C-17_francesco_standard` | 2011-06 | Primary retail | high |
| `C-26_ramone_standard` | 2021-04 | Primary retail | high |
| `C-01_mcqueen_standard` | 2011-06 | Primary retail | medium |
| `C-04_mater_standard` | 2011-06 | Primary retail | medium |

## 重核（易錯／覆寫過／C-21 系列）

| number | releaseDate | 結果 |
|---|---|---|
| `C-34_mcqueen_grc` | 2025-10-18 | 維持 2025-10-18；mall＋2510 Official high |
| `C-15_cruz_road_patrol` | 2025-07-26 | 維持 2025-07-26；2507 Official high |
| `C-03_mcqueen_20th` | 2026-06 | 維持 2026-06；2606＋20th Official high |
| `SP_storm_20th` | 2026-08 | 維持 2026-08；2608 Official high |
| `SP_mcqueen_piston_cup_mcqueen_2026special` | 2026-09 | 維持 2026-09；2609 Official high |
| `C-21_j_p_standard` | 2018-10 | 補 2018-10；HobbySearch list/4；對應 easter egg Apple #84 |
| `C-21_holly_standard` | 2011-07 | 維持 2011-07；HobbySearch list/1 |
| `C-21_mcqueen_cars3_standard` | 2022-04 | 維持 2022-04；HobbySearch list/4 |

## character_easter_eggs / Apple #84

- `data/character_easter_eggs.json` → `tomicaMatch.number` = `C-21_j_p_standard`（不變）。
- 彩蛋正文來源：`Snow Chang 手寫／2026-10-25`（本回合不改寫正文）。
- 該筆發售日本回合由 Primary retail 補為 `2018-10`（high）。

## 欄位契約（corrections.json 每筆）

`number`, `displayNumber`, `officialNameJp`, `nameZh`, `releaseDate`, `releaseDatePrecision`, `sourceTier`, `confidence`, `verifiedAt`, `evidenceUrls`, `notes`（保留 `*Changed` 旗標語意）。

