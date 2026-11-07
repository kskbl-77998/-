# -*- coding: utf-8 -*-
"""位网格控件：一排位方块 + 列高亮 + 进位弧形箭头。

负责人：聂莹莹（分支 feature/canvas-render）

实现要点（详见设计文档 7.2 可视化映射表）：
    1. 位方块等宽、等间距，使用等宽字体；
    2. 符号位列用 RED 描边，始终可见；
    3. 进位箭头用 create_line(smooth=True) 画二次曲线，最高点标 C_i；
    4. 每次只 delete("carry") 与 delete("cell")，不整体清空画布；
    5. 视野外图元做剔除（culling），16 位时不卡顿。
"""

import tkinter as tk


class BitGrid(tk.Frame):
    """位网格。"""

    def __init__(self, master, width=8, cell_w=62, cell_h=52, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def render(self, bits, highlight=None, carries=None):
        """重绘位网格。

        Args:
            bits: 位列表，索引 0 为符号位。
            highlight: 需要高亮的位序号集合。
            carries: 进位字典 {位序号: 0/1}，用于画箭头。
        """
        raise NotImplementedError("TODO(聂莹莹): 实现位方块与进位箭头绘制")

    def animate_invert(self, before, after, duration_ms=300):
        """求补阶段的逐位翻转动画。"""
        raise NotImplementedError("TODO(聂莹莹): 实现逐位翻转动画")
