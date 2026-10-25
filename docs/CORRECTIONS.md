# Tomica Cars 名稱／發售日校正說明（給 Snow）

**執行時間（Asia/Taipei）：** 2026-10-25（含同日來源再校正）  
**範圍：** 僅 Cars／カーズトミカ（registry 152 筆；含 SP／遊具／World）。非 Tomica（Mattel 等）不捏造發售日。  
**台灣代理：** 卡布（Cabu）— 繁中名優先對齊可查的台灣通路標題。

## 來源等級與信心（2026-10-25 再校正）

詳見 `docs/SOURCE_AUDIT.md`。

| 等級 | 意義 |
|---|---|
| Official | Takara 公式（disney/cars、tomica/new、mall） |
| Primary retail | 日本一級通路（本輪：HobbySearch 1999.co.jp 列表活頁） |
| Secondary | 台灣通路／轉貼等 |
| Community | 收藏家年表（tomicadas）— 不可單獨升 high |
| Unverified | 無可用依據 |

- **confidence high**：發售日須有 Official 或 Primary retail 活頁依據。
- **禁止猜填日期**；衝突或多世代未分清 →「官方未載明」。
- 每筆 corrections 現含：`sourceTier`／`confidence`／`verifiedAt`／`evidenceUrls`。
- 品相：本輪為新品／官方商品頁（無品相欄）。

## 鐵則（已遵守）

1. 每個寫入的 `releaseDate`／`nameZh`／`officialNameJp` 變更，`sources`／`evidenceUrls` 皆為可點 URL（或 tried: …）。
2. **禁止**憑記憶、論壇口耳、無 URL 年表、推測年月。
3. 查不到維持「官方未載明」，並列於「仍未載明」表。
4. 次要來源須與另一可打開來源交叉同意 YYYY-MM 才寫死；Takara 新聞／mall／HobbySearch 一級列表可採用。

## 統計（來源再校正後）

| 項目 | 值 |
|---|---:|
| 有可讀發售日 | **149**（再校正前 127；+22） |
| 有繁中名 | 152 |
| 仍「官方未載明」發售日 | **3** |
| confidence high／medium／low | 147／2／3 |

## 仍「官方未載明」發售日（3）

| number | display | officialNameJp | 說明 |
|---|---|---|---|
| `C-02_mcqueen_dinoco` | C-2 | ライトニング・マックィーン(DINOCOタイプ) | HobbySearch 日期衝突（2011-06 vs 2020-12） |
| `SP_lightning_mcqueen_cars_3_metallic_rust_eze_racing_center` | SP | Lightning McQueen (Cars 3 Metallic Rust-eze Racing | 非 Tomica（Mattel） |
| `SET_mcqueen_2026special` | 官方未載明 | ライトニング・マックィーンデイ2026特別仕様のカーズ トミカが登場! 作品と一緒に楽しもう! | 公式系列見出し，非單一 SKU |

## 本回合補上的發售日（節錄）

| number | releaseDate | 依據 |
|---|---|---|
| `C-21_j_p_standard` | 2018-10 | HobbySearch list/4 |
| `C-34_mcqueen_grc` | 2025-10-18（重核） | mall＋new/2510 |
| `SET_carwash` | 2026-11 | new/2611＋20th |
| `SET_mcqueen_deruderu_bucket` | 2026-08 | new/2608 |
| 銀賽車四筆 C-31/38/39/40 | 2020-03 | HobbySearch＋公式銀系列公告交叉 |

（完整見 `corrections.json`／`SOURCE_AUDIT.md`）

---

以下保留先前校正說明（歷史）：

## 做了什麼

1. 重抓／核對 Takara トミカ新製品頁（`…/tomica/new/YYmm.htm`）中含カーズ的條目，寫入月或日精度發售日。
2. 以 takaratomymall 商品頁核對例：C-34 GRC `2025-10-18`。
3. Hobby Search 列表頁（`1999.co.jp/list/2547/7/1`～`3` 等，本回合 WebFetch 可打開）＋ tomicadas 年表（`http://tomicadas.on.coocan.jp/c_disney_cars_list.htm`）交叉填補歷史月精度。
4. 發現多筆原 registry **錯世代／錯日期**（與 Takara 新聞不符），已覆寫（見下表）。
5. 全數補齊／統一繁中名（角色＋類型）；台灣通路可查者優先（脫線、奇諾、韓大夫、阿飛、雷蒙、麥大叔、風暴傑森、路易吉／卡布 等）。

## 主要來源清單

- https://www.takaratomy.co.jp/products/disney/cars/
- https://www.takaratomy.co.jp/products/disney/cars/archive.html
- https://www.takaratomy.co.jp/products/disney/cars/20th/
- https://www.takaratomy.co.jp/products/disney/cars/cars_tomica_world.html
- https://www.takaratomy.co.jp/products/tomica/new/ （各月新製品，例 2401／2406／2407／2410／2507／2510／2601／2606／2608／2609…）
- https://takaratomymall.jp/shop/g/g4904810981015/ （C-34 GRC 発売日）
- https://www.1999.co.jp/list/2547/7/1 （及 /2、/3）
- http://tomicadas.on.coocan.jp/c_disney_cars_list.htm （僅作交叉，不單源寫死）
- 台灣通路例：https://shop.funbox.com.tw/products/ds18948 、https://24h.pchome.com.tw/prod/DEAS20-B900I2ULR 等

本包亦存研究快取：`research/takara_new/*.htm`、`research/hobby_search_cars.json`、`research/tomicadas_parsed.json`、`research/mall_c34_grc_evidence.json`。

## 原 registry 日期與公式不符（已覆寫，節錄）

| number | 新 releaseDate | 說明 |
|---|---|---|
| `C-06_cruz_dinoco` | → `2022-07` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-06 クルーズ・ラミレス（DINOCOレーシングタイプ）； |
| `C-15_cruz_road_patrol` | → `2025-07-26` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-15 クルーズ・ラミレス（道路パトロールカータイプ）；原  |
| `C-19_fillmore_fire_command` | → `2024-12` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-19 フィルモア（消防指揮車タイプ）；原 registry「2020-04-25」與公式不 |
| `C-22_mater_ice` | → `2024-02` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-22 メーター（アイスレーシングタイプ）；原 regist |
| `C-23_guido_ambulance` | → `2024-10` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-23 グイド（救急車タイプ）；原 registry「2020-04-25」與公式不符，已覆 |
| `C-23_max_standard` | → `2021-10` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：Ｃ－２３ マックス・シュネル；原 registry「2011- |
| `C-24_mcqueen_ice` | → `2024-01` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-24 ライトニング・マックィーン（アイスレーシングタイプ） |
| `C-25_cruz_ice` | → `2024-01` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-25 クルーズ・ラミレス（アイスレーシングタイプ）；原 r |
| `C-27_doc_patrol` | → `2024-07` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-27 ドック・ハドソン（パトカータイプ）；原 registry「2019-09-21」與公 |
| `C-28_fritter_standard` | → `2022-04` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-28 ミス・フリッター；原 registry「2017-0 |
| `C-30_mcqueen_sheriff` | → `2023-10` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-30 ライトニング・マックィーン（シェリフタイプ）；原 r |
| `C-33_todd_standard` | → `2023-10` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-33 トッド（スタンダードタイプ）；原 registry「2018-04-21」與公式不符 |
| `C-34_mcqueen_grc` | → `2025-10-18` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C－34 ライトニング・マックィーン(GRCタイプ) 発売日2025年10月18日；亦見 ht |
| `C-36_mcqueen_patrol` | → `2024-06` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-36 ライトニング・マックィーン（パトカータイプ）；原 registry「2019-11- |
| `C-38_mater_firetruck` | → `2024-06` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：C-38 メーター（消防車タイプ）；原 registry「20 |
| `C-39_luigi_ambulance` | → `2024-10` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-39 ルイジ（救急車タイプ）；原 registry「2020-04-25」與公式不符，已覆 |
| `C-40_ramone_road_patrol` | → `2024-12` | 繁中優先對齊台灣通路標題；代理商：卡布；Takara/公式可核對：C-40 ラモーン（道路パトロールカータイプ）；原 registry「2020-05-23」與 |
| `SP_storm_20th` | → `2026-08` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：SP ジャクソン・ストーム（20周年記念タイプ）；原 regi |
| `SP_mcqueen_piston_cup_mcqueen_2026special` | → `2026-09` | 繁中由 Takara 日文官名意譯；台灣代理：卡布；角色名採台灣常見譯；Takara/公式可核對：ライトニング・マックィーン ピストン・カップ付き（マックィーン |

（完整見 `corrections.json` 內 `notes` 含「原 registry」者）

## 仍「官方未載明」發售日（25）

| number | display | officialNameJp | tried |
|---|---|---|---|
| `C-01_mcqueen_standard` | C-1 | ライトニング・マックィーン(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-02_mcqueen_dinoco` | C-2 | ライトニング・マックィーン(DINOCOタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-04_mater_standard` | C-4 | メーター(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-06_doc_standard` | C-6 | ドック・ハドソン(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-08_doc_fabulous` | C-8 | ドック・ハドソン(ファビュラスタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-08_ramone_standard` | C-8 | ラモーン(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-17_francesco_standard` | C-17 | フランチェスコ・ベルヌーイ(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-18_shu_standard` | C-18 | シュウ・トドロキ(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-20_sarge_standard` | C-20 | サージ(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-21_j_p_standard` | C-21 | J・P・ドライブ(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-22_luigi_rrc` | C-22 | ルイジ(RRCタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-25_mcqueen_hotrod` | C-25 | ライトニング・マックィーン(ホットロッドタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-26_ramone_standard` | C-26 | ラモーン(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-31_mcqueen_silver` | C-31 | ライトニング・マックィーン(シルバーレーサータイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-37_storm_thomasville` | C-37 | ジャクソン・ストーム(トーマスビルタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-38_storm_silver` | C-38 | ジャクソン・ストーム(シルバーレーサータイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-39_cruz_silver` | C-39 | クルーズ・ラミレス(シルバーレーサータイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-39_topper3_standard` | C-39 | トッパー・デッキントン3世(スタンダードタイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `C-40_doc_silver` | C-40 | ドック・ハドソン(シルバーレーサータイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `SP_lightning_mcqueen_cars_3_metallic_rust_eze_racing_center` | SP | Lightning McQueen (Cars 3 Metallic Rust- | tried: scope excludes non_tomica Mattel |
| `SP_mater_mcqueen_2023_special` | SP | メーター(ライトニング・マックィーンデイ 2023 特別仕様) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `マック_cars3_transporter` | マック | (カーズ3 トランスポータータイプ) | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `SET_mcqueen_deruderu_bucket` | 官方未載明 | カーズ トミカと一緒に楽しもう! ライトニング・マックィーンデザインのでるでるバ | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `SET_mcqueen_2026special` | 官方未載明 | ライトニング・マックィーンデイ2026特別仕様のカーズ トミカが登場! 作品と一 | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |
| `SET_carwash` | 官方未載明 | 洗車場 | tried: https://www.takaratomy.co.jp/products/disney/cars/ | https://www.takaratomy.co.jp/products/disney/cars/archive.html | https://www.takaratomy.co.jp/products/disney/cars/20th/ | https://www.1999.co.jp/list/2547/7/1 | http://tomicadas.on.coocan.jp/c_disney_cars_list.htm |

### 仍缺最多的區塊

1. **初代長期販售／再販**（C-01／C-02／C-04／C-06 等）：Hobby Search 常顯示再販月，與年表首發月不一致 → 兩源無法交叉，維持未載明。
2. **銀色賽車系列／部分 RRC／熱桿**（C-31 silver、C-37 Thomasville、C-38／C-39／C-40 silver 等）：單源月分不一致或缺 Hobby 列。
3. **套組文案列**（SET_carwash、SET_mcqueen_* 宣傳句）與 **非 Tomica Mattel SP**。
4. **SP 麥坤日 2023 脫線**：本回合未取到對應 Takara `2309.htm`；僅單一路徑線索 → 未寫死。

## 產出檔

- `corrections.json` — Antigravity 可套用的校正陣列
- `registry_patched.json` — 已套用的完整 registry
- `NAME_STYLE.md` — 譯名對照
- `ANTIGRAVITY_PROMPT.md` — 可貼上的套用指示
- `checklist.md`
