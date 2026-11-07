# -*- coding: utf-8 -*-
"""数轴控件：显示补码可表示区间，结果越界时红点跳出。

负责人：成员D（分支 feature/canvas-render）
"""

import tkinter as tk


class NumberLine(tk.Frame):
    """数值区间数轴。"""

    def __init__(self, master, width=8, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.canvas = tk.Canvas(self, height=90, highlightthickness=0)
        self.canvas.pack(fill=tk.X, expand=True)

    def render(self, width, result_value):
        """重绘数轴。

        Args:
            width: 字长，决定区间 [-2^(n-1), 2^(n-1)-1]。
            result_value: 机器结果的真值，用于定位红点。
        """
        raise NotImplementedError("TODO(成员D): 实现数轴与越界红点")

    def animate_overflow(self):
        """溢出时红点跳出区间并闪烁 3 次。"""
        raise NotImplementedError("TODO(成员D): 实现越界动画")
