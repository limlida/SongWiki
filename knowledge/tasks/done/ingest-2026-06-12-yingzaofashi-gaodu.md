# Ingest：从《营造法式》解析宋代建筑高度

> **task-id**：ingest-2026-06-12-yingzaofashi-gaodu
> **时间**：2026-06-12 10:00
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。断线回来 → 找第一个 `- [ ]` 继续。

## 来源

- [x] 来源页：`knowledge/wiki/sources/营造法式建筑高度考.md`
- [x] 源文件路径：`knowledge/converted/mineru/convert-2026-06-12-yingzaofashi-gaodu/从《营造法式》解析宋代建筑高度/auto/从《营造法式》解析宋代建筑高度.md`
- [x] 源类型：填充层
- [x] 批次切分方式：全文一batch（12页/274行）

## Step 1: 建结构

- [x] 已读 KNOWLEDGE.md §Ingest（完整步骤 + 行号标注规则）
- [x] sources/ 页已建
- [x] 全文一batch（274行）

## Step 2: 报告发现

- [x] 已向 boss 报告：15页清单（1 source + 10 entities + 4 concepts + 1 synthesis）

## Step 3: 全量实体提取

- [x] 逐一建页：营造法式、李诫、版门、乌头门、垒墙、露墙、抽紝墙、露篱、檐柱、金柱
- [x] 原子写入（.tmp → 校验 → rename）
- [x] frontmatter 必填字段已填满
- [x] wikilink ≥ 最低阈值
- [x] 每条事实断言已标注源行号

## Step 4: 全量概念提取

- [x] 逐一建页：材分制、宋代建筑三分法、宋代台基制度、宋代墙体高厚比
- [x] 原子写入 + frontmatter + wikilink + 行号标注

## Step 5: 综合页

- [x] 已建 syntheses/宋代建筑高度游戏化应用.md

## Step 6: 跨章回溯

- [x] entities/料敌塔.md：已读，建筑墙体数据不直接适用于佛塔，无需更新
- [x] entities/地下长城.md：已读，地下战道用砖砌与营造法式土墙规范不同，无需更新
- [x] 本批无受影响已建页面需要更新

## 批次记录

### Batch 1：全文（L1-L274）

- [x] 计划范围：全文12页/274行
- [x] 已读范围：L1-L274
- [x] 新建页面：source×1, entity×10, concept×4, synthesis×1 = 16页
- [x] 更新页面：无
- [x] 回溯页面：料敌塔（无需更新）、地下长城（无需更新）
- [x] 未处理/疑问：屋顶（上分）高度数据在当前来源缺失
- [x] 本批 citation 行号均落在已读范围内

## Step 7: 更新枢纽

- [x] 更新 wiki/index.md
- [x] 追加 wiki/log.md
- [x] 重生成 wiki/MOC.md（795行）

## 收尾

- [ ] 更新 sources/ 页的「产出页面清单」
- [ ] 重写 wiki/overview.md
- [ ] 已准备提交摘要：`ingest: <来源标题> — <N> pages`
- [ ] boss 确认后再执行 git commit
- [ ] 文件移到 `tasks/done/`
- [ ] **回顾本清单**：所有已完成动作已 ✔，无遗漏 `- [ ]`
