# -*- coding: utf-8 -*-
"""溢出判定：三种方法并列，结论必须一致。

    ① 单符号位：V = C_n ⊕ C_(n−1)
    ② 双符号位（变形补码）：结果高两位 00/11 正常，01 正溢，10 负溢
    ③ 操作数符号法：同号相加得异号 → 溢出

⚠️ 不变量：三种方法结论一致。一致性校验写进单元测试。

负责人：张家昂
"""

from typing import List

from .models import OverflowReport


def _carry_into_sign(a_bits: List[int], b_bits: List[int]) -> int:
    """重算进位链，取出「最高数值位 → 符号位」的进位 C_(n−1)。

    之所以在这里重算而不是要求调用方传进来，是为了保持 detect() 的签名简单：
    只会用到 n 次加法，代价可以忽略。
    """
    n = len(a_bits)
    carry = 0
    c_sign_in = 0
    for bit in range(n):
        i = n - 1 - bit
        carry = (a_bits[i] + b_bits[i] + carry) >> 1
        if i == 1:                       # 第 1 位（次高位）的进位输出 = 进入符号位的进位
            c_sign_in = carry
    return c_sign_in


def detect(a_bits: List[int], b_bits: List[int], sum_bits: List[int], c_out: int) -> OverflowReport:
    """判定一次加法是否溢出。

    Args:
        a_bits: 被加数补码位串。
        b_bits: 加数补码位串。
        sum_bits: 结果补码位串。
        c_out: 符号位向外的进位 C_n。

    Returns:
        OverflowReport，method_results 含三种方法的文字结论，
        consistent 表示三者是否一致。
    """
    n = len(a_bits)
    c_sign_in = _carry_into_sign(a_bits, b_bits)

    # ① 单符号位：两个进位不同 → 溢出
    v_xor = c_out ^ c_sign_in

    # ② 双符号位：把两个操作数各扩展一位符号位后再加，
    #    结果的高两位是 (第二个符号位的和, 原符号位 S_msb)，进位丢弃。
    #    00/11 正常，01 正溢，10 负溢。
    second_sign = (a_bits[0] + b_bits[0] + c_out) & 1
    high2 = (second_sign, sum_bits[0])
    v_dual = high2 in ((0, 1), (1, 0))
    if high2 == (0, 1):
        dual_text = "扩展结果 01 → 正溢出"
    elif high2 == (1, 0):
        dual_text = "扩展结果 10 → 负溢出"
    else:
        dual_text = f"扩展结果 {high2[0]}{high2[1]} → 正常"

    # ③ 操作数符号法：同号相加却得到异号
    v_sign = (a_bits[0] == b_bits[0]) and (sum_bits[0] != a_bits[0])
    if a_bits[0] != b_bits[0]:
        sign_text = "异号相加，结果符号不可能是错的 → 不溢出"
    elif v_sign:
        sign_text = f"同号（{a_bits[0]}）相加却得到 {sum_bits[0]} → 溢出"
    else:
        sign_text = f"同号（{a_bits[0]}）相加得到 {sum_bits[0]} → 不溢出"

    method_results = [
        ("单符号位", bool(v_xor),
         f"V = C{n} ⊕ C{n - 1} = {c_out} ⊕ {c_sign_in} = {v_xor}"),
        ("双符号位", bool(v_dual), dual_text),
        ("操作数符号法", bool(v_sign), sign_text),
    ]

    consistent = len({bool(v_xor), bool(v_dual), bool(v_sign)}) == 1

    return OverflowReport(
        overflowed=bool(v_xor),
        c_out=c_out,
        c_sign_in=c_sign_in,
        method_results=method_results,
        consistent=consistent,
    )


def validate_consistent(report: OverflowReport) -> None:
    """断言三种方法结论一致，不一致则抛 AssertionError。供测试调用。"""
    if not report.consistent:
        detail = "；".join(f"{name}={'溢出' if v else '正常'}" for name, v, _ in report.method_results)
        raise AssertionError(f"三种溢出判定结论不一致：{detail}")
