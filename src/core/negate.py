# -*- coding: utf-8 -*-
"""求补：[−X]补 = ~[X]补 + 1（连同符号位整体取反再加一）。

⚠️ 边界：X = -2^(n-1) 时 -X 超出表示范围，本函数返回 None，
   由上层（engine）转换为"该数无相反数"的提示。

负责人：成员B
"""

from typing import List, Optional, Tuple


def negate(bits: List[int]) -> Optional[Tuple[List[int], List[int], List[dict]]]:
    """对补码位串求补，返回 (结果位串, 进位链, 步骤 trace)。

    Args:
        bits: 补码位列表，索引 0 为符号位。

    Returns:
        (result_bits, carry_chain, trace)
            result_bits: 求补结果的位列表
            carry_chain: 每一位的进位，长度与 bits 相同
            trace: 逐步说明，每项形如
                {"index": 1, "phase": "invert", "col": 3, "detail": "..."}
        若该数无相反数（如 8 位的 -128），返回 None。

    >>> negate([0, 0, 0, 0, 0, 1, 0, 1])[0]
    [1, 1, 1, 1, 1, 0, 1, 1]

    >>> negate([1, 0, 0, 0, 0, 0, 0, 0]) is None
    True
    """
    raise NotImplementedError("TODO(成员B): 实现求补，含 -2^(n-1) 边界")
