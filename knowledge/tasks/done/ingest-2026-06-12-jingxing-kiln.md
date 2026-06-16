# Ingest：<来源标题>

> **task-id**：ingest-YYYY-MM-DD-<slug>
> **时间**：YYYY-MM-DD HH:MM
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。断线回来 → 找第一个 `- [ ]` 继续。

## 来源

- [ ] 来源页：`knowledge/wiki/sources/<slug>.md`
- [ ] 源文件路径：`knowledge/converted/<tool>/<path>`
- [ ] 源类型：骨架层 / 填充层 / 标注层
- [ ] 批次切分方式：按章 / 按页码 / 按 converted 行号

## Step 1: 建结构

- [ ] 已读 KNOWLEDGE.md §Ingest（完整步骤 + 行号标注规则）
- [ ] 如首次 Ingest 此源：sources/ 页已建、全书结构页已建
- [ ] 已规划批次范围，见「批次记录」

## Step 2: 报告发现

- [ ] 已向 boss 报告：核心要点、与已有页面关联、将要创建/更新的页面清单

## Step 3: 全量实体提取

- [ ] 逐一建页，不筛选
- [ ] 原子写入（.tmp → 校验 → rename）
- [ ] frontmatter 必填字段已填满
- [ ] wikilink ≥ 最低阈值（entity≥1 / concept≥2 / synthesis≥3）
- [ ] 每条事实断言已标注源行号（强制两步验证）

## Step 4: 全量概念提取

- [ ] 逐一建页，不筛选
- [ ] 原子写入 + frontmatter + wikilink + 行号标注

## Step 5: 综合页

- [ ] 有跨域关联即时建 syntheses/ 页，无则跳过

## Step 6: 跨章回溯

- [ ] 扫所有已建页面，用本次新内容补充/修正/标记矛盾
- [ ] 已记录本批回溯页面及判断结果
- [ ] 已更新受影响的已有页面

## 批次记录

> 每批完成后追加一条。没有批次记录，不算完成该批。

### Batch 1：<章节 / 页码 / 行号范围>

- [ ] 计划范围：
- [ ] 已读范围（converted 行号）：
- [ ] 新建页面：
- [ ] 更新页面：
- [ ] 回溯页面：
  - `<页面>`：已更新 / 无需更新 / 有冲突待处理
- [ ] 未处理/疑问：
- [ ] 本批 citation 行号均落在已读范围内；如引用其他批次，已说明原因

## Step 7: 更新枢纽

- [ ] 更新 wiki/index.md
- [ ] 追加 wiki/log.md
- [ ] 重生成 wiki/MOC.md（`python3 tools/gen_moc.py`）

## 收尾

- [ ] 更新 sources/ 页的「产出页面清单」
- [ ] 重写 wiki/overview.md
- [ ] 已准备提交摘要：`ingest: <来源标题> — <N> pages`
- [ ] boss 确认后再执行 git commit
- [ ] 文件移到 `tasks/done/`
- [ ] **回顾本清单**：所有已完成动作已 ✔，无遗漏 `- [ ]`
