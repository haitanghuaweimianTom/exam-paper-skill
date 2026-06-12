---
name: exam-paper
description: Generate exam papers, study guides, practice tests, and teaching materials from any subject. Extracts and synthesizes user-provided materials, generates "举一反三" questions, outputs beautiful compact MD and PDF via Pandoc + ctexart + xelatex.
keywords:
  - exam-paper
  - 试卷
  - 出题
  - 讲义
  - 复习全书
  - 举一反三
  - 试卷排版
  - pandoc-exam
  - ctexart-exam
  - 知识提炼
  - xelatex
---

# Exam Paper & Teaching Material Generation Skill

Generate exam papers, practice tests, study guides, review books, and teaching materials from **any subject**. Works end-to-end: extract knowledge from user materials → synthesize → generate questions that encourage "举一反三" → output compact MD + PDF.

## When to use

- User provides reference materials and wants exam papers / practice questions / study guides / review books
- User asks to "提炼知识点出题" or "根据这份资料出几道题" or "生成复习全书"
- User wants teaching materials with detailed explanations + worked examples
- User needs compact, printable PDFs without page break lines
- User says "出一套xx试卷" or "根据xx内容整理讲义" or "写一本xx复习全书"

## When NOT to use

- User only wants a simple text list (no PDF needed)
- User provides a LaTeX `.tex` source file directly and only wants minor edits
- User explicitly asks for interactive quiz / online test platform

## Workflow Overview

1. **Explore materials** — read user-provided files (PDF, DOCX, Markdown, images via OCR if needed). Identify the subject and scope.
2. **Extract & synthesize** — identify core knowledge points (考点), key formulas, common patterns, and exam traps.
3. **Design document structure** — choose document type (exam paper / study guide / review book / practice questions) and outline chapters/sections.
4. **Write markdown** — use proper YAML frontmatter, correct formula rendering, Chinese typography rules, and no page-break horizontal rules.
5. **Generate questions** — for each topic, create 基础题、变式题、综合题、开放题 with detailed answers.
6. **Compile PDF** — use pandoc + xelatex. Verify no rendering warnings/errors.
7. **Verify** — check PDF visually for formula display, layout, page breaks, orphan lines, and missing characters.

## Document Types

### Type A: Exam Paper (试卷)
- Purpose: simulate a real exam; compact and printable
- Layout: minimal title, no headers/footers/page numbers, 10.5–11pt, 2.0–2.5cm margins
- Content: instructions, multiple question types, answer key (optional, at end)
- Include reference data (constants, tables) if needed

### Type B: Study Guide / Teaching Material (讲义)
- Purpose: systematic learning material
- Layout: title page, chapter headings, 10.5pt, 2.2cm margins
- Content: 知识梳理 + 1–2 worked examples per topic + "举一反三引导" questions
- Use comparison tables and formula boxes

### Type C: Review Book (复习全书)
- Purpose: comprehensive end-of-term / exam-prep reference
- Layout: title page, multi-chapter, 10.5pt, 2.2cm margins
- Content: theory summary + examples (choice / T-F / calculation / proof / short answer) + detailed solutions
- Each chapter should be self-contained but coherent

### Type D: Practice Questions Only (纯题)
- Purpose: maximize question density for drilling
- Layout: 8.5–9pt, 1.2–1.5cm margins, minimal explanations
- Content: questions grouped by topic; answers in separate file or at end

## Markdown Frontmatter Templates

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
  \usepackage{amssymb}
  \usepackage{graphicx}
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Serif CJK SC"
---
```

### Type B/C: Study Guide / Review Book

```yaml
---
title: "学科名 期末复习全书（详细版）"
subtitle: "Subtitle"
fontsize: 10.5pt
documentclass: ctexart
geometry: margin=2.2cm
colorlinks: true
header-includes: |
  \setlength{\emergencystretch}{3em}
  \linespread{1.25}
  \setlength{\tabcolsep}{3pt}
  \renewcommand{\arraystretch}{1.05}
  \widowpenalty=10000
  \clubpenalty=10000
  \brokenpenalty=10000
  \usepackage{amsmath}
  \usepackage{amssymb}
  \usepackage{booktabs}
  \usepackage{tikz}
  \usetikzlibrary{calc,positioning}
  \usepackage{tcolorbox}
  \tcbuselibrary{skins,breakable}
  \renewenvironment{quote}{\begin{tcolorbox}[colback=blue!3!white,colframe=blue!40!black,boxrule=0.4pt,arc=1.5mm,breakable,left=2mm,right=2mm,top=1mm,bottom=1mm]}{\end{tcolorbox}}
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Serif CJK SC"
---
```

### Type D: Practice Questions Only (Ultra-Compact)

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
  \brokenpenalty=10000
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Serif CJK SC"
---
```

**Critical:** ALL documents must include `\widowpenalty`, `\clubpenalty`, `\brokenpenalty` set to 10000 to prevent orphan/widow lines and unwanted page breaks. Always set `mainfont` and `sansfont` to a CJK font such as Noto Serif CJK SC.

## CRITICAL: NO Horizontal Rules

**NEVER use `---` (three dashes) in markdown content.** Pandoc converts `---` to a horizontal rule which becomes a visible line / page break in the PDF. Use blank lines or section headers to separate content instead.

Exception: the YAML frontmatter at the very top of the file, which is delimited by `---`.

## Chinese Typography Rules

### 1. Chinese Quotes

**NEVER use straight ASCII `"` or `'` for Chinese quotes.** They render incorrectly and may be interpreted as math mode delimiters.

Use full-width Chinese quotes:

| Wrong | Correct |
|-------|---------|
| "特征反应" | “特征反应” |
| "三看" | “三看” |
| "远距离先反应" | “远距离先反应” |

### 2. Dashes and Ellipsis

| Wrong | Correct | Notes |
|-------|---------|-------|
| --    | ——      | Chinese em dash (U+2014 U+2014) |
| ...   | ……      | Chinese ellipsis |

### 3. Punctuation in Math Mode

Chinese punctuation inside math mode may cause font warnings. Keep punctuation such as `，`、`。`、`；` outside `$...$`. For example:

- Wrong: `$x = 1。$`
- Correct: `$x = 1$。`

## Text and Formula Rendering Rules

### 1. Unicode Superscript/Subscript Conversion

**ALL Unicode superscript/subscript characters MUST be converted to LaTeX math mode.** Never leave them as raw Unicode — they will render as squares/blocks in the PDF.

Conversion map:

| Unicode | LaTeX | Example |
|---------|-------|---------|
| ₀-₉ (U+2080-2089) | `$_n$` | O₂ → O$_2$ |
| ² (U+00B2) | `$^2$` | Cu²⁺ → Cu$^{2+}$ |
| ³ (U+00B3) | `$^3$` | Fe³⁺ → Fe$^{3+}$ |
| ⁺ (U+207A) | `$^+$` | Ag⁺ → Ag$^+$ |
| ⁻ (U+207B) | `$^-$` | Cl⁻ → Cl$^-$ |
| ⁰-⁹ (U+2070-2079) | `$^n$` | CO₃²⁻ → CO$_3^{2-}$ |

**Combined superscripts/subscripts:** Write as a single math mode expression:
- Cu²⁺ → `Cu$^{2+}$` (NOT `Cu$^2$$^+$`)
- SO₄²⁻ → `SO$_4^{2-}$` (NOT `SO$_4$$^{2-}$`)
- CO₃²⁻ → `CO$_3^{2-}$`
- HCO₃⁻ → `HCO$_3^-$`
- Fe³⁺ → `Fe$^{3+}$`
- OH⁻ → `OH$^-$`
- NH₄⁺ → `NH$_4^+$`

### 2. Chinese Characters Inside Math Mode

When Chinese text appears inside `$...$`, wrap it with `\text{...}`. Otherwise xelatex will try to render Chinese with the math font and emit `Missing character in font latinmodern-math` warnings.

| Wrong | Correct |
|-------|---------|
| `$\{有毛, 吃草, 黑条纹\}$` | `$\{\text{有毛}, \text{吃草}, \text{黑条纹}\}$` |
| `$P(是)$` | `$P(\text{是})$` |
| `$\xrightarrow{点燃}$` | `$\xrightarrow{\text{点燃}}$` |

### 3. Unicode Logic Symbols

Avoid Unicode logic symbols such as `∧` (U+2227), `∨` (U+2228), `¬` (U+00AC), `→` (U+2192) inside code blocks or plain text where the monospace font may lack glyphs. Use LaTeX commands instead:

| Unicode | LaTeX |
|---------|-------|
| ∧ | `\land` or `\wedge` |
| ∨ | `\lor` or `\vee` |
| ¬ | `\neg` |
| → | `\rightarrow` or `\Rightarrow` |
| ↔ | `\leftrightarrow` |
| ∀ | `\forall` |
| ∃ | `\exists` |

### 4. Subscripts/Superscripts in Tables

When subscripts/superscripts appear in markdown tables, ensure each cell's math mode is complete:

```markdown
| CO$_3^{2-}$ | BaCl$_2$ 溶液 | 白色沉淀 |
```

NOT: `| CO^{2-}$ |` (missing opening `$` and subscript)

## Python Raw-String Traps When Generating Markdown

If you generate markdown content using Python raw strings (`r"..."`), remember that a literal `\n` in the raw string is two characters (backslash + n), NOT a newline. You must convert it to a real newline before writing the file. **However**, naive replacement will destroy LaTeX commands that start with `\n`.

### Safe conversion pattern

```python
# Protect LaTeX commands that start with \n before converting \n to newline
content = content.replace('\\newpage', '__NEWPAGE__')
content = content.replace('\\neq', '__NEQ__')
content = content.replace('\\neg', '__NEG__')
content = content.replace('\\ni', '__NI__')
content = content.replace('\\n', '\n')
content = content.replace('__NEWPAGE__', '\\newpage')
content = content.replace('__NEQ__', '\\neq')
content = content.replace('__NEG__', '\\neg')
content = content.replace('__NI__', '\\ni')
```

Also protect any other `\` command you use that begins with `n`.

### Even bigger trap: Python escape sequences in LaTeX commands

In **normal** Python strings (not raw), backslash + one of `a b f n r t v` is interpreted as a control character. This corrupts many common LaTeX commands:

| LaTeX command | Corrupted to | Result in PDF |
|---------------|--------------|---------------|
| `\forall` | form feed (`\f`) + `orall` | `Missing $ inserted` |
| `\rightarrow` | carriage return (`\r`) + `ightarrow` | math error |
| `\theta` | tab (`\t`) + `heta` | weird spacing / error |
| `\times` | tab (`\t`) + `imes` | weird spacing / error |
| `\text{...}` | tab (`\t`) + `ext{...}` | error |
| `\alpha` | bell (`\a`) + `lpha` | invisible / error |
| `\beta` | backspace (`\b`) + `eta` | invisible / error |
| `\frac` | form feed (`\f`) + `rac` | error |

**Rule of thumb**: any Python string that will contain LaTeX commands should be a **raw string** (`r"..."` or `r"""..."""`). If you must use a normal string, double every backslash: `\\forall`, `\\rightarrow`, etc.

**Recommended pattern**: build chapter content with `r"""..."""` and make helper-function arguments raw strings as well:

```python
def ex_choice(q, opts, ans, expl):
    return f"{box('例题·选择题', q)}\n\n{opts}\n\n{box('答案与解析', f'**答案：{ans}**\\n\\n{expl}')}\n"

ex_choice(
    r"将公式 $(\forall x)(P(x) \rightarrow Q(x))$ 化为子句集。",
    r"A. ...\n\nB. ...",
    r"B",
    r"解析中使用 $\forall$、$\rightarrow$ 等命令。"
)
```

## Compilation Commands

### Basic command

```bash
pandoc input.md -o output.pdf --pdf-engine=xelatex
```

### Recommended command for Chinese documents with math

```bash
pandoc input.md -o output.pdf \
  --from markdown+raw_tex \
  --pdf-engine=xelatex \
  -V CJKmainfont="Noto Serif CJK SC" \
  -V mainfont="Noto Serif CJK SC" \
  -V sansfont="Noto Serif CJK SC" \
  --variable geometry:margin=2.2cm \
  --variable fontsize=10.5pt
```

### Verbose debugging command

```bash
pandoc input.md -o output.pdf \
  --from markdown+raw_tex \
  --pdf-engine=xelatex \
  --verbose \
  2>&1 | tee pandoc.log
```

Always inspect `pandoc.log` for `Missing character` or `Undefined control sequence` warnings.

## Question Type Templates

Use the following markdown structures to keep questions and answers visually distinct. The review-book frontmatter turns `quote` blocks into light-blue example boxes.

### Multiple Choice

```markdown
> **【例题·选择题】**
>
> 题干内容……

A. 选项一

B. 选项二

C. 选项三

D. 选项四

> **【答案与解析】**
>
> **答案：C**
>
> 解析内容……
```

### True / False

```markdown
> **【例题·判断题】**
>
> 题干内容……

> **【答案与解析】**
>
> **答案：错误**
>
> 解析内容……
```

### Calculation / Proof

```markdown
> **【例题·计算/证明题】**
>
> 题干内容……

> **【答案与解析】**
>
> 详细解答步骤……
```

### Short Answer

```markdown
> **【例题·简答题】**
>
> 题干内容……

> **【答案与解析】**
>
> 简明扼要的答案……
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

1. **Direct**: Fe + CuSO₄ → ? (basic substitution)
2. **Variant**: Zn + AgNO₃ → ? (different metals, same pattern)
3. **Multi-step**: Zn added to Cu(NO₃)₂ + AgNO₃ mixture → filter residue?
4. **Reverse reasoning**: Given residue composition, what was added?
5. **Real-world**: Why can't iron pots store copper sulfate solution?

Guiding questions for students:
- "如果换成铁粉而不是锌粉，结论有何不同？"
- "滤液滤渣问题中，'一定'和'可能'的区别是什么？"

## Post-Compilation Checklist

1. **Read PDF visually** — check formula rendering, layout, page breaks
2. **Check for missing Unicode** — any squares/blocks mean unconverted subscripts or logic symbols
3. **Check math mode** — `Cu$^{2+}$` not `Cu$^2$$^+$`, `CO$_3^{2-}$` not `CO$_3$$^{2-}$`
4. **Check Chinese in math** — wrap with `\text{...}` when necessary
5. **Check tables** — all cells properly formatted
6. **Check quotes** — no straight `"`, only `“”`
7. **Check page breaks** — no `---` horizontal rules in content
8. **Recompile if needed**

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| Chemical formula shows as square | Unicode sub/sup not converted | Convert to `$_n$` and `$^n$` |
| Cu$^2$$^+$ appears as two separate | Adjacent math modes | Merge: `Cu$^{2+}$` |
| CO$_3$^{2-}$ broken | Split sub/sup | Merge: `CO$_3^{2-}$` |
| `Missing character in font latinmodern-math` | Chinese in math mode | Wrap with `\text{...}` |
| Unicode `∧` / `∨` shows as square | Monospace font lacks glyph | Use `\land` / `\lor` |
| Table cells misaligned | Missing math mode delimiters | Ensure each cell's formula is complete |
| Chinese quotes look wrong | Using `"` | Use `“”` |
| Page break lines appear | `---` in markdown | Remove all content `---` |
| Widow/orphan lines | No penalty settings | Add `\widowpenalty=10000` etc. |
| Text overflow on right | Long Chinese sentences | `\emergencystretch=3em` |
| `\neg` rendered as `eg` | Raw string `\n` replacement | Protect `\neg` before converting `\n` |

## Subject Adaptations

### Chemistry
- Chemical equations with proper subscripts: `$\text{H}_2\text{SO}_4$` or `H$_2$SO$_4$`
- Ion charges: `Cu$^{2+}$`, `SO$_4^{2-}$`
- Reaction conditions: `$\xrightarrow{\text{点燃}}$`, `$\xrightarrow{\triangle}$`
- Gas/precipitate symbols: `↑` `↓` (keep as Unicode)
- Knowledge guide topics: metal activity, acid-base-salt, gas preparation, mass conservation

### Physics
- Units: `m/s$^2$`, `kg·m/s$^2$`, `10$^3$ Pa`
- Circuit: use matplotlib or TikZ for diagrams
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

### Economics / Econometrics
- Regression models: always use math mode for equations, e.g. `$y_i = \beta_0 + \beta_1 x_i + u_i$`
- Matrix notation: `$\hat{\boldsymbol{\beta}} = (\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'\mathbf{y}$`
- Greek letters: `\beta`, `\sigma`, `\alpha`, `\delta` (LaTeX commands)
- OLS assumptions: label as MLR.1~MLR.6 or SLR.1~SLR.5
- Hypothesis tests: write t-stat and F-stat formulas explicitly
- Panel data: use double subscripts `$y_{it}$`, fixed effects `$a_i$`
- Difference-in-Differences: clearly write interaction term `$Post_t \times Treat_i$`
- Heteroskedasticity: mention robust SE, BP test, White test, WLS/FGLS
- Key topics: OLS derivation, BLUE/Gauss-Markov, consistency, asymptotic normality, omitted variable bias, dummy variables, LPM, heteroskedasticity, panel data (FD, FE, DiD)
- Exam style: closed-book, 90–100 min, 100 points; mix of proofs, calculations, and applied analysis

### Game Theory
- Represent games in normal form: `$G = \{N, (S_i), (u_i)\}$`
- Use payoff matrices in markdown tables; ensure math symbols are in `$...$`
- Key concepts: Nash equilibrium, dominant strategy, mixed strategy, subgame perfect equilibrium, Bayesian Nash equilibrium, perfect Bayesian equilibrium
- Common solution methods: underline best responses, iterative deletion of dominated strategies, backward induction
- Typical questions: find pure/mixed strategy Nash equilibria, solve extensive-form games, auction/game design, bargaining models

### Artificial Intelligence
- Knowledge representation: predicates, production rules, frames, semantic networks, knowledge graphs
- Deterministic reasoning: natural deduction, resolution, clause sets
- Uncertain reasoning: Bayes formula, CF method, fuzzy sets, Bayesian networks
- Search: BFS, DFS, A\*, Minimax, alpha-beta pruning
- Machine learning: supervised/unsupervised/reinforcement learning, overfitting/underfitting, evaluation metrics, decision trees, SVM, naive Bayes, K-Means
- Neural networks: perceptron, activation functions, backpropagation, CNN, RNN, Transformer
- When writing formulas, wrap Chinese labels with `\text{...}` and protect `\neg`, `\neq`, `\newpage` from raw-string conversion

## Output Directory Convention

- Place generated markdown and PDF under an `output/` subdirectory of the current project folder.
- Use descriptive filenames in Chinese, e.g. `计量经济学_期末复习全书.pdf`, `博弈论_模拟试卷_一.pdf`.
- Keep intermediate markdown files for debugging: `output/review.md`, `output/exam.md`.

## Complete Workflow Example

User request: "根据课件和复习资料生成人工智能期末复习全书，包含例题与解答，并输出 PDF。"

Agent steps:
1. List files in `课件/`, `课件提取文本/`, `复习资料/` to understand scope.
2. Determine chapters based on course syllabus (e.g., 绪论、知识表示、确定性推理、不确定性推理、搜索、机器学习、神经网络、附录).
3. Generate markdown with review-book frontmatter.
4. For each chapter:
   - Write theory summary in Chinese.
   - Add 1–2 examples per key concept using the question templates.
   - Ensure all math-mode Chinese uses `\text{...}`.
5. Convert literal `\n` to newlines safely (protect `\neg`, `\neq`, `\newpage`).
6. Compile with pandoc + xelatex.
7. Inspect log for `Missing character` warnings; fix any issues.
8. Report the generated PDF path to the user.
