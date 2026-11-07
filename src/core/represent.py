# -*- coding: utf-8 -*-
"""四种码制的相互转换：原码 / 反码 / 补码 / 移码。

必须处理的三个特例（见设计文档 6.5）：
    1. 0 的原码与反码有两种（+0 / -0），补码唯一；
    2. -2^(n-1) 没有原码与反码表示，应返回 None 并由界面提示"不可表示"；
    3. 移码 = 补码符号位取反，用于阶码比较。

负责人：张家昂
"""

from typing import List, Optional


def to_sign_magnitude(value: int, width: int) -> Optional[List[int]]:
    """十进制真值 -> 原码。无法表示时返回 None。

    >>> to_sign_magnitude(-5, 8)
    [1, 0, 0, 0, 0, 1, 0, 1]

    >>> to_sign_magnitude(-128, 8) is None
    True
    """
    raise NotImplementedError("TODO(张家昂): 实现原码转换，注意 -2^(n-1) 返回 None")


def to_ones_complement(value: int, width: int) -> Optional[List[int]]:
    """十进制真值 -> 反码。无法表示时返回 None。"""
    raise NotImplementedError("TODO(张家昂): 实现反码转换")


def to_twos_complement(value: int, width: int) -> List[int]:
    """十进制真值 -> 补码。超出范围时抛 OverflowError。"""
    raise NotImplementedError("TODO(张家昂): 实现补码转换")


def to_offset_binary(value: int, width: int) -> List[int]:
    """十进制真值 -> 移码（补码符号位取反）。"""
    raise NotImplementedError("TODO(张家昂): 实现移码转换")


def four_codes(value: int, width: int) -> dict:
    """一次返回四种码制，供界面四码对照表直接使用。

    Returns:
        {
            "true": -5,
            "sign_magnitude": [1, 0, 0, 0, 0, 1, 0, 1] | None,
            "ones": [...] | None,
            "twos": [...],
            "offset": [...],
        }
    """
    raise NotImplementedError("TODO(张家昂): 汇总四种码制")
