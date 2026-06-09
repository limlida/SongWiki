# <类型>：<书名>

> **task-id**：convert-YYYY-MM-DD-<slug>
> **时间**：YYYY-MM-DD HH:MM
> **如何执行**：从第一个 `- [ ]` 开始，做完 ✔。不要跳步。断线回来 → 找第一个 `- [ ]` 继续。

## 来源

- [ ] 书名：
- [ ] 作者：
- [ ] 年份：
- [ ] 类型：专著 / 论文 / 古籍 / 其他
- [ ] PDF 路径：`knowledge/raw/pdf/<文件名>`
- [ ] 文件大小：___ MB，页数：___

## Step 1: 注册

- [ ] 文件已保存到 `tasks/pending/<task-id>.md`
- [ ] 已追加 `tasks/index.md`：`| HH:MM | <task-id> | convert | <书名> | pending |`
- [ ] 文件已移动到 `tasks/running/`
- [ ] 已追加 `tasks/index.md`：`| HH:MM | <task-id> | convert | <书名> | running:Step1 |`

## Step 2: 转换

- [ ] 已读 `TOOLS.md` MinerU 节
- [ ] vLLM 状态确认：`curl localhost:30000/health`
- [ ] 如需启动 vLLM：`bash tools/start-vllm`（~55s）
- [ ] 转换命令已执行：
  ```bash
  bash tools/magic-pdf -p <pdf> -o knowledge/converted/mineru/<task-id>/ -m auto -l ch
  ```
- [ ] 🔴 确认未使用 hybrid-auto-engine
- [ ] 输出路径已确认：`knowledge/converted/mineru/<task-id>/`
- [ ] 转换耗时 ___ 秒，结果：[成功 / 失败]
- [ ] 已追加 `tasks/index.md`：`running:Step2`

## Step 3: 质量检查

- [ ] 行数检查：MD 共 ___ 行（≥ PDF 页数 × 10？[是/否]）
- [ ] 表格完整性：MD ___ 个表格 vs PDF 可见约 ___ 个（匹配度 ___%）
- [ ] 图片引用：MD `![]()` ___ 处 vs PDF 约 ___ 张（匹配度 ___%）
- [ ] 乱码率：随机 5 段 >200 字，乱码率 ___%（[<5% OK / 5-15% 警告 / >15% 不合格]）
- [ ] 章节结构：MD 含 `#` 标题层级？（一级标题 ___ 个）
- [ ] 综合判定：___（合格 / 警告可用 / 不合格需回退）
- [ ] 如不合格 → 立即执行回退（跳转到「回退」节）
- [ ] 已追加 `tasks/index.md`：`running:Step3`

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

---

> **命名规范**
> - convert → `convert-YYYY-MM-DD-<slug>`
> - ingest → `ingest-YYYY-MM-DD-<slug>`
> - lint → `lint-YYYY-MM-DD`
> - query → `query-YYYY-MM-DD-<slug>`
> - slug = 简短英文或拼音，`-` 连接，≤30 字符
