# 原子写入规则

> 所有 wiki 页面的写入必须遵循此规则。依据 CLAUDE.md——rename 是原子系统调用，不留半截文件。

## 流程

```
1. 写入临时文件
   write path="wiki/.../page.md.tmp"

2. 校验
   - frontmatter 可解析（`---` 开头，YAML 合法）
   - body ≥ 50 字符（非空页）
   - provenanceState 字段存在且合法
   - confidence 在 0.0-1.0 范围

3. 校验通过 → 原子 rename
   mv page.md.tmp page.md

4. 校验失败 → 删 .tmp，重写
```

## 为什么不用直接覆写

- Write/Edit 直接覆写目标文件 → 中断可留截断页面
- rename 是原子系统调用 → 要么旧文件完整，要么新文件完整

## 执行方式

当前必须执行 `.tmp → 校验 → rename`。如果校验脚本尚未存在，不得声称已运行脚本；按上方字段逐项手动校验后再 rename。

```bash
# 待补工具：tools/validate-page.sh
# 存在时可用脚本校验；不存在时执行手动校验
bash tools/validate-page.sh wiki/entities/xxx.md.tmp && \
  mv wiki/entities/xxx.md.tmp wiki/entities/xxx.md
```

## 适用范围

- `wiki/sources/`、`wiki/entities/`、`wiki/concepts/`、`wiki/syntheses/` 下所有 `.md` 页面
- 不适用于 hub 文件（index.md / log.md / overview.md）——这些是追加/覆写或脚本生成模式
