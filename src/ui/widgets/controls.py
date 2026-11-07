# -*- coding: utf-8 -*-
"""控制条：字长选择、操作数输入、运算选择、播放控制。

负责人：成员C（分支 feature/ui-layout）
"""

import tkinter as tk
from tkinter import ttk

from .. import theme


class ControlPanel(tk.Frame):
    """左侧参数与播放控制。"""

    def __init__(self, master, on_generate=None, on_step=None, on_auto=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_generate = on_generate
        self.on_step = on_step
        self.on_auto = on_auto

        self.var_width = tk.IntVar(value=8)
        self.var_op = tk.StringVar(value="+")
        self.var_x = tk.StringVar(value="-5")
        self.var_y = tk.StringVar(value="12")
        self.var_delay = tk.DoubleVar(value=0.8)
        self._build()

    def _build(self):
        """按设计文档 7.1 的左栏结构搭建控件。"""
        raise NotImplementedError("TODO(成员C): 实现字长/输入/运算/按钮/调速/示例库")

    def read(self):
        """读取当前输入，返回 (width, x_text, y_text, op)。"""
        raise NotImplementedError("TODO(成员C): 实现输入读取")

    def set_enabled(self, enabled: bool):
        """RUNNING 状态下禁用输入，避免播放中数据被改。"""
        raise NotImplementedError("TODO(成员C): 实现控件启用/禁用")
