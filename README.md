# SongWiki — LLM Wiki 知识库

基于 [Karpathy LLM Wiki 方法论](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的宋代史知识库，由 LLM Agent（扫地僧）自动维护。

## 核心理念

知识在录入时编译，页面持续更新，LLM 做全部簿记。这不是档案馆——这是活的知识有机体。

## 目录结构

```
├── knowledge/           # 知识库本体
│   ├── raw/             # 原始来源（不可变）
│   ├── converted/       # 转换成品（MinerU / pdf-craft 输出）
│   ├── web-buffer/      # Web 搜索结果隔离区
│   ├── wiki/            # 知识编译层
│   │   ├── index.md     # 全局符号表
│   │   ├── log.md       # 操作日志
│   │   ├── overview.md  # 宏观大纲
│   │   ├── sources/     # 来源摘要
│   │   ├── entities/    # 客观实体（人/地/事/物）
│   │   ├── concepts/    # 抽象概念
│   │   └── syntheses/   # 综合论述
│   ├── tasks/           # 任务状态机
│   └── templates/       # 页面模板
├── .agents/skills/      # Agent 技能定义
├── tools/               # 工具脚本（MinerU、vLLM）
├── CLAUDE.md            # Agent 会话指令
├── KNOWLEDGE.md         # 知识库工作流
├── RULES.md             # 硬规则
└── TOOLS.md             # 工具与环境
```

## 当前状态

- **总页数**：140
- **活跃领域**：宋代全史（陶瓷、茶、社会生活、军事、宗教、交通、服饰）
- **来源**：5 本专著（一手史料 + 二手研究）

## 快速开始

### 浏览 Wiki

通过 Dashboard 在线浏览：`https://github.com/limlida/openclaw-wiki-dashboard`（GitHub Pages）

或本地使用 Obsidian 打开 `knowledge/wiki/` 目录。

### 运行自检

```bash
python3 .agents/skills/openclaw-kb-selfcheck/scripts/selfcheck.py --json
```

### PDF 转换（需要 GPU）

```bash
bash tools/start-vllm          # 启动 VLM 推理服务
bash tools/magic-pdf -p <pdf>  # PDF → Markdown
```

详见 [TOOLS.md](TOOLS.md)。

## CI / 质量保障

| 组件 | 说明 |
|------|------|
| CI 流水线 | push/PR 自动触发自检 + lint |
| 第三方审计 | 每日 cron 独立审计（结构合规、内容保真度、回答质量） |
| Dashboard | Web 前端（审计趋势 + Wiki 浏览 + 知识图谱） |

## 致谢

方法论源自 **Andrej Karpathy** 的 [llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。Agent 运行在 [OpenClaw](https://github.com/code-yeongyu/oh-my-openagent) 框架上。
