# -*- coding: utf-8 -*-
"""逐列全加器：返回每一列的完整输入输出，供界面画进位箭头。

进位从最低位 b0 开始，逐列向高位传递：
    A + B + Cin = 2·Cout + S

负责人：张家昂
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
            sum_bits: 结果位列表（索引 0 为符号位）
            columns: 每列的 BitColumn，索引 0 是最低位 b0
            c_out: 符号位向外的进位 C_n（补码加法里被丢弃）

    >>> s, cols, c = add([0,0,0,0,0,1,0,1], [0,0,0,0,1,1,0,0])
    >>> c
    0
    """
    if len(a_bits) != len(b_bits):
        raise ValueError("两个操作数必须等长")
    if not a_bits:
        raise ValueError("操作数不能为空")

    n = len(a_bits)
    columns: List[BitColumn] = []
    carry = 0

    for bit in range(n):                 # bit=0 是最低位 b0
        i = n - 1 - bit                  # 对应列表下标
        total = a_bits[i] + b_bits[i] + carry
        columns.append(BitColumn(
            index=bit,
            a=a_bits[i],
            b=b_bits[i],
            cin=carry,
            s=total & 1,
            cout=total >> 1,
        ))
        carry = total >> 1

    sum_bits = [0] * n
    for col in columns:
        sum_bits[n - 1 - col.index] = col.s

    return sum_bits, columns, carry


def add_one(bits: List[int]) -> Tuple[List[int], List[int]]:
    """末位加一，返回 (结果位串, 进位链)。

    进位链 carries[bit] 表示第 bit 列向高位送出的进位（bit=0 为最低位）。
    求补的第二步直接复用本函数。
    """
    n = len(bits)
    if n == 0:
        raise ValueError("位串不能为空")

    result = list(bits)
    carries = [0] * n
    carry = 1                            # 末位加的那个 1

    for bit in range(n):
        i = n - 1 - bit
        total = result[i] + carry
        result[i] = total & 1
        carry = total >> 1
        carries[bit] = carry             # 本列送出的进位

    return result, carries
