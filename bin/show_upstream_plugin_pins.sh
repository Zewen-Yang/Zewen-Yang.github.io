#!/usr/bin/env bash
# Compare local al-folio gem pins with upstream/main.
# Run from the site repo root. Fetches upstream first.
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

if ! git remote get-url upstream >/dev/null 2>&1; then
  echo "No 'upstream' remote. Add: git remote add upstream https://github.com/alshedivat/al-folio.git" >&2
  exit 1
fi

git fetch upstream

extract_pins() {
  awk '/group :al_folio_plugins/,/^end$/'
}

echo "=== upstream/main Gemfile (:al_folio_plugins) ==="
git show upstream/main:Gemfile | extract_pins
echo
echo "=== local Gemfile (:al_folio_plugins) ==="
extract_pins < Gemfile
