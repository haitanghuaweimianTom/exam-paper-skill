#!/bin/bash
# Exam Paper Skill Installer
# Usage: bash install.sh [target_dir]
#   target_dir: ~/.claude/skills (default) or a project's .claude/skills

TARGET="${1:-$HOME/.claude/skills}"
SKILL_DIR="$TARGET/exam-paper-skill"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "$SKILL_DIR"
cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"

# Copy optional tools/helpers if present
if [ -d "$SCRIPT_DIR/tools" ]; then
    cp -r "$SCRIPT_DIR/tools" "$SKILL_DIR/tools"
fi

echo "Installed exam-paper skill to $SKILL_DIR"
