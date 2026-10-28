#!/usr/bin/env bash
# Pre-render all inline ```mermaid blocks (normally done automatically by scripts/mermaid.lua during the build).
set -euo pipefail
cd "$(dirname "$0")/.."
for f in book/vol*/part-*/*.md book/shared/appendices/*.md book/vol*/appendices/*.md; do
  pandoc "$f" --lua-filter=scripts/mermaid.lua -t native -o /dev/null
done
echo "diagrams cached in build/diagrams/"
