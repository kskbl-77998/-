# -*- coding: utf-8 -*-
"""编排层：把一次运算拆成可播放的步骤序列。

职责边界：
    - 校验输入（范围、字长、运算符）；
    - 调用 bits / represent / negate / adders / overflow；
    - 组装 Scenario，**不产生任何界面依赖**。

界面拿到 Scenario 后只负责"把 steps[i] 画出来"，不再做任何计算。

负责人：马子尊
"""

from typing import List

from .adders import add
from .bits import from_bits, to_bits, to_string, value_range
from .models import (PHASE_ADD, PHASE_LOAD, PHASE_NEGATE, PHASE_RESULT, Scenario,
                     Step)
from .negate import negate
from .overflow import detect


class InputError(ValueError):
    """输入非法（超出范围、格式错误等），由界面转为状态栏提示。"""


def _bits_str(bits: List[int]) -> str:
    """把位列表格式化成 4 位一组的字符串，便于阅读。"""
    text = to_string(bits)
    groups = [text[i:i + 4] for i in range(0, len(text), 4)]
    return " ".join(groups)


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

    >>> parse_operand("11111011", 8, "bin")
    -5
    """
    if width not in (4, 8, 16):
        raise InputError(f"不支持的字长 {width}")

    text = (text or "").strip()
    if not text:
        raise InputError("不能为空")

    lo, hi = value_range(width)

    if base == "dec":
        try:
            value = int(text)
        except ValueError:
            raise InputError(f"「{text}」不是整数")
        if not (lo <= value <= hi):
            raise InputError(f"超出 {width} 位补码范围 [{lo}, {hi}]")
        return value

    if base == "bin":
        raw = text.replace(" ", "").replace("_", "")
        if any(ch not in "01" for ch in raw):
            raise InputError("补码串只能包含 0 和 1")
        if len(raw) != width:
            raise InputError(f"需要 {width} 位，你输入了 {len(raw)} 位")
        return from_bits([int(ch) for ch in raw])

    raise InputError(f"不支持的输入进制：{base}")


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

    >>> sc = build_scenario(-5, 12, "+", 8)
    >>> sc.machine_value, sc.math_value
    (7, 7)
    """
    if op not in ("+", "-"):
        raise InputError(f"不支持的运算符：{op}")
    if width not in (4, 8, 16):
        raise InputError(f"不支持的字长：{width}")

    lo, hi = value_range(width)
    for name, v in (("X", x_true), ("Y", y_true)):
        if not (lo <= v <= hi):
            raise InputError(f"{name} = {v} 超出 {width} 位范围 [{lo}, {hi}]")

    steps: List[Step] = []

    def add_step(phase: str, title: str, detail: str,
                 highlight=None, column=None) -> None:
        steps.append(Step(
            index=len(steps) + 1,
            phase=phase,
            title=title,
            detail=detail,
            highlight=list(highlight or []),
            column=column,
        ))

    # ---- 1. 载入两个操作数 ----
    x_bits = to_bits(x_true, width)
    y_bits = to_bits(y_true, width)
    add_step(PHASE_LOAD, "载入 X",
             f"X = {x_true} → [X]补 = {_bits_str(x_bits)}",
             highlight=range(width))
    add_step(PHASE_LOAD, "载入 Y",
             f"Y = {y_true} → [Y]补 = {_bits_str(y_bits)}",
             highlight=range(width))

    # ---- 2. 减法先把 Y 求补成 [−Y]补 ----
    neg_y_bits = None
    if op == "-":
        result = negate(y_bits)
        if result is None:
            raise InputError(
                f"Y = {y_true} 的相反数超出 {width} 位表示范围，无法做减法")
        neg_y_bits, _carries, trace = result
        add_step(PHASE_NEGATE, "减法转加法",
                 f"[X − Y]补 = [X]补 + [−Y]补，先对 [Y]补 = {_bits_str(y_bits)} 求补",
                 highlight=range(width))
        for item in trace:
            add_step(item["phase"], "求补", item["detail"], column=item.get("col"))

    addend = neg_y_bits if neg_y_bits is not None else y_bits

    # ---- 3. 逐列相加 ----
    sum_bits, columns, c_out = add(x_bits, addend)
    for col in columns:
        bit = col.index                       # 0 是最低位 b0
        total = col.a + col.b + col.cin
        if bit == width - 1:                  # 符号位
            detail = (f"{col.a} + {col.b} + 进位 {col.cin} = {total}，本位写 {col.s}，"
                      f"向符号位外送出进位 C{width} = {col.cout}"
                      f"（补码加法中丢弃，但溢出判定要用）")
        else:
            detail = (f"{col.a} + {col.b} + 进位 {col.cin} = {total}，"
                      f"本位写 {col.s}，向 b{bit + 1} 进位 {col.cout}")
        add_step(
            PHASE_ADD,
            f"第 b{bit} 位" + ("（符号位）" if bit == width - 1 else ""),
            detail,
            highlight=[width - 1 - bit],
            column=bit,
        )

    # ---- 4. 结论 ----
    report = detect(x_bits, addend, sum_bits, c_out)
    machine_value = from_bits(sum_bits)
    math_value = x_true + y_true if op == "+" else x_true - y_true

    detail = (f"结果 [S]补 = {_bits_str(sum_bits)}，按补码读作 {machine_value}"
              f"（数学结果 {math_value}）")
    if report.overflowed:
        detail += "。V = 1，发生溢出，机器结果不可信"
    else:
        detail += "。V = 0，未溢出，结果可信"
    add_step(PHASE_RESULT, "结果与溢出", detail, highlight=range(width))

    return Scenario(
        width=width,
        op=op,
        x_true=x_true,
        y_true=y_true,
        x_bits=x_bits,
        y_bits=y_bits,
        neg_y_bits=neg_y_bits,
        result_bits=sum_bits,
        columns=columns,
        overflow=report,
        steps=steps,
        machine_value=machine_value,
        math_value=math_value,
    )
