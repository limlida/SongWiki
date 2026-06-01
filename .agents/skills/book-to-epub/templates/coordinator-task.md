# Book-to-EPUB Coordinator 执行模板

## 架构

```
PDF → MinerU → Process → Reviewer → EPUB
      OCR解析   epub-process  12项审核  epub3-boilerplate
                reorder                 手工打包
```

- 🛑 检查点1：MinerU 完成后展示 TOC+统计，用户确认
- 🛑 检查点2：Reviewer 完成后展示审核报告，用户确认
- 🛑 检查点3：EPUB 构建后展示文件清单，用户确认
- ❌ FAIL → 回退 Process（最多3轮）→ 仍FAIL → 降级输出

## 🚫 硬约束

| 违规 | 正确行为 |
|------|---------|
| 脚本报错后静默跳过 | → 报告错误 + 原因 + 等待用户指令 |
| 步骤耗时太长就找捷径 | → 告知预计耗时 + 询问用户是否等待 |
| 阶段未跑就声称完成 | → 每阶段后必须执行自检 |
| 构建产物不验证就交付 | → 自检：文件大小 + 图片数 + 结构完整性 |

**逐阶段自检**（任一失败 → 中止 + 报告）：
```
□ 输出文件是否存在？ ls -lh <output>
□ 大小是否合理？ 对比上阶段，偏差应在 ±30% 内
□ 图片数完整？ grep -c '!\[.*\](' <output>
```

---

## 阶段一：MinerU 解析

```bash
/home/hello/.venv/mineru/bin/mineru -p <pdf> -o raw/ -m auto -b hybrid-auto-engine
```

- 输入：PDF 文件
- 输出：`raw/<pdf_name>/hybrid_auto/<pdf_name>.md` + `images/`
- 失败处理：退出码非 0 或输出为空 → 重试 1 次 → 仍失败则中止

自检：
```
□ 输出 .md 存在且 > 10KB？   ls -lh raw/*/hybrid_auto/*.md
□ 图片目录有文件？            ls raw/*/hybrid_auto/images/ | wc -l
□ 字符数合理？                wc -c raw/*/hybrid_auto/*.md
```

🛑 检查点 1：展示 TOC（从输出提取 H2/H3）+ 图片数 + 字符数，用户确认。

---

## 阶段二：Process（epub-process / reorder）

执行 `epub-process` skill，详细规则见 `../epub-process/SKILL.md`。

流程：
1. 通读 MinerU 输出，识别结构和排版问题
2. 提取原书目录结构（B 段）
3. 内容修复与衔接（C 段：图片切断、图片标题、重复标注）
4. 排版优化（D 段：标题层级、列表、段落、逐字换行、公式、化学式去 LaTeX、段首缩进、结构化形态）

输出：
- 整理后的 Markdown
- `QUALITY_REPORT.md`（修复记录 + 待确认项 ≤ 3）

自检：
```
□ 输出 Markdown 存在？     ls -lh <output>.md
□ QUALITY_REPORT.md 存在？ ls -lh QUALITY_REPORT.md
□ 图片数与 MinerU 一致？   grep -c '!\[.*\](' 对比
□ 待确认项 ≤ 3？           grep -c '【待确认】' QUALITY_REPORT.md
```

---

## 阶段三：Reviewer 审核

执行 12 项审核，详细模板见 `templates/reviewer-task.md`：

1. 图片完整性（一票否决）
2. 标题层级（与 TOC 一致）
3. 标题顺序（与 TOC 一致）
4. 目录保留（无丢失）
5. LaTeX 残留
6. 图片切断修复
7. 逐字换行修复
8. NEEDS_CAPTION
9. 噪音标题
10. 缩进完整
11. 内容完整
12. 质量报告

PASS → 进入阶段四。FAIL → 回退阶段二（最多 3 轮）。

🛑 检查点 2：展示审核报告，用户确认。

---

## 阶段四：EPUB 构建

按 epub3-boilerplate 模板手工构建，禁止裸用 Calibre。

### 构建步骤

```bash
# 1. 创建目录结构
mkdir -p build/OEBPS/{text,images,styles}

# 2. 按 H2 分割 Markdown → XHTML 章节文件
# 命名规范：chapter001.xhtml, chapter002.xhtml ...

# 3. 复制 CSS
cp references/epub3-boilerplate/template/Content/style/*.css build/OEBPS/styles/
cp templates/caption.css build/OEBPS/styles/

# 4. 复制 MinerU 输出的所有图片到 build/OEBPS/images/

# 5. 生成 cover.xhtml + titlepage.xhtml + nav.xhtml（EPUB 3 目录）

# 6. 编写 content.opf（metadata + manifest + spine）
#    编写 toc.ncx（EPUB 2 兼容目录）

# 7. 编写 mimetype + META-INF/container.xml

# 8. 打包
cd build
zip -X0 ../book.epub mimetype
zip -Xr9 ../book.epub META-INF/ OEBPS/
```

### 构建自检

```
□ EPUB > 1MB（含图片）？       ls -lh book.epub
□ 图片收入？                   unzip -l book.epub | grep 'images/' | wc -l
□ nav.xhtml 存在？             unzip -l book.epub | grep nav.xhtml
□ toc.ncx 存在？               unzip -l book.epub | grep toc.ncx
□ content.opf 有正确的 metadata？
```

🛑 检查点 3：展示 EPUB 大小 + 文件清单 + 图片数，用户确认后交付。
