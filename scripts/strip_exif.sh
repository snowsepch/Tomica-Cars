#!/usr/bin/env bash
# 將來源圖重編碼為無 EXIF／GPS 的 JPEG。
# 用法：./strip_exif.sh <來源檔或資料夾> [輸出資料夾]
set -euo pipefail
SRC="${1:?用法: $0 <檔或資料夾> [輸出資料夾]}"
OUT="${2:-./sanitized_out}"
mkdir -p "$OUT"

strip_one() {
  local f="$1"
  local base stem dest
  base=$(basename "$f")
  stem="${base%.*}"
  dest="$OUT/${stem}.jpg"
  python3 - "$f" "$dest" <<'PY'
import sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
# 不傳 exif= → 新檔無拍攝中繼資料
im.save(dst, "JPEG", quality=92, optimize=True)
print(dst)
PY
}

if [[ -d "$SRC" ]]; then
  shopt -s nullglob
  for f in "$SRC"/*; do
    case "${f,,}" in
      *.jpg|*.jpeg|*.png|*.heic|*.webp) strip_one "$f" ;;
    esac
  done
elif [[ -f "$SRC" ]]; then
  strip_one "$SRC"
else
  echo "找不到: $SRC" >&2
  exit 1
fi

echo "--- 驗證（應無 GPS Latitude）---"
exiftool -r -gps:all "$OUT" 2>/dev/null | grep -c "GPS Latitude" && echo "警告：仍有 GPS" >&2 || echo "GPS Latitude hits: 0（通過）"
