# -*- coding: utf-8 -*-
"""求补：[−X]补 = ~[X]补 + 1（连同符号位整体取反再加一）。

⚠️ 边界：X = −2^(n−1) 时 −X 超出表示范围，本函数返回 None，
   由上层（engine）转换成「该数无相反数」的提示。

负责人：张家昂
"""

from typing import List, Optional, Tuple

from .adders import add_one
from .bits import from_bits, invert, to_string
from .models import PHASE_ADD_ONE, PHASE_INVERT


def negate(bits: List[int]) -> Optional[Tuple[List[int], List[int], List[dict]]]:
    """对补码位串求补，返回 (结果位串, 进位链, 步骤 trace)。

    Args:
        bits: 补码位列表，索引 0 为符号位。

    Returns:
        (result_bits, carry_chain, trace)
            result_bits: 求补结果的位列表
            carry_chain: 每一位送出的进位，长度与 bits 相同
            trace: 逐步说明，每项形如
                {"index": 1, "phase": "invert", "col": None, "detail": "..."}
        若该数无相反数（如 8 位的 −128），返回 None。

    >>> negate([0, 0, 0, 0, 0, 1, 0, 1])[0]
    [1, 1, 1, 1, 1, 0, 1, 1]

    >>> negate([1, 0, 0, 0, 0, 0, 0, 0]) is None
    True
    """
    n = len(bits)
    if n == 0:
        raise ValueError("位串不能为空")

    value = from_bits(bits)
    if value == -(1 << (n - 1)):         # 只有它没有相反数
        return None

    inverted = invert(bits)
    result, carries = add_one(inverted)

    trace = [{
        "index": 1,
        "phase": PHASE_INVERT,
        "col": None,
        "detail": (f"连同符号位整体取反：{to_string(bits)} → {to_string(inverted)}"
                   f"（共 {n} 位，符号位也参与）"),
    }]

    # 加一时，只有在「进位真正传过去」的位上才值得生成一条步骤
    for bit in range(n):
        carry = carries[bit]
        digit = result[n - 1 - bit]
        if bit == 0:
            detail = f"末位 b0 加 1：{inverted[n - 1]} + 1 = {digit}，向 b1 进位 {carry}"
        else:
            detail = (f"第 b{bit} 位：{inverted[n - 1 - bit]} + 进位 {carries[bit - 1]} "
                      f"= {digit}，向高位进位 {carry}")
        trace.append({
            "index": len(trace) + 1,
            "phase": PHASE_ADD_ONE,
            "col": bit,
            "detail": detail,
        })

    trace.append({
        "index": len(trace) + 1,
        "phase": PHASE_ADD_ONE,
        "col": None,
        "detail": f"求补完成：[−X]补 = {to_string(result)}（真值 {from_bits(result)}）",
    })

    return result, carries, trace
