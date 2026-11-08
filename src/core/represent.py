# -*- coding: utf-8 -*-
"""四种码制的相互转换：原码 / 反码 / 补码 / 移码。

三个必须处理的特例（见设计文档 6.5）：
    1. 0 的原码与反码有两种（+0 / −0），补码唯一；
    2. −2^(n-1) 没有原码与反码表示，返回 None，由界面提示「不可表示」；
    3. 移码 = 补码符号位取反，用于阶码比较。

负责人：张家昂
"""

from typing import List, Optional

from .bits import _check_width, to_bits, value_range


def _magnitude(value: int, bits: int) -> List[int]:
    """把非负整数转成定长位列表（不做符号处理）。"""
    return [(value >> (bits - 1 - i)) & 1 for i in range(bits)]


def to_sign_magnitude(value: int, width: int) -> Optional[List[int]]:
    """十进制真值 -> 原码。无法表示时返回 None。

    >>> to_sign_magnitude(-5, 8)
    [1, 0, 0, 0, 0, 1, 0, 1]

    >>> to_sign_magnitude(-128, 8) is None
    True
    """
    _check_width(width)
    lo, hi = value_range(width)
    if not (lo <= value <= hi):
        raise OverflowError(f"{value} 超出 {width} 位范围 [{lo}, {hi}]")

    # −2^(n−1) 的绝对值放不进 n−1 位数值位
    if value == lo:
        return None

    if value >= 0:
        return [0] + _magnitude(value, width - 1)
    return [1] + _magnitude(-value, width - 1)


def to_ones_complement(value: int, width: int) -> Optional[List[int]]:
    """十进制真值 -> 反码。无法表示时返回 None。

    正数与 +0 的反码与原码相同；负数是「符号位不变、数值位取反」。
    """
    sm = to_sign_magnitude(value, width)
    if sm is None:
        return None
    if value >= 0:
        return sm
    return [1] + [1 - b for b in sm[1:]]


def to_twos_complement(value: int, width: int) -> List[int]:
    """十进制真值 -> 补码。超出范围时抛 OverflowError。

    直接复用 bits.to_bits：整数取掩码后就是补码位模式，最省事也最不容易错。
    """
    return to_bits(value, width)


def to_offset_binary(value: int, width: int) -> List[int]:
    """十进制真值 -> 移码（补码符号位取反）。"""
    bits = to_twos_complement(value, width)
    return [1 - bits[0]] + bits[1:]


def four_codes(value: int, width: int) -> dict:
    """一次返回四种码制，供界面四码对照表直接使用。

    Returns:
        {
            "true": -5,
            "sign_magnitude": [...] | None,
            "ones": [...] | None,
            "twos": [...],
            "offset": [...],
        }
    """
    return {
        "true": value,
        "sign_magnitude": to_sign_magnitude(value, width),
        "ones": to_ones_complement(value, width),
        "twos": to_twos_complement(value, width),
        "offset": to_offset_binary(value, width),
    }
