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
    """Draw a 2D coordinate system with optional points and line segments."""
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


def function_plot(func, x_range, output_path="diagram_function.png", title="", xlabel="x", ylabel="y",
                  num_points=400):
    """Plot a mathematical function y = func(x) over x_range.

    Args:
        func: callable that takes a numpy array and returns an array
        x_range: tuple (xmin, xmax)
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    x = np.linspace(x_range[0], x_range[1], num_points)
    y = func(x)
    ax.plot(x, y, color="steelblue", linewidth=1.8)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.5)
    return _save(fig, output_path)


def number_line(points, output_path="diagram_numberline.png", xlim=None, labels=None):
    """Draw a number line with marked points.

    Args:
        points: list of numbers to mark
        labels: dict mapping point index to label string
    """
    fig, ax = plt.subplots(figsize=(7, 1.0))
    points = sorted(points)
    if xlim is None:
        pad = max(1.0, (points[-1] - points[0]) * 0.2)
        xlim = (points[0] - pad, points[-1] + pad)

    ax.set_xlim(xlim)
    ax.set_ylim(-0.5, 0.5)
    ax.axhline(0, color="black", linewidth=1.2)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    for idx, p in enumerate(points):
        ax.plot([p], [0], marker="o", color="blue", markersize=7)
        label = labels.get(idx, str(p)) if labels else str(p)
        ax.text(p, 0.12, label, ha="center", va="bottom", fontsize=10)

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


def scatter_plot(x, y, output_path="diagram_scatter.png", title="", xlabel="x", ylabel="y"):
    """Draw a scatter plot."""
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x, y, color="steelblue", s=60, alpha=0.7)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle="--", alpha=0.5)
    return _save(fig, output_path)


def box_plot(data, labels=None, output_path="diagram_box.png", title=""):
    """Draw a box plot.

    Args:
        data: list of lists/arrays, one per box
        labels: list of labels for each box
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    try:
        ax.boxplot(data, tick_labels=labels)
    except TypeError:
        # Fallback for older matplotlib
        ax.boxplot(data, labels=labels)
    ax.set_title(title)
    return _save(fig, output_path)


def probability_tree(branches, output_path="diagram_probtree.png"):
    """Draw a simple two-level probability tree.

    Args:
        branches: list of dicts {"label": "A", "prob": 0.5, "children": [{"label": "B", "prob": 0.6}, ...]}
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    root_x, root_y = 0, 2.5
    level1_y = 1.0
    level2_y = -0.5

    ax.text(root_x, root_y, "Start", ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))

    n = len(branches)
    x_positions = np.linspace(-(n - 1) * 1.5, (n - 1) * 1.5, n)

    def _edge_label(x1, y1, x2, y2, text, offset=0.12):
        dx, dy = x2 - x1, y2 - y1
        length = np.hypot(dx, dy) or 1.0
        # Perpendicular unit vector pointing up-left-ish
        perp_x, perp_y = -dy / length, dx / length
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + perp_x * offset, mid_y + perp_y * offset, str(text),
                ha="center", va="center", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.8))

    for i, branch in enumerate(branches):
        x1 = x_positions[i]
        ax.plot([root_x, x1], [root_y, level1_y], color="black")
        _edge_label(root_x, root_y, x1, level1_y, branch.get("prob", ""))
        ax.text(x1, level1_y, branch.get("label", ""), ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

        children = branch.get("children", [])
        if children:
            m = len(children)
            child_xs = np.linspace(x1 - (m - 1) * 0.7, x1 + (m - 1) * 0.7, m)
            for j, child in enumerate(children):
                cx = child_xs[j]
                ax.plot([x1, cx], [level1_y, level2_y], color="black")
                _edge_label(x1, level1_y, cx, level2_y, child.get("prob", ""))
                ax.text(cx, level2_y, child.get("label", ""), ha="center", va="center",
                        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))

    ax.set_xlim(-(n + 1) * 1.5, (n + 1) * 1.5)
    ax.set_ylim(-1.5, 3.5)
    ax.axis("off")
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
    xs, ys = [], []
    for name, (x, y) in nodes.items():
        ax.text(x, y, name, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", edgecolor="black"))
        xs.append(x)
        ys.append(y)
    for start, end in edges:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black"))
    # Auto-scale limits with padding so arrows and labels fit
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_pad = max(1.0, (x_max - x_min) * 0.15)
    y_pad = max(1.0, (y_max - y_min) * 0.3)
    ax.set_xlim(x_min - x_pad, x_max + x_pad)
    ax.set_ylim(y_min - y_pad, y_max + y_pad)
    ax.axis("off")
    return _save(fig, output_path)


if __name__ == "__main__":
    # Run simple smoke tests
    coordinate_system(points=[(1, 2), (-2, -1)], segments=[((0, 0), (1, 2))], output_path="/tmp/exam_skill_test/coord.png")
    function_plot(lambda x: x ** 2, (-3, 3), output_path="/tmp/exam_skill_test/function.png", title=r"$y = x^2$")
    number_line([-3, -1, 0, 2, 4], output_path="/tmp/exam_skill_test/numberline.png")
    force_diagram([{"x": 2, "y": 1, "label": "F1", "color": "red"},
                   {"x": -1, "y": 2, "label": "F2", "color": "blue"}],
                  output_path="/tmp/exam_skill_test/forces.png")
    geometry_triangle(3, 4, 5, output_path="/tmp/exam_skill_test/triangle.png")
    bar_chart(["A", "B", "C"], [10, 20, 15], output_path="/tmp/exam_skill_test/bar.png")
    line_chart([0, 1, 2, 3], [0, 1, 4, 9], output_path="/tmp/exam_skill_test/line.png")
    scatter_plot([1, 2, 3, 4], [2, 3, 5, 4], output_path="/tmp/exam_skill_test/scatter.png")
    box_plot([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]], labels=["Group A", "Group B"], output_path="/tmp/exam_skill_test/box.png")
    probability_tree([
        {"label": "A", "prob": "0.5", "children": [{"label": "B", "prob": "0.6"}, {"label": "B'", "prob": "0.4"}]},
        {"label": "A'", "prob": "0.5", "children": [{"label": "B", "prob": "0.3"}, {"label": "B'", "prob": "0.7"}]},
    ], output_path="/tmp/exam_skill_test/probtree.png")
    venn_diagram({"A": "A", "B": "B", "A_only": "10", "B_only": "15", "intersection": "5"},
                 output_path="/tmp/exam_skill_test/venn.png")
    flowchart({"开始": (1, 4), "输入": (3, 4), "处理": (5, 4), "结束": (7, 4)},
              [("开始", "输入"), ("输入", "处理"), ("处理", "结束")],
              output_path="/tmp/exam_skill_test/flow.png")
    print("Smoke test outputs written to /tmp/exam_skill_test/")
