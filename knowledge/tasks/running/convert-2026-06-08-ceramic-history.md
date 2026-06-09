# convert：陶瓷简史

> **task-id**：convert-2026-06-08-ceramic-history
> **时间**：2026-06-08 17:18
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。

## 来源

- [x] 书名：《陶瓷简史：从石器时代到后工业时代》
- [x] 作者：有泉
- [x] 年份：2018
- [x] 类型：专著（江西美术出版社，320千字）
- [x] PDF 路径：`knowledge/raw/pdf/陶瓷简史：从石器时代到后工业时代.pdf`
- [x] 文件大小：48 MB

## Step 1: 注册

- [x] 文件已保存到 `tasks/pending/convert-2026-06-08-ceramic-history.md`
- [x] 已追加 `tasks/index.md`：pending 行
- [x] 文件已移动到 `tasks/running/`
- [x] 已追加 `tasks/index.md`：running:Step1 行

## Step 2: 转换

- [x] 已读 `TOOLS.md` MinerU 节
- [x] vLLM 启动：`bash tools/start-vllm`（~55s）
- [x] vLLM 健康确认：`curl localhost:30000/health` → 200 OK
- [x] 转换命令已执行：`bash tools/magic-pdf -p <pdf> -o knowledge/converted/mineru/convert-2026-06-08-ceramic-history/ -m auto -l ch`
- [x] 🔴 确认未使用 hybrid-auto-engine
- [x] 输出路径已确认：`knowledge/converted/mineru/convert-2026-06-08-ceramic-history/陶瓷简史：从石器时代到后工业时代/auto/陶瓷简史：从石器时代到后工业时代.md`
- [x] 已追加 `tasks/index.md`：running:Step2

## Step 3: 质量检查

- [x] 行数检查：3540 行 ✅
- [x] 表格完整性：表模型未启用（rapid_table disabled），无需检查
- [x] 图片引用：214 张 ✅
- [x] 乱码率：~0% ✅
- [x] 章节结构：火/土/釉/形/窑 五篇 + 子章节完整 ✅
- [x] 综合判定：合格 ✅
- [x] 无需回退
- [x] 已追加 `tasks/index.md`：running:Step3

## Step 4: 报告

- [x] 质量报告已发给 boss（见本轮消息）
- [x] boss 确认进 Ingest（2026-06-09）
- [x] 已追加 `tasks/index.md`：running:Step4
- [ ] Ingest: 建 source 页

## 收尾

- [ ] 文件已移动到 `tasks/done/`
- [ ] 已追加 `tasks/index.md`：done 行
- [ ] **回顾本清单**

## 回退

- [ ] 删除 `knowledge/converted/mineru/convert-2026-06-08-ceramic-history/`
- [ ] 文件移至 `tasks/failed/`
- [ ] 追加 `tasks/index.md`：failed 行
- [ ] 通知 boss
