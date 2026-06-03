# TOOLS.md - 工具与环境

本文件只记录工具路径和命令。使用策略见 `RULES.md`，转换策略见 `KNOWLEDGE.md`。

## 工作区

- 主工作区：`e:\Projects\OpenclawWorkspace`
- 本地知识库：`knowledge/`

## 文档转换工具

### pdf-craft

用途：扫描书、整本书、古籍影印、现代研究书 PDF → Markdown/EPUB。

安装位置：`/home/hello/.venv/pdf-craft/`（venv）
版本：v1.0.13
调用：`/home/hello/.venv/pdf-craft/bin/python -c "from pdf_craft import ..."`

### MinerU

用途：复杂版面论文、多栏报告、Office 转 PDF、表格密集文档 → Markdown/JSON。扫描书/无文本层 PDF 也用 pipeline 后端。

安装位置：`/home/hello/.venv/mineru/`（venv）
版本：v3.2.1
CLI：`/home/hello/.venv/mineru/bin/mineru`
常用命令：
```bash
# pipeline 后端（扫描书/通用，最低 4GB VRAM，推荐）
/home/hello/.venv/mineru/bin/mineru -p <input> -o <output> -b pipeline

# hybrid 后端（高精度，最低 8GB VRAM）
/home/hello/.venv/mineru/bin/mineru -p <input> -o <output> -b hybrid
```
模型目录：`/mnt/e/Projects/OpenclawWorkspace/tools/models/mineru/`
⚠️ 禁止使用旧版 `magic-pdf` 命令，那是 1.x 时代的 CLI，已废弃。

## 飞书工具

```bash
lark-cli im          # 消息、群聊、附件下载和回复
lark-cli event       # 监听飞书消息事件
lark-cli docs --api-version v2  # 飞书云文档读写
lark-cli drive       # 云空间搜索、上传、下载
```

## Gateway 管理

```bash
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
```

不生效时用端口排查：

```bash
lsof -i :<port>
kill <PID>
```

## 浏览器

- 固定 profile：`openclaw`。
- 复用已有 tab，收录完成后关闭。
- 卡顿时先关非活跃 tab。

## 配置

实际 `openclaw.json` 不提交仓库。敏感字段通过环境变量或 secret provider 注入：
- API Key
- 飞书 App Secret
- Gateway Token

不要在聊天、日志或文件中输出这些值。

验证配置：

```bash
python .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check
```
