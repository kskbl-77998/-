# -*- coding: utf-8 -*-
"""Canvas 练习场 —— 给聂莹莹的参考实现（可直接运行）

运行：
    python docs/examples/canvas_playground.py

它演示了位网格任务里最容易出错的四件事：
    1. 位方块怎么画（等宽、居中、符号位描边）
    2. 进位弧形箭头怎么画、**方向为什么是向左**
    3. 数轴怎么把数字映射成坐标，越界红点怎么画
    4. 用 after() 做逐列高亮动画（不要用 time.sleep）

⚠️ 这是**学习用**的独立脚本，不是项目模块。
   看懂后请把逻辑搬进 src/ui/widgets/bit_grid.py 与 number_line.py，
   并按设计文档的规范改写尺寸、配色与数据结构。

作者：马子尊（示例）/ 聂莹莹（正式实现）
"""

import tkinter as tk

# ---------------------------------------------------------------- 规范常量
# 正式实现请直接引用 src/ui/theme.py，不要在这里重复定义
COLOR_BG = "#F6F8FB"
COLOR_PANEL = "#FFFFFF"
COLOR_PRIMARY = "#2F6FEB"
COLOR_DANGER = "#C93B3B"
COLOR_MUTED = "#6B7C93"
COLOR_TEXT = "#22303F"

CELL_W, CELL_H, CELL_GAP = 62, 52, 8
ARC_LIFT = 38

# 纵向布局（自上而下）
Y_BIT_LABEL = 96
Y_ARC = 184
Y_A = 190
Y_B = 290
Y_S = 420
Y_NUMLINE = 570

WIN_W, WIN_H = 860, 720


class PlaygroundApp:
    def __init__(self, root):
        self.root = root
        root.title("Canvas 练习场 —— 位网格 / 进位箭头 / 数轴")
        root.geometry(f"{WIN_W}x{WIN_H}")
        root.configure(bg=COLOR_BG)
        root.minsize(760, 640)

        self.canvas = tk.Canvas(root, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=(14, 6))

        self.btn = tk.Button(root, text="▶ 播放进位动画", command=self.start_animation,
                             font=("Microsoft YaHei", 11), bg=COLOR_PRIMARY, fg="white",
                             activebackground="#1F57C3", activeforeground="white",
                             relief=tk.FLAT, padx=18, pady=6)
        self.btn.pack(pady=(0, 14))

        # 示例数据：100 + 50（与设计文档一致）
        self.a = [0, 1, 1, 0, 0, 1, 0, 0]   # [X]补 = 0110 0100
        self.b = [0, 0, 1, 1, 0, 0, 1, 0]   # [Y]补 = 0011 0010
        self.s = [1, 0, 0, 1, 0, 1, 1, 0]   # 结果   = 1001 0110

        # carries[i] = 进入第 i 列（b{7-i}）的进位，即 C{7-i}
        # 100+50 时：C7=1、C6=1，其余为 0
        self.carries = [1, 1, 0, 0, 0, 0, 0, 0]

        self.col = -1            # 当前高亮列，-1 表示无
        self.timer = None        # 同一时刻只允许一个定时器
        self.draw()

    # ------------------------------------------------------------ 总入口
    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            24, 20, anchor="nw",
            text="示例：[X]补 0110 0100（+100）  +  [Y]补 0011 0010（+50）",
            font=("Microsoft YaHei", 11), fill=COLOR_MUTED)
        self.draw_bit_grid()
        self.draw_number_line()

    # ------------------------------------------------------------ 位网格
    def layout(self):
        """返回 (x0, 列间距)，供各处复用，避免坐标各写一套。"""
        n = 8
        total_w = n * CELL_W + (n - 1) * CELL_GAP
        x0 = (WIN_W - total_w) / 2
        return x0, CELL_W + CELL_GAP

    def draw_bit_grid(self):
        x0, step = self.layout()
        n = 8

        # 位序号
        for i in range(n):
            cx = x0 + i * step + CELL_W / 2
            self.canvas.create_text(cx, Y_BIT_LABEL, text=f"b{7 - i}",
                                    font=("Consolas", 12), fill=COLOR_MUTED)

        # 三行数据
        for bits, name, y in ((self.a, "A", Y_A), (self.b, "B", Y_B), (self.s, "S", Y_S)):
            self.canvas.create_text(x0 - 24, y + CELL_H / 2, text=f"[{name}]补",
                                    font=("Microsoft YaHei", 10),
                                    fill=COLOR_MUTED, anchor="e")
            for i, bit in enumerate(bits):
                x = x0 + i * step
                is_sign = (i == 0)
                is_hl = (self.col == i)
                outline = COLOR_DANGER if is_sign else COLOR_PRIMARY
                fill = "#FDEDED" if is_sign else ("#EDF3FE" if is_hl else COLOR_PANEL)
                self.canvas.create_rectangle(
                    x, y, x + CELL_W, y + CELL_H, fill=fill, outline=outline,
                    width=3 if (is_sign or is_hl) else 1, tags="cell")
                self.canvas.create_text(
                    x + CELL_W / 2, y + CELL_H / 2, text=str(bit),
                    font=("Consolas", 20, "bold"), fill=COLOR_TEXT, tags="cell")

        # 进位箭头：C_i 表示「从第 i-1 位进到第 i 位」，所以箭头方向向左。
        # 列 j（0 起）对应的位号是 7-j；从列 j 指向列 j-1 的那条箭头，标签是 C(8-j)。
        for j in range(1, n):
            if self.carries[j - 1] == 0:
                continue
            label = f"C{8 - j}"
            x_from = x0 + j * step + CELL_W / 2 - 8        # 右列（源）
            x_to = x0 + (j - 1) * step + CELL_W / 2 + 8    # 左列（目标）
            self.draw_carry(x_from, x_to, label)

        # 一句话点题：箭头为什么往左
        self.canvas.create_text(
            WIN_W - 60, Y_ARC - ARC_LIFT + 6, anchor="e",
            text="进位由低位向高位传播 → 箭头向左",
            font=("Microsoft YaHei", 9), fill=COLOR_MUTED)

        # 当前列说明
        if 0 <= self.col < n:
            x = x0 + self.col * step + CELL_W / 2
            self.canvas.create_text(
                x, Y_S + CELL_H + 18, text=f"正在计算 b{7 - self.col}",
                font=("Microsoft YaHei", 10), fill=COLOR_PRIMARY, anchor="n")

    def draw_carry(self, x_from, x_to, label):
        """二次贝塞尔 + 箭头头部；set(A,B,C) 平滑曲线等价于以 B 为控制点的抛物线。"""
        ctrl_x = (x_from + x_to) / 2
        ctrl_y = Y_ARC - ARC_LIFT
        self.canvas.create_line(
            x_from, Y_ARC, ctrl_x, ctrl_y, x_to, Y_ARC,
            smooth=True, width=2, fill=COLOR_PRIMARY,
            arrow="last", arrowshape=(9, 11, 3), tags="carry")
        self.canvas.create_text(ctrl_x, ctrl_y - 6, text=label,
                                font=("Microsoft YaHei", 9, "bold"),
                                fill=COLOR_PRIMARY, anchor="s", tags="carry")

    # ------------------------------------------------------------ 数轴
    def draw_number_line(self):
        left, right = 110, 720
        lo, hi = -128, 127

        def to_x(v):
            """真值 → 画布 x 坐标。这是数轴控件唯一需要记住的公式。"""
            return left + (v - lo) / (hi - lo) * (right - left)

        self.canvas.create_line(left, Y_NUMLINE, right, Y_NUMLINE,
                                fill=COLOR_MUTED, width=2)
        for v in (lo, -64, 0, 64, hi):
            x = to_x(v)
            self.canvas.create_line(x, Y_NUMLINE - 5, x, Y_NUMLINE + 5,
                                    fill=COLOR_MUTED, width=2)
            self.canvas.create_text(x, Y_NUMLINE + 12, text=str(v),
                                    font=("Consolas", 10), fill=COLOR_MUTED, anchor="n")

        # 机器结果 -106：在区间内，正常落点
        v = -106
        x = to_x(v)
        self.canvas.create_oval(x - 6, Y_NUMLINE - 6, x + 6, Y_NUMLINE + 6,
                                fill=COLOR_DANGER, outline="", tags="dot")
        self.canvas.create_text(x, Y_NUMLINE - 14, text=f"机器结果 {v}",
                                font=("Microsoft YaHei", 10),
                                fill=COLOR_DANGER, anchor="s")

        # 数学结果 +150 已越界：在右端画一个向外的红色箭头
        self.canvas.create_line(right, Y_NUMLINE, right + 26, Y_NUMLINE,
                                fill=COLOR_DANGER, width=2,
                                arrow="last", arrowshape=(8, 10, 3))
        self.canvas.create_text(right - 6, Y_NUMLINE - 26, anchor="e",
                                text="数学结果 +150（已越界）",
                                font=("Microsoft YaHei", 10), fill=COLOR_DANGER)

    # ------------------------------------------------------------ 动画
    def start_animation(self):
        if self.timer is not None:
            return                      # 防连点：已有动画在跑
        self.btn.configure(state=tk.DISABLED)
        self.col = 0
        self.draw()
        self.timer = self.root.after(450, self.next_column)

    def next_column(self):
        self.col += 1
        if self.col >= 8:
            self.col = -1
            self.timer = None
            self.draw()
            self.btn.configure(state=tk.NORMAL)
            return
        self.draw()
        self.timer = self.root.after(450, self.next_column)


if __name__ == "__main__":
    root = tk.Tk()
    PlaygroundApp(root)
    root.mainloop()
