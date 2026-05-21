#!/bin/bash
# Exam Paper Skill Installer
# Usage: bash install.sh [target_dir]
#   target_dir: ~/.claude/skills (default) or a project's .claude/skills

TARGET="${1:-$HOME/.claude/skills}"
SKILL_DIR="$TARGET/exam-paper"

mkdir -p "$SKILL_DIR"
cp "$(dirname "$0")/SKILL.md" "$SKILL_DIR/SKILL.md"
echo "Installed exam-paper skill to $SKILL_DIR"
