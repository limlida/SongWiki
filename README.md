# OpenClaw

**"第二大脑"知识管理系统** — 由 LLM 维护的本地 Markdown wiki。

## 核心理念

LLM 承担全部簿记，人类只管思考。维护成本趋近于零 → 知识持续复利。

## 当前状态

[*] 初始状态 — 等待第一个 Ingest 任务。

| 指标 | 数值 |
|------|------|
| Wiki 页面 | 0 |
| 收录来源 | 0 |
| 活跃任务 | 0 |

## 快速开始

### 收录新知识

1. 把 PDF 放入 `knowledge/raw/`
2. 告诉 Claude："收录 `<路径>`"
3. Claude 执行：转换 → 提取 → 建页 → 索引 → 提交

### 查询知识

直接问 Claude。wiki 优先，web 补充。

### 认知审计

```bash
python .agents/skills/openclaw-kb-selfcheck/scripts/selfcheck.py
```

## 架构

```
raw/           原始来源，不可变（PDF 等）
    ↓ 转换（MinerU / magic-pdf）
wiki/          LLM 全权维护的知识页
    sources/  →  entities/  →  concepts/  →  syntheses/
    ↓ 演进
Schema         AGENTS.md / RULES.md / SOUL.md / KNOWLEDGE.md
```

## 命令

```bash
# 工具链健康检查
python .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check

# 知识库自检
python .agents/skills/openclaw-kb-selfcheck/scripts/selfcheck.py

# PDF 转换
bash tools/magic-pdf -p <input.pdf> -o <output_dir> -m auto -l ch

# 生成索引
python tools/indexgen.py
```

## 关键文件

| 文件 | 角色 |
|------|------|
| `AGENTS.md` | 入口、工作区地图 |
| `RULES.md` | 硬规则（唯一权威） |
| `KNOWLEDGE.md` | 知识库工作流 |
| `SOUL.md` | 角色与行事准则 |
| `MEMORY.md` | 唤醒协议 |
| `TOOLS.md` | 工具路径与命令 |

## 来源等级

| 等级 | 含义 | 例子 |
|------|------|------|
| 一手 | 原始文献、官方文档、考古报告 | 窑址发掘报告 |
| 二手 | 研究专著、整理著作 | 学术专著 |
| 待验证 | 网页、聊天、出处不明的说法 | 论坛帖子 |

## 方法论

方法论源自 **Andrej Karpathy** 的 [llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。Agent 运行在 [OpenClaw](https://github.com/code-yeongyu/oh-my-openagent) 框架上。
