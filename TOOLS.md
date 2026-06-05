# TOOLS.md - 工具与环境

> 本文件是所有工具路径和命令的**唯一权威来源**。其他文件不得与本文件冲突。
> 上次验证：2026-06-04（magic-pdf vlm-http-client 成功转换三本书）

## 工具速查（TL;DR）

| 工具 | 命令 | 用途 |
|------|------|------|
| magic-pdf | `bash tools/magic-pdf -p <pdf> -o <out> -m auto -l ch` | PDF → Markdown |
| vLLM 启动 | `bash tools/start-vllm` | 启动 VLM 推理服务 |
| vLLM 健康 | `curl localhost:30000/health` | 确认 vLLM 已启动 |
| vLLM 管理 | `ps aux \| grep mineru-openai` / `pkill -f mineru-openai-server` | 查看/停止 vLLM |
| 工具链自检 | `python3 .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check` | 全量检查 |

## 工作区

- 主工作区：`/mnt/e/Projects/OpenclawWorkspace/`
- Python：`python3`（WSL 无 `python` 命令）
- 知识库：`knowledge/`
- 工具脚本：`tools/`
- **所有文件输出写入工作区，禁止写入 `/tmp/`**

---

## MinerU 架构

两个 Python venv，各司其职。magic-pdf 是客户端，vLLM server 是推理引擎。必须先启动 engine 再跑客户端。

```
┌──────────────────────────────────────────────────────┐
│ tools/magic-pdf                                       │  ← wrapper
│   → /home/hello/venv_mineru/bin/magic-pdf (1.3.12)   │     PDF转换CLI
│   后端: vlm-http-client                               │     连 localhost:30000
│   magic-pdf 自身不做 OCR/VLM推理，全靠 vLLM            │
└──────────────────────┬───────────────────────────────┘
                       │ HTTP (localhost:30000)
┌──────────────────────▼───────────────────────────────┐
│ tools/start-vllm                                      │  ← wrapper
│   → /home/hello/.venv/mineru/                          │     vLLM 推理服务
│      bin/mineru-openai-server                          │     (MinerU 3.2.1, vLLM 0.21.0)
│   模型: MinerU2.5-Pro-2605-1.2B                       │     RTX 5070 12GB VRAM
│   GPU: SM12.0 (Blackwell), PyTorch 2.11.0, CUDA 13.0  │
└──────────────────────────────────────────────────────┘
```

### 环境信息

| 组件 | 版本 | 路径 |
|------|------|------|
| magic-pdf | 1.3.12 | `/home/hello/venv_mineru/bin/magic-pdf` |
| vLLM server | 0.21.0 | `/home/hello/.venv/mineru/bin/mineru-openai-server` |
| PyTorch | 2.11.0 | CUDA 13.0 |
| GPU | RTX 5070 | 12GB VRAM, SM12.0 (Blackwell) |
| 模型 | MinerU2.5-Pro-2605-1.2B | `~/.cache/huggingface/hub/models--opendatalab--MinerU2.5-Pro-2605-1.2B/` |

---

### 步骤 1：启动 vLLM 推理服务

**一键（推荐）：**

```bash
bash tools/start-vllm
```

**手动：**

```bash
VLLM_USE_FLASHINFER_SAMPLER=0 \
HF_HUB_OFFLINE=1 \
TRANSFORMERS_OFFLINE=1 \
/home/hello/.venv/mineru/bin/mineru-openai-server \
  --host 0.0.0.0 \
  --port 30000
```

启动耗时约 **50-55 秒**（torch.compile + CUDA graph capture）。

#### 必设环境变量（RTX 5070 Blackwell + WSL）

| 变量 | 为什么必须设 | 不设的后果 |
|------|------------|-----------|
| `VLLM_USE_FLASHINFER_SAMPLER=0` | FlashInfer 与 Blackwell SM12.0 不兼容 | `RuntimeError: FlashInfer requires GPUs with sm75 or higher` |
| `HF_HUB_OFFLINE=1` | WSL 无法访问 huggingface.co | `Network is unreachable`，vLLM 无限重试 |
| `TRANSFORMERS_OFFLINE=1` | 同上，transformers 库离线模式 | 同上 |

#### 验证 vLLM 已启动

```bash
curl http://localhost:30000/health          # → {"status":"ok"}
curl http://localhost:30000/v1/models       # → 列出 MinerU 模型
```

---

### 步骤 2：转换 PDF → Markdown

**vLLM 确认在跑后**，执行：

```bash
bash tools/magic-pdf \
  -p <input.pdf> \
  -o <output_dir> \
  -m auto \
  -l ch
```

输出目录：`<output_dir>/<pdf_name>/vlm/`，入口文件：`<pdf_name>.md`。

---

### 🔴 禁止事项

| 禁止 | 原因 |
|------|------|
| **`-b vlm-auto-engine` / `hybrid-auto-engine`** | 自启 vLLM 引擎，与已在跑的 server 抢 GPU（12GB 不够两个 vLLM），**挂死** |
| **`pip install`** | 所有工具链已安装 |
| **下载模型** | 模型缓存已就绪（见下方缓存清单） |
| **旧版 `mineru` CLI**（`/home/hello/.venv/mineru/bin/mineru`） | 那是 v3.2.1，不兼容 magic-pdf 1.3.12 的 vlm-http-client 模式 |

工具不可用时：先 `curl localhost:30000/health` 确认 vLLM → server 正常但 magic-pdf 失败 → **报告 boss**。禁止自行"修"。

---

### 模型缓存（已下载，禁止重装）

| 缓存位置 | 用途 |
|---------|------|
| `~/.cache/mineru_models/` | MinerU 模型 |
| `~/.cache/modelscope/` | ModelScope 模型 |
| `~/.cache/paddle/` | PaddleOCR 模型 |
| `~/.cache/huggingface/hub/models--opendatalab--MinerU2.5-Pro-2605-1.2B/` | vLLM 模型权重（2.16 GiB） |

---

### 故障排查树

```
vLLM 启动失败？
├─ 报 huggingface.co Network unreachable
│   → 确认 HF_HUB_OFFLINE=1 + TRANSFORMERS_OFFLINE=1 已设
├─ 报 FlashInfer sm75 error
│   → 确认 VLLM_USE_FLASHINFER_SAMPLER=0 已设
├─ 报 CUDA out of memory
│   → 加 --gpu-memory-utilization 0.3
├─ 进程被 SIGKILL
│   → nohup 后台启动：nohup bash tools/start-vllm &
└─ 模型文件找不到
    → 检查 ~/.cache/huggingface/hub/models--opendatalab--MinerU2.5-Pro-2605-1.2B/ 是否存在

magic-pdf 转换失败？
├─ 端口 30000 无响应
│   → curl localhost:30000/health 确认
│   → 确认只有 1 个 vLLM 进程（ps aux | grep mineru-openai）
├─ GPU OOM 挂死
│   → 确认没用 hybrid-auto-engine
│   → pkill -f mineru-openai-server 后重来
├─ 输出乱码/空白
│   → 检查 PDF 是否加密（qpdf --decrypt 先解密）
│   → 扫描件 PDF：确认 vLLM 已加载 VLM 模型（curl localhost:30000/v1/models）
│   → 文本层 PDF：检查 -m auto 参数是否正确
└─ 输出极短/截断
    → 检查 PDF 页数，大文件可能需更长等待
```

---

## 转换成品目录

`knowledge/converted/mineru/<task-id>/` — 一次转换任务一个子目录，不混放。

---

## lark-cli

用途：飞书消息、云文档、云空间操作。

```bash
lark-cli im       # 消息操作
lark-cli drive    # 云空间
lark-cli docs     # 云文档
```

lark-cli 的安装方式和授权配置取决于本机环境。首次使用需完成飞书应用配置。

---

## 浏览器

- Profile：`openclaw`
- 用完关闭 tab
- 与 MinerU/OCR 不得并发

---

## 并发限制

| 工具 | 同时最多 |
|------|---------|
| MinerU (magic-pdf) | 1 |
| pdf-craft | 1 |
| OCR | 1 |
| 浏览器抓取 | 1 |
