# Lint：<范围>

> **task-id**：lint-YYYY-MM-DD
> **时间**：YYYY-MM-DD HH:MM
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。

## 范围

- [ ] 范围：全库 / <指定目录>
- [ ] 检查对象仅限四类知识页：`wiki/sources/`、`wiki/entities/`、`wiki/concepts/`、`wiki/syntheses/`
- [ ] hub 文件（index/log/overview/MOC）不套用知识页规则
- [ ] 已读 KNOWLEDGE.md §Lint（13 条机审规则）

## 阶段 1：基础结构检查（8 条）

- [ ] #1 missing-frontmatter：扫描不以 `---` 开头的 .md 文件
- [ ] #2 broken-wikilink：所有 `[[...]]` slug 对全库页面集合
- [ ] #5 duplicate-concept：title 归一化 + slug 编辑距离 < 3
- [ ] #6 empty-page：body < 50 字符
- [ ] #8 orphaned-page：非 source 页 backlinks = 0 且 age_days > 30
- [ ] #9 low-confidence：confidence < 0.5
- [ ] #11 schema-cross-links：wikilink 数 < pageKind 最小阈值
- [ ] #13 unmaterialized-term（info/0分）：普通文本术语在 ≥3 个知识页出现，且不在 slug/title/aliases 中

## 阶段 2：引用格式检查（4 条）

- [ ] #3 broken-citation：`^[source:行号]` 无法映射到 source.converted_path，或行号越界
- [ ] #4 malformed-claim-citation：`^[...]` 空条目/含`..`/行号非法
- [ ] #7 missing-summary：frontmatter.summary 缺失
- [ ] #12 excess-inferred-paragraphs：无 `^[...]` 引用的 prose 段落 > 2

## 阶段 3：矛盾标记检查（1 条）

- [ ] #10 contradicted-page：frontmatter.contradictedBy 非空

## 报告

- [ ] 计算健康分：`health_score = max(0, 100 - Σ扣分)`
- [ ] 生成问题列表（含处理建议）
- [ ] 生成补课式 Ingest 候选清单（#13，不计入健康分）
- [ ] 报告 boss：「Lint 完成。健康分 X/100。发现问题 N 条。」
- [ ] boss 逐条决策（删除/合并/降级/忽略）

## 修复（boss 确认后）

- [ ] 逐条执行 boss 决定的动作
- [ ] 修复后重新 grep 确认无残留死链/错误
- [ ] 更新 wiki/index.md
- [ ] 追加 wiki/log.md：`## [YYYY-MM-DD] lint — 健康分 X/100，修复 N 条`

## 收尾

- [ ] 文件移到 `tasks/done/`
- [ ] 已追加 `tasks/index.md`：done 行
- [ ] **回顾本清单**：所有已完成动作已 ✔
