# 驗證摘要（2026-10-25）

| 項目 | 結果 |
|---|---|
| 原檔張數 | 69（`/workspace/tomica-owned-reshoot/photos/`） |
| 抽樣原檔 GPS | 有（含緯經度／海拔／方位）→ **不可直接上架** |
| 去 EXIF 後張數 | 69（`sanitized_photos/*.jpg`） |
| sanitized GPS Latitude hits | **0** |
| 方法 | Pillow RGB 重存 JPEG quality=92，不寫入 exif |

注意：去 EXIF ≠ 視覺安全。上架前仍須過 `PRIVACY_CHECKLIST.md`（地板／價簽／反光等）。
