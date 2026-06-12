---
name: exam-paper
description: Generate exam papers, study guides, review books, and teaching materials from any subject. Extracts and synthesizes user-provided materials, generates transfer-oriented questions, and outputs compact Markdown + PDF via Pandoc + ctexart + xelatex.
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
  - 跨学科
---

# Exam Paper & Teaching Material Generation Skill

Generate exam papers, practice tests, study guides, review books, and teaching materials from **any subject**. Works end-to-end: extract knowledge from user materials → synthesize → generate questions that encourage "举一反三" (transfer learning) → output compact MD + PDF.

This skill is **content-type centric**, not subject-list centric. Whether the input is chemistry formulas, historical essays, legal cases, medical symptoms, or engineering diagrams, follow the same workflow and apply the corresponding content-type rules below.

## When to use

- User provides reference materials and wants exam papers / practice questions / study guides / review books
- User asks to "提炼知识点出题" or "根据这份资料出几道题" or "生成复习全书"
- User wants teaching materials with detailed explanations + worked examples
- User needs compact, printable PDFs without page break lines
- User says "出一套xx试卷" or "根据xx内容整理讲义" or "写一本xx复习全书"

## When NOT to use

- User only wants a simple text list (no PDF needed)
- User provides a LaTeX `.tex` source file directly and only wants minor edits
- User explicitly asks for an interactive quiz / online test platform

## Workflow Overview

1. **Explore materials** — read user-provided files (PDF, DOCX, Markdown, images via OCR if needed). Identify the subject and scope.
2. **Extract & synthesize** — identify core knowledge points (考点), key formulas, common patterns, and exam traps.
3. **Design document structure** — choose document type (exam paper / study guide / review book / practice questions) and outline chapters/sections.
4. **Apply content-type rules** — decide which rules from this skill apply: formulas, tables, diagrams, code, multilingual text, citations/proofs, etc.
5. **Write markdown** — use proper YAML frontmatter, correct formula rendering, Chinese typography rules, and no page-break horizontal rules.
6. **Generate questions** — for each topic, create 基础题、变式题、综合题、开放题 with detailed answers.
7. **Compile PDF** — use pandoc + xelatex. Verify no rendering warnings/errors.
8. **Verify** — check PDF visually for formula display, layout, page breaks, orphan lines, and missing characters.

## Document Types

### Type A: Exam Paper (试卷)
- Purpose: simulate a real exam; compact and printable
- Layout: minimal title, no headers/footers/page numbers, 10.5–11pt, 2.0–2.5cm margins
- Content: instructions, multiple question types, answer key (optional, at end)
- Include reference data (constants, tables, terminology) if needed

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

**Critical:** ALL documents must include `\widowpenalty`, `\clubpenalty`, `\brokenpenalty` set to 10000 to prevent orphan/widow lines and unwanted page breaks. For Chinese documents, always set `mainfont` and `sansfont` to a CJK font such as Noto Serif CJK SC.

### Type E: English Document

For non-CJK documents, use a Latin font and the standard `article` class:

```yaml
---
title: "Calculus Final Review"
subtitle: "Example English Review Book"
fontsize: 11pt
documentclass: article
geometry: margin=2.2cm
colorlinks: true
header-includes: |
  \setlength{\emergencystretch}{3em}
  \linespread{1.2}
  \widowpenalty=10000
  \clubpenalty=10000
  \brokenpenalty=10000
  \usepackage{amsmath}
  \usepackage{amssymb}
  \usepackage{booktabs}
---
```

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

## Content-Type Rules (Universal)

Instead of memorizing per-subject rules, identify which content types appear in the material and apply the matching rules below.

### 1. Formulas and Symbols

- Always use LaTeX math mode for formulas, Greek letters, operators, subscripts, and superscripts.
- Common commands: `\alpha`, `\beta`, `\gamma`, `\theta`, `\sigma`, `\mu`, `\pi`, `\sum`, `\int`, `\prod`, `\frac`, `\sqrt`, `\lim`, `\infty`, `\pm`, `\times`, `\div`, `\leq`, `\geq`, `\neq`, `\approx`.
- Wrap Chinese text inside math mode with `\text{...}`.
- Convert Unicode subscripts/superscripts to LaTeX (e.g., H₂O → H$_2$O, x² → $x^2$).
- Avoid Unicode logic symbols (`∧`, `∨`, `¬`, `→`); use `\land`, `\lor`, `\neg`, `\rightarrow`.

**Example matrix**:

```latex
$$
\mathbf{A} = \begin{bmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{bmatrix}
$$
```

**Example piecewise function**:

```latex
$$
f(x) = \begin{cases} x, & x \geq 0 \\ 0, & x < 0 \end{cases}
$$
```

### 2. Tables and Comparisons

- Use markdown tables for comparisons, terminology mappings, and summary sheets.
- Ensure every cell containing math is fully wrapped in `$...$`.
- For very long tables, consider splitting or reducing font size in the frontmatter.
- Avoid multi-line content inside a single table cell; use separate rows instead.

**Example**:

```markdown
| 概念 | 定义 | 公式 |
|-----|------|------|
| 熵 | 系统不确定性的度量 | $H(X) = -\sum p_i \log p_i$ |
| 条件熵 | 已知 $Y$ 后 $X$ 的不确定性 | $H(X|Y) = -\sum p(x,y) \log p(x|y)$ |
```

### 3. Diagrams and Figures

You have three ways to include diagrams, depending on complexity:

1. **TikZ inside markdown** — best for simple geometry, arrows, trees, and anything that should stay vector in PDF.
2. **matplotlib helper script** — best for coordinate systems, force diagrams, bar/line charts, Venn diagrams, flowcharts, and triangles.
3. **External image** — for hand-drawn or complex figures, include with `![caption](path.png)`.

#### 3.1 TikZ in markdown

Use raw LaTeX blocks (works with `--from markdown+raw_tex`):

```latex
\begin{tikzpicture}
  \node (A) at (0,0) {A};
  \node (B) at (3,0) {B};
  \draw[->] (A) -- (B) node[midway,above] {$f$};
\end{tikzpicture}
```

More examples:

```latex
% Right triangle
\begin{tikzpicture}
  \draw (0,0) -- (4,0) -- (4,3) -- cycle;
  \node at (-0.2,-0.2) {A};
  \node at (4.2,-0.2) {B};
  \node at (4.2,3.2) {C};
\end{tikzpicture}
```

```latex
% Tree / hierarchy
\begin{tikzpicture}
  \node {Root}
    child {node {Left}}
    child {node {Right}};
\end{tikzpicture}
```

#### 3.2 Using the bundled matplotlib helper

The skill includes `tools/diagram_tools.py` with ready-to-use functions:

- `coordinate_system()`
- `function_plot()`
- `number_line()`
- `force_diagram()`
- `geometry_triangle()`
- `bar_chart()`
- `line_chart()`
- `scatter_plot()`
- `box_plot()`
- `probability_tree()`
- `venn_diagram()`
- `flowchart()`

Call them from your generation script:

```python
from tools.diagram_tools import (
    coordinate_system, function_plot, number_line,
    force_diagram, geometry_triangle,
    bar_chart, line_chart, scatter_plot, box_plot,
    probability_tree, venn_diagram, flowchart
)

# Example: coordinate system with points and segments
coordinate_system(
    points=[(1, 2), (-2, -1)],
    segments=[((0, 0), (1, 2))],
    labels={0: "P", 1: "Q"},
    output_path="output/diagram_coord.png"
)

# Example: function plot
function_plot(
    lambda x: x ** 2,
    x_range=(-3, 3),
    output_path="output/diagram_function.png",
    title=r"$y = x^2$"
)

# Example: number line
number_line(
    points=[-2, -1, 0, 1, 2],
    output_path="output/diagram_numberline.png"
)

# Example: free-body force diagram
force_diagram(
    forces=[
        {"x": 2, "y": 1, "label": "F1", "color": "red"},
        {"x": -1, "y": 2, "label": "F2", "color": "blue"},
    ],
    output_path="output/diagram_forces.png"
)

# Example: bar chart
bar_chart(
    categories=["A", "B", "C"],
    values=[10, 20, 15],
    output_path="output/diagram_bar.png",
    title="Sample Comparison"
)
```

Then embed the generated image in markdown:

```markdown
![坐标系示例](output/diagram_coord.png)
```

#### 3.3 External images

If the user provides images or you draw them elsewhere, embed normally:

```markdown
![受力分析图](images/force_diagram.png)
```

Keep image resolution at least 150 DPI for print quality.

### 4. Code and Pseudocode

- Use fenced code blocks with language identifier for actual code.
- For pseudocode, use numbered lists or plain code blocks without language tag.
- Ensure monospace fonts contain glyphs for any special Unicode used.

```markdown
```python
def foo(x):
    return x + 1
```
```

### 5. Multilingual and Specialized Text

- Classical Chinese, foreign language passages, legal articles, medical terminology: keep as normal text, but mark special terms with quotes or emphasis.
- For terminology lists, use tables with original term / definition / symbol columns.
- Romanize or transliterate where helpful, but preserve original characters for accuracy.

### 6. Theorems, Proofs, and Citations

- Use section headings or bold labels for theorems, lemmas, corollaries, and proofs.
- End proofs with a clear marker such as **证毕** or `\square` if in math mode.
- For citation-style references, use numbered lists or parenthetical notes.

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

## Quality Check

Before compiling, run `tools/quality_check.py` on your generated markdown to catch common mistakes early:

```bash
python tools/quality_check.py output/review.md
```

It checks for:
- Horizontal rules `---` in content
- Straight quotes used as Chinese quotes
- Chinese characters inside math mode without `\text{}`
- Unicode subscripts/superscripts not converted to LaTeX
- Unicode logic symbols (`∧`, `∨`, `¬`, etc.) not converted
- Control characters from corrupted LaTeX commands (e.g., `\forall` becoming form feed)
- Unclosed inline math mode
- Table cells with unclosed math mode
- Adjacent math modes that should be merged

A non-zero exit code is returned if any ERROR-level issue is found. Integrate this step into your generation pipeline:

```python
import subprocess
subprocess.run(["python", "tools/quality_check.py", "output/review.md"], check=True)
```

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

## Subject Adaptation Framework

This skill is designed to work with **any subject**. Use the following framework instead of looking up a fixed subject list.

### Step 1: Identify the dominant content types

Ask: what does this subject primarily use?
- Formulas and symbols
- Tables and comparisons
- Diagrams and figures
- Code and algorithms
- Long text passages
- Legal/medical/engineering cases
- Multilingual terminology

### Step 2: Apply the matching Content-Type Rules

Map each dominant content type to the rules in the "Content-Type Rules" section above.

### Step 3: Capture subject-specific conventions

Note down:
- Common symbols and notation
- Standard abbreviations
- Typical question formats
- Common traps or grading points
- Required reference data (constants, tables, terminology)

### Step 4: Generate and compile

Use the appropriate frontmatter, question templates, and compilation command.

### New Subject Quick-Start Template

When extending this skill to a new subject, fill in:

```markdown
## 学科名称

- 核心内容类型：公式 / 图表 / 代码 / 文本 / 病例 / 法条 / 工程图 / …
- 常用 LaTeX 宏包/命令：
- 典型题型：选择题 / 判断题 / 计算题 / 证明题 / 简答题 / 案例分析 / …
- 常见符号与约定：
- 易错排版点：
- 推荐 frontmatter 调整（如有）：
```

## Example Subject Snapshots

The following are **illustrative applications** of the framework, not an exhaustive subject list.

### Example A: Natural Sciences (Chemistry / Physics / Biology)
- Convert all Unicode subscripts/superscripts to LaTeX math mode
- Chemical equations: `H$_2$SO$_4$`, ion charges `Cu$^{2+}$`
- Reaction conditions: `$\xrightarrow{\text{点燃}}$`
- Units: `m/s$^2$`, `kg·m/s$^2$`
- Diagrams: molecular structures, force diagrams, cell diagrams via TikZ or matplotlib

### Example B: Mathematics
- Equations: `$x^2 + 2x - 3 = 0$`
- Functions: `$f(x) = \sin x$`
- Geometry: coordinates, angles, areas, TikZ diagrams
- Statistics: probability, distributions, data tables

### Example C: Humanities and Languages
- Long reading passages as plain text
- Terminology tables (term / definition / context)
- Classical text annotations
- Essay prompts with grading rubrics

### Example D: Social Sciences (Economics / Political Science / Sociology)
- Regression models and matrix notation in math mode
- Causal diagrams (DAGs) via TikZ
- Terminology and theory comparison tables
- Case-study questions with structured analysis

### Example E: Engineering and Computer Science
- Pseudocode and actual code blocks
- Algorithms with step-by-step examples
- Circuit diagrams, flowcharts, system architecture diagrams
- Mathematical modeling and unit analysis

### Example F: Medicine and Law
- Case-based questions with structured facts → analysis → conclusion
- Terminology tables with Latin/legal terms
- Diagnostic / legal reasoning flowcharts
- Citation of articles, clauses, or guidelines

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
| `\forall` becomes form feed | Normal-string `\f` escape | Use raw strings for LaTeX |

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
