#!/usr/bin/env python3
"""Lightweight matplotlib-based diagram helpers for exam-paper-skill.

These functions generate common diagrams used in exam papers and study guides.
Output is PNG by default; images can be embedded in markdown with ![](path.png).
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Use a CJK-compatible font for Chinese labels if available
try:
    from matplotlib import font_manager
    cjk_font = next((f.name for f in font_manager.fontManager.ttflist
                     if "Noto Sans CJK" in f.name or "Source Han" in f.name
                     or "WenQuanYi" in f.name), None)
    if cjk_font:
        plt.rcParams["font.sans-serif"] = [cjk_font, "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False
except Exception:
    pass


def _save(fig, output_path, dpi=150):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    return output_path


def coordinate_system(points=None, segments=None, labels=None, output_path="diagram_coord.png",
                      xlim=(-5, 5), ylim=(-5, 5), show_grid=True):
    """Draw a 2D coordinate system with optional points and line segments.

    Args:
        points: list of (x, y) tuples
        segments: list of ((x1, y1), (x2, y2)) tuples
        labels: dict mapping point index to label string
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_aspect("equal")
    if show_grid:
        ax.grid(True, linestyle="--", alpha=0.5)

    if points:
        xs, ys = zip(*points)
        ax.scatter(xs, ys, color="blue", zorder=5)
        if labels:
            for idx, label in labels.items():
                ax.annotate(label, (xs[idx], ys[idx]), textcoords="offset points", xytext=(5, 5))

    if segments:
        for (x1, y1), (x2, y2) in segments:
            ax.plot([x1, x2], [y1, y2], color="red", linewidth=1.5)

    return _save(fig, output_path)


def force_diagram(forces, output_path="diagram_forces.png", xlim=(-3, 3), ylim=(-3, 3)):
    """Draw a free-body / force diagram.

    Args:
        forces: list of dicts {"x": dx, "y": dy, "label": "F1", "color": "red"}
    """
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_aspect("equal")

    ax.scatter([0], [0], color="black", s=80, zorder=5)
    for f in forces:
        dx, dy = f["x"], f["y"]
        color = f.get("color", "blue")
        label = f.get("label", "")
        ax.arrow(0, 0, dx, dy, head_width=0.15, head_length=0.15, fc=color, ec=color, linewidth=1.5)
        if label:
            ax.text(dx * 1.15, dy * 1.15, label, fontsize=11, color=color)

    return _save(fig, output_path)


def geometry_triangle(a, b, c, labels=("A", "B", "C"), output_path="diagram_triangle.png"):
    """Draw a triangle given three side lengths a, b, c.

    Places vertex A at origin, B on positive x-axis, C by law of cosines.
    """
    # Law of cosines: c^2 = a^2 + b^2 - 2ab cos(C)
    # Here a = BC, b = AC, c = AB
    A = np.array([0.0, 0.0])
    B = np.array([c, 0.0])
    cos_angle = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
    cos_angle = max(-1, min(1, cos_angle))
    sin_angle = np.sqrt(1 - cos_angle ** 2)
    C = np.array([b * cos_angle, b * sin_angle])

    fig, ax = plt.subplots(figsize=(5, 4))
    triangle = plt.Polygon([A, B, C], fill=False, edgecolor="black", linewidth=1.5)
    ax.add_patch(triangle)
    ax.scatter(*zip(A, B, C), color="black", zorder=5)
    ax.annotate(labels[0], A, textcoords="offset points", xytext=(-15, -10), fontsize=12)
    ax.annotate(labels[1], B, textcoords="offset points", xytext=(5, -10), fontsize=12)
    ax.annotate(labels[2], C, textcoords="offset points", xytext=(5, 5), fontsize=12)

    ax.set_aspect("equal")
    ax.autoscale_view()
    ax.axis("off")
    return _save(fig, output_path)


def bar_chart(categories, values, output_path="diagram_bar.png", title="", xlabel="", ylabel=""):
    """Draw a simple bar chart."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(categories, values, color="steelblue")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return _save(fig, output_path)


def line_chart(x, y, output_path="diagram_line.png", title="", xlabel="", ylabel=""):
    """Draw a simple line chart."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, marker="o", color="steelblue")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.5)
    return _save(fig, output_path)


def venn_diagram(labels, output_path="diagram_venn.png"):
    """Draw a two-set Venn diagram.

    Args:
        labels: dict with keys "A", "B", "A_only", "B_only", "intersection"
    """
    from matplotlib.patches import Circle
    fig, ax = plt.subplots(figsize=(5, 4))
    c1 = Circle((-0.5, 0), 1.0, color="skyblue", alpha=0.4)
    c2 = Circle((0.5, 0), 1.0, color="lightcoral", alpha=0.4)
    ax.add_patch(c1)
    ax.add_patch(c2)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(-1.0, 0.8, labels.get("A", "A"), fontsize=12, ha="center")
    ax.text(1.0, 0.8, labels.get("B", "B"), fontsize=12, ha="center")
    ax.text(-0.9, 0, labels.get("A_only", ""), fontsize=11, ha="center")
    ax.text(0.9, 0, labels.get("B_only", ""), fontsize=11, ha="center")
    ax.text(0, 0, labels.get("intersection", ""), fontsize=11, ha="center")

    return _save(fig, output_path)


def flowchart(nodes, edges, output_path="diagram_flow.png"):
    """Draw a simple flowchart.

    Args:
        nodes: dict {name: (x, y)}
        edges: list of (from, to)
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    for name, (x, y) in nodes.items():
        ax.text(x, y, name, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="black"))
    for start, end in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black"))
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 5)
    ax.axis("off")
    return _save(fig, output_path)


if __name__ == "__main__":
    # Run simple smoke tests
    coordinate_system(points=[(1, 2), (-2, -1)], segments=[((0, 0), (1, 2))], output_path="/tmp/exam_skill_test/coord.png")
    force_diagram([{"x": 2, "y": 1, "label": "F1"}, {"x": -1, "y": 2, "label": "F2"}], output_path="/tmp/exam_skill_test/forces.png")
    geometry_triangle(3, 4, 5, output_path="/tmp/exam_skill_test/triangle.png")
    bar_chart(["A", "B", "C"], [10, 20, 15], output_path="/tmp/exam_skill_test/bar.png")
    line_chart([0, 1, 2, 3], [0, 1, 4, 9], output_path="/tmp/exam_skill_test/line.png")
    venn_diagram({"A": "集合 A", "B": "集合 B", "A_only": "仅 A", "B_only": "仅 B", "intersection": "A∩B"},
                 output_path="/tmp/exam_skill_test/venn.png")
    flowchart({"开始": (0, 4), "处理": (3, 4), "结束": (6, 4)},
              [("开始", "处理"), ("处理", "结束")], output_path="/tmp/exam_skill_test/flow.png")
    print("Smoke test outputs written to /tmp/exam_skill_test/")
