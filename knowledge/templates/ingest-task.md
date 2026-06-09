# Ingest：<书名/来源标题>

> **task-id**：ingest-YYYY-MM-DD-<slug>
> **时间**：YYYY-MM-DD HH:MM
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。断线回来 → 找第一个 `- [ ]` 继续。

## 来源

- [ ] 来源页：`knowledge/wiki/sources/<slug>.md`
- [ ] 源文件路径：`knowledge/converted/<tool>/<task-id>/.../<name>.md`
- [ ] 源类型：骨架层 / 填充层 / 标注层

## Step 1: 源页建结构

- [ ] 已读 KNOWLEDGE.md §Ingest（完整 11 步 + 行号标注规则）
- [ ] sources/ 页已建（按模板，含背景偏见 + 来源等级）
- [ ] 目录/全书结构页已建（entities/）
- [ ] 已读源文件全文（逐页逐行逐字，不跳过）

## Step 2: 报告发现

- [ ] 已向 boss 报告：核心要点、与已有页面关联、将要创建/更新的页面清单
- [ ] 已追加 `tasks/index.md`

## Step 3-N: 逐章全量提取

> 每章重复以下子清单。一本书一个 task-id，不另建任务文件。

### 第 N 章：<章节名>

- [ ] 已读本章源文本全段
- [ ] 全量实体提取（entities/）：逐一建页，不筛选
- [ ] 全量概念提取（concepts/）：逐一建页，不筛选
- [ ] 综合页（syntheses/）：有跨域关联即时建
- [ ] 所有新页原子写入（.tmp → 校验 → rename）
- [ ] 所有新页 frontmatter 必填字段已填满
- [ ] 所有新页 wikilink ≥ 最低阈值（entity≥1 / concept≥2 / synthesis≥3）
- [ ] 所有新页每条事实断言已标注源行号（强制两步验证）
- [ ] 跨章回溯：扫所有已建页，用本章新内容补充/修正/标记矛盾
- [ ] 更新 wiki/index.md
- [ ] 追加 wiki/log.md

## 收尾

- [ ] 所有章节提取完毕
- [ ] 全书跨章回溯最终检查
- [ ] 更新 sources/ 页的「产出页面清单」
- [ ] 重写 wiki/overview.md
- [ ] 文件移到 `tasks/done/`
- [ ] 已追加 `tasks/index.md`：done 行
- [ ] git commit: `ingest: <来源标题> — 全量提取 <N> pages`
- [ ] **回顾本清单**：所有已完成动作已 ✔，无遗漏 `- [ ]`
