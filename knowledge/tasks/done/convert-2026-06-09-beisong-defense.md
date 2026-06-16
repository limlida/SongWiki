# convert：北宋河北边防建设研究

> **task-id**：convert-2026-06-09-beisong-defense
> **时间**：2026-06-09 16:00
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。断线回来 → 找第一个 `- [ ]` 继续。

## 来源

- [x] 书名：《北宋河北边防建设研究》
- [x] 作者：王轶英
- [ ] 年份：
- [ ] 类型：专著（博士论文）
- [x] PDF 路径：`knowledge/raw/pdf/北宋河北边防建设研究_王轶英.pdf`
- [x] 文件大小：7.6 MB，页数：80

## Step 1: 注册

- [x] 文件已保存到 `tasks/running/convert-2026-06-09-beisong-defense.md`
- [x] 已追加 `tasks/index.md`

## Step 2: 转换

- [x] 已读 `TOOLS.md` MinerU 节
- [x] vLLM 状态确认：`curl localhost:30000/health` → 200 OK
- [x] 无需启动 vLLM（已在运行）
- [x] 转换命令已执行：
  ```bash
  bash tools/magic-pdf -p knowledge/raw/pdf/北宋河北边防建设研究_王轶英.pdf -o knowledge/converted/mineru/convert-2026-06-09-beisong-defense/ -m auto -l ch
  ```
- [x] 🔴 确认未使用 hybrid-auto-engine
- [x] 输出路径已确认：`knowledge/converted/mineru/convert-2026-06-09-beisong-defense/北宋河北边防建设研究_王轶英/auto/`
- [x] 转换耗时 ~55 秒，结果：成功
- [x] 已追加 `tasks/index.md`：`running:Step2`

## Step 3: 质量检查

- [x] 行数检查：MD 共 887 行（≥ 80×10=800？是 ✅）
- [x] 表格完整性：MD 0 个表格（学术专著，无表格，正常）
- [x] 图片引用：MD `![]()` 9 处
- [x] 乱码率：随机 5 段 >200 字，乱码率 0%（<5% OK ✅）
- [x] 章节结构：MD 含 `#` 标题层级？一级标题 78 个
- [x] 综合判定：合格 ✅
- [x] 无需回退
- [x] 已追加 `tasks/index.md`：`running:Step3`

## Step 4: 报告

- [x] 质量报告已发给 boss（含五维检查表 + 输出路径）
- [ ] boss 回复：___（确认进 Ingest / 拒绝 / 其他）
- [x] 已追加 `tasks/index.md`：`running:Step4`

## 收尾

- [ ] 文件已移动到 `tasks/done/`
- [ ] 已追加 `tasks/index.md`
- [ ] converted/ 产物保留，等待 Ingest
- [ ] **回顾本清单**：所有已完成动作已 ✔，无遗漏 `- [ ]`

## 回退

- [ ] `knowledge/converted/mineru/convert-2026-06-09-beisong-defense/` 整个目录已删除
- [ ] 文件已移动到 `tasks/failed/`
- [ ] 已追加 `tasks/index.md`
- [ ] 已通知 boss 失败原因
