#!/bin/bash
# Sets up a working directory for IBM deck HTML slides.
# Symlinks media/ and fonts/ from the skill's bundled assets so HTML
# templates can resolve their relative paths (media/image6.png, fonts/inter.css).
#
# Usage: bash .claude/skills/ibm-deck/scripts/setup-workspace.sh <target-dir>
# Example: bash .claude/skills/ibm-deck/scripts/setup-workspace.sh playgrounds/IBM

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-.}"

mkdir -p "$TARGET_DIR/images"

# Symlink media/ and fonts/ if not already present
if [ ! -e "$TARGET_DIR/media" ]; then
  ln -s "$SKILL_DIR/assets/media" "$TARGET_DIR/media"
  echo "Linked media/ → $SKILL_DIR/assets/media"
fi

if [ ! -e "$TARGET_DIR/fonts" ]; then
  ln -s "$SKILL_DIR/assets/fonts" "$TARGET_DIR/fonts"
  echo "Linked fonts/ → $SKILL_DIR/assets/fonts"
fi

# Copy templates to target if not already there
for tmpl in slide-title-template.html slide-divider-template.html; do
  if [ ! -e "$TARGET_DIR/$tmpl" ]; then
    cp "$SKILL_DIR/assets/$tmpl" "$TARGET_DIR/$tmpl"
    echo "Copied $tmpl → $TARGET_DIR/"
  fi
done

echo "Workspace ready at $TARGET_DIR"
