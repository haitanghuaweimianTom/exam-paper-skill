# Exam Paper Skill

通用跨学科的试卷、讲义、复习全书与复习资料生成 Skill。从任意学科的材料中提取知识，生成包含「举一反三」式问题的精美 Markdown + PDF。

## 功能

- **知识提炼**：自动读取用户提供的教材、课件、历年试卷，提取核心考点
- **举一反三出题**：生成基础题、变式题、综合题、开放题，培养迁移能力
- **多类型输出**：
  - **试卷（Exam Paper）**：紧凑排版，适合打印
  - **讲义（Study Guide）**：知识梳理 + 典例 + 引导思考
  - **复习全书（Review Book）**：系统理论 + 多题型例题 + 详解
  - **纯练习题（Practice Questions）**：超紧凑，最大化题量
- **LaTeX 公式支持**：通过 Pandoc + XeLaTeX 输出高质量 PDF，完美渲染数学公式
- **中文排版规范化**：中文引号、省略号、破折号、数学模式中文处理
- **图表绘制支持**：
  - 内置 TikZ 矢量图模板（几何图、流程图、树形图等）
  - 内置 matplotlib 绘图工具（坐标系、函数图像、数轴、受力图、柱状图、折线图、散点图、箱线图、韦恩图、流程图、概率树、三角形）
- **生成质量检查**：`tools/quality_check.py` 自动扫描 markdown，发现直引号、水平分割线、数学模式中文、未闭合公式等常见问题
- **跨学科通用框架**：不依赖固定学科列表，按「内容类型」抽象规则，任意学科均可扩展
- **英文模式支持**：提供 `article` 类 frontmatter 模板，可生成纯英文试卷/讲义

## 安装

```bash
bash install.sh
```

安装脚本会自动检查 `pandoc`、`xelatex`、`matplotlib` 等依赖是否已安装。

```bash
# 或安装到项目级 skill 目录
bash install.sh /path/to/project/.claude/skills
```

安装后，skill 目录下会生成 `SKILL.md`、`tools/`、`examples/`、`assets/`，Agent 即可识别并调用。

**依赖**：
- Python 3.8+
- Pandoc
- XeLaTeX（需包含 ctex、xeCJK 等中文宏包）
- Noto Serif CJK SC（或系统自带的中文字体）
- matplotlib（用于 `tools/diagram_tools.py` 绘图）

## 使用

在 Claude / Kimi Code CLI 等支持 skill 的 Agent 环境中，直接描述需求即可：

```
请根据这份教材生成一套计量经济学期末模拟试卷，包含证明题、计算题和综合应用题。
```

Agent 会自动：
1. 读取材料并提炼知识点
2. 识别内容类型（公式、图表、文本、代码等）并套用对应规则
3. 设计符合学科特点的题型
4. 输出 Markdown 文件
5. 调用 Pandoc 编译为 PDF
6. 检查公式渲染、中文排版和缺字警告

## 快速上手示例

仓库包含可直接运行的示例脚本：

```bash
cd examples
python generate_exam.py          # 生成中文期末试卷 PDF
python generate_review_book.py   # 生成中文复习全书 PDF
python generate_english_exam.py  # 生成英文试卷 PDF
python generate_diagrams.py      # 批量生成各类图表 PNG
```

生成后查看 `examples/output/` 目录。

## 内容类型支持

| 内容类型 | 处理方式 |
|---------|---------|
| 公式与符号 | LaTeX 数学模式、希腊字母、上下标、矩阵、分段函数 |
| 表格与对照 | Markdown 表格、单元格数学模式、长表格分页 |
| 图表与图形 | TikZ 模板 + matplotlib 绘图工具 |
| 代码与伪代码 | 代码块、算法步骤 |
| 多语言文本 | 文言文、外语、术语对照 |
| 引用与证明 | 定理、引理、证明环境、引用标注 |
| 案例与论述 | 结构化事实→分析→结论 |

## 示例学科

以下仅为框架应用示例，不代表有限列表：

- 化学 / 物理 / 生物
- 数学 / 统计学
- 英语 / 语文
- 经济学 / 计量经济学 / 博弈论
- 人工智能 / 计算机科学
- 法学 / 医学 / 工程学

任何未列出的学科，Agent 都可以根据 SKILL.md 中的「学科适配框架」自行推导规则。

## 项目结构

```
exam-paper-skill/
├── install.sh       # 安装脚本（含依赖检查）
├── SKILL.md         # Skill 核心定义与使用规范
├── README.md        # 本文件
├── tools/           # 绘图与辅助工具
│   ├── diagram_tools.py
│   └── quality_check.py
├── examples/        # 可直接运行的示例脚本
│   ├── generate_exam.py
│   ├── generate_review_book.py
│   ├── generate_english_exam.py
│   └── generate_diagrams.py
└── assets/          # README 示例图片
    ├── example_coordinate.png
    ├── example_triangle.png
    ├── example_forces.png
    ├── example_bar.png
    ├── example_venn.png
    └── example_flowchart.png
```

## 最近改进

- 重构为内容类型驱动的通用跨学科框架
- 增加复习全书（Review Book）文档类型与 frontmatter 模板
- 补充数学模式中文字符处理、Unicode 逻辑符号规避、raw-string 转义陷阱
- 增加选择题/判断题/计算题/简答题 Markdown 模板
- 新增 TikZ 模板与 matplotlib 绘图工具，实现真正的图表绘制能力
- 新增 `quality_check.py` 生成质量检查脚本
- 新增 `examples/` 可直接运行的示例
- `install.sh` 增加依赖检测
- 新增英文文档 frontmatter 模板
- 完善 PDF 编译命令与排错清单

## 贡献

欢迎提交 Issue 和 PR。如果你有新的内容类型需求，或发现了排版/公式渲染/绘图的问题，请在 SKILL.md 的对应章节补充规则，并更新本 README。

## 许可证

MIT
