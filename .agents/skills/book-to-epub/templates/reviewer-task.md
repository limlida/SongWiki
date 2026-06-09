# Book-to-EPUB 审核模板

---

## Review-A：标注审核（Process 后，EPUB 构建前）

直接检查 Process 输出的 Markdown 源码。

### 审核清单（12 项）

| # | 检查项 | Agent 执行方法 (命令行) | 通过标准 |
|----|--------|------|---------|
| 1 | 图片完整性 🔴 | `grep -c '!\[.*\]('` 对比两个文件 | Process >= MinerU |
| 2 | 标题层级与跳级 | `grep -E '^#{1,3} ' <output>.md \| awk '{print length($1)}' \| awk 'NR>1 && $1>prev+1 {print "跳级:"NR} {prev=$1}'` | 无输出 (无跳级) |
| 3 | 标题顺序 | `grep -E '^#{2,3} ' <output>.md` 提取列表 | 与 TOC 顺序一致 |
| 4 | 目录保留 | 对比 TOC 区域与正文 H2/H3 | 无丢失 |
| 5 | LaTeX 残留 | `grep '\$' <output>.md` | =0 |
| 6 | 图片切断修复 | `grep -B 2 -A 2 '!\[' <output>.md \| head -30` (抽检前3处) | 图片前后句子连贯 |
| 7 | 逐字换行修复 | `awk 'length($0) <= 2 && $0 ~ /[一-龥]/' <output>.md` | =0 (排除标题/列表) |
| 8 | MinerU 遗留块 | `grep '<details>' <output>.md` | =0 |
| 9 | 图注标注 | `grep '<span class="caption">' <output>.md` | 图片下方短文本已标注 |
| 10 | 篇章起始页 | `grep '<div class="chapter-start">' <output>.md` | 每章起始页已标注 |
| 11 | 图片类型 | `grep -E 'figure-single\|figure-pair\|figure-fullpage' <output>.md` | 密集书至少各 1 例 |
| 12 | 侧栏/页眉页脚 | 全文搜索重复装饰文本 | 已从正文流分离 |

---

## Review-B：源码与结构审核（EPUB 构建后）🛑

**前置准备：必须先解压 EPUB 到临时目录**

```bash
rm -rf epub_check && mkdir epub_check
unzip book.epub -d epub_check/
```

### 审核清单（12 项）

| # | 检查项 | Agent 执行方法 (命令行) | 通过标准 |
|----|--------|------|---------|
| 1 | 图片完整性 🔴 | `find epub_check/ -type d -name images -exec ls {} \; \| wc -l` (动态定位) | >= MinerU 图片数 |
| 2 | 目录结构 | `find epub_check/ -name toc.ncx -o -name nav.xhtml \| xargs cat` | 包含正确的 `<navPoint>` 或 `<li>` 节点 |
| 3 | 标题层级 | `find epub_check/ -name '*.xhtml' -exec grep -E '<h[1-3]' {} +` | 标签层级与 TOC 一致 |
| 4 | 标题顺序 | 同上，按文件名顺序检查 | 与原书 TOC 一致 |
| 5 | 章首无重复 | `find epub_check/ -name 'chapter*.xhtml' -exec head -20 {} \;` | 无重复的 `<h1>` 或 TOC 残留 |
| 6 | LaTeX 残留 | `grep -r '\$' epub_check/` | =0 |
| 7 | 图片标题样式 | `find epub_check/ -name '*.xhtml' -exec grep -A 2 'class="caption"' {} +` | 标签存在且未被 `<p>` 错误包裹 |
| 8 | 段首缩进 | `find epub_check/ -name '*.css' -exec grep 'text-indent' {} \;` | CSS 规则存在 |
| 9 | MinerU 遗留块 | `grep -r '<details>' epub_check/` | =0 |
| 10 | 内容完整 | `find epub_check/ -name '*.xhtml' -exec cat {} \; \| wc -c` 对比原 MD | 偏差 ≤ ±15% |
| 11 | 版式语义渲染 | `find epub_check/ -name '*.xhtml' -exec grep -E 'class="chapter-start"\|class="figure-' {} +` | 对应 class 保留在 XHTML 中 |
| 12 | 样式注入 | `find epub_check/ -name content.opf -exec grep -E 'book-style\|caption' {} \;` | CSS 文件已注册到 OPF 清单 |

### 输出格式 (Review-A 与 Review-B 通用)

```markdown
# [Review-A/B] 审核报告

## 结论: PASS / FAIL

## 逐项结果
| # | 检查项 | 结果 | 详情 (Agent 填入命令执行的真实输出摘要) |
|---|--------|:---:|------|
| 1 | 图片完整性 | ✅/❌ | MinerU=15, Process=15 |
| ... | ... | ... | ... |

## 问题列表 (若 FAIL)
- [ ] 项 X 失败：具体原因...
```

### 通过标准
- Review-A：图片 ❌ → 直接 FAIL；其他项 ❌ ≥ 3 → FAIL
- Review-B：图片 ❌ → 直接 FAIL；其他项 ❌ ≥ 3 → FAIL
- FAIL → 回退 Process（最多 3 轮）
- Review-B 🛑 唯一需用户确认的检查点
