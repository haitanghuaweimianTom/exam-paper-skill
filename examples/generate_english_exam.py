#!/usr/bin/env python3
"""Example: generate an English-language exam paper."""

import os
import subprocess

OUTPUT_DIR = "output"
MD_PATH = os.path.join(OUTPUT_DIR, "example_english_exam.md")
PDF_PATH = os.path.join(OUTPUT_DIR, "example_english_exam.pdf")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    content = r"""---
title: "Calculus I — Sample Final Exam"
documentclass: article
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
---

**Time: 90 minutes　　Total: 100 points**

## Part I: Multiple Choice (5 points each)

1. The derivative of $f(x) = x^3$ is

A. $3x$　　B. $3x^2$　　C. $x^2$　　D. $\frac{x^4}{4}$

2. The value of $\int_0^1 2x \, dx$ is

A. $0$　　B. $1$　　C. $2$　　D. $4$

## Part II: Computation

3. (15 points) Find the limit $\lim_{x \to 0} \frac{\sin x}{x}$.

4. (15 points) Compute $\frac{d}{dx} \left( e^{2x} \right)$.

## Answer Key

1. B　　2. B

3. $1$

4. $2e^{2x}$
"""

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    cmd = [
        "pandoc", MD_PATH,
        "-o", PDF_PATH,
        "--from", "markdown+raw_tex",
        "--pdf-engine=xelatex",
    ]
    subprocess.run(cmd, check=True)
    print(f"English exam generated: {PDF_PATH}")


if __name__ == "__main__":
    main()
