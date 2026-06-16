# convert：从《营造法式》解析宋代建筑高度

> **task-id**：convert-2026-06-12-yingzaofashi-gaodu
> **时间**：2026-06-12 09:44
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。断线回来 → 找第一个 `- [ ]` 继续。

## 来源

- [ ] 书名：从《营造法式》解析宋代建筑高度
- [ ] 作者：（待确认，下载后提取）
- [ ] 年份：（待确认）
- [ ] 类型：论文
- [x] PDF 路径：`knowledge/raw/pdf/从《营造法式》解析宋代建筑高度.pdf`
- [x] 文件大小：7.0 MB，页数：12

## Step 1: 注册

- [x] 文件已保存到 `tasks/pending/<task-id>.md`
- [ ] 已追加 `tasks/index.md`：`| HH:MM | <task-id> | convert | <书名> | pending |`
- [x] 文件已移动到 `tasks/running/`
- [x] 已追加 `tasks/index.md`：`| HH:MM | <task-id> | convert | <书名> | running:Step1 |`

## Step 2: 转换

- [x] 已读 `TOOLS.md` MinerU 节
- [x] vLLM 状态确认：启动（~35s，含 CUDA graph capture）
- [x] 转换命令已执行：bash tools/magic-pdf
- [x] 🔴 确认未使用 hybrid-auto-engine
- [x] 输出路径已确认：`knowledge/converted/mineru/convert-2026-06-12-yingzaofashi-gaodu/从《营造法式》解析宋代建筑高度/auto/从《营造法式》解析宋代建筑高度.md`
- [x] 转换结果：成功（274行/15KB/16张图片）
- [x] 已追加 `tasks/index.md`：`running:Step2`

## Step 3: 质量检查

- [x] 行数检查：274 行 ≥ 120（12页×10）→ ✅
- [x] 表格完整性：MD 0 个表格 vs PDF 可见 1 个（表格为图片格式，非文字提取）→ ⚠️ 可接受
- [x] 图片引用：MD 16 处 vs 约 16 张（匹配度 100%）→ ✅
- [x] 乱码率：0.0%（2 段 >200 字全中文无异码）→ ✅
- [x] 章节结构：46 个标题，层级分明 → ✅
- [x] 综合判定：**合格**
- [x] 已追加 `tasks/index.md`：`running:Step3`

## Step 4: 报告

- [ ] 质量报告已发给 boss（含五维检查表 + 输出路径）
- [ ] boss 回复：___（确认进 Ingest / 拒绝 / 其他）
- [ ] 已追加 `tasks/index.md`：`running:Step4`

## 收尾

- [ ] 文件已移动到 `tasks/done/`
- [ ] 已追加 `tasks/index.md`：`| HH:MM | <task-id> | convert | <书名> | done | 质量N/5通过 |`
- [ ] converted/ 产物保留，等待 Ingest
- [ ] **回顾本清单**：所有已完成动作已 ✔，无遗漏 `- [ ]`

## 回退

> 仅当任一步骤失败时执行此节。逐项勾。

- [ ] `knowledge/converted/mineru/<task-id>/` 整个目录已删除
- [ ] 文件已移动到 `tasks/failed/`
- [ ] 已追加 `tasks/index.md`：`| HH:MM | <task-id> | convert | <书名> | failed:Step<N> | <原因> |`
- [ ] 已通知 boss 失败原因
