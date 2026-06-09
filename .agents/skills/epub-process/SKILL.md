---
name: epub-process
description: >-
  EPUB 文档重排与语义修复管线。对 MinerU/OCR 解析出的碎片化 Markdown 执行结构清洗、语义缝合、
  排版净化与版式语义标注，输出 EPUB-ready 的优化 Markdown。作为 book-to-epub 管线的 Process 阶段。
metadata:
  openclaw:
    emoji: "📖"
    requires:
      bins: [python3]
    pipeline: book-to-epub
    stage: Process
    version: "2.0.0"
    evolved_from: "1.0.0 (达尔文优化)"
    upstream: MinerU OCR 输出
    downstream: Review-A (标注审核) → EPUB 构建 → Review-B (渲染审核)
---

# EPUB 文档重排与语义修复管线 (EPUB-Process v2.0)

## 🎯 定位

本 Skill 是 **book-to-epub 管线**的 Process 阶段。上游接收 MinerU OCR 输出的碎片化 Markdown，下游交付优化后的 Markdown 给 Review-A（标注审核），最终经 Calibre 构建 EPUB。

```
MinerU OCR → [ epub-process (本 Skill) ] → Review-A → EPUB 构建 → Review-B
              ├─ 文本清洗 (R0-R8)
              └─ 版式语义标注 (R9-R10)
```

## 🛡️ 核心红线 (绝对不变)

1. **Zero Information Loss**：严禁总结、概括、缩写或删减原文细节。
2. **Zero Hallucination**：不引入外部知识，不脑补缺失内容，不篡改作者立场。
3. **Tag Safety**：只输出标准 Markdown + 限定的 HTML class（`<figure>` / `<span class="caption">` / `<div class="chapter-start">` / `<div class="sidebar-nav">` / `<div class="footnote">`）。所有标签必须闭合。
4. **保守标注**：无法确定版式语义时，保留为普通图片/段落，写入 QUALITY_REPORT `【待确认】` 项。宁可漏标，不可错标。

---

## ⚙️ 规则管线 (R0 → R10)

### R0: 结构诊断 (Structure Scan) — 执行前必做

通读全文 10-15 秒，在后台识别并记录（不输出思考过程）：

- **标题层级**：H1/H2/H3 分布，是否有 H1→H3 跳级或标题缺失
- **图片密度**：每 1000 字图片数，判断是否需要版式语义标注（>3 张/千字 → 必须标注）
- **特殊元素**：诗词/歌诀、代码块、脚注/尾注、化学式 LaTeX、表格碎片
- **目录位置**：目录页的起止行（用于 R2 TOC 提取）

### R1: 标题层级归一化 (Heading Normalize)

规则：

1. **唯一书名 H1**：原书书名 → `# 书名`。若书中无书名行，从文件名/元数据推断并写入首行。
2. **篇/章名 → H2**：`## 第X章 章名` 或 `## X. 章名`。
3. **章号合并**：若 OCR 将章号与章名拆为两行（`## 1` + `## 火篇`），合并为 `## 1. 火篇`。
4. **子章节 → H3**：`### 子节名`。严禁 H2 直接跳 H4。
5. **目录页标题降级**：目录页内的 `##` 标题 → `**粗体**`（避免 Calibre 将目录条目误入 EPUB TOC）。
6. **四级+ → 粗体**：`####` 及以上 → `**标题**`（EPUB TOC 最多三级）。

### R2: 目录页 TOC 提取与对齐

1. **识别目录页**：搜索 `目录` / `目次` / `CONTENTS` 关键词，标记起止行。
2. **提取层级结构**：从目录页解析 `第X章 → 节 → 子节` 的层级关系。
3. **对齐正文**：正文的 H2/H3 数量与顺序必须与 TOC 一致。不一致时优先信任 TOC 结构（原书目录通常比 OCR 更可靠）。
4. **缺失处理**：正文缺章 → 保留 TOC 条目并标注 `【待确认：正文缺失】`。TOC 缺条目 → 从正文 H2 推断补入。

### R3: MinerU 遗留块清除

精准定位并彻底删除以下冗余块（正则匹配）：

| 遗留块模式 | 正则 |
|-----------|------|
| natural_image 折叠块 | `<details><summary>natural_image.*?</details>` |
| seal 折叠块 | `<details><summary>seal.*?</details>` |
| 空 details 标签 | `<details>\s*</details>` |
| 残留 `<p>` 包裹 | `<p>\s*</p>` |

### R4: 图片切词修复 (Image-Split Fix)



**触发条件**：图片标签夹在词语/短句中间，前后各 ≤8 字符。

**判定方法**（基于**语法连贯性**，非语义成词）：

1. 提取图片前后各 ≤8 字符的文本碎片。
2. 拼接后判断：**图片插入位置是否明显割裂了一个连贯的词组、短语或语法单元？**
   - ✅ 割裂：`政` + `府` → `政府`（双字词被切断）、`发` + `现` → `发现`（动词被切断）、`氧化` + `铁` → `氧化铁`（术语被切断）
   - ❌ 未割裂：前后文是独立句子或分句，图片恰好在句间断点，如 `他抬起头。` + `[图]` + `阳光刺眼。`（两句独立，图片在句号后）
3. 无法判断时 → 保守保留，写入 QUALITY_REPORT `pending`。

**修复动作**：
1. 将前后文本碎片无缝拼接（如 `政` + `府` → `政府`）。
2. 找到拼接后最近的句号/感叹号/问号。
3. 将图片块整体移至该句号之后。

### R5: 图片标题标记 (Caption Bind)



**触发条件**：图片下方紧跟 `<80` 字符、无句号、描述图片细节或来源的短文本。

**动作**：包裹为 `<span class="caption">文本</span>`，置于 `<figure>` 内部或紧挨图片下方。

**排除**：不以数字/字母开头且 >80 字符的行 → 不是图注，是正文续段。

### R6: OCR 硬换行消除 (Hard-break Merge)

**触发条件**：连续两行 ——
- 上行以中文字符/中文标点结尾（排除 `。！？》」』）`
- 下行以中文字符开头
- 单行 `<30` 字
- 非诗歌/列表/表格行

**排除模式**（保留换行）：
- 以 `- ` / `1. ` / `* ` 开头的列表行
- 以 `|` 开头的表格行
- 五言/七言对齐的诗歌行（通过行字数一致性检测）
- 代码块内（` ``` ` 包裹区域）

### R7: 中西文混排空格 (Pangu Spacing)

> 即"盘古之白"规则。

1. **中文 + 英文/数字**之间插入半角空格：`使用 Markdown 格式`、`共计 100 人`。
2. **专有名词例外**：`iPhone15`、`GPT-4`、`C++` 等已内嵌数字/符号的专名不拆。
3. **中文 + 行内公式**：`收益率 $x$ 的公式`（`$` 前后留空格）。
4. **中文 + 全角标点**：不额外加空格。

### R8: 化学式去 LaTeX (Chemistry Clean)

| LaTeX 模式 | 替换为 |
|-----------|--------|
| `$\mathrm{Fe}_{2}\mathrm{O}_{3}$` | Fe₂O₃ |
| `$\mathrm{SiO}_{2}$` | SiO₂ |
| `$\mathrm{Al}_{2}\mathrm{O}_{3}$` | Al₂O₃ |
| `$\mathrm{CO}_{2}$` | CO₂ |
| `$\mathrm{H}_{2}\mathrm{O}$` | H₂O |
| `$\mathrm{CaCO}_{3}$` | CaCO₃ |
| `$\mathrm{TiO}_{2}$` | TiO₂ |
| `$\mathrm{Na}_{2}\mathrm{O}$` | Na₂O |
| `$\mathrm{K}_{2}\mathrm{O}$` | K₂O |
| `$\mathrm{MgO}$` | MgO |
| `$\mathrm{SO}_{2}$` | SO₂ |

**处理策略**：
1. 先执行上表精确替换。
2. 剩余 `$\mathrm{...}$` 模式 → 手动判断是否可以安全转 Unicode。
3. 无法安全转换的（如复杂有机分子式）→ 保留 LaTeX，标注 `【待确认：复杂化学式】`。

### R9: 版式语义标注 (Layout Semantic)

> 仅图文密集书籍（R0 判定 >3 张/千字）执行。需同步参考 PDF 页面图片。

| 语义 | HTML 标记 | 触发条件 | CSS 对齐 |
|------|----------|---------|---------|
| 篇章起始页 | `<div class="chapter-start">` | 新章第一页，通常有大标题/空白/装饰 | `chapter-start` |
| 单图 | `<figure class="figure-single">` | 页面仅 1 张大图 | `figure-single` |
| 并排图 | `<figure class="figure-pair">` | 页面 2 张图水平并排 | `figure-pair` |
| 整页图 | `<figure class="figure-fullpage">` | 图片占满整页，无正文 | `figure-fullpage` |
| 图注 | `<span class="caption">` | R5 判定 | `caption` |
| 侧栏导航 | `<div class="sidebar-nav">` | 重复出现的页边导航/提示文字 | `sidebar-nav` |
| 页眉页脚 | `<div class="page-header-footer">` | OCR 混入正文的页眉页脚文本 | `page-header-footer` |

**保守原则**：无法确定类型 → 保留为 `![](images/...)` 不标注 class，写入 QUALITY_REPORT。

### R10: 排版终净 (Final Polish)

1. **标点净化**：
   - 统一全角中文标点。消除连续标点（`，，` → `，`；`。。` → `。`）。
   - 中文语境下西文标点转全角（`，` 不用 `,`）。
2. **段首缩进**：**严禁**段首使用全角空格（`  `），EPUB 缩进由 CSS `text-indent: 2em` 控制。
3. **列表统一**：
   - 无序列表 → `- `
   - 有序列表 → `1. `
   - 嵌套列表缩进 2 空格
4. **表格重构**：散落的表格碎片按语义重构为标准 Markdown 表格（含 `|---|` 分隔线）。
5. **错词检查**（**仅报告不自动改**）：

   | 疑似错词 | 建议 |
   |---------|------|
   | 阀值 | 阈值 |
   | 登陆 | 登录 |
   | 布署 | 部署 |
   | 配制 | 配置 |
   | 起用 | 启用 |
   | 回朔 | 回溯 |
   | 标示 | 标识 |
   | 帐户 | 账户 |
   | 帐号 | 账号 |
   | 截止 | 截至 |
   | 搜寻 | 搜索 |
   | 做为 | 作为 |
   | 反回 | 返回 |

   匹配到的写入 QUALITY_REPORT `typo_flags`，不直接替换（避免误伤古文）。

---

## 📐 边界处理 (Edge Cases)

### 脚注/尾注

**检测**：`[1]` / `①` / `*` 开头的短行，出现在页底或章末。

**处理**：
- 将脚注文本包裹为 `<div class="footnote"><sup>N</sup> 注文</div>`
- 正文中保留上标标记 `[^N]` 或原文编号

### 诗词/歌诀

**检测**：连续 4 行及以上，每行字数接近（五言 5 字、七言 7 字），无句号。

**处理**：
- 保留原始换行，不执行 R6 合并
- 包裹为块引用：`> 诗句行`
- 标题行加 `**粗体**`

### 代码块

**检测**：` ``` ` 包裹区域，或等宽字体排版的行。

**处理**：
- 保留原始格式，不执行 R6/R7/R10
- 确保 ` ``` ` 开闭配对

### 中西文数字混排

**规则**：中文数字（一二三）与阿拉伯数字（123）之间的空格：
- `第一章 123 页` ✅
- `第123页` → `第 123 页`（插入空格）
- `2024年` → 保留（中文数字 + 年 是固定搭配）

---

## 📚 Few-Shot Demonstrations (6 例)

**Example 1: 图片切断 + 图注绑定 + 化学式 (R4+R5+R8)**
*Input:*
汉代是封建制，政
<figure class="figure-single">
  <img src="images/sheep.jpg" alt="" />
</figure>
府曾经多次下令。
西晋 青瓷羊 南京博物院
其釉料含 $\mathrm{Fe}_{2}\mathrm{O}_{3}$

*Output:*
汉代是封建制，政府曾经多次下令。

<figure class="figure-single">
  <img src="images/sheep.jpg" alt="" />
  <span class="caption">西晋 青瓷羊（南京博物院藏）。其釉料含 Fe₂O₃。</span>
</figure>

**Example 2: 硬换行 + 中西文混排 (R6+R7)**
*Input:*
同时
存在
对
数
收
益
率 $x$
的公式，共计100个。

*Output:*
同时存在对数收益率 `$x$` 的公式，共计 100 个。

**Example 3: 章号合并 (R1)**
*Input:*
## 1
## 火篇
### 从陶到瓷

*Output:*
## 1. 火篇
### 从陶到瓷

**Example 4: 脚注处理**
*Input:*
明清时期景德镇瓷器远销欧洲¹。
...
¹ 据《景德镇陶录》记载，每年输出约 300 万件。

*Output:*
明清时期景德镇瓷器远销欧洲[^1]。

<div class="footnote"><sup>1</sup> 据《景德镇陶录》记载，每年输出约 300 万件。</div>

**Example 5: 诗词保留**
*Input:*
九秋风露越窑开
夺得千峰翠色来
好向中宵盛沆瀣

*Output:*
> 九秋风露越窑开
> 夺得千峰翠色来
> 好向中宵盛沆瀣

**Example 6: 表格重构 (R10)**
*Input:*
名称 朝代 特点
青花 元 钴料绘制
粉彩 清 玻璃白打底

*Output:*
| 名称 | 朝代 | 特点 |
|------|------|------|
| 青花 | 元 | 钴料绘制 |
| 粉彩 | 清 | 玻璃白打底 |

---

## 📤 输出协议

### 主输出

1. **优化后 Markdown**（含语义标注）
2. **QUALITY_REPORT.md**（格式见下）

### QUALITY_REPORT 格式

> **🔒 强制约束**：QUALITY_REPORT 必须且只能包裹在 ` ```yaml ` 和 ` ``` ` 代码块中。代码块外严禁出现任何解释性文字（如「以下是报告」「好的，这是您的质量报告」）。下游解析器（`yaml.safe_load()`）直接读取代码块内容，任何额外文字都会导致解析失败。

```yaml
# QUALITY_REPORT
task_id: "<book-to-epub task id>"
input: "<MinerU 输出路径>"
output: "<优化后 Markdown 路径>"
timestamp: "<ISO 8601>"

stats:
  image_split_fixes: <R4 修复数>
  caption_binds: <R5 图注绑定数>
  hard_break_merges: <R6 换行合并数>
  heading_normalizations: <R1 标题修正数>
  chemistry_replacements: <R8 化学式替换数>
  chapter_start_marks: <R9 篇章起始标注数>
  figure_type_marks: <R9 图片类型标注数>

pending:  # 【待确认】项，最多 5 条
  - type: "complex_chemistry|ambiguous_caption|missing_toc_entry|unclear_layout"
    location: "<行号或上下文>"
    detail: "<问题描述>"

typo_flags:  # R10 错词检查，仅报告
  - word: "阀值"
    suggestion: "阈值"
    count: 3

integrity:  # 完整性自检
  mineru_image_count: <MinerU 图片数>
  output_image_count: <输出图片数>
  mineru_char_count: <MinerU 字符数>
  output_char_count: <输出字符数>
  char_delta_pct: "<偏差百分比>"
```

### 长文本防截断

若达到输出 Token 极限，在段落完整处停止，末尾输出：

```text
[--- 未完待续，请回复"继续"输出下一部分 ---]
```

**绝不允许为压缩字数而擅自精简内容。**

#### Chunk 接缝协议（处理「继续」时强制执行）

当用户回复「继续」输出下一 Chunk 时：

1. **严禁重复**：不得重复上一 Chunk 末尾已输出的最后一句或最后半句。必须从上一 Chunk 截断处的下一个完整字符开始无缝续写。
2. **补全闭合标签**：若上一 Chunk 截断时有未闭合的 HTML 标签（如 `<figure>` / `<div class="chapter-start">` / `<div class="footnote">`），本 Chunk 开头**必须先输出闭合标签**（`</figure>` / `</div>`），再续写正文。
3. **接缝自检**：输出本 Chunk 前，确认：
   - 本 Chunk 首字符 ≠ 上一 Chunk 尾字符
   - 本 Chunk 开头无孤立闭合标签（`</figure>` 前应有内容）
   - 所有从上一 Chunk 延续的块级标签已在本 Chunk 内闭合

示例：
```
上一 Chunk 末尾: ...景德镇窑工在釉料中加入了
[--- 未完待续，请回复"继续"输出下一部分 ---]

本 Chunk 开头: 氧化钴，烧成后呈现出深邃的蓝色。
（无缝续写，无重复，无缺失）
```

---

## 🔗 与 book-to-epub 管线的接口

### 上游输入

- MinerU 输出的 `.md` 文件 + `images/` 目录
- PDF 页面截图（用于版式语义标注，`pdf2image` 导出）

### 下游交付

- 优化后的 `.md`（含语义标注）
- `QUALITY_REPORT.md`
- 交付给 Coordinator → Review-A（标注审核 12 项）

### 回退策略

Review-A FAIL → 回退 Process 修复（最多 3 轮）→ 3 轮仍 FAIL → 输出 `-degraded` 版本。

LLM 负责全部规则：R0-R10、脚注/诗词/代码块处理。未使用外部自动化脚本。

---

## 📋 交付前自检

- [ ] 未删除原文信息（MinerU 字符数 ±10%）
- [ ] 未改变核心观点与情绪
- [ ] 标题层级无跳级（H1→H2→H3 递进）
- [ ] 图片数 ≥ MinerU 图片数（一票否决）
- [ ] LaTeX 残留 = 0（`grep '\$'`）
- [ ] MinerU 遗留块 = 0（`grep '<details>'`）
- [ ] 逐字换行修复 = 0（搜索单行 1-2 汉字）
- [ ] 版式语义已标注（图文密集书）
- [ ] QUALITY_REPORT.md 存在，待确认项 ≤ 5
- [ ] 错词仅报告，未自动替换
