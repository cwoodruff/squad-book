#!/usr/bin/env bash
# Check that external links in the book resolve (HTTP < 400). Usage: scripts/check-links.sh
set -uo pipefail
cd "$(dirname "$0")/.."
grep -rhoE 'https?://[^ )>"`]+' book | sed 's/[.,;:]$//' | sort -u > /tmp/squad-book-links.txt
fail=0
while read -r u; do
  code=$(curl -s -o /dev/null -L -m 15 -w '%{http_code}' "$u")
  if [ "$code" -ge 400 ] || [ "$code" = "000" ]; then echo "BROKEN $code $u"; fail=1; fi
done < /tmp/squad-book-links.txt
echo "checked $(wc -l < /tmp/squad-book-links.txt) links"; exit $fail
