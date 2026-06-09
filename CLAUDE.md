# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作提供指引。

## 项目身份

**OpenClaw** — "第二大脑"知识管理系统。不是软件工程仓库。仓库本身就是知识库：由 Claude 维护的本地 Markdown wiki（角色：🧹 扫地僧）。默认语言：简体中文。主人：林立达（boss）。

**核心理念**：LLM 承担全部簿记，人类只管思考。维护成本趋近于零 → 知识持续复利（Karpathy LLM Wiki 模式）。

## 信任模型

### 当前信任锚

```
来源 → MinerU 转换 → Claude 读 → Claude 写页面 → Claude 自检 → boss 审阅 → wiki/
```

信任建立在 Claude 的诚实上，没有机器闸门。每个断言标注 [[wikilinks]]（页面级出处），每页 frontmatter 标注 source + confidence。**Claude 既写页面又审页面。**

### 已知盲区

Claude 自己发现不了的问题：

- [[wikilink]] 死链 — 写了不验证，目标页面不存在
- 同名概念重复建页 — 记不住全部 362 个标题
- wikilink 不足 — 写页时忘了数
- 孤立页无人引用 — Query 回填后其他页没加回链
- 推断混入提取 — 读者分不出哪句是源里的、哪句是 LLM 串的
- frontmatter 缺失 — 274 entity 中仅 129 有 frontmatter（47%），Claude 手工写页时漏写 YAML 头

### 与 llm-wiki-compiler 的关键差异

Compiler 信任工具链，OpenClaw 信任 LLM：

| | compiler | OpenClaw |
|---|----------|----------|
| frontmatter | 机器 `buildMergedFrontmatter()` 组装 → 100% 一致 | LLM 写整页 → 47% |
| 源追踪 | `state.json` 记录 SHA-256 + 概念列表 → 增量编译 | 无机制，靠人说"新书到了" |
| lint | 13 条机器规则自动跑 | Claude 手工跑 |
| 引用 | `^[source:行号]` 机器可验证 | 页面级 wikilink |

**本质**：compiler 把生成和包装分离——LLM 只生成 body，机器组装 frontmatter。OpenClaw 把全部责任交给 LLM，LLM 不擅长格式一致性。

### 演进方向

- **阶段 1**（8 条机审规则）：不改写作习惯，脚本自动检查
- **阶段 2**（4 条规则）：引入 `^[source:行号]` 引用格式，强制区分提取 vs 推断
- **阶段 3**：启用 contradictedBy 字段 + eval 持续跑分

**底线**：机器验证层是补充，不是替代。内容正确性仍靠人 + LLM。

## 每次会话必读（按顺序）

1. `MEMORY.md` — 唤醒协议（强制，不可跳过）
2. `AGENTS.md` — 入口、工作区地图、工作模型
3. `RULES.md` — 硬规则（唯一权威），🔴=铁律 🟡=工作约定 🟢=操作备忘
4. `KNOWLEDGE.md` — 知识库工作流（Ingest / Query / Lint）
5. `SOUL.md` — 角色、行事准则、边界
6. `LARK.md` — 飞书交互协议
7. `TOOLS.md` — 工具路径与命令（所有工具路径的唯一权威来源）

## 唤醒协议（每次新会话强制，不可跳过）

```
1. python3 .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check
2. 读 knowledge/wiki/index.md（全局地图：~362 页）
3. 读 knowledge/wiki/log.md 最后 10 条
4. 检查 knowledge/tasks/ 是否有 running/pending 任务
5. 按需读 KNOWLEDGE.md / LARK.md / TOOLS.md
6. 上述 5 步完成前，禁止调 web_search / exec / MinerU / OCR / 浏览器抓取
```

## 命令

### 工具链
```bash
# 全量工具链健康检查
python3 .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check

# 知识库一致性自检（只读，输出 PASS/WARN/FAIL 分级报告）
# 当前检查：目录结构 / task 格式 / index 同步
# 阶段 1 lint 将增加：frontmatter 缺失 / wikilink 死链 / 重复标题 / 空页 / 孤立页 / wikilink 不足 / 暗概念
python .agents/skills/openclaw-kb-selfcheck/scripts/selfcheck.py

# 机器可读 JSON 输出
python .agents/skills/openclaw-kb-selfcheck/scripts/selfcheck.py --json
```

### PDF 转换（MinerU 管道）
```bash
# 第 1 步：启动 vLLM 推理服务（启动约 50-55 秒，RTX 5070 12GB）
bash tools/start-vllm

# 确认 vLLM 已就绪
curl http://localhost:30000/health          # → {"status":"ok"}

# 第 2 步：PDF → Markdown（必须等 vLLM 就绪后再执行）
bash tools/magic-pdf -p <input.pdf> -o <output_dir> -m auto -l ch

# 输出目录：<output_dir>/<pdf_name>/vlm/，入口文件：<pdf_name>.md
```

**严禁**：
- 使用 `-b vlm-auto-engine` 或 `hybrid-auto-engine` — 会自启第二个 vLLM，GPU OOM
- `pip install` 或下载模型 — 全部已预装
- 工具不可用时自行"修复" — 先 `curl localhost:30000/health` 确认 vLLM → 仍失败则报告 boss

### 飞书
```bash
lark-cli im       # 消息
lark-cli drive    # 云空间
lark-cli docs     # 云文档
```

### Git
- 提交格式：`ingest: <来源标题> — 全量提取 <N> pages` 或 `schema: <文件名> -- <变更说明> (trigger: <触发原因>)`
- 或：`lint: <操作说明> — <统计>`（如 `lint: 自动清理 N 页（删除 X / 合并 Y / 降级 Z）`）
- 不 amend 已有提交。不跳过 hooks。

## 架构

### 三层知识架构
```
raw/           原始来源，不可变（PDF、图片等）。LLM 只读。绝不删除。
    ↓ 转换（MinerU）
wiki/          LLM 全权维护的知识页。四文件夹分类，严格物理约束。
    ↓ 演进
Schema         AGENTS.md / RULES.md / SOUL.md / KNOWLEDGE.md。与 LLM 共同演进。
```

### Wiki 四文件夹分类（硬约束）
```
sources/     →   entities/   →   concepts/   →   syntheses/
来源摘要          事实原子          抽象模式          综合论述
```
从左到右：抽象度递增，[[WikiLinks]] 引用密度递增。**严禁在 wiki/ 根目录创建知识页。**

### 枢纽文件

| 文件 | 角色 | 触发更新时机 |
|------|------|-------------|
| `wiki/index.md` | 图书馆卡片目录 — 每页一行，按四分类索引 | 每次建/改/删页面 |
| `wiki/log.md` | 航海日志 — 追加只写，`## [YYYY-MM-DD]` 条目 | 每次操作 |
| `wiki/overview.md` | 书的前言 — 5-10 段知识全景摘要 | 每 5-10 次 Ingest |
| `wiki/MOC.md` | 话题交叉索引 — 按 tag 分组列出所有页面（待建） | 每次 Ingest（全自动生成） |
| `wiki/source-state.json` | 源→概念→hash 映射，支撑增量编译（待建） | 每次 Ingest（机器维护） |

### MOC（Map of Content）

tag 交叉索引，与 index.md（四分类扁平列举）互补。compiler 做法：读所有页面 frontmatter.tags → `groupByTag()` → 字母排序输出。纯机器，零 LLM 幻觉。

OpenClaw 差异：tags 需按维度分层归一化。当前存在的语义问题——同概念多名字（"烧制工艺"/"烧制"/"烧成工艺"）、粒度平铺（"宋代"和"冰裂纹"同级）、维度混杂（时代/地区/材料/技法/窑口/制度/器物全放一起）。全库重编译时统一标签体系：按维度分层（时代 / 地区 / 材料 / 技法 / 窑口 / 制度 / 器物 / 人物），同概念归一化。

### 来源追踪与增量编译

compiler 的核心能力：`state.json` 记录每个源的 SHA-256 哈希 + 产出概念 slug 列表 + 编译时间。`detectChanges()` 逐文件 SHA-256 比对 → new/changed/unchanged/deleted。`buildConceptToSourcesMap()` 建 slug → 贡献源列表反向索引。源被修改或删除时，`findAffectedSources()` 通过 conceptMap 传播影响——共享同一概念的其他源也重新编译。删源时，与剩余源共享的概念 → frozenSlugs 保护；独有概念 → orphaned 标记。LLM 抽取失败 → 旧概念 freeze + 空 hash 触发重试。

OpenClaw 当前无源追踪机制。Claude 手工维护，信息存在会话记忆和 wiki 页面里，无法程序化查询。重编译后在 `knowledge/` 下建 `source-state.json`，脚本化 `conceptMap` 构建，支持跨源概念合并检测。

### 原子写入

所有 wiki 页面写入必须两步：

```
先写 page.md.tmp →     // Write 工具写入临时文件
校验（frontmatter 可解析 + body ≥ 50 字）→
rename 到 page.md       // 文件系统原子操作，不会留半截文件
```

compiler 用 `atomicWrite()`：`writeFile(tmpPath)` → `rename(tmpPath, filePath)`。`rename` 是原子系统调用——要么旧文件完整，要么新文件完整，不存在中间态。OpenClaw 当前 Write/Edit 直接覆写目标文件，中断可留截断页面。

### 任务状态机（硬约束）
```
pending → running → done
  ↑         ↓
  │       failed（任一步骤失败 → 原子回退）
  └── boss 指令重试
```
任务文件所在目录 = 任务真实状态。目录移动 + index.md 追加必须在同一轮完成。同一时间最多 1 个 running 任务。串行执行：当前 Step 全部 checkbox 勾完才能进下一个 Step。

### 任务 ID 格式
- `convert-YYYY-MM-DD-<slug>` — PDF 转换
- `ingest-YYYY-MM-DD-<slug>` — 知识收录
- `lint-YYYY-MM-DD` — 认知审计

## 核心操作

### 1. 转换（PDF → Markdown）
原子 4 步管道。任一步骤失败 → 全部回退。使用 MinerU（magic-pdf + vLLM）。质量检查强制执行五维：行数合理性、表格完整性、图片引用数、乱码率、章节结构。通过标准见 `KNOWLEDGE.md` §文档转换。

### 2. Ingest（全量提取）
逐页逐行逐字读源全文。提取所有实体和概念——不筛选、不评分、不设阈值。每个实体建页，每个概念建页。更新所有受影响的已有页面。更新 index.md、log.md、overview.md。Git commit。

**编译时 LLM 标记**（lint 只机审报告，不发现新问题）：
- 填满 frontmatter 所有必填字段（见下方「页面 frontmatter 关键字段」）
- 标 `confidence`（单源自动 ≤ medium）
- 标 `contradictedBy`（发现跨页矛盾时）
- 标 `provenanceState`（extracted / merged / inferred / ambiguous）
- 标 `aliases`（同义词，防重复建页）
- 标 `tags`（按维度分层）
- 发现幽灵实体（源中有但 wiki 未建页）→ 标记到 source-state.json

**书**：先喂目录建结构页 → 再逐章对话式 Ingest。骨架层书 boss 必须全程参与对话。

### 3. Query（跨源编织）
```
读 index.md → 定位页面 → 读 wiki 页面
  → wiki 够用 → 按 RULES.md §7 格式回答
  → wiki 不够 → web_search（最后手段）→ 标 🌐 + URL，置信度 low
```
**铁律**：禁止绕过 wiki 直接搜 web。每个断言必须能回溯到 wiki 页面。回答格式：问题界定 → 结论等级 → 核心回答 → 依据链 → 限制与反例 → 缺口与下一步。

### 4. Lint（机审 + 编译时标记）

核心原则：**编译时 LLM 标记，lint 时只机审报告。Lint 不发现新问题，只报告已标记问题。**

原七维概念审计已拆解：
- 新鲜度 → 砍掉。时间戳比较不解决真实质量问题
- 暗概念 → 保留为规则 #13
- 幽灵实体 → 移到编译时（LLM 在 Ingest 时标记到 source-state.json）
- 矛盾 → 移到编译时（LLM 写页时填 `contradictedBy`，lint 报告）
- 断链/孤立页 → 已是 #2、#8
- 覆盖报告 → 砍掉。改成 Ingest 统计看一眼
- 可疑高置信度 → 砍掉。编译时已约束单源 ≤ medium

#### 13 条机审规则（5 error + 8 warning）

| # | 规则 | 严重度 | 扣分 | 核心逻辑 | 阶段 |
|---|------|--------|------|---------|------|
| 1 | missing-frontmatter | error | -4 | 不以 `---` 开头 | 1 |
| 2 | broken-wikilink | error | -4 | `[[...]]` slug 不在全库页面集合中 | 1 |
| 3 | broken-citation | error | -4 | `^[source:行号]` 源文件不存在或行号越界 | 2 |
| 4 | malformed-claim-citation | error | -4 | `^[...]` 空条目/含`..`/行号非法 | 2 |
| 5 | duplicate-concept | error | -4 | title 归一化重复 + slug 编辑距离 < 3 | 1 |
| 6 | empty-page | warning | -1 | body < 50 字符 | 1 |
| 7 | missing-summary | warning | -1 | frontmatter.summary 缺失 | 2 |
| 8 | orphaned-page | warning | -1 | backlinks=0（反向引用计数） | 1 |
| 9 | low-confidence | warning | -1 | frontmatter.confidence < 0.5 | 1 |
| 10 | contradicted-page | warning | -2 | frontmatter.contradictedBy 非空（编译时标记） | 3 |
| 11 | schema-cross-links | warning | -1 | wikilink 数 < pageKind 最小阈值 | 1 |
| 12 | excess-inferred-paragraphs | warning | -1 | 无 `^[...]` 引用的 prose 段落 > 2 | 2 |
| 13 | dark-concepts | warning | -1 | [[wikilinks]] 被 ≥3 页引用但无独立页 | 1 |

**wikilink 最小阈值（#11 依据）**：
- entity ≥ 1（至少引用一个 source）
- concept ≥ 2（至少挂两个 entity 案例）
- synthesis ≥ 3（跨域论述需要更多证据链）
- source ≥ 0（源页面是被引用的对象）

**健康分**：`health_score = max(0, 100 - Σ扣分)`，error -4/条，contradicted -2/条，其他 warning -1/条。

**分阶段**：阶段 1（8 条：1/2/5/6/8/9/11/13）→ 阶段 2（4 条：3/4/7/12）→ 阶段 3（1 条：10）

## 页面 frontmatter 关键字段

以下字段对信任链至关重要，编译时必须全部填写：

- `provenanceState`：`extracted`（直接从源提取）| `merged`（多源合并）| `inferred`（LLM 跨源推断）| `ambiguous`（来源冲突）。区分"源里写的"和"LLM 串的"
- `aliases`：同义词列表，防重复建页
- `confidence`：0-1。编译时约束：单源 ≤ medium
- `contradictedBy`：矛盾页面引用列表 `[{slug, reason}]`。编译时 LLM 标记，lint 机审报告
- `tags`：按维度分层打标（时代 / 地区 / 材料 / 技法 / 窑口 / 制度 / 器物 / 人物），MOC 生成依赖

## 硬规则速查（来自 RULES.md）

- 🔴 每个断言必须能回溯到 ≥1 个 wiki 页面。绝不捏造。
- 🔴 禁止绕过 wiki 直接搜 web。wiki 优先，web 是最后补充。
- 🔴 证据不足时说"不足以判断"，不得编造。
- 🔴 飞书任务 >10 秒 → 先写任务文件 + 发回执，再后台执行。
- 🔴 删除/覆盖/发布 → 必须先确认。
- 🔴 不得自行修改 Schema 文件（AGENTS/KNOWLEDGE/SOUL/RULES/LARK/TOOLS）。先提议 → 确认 → 再执行。
- 🔴 web 内容 → 只能写入 `knowledge/web-buffer/`。boss 审定前不得进入 `wiki/`。
- 🔴 token、密钥、appSecret → 绝不输出，绝不提交。
- 🔴 上下文压缩恢复：检查 running 任务 → 读任务文件 → 从最后完成步骤继续。

## 来源等级
| 等级 | 含义 | 例子 |
|------|------|------|
| 一手 | 原始文献、官方文档、考古报告 | 窑址发掘报告、清宫档案 |
| 二手 | 研究专著、整理著作 | 有泉《陶瓷简史》 |
| 待验证 | 网页、聊天、出处不明的说法 | 论坛帖子、口述 |

## 关键路径
```
knowledge/raw/              不可变原始来源（PDF 等）
knowledge/converted/        MinerU 转换产物（<tool>/<task-id>/）
knowledge/web-buffer/       隔离的 web 内容（待 boss 审定）
knowledge/wiki/             知识页（sources/ entities/ concepts/ syntheses/）
knowledge/tasks/            任务文件（pending/ running/ review/ done/ failed/）
knowledge/templates/        页面模板和任务模板
knowledge/inbox/            飞书临时落地（处理完清空）
.agents/skills/             技能定义
openspec/                   变更提案与设计文档
tools/                      封装脚本（magic-pdf、start-vllm）
```

## 关键模板
- 知识页：`knowledge/templates/entry.md`
- 来源页：`knowledge/templates/source.md`
- 收录任务：`knowledge/templates/ingest-task.md`
- 领域元信息：`knowledge/templates/domain.md`

## 知识库当前状态
- **总页数**：140 — 全量编译完成（2026-06-09）
- **排队来源**（5 本）：《陶瓷简史》《参天台五台山记》《参天台五台山记研究》《北宋河北边防建设研究》《日本藏三方北宋官印考》
- **当前任务**：`convert-2026-06-08-ceramic-history` — Step 2（vLLM 已启动，待执行转换）
- **活跃领域**：宋代全史（陶瓷/茶/社会生活/军事/宗教/交通/服饰等）
