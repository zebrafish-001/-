#!/usr/bin/env bash
# Fetch the full open icon libraries (not vendored in the repo) for a much larger search space.
# Afterwards: export TOCMAKER_ICON_PATHS="$PWD/tocmaker/assets/icons/external/bioicons/static/icons:$PWD/tocmaker/assets/icons/external/healthicons/public/icons/svg/filled"
set -euo pipefail
DST="$(dirname "$0")/../tocmaker/assets/icons/external"
mkdir -p "$DST"
if [ ! -d "$DST/bioicons" ]; then
  git clone --depth 1 --filter=blob:none --sparse https://github.com/duerrsimon/bioicons "$DST/bioicons"
  (cd "$DST/bioicons" && git sparse-checkout set static/icons)
fi
if [ ! -d "$DST/healthicons" ]; then
  git clone --depth 1 --filter=blob:none --sparse https://github.com/resolvetosavelives/healthicons "$DST/healthicons"
  (cd "$DST/healthicons" && git sparse-checkout set public/icons/svg/filled public/icons/svg/outline)
fi
echo "Bioicons: $(find "$DST/bioicons/static/icons" -name '*.svg' | wc -l) SVGs (licence per icon: cc-0 / mit / cc-by / cc-by-sa folders)"
echo "Health Icons: $(find "$DST/healthicons/public/icons/svg" -name '*.svg' | wc -l) SVGs (MIT)"
