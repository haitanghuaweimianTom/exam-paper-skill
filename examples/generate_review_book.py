#!/usr/bin/env python3
"""Example: generate a short review book with theory + examples."""

import os
import subprocess

OUTPUT_DIR = "output"
MD_PATH = os.path.join(OUTPUT_DIR, "example_review.md")
PDF_PATH = os.path.join(OUTPUT_DIR, "example_review.pdf")


def box(title, content):
    content = content.rstrip().replace('\n', '\n> ')
    return f"> **【{title}】**\n>\n> {content}\n"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = r"""---
title: "示例学科期末复习全书"
subtitle: "A Short Review Book Example"
fontsize: 10.5pt
documentclass: ctexart
geometry: margin=2.2cm
colorlinks: true
header-includes: |
  \setlength{\emergencystretch}{3em}
  \linespread{1.25}
  \widowpenalty=10000
  \clubpenalty=10000
  \brokenpenalty=10000
  \usepackage{amsmath}
  \usepackage{amssymb}
  \usepackage{booktabs}
  \usepackage{tcolorbox}
  \tcbuselibrary{skins,breakable}
  \renewenvironment{quote}{\begin{tcolorbox}[colback=blue!3!white,colframe=blue!40!black,boxrule=0.4pt,arc=1.5mm,breakable,left=2mm,right=2mm,top=1mm,bottom=1mm]}{\end{tcolorbox}}
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Serif CJK SC"
---

# 第一章 导数及其应用

## 1.1 导数的定义

函数 $f(x)$ 在 $x_0$ 处的导数定义为：

$$f'(x_0) = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}$$

几何意义：切线的斜率。

""" + box("例题·计算题", r"""求函数 $f(x) = x^2$ 在 $x = 1$ 处的导数。""") + r"""

""" + box("答案与解析", r"""根据导数定义：

$$f'(1) = \lim_{\Delta x \to 0} \frac{(1 + \Delta x)^2 - 1^2}{\Delta x} = \lim_{\Delta x \to 0} (2 + \Delta x) = 2$$

因此 $f'(1) = 2$。""") + r"""

## 1.2 常见导数公式

| 函数 | 导数 |
|------|------|
| $C$（常数） | $0$ |
| $x^n$ | $n x^{n-1}$ |
| $\sin x$ | $\cos x$ |
| $\cos x$ | $-\sin x$ |
| $e^x$ | $e^x$ |
| $\ln x$ | $\frac{1}{x}$ |

""" + box("例题·选择题", r"""下列函数中，导数为 $\cos x$ 的是（ ）

A. $\sin x$   B. $\cos x$   C. $-\sin x$   D. $\tan x$""") + r"""

""" + box("答案与解析", r"""**答案：A**

因为 $(\sin x)' = \cos x$，所以选 A。""") + r"""
"""

    # Protect LaTeX commands starting with \n
    content = content.replace('\\newpage', '__NEWPAGE__')
    content = content.replace('\\neg', '__NEG__')
    content = content.replace('\\neq', '__NEQ__')
    content = content.replace('\\n', '\n')
    content = content.replace('__NEWPAGE__', '\\newpage')
    content = content.replace('__NEG__', '\\neg')
    content = content.replace('__NEQ__', '\\neq')

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    cmd = [
        "pandoc", MD_PATH,
        "-o", PDF_PATH,
        "--from", "markdown+raw_tex",
        "--pdf-engine=xelatex",
        "-V", "CJKmainfont=Noto Serif CJK SC",
        "-V", "mainfont=Noto Serif CJK SC",
        "-V", "sansfont=Noto Serif CJK SC",
    ]
    subprocess.run(cmd, check=True)
    print(f"Review book generated: {PDF_PATH}")


if __name__ == "__main__":
    main()
