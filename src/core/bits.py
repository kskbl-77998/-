# -*- coding: utf-8 -*-
"""位与位串的基础操作。

设计原则：本模块只做"位"层面的搬运，不做任何码制解释。
码制相关的逻辑放在 represent.py。

负责人：成员B
"""

from typing import List

# 支持的三种字长
SUPPORTED_WIDTHS = (4, 8, 16)


def value_range(width: int) -> tuple:
    """返回该字长下补码能表示的闭区间 (最小值, 最大值)。

    >>> value_range(8)
    (-128, 127)
    """
    if width not in SUPPORTED_WIDTHS:
        raise ValueError(f"不支持的字长: {width}")
    return (-(1 << (width - 1)), (1 << (width - 1)) - 1)


def to_bits(value: int, width: int) -> List[int]:
    """把整数按补码转成长度为 width 的位列表，索引 0 为符号位。

    >>> to_bits(-5, 8)
    [1, 1, 1, 1, 1, 0, 1, 1]
    """
    raise NotImplementedError("TODO(成员B): 实现 to_bits，注意越界检查")


def from_bits(bits: List[int]) -> int:
    """把补码位列表（索引 0 为符号位）还原为带符号十进制真值。

    >>> from_bits([1, 0, 0, 0, 0, 0, 0, 0])
    -128
    """
    raise NotImplementedError("TODO(成员B): 实现 from_bits")


def sign_bit(bits: List[int]) -> int:
    """返回符号位（最高位）。"""
    raise NotImplementedError("TODO(成员B): 实现 sign_bit")


def invert(bits: List[int]) -> List[int]:
    """按位取反（含符号位）。"""
    raise NotImplementedError("TODO(成员B): 实现 invert")


def pad_or_trim(bits: List[int], width: int) -> List[int]:
    """把位串补齐或截断到指定字长，用于切换字长时的处理。"""
    raise NotImplementedError("TODO(成员B): 实现 pad_or_trim")


def is_valid_bits(bits) -> bool:
    """校验一个序列是否只由 0/1 组成。"""
    raise NotImplementedError("TODO(成员B): 实现 is_valid_bits")
