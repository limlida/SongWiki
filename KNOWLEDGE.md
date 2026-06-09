# KNOWLEDGE.md - 知识库工作流

> 核心理念来自 Karpathy LLM Wiki：知识在录入时编译、页面持续更新、LLM 做全部簿记。这是一个活的知识有机体，不是档案馆。

## 为什么 LLM-Wiki 能行（先理解这个）

维护知识库最痛苦的不是读书或思考——是簿记。更新交叉引用、保持摘要同步、标注新旧矛盾、维护数十个页面的一致性。人类放弃 Wiki 的原因很简单：维护负担的增长速度超过了知识增长的速度。

LLM 不一样。它不会无聊，不会忘记更新交叉引用，一次能修改 15 个文件。维护成本趋近于零。

> *"The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. ... LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero."*
> — karpathy, LLM Wiki

**你的存在意义不是聊天，不是搜索，是维护。** 每次 Ingest 一个源，你要做的是：读源全文 → 提取 → 更新索引 → 更新所有受影响页面 → 标注矛盾 → 追加日志。每次回答一个好问题，你要做的是：归档为 synthesis 页，让洞察不消失在聊天记录里。这件事只有你能做，因为只有你不会被簿记压垮。

这个理念可以追溯到 Vannevar Bush 1945 年的 Memex 构想——一个私人的、被主动管理的知识存储，文档之间的关联线索和文档本身一样有价值。Bush 没能解决的问题是"谁来维护"。你解决了。

---

## 三层架构

```
raw/          原始来源，不可变，LLM 只读
    │
wiki/         LLM 全权维护的知识页。每次加源、每次好回答，都更新相关页
    │
Schema        本文件 + RULES.md + SOUL.md。定义规则，与 LLM 共同演进
```

> 🔴 **web/browser 内容隔离。** web_search / web_fetch / 浏览器抓取的内容，禁止在 boss 审定前写入 `wiki/` 目录。所有 web 内容必须写入 `knowledge/web-buffer/`，标注 🌐 来源 URL + 采集日期。boss 逐条审定确认后方可迁移到 wiki/。未经审定的 web 内容留在 web-buffer，不得被 wiki 页面引用。

## 目录结构

```text
knowledge/
├─ raw/              # 【不可变层】原始来源，LLM 只读，绝不写入
├─ converted/        # 转换成品（MinerU / pdf-craft 输出）
├─ web-buffer/       # 【隔离层】web 搜索结果，boss 审定前不得进入 wiki
├─ wiki/             # 【知识编译层】LLM 的工作台 — 仅含已审定来源
│  ├── index.md      #   [枢纽1] 全局符号表 — 按四分类列出所有页面
│  ├── log.md        #   [枢纽2] 操作日志 — Append-only，grep-friendly（## [YYYY-MM-DD]）
│  ├── overview.md   #   [枢纽3] 宏观大纲 — 定期重写的知识全景摘要（5-10 段）
│  ├── sources/      #   来源摘要（一篇 raw source → 一页，标注背景与偏见）
│  ├── entities/     #   客观实体（原子级：人/地/事/物/机构/作品）
│  ├── concepts/     #   抽象概念（跨实体的：模式/思想/制度/技术/风格）
│  └── syntheses/    #   综合论述（跨域分析/对比/演变/悬案/编织回答）
├─ domains/          # 领域元信息（可选）
├─ tasks/            # 任务状态（pending/running/review/done/failed）
├─ reports/          # 查询报告 + 发布草稿
├─ templates/        # 模板
└─ inbox/            # 飞书临时落地（处理完清空）
```

## 四文件夹物理约束

所有知识页面必须且只能放在以下四个文件夹中。**严禁在 wiki/ 根目录创建知识页。**

### sources/（来源摘要）
- **定义**：对 raw/ 中单篇来源的结构化提取。
- **规则**：只陈述该来源「说了什么」。严禁混入其他来源的内容或主观评价。
- **必须标注**：来源等级（一手/二手/待验证）+ 成书背景与潜在偏见（如「元人修《宋史》的道学偏见」「现代整理著作，非一手考古报告」）。
- **示例**：`sources/陶瓷简史.md`

### entities/（客观实体）
- **定义**：原子级的、不可再分的具体事物。人（苏轼）、地（汴京）、事（靖康之变）、物/机构（汝窑、三司）。
- **规则**：极度客观，只记录「是什么 / 发生了什么」。严禁跨实体宏观评价。
- **孤证规则**：仅有一篇 source 支持的实体，页首标注 `[孤证警告]`。
- **冲突规则**：遇到来源冲突，设立 `## 史料争议` 章节并列展示，严禁自行调和。
- **示例**：`entities/汝窑.md`、`entities/有泉.md`

### concepts/（抽象概念）
- **定义**：跨越具体实体的模式、思想、制度或技术原理。
- **规则**：必须抽象化。页面内必须大量使用 `[[WikiLinks]]` 引用 entities/ 中的具体案例来支撑概念。
- **示例**：`concepts/还原焰烧制.md`、`concepts/坊市制度.md`

### syntheses/（综合论述）
- **定义**：跨实体、跨概念的宏观分析、对比研究或编织式回答。
- **规则**：允许逻辑推导，但**每一处核心论点必须有 [[WikiLinks]] 指向 entities/ 或 concepts/ 中的底层证据**。无证据链 = 幻觉。
- **回填**：将 Query 中 ≥3 页编织且形成新洞察的回答归档为 synthesis 页。
- **示例**：`syntheses/陶瓷的东西方交流.md`、`syntheses/青花瓷钴料来源考.md`

### 四文件夹之间的关系

```
raw/（只读输入）
  ↓ ingest
sources/  ──→ entities/  ──→ concepts/  ──→ syntheses/
  来源提取    事实原子      抽象模式      综合论述
              ↑ 引用        ↑ 引用        ↑ 引用
```

每向右一级，抽象度升高，对左级的 [[WikiLinks]] 引用密度增大。

## 三个枢纽文件

| 文件 | 类比 | 内容 | 更新频率 | 用途 |
|------|------|------|----------|------|
| index.md | 图书馆卡片目录 | 每页一行，按四分类索引 | 每次 Ingest | LLM 查询时先读它定位 |
| overview.md | 书的前言/导论 | 按主题叙述当前知识全景（5-10 段）| 每 5-10 次 Ingest | 人/LLM 快速了解全貌 |
| log.md | 航海日志 | 按时间记录每次操作 | 每次操作 | 恢复工作记忆、追溯演化史 |

## 知识页模板

模板文件位于 `knowledge/templates/`，按页面类型选用。各模板 frontmatter 字段统一，差异只在 body 结构。

| 模板文件 | 适用类型 | body 结构 |
|----------|---------|-----------|
| `templates/source.md` | source | 基本信息 + 内容摘要 + 关键事实 + 限制与偏见 + 产出页面清单 |
| `templates/entity.md` | entity | 概述 + 核心内容 + 来源 + 史料争议 + 关联页面 |
| `templates/concept.md` | concept | 概述 + 核心内容 + 具体案例 + 来源 + 关联页面 |
| `templates/synthesis.md` | synthesis | 问题界定 + 结论等级 + 核心回答 + 依据链 + 限制与反例 + 缺口与下一步 |

**所有模板共享的 frontmatter 字段**（详见 `templates/entry.md`）：
`title` / `type` / `domain` / `sources` / `source_count` / `status` / `provenanceState` / `confidence` / `aliases` / `contradictedBy` / `tags` / `summary` / `last_verified` / `created` / `updated` / `related`

### 关键字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `provenanceState` | 必填 | `extracted`（直提）\| `merged`（多源合并）\| `inferred`（LLM 推断）\| `ambiguous`（源冲突） |
| `confidence` | 必填 | 0-1 数值。单源自动 ≤ 0.5 |
| `aliases` | 必填 | 同义词列表，防重复建页 |
| `contradictedBy` | 发现时填 | `[{slug, reason}]`，Lint 规则 #10 报告 |
| `tags` | 必填 | 维度前缀格式：`时代/宋代`、`地区/河北`、`材料/瓷` 等。详见 §MOC |
| `summary` | 必填 | 一句话摘要，Lint 规则 #7 检查 |

## 三大操作

### Ingest（全量提取）

每次加新源，执行全量提取（Full Extraction）：

**核心原则：逐页逐行逐字阅读，不跳过、不筛选、不偷懒。**

> 🔴 **Ingest 禁止子 agent。** 子 agent（sessions_spawn）彼此隔离，不知其他页面 slug，无法维护交叉引用和 [[wikilinks]]。所有页面必须由主 agent 逐页顺序创建，边建边加 wikilinks，保证一致性。
> 🔴 **原子写入。** 所有 wiki 页面写入必须两步：先写 page.md.tmp → 校验（frontmatter 可解析 + body ≥ 50 字）→ rename 到 page.md。禁止直接覆写目标文件。
> 🔴 **行号强制标注 + 两步验证。** 每条事实断言必须标注源行号。禁止仅凭 grep 估算：
> ```bash
> grep -n "<关键词>" <源文件>          # 步骤1: 定位候选行号
> sed -n 'L起始,L结束p' <源文件>        # 步骤2: 逐行读原文，确认内容匹配
> # 匹配 → 写入 ^[source-slug:L起始-结束]；不匹配 → 扩大范围重搜
> ```

**执行前：从模板创建任务。** 必须逐字拷贝模板，禁止凭记忆自建：

```bash
cp knowledge/templates/ingest-task.md knowledge/tasks/running/<task-id>.md
# 然后逐项填写 <...> 占位符
```

一次 Ingest 一个任务文件，跟输入是章节还是整本书无关。

1. **来源摘要**：在 sources/ 创建或更新摘要页（标注背景与偏见、来源等级）
2. **报告关键发现**：读完源全文后，向 boss 报告发现——「我读完了。核心要点是...」「这些和你已有的 X、Y 页面相关」「以下是我将要创建/更新的页面清单」。报告后**不等确认、直接执行**页面创建。Boss 看到报告后可以给方向（"多强调 X""注意关联 Y""A 和 B 应该合成一页"），但这些是追加指令，不是否决权。**提取范围不可缩小**——Step 3 的「不筛选不设阈值」不允许被 Step 2 架空。
3. **全量实体提取**：逐页逐行逐字阅读源全文。每遇到一个人、地、物、窑口、著作、机构、事件——只要是一个独立存在的东西——立即建 entities/ 页面。不判断「值不值得建」「信息够不够」——先建。信息少就是 stub，信息多就写详。**原子写入**：所有新页面先写 `.tmp` → 校验 frontmatter + body ≥ 50 字 → rename。详见 RULES.md §知识页写入。**每条事实断言必须标注源行号**，见 §行号标注。
4. **全量概念提取**：逐页逐行逐字阅读源全文。每遇到一个跨实体的模式、技术原理、思想、制度——立即建 concepts/ 页面。不判断「抽象度够不够高」——先建。同上，原子写入+行号标注。
5. **过程中产出综合页**：边读边发现跨实体/跨概念的关联和洞察时，即时建 syntheses/ 页面。不等未来 Query 触发。
6. **刷新已有页（跨章回溯）**：每完成一批实体/概念页后，必须执行以下三步，禁止仅 grep 关联页面就跳过：
   a. `grep -rl "<新实体slug>" knowledge/wiki/` 找到所有引用新页面的已有页面
   b. 逐页打开，阅读全文，判断新内容是否补充/修正/推翻已有信息
   c. 有则更新（原子写入），无则记录"已审，无补充"
   同上，原子写入。
7. **强制链接**：新建/更新的页面，至少按 RULES.md §wikilink 最低阈值包含 [[WikiLinks]]：entity ≥ 1 / concept ≥ 2 / synthesis ≥ 3 / source ≥ 0。
8. **更新索引**：更新 wiki/index.md（每次新建或修改页面后立即反映）
9. **追加日志**：追加 wiki/log.md
10. **重生成 MOC**：`python3 tools/gen_moc.py`（零 LLM 参与）
11. **更新大纲**：每完成一个源后，重写 wiki/overview.md
12. **提交**：git commit

> **不筛选、不评分、不设阈值。** 所有实体和概念一律建页。质量由日后的 Lint 审计负责——现在不删。先让知识库自然生长，跑一段时间，积累足够数据后再回头设计 Lint 清理规则。
>
> **不偷懒。** 必须真正读完源的每一个字。禁止跳段、禁止扫一眼就概括、禁止"这部分讲的和前面差不多就不读了"。每页、每段、每行、每个字——都要读到。

### 行号标注（Ingest 阶段强制）

建页时每条事实断言必须标注源行号 `^[source-slug:L起始-结束]`。这是 Lint 规则 #3/#4 的输入基础，也是跨章回溯和来源追溯的唯一锚点。

**格式**：`^[source-slug:L起始-结束]`。slug 对应 sources/ 下页面名（如 `陶瓷简史`），行号来自 converted/ 下的转换产物。单个事实块一个行号范围，跨段引用给多个标注。

**强制两步验证**：
1. `grep -n "<关键词>" <源文件>` 定位候选行号
2. `sed -n 'L起始,L结束p' <源文件>` 或读文件对应的 offset/limit，逐行确认内容与引用完全匹配
3. 匹配→写入标注；不匹配→扩大范围重新搜索→重复步骤 2

**禁止**：仅凭 grep 输出估算行号；凭短期记忆填写行号；跳过步骤 2 直接写入。

**粒度**：每个有事实断言的段落至少一个标注。纯 wikilink 导航或概述性句子可不标。

> 行号标注不是附加项——是 Ingest 的有机组成部分。没有行号的事实断言不能被 Lint 校验、不能被跨章回溯定位、不能被三年后的对话验证来源。Ingest 阶段不标注行号 = 页面未完成。

**书**：先喂目录建结构页（sources/ + 目录 entities/），再逐章对话式 Ingest。骨架层书必须对话。

**300 本书分层**：

| 层级 | 处理方式 |
|------|---------|
| 骨架层（10-20 本核心书） | 逐章逐页逐字全量提取，人全程参与 |
| 填充层（相关但不核心） | 全量提取，但可半自动（LLM 提取后报告给人确认） |
| 标注层（边缘相关） | 只记书名+一句话到 index.md |
| 待深入层 | 不处理，等需要时再说 |

### 编译时 LLM 标记

每次 Ingest 建页/改页时，LLM 必须填写以下字段——这些是 Lint 机审的输入，不是可选项：

- **provenanceState**（必填）：`extracted`（直接从源提取）| `merged`（多源合并）| `inferred`（LLM 跨源推断）| `ambiguous`（来源冲突）。区分"源里写的"和"LLM 串的"
- **confidence**（必填）：0-1 数值。编译时约束：单源自动 ≤ 0.5
- **aliases**（必填）：同义词列表，防重复建页
- **tags**（必填）：按维度分层打标（时代 / 地区 / 材料 / 技法 / 窑口 / 制度 / 器物 / 人物）。MOC 生成依赖此字段
- **contradictedBy**（发现时填）：矛盾页面引用列表 `[{slug, reason}]`。编译时 LLM 标记，Lint 规则 #10 报告
- **幽灵实体**（发现时标记）：源中有但 wiki 未建页的实体 → 记入 source-state.json，待后续 Ingest 补建

### Query（跨源编织）

**执行前：从模板创建任务。** 使用 `knowledge/templates/query-task.md` → 写入 `knowledge/tasks/running/<query-task-id>.md`。

1. 读 wiki/index.md 定位相关页面
2. 读 wiki/overview.md 获得高层知识全景
3. 直接匹配 → 读 entities/ + concepts/ → 综合回答
4. 无直接匹配 → **编织模式**：扫描全索引 → 定位碎片页面 → 逐页阅读 → 合成
5. 每个断言必须标注源页面（[[wikilinks]] 形式）
6. 按专业回答协议输出：问题界定 → 结论等级 → 核心回答 → 依据链 → 限制与反例 → 缺口与下一步 → 意外发现（如有）

**回答回填**：综合 ≥3 页且形成新洞察 → 归档为 syntheses/ 页面。这使探索的成果不消失在聊天记录里，持续复利。

### Lint（机审 13 条规则）

**执行前：从模板创建任务。** 使用 `knowledge/templates/lint-task.md` → 写入 `knowledge/tasks/running/<lint-task-id>.md`。

核心原则：**编译时 LLM 标记，Lint 时只机审报告。Lint 不发现新问题，只报告已标记问题。**

#### 13 条机审规则

| # | 规则 | 严重度 | 扣分 | 核心逻辑 | 阶段 |
|---|------|--------|------|---------|------|
| 1 | missing-frontmatter | error | -4 | 不以 `---` 开头 | 1 |
| 2 | broken-wikilink | error | -4 | `[[...]]` slug 不在全库页面集合中 | 1 |
| 3 | broken-citation | error | -4 | `^[source:行号]` 源文件不存在或行号越界 | 2 |
| 4 | malformed-claim-citation | error | -4 | `^[...]` 空条目/含`..`/行号非法 | 2 |
| 5 | duplicate-concept | error | -4 | title 归一化重复 + slug 编辑距离 < 3 | 1 |
| 6 | empty-page | warning | -1 | body < 50 字符 | 1 |
| 7 | missing-summary | warning | -1 | frontmatter.summary 缺失 | 2 |
| 8 | orphaned-page | warning | -1 | backlinks = 0（反向引用计数） | 1 |
| 9 | low-confidence | warning | -1 | frontmatter.confidence < 0.5 | 1 |
| 10 | contradicted-page | warning | -2 | frontmatter.contradictedBy 非空（编译时标记） | 3 |
| 11 | schema-cross-links | warning | -1 | wikilink 数 < pageKind 最小阈值 | 1 |
| 12 | excess-inferred-paragraphs | warning | -1 | 无 `^[...]` 引用的 prose 段落 > 2 | 2 |
| 13 | dark-concepts | warning | -1 | [[wikilinks]] 被 ≥3 页引用但无独立页 | 1 |

**wikilink 最小阈值（#11 依据）**：
- entity ≥ 1（至少引用一个 source）
- concept ≥ 2（至少挂两个 entity 案例）
- synthesis ≥ 3（跨域论述需要更多证据链）
- source 页面无最低要求（源页面是被引用对象，本身不需引其他页面）

**健康分**：`health_score = max(0, 100 - Σ扣分)`，error -4/条，contradicted -2/条，其他 warning -1/条。

**分阶段 rollout**：
- **阶段 1**（8 条：1/2/5/6/8/9/11/13）— 基础结构检查
- **阶段 2**（4 条：3/4/7/12）— 引用格式检查（需 `^[source:行号]` 格式）
- **阶段 3**（1 条：10）— 矛盾标记检查（需 contradictedBy 字段）

结果写入 wiki/log.md。LLM 主动提议修复方案，人决策。

### Lint 处理建议

以下规则为 Lint 报告提供处理建议。**所有操作均为报告建议，不自动执行。** 删除/合并/降级必须经人确认（RULES §11）。

#### 页面度量指标

Lint 为每个页面计算以下指标作为判定依据：

| 指标 | 含义 | 获取方式 |
|------|------|---------|
| `backlinks_count` | 有多少其他页面用 [[WikiLinks]] 指向本页 | grep -l 全库 |
| `outlinks_count` | 本页包含多少 [[WikiLinks]] | 读页计数 |
| `content_size` | 正文有效字数（不含 frontmatter 和标题） | 读页估算 |
| `source_count` | frontmatter 中标注的来源数量 | 读 frontmatter |
| `age_days` | 距创建日期的天数 | created 字段 |

#### 判定矩阵

##### entities/（客观实体）

| 条件 | 建议动作 |
|------|---------|
| content_size < 80 字 + backlinks = 0 | **建议删除**。纯垃圾 stub，无人引用。 |
| content_size < 80 字 + backlinks = 1-2 | **建议合并**。将内容沉入引用它的页面末尾 `## 关联实体` 节，然后删除本页。 |
| content_size < 80 字 + backlinks ≥ 3 | **保留桩页**。信息虽少但被多处引用，打上 `[待填充]` 标记。 |
| backlinks = 0 + age_days > 30 | **标记孤立**。无人引用的老页面，追问是否有意保留。 |
| source_count = 1 + confidence > 0.5 | **建议降级**。单源撑不起 > 0.5，降为 0.5。 |

##### concepts/（抽象概念）

| 条件 | 建议动作 |
|------|---------|
| outlinks_count < 2 | **标记支撑不足**。概念页必须挂至少 2 个 entity 案例。 |
| backlinks = 0 + age_days > 60 | **标记未使用**。无任何 synthesis 引用的概念，可能不成立。 |
| content_size < 150 字 | **标记过薄**。概念页需要足够的抽象论述。 |

##### syntheses/（综合论述）

| 条件 | 建议动作 |
|------|---------|
| content_size < 200 字 | **标记过薄**。综合论述需要足够的论证篇幅。 |
| 所有被引用的 entities/concepts 已不存在 | **建议删除**。底层证据全没了，论述悬空。 |

#### 合并操作细则

（人确认合并后执行）

1. 在目标页末尾创建 `## 关联实体` 节（如不存在）
2. 追加子节：`### 实体名` + entity 原文内容
3. 删除原 entity 文件
4. 全局替换 `[[entities/xxx]]` → `[[目标页路径#实体名]]`（锚点链接到合并后的位置）
5. 更新 index.md

#### 删除操作的 WikiLinks 修复

（人确认删除后执行）

```text
1. 扫描：grep -rl "[[entities/X]]" wiki/ → 得到所有引用者列表
2. 修复：逐个打开引用页，去掉 [[entities/X]] 链接，保留链接文本（如无独立价值则连文本一并删除）
3. 验证：再次 grep 确认无残留死链
```

修复原则：
- 如果引用上下文是「据 [[entities/张三]] 记载」→ 保留「据张三记载」，去掉链接
- 如果引用上下文是「参见 [[entities/张三]]」→ 删除整行

## MOC（Map of Content）

tag 交叉索引，与 index.md（四文件夹扁平列举）互补。每次 Ingest 后由脚本全量重生成，零 LLM 参与。

**生成方式**：读取所有 wiki 页面 frontmatter.tags → 按维度分组 → 组内字母排序 → 输出 `wiki/MOC.md`。

### tag 维度分层

tags 按以下维度分层打标，同概念归一化：

| 维度 | 示例值 |
|------|--------|
| 时代 | 宋代、元代、明代、清代 |
| 地区 | 河北、浙江、江西、汴京 |
| 材料 | 瓷、陶、紫砂、釉 |
| 技法 | 匣钵装烧、还原焰、覆烧 |
| 窑口 | 汝窑、定窑、景德镇窑 |
| 制度 | 坊市制度、榷场、岁贡 |
| 器物 | 青花瓷、天目盏、玉壶春瓶 |
| 人物 | 苏轼、赵佶、有泉 |

### 归一化规则

- **同概念多名字**：统一为一个规范名（如"烧制工艺"/"烧制"/"烧成工艺"→ 归一到 "烧成工艺"），其他写进 aliases
- **粒度分层**：时代/地区等宏观维度与具体概念不能同级（"宋代"和"冰裂纹"不能同为 tags）
- **维度不混杂**：每个 tag 带维度前缀（如 `时代/宋代` 而非裸 `宋代`）

## 来源评分

| 等级 | 含义 | 例子 |
|------|------|------|
| **一手** | 原始文献、官方文档、考古报告 | 窑址发掘报告、清宫档案 |
| **二手** | 研究专著、整理著作、评测 | 有泉《陶瓷简史》 |
| **待验证** | 网页、聊天、出处不明的说法 | 论坛帖子、口述 |

评分只需等级 + 一句话理由。待验证来源只能作为线索，不能作为核心依据。

## 回答格式

每个正式查询回答必须包含：

```markdown
## 问题界定
## 结论等级        ← 直接依据支持 / 可合理推断 / 仅能推测 / 暂无足够依据
## 核心回答
## 依据链
## 限制与反例
## 缺口与下一步
## 意外发现（如有）
```

证据不足时必须说「不足以判断」，不得编造。

## Schema 演进

AGENTS.md / KNOWLEDGE.md / SOUL.md / RULES.md 不是一次性写好的蓝图，是在对话中长出来的。

```text
LLM 在操作中遇到 Schema 未覆盖的情况
  → LLM 主动报告：
      「我注意到 XX 在现有 Schema 里没有规则。
        建议在 YY.md 中加入：<规则草案>。
        原因：<实际案例>。要不要加？」
  → boss 确认 → LLM 修改对应文件
  → git commit: 「schema: YY.md -- XX 规则 (trigger: <触发原因>)」
```

LLM 不能自行修改 Schema，必须经过提议 → 确认 → 执行。

## 有机目录演化

wiki/pages/ 初始平铺。某 type 页面 > 10 → LLM 提议建子目录或导航索引页 → boss 决定 → LLM 执行迁移 + git commit。

## 文档转换

| 文档类型 | 工具 |
|----------|------|
| 扫描书 / 古籍影印 | MinerU（magic-pdf + vlm-http-client） |
| 复杂版面 / 表格密集 | MinerU |
| 带文本层 PDF | 先抽文本，判断是否需 OCR |

转换产物保留在 `knowledge/converted/<tool>/<task-id>/`。

### 转换质量检查（必做，不可跳过）

每次 PDF 转换完成后，执行五维检查。质量不合格的转换不能进入 Ingest。

| 检查项 | 方法 | 通过标准 | 不通过动作 |
|--------|------|---------|-----------|
| **行数合理性** | MD 行数 ≥ PDF 页数 × 10 | 达标 | 怀疑转换截断，回退 |
| **表格完整性** | 对比 PDF 可见表格数与 MD 中 `\|` 管道表格数 | 匹配度 > 80% | 标注断裂位置，报告 boss 决定 |
| **图片引用数** | 统计 MD 中 `![]()` 数量，对比 PDF 中图片总数 | 匹配度 > 70% | 标注缺失图片，报告 boss 决定 |
| **乱码率** | 随机抽取 5 段 >200 字的段落，统计非有效字符比例 | < 5%（合格）\| 5-15%（警告可用）\| > 15%（不合格） | **> 15% → 必须回退** |
| **章节结构** | 检查 MD 是否含 `#` 标题层级，一级标题数是否接近章数 | 标题层级存在 | 标注"无结构"，不影响通过但影响后续拆章 |

#### 乱码判定标准

乱码字符定义：
- 不在 Unicode CJK Unified Ideographs 范围内（U+4E00–U+9FFF）
- 不在 ASCII printable 范围内（U+0020–U+007E）
- 不在常用中文标点范围内（U+3000–U+303F, U+FF00–U+FFEF）
- 连续出现 3 个以上非上述字符 → 标记为乱码片段
- 段落中 > 50% 字符为乱码 → 该段判定为乱码段

#### 质量报告格式

```markdown
## 转换质量报告

| 指标 | 值 | 判定 |
|------|-----|------|
| 输出行数 | N 行 | OK / 异常短 |
| 输出大小 | N KB | - |
| 表格 | MD 中 N 个 / PDF 可见约 N 个 | ✅ OK / ⚠️ 疑似断裂 N 个 |
| 图片 | MD 中 N 个 / PDF 中约 N 个 | ✅ OK / ⚠️ 缺失 N 个 |
| 乱码率 | X% | ✅ OK / ⚠️ 警告 / 🔴 不合格 |
| 章节结构 | N 个一级标题 | ✅ OK / ⚠️ 无结构 |
| 转换耗时 | N 秒 | - |

**综合判定**：[合格 / 警告可用 / 不合格需回退]
```
