# -*- coding: utf-8 -*-
"""逐列全加器：返回每一列的完整输入输出，供界面画进位箭头。

负责人：成员B
"""

from typing import List, Tuple

from .models import BitColumn


def add(a_bits: List[int], b_bits: List[int]) -> Tuple[List[int], List[BitColumn], int]:
    """逐列相加两个等长补码位串。

    Args:
        a_bits: 被加数，索引 0 为符号位。
        b_bits: 加数，索引 0 为符号位。

    Returns:
        (sum_bits, columns, c_out)
            sum_bits: 结果位列表
            columns: 每列的 BitColumn，长度等于字长
            c_out: 符号位向外的进位 C_n

    >>> s, cols, c = add([0,0,0,0,0,1,0,1], [0,0,0,0,1,1,0,0])
    >>> c
    0
    """
    raise NotImplementedError("TODO(成员B): 实现逐列全加，注意从 b0 开始进位")


def add_one(bits: List[int]) -> Tuple[List[int], List[int]]:
    """末位加一，返回 (结果位串, 进位链)。求补的第二步复用此函数。"""
    raise NotImplementedError("TODO(成员B): 实现末位加一")
