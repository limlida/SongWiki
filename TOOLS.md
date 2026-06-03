# TOOLS.md - 工具与环境

本文件只记录工具路径和命令。使用策略见 RULES.md，转换策略见 KNOWLEDGE.md。

## 工作区

- 主工作区：`/mnt/e/Projects/OpenclawWorkspace/`
- Python：`python3`（WSL 无 `python` 命令）
- 知识库：`knowledge/`

## MinerU

用途：PDF/扫描书/复杂文档 → Markdown。

```bash
# venv
/home/hello/.venv/mineru/bin/python
# CLI
/home/hello/.venv/mineru/bin/mineru -p <input> -o <output> -m ocr -b vlm-auto-engine
# vLLM 服务启动
bash /home/hello/.venv/mineru/start-vllm.sh
```

模型：MinerU2.5-Pro-2605-1.2B（vLLM 0.20.2），端口 30000
版本：v3.2.1

## pdf-craft

用途：扫描书/古籍影印 PDF → Markdown/EPUB。

```bash
/home/hello/.venv/pdf-craft/bin/python
# Python API
from pdf_craft import transform_markdown
```

版本：v1.0.13

## lark-cli

用途：飞书消息、云文档、云空间操作。

```bash
lark-cli          # 飞书 CLI（v1.0.42）
lark-cli im       # 消息操作
lark-cli drive    # 云空间
lark-cli docs     # 云文档
```

## 工具链检查

```bash
python3 .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check
```

## 浏览器

- Profile：`openclaw`
- 用完关闭 tab

## 注意

- 所有文件输出写入工作区，禁止写入 `/tmp/`
- image 工具只能读取工作区内的本地文件
- 实际 `openclaw.json` 不提交仓库，敏感字段通过环境变量注入
