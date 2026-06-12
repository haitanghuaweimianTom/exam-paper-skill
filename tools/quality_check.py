#!/usr/bin/env python3
"""Quality checker for exam-paper-skill generated markdown.

Scans markdown content for common PDF-rendering mistakes and reports them.
"""

import argparse
import re
import sys
from pathlib import Path


class MarkdownChecker:
    def __init__(self, content):
        self.content = content
        self.issues = []
        self.lines = content.splitlines()
        self.content_start_line = self._find_content_start()
        self.content_lines = self.lines[self.content_start_line:]
        self.content_text = '\n'.join(self.content_lines)

    def _find_content_start(self):
        """Return line index where markdown body starts (after frontmatter)."""
        if self.lines and self.lines[0].strip() == "---":
            for i in range(1, len(self.lines)):
                if self.lines[i].strip() == "---":
                    return i + 1
        return 0

    def add(self, line_no, severity, message):
        self.issues.append((line_no, severity, message))

    def check_horizontal_rules(self):
        """Detect --- in content (frontmatter delimiter is allowed at top)."""
        in_frontmatter = False
        frontmatter_closed = False
        for i, line in enumerate(self.lines, start=1):
            stripped = line.strip()
            if stripped == "---":
                if not frontmatter_closed:
                    in_frontmatter = not in_frontmatter
                    if not in_frontmatter:
                        frontmatter_closed = True
                    continue
                self.add(i, "ERROR", "Horizontal rule `---` found in content; will become a visible line in PDF")

    def check_straight_quotes(self):
        """Detect ASCII straight quotes used as Chinese quotes."""
        def is_cjk(ch):
            return '\u4e00' <= ch <= '\u9fff'

        in_code = False
        for idx, line in enumerate(self.content_lines, start=self.content_start_line + 1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            # Skip lines that are mostly LaTeX/math
            if line.count('$') >= 2:
                continue
            # Simple heuristic: straight quote adjacent to CJK character
            for j, ch in enumerate(line):
                if ch in '"\'':
                    prev_cjk = j > 0 and is_cjk(line[j - 1])
                    next_cjk = j < len(line) - 1 and is_cjk(line[j + 1])
                    if prev_cjk or next_cjk:
                        self.add(idx, "WARNING", "Possible straight quote used as Chinese quote; consider “”")
                        break

    def check_chinese_in_math(self):
        """Detect Chinese characters inside $...$ not wrapped in \\text{}."""
        # Split content by math delimiters
        parts = re.split(r'(?<!\$)\$(?!\$)', self.content_text)
        # Even-indexed parts are outside math, odd-indexed are inside math
        for idx in range(1, len(parts), 2):
            math_part = parts[idx]
            # Find Chinese chars not inside \text{...}
            cleaned = re.sub(r'\\text\{[^}]*\}', '', math_part)
            for ch in cleaned:
                if '\u4e00' <= ch <= '\u9fff':
                    marker = "$" + math_part + "$"
                    line_no = self._find_line(marker)
                    self.add(line_no, "ERROR", f"Chinese character '{ch}' inside math mode without \\text{{}}")
                    break

    def check_unicode_subscripts_superscripts(self):
        """Detect Unicode sub/sup characters that should be LaTeX."""
        sub_sup_pattern = re.compile(r'[\u00B2\u00B3\u2070-\u209F]+')
        for idx, line in enumerate(self.content_lines, start=self.content_start_line + 1):
            if sub_sup_pattern.search(line):
                self.add(idx, "WARNING", "Unicode subscript/superscript found; convert to LaTeX $_n$ / $^n$")

    def check_unicode_logic_symbols(self):
        """Detect Unicode logic symbols that should be LaTeX commands."""
        symbols = {
            '\u2227': '\\land', '\u2228': '\\lor', '\u00AC': '\\neg',
            '\u2192': '\\rightarrow', '\u2194': '\\leftrightarrow',
            '\u2200': '\\forall', '\u2203': '\\exists'
        }
        for idx, line in enumerate(self.content_lines, start=self.content_start_line + 1):
            for sym, replacement in symbols.items():
                if sym in line:
                    self.add(idx, "WARNING", f"Unicode logic symbol '{sym}' found; use `{replacement}`")

    def check_control_characters(self):
        """Detect control characters from corrupted LaTeX commands."""
        control_chars = {
            '\x07': 'BEL (\\a prefix, e.g. \\alpha)',
            '\x08': 'BS (\\b prefix, e.g. \\beta)',
            '\x0C': 'FF (\\f prefix, e.g. \\forall)',
            '\x0D': 'CR (\\r prefix, e.g. \\rightarrow)',
            '\x09': 'TAB (\\t prefix, e.g. \\theta)',
            '\x0B': 'VT (\\v prefix, e.g. \\varepsilon)',
        }
        for idx, line in enumerate(self.content_lines, start=self.content_start_line + 1):
            for char, desc in control_chars.items():
                if char in line:
                    self.add(idx, "ERROR", f"Control character {desc} detected; LaTeX command corrupted")

    def check_unclosed_math(self):
        """Detect odd number of single $ delimiters."""
        normal_math = re.sub(r'\$\$.*?\$\$', '', self.content_text, flags=re.DOTALL)
        count = normal_math.count('$')
        if count % 2 != 0:
            self.add(self._find_line('$'), "ERROR", f"Unclosed inline math mode: {count} $ delimiters (odd)")

    def check_table_cells(self):
        """Detect incomplete math mode in table cells (heuristic)."""
        in_table = False
        for idx, line in enumerate(self.content_lines, start=self.content_start_line + 1):
            if re.match(r'^\|.*\|$', line.strip()):
                in_table = True
                cells = line.strip().split('|')[1:-1]
                for cell in cells:
                    if cell.count('$') % 2 != 0:
                        self.add(idx, "ERROR", f"Table cell has unclosed math mode: {cell.strip()}")
            elif in_table and not line.strip().startswith('|'):
                in_table = False

    def check_adjacent_math(self):
        """Detect adjacent math modes like $x$$y$ or Cu$^2$$^+$."""
        for idx, line in enumerate(self.content_lines, start=self.content_start_line + 1):
            if re.search(r'\$\$+\S*\$\$+', line):
                self.add(idx, "WARNING", "Adjacent math modes detected; merge into single $...$")

    def _find_line(self, snippet):
        for i, line in enumerate(self.lines, start=1):
            if snippet in line:
                return i
        return 0

    def run_all(self):
        self.check_horizontal_rules()
        self.check_straight_quotes()
        self.check_chinese_in_math()
        self.check_unicode_subscripts_superscripts()
        self.check_unicode_logic_symbols()
        self.check_control_characters()
        self.check_unclosed_math()
        self.check_table_cells()
        self.check_adjacent_math()
        return self.issues

    def report(self):
        if not self.issues:
            print("No issues found.")
            return 0

        errors = [x for x in self.issues if x[1] == "ERROR"]
        warnings = [x for x in self.issues if x[1] == "WARNING"]

        for line_no, severity, message in sorted(self.issues, key=lambda x: (x[0], x[1])):
            print(f"Line {line_no:4d} [{severity:7s}] {message}")

        print(f"\nTotal: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Check exam-paper generated markdown for common issues")
    parser.add_argument("input", help="Path to markdown file")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(2)

    content = path.read_text(encoding="utf-8")
    checker = MarkdownChecker(content)
    checker.run_all()
    sys.exit(checker.report())


if __name__ == "__main__":
    main()
