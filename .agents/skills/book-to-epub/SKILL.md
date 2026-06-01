---
name: book-to-epub
description: >-
  将 PDF 书籍转换为高质量 EPUB。MinerU OCR 解析 → Process（epub-process/reorder）
  补充语义标记 → epub3-boilerplate 模板构建 EPUB → Reviewer 检查最终产物。
  当用户说「转 EPUB」「PDF 转电子书」「这本书做成 epub」「convert pdf to epub」时触发。
  Requires: MinerU2.5-Pro + Python3 + zip.
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins:
        - mineru
        - ebook-convert
        - python3
        - zip
---

# Book-to-EPUB 书籍转换管线

## 架构

```
PDF → MinerU → Process → EPUB → Reviewer
       OCR解析   补充语义   构建打包   检查EPUB
                标记       CSS渲染    最终产物
```

- 🛑 检查点1：MinerU 完成后展示 TOC+统计，用户确认
- 🛑 检查点2：EPUB 构建后展示文件清单，用户确认
- 🛑 检查点3：Reviewer 完成后展示审核报告，用户确认
- ❌ FAIL → 回退 Process 修复（最多3轮）→ 仍FAIL → 降级输出

## 什么时候使用

- 用户提供一本 PDF 书籍，要求转换为高质量 EPUB
- 书籍含图片/表格/公式，需要结构化优化

## 异常处理与边界条件

### MinerU 解析失败
- 解析失败（退出码非 0 或输出为空）→ 重试 1 次；仍失败 → 中止并报告
- MinerU 不可用 → 提示用户改用 `references/pdf2epub-paddle/` (PaddleOCR 方案)
- 部分图片丢失 → 保留剩余图片，报告中列明丢失项

### PDF 无目录 (TOC)
- Process 阶段 B 段会自动从 MinerU 输出中识别目录区域并提取 TOC
- 如 B 段无法识别目录页，则从正文 H2/H3 生成 TOC 结构
- 提取后展示给用户确认

### 短文档 (<10 页)
- 简化流程：直接 MinerU 解析，跳过 epub-process 的图片切断修复和段落衔接（无跨页需求）
- 保留标题层级、目录提取、化学式处理和 Reviewer 审核

### Reviewer FAIL
- 回退 Process 修复（最多 3 轮）→ 3 轮仍 FAIL → 输出降级 EPUB（标记 `-degraded`）
- 在 EPUB 扉页后插入「待修复问题清单」页

### 图片全部丢失
- 立即中止管线
- 报告 MinerU 输出中 `![](images/...)` 计数为 0

## Coordinator 职责

Coordinator 负责流程调度、EPUB 构建和最终交付。严格按 [templates/coordinator-task.md](templates/coordinator-task.md) 执行各阶段，不得跳过。

### 🚫 行为硬约束

**禁止静默降级** — 以下行为视为管线失败，必须中止并报告用户：

| 违规行为 | 示例 | 正确做法 |
|---------|------|---------|
| 脚本报错后静默跳过 | Process 脚本 FileNotFoundError → 不吭声继续 | 报告错误 → 修路径重试 → 仍失败则询问用户 |
| 步骤耗时过长就找捷径 | MinerU 太慢 → 复用旧产物 | 告知预计耗时 → 询问是否等待或复用 |
| 阶段未跑就声称完成 | Process 没跑 → 直接构建 EPUB | 每阶段完成后**自检清单**，确认产物存在再进入下一阶段 |
| 构建产物不验证就交付 | EPUB 283KB 就发给用户 | 构建后**必须自检**：`ls -lh` + `unzip -l` 确认图片数、文件数 |

**逐阶段自检**（任一失败 → 中止 + 报告）：
```
□ 输出文件是否存在？ ls -lh <output>
□ 大小是否合理？ 对比上阶段，偏差应在 ±30% 内
□ 图片数完整？ grep -c '!\\[.*\\](' <output>
```

### EPUB 构建规范
- **禁止裸用 Calibre** — 产物应是手工构建的 epub3-boilerplate 结构，非 `index_split_000.html`
- **必须使用 `references/epub3-boilerplate/template/` 作为输出结构模板**：
  - 内容文件命名：`cover.xhtml` / `chapter001.xhtml` / `chapter002.xhtml` ...
  - 目录结构：生成 `nav.xhtml`（EPUB 3 TOC）+ 保留 `toc.ncx`（EPUB 2 兼容）
  - CSS 分区：`style/base.css` + `style/bodymatter.css`
  - 图片目录：`images/` 而非 Calibre 默认 hash 散落根目录
- 渲染命令示例：
  ```bash
  mkdir -p build/OEBPS/{text,images,styles}
  # 将 chapter*.xhtml 写入 build/OEBPS/text/
  cp references/epub3-boilerplate/template/Content/style/*.css build/OEBPS/styles/
  cp references/epub3-boilerplate/template/package.opf build/OEBPS/content.opf
  # 编辑 content.opf 的 metadata/manifest/spine
  cd build && zip -X0 ../book.epub mimetype && zip -Xr9 ../book.epub META-INF/ OEBPS/
  ```

## Process 职责

Process 阶段执行 `epub-process` skill（`reorder`），对 MinerU 输出做全文档结构整理和排版修复。详细规则见 [epub-process SKILL.md](../epub-process/SKILL.md)。

完成后输出：整理后的 Markdown + `QUALITY_REPORT.md`。

## Reviewer 职责

Reviewer 打开最终 .epub 文件，逐项检查实际渲染效果。所有标准从 Process 产出的 TOC 动态获取，不硬编码。

| # | 检查项 | 方法 | 通过标准 |
|----|--------|------|---------|
| 1 | 图片完整性 | `unzip -l` 统计 images/ 文件数 | >= MinerU images 目录文件数（一票否决） |
| 2 | 目录页 | 打开 EPUB 翻到目录页 | 目录页存在，条目与原书一致 |
| 3 | 标题层级 | 打开 EPUB 检查各章标题 | 篇名=H1、节名=H2，与 TOC 一致 |
| 4 | 标题顺序 | 逐章翻看 | 火土釉形彩窑艺顺序（或与原书 TOC 一致） |
| 5 | 章首无重复标题 | 打开火篇/土篇等第一页 | 无 TOC 预览条目残留 |
| 6 | LaTeX 残留 | `unzip -p` 全文搜索 `\$` | =0 |
| 7 | 图片标题样式 | 随机打开 3 处图片 | `<span class="caption">` 灰体小字居中生效 |
| 8 | 段首缩进 | 随机打开 3 页正文 | CSS `text-indent: 2em` 生效 |
| 9 | 图片占位符 | `unzip -p` 全文搜索 | 无 `<details><summary>natural_image` 残留 |
| 10 | 内容完整 | `unzip -p` 全文字符数 vs MinerU | 偏差 ≤ ±10% |
| 11 | 结构完整 | 检查 content.opf | manifest 包含所有 chapter + nav.xhtml + toc.ncx |
| 12 | 文件大小 | `ls -lh` | >1MB（含图片） |

输出 PASS / FAIL + 逐项结果。FAIL → 回退 Process（最多 3 轮）。

## 模板

- `templates/coordinator-task.md` — Coordinator 执行流程（每步命令 + 自检清单）
- `templates/reviewer-task.md` — Reviewer 12 项审核模板
- `templates/caption.css` — 图片标题 CSS

## 参考

- `references/quality-checklist.md` — 质检清单
- `references/epub3-boilerplate/template/` — EPUB 3.2 标准骨架，构建输出结构以此为准
- `references/pdf2epub-paddle/` — PaddleOCR 扫描版 PDF 方案（MinerU 不可用时降级备选）
