# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
registry_lint.py — 命题登记表（SSOT）自检工具
配套《认知语义基元三论》导航卷使用，校验三框架统一命题登记表的内部一致性。

用法:
    python registry_lint.py [命题登记表.csv]

默认读取同目录下的 命题登记表.csv。
"""
import csv
import os
import sys
from collections import Counter


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "命题登记表.csv")
    if not os.path.exists(path):
        print(f"[错误] 找不到文件: {path}")
        sys.exit(1)

    rows = []
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row:
                rows.append(row)

    ids = [r[0] for r in rows]
    errors = []

    print(f"命题总数: {len(rows)}")
    print(f"表头: {header}")

    # 1) 重复 ID 检查
    dups = {k: v for k, v in Counter(ids).items() if v > 1}
    if dups:
        print(f"[P0] 重复 ID: {dups}")
        errors.append("duplicate_id")
    else:
        print("[OK] 无重复 ID")

    # 2) cart_source 列完整性（CART 相关行建议填 cart_source）
    missing = [r[0] for r in rows if len(r) < 6 or not r[5].strip()]
    if missing:
        sample = missing[:12]
        print(f"[提示] cart_source 为空 {len(missing)} 行（CSMT 原生条目可空，CART 条目应填）: {sample}")
    else:
        print("[OK] cart_source 列已全覆盖")

    # 3) 层级分布
    layers = Counter(r[1] for r in rows)
    print(f"层级分布: {dict(layers)}")

    # 4) 数量预期（与导航卷对齐）
    # 与导航卷 §一 SSOT 条数成对同步（2026-09-16 实测）
    expected = 274
    if len(rows) != expected:
        print(f"[提示] 当前 {len(rows)} 行，声明 SSOT 总量为 {expected} 条")
    else:
        print(f"[OK] 行数 == 声明总量 {expected}")

    if errors:
        print(f"\n自检未通过: {errors}")
        sys.exit(1)
    print("\n✅ SSOT 自检通过（无阻断级问题）")


if __name__ == "__main__":
    main()
