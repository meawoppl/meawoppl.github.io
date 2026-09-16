#!/usr/bin/env bash
# Build public/resume/MatthewGoodman.pdf from its LaTeX source.
# Aux files go to a temp dir so only the PDF lands in public/.
set -euo pipefail

cd "$(dirname "$0")/../../public/resume"
out="$(mktemp -d)"
trap 'rm -rf "$out"' EXIT

# Two passes so hyperref's PDF bookmarks resolve.
for _ in 1 2; do
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$out" MatthewGoodman.tex >/dev/null \
    || { cat "$out/MatthewGoodman.log"; exit 1; }
done

cp "$out/MatthewGoodman.pdf" MatthewGoodman.pdf
echo "Built public/resume/MatthewGoodman.pdf"
