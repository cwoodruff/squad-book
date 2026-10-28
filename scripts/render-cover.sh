#!/usr/bin/env bash
# Render per-volume covers from book/images/src/cover.html to book/images/cover-volN.png (1600x2400).
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
render() {
  local vol="$1" sub="$2" ver="$3" tmp
  tmp="$(mktemp -t cover).html"
  sed -e "s|{{SUBTITLE}}|$sub|" -e "s|{{VOLUME}}|$ver|" book/images/src/cover.html > "$tmp"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1600,2400 \
    --screenshot="$PWD/book/images/cover-$vol.png" "file://$tmp" >/dev/null 2>&1
  rm -f "$tmp"; echo "rendered book/images/cover-$vol.png"
}
render vol1 "Volume 1: Using Squad<br>From First Session to Everyday Practice" "Covers Squad v1.1.0"
render vol2 "Volume 2: Operating and Extending Squad<br>Production, Internals, and Squad 2.0" "Covers Squad v1.1.0 and the 2.0 preview"
