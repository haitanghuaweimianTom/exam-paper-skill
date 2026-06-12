#!/usr/bin/env python3
"""Example: generate a compact exam paper with mixed question types."""

import os
import subprocess

OUTPUT_DIR = "output"
MD_PATH = os.path.join(OUTPUT_DIR, "example_exam.md")
PDF_PATH = os.path.join(OUTPUT_DIR, "example_exam.pdf")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = r"""---
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
mainfont: "Noto Serif CJK SC"
sansfont: "Noto Serif CJK SC"
---

**考试时间：90 分钟　　满分：100 分**

## 一、选择题（每题 5 分，共 20 分）

1. 下列函数中，导数为 $f'(x) = 2x$ 的是（ ）

A. $f(x) = x$   B. $f(x) = x^2$   C. $f(x) = 2x$   D. $f(x) = \ln x$

2. 集合 $A = \{1, 2, 3\}$，$B = \{2, 3, 4\}$，则 $A \cap B =$（ ）

A. $\{1\}$　　B. $\{2, 3\}$　　C. $\{4\}$　　D. $\{1, 2, 3, 4\}$

## 二、填空题（每题 5 分，共 20 分）

3. 若 $x^2 - 5x + 6 = 0$，则 $x =$ __________。

4. 向量 $\vec{a} = (1, 2)$ 与 $\vec{b} = (2, -1)$ 的数量积为 __________。

## 三、计算题（共 30 分）

5. （15 分）求函数 $f(x) = x^3 - 3x^2 + 2$ 的极值。

6. （15 分）已知等差数列 $\{a_n\}$ 中 $a_1 = 2$，$d = 3$，求前 10 项和 $S_{10}$。

## 参考答案

1. B　　2. B

3. $2$ 或 $3$

4. $0$

5. $f'(x) = 3x^2 - 6x = 3x(x - 2)$，令 $f'(x) = 0$ 得 $x = 0$ 或 $x = 2$。极大值 $f(0) = 2$，极小值 $f(2) = -2$。

6. $S_{10} = 10a_1 + \frac{10 \times 9}{2}d = 20 + 135 = 155$。
"""

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
    print(f"Exam generated: {PDF_PATH}")


if __name__ == "__main__":
    main()
