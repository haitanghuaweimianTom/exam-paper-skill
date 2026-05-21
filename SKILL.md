---
name: exam-paper
description: Generate exam papers, study guides, practice tests, and teaching materials from any subject. Extracts and synthesizes user-provided materials, generates "举一反三" questions, outputs beautiful compact MD and PDF via Pandoc + ctexart + xelatex.
keywords:
  - exam-paper
  - 试卷
  - 出题
  - 讲义
  - 举一反三
  - 试卷排版
  - pandoc-exam
  - ctexart-exam
  - 知识提炼
---

# Exam Paper & Teaching Material Generation Skill

Generate exam papers, practice tests, study guides, and teaching materials from **any subject**. Works end-to-end: extract knowledge from user materials → synthesize → generate questions that encourage "举一反三" → output compact MD + PDF.

## When to use

- User provides reference materials and wants exam papers / practice questions / study guides
- User asks to "提炼知识点出题" or "根据这份资料出几道题"
- User wants teaching materials with detailed explanations + few examples
- User needs compact, printable PDFs without page break lines
- User says "出一套xx试卷" or "根据xx内容整理讲义"

## When NOT to use

- User only wants a simple text list (no PDF needed)
- User provides a LaTeX `.tex` source file directly

## Workflow Overview

1. **Extract & synthesize** — read user materials, identify core knowledge points, summarize key patterns
2. **Design questions** — generate questions that test understanding and encourage "举一反三" (not just memorization)
3. **Write markdown** — with proper YAML frontmatter, correct formula rendering, no page break lines
4. **Compile PDF** — pandoc + xelatex, verify no rendering issues
5. **Verify** — check PDF visually for formula display, layout, page breaks

## Document Types

This skill produces three types of documents:

### Type A: Exam Paper (试卷)
- No title needed (or minimal)
- Compact layout, no headers/footers/page numbers
- Multiple question types: choice, fill-in-blank, calculation, essay
- Include reference data (atomic masses, constants) if needed

### Type B: Study Guide / Teaching Material (讲义)
- Detailed knowledge explanation (知识梳理)
- 1-2 worked examples per topic (典例)
- "举一反三引导" section with thought-provoking questions
- No horizontal rules (---) — they become page break lines in PDF
- Tables for comparison/summary

### Type C: Practice Questions Only (纯题)
- Questions only, no explanations
- Ultra-compact: 8-9pt font, 1.2cm margins
- Grouped by topic
- Fits many questions in minimal pages

## Markdown Frontmatter

### Type A: Exam Paper

```yaml
---
documentclass: ctexart
geometry: margin=2.5cm,top=2cm,bottom=2cm
fontsize: 11pt
header-includes: |
  \setlength{\emergencystretch}{3em}
  \pagestyle{empty}
  \widowpenalty=10000
  \clubpenalty=10000
  \brokenpenalty=10000
  \usepackage{enumitem}
  \setlist[enumerate]{nosep}
  \setlength{\parskip}{0.3em}
  \setlength{\parindent}{0pt}
  \usepackage{booktabs}
  \usepackage{amsmath}
  \usepackage{graphicx}
---
```

### Type B: Study Guide / Teaching Material

```yaml
---
title: "标题"
fontsize: 10.5pt
documentclass: ctexart
geometry: margin=2.2cm
colorlinks: true
header-includes: |
  \setlength{\emergencystretch}{3em}
  \linespread{1.2}
  \setlength{\tabcolsep}{3pt}
  \renewcommand{\arraystretch}{1.05}
  \widowpenalty=10000
  \clubpenalty=10000
  \brokenpenalty=10000
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Serif CJK SC"
---
```

### Type C: Practice Questions Only (Ultra-Compact)

```yaml
---
fontsize: 8.5pt
documentclass: ctexart
geometry: margin=1.2cm
header-includes: |
  \setlength{\emergencystretch}{3em}
  \linespread{1.05}
  \setlength{\parindent}{0pt}
  \setlength{\parskip}{0.05em}
  \setlength{\tabcolsep}{2pt}
  \renewcommand{\arraystretch}{1.0}
  \widowpenalty=10000
  \clubpenalty=10000
---
```

**Critical:** ALL documents must include `\widowpenalty`, `\clubpenalty`, `\brokenpenalty` set to 10000 to prevent orphan/widow lines and unwanted page breaks.

## CRITICAL: NO Horizontal Rules

**NEVER use `---` (three dashes) in markdown content.** Pandoc converts `---` to a horizontal rule which becomes a page break line in the PDF. Use blank lines or section headers to separate content instead.

## Text Rendering Rules

### 1. Unicode Superscript/Subscript Conversion

**ALL Unicode superscript/subscript characters MUST be converted to LaTeX math mode.** Never leave them as raw Unicode — they will render as squares/blocks in the PDF.

Conversion map:

| Unicode | LaTeX | Example |
|---------|-------|---------|
| ₀-₉ (U+2080-2089) | `$_n$` | O₂ → O$_2$ |
| ² (U+00B2) | `$^2$` | Cu²⁺ → Cu$^{2+}$ |
| ³ (U+00B3) | `$^3$` | Fe³⁺ → Fe$^{3+}$ |
| ⁺ (U+207A) | `$^+$` | Ag⁺ → Ag$^+$ |
|  (U+207B) | `$^-$` | Cl⁻ → Cl$^-$ |
| ⁰-⁹ (U+2070-2079) | `$^n$` | CO₃²⁻ → CO$_3^{2-}$ |

**Combined superscripts/subscripts:** Write as a single math mode expression:
- Cu²⁺ → `Cu$^{2+}$` (NOT `Cu$^2$$^+$`)
- SO₄²⁻ → `SO$_4^{2-}$` (NOT `SO$_4$$^{2-}$`)
- CO²⁻ → `CO$_3^{2-}$`
- HCO₃ → `HCO$_3^-$`
- Fe³⁺ → `Fe$^{3+}$`
- OH⁻ → `OH$^-$`
- NH₄⁺ → `NH$_4^+$`

### 2. Chinese Quotes

**NEVER use `"` or `"` for Chinese quotes.** They render incorrectly in LaTeX. Use full-width Chinese corner quotes:

| Wrong | Correct |
|-------|---------|
| "特征反应" | 「特征反应」 |
| "三看" | 「三看」 |
| "远距离先反应" | 「远距离先反应」 |

### 3. Subscripts/Superscripts in Tables

When subscripts/superscripts appear in markdown tables, ensure each cell's math mode is complete:

```markdown
| CO$_3^{2-}$ | BaCl$_2$ 溶液 | 白色沉淀 |
```

NOT: `| CO^{2-}$ |` (missing opening `$` and subscript)

## Compilation Command

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex --shift-heading-level-by=0
```

## Question Generation Principles

### Extract & Synthesize Knowledge

When user provides reference materials:
1. Read ALL materials first
2. Identify core knowledge points (考点)
3. Summarize key patterns and rules
4. Note common mistakes and exam traps

### Design "举一反三" Questions

Questions should NOT just test memorization. They should guide students to:
- **Transfer knowledge**: Apply learned patterns to new situations
- **Compare and contrast**: Identify similarities/differences between similar concepts
- **Analyze conditions**: What changes if a variable changes?
- **Multiple approaches**: Solve the same problem using different methods

### Question Variety

For each knowledge point, generate questions of varying difficulty:
- **基础题**: Direct application of learned rules
- **变式题**: Same concept, different context/presentation
- **综合题**: Combining multiple knowledge points
- **开放题**: "如果…会怎样？" encouraging deeper thinking

### Example: "举一反三" Question Sets

For a chemistry topic on metal displacement:

1. **Direct**: Fe + CuSO → ? (basic substitution)
2. **Variant**: Zn + AgNO₃ → ? (different metals, same pattern)
3. **Multi-step**: Zn added to Cu(NO)₂ + AgNO₃ mixture → filter residue?
4. **Reverse reasoning**: Given residue composition, what was added?
5. **Real-world**: Why can't iron pots store copper sulfate solution?

Guiding questions for students:
- "如果换成铁粉而不是锌粉，结论有何不同？"
- "滤液滤渣问题中，'一定'和'可能'的区别是什么？"

## Post-Compilation Checklist

1. **Read PDF visually** — check formula rendering, layout
2. **Check for missing Unicode** — any squares/blocks mean unconverted subscripts
3. **Check math mode** — `Cu$^{2+}$` not `Cu$^2$$^+$`, `CO$_3^{2-}$` not `CO$_3$$^{2-}$`
4. **Check tables** — all cells properly formatted
5. **Check quotes** — no `"` or `"`, only `「」`
6. **Check page breaks** — no `---` horizontal rules
7. **Recompile if needed**

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Chemical formula shows as square | Unicode sub/sup not converted | Convert to `$_n$` and `$^n$` |
| Cu$^2$$^+$ appears as two separate | Adjacent math modes | Merge: `Cu$^{2+}$` |
| CO$_3$^{2-}$ broken | Split sub/sup | Merge: `CO$_3^{2-}$` |
| Table cells misaligned | Missing math mode delimiters | Ensure each cell's formula is complete |
| Chinese quotes look wrong | Using `"` or `"` | Use `「」` |
| Page break lines appear | `---` in markdown | Remove all `---` |
| Widow/orphan lines | No penalty settings | Add `\widowpenalty=10000` etc. |
| Text overflow on right | Long Chinese sentences | `emergencystretch=3em` |

## Subject Adaptations

### Chemistry
- Chemical equations with proper subscripts: `$\text{H}_2\text{SO}_4$` or `H$_2$SO$_4$`
- Ion charges: `Cu$^{2+}$`, `SO$_4^{2-}$`
- Reaction conditions: `$\xrightarrow{\text{点燃}}$`, `$\xrightarrow{\triangle}$`
- Gas/precipitate symbols: `↑` `↓` (keep as Unicode)
- Knowledge guide topics: metal activity, acid-base-salt, gas preparation, mass conservation

### Physics
- Units: `m/s$^2$`, `kg·m/s$^2$`, `10$^3$ Pa`
- Circuit: use matplotlib for diagrams
- Force diagrams: vector arrows, free-body diagrams
- Formulas: `$F = ma$`, `$E = mc^2$`

### Biology
- Cell organelles, DNA structure
- Genetics: Punnett squares, heredity patterns
- Ecosystem: food chains, energy pyramids

### Math
- Equations: `$x^2 + 2x - 3 = 0$`
- Functions: `$f(x) = \sin x$`
- Geometry: coordinates, angles, areas
- Statistics: probability, data analysis

### English
- Reading comprehension passages
- Grammar exercises (tense, voice, clauses)
- Vocabulary: context-based questions
- Writing: essay prompts with structure guides

### Chinese (Language)
- Classical Chinese reading comprehension
- Poetry analysis (意象, 手法, 情感)
- Essay writing (议论文, 记叙文)
- Language usage: 病句修改, 词语辨析
