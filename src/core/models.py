# -*- coding: utf-8 -*-
"""核心数据结构：界面与算法之间的唯一契约。

⚠️ 接口冻结说明（马子尊，第 2 周）
    本文件中的字段名与语义一经发布即冻结，后续只允许**追加**字段（带默认值），
    不允许重命名或改变语义。界面开发（成员C / 成员D）依赖这些字段名。

作者：马子尊
"""

from dataclasses import dataclass, field
from typing import List, Optional

# 步骤所处的阶段，界面据此决定高亮样式
PHASE_LOAD = "load"        # 载入操作数
PHASE_NEGATE = "negate"    # 减法时求 [-Y]补
PHASE_INVERT = "invert"    # 按位取反
PHASE_ADD_ONE = "add_one"  # 末位加一
PHASE_ADD = "add"          # 逐列相加
PHASE_RESULT = "result"    # 结论


@dataclass(frozen=True)
class BitColumn:
    """一列全加器的完整输入输出，供界面逐列渲染。

    Attributes:
        index: 位序号，0 为最低位 b0。
        a: 被加数（[X]补）在该位的值。
        b: 加数（[Y]补 或 [-Y]补）在该位的值。
        cin: 来自低位的进位。
        s: 本位和。
        cout: 向高位的进位。
    """

    index: int
    a: int
    b: int
    cin: int
    s: int
    cout: int


@dataclass
class Step:
    """一个可播放的演示步骤。

    Attributes:
        index: 步骤序号，从 1 开始，用于日志编号。
        phase: 阶段常量，取 PHASE_* 之一。
        title: 短标题，日志首行。
        detail: 中文解释，日志正文。
        highlight: 需要高亮的位序号列表（空表示不高亮任何位）。
        column: 需要高亮的列序号，用于进位动画；None 表示不高亮列。
    """

    index: int
    phase: str
    title: str
    detail: str
    highlight: List[int] = field(default_factory=list)
    column: Optional[int] = None


@dataclass
class OverflowReport:
    """溢出判定报告：三种方法必须给出一致结论。

    Attributes:
        overflowed: 最终结论，True 表示溢出。
        c_out: 符号位向外的进位 C_n。
        c_sign_in: 最高数值位向符号位的进位 C_(n-1)。
        method_results: 三种方法的文字结论，形如
            [("单符号位", True, "V = C8 ⊕ C7 = 1"), ...]。
        consistent: 三种方法结论是否一致。为 False 说明实现有 Bug。
    """

    overflowed: bool
    c_out: int
    c_sign_in: int
    method_results: List[tuple] = field(default_factory=list)
    consistent: bool = True


@dataclass
class Scenario:
    """一次完整运算的全部结果。界面只读，不做任何计算。

    Attributes:
        width: 字长 n。
        op: 运算符，取 "+" 或 "-"。
        x_true: 操作数 X 的十进制真值。
        y_true: 操作数 Y 的十进制真值。
        x_bits: [X]补 的位列表，索引 0 为符号位。
        y_bits: [Y]补 的位列表。
        neg_y_bits: 减法时为 [-Y]补；加法时为 None。
        result_bits: 运算结果的补码位列表。
        columns: 逐列加法明细，长度等于字长。
        overflow: 溢出报告。
        steps: 可播放的步骤序列。
        machine_value: 结果补码反解出的真值（机器认为的值）。
        math_value: 数学上正确的结果（可能与 machine_value 不同）。
    """

    width: int
    op: str
    x_true: int
    y_true: int
    x_bits: List[int]
    y_bits: List[int]
    neg_y_bits: Optional[List[int]]
    result_bits: List[int]
    columns: List[BitColumn]
    overflow: OverflowReport
    steps: List[Step]
    machine_value: int
    math_value: int
