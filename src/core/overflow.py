# -*- coding: utf-8 -*-
"""溢出判定：三种方法并列，结论必须一致。

   ① 单符号位：V = C_n ⊕ C_(n-1)
   ② 双符号位（变形补码）：00/11 正常，01 正溢，10 负溢
   ③ 操作数符号法：同号相加得异号 -> 溢出

⚠️ 不变量：三种方法结论一致。一致性校验写进单元测试。

负责人：张家昂
"""

from typing import List

from .models import OverflowReport


def detect(a_bits: List[int], b_bits: List[int], sum_bits: List[int], c_out: int) -> OverflowReport:
    """判定一次加法是否溢出。

    Args:
        a_bits: 被加数补码位串。
        b_bits: 加数补码位串。
        sum_bits: 结果补码位串。
        c_out: 符号位向外的进位 C_n。

    Returns:
        OverflowReport，其中 method_results 需包含三种方法的文字结论，
        consistent 表示三者是否一致。
    """
    raise NotImplementedError("TODO(张家昂): 实现三种判定并校验一致性")


def validate_consistent(report: OverflowReport) -> None:
    """断言三种方法结论一致，不一致则抛 AssertionError。供测试调用。"""
    raise NotImplementedError("TODO(张家昂): 实现一致性断言")
