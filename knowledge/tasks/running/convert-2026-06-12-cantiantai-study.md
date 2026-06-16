# Convert：《参天台五台山记》所见宋代社会生活研究

> **task-id**：convert-2026-06-12-cantiantai-study
> **时间**：2026-06-12 18:06
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。

## 来源

- [x] 书名：《参天台五台山记》所见宋代社会生活研究
- [x] 作者：胡培培
- [x] 年份：2025（CNKI 优博/硕博论文）
- [x] 类型：论文（CNKI）
- [x] PDF 路径：`knowledge/raw/pdf/《参天台五台山记》所见宋代社会生活研究_胡培培.pdf`
- [x] 文件大小：2.2 MB，页数：76
- [x] ⚠️ PDF 已加密（AES），需先 qpdf 解密

## Step 1: 注册

- [x] 文件已移动到 `tasks/running/`
- [ ] 已追加 `tasks/index.md`：`| 18:06 | convert-2026-06-12-cantiantai-study | convert | 参天台研究 | running:Step1 |`

## Step 2: 转换

- [x] 已读 `TOOLS.md` MinerU 节
- [x] vLLM 状态确认 → 已启动
- [x] PDF 解密：PyPDF2 + pycryptodome（空密码）
- [x] 转换命令已执行
- [x] 输出路径：`knowledge/converted/mineru/convert-2026-06-12-cantiantai-study/`
- [x] 转换耗时 ~25 秒

## Step 3: 质量检查

- [x] 行数检查：MD 共 771 行（≥760 ✅）
- [x] 表格完整性：MD 0 个 `|---|` 表格（⚠️）
- [x] 图片引用：MD `![]()` 3 处（⚠️偏少）
- [x] 乱码率：1.3%（✅ <5%）
- [x] 章节结构：77 个标题，完整的章节目录 ✅
- [x] 综合判定：合格（警告可用）

## Step 4: 报告

- [ ] 质量报告已发给 boss
- [ ] boss 回复：___

## 收尾

- [ ] 文件已移动到 `tasks/done/`

## 回退

> 仅当任一步骤失败时执行此节。

- [ ] `knowledge/converted/mineru/convert-2026-06-12-cantiantai-study/` 已删除
- [ ] 文件已移动到 `tasks/failed/`
- [ ] 已通知 boss
