#!/usr/bin/env python3
"""Example: generate various diagrams using diagram_tools.py."""

import sys
import os

# Add parent directory to import tools
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from diagram_tools import (
    coordinate_system,
    force_diagram,
    geometry_triangle,
    bar_chart,
    line_chart,
    venn_diagram,
    flowchart,
)


def main():
    out_dir = "output"
    os.makedirs(out_dir, exist_ok=True)

    coordinate_system(
        points=[(0, 0), (2, 3), (-2, 1)],
        segments=[((0, 0), (2, 3)), ((0, 0), (-2, 1))],
        labels={0: "O", 1: "A", 2: "B"},
        output_path=os.path.join(out_dir, "diagram_coordinate.png"),
    )

    force_diagram(
        forces=[
            {"x": 3, "y": 0, "label": "F1", "color": "red"},
            {"x": 0, "y": 3, "label": "F2", "color": "blue"},
            {"x": -2, "y": -2, "label": "F3", "color": "green"},
        ],
        output_path=os.path.join(out_dir, "diagram_forces.png"),
        xlim=(-4, 4),
        ylim=(-4, 4),
    )

    geometry_triangle(
        3, 4, 5,
        labels=("A", "B", "C"),
        output_path=os.path.join(out_dir, "diagram_triangle.png"),
    )

    bar_chart(
        categories=["Q1", "Q2", "Q3", "Q4"],
        values=[120, 190, 150, 220],
        output_path=os.path.join(out_dir, "diagram_bar.png"),
        title="Quarterly Data",
    )

    line_chart(
        x=[0, 1, 2, 3, 4, 5],
        y=[0, 1, 4, 9, 16, 25],
        output_path=os.path.join(out_dir, "diagram_line.png"),
        title=r"$y = x^2$",
        xlabel="x",
        ylabel="y",
    )

    venn_diagram(
        {"A": "A", "B": "B", "A_only": "12", "B_only": "18", "intersection": "5"},
        output_path=os.path.join(out_dir, "diagram_venn.png"),
    )

    flowchart(
        nodes={
            "开始": {"pos": (0, 0), "type": "start"},
            "输入n": {"pos": (2, 0), "type": "io"},
            "n>0?": {"pos": (4, 0), "type": "decision"},
            "计算": {"pos": (6, 1.5), "type": "process"},
            "报错": {"pos": (6, -1.5), "type": "process"},
            "输出结果": {"pos": (8, 0), "type": "io"},
            "结束": {"pos": (10, 0), "type": "end"},
        },
        edges=[
            ("开始", "输入n"),
            ("输入n", "n>0?"),
            ("n>0?", "计算", "是"),
            ("n>0?", "报错", "否"),
            ("计算", "输出结果"),
            ("报错", "输出结果"),
            ("输出结果", "结束"),
        ],
        output_path=os.path.join(out_dir, "diagram_flowchart.png"),
    )

    print(f"All diagrams saved to {out_dir}/")


if __name__ == "__main__":
    main()
