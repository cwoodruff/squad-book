#!/usr/bin/env bash
# Check that external links in the book resolve (HTTP < 400), and that no link still points at
# the pre-2.0 Squad hosts (bradygaster.github.io/squad, github.com/bradygaster/squad).
# Scans book/ and exercises/. Every unique URL is probed once, except the skip list below.
# Usage: scripts/check-links.sh
#   LINK_JOBS=N     parallel probes (default 8)
#   LINK_DRY_RUN=1  extract, skip and count as usual, but do not touch the network
set -uo pipefail
cd "$(dirname "$0")/.."

# Skip list: local endpoints and documentation placeholders that can never resolve.
# One extended regex per entry, matched against the whole URL. Keep it small and explain each.
SKIP_PATTERNS=(
  '^https?://(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])([:/?#]|$)'   # loopback (sample API, OTel, Aspire)
  '^https?://([^/]*\.)?example\.(com|org|net)([:/?#]|$)'              # RFC 2606 example hosts
  '^https?://[^/]*\.(example|test|invalid|localhost)([:/?#]|$)'       # RFC 2606 reserved TLDs
  'YOUR_[A-Z_]+'                                                      # fill-in placeholder (YOUR_ORG, ...)
  '^https?://github\.com/acme/'                                       # App A example remote
)
OLD_HOST='^https?://(bradygaster\.github\.io/squad|github\.com/bradygaster/squad|raw\.githubusercontent\.com/bradygaster/squad)([/?#]|$)'

tmp="$(mktemp -d "${TMPDIR:-/tmp}/squad-book-links.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

# Extract: a URL stops at whitespace, quotes, backticks, brackets, braces, <, >, |, $ or \.
# Then strip trailing sentence punctuation and Markdown emphasis (repeatedly: "url).", "url**,").
grep -rhoE "https?://[^][:space:]\"'\`<>(){}|\\\$]+" book exercises \
  | sed -E 's/[].,;:!?*_]+$//' | sort -u > "$tmp/all"
total=$(wc -l < "$tmp/all" | tr -d ' ')

fail=0
if old=$(grep -E "$OLD_HOST" "$tmp/all"); then
  echo "$old" | sed 's/^/OLD-HOST /'; fail=1
fi

skip_re=$(IFS='|'; echo "${SKIP_PATTERNS[*]}")
grep -E  "$skip_re" "$tmp/all" > "$tmp/skipped" || true
grep -vE "$skip_re" "$tmp/all" > "$tmp/probe"   || true
skipped=$(wc -l < "$tmp/skipped" | tr -d ' ')
expected=$(wc -l < "$tmp/probe" | tr -d ' ')
sed 's/^/SKIP /' "$tmp/skipped"

# Each probe prints exactly one line ("OK code url" or "BROKEN code url") and exits 0;
# a non-zero xargs status therefore means a probe itself failed to run.
probe() {
  if [ -n "${LINK_DRY_RUN:-}" ]; then code=200
  else code=$(curl -s -o /dev/null -L -m 15 -w '%{http_code}' "$1"); fi
  case "$code" in ''|000|[4-9]??) echo "BROKEN ${code:-none} $1" ;; *) echo "OK $code $1" ;; esac
}
export -f probe
# NUL-delimited input so xargs never interprets quotes or backslashes in a URL.
tr '\n' '\0' < "$tmp/probe" \
  | xargs -0 -n1 -P "${LINK_JOBS:-8}" bash -c 'probe "$1"' _ > "$tmp/results"
xs=$?
[ "$xs" -ne 0 ] && { echo "ERROR xargs exited $xs"; fail=1; }

grep '^BROKEN ' "$tmp/results" && fail=1
checked=$(grep -cE '^(OK|BROKEN) ' "$tmp/results")
broken=$(grep -c '^BROKEN ' "$tmp/results")
if [ "$checked" -ne "$expected" ]; then
  echo "ERROR probed $checked of $expected URLs"; fail=1
fi
mode=""; [ -n "${LINK_DRY_RUN:-}" ] && mode=" (dry run, no network)"
echo "found $total unique URLs: checked $checked, skipped $skipped, broken $broken$mode"
exit $fail
