# Query：<问题简述>

> **task-id**：query-YYYY-MM-DD-<slug>
> **时间**：YYYY-MM-DD HH:MM
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。

## 问题

- [ ] 问题已明确界定
- [ ] 问题已写入任务文件

## Step 1: 查 wiki

- [ ] 精确直达判断：明确 slug/title 唯一命中？___（是：直接读对应页 / 否：继续检索）
- [ ] 已运行 `python tools/retrieve.py "<user query>" --top 5 --depth 1` 定位相关页面
- [ ] 如 retrieve.py 不可用：已降级为读 wiki/index.md → 搜索标题/tags
- [ ] 已读 wiki/overview.md 获得高层全景
- [ ] 已读匹配的 sources/ + entities/ + concepts/ + syntheses/ 页面
- [ ] wiki 覆盖程度：___（充分 / 部分 / 不足）

## Step 2: 判断是否需要 web 补充

- [ ] 如 wiki 充分 → 跳过 web，直接合成
- [ ] 如 wiki 不足 → web_search/web_fetch 补充
  - [ ] web 内容写入 `knowledge/web-buffer/<topic>.md`
  - [ ] 标注 🌐 来源 URL + 采集日期
  - [ ] 报告 boss 待审定

## Step 3: 合成回答

- [ ] 按回答格式输出：问题界定 → 结论等级 → 核心回答 → 依据链 → 限制与反例 → 缺口与下一步
- [ ] 每个断言标注来源（✅wiki 页面名 / 🌐web URL / ⚠️推测）
- [ ] 回答末尾附来源汇总

## Step 4: 回写（如触发）

- [ ] 综合 ≥3 页且形成新洞察 → 归档为 synthesis 页
- [ ] 更新受影响已有页面
- [ ] 运行 `python tools/indexgen.py` 更新 wiki/index.md
- [ ] 运行 `python tools/gen_moc.py` 更新 wiki/MOC.md
- [ ] 追加 wiki/log.md

## 收尾

- [ ] 文件移到 `tasks/done/`
- [ ] 已追加 `tasks/index.md`：done 行
- [ ] **回顾本清单**：所有已完成动作已 ✔
