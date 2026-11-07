#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补码模拟器 —— 程序入口。

用法：
    python main.py

本文件只做三件事：
1. 创建 Tk 根窗口；
2. 挂载 :class:`src.ui.app.ComplementApp`；
3. 兜底捕获未处理异常，避免演示时直接闪退。

作者：马子尊（项目负责人）
"""

import sys
import traceback


def main() -> int:
    """启动图形界面，返回进程退出码。"""
    try:
        import tkinter as tk
    except ImportError:
        print("[错误] 未找到 tkinter。", file=sys.stderr)
        print("Linux 用户请安装：sudo apt install python3-tk", file=sys.stderr)
        return 1

    from src.ui.app import ComplementApp

    root = tk.Tk()
    root.title("补码模拟器 · 加减运算与溢出判定")

    app = ComplementApp(root)

    def _on_error(exc_type, exc_value, exc_tb):
        """把未捕获异常打到控制台并弹窗提示，而不是让窗口静默消失。"""
        traceback.print_exception(exc_type, exc_value, exc_tb)
        try:
            from tkinter import messagebox

            messagebox.showerror(
                "程序异常",
                "发生了未预期的错误，详情见控制台输出。\n\n"
                f"{exc_type.__name__}: {exc_value}",
            )
        except Exception:
            pass

    root.report_callback_exception = _on_error
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
