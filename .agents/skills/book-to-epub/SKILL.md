---
name: book-to-epub
description: >-
  将 PDF 书籍转换为高质量 EPUB 的自动化管线。
  MinerU OCR 解析 → Process（语义修复与标注）→ Review-A（Markdown 审核）→ EPUB 构建 → Review-B（EPUB 结构审核）。
  当用户说「转 EPUB」「PDF 转电子书」「这本书做成 epub」时触发。
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: [mineru, pandoc, ebook-convert, python3, unzip, zip]
    optional_bins: [pdftoppm]
---

# Book-to-EPUB 书籍转换管线 (Coordinator)

## 🏗️ 架构与数据流

```text
[PDF]
 ↓ (MinerU OCR + pdftoppm 可选)
[raw/<book_name>.md + raw/images/ + raw/pages/(可选)]
 ↓ (epub-process Skill: R0-R10 规则)
[<book_name>_processed.md + QUALITY_REPORT.md]
 ↓ (Review-A: Markdown 静态审核)
[Pandoc / Calibre 构建]
 ↓
[<book_name>.epub]
 ↓ (Review-B: EPUB 解压与源码审核)
[最终交付 / 降级交付]
```

- **自动流转**：逐阶段自检，失败时报告并触发回退。
- **回退机制**：Review FAIL → 回退 Process 修复（最多 3 轮）→ 仍 FAIL → 触发降级输出。
- 🛑 **唯一用户确认点**：Review-B 完成后展示审核报告，等待用户确认交付。

## 🚫 Coordinator 行为硬约束 (Agent 必须遵守)

**禁止静默降级与幻觉执行**：

| 违规行为 | 正确做法 |
|---------|---------|
| 脚本报错后静默跳过 | 捕获 stderr → 报告错误 → 修路径重试 → 仍失败则中止并询问用户 |
| 阶段未跑就声称完成 | 每阶段完成后**必须执行自检命令**，确认产物存在且大小合理再进入下一阶段 |
| 试图"视觉打开"EPUB | **严禁**使用"打开/查看"等视觉动词。必须使用 `unzip` 和 `grep` 检查 EPUB 内部 XHTML 源码 |
| 构建产物不验证 | 构建后**必须自检**：`ls -lh <epub>` + `unzip -l <epub>` 确认图片数与文件数 |

## ⚙️ 阶段执行规范

### 1. 解析与参考图导出阶段
- **MinerU 解析**：`mineru -p <input.pdf> -o raw/ -m auto -b hybrid-auto-engine`
- **PDF 页面参考图导出（可选）**：`mkdir -p raw/pages && pdftoppm -jpeg -r 150 <input.pdf> raw/pages/page`。
  - 若 `pdftoppm` 不可用或当前 LLM 不支持图像解析，跳过此步骤。R9 版式语义标注在无参考图时**仅基于文本结构推断**，无法确定时保守保留并记入 QUALITY_REPORT。
- **异常处理**：任一命令退出码非 0 → 重试 1 次；仍失败 → 中止。

### 2. Process 阶段 (调用 `epub-process` Skill)
- **输入**：MinerU 产出的 `.md` 文件及 `raw/pages/` 参考图（如有）。
- **动作**：严格执行 `epub-process` 的 R0-R10 管线规则，输出 `<book_name>_processed.md` 和 `QUALITY_REPORT.md`。
- **HTML 块空行强制约束**：确保所有 Block 级 HTML 标签（`<div>`, `<figure>`, `<table>`）的**上下必须至少有一个空行**。

### 3. Review-A (Markdown 静态审核)
在 EPUB 构建前，使用 `grep`, `awk` 等命令对 `.md` 源码进行自动化检查。FAIL 则回退 Process。

### 4. EPUB 构建阶段
- **首选工具 (Pandoc)**：
  ```bash
  # 必须 cd 到本 SKILL 所在目录以确保 CSS 相对路径正确
  SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
  cd "$SKILL_DIR" && pandoc <output>.md -o <book>.epub \
    --toc --toc-depth=2 --metadata language=zh-CN \
    --css="$SKILL_DIR/templates/book-style.css" \
    --css="$SKILL_DIR/templates/caption.css"
  ```
- **备选工具 (Calibre)**：若 Pandoc 不可用，使用 `ebook-convert`（需确保 HTML 块前后有空行）。

### 5. Review-B (EPUB 源码审核) 🛑
**Agent 严禁尝试"视觉阅读"，必须通过解压 EPUB 检查内部 XHTML/CSS 源码。**
- **准备工作**：`unzip <book>.epub -d epub_check/`
- **核心检查**：通过 `grep` 和 `find` 检查图片数、目录结构、CSS 注入、内容完整性等。

## ⚠️ 降级输出规范 (Degraded Output)
当 Review-A 或 Review-B 的**核心项**（图片完整性、内容完整度）回退 3 轮仍 FAIL 时触发：
1. **差异**：剥离所有复杂的版式语义标注（如 `<div class="chapter-start">`, `<figure class="figure-pair">`），仅保留基础 Markdown 语法（`#`, `![]()`）和基础 HTML 标签，确保 EPUB 能成功构建。
2. **命名**：输出文件追加 `-degraded` 后缀（如 `<book>-degraded.epub`）。
3. **待修复清单**：在 EPUB 同级目录生成 `DEGRADED_ISSUES.md`，格式如下：
   ```markdown
   # 降级输出问题清单
   - [ ] 图片丢失：MinerU 提取 50 张，最终 EPUB 仅包含 42 张（缺失：img_012.jpg, img_034.jpg...）
   - [ ] 内容截断：第 3 章末尾文本在 Process 阶段被意外截断。
   ```

## ⚠️ 异常与边界条件
- **短文档 (<10 页)**：跳过 Process 的跨页衔接（R4/R6 规则），直接 MinerU → 简单清洗 → 构建。
- **PDF 无目录**：Process 阶段 R2 从正文 H2/H3 自动生成 TOC。
- **无页面参考图**：Process 阶段 R9 版式语义标注降级为纯文本推断，`chapter-start` / `figure-single` 等标记可能偏少。
