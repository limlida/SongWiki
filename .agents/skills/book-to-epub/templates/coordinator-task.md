# Book-to-EPUB Coordinator 执行模板

## 架构
```
PDF → MinerU (+ pdftoppm 可选) → Process（R0-R10 规则）→ Review-A → EPUB 构建 → Review-B 🛑
       OCR / 参考图导出           epub-process         标注审核    构建打包     源码审核
```

## 🚫 硬约束
| 违规 | 正确行为 |
|------|---------|
| 脚本报错后静默跳过 | → 报告错误 + 原因 + 等待用户指令 |
| 阶段未跑就声称完成 | → 每阶段后必须执行自检命令 |
| 试图"视觉打开"EPUB | → **严禁**使用"打开/查看"等视觉动词，必须使用 `unzip` 和 `grep` 检查源码 |

---

## 阶段一：解析与参考图导出

```bash
# 1. MinerU 解析
/home/hello/.venv/mineru/bin/mineru -p <pdf> -o raw/ -m auto -b hybrid-auto-engine

# 2. 导出 PDF 页面参考图 (可选，供 R9 版式标注使用。若 pdftoppm 不可用则跳过)
mkdir -p raw/pages && pdftoppm -jpeg -r 150 <pdf> raw/pages/page
```

**自检：**
```bash
□ 输出 .md 存在且 > 10KB？   ls -lh raw/*/hybrid_auto/*.md
□ 图片目录有文件？            ls raw/*/hybrid_auto/images/ | wc -l
□ 页面参考图已生成（可选）？   ls raw/pages/ | wc -l
```

通过自检后自动进入阶段二。

---

## 阶段二：Process（含语义标注）

执行 `epub-process` skill（严格遵循 R0-R10 管线规则，详见 `../epub-process/SKILL.md`）。

**自检：**
```bash
□ 输出 Markdown 存在？     ls -lh <output>.md
□ QUALITY_REPORT.md 存在？ ls -lh QUALITY_REPORT.md
□ 图片数与 MinerU 一致？   diff <(grep -c '!\[.*\](' raw/*/hybrid_auto/*.md) <(grep -c '!\[.*\](' <output>.md)
□ 待确认项 ≤ 5？           grep -c '【待确认】' QUALITY_REPORT.md
```

通过自检后自动进入 Review-A。

---

## 阶段三：Review-A（标注审核）

在 Process 输出上直接检查 Markdown 源码质量。详细检查项见 `templates/reviewer-task.md`。

PASS → 进入阶段四。FAIL → 回退阶段二（最多 3 轮）。

---

## 阶段四：EPUB 构建

### 构建前强制检查（防 Calibre 吞噬 HTML 标签）

```bash
# 检查 Block 级 HTML 标签前后是否有空行（如果没有，Calibre 会解析错误）
awk '/<figure|<div/{if(prev!~/^$/) print NR": "$0" (缺少前置空行)"} {prev=$0}' <output>.md
```
*如果上述命令有输出，必须回退 Process 修复空行，否则禁止构建。*

### 执行构建 (首选 Pandoc)

```bash
# 必须 cd 到本 SKILL 所在目录以确保 CSS 相对路径正确
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SKILL_DIR" && pandoc <output>.md -o book.epub \
  --toc --toc-depth=2 --metadata language=zh-CN \
  --css="$SKILL_DIR/templates/book-style.css" \
  --css="$SKILL_DIR/templates/caption.css"
```
*(若 Pandoc 不可用，降级使用 `ebook-convert <output>.md book.epub --extra-css <SKILL_DIR>/templates/book-style.css --extra-css <SKILL_DIR>/templates/caption.css`)*

### 构建自检

```bash
□ EPUB 文件存在且 > 1MB？       ls -lh book.epub
□ 图片实际收入？                 unzip -l book.epub | grep -iE '\.(jpg|jpeg|png|gif|webp)' | wc -l
□ 结构完整？                     unzip -l book.epub | grep -E 'toc\.ncx|nav\.xhtml|content\.opf'
```

通过自检后自动进入 Review-B。

---

## 阶段五：Review-B（源码与渲染审核）🛑

**Agent 严禁尝试"视觉阅读"，必须通过解压 EPUB 检查内部 XHTML/CSS 源码。**
详细检查命令见 `templates/reviewer-task.md`。

🛑 唯一需用户确认的检查点：向用户展示 Review-B 报告，等待确认。若核心项 3 轮 FAIL，触发降级输出流程（见 SKILL.md）。
