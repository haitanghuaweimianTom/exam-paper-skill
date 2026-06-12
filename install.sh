#!/bin/bash
# Exam Paper Skill Installer
# Usage: bash install.sh [target_dir]
#   target_dir: ~/.claude/skills (default) or a project's .claude/skills

set -e

TARGET="${1:-$HOME/.claude/skills}"
SKILL_DIR="$TARGET/exam-paper-skill"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing exam-paper skill to $SKILL_DIR..."

# Dependency checks
missing=()

command -v pandoc >/dev/null 2>&1 || missing+=("pandoc")
command -v xelatex >/dev/null 2>&1 || missing+=("xelatex (TeX Live)")
python3 -c "import matplotlib" >/dev/null 2>&1 || missing+=("matplotlib Python package")

if [ ${#missing[@]} -ne 0 ]; then
    echo "WARNING: The following dependencies are missing or not in PATH:"
    for dep in "${missing[@]}"; do
        echo "  - $dep"
    done
    echo "Please install them before generating PDFs or diagrams."
fi

mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

# Copy optional tools/helpers if present
if [ -d "$SCRIPT_DIR/tools" ]; then
    cp -r "$SCRIPT_DIR/tools" "$SKILL_DIR/tools"
fi

# Copy examples if present
if [ -d "$SCRIPT_DIR/examples" ]; then
    cp -r "$SCRIPT_DIR/examples" "$SKILL_DIR/examples"
fi

# Copy assets if present
if [ -d "$SCRIPT_DIR/assets" ]; then
    cp -r "$SCRIPT_DIR/assets" "$SKILL_DIR/assets"
fi

echo "Installed exam-paper skill to $SKILL_DIR"
