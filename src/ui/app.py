# -*- coding: utf-8 -*-
"""主窗口：布局、事件绑定、交互状态机。

当前状态：**布局骨架**（可运行，用于成员C 后续填充控件、成员D 挂载可视化组件）。
状态机 IDLE / READY / RUNNING / DONE / ERROR 尚未实现，见 TODO。

负责人：成员C
"""

import tkinter as tk
from tkinter import ttk

from ..core.models import Scenario
from . import theme

# 交互状态
STATE_IDLE = "IDLE"
STATE_READY = "READY"
STATE_RUNNING = "RUNNING"
STATE_DONE = "DONE"
STATE_ERROR = "ERROR"


class ComplementApp:
    """补码模拟器主窗口。"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.state = STATE_IDLE
        self.scenario = None  # type: Scenario | None
        self.step_index = 0

        theme.init_style(root)
        self._init_window()
        self._init_status()   # 先占底部，避免被 expand 的主区挤掉
        self._init_layout()

    # ------------------------------------------------------------ 窗口
    def _init_window(self) -> None:
        """设置窗口尺寸与最小尺寸。

        ⚠️ 冲突演练点：成员D 会在本函数追加画布尺寸参数。
        """
        self.root.geometry(
            f"{theme.SIZES['window_w']}x{theme.SIZES['window_h']}"
        )
        self.root.minsize(theme.SIZES["min_w"], theme.SIZES["min_h"])
        self.root.configure(bg=theme.COLORS["bg"])

    # ------------------------------------------------------------ 布局
    def _init_layout(self) -> None:
        """顶栏 / 三栏 / 底栏。"""
        self._build_header()

        main = tk.Frame(self.root, bg=theme.COLORS["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=theme.SIZES["pad"],
                  pady=(0, theme.SIZES["gap"]))

        self._build_left(main)
        self._build_right(main)
        self._build_center(main)   # 最后 pack，才能吸收剩余空间

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=theme.COLORS["header"],
                          height=theme.SIZES["header_h"])
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header,
            text="补码模拟器 · 加减运算与溢出判定",
            font=theme.ui_font(self.root, "title", bold=True),
            fg="#FFFFFF", bg=theme.COLORS["header"],
        ).pack(side=tk.LEFT, padx=24)

        self.lbl_width = tk.Label(
            header,
            text="8 位 · 二进制",
            font=theme.ui_font(self.root, "subtitle"),
            fg="#9FB0C4", bg=theme.COLORS["header"],
        )
        self.lbl_width.pack(side=tk.RIGHT, padx=24)

    def _build_left(self, parent: tk.Frame) -> None:
        """左栏：参数与播放控制（成员C 填充）。"""
        left = tk.Frame(parent, bg=theme.COLORS["primary_light"],
                        width=theme.SIZES["left_w"], bd=1, relief=tk.SOLID)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, theme.SIZES["gap"]))
        left.pack_propagate(False)

        tk.Label(
            left, text="① 参数与输入",
            font=theme.ui_font(self.root, "section", bold=True),
            fg=theme.COLORS["primary"], bg=theme.COLORS["primary_light"],
        ).pack(anchor="w", padx=16, pady=(14, 8))

        ttk.Button(left, text="生成 / 重置", command=self._on_generate).pack(
            fill=tk.X, padx=16, pady=4)
        ttk.Button(left, text="单步执行", command=self._on_step).pack(
            fill=tk.X, padx=16, pady=4)
        ttk.Button(left, text="自动播放", command=self._on_auto).pack(
            fill=tk.X, padx=16, pady=4)

        # TODO(成员C): 字长单选、X/Y 输入框、加减切换、调速滑块、示例库

    def _build_center(self, parent: tk.Frame) -> None:
        """中栏：四码对照 + 进位链 + 数轴（成员D 挂载 Canvas）。"""
        center = tk.Frame(parent, bg=theme.COLORS["bg"])
        center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        card = tk.Frame(center, bg=theme.COLORS["panel"], bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            card, text="③ 四码对照 / ④ 逐位加法与进位链",
            font=theme.ui_font(self.root, "section", bold=True),
            fg=theme.COLORS["ink_navy"], bg=theme.COLORS["panel"],
        ).pack(anchor="w", padx=16, pady=(14, 6))

        self.canvas = tk.Canvas(card, bg=theme.COLORS["panel"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
        self.canvas.create_text(
            20, 20, anchor="nw",
            text="[占位] 位网格与进位箭头由成员D 在 feature/canvas-render 实现",
            font=theme.ui_font(self.root, "small"),
            fill=theme.COLORS["muted"],
        )

    def _build_right(self, parent: tk.Frame) -> None:
        """右栏：步骤日志 + 溢出结论（成员C 填充）。"""
        right = tk.Frame(parent, bg=theme.COLORS["panel"],
                         width=theme.SIZES["right_w"], bd=1, relief=tk.SOLID)
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=(theme.SIZES["gap"], 0))
        right.pack_propagate(False)

        tk.Label(
            right, text="⑤ 步骤日志",
            font=theme.ui_font(self.root, "section", bold=True),
            fg=theme.COLORS["ink_navy"], bg=theme.COLORS["panel"],
        ).pack(anchor="w", padx=14, pady=(14, 6))

        self.txt_log = tk.Text(
            right, height=14, wrap=tk.WORD, bd=0,
            font=theme.ui_font(self.root, "small"),
            bg=theme.COLORS["panel"], fg=theme.COLORS["text"],
        )
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=14, pady=(0, 10))
        self.txt_log.insert("end", "[1] 等待输入…\n")
        self.txt_log.configure(state=tk.DISABLED)

    def _init_status(self) -> None:
        footer = tk.Frame(self.root, bg="#EFF2F6", height=theme.SIZES["footer_h"])
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        self.lbl_status = tk.Label(
            footer, text="状态：就绪　｜　请输入两个操作数",
            font=theme.ui_font(self.root, "small"),
            fg=theme.COLORS["muted"], bg="#EFF2F6",
        )
        self.lbl_status.pack(side=tk.LEFT, padx=16)

    # ------------------------------------------------------------ 事件
    def _set_status(self, text: str) -> None:
        self.lbl_status.configure(text=f"状态：{text}")

    def _on_generate(self) -> None:
        self._set_status("生成功能开发中（见 docs/Team_Task_Allocation.md 任务 10–12）")

    def _on_step(self) -> None:
        self._set_status("单步功能开发中")

    def _on_auto(self) -> None:
        self._set_status("自动播放功能开发中")

    # TODO(成员C): 实现状态机切换、输入校验、日志滚动、快捷键绑定
    # TODO(成员D): 在 canvas 上调用 BitGrid / NumberLine 渲染

    def run(self) -> None:
        self.root.mainloop()
