#!/usr/bin/env bash
# Install (or remove) the OpenCode build of likbez.
#
#   scripts/install-opencode.sh            install / refresh
#   scripts/install-opencode.sh --remove   uninstall everything installed here
#
# Layout (details: docs/opencode.md):
#   ~/.config/opencode/skills/likbez-*/     generated skills (with their
#                                           references/, assets/, scripts/ subtrees)
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
OC="$CONFIG_HOME/opencode"

if [ "${1:-}" = "--remove" ]; then
  rm -rf "$OC/skills"/likbez-*
  echo "likbez: removed from $OC"
  exit 0
fi

if [ ! -f "$SRC/.claude-plugin/marketplace.json" ]; then
  echo "likbez: $SRC does not look like the likbez checkout" >&2
  exit 1
fi

echo "likbez: installing from $SRC into $OC"

# 1. Generate the OpenCode artifacts (into <checkout>/opencode/dist).
DIST="$SRC/opencode/dist"
rm -rf "$DIST"
python3 "$SRC/scripts/build_opencode.py" --source "$SRC" --out "$DIST"

# 2. Place them into OpenCode's flat discovery directory (stale copies first).
mkdir -p "$OC/skills"
rm -rf "$OC/skills"/likbez-*
cp -R "$DIST/skills/." "$OC/skills/"

COUNT="$(find "$OC/skills" -maxdepth 1 -type d -name 'likbez-*' | wc -l | tr -d ' ')"
echo "likbez: installed $COUNT skills"
echo "likbez: restart opencode to load them; see docs/opencode.md"
