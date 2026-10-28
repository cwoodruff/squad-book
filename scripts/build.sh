#!/usr/bin/env bash
# Build one volume as EPUB (default) or single-page HTML.
# Usage: scripts/build.sh <vol1|vol2> [epub|html]
set -euo pipefail
cd "$(dirname "$0")/.."
VOL="${1:?usage: build.sh <vol1|vol2> [epub|html]}"
FORMAT="${2:-epub}"
mkdir -p dist
FILES=()
while IFS= read -r f; do FILES+=("$f"); done < <(
  ls book/$VOL/00-front/*.md
  ls book/$VOL/part-*/*.md
  ls book/shared/appendices/*.md book/$VOL/appendices/*.md 2>/dev/null | awk -F/ '{print $NF"\t"$0}' | sort | cut -f2
)
OUT="dist/mastering-squad-$VOL"
COMMON=(--from=markdown+smart+pipe_tables+fenced_divs-raw_html --resource-path=.:book:book/images --toc --toc-depth=1 --metadata-file=book/metadata-$VOL.yaml --lua-filter=scripts/mermaid.lua)
case "$FORMAT" in
  epub) pandoc "${COMMON[@]}" --to=epub3 --split-level=1 --css=styles/epub.css -o "$OUT.epub" "${FILES[@]}" ;;
  html) pandoc "${COMMON[@]}" --to=html5 --standalone --embed-resources --css=styles/epub.css -o "$OUT.html" "${FILES[@]}" ;;
  *) echo "unknown format $FORMAT"; exit 1 ;;
esac
echo "Built $OUT.$FORMAT from ${#FILES[@]} files"
