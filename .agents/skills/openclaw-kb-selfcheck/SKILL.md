---
name: openclaw-kb-selfcheck
description: 对 OpenClaw 本地知识库做一致性自检。扫描 knowledge/ 的结构缺失、试验产物泄漏、wiki/index/log 与实际脱节、任务文件格式不规范、tasks 总账与任务文件状态不一致、收录任务卡在 running 未走完六项。Use when 用户要求检查/整理知识库、收录任务收尾前自检、怀疑 knowledge 目录乱、或排查 wiki/index.md / wiki/log.md / tasks/index.md 与实际不一致。
---

# OpenClaw 知识库自检

## 什么时候用

- 用户说「检查知识库」「knowledge 乱了」「整理一下」
- 一个收录任务准备移出 `tasks/running/` 之前的收尾自检
- 怀疑 `index.md` / `log.md` 与实际文件脱节
- 怀疑试验产物（MinerU 中间 JSON、临时脚本）混进了 `knowledge/`

## 怎么用

跑只读脚本，拿到分级报告（不会改任何文件）：

```bash
python .agents/skills/openclaw-kb-selfcheck/scripts/selfcheck.py
```

需要机器可读输出时加 `--json`。退出码：有 FAIL 项返回 1，否则 0。

## 报告分级

- `FAIL`：违反硬规则，必须修。结构缺目录、`wiki/index.md` / `wiki/log.md` 与实际矛盾。
- `WARN`：待整理，不阻断。试验产物泄漏、任务格式不规范、`tasks/index.md` 与任务文件进度不一致、running ingest 链未走完。
- `OK`：无问题。

## 检查项与对应规则

脚本检查的就是收录最容易跳步的几处，对应 `KNOWLEDGE.md` 与 `templates/ingest-task.md` 的六项清单：

| 检查 | 含义 | 依据 |
|------|------|------|
| structure | `knowledge/` 必需目录/文件齐全 | KNOWLEDGE.md 目录结构 |
| experiment-leak | `inbox/` `converted/` 里出现 `*_middle.json` / `*_model.json` / `*_content_list*.json` / 脚本 | 试验产物只能放仓库根 `experiments/` |
| index-sync | `wiki/index.md` 的四分区（sources/entities/concepts/syntheses）与实际页数/占位文案脱节 | 清单第 4 项 |
| log-sync | `wiki/log.md` 写「暂无记录」但 tasks/ 已有任务 | 清单第 5 项、RULES.md 任务日志 |
| task-format | 任务应为 checklist 风格 `.md`，包含 `task-id`；JSON 任务报 WARN | templates/ingest-task.md |
| stuck-ingest | `running/` 的 ingest 任务存在，但 `wiki/sources/` 为空，收录链未走完 | 清单第 3/6 项 |
| task-index-sync | `tasks/index.md` 的状态与任务文件所在目录/步骤不一致 | tasks/index.md 状态机 |

## 处理顺序

1. 先修所有 `FAIL`（否则视为知识库不一致）。
2. 再逐条处理 `WARN`：试验产物迁到 `experiments/`、补任务元信息、修正 `tasks/index.md` 状态、把走完六项的任务移到 `done/`。
3. 涉及**删除或移动文件**时，先向用户确认（`RULES.md` 操作安全条款）。
4. 修完重跑脚本，直到 `FAIL=0`。

## 边界

- 本 Skill 只读、只报告，不自动修复。修复动作由 Agent 按报告执行，并遵守确认规则。
- 六项收录清单的权威定义在 `knowledge/templates/ingest-task.md`，脚本只做可自动判定部分的近似校验。
