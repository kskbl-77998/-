# -*- coding: utf-8 -*-
"""界面主题：配色、字体、尺寸常量与 DPI 缩放。

所有魔法数字集中在此，界面代码只引用常量，不写字面量。

负责人：成员C
"""

# ---------------------------------------------------------------- 配色
COLORS = {
    "bg": "#F6F8FB",          # 主背景
    "panel": "#FFFFFF",       # 卡片背景
    "header": "#132238",      # 顶栏
    "primary": "#2F6FEB",     # 主色
    "primary_light": "#EDF3FE",
    "danger": "#C93B3B",      # 符号位 / 溢出
    "danger_light": "#FDEDED",
    "warning": "#B8730A",     # 求补口诀
    "warning_light": "#FDF4E3",
    "success": "#12855E",     # 校验通过
    "success_light": "#E9F7F1",
    "text": "#22303F",
    "muted": "#6B7C93",
    "border": "#D9E1EC",
    "ink_navy": "#132238",
}

# ---------------------------------------------------------------- 字体
FONT_UI = "Microsoft YaHei"   # 中文界面
FONT_MONO = "Consolas"        # 位串与数字，必须等宽

# 各区域基准字号（未缩放前）
FONT_SIZES = {
    "title": 16,
    "subtitle": 10,
    "section": 11,
    "body": 10,
    "small": 9,
    "mono": 12,
}

# ---------------------------------------------------------------- 尺寸
SIZES = {
    "window_w": 1280,
    "window_h": 800,
    "min_w": 1100,
    "min_h": 700,
    "header_h": 62,
    "footer_h": 52,
    "left_w": 360,
    "right_w": 320,
    "pad": 12,
    "gap": 8,
    "bit_cell_w": 62,
    "bit_cell_h": 52,
}


def base_scale(root) -> float:
    """取系统 DPI 缩放系数并钳制在 [0.8, 2.0]。

    高分屏上 tk scaling 可能返回 2.5 以上，直接乘字号会导致界面不可用。
    """
    cached = getattr(root, "_dpi_scale", None)
    if cached is not None:
        return cached
    try:
        scale = float(root.tk.call("tk", "scaling"))
    except Exception:
        scale = 1.0
    scale = max(0.8, min(2.0, scale))
    root._dpi_scale = scale
    return scale


def ui_font(root, key: str = "body", bold: bool = False) -> tuple:
    """按 key 取界面字体元组，已应用 DPI 缩放。

    >>> ui_font(root, "title", bold=True)   # doctest: +SKIP
    ('Microsoft YaHei', 24, 'bold')
    """
    size = int(round(FONT_SIZES.get(key, FONT_SIZES["body"]) * base_scale(root)))
    return (FONT_UI, max(8, size), "bold") if bold else (FONT_UI, max(8, size))


def mono_font(root, size_key: str = "mono", bold: bool = False) -> tuple:
    """取等宽字体元组，用于位串与数字对齐。"""
    size = int(round(FONT_SIZES.get(size_key, FONT_SIZES["mono"]) * base_scale(root)))
    return (FONT_MONO, max(8, size), "bold") if bold else (FONT_MONO, max(8, size))


def init_style(root) -> None:
    """初始化 ttk 全局样式（主题、背景色）。"""
    from tkinter import ttk

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["panel"])
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])
    style.configure("Card.TLabel", background=COLORS["panel"], foreground=COLORS["text"])
    style.configure("Muted.TLabel", background=COLORS["panel"], foreground=COLORS["muted"])
