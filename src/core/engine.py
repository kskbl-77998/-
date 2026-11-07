# -*- coding: utf-8 -*-
"""编排层：把一次运算拆成可播放的步骤序列。

职责边界：
    - 校验输入（范围、字长、运算符）；
    - 调用 bits / represent / negate / adders / overflow；
    - 组装 Scenario，**不产生任何界面依赖**。

负责人：马子尊
"""

from .models import Scenario


class InputError(ValueError):
    """输入非法（超出范围、格式错误等），由界面转为状态栏提示。"""


def build_scenario(x_true: int, y_true: int, op: str, width: int) -> Scenario:
    """构造一次完整运算的演示场景。

    Args:
        x_true: 操作数 X 的十进制真值。
        y_true: 操作数 Y 的十进制真值。
        op: "+" 或 "-"。
        width: 字长，取 4 / 8 / 16。

    Returns:
        Scenario。

    Raises:
        InputError: 输入超出该字长范围，或运算符非法。
    """
    raise NotImplementedError("TODO(马子尊): 串联四步算法生成 Scenario")


def parse_operand(text: str, width: int, base: str = "dec") -> int:
    """把用户输入解析为十进制真值。

    Args:
        text: 用户输入，例如 "-5"、"11111011"。
        width: 当前字长。
        base: "dec" 按十进制真值解析；"bin" 按补码位串解析。

    Raises:
        InputError: 空串、非法字符或超出范围。

    >>> parse_operand("-5", 8)
    -5
    """
    raise NotImplementedError("TODO(马子尊): 实现输入解析与校验")
