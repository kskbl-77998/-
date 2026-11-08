# -*- coding: utf-8 -*-
"""位与位串的基础操作。

设计原则：本模块只做「位」层面的搬运，不做任何码制解释。
码制相关的逻辑放在 represent.py。

约定：位列表的 **索引 0 是最高位（符号位）**，索引 n-1 是最低位 b0。
      这与教材竖式的书写顺序一致。

负责人：张家昂
"""

from typing import List

# 支持的三种字长
SUPPORTED_WIDTHS = (4, 8, 16)


def _check_width(width: int) -> None:
    if width not in SUPPORTED_WIDTHS:
        raise ValueError(f"不支持的字长 {width}，只支持 {SUPPORTED_WIDTHS}")


def value_range(width: int) -> tuple:
    """返回该字长下补码能表示的闭区间 (最小值, 最大值)。

    >>> value_range(8)
    (-128, 127)
    """
    _check_width(width)
    return (-(1 << (width - 1)), (1 << (width - 1)) - 1)


def to_bits(value: int, width: int) -> List[int]:
    """把整数按补码转成长度为 width 的位列表，索引 0 为符号位。

    >>> to_bits(-5, 8)
    [1, 1, 1, 1, 1, 0, 1, 1]
    """
    _check_width(width)
    lo, hi = value_range(width)
    if not (lo <= value <= hi):
        raise OverflowError(f"{value} 超出 {width} 位补码范围 [{lo}, {hi}]")

    mask = (1 << width) - 1
    unsigned = value & mask          # 负数取到的是补码的位模式
    return [(unsigned >> (width - 1 - i)) & 1 for i in range(width)]


def from_bits(bits: List[int]) -> int:
    """把补码位列表（索引 0 为符号位）还原为带符号十进制真值。

    >>> from_bits([1, 0, 0, 0, 0, 0, 0, 0])
    -128
    """
    if not is_valid_bits(bits):
        raise ValueError("位串必须由 0/1 组成且非空")

    n = len(bits)
    value = 0
    for b in bits:
        value = (value << 1) | b
    if bits[0] == 1:                 # 符号位为 1 → 减去 2^n
        value -= 1 << n
    return value


def sign_bit(bits: List[int]) -> int:
    """返回符号位（最高位）。"""
    if not bits:
        raise ValueError("位串不能为空")
    return bits[0]


def invert(bits: List[int]) -> List[int]:
    """按位取反（含符号位）。"""
    return [1 - b for b in bits]


def pad_or_trim(bits: List[int], width: int) -> List[int]:
    """把位串补齐或截断到指定字长，用于切换字长时的处理。

    负数高位补 1、正数高位补 0；截断时保留低位、丢掉高位。
    """
    _check_width(width)
    if len(bits) == width:
        return list(bits)
    if len(bits) > width:
        return list(bits[-width:])
    fill = bits[0] if bits else 0
    return [fill] * (width - len(bits)) + list(bits)


def is_valid_bits(bits) -> bool:
    """校验一个序列是否只由 0/1 组成且非空。"""
    try:
        return len(bits) > 0 and all(b in (0, 1) for b in bits)
    except TypeError:
        return False


def to_string(bits: List[int]) -> str:
    """位列表转字符串，便于写日志。

    >>> to_string([1, 0, 1])
    '101'
    """
    return "".join(str(b) for b in bits)


def from_string(text: str) -> List[int]:
    """字符串转位列表，含非法字符时抛 ValueError。"""
    text = text.strip()
    if not text or any(ch not in "01" for ch in text):
        raise ValueError(f"不是合法的二进制串：{text!r}")
    return [int(ch) for ch in text]
