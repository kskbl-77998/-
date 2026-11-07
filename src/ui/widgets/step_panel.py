# -*- coding: utf-8 -*-
"""步骤日志面板：按 Step 序列逐条显示，自动滚动到当前行。

负责人：成员C（分支 feature/ui-layout）
"""

import tkinter as tk


class StepPanel(tk.Frame):
    """日志列表。"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.text = tk.Text(self, wrap=tk.WORD, bd=0, state=tk.DISABLED)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.scroll = tk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)

    def load(self, steps):
        """载入步骤序列，展示到第 0 步。

        Args:
            steps: Step 列表。
        """
        raise NotImplementedError("TODO(成员C): 实现日志载入与编号")

    def goto(self, index):
        """高亮并滚动到第 index 步（从 1 开始）。"""
        raise NotImplementedError("TODO(成员C): 实现当前行高亮与见即滚动")
