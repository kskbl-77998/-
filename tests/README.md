# 测试目录

本目录存放核心算法层的单元测试（`pytest`）。

## 运行

```bash
python -m pytest tests/ -v
python -m pytest tests/ --cov=src/core --cov-report=term-missing   # 需安装 pytest-cov
```

## 组织方式

| 文件 | 覆盖模块 | 负责人 |
| :--- | :--- | :--- |
| `test_bits.py` | `src/core/bits.py` | 成员E（成员B 提供断言） |
| `test_represent.py` | `src/core/represent.py` | 成员E |
| `test_negate.py` | `src/core/negate.py` | 成员E |
| `test_adders.py` | `src/core/adders.py` | 成员E |
| `test_overflow.py` | `src/core/overflow.py` | 成员E |
| `test_engine.py` | `src/core/engine.py` | 成员E |
| `test_random_fuzz.py` | 全核心层随机对拍 | 成员B |

## 用例来源

测试用例以 [`docs/Test_Case_Matrix.md`](../docs/Test_Case_Matrix.md) 为准，
每条 TC 编号对应至少一个测试函数，函数名带编号，例如：

```python
def test_tc02_pos_plus_pos_overflow():
    """TC-02：100 + 50 在 8 位下正溢出，机器结果 -106。"""
```

## 必须覆盖的边界

1. `−2^(n-1)`（如 8 位 `−128`）求补无结果；
2. `−128` 没有原码与反码；
3. `0` 的原码有两种表示，补码唯一；
4. `C_n` 与 `C_(n-1)` 同时为 1 时不溢出（两个负数相加的正常情况）；
5. 三种溢出判定在同一用例上结论必须一致。
