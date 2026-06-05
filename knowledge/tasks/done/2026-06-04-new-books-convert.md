# 任务：三本新书 PDF 转 Markdown

- **创建时间**：2026-06-04 18:32
- **状态**：running
- **预估耗时**：~30 分钟（三本串行）

## 待转换文件

| # | 源文件 | 大小 | 状态 |
|---|--------|------|------|
| 1 | `knowledge/raw/pdf/北宋河北边防建设研究_王轶英.pdf` | 7.7MB | pending |
| 2 | `knowledge/raw/pdf/参天台五台山记_白话译文.pdf` | 7.9MB | pending |
| 3 | `knowledge/raw/pdf/新见日本藏三方北宋官印考_刘铮.pdf` | 1.6MB | pending |

## 转换方案

- 工具：magic-pdf (MinerU 1.3.12)，`-m auto -l ch`
- 输出：`knowledge/converted/mineru/2026-06-04-books/`

## 进度

- [x] 检查 MinerU server 状态 → 未运行
- [x] 启动 MinerU server（预计 50-55s）
- [x] 书1：王轶英河北边防 ✅ (1003行/176KB, 80页, 90秒)
- [x] 书2：成寻白话译文 ✅ (6056行/753KB, 287页, ~4分钟)
- [x] 书3：刘铮官印考 ✅ (188行/15KB, 4页, 13秒)
- [ ] 报告 boss：篇幅 + 可读性
- [ ] 等待 boss 确认进 Ingest

## 转换方案

最终采用 `vlm-http-client` 后端（复用端口30000已有 vLLM server）。`hybrid-auto-engine` 会自启引擎与已有 vLLM 争抢 GPU 12GB VRAM，导致挂死。

## 执行日志

- 2026-06-04 18:55 检查 server：未运行
- 2026-06-04 18:56 启动 MinerU vLLM server ✅ (PID 25529)
- 2026-06-04 18:57 hybrid-auto-engine 尝试 → GPU 争抢，kill
- 2026-06-04 19:00 改用 vlm-http-client 方案 ✅
- 2026-06-04 19:00 书3 官印考 完成 ✅
- 2026-06-04 19:01 书1 河北边防 完成 ✅
- 2026-06-04 19:03 书2 成寻白话译文 完成 ✅
- 2026-06-04 19:07 全量转换完成
