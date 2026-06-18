#!/usr/bin/env python3
"""
indexgen.py — Auto-generate wiki/index.md from page frontmatter.

仿 llm-wiki-compiler 的 indexgen.ts。
扫描四类 wiki 页面的 YAML frontmatter，按 type 分组生成字母序符号表。
每次 Ingest/Lint 后运行，保持 index.md 与磁盘页面同步。

Usage:
  python tools/indexgen.py                    # 写入 knowledge/wiki/index.md
  python tools/indexgen.py --dry-run          # 仅打印到 stdout
  python tools/indexgen.py --root <path>      # 指定项目根目录
"""

import os
import sys
import yaml
from datetime import datetime, timezone
from collections import defaultdict

WIKI_DIR = "knowledge/wiki"
PAGE_DIRS = ["sources", "entities", "concepts", "syntheses"]
INDEX_FILE = "knowledge/wiki/index.md"

# 中文类型标签
TYPE_LABELS = {
    "source": "sources（来源摘要）",
    "entity": "entities（客观实体）",
    "concept": "concepts（抽象概念）",
    "synthesis": "syntheses（综合论述）",
}


def find_root():
    """回退到含 knowledge/wiki/ 的目录。"""
    cwd = os.getcwd()
    for _ in range(5):
        if os.path.isdir(os.path.join(cwd, WIKI_DIR)):
            return cwd
        cwd = os.path.dirname(cwd)
    return os.getcwd()


def parse_frontmatter(filepath):
    """读取 .md 文件，返回 (frontmatter_dict, body) 或 (None, None)。"""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except (OSError, UnicodeDecodeError):
        return None, None

    if not content.startswith("---"):
        return None, None

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None, None

    if not isinstance(fm, dict):
        return None, None

    return fm, parts[2]


PAGE_DIR_TO_TYPE = {
    "sources": "source",
    "entities": "entity",
    "concepts": "concept",
    "syntheses": "synthesis",
}


def collect_pages(root):
    """扫描四类目录，返回 {type: [page_dict, ...]}。"""
    pages = defaultdict(list)
    base = os.path.join(root, WIKI_DIR)

    for page_dir in PAGE_DIRS:
        dirpath = os.path.join(base, page_dir)
        if not os.path.isdir(dirpath):
            continue

        for fname in sorted(os.listdir(dirpath)):
            if not fname.endswith(".md"):
                continue

            filepath = os.path.join(dirpath, fname)
            fm, body = parse_frontmatter(filepath)

            if fm is None:
                continue

            # 过滤 orphaned
            if fm.get("orphaned"):
                continue

            slug = fname[:-3]  # 去掉 .md
            title = fm.get("title", slug)
            if not isinstance(title, str) or not title.strip():
                title = slug

            pages[page_dir].append({
                "slug": slug,
                "title": str(title).strip(),
                "type": fm.get("type", PAGE_DIR_TO_TYPE.get(page_dir, page_dir)),
                "tags": fm.get("tags") if isinstance(fm.get("tags"), list) else [],
                "summary": fm.get("summary", ""),
                "status": fm.get("status", ""),
                "domain": fm.get("domain", ""),
            })

    return pages


def build_index(pages):
    """从页面数据生成 index.md 内容。"""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 统计总数
    total = sum(len(v) for v in pages.values())
    counts = {d: len(pages.get(d, [])) for d in PAGE_DIRS}

    lines = [
        "# Wiki 全局符号表",
        "",
        f"> 自动生成 | 最后更新：{now}",
        f"> 总页数：{total}（sources {counts['sources']} + entities {counts['entities']} + concepts {counts['concepts']} + syntheses {counts['syntheses']}）",
        f"> 生成脚本：tools/indexgen.py（零 LLM 参与）",
        "",
        "---",
        "",
    ]

    # 按 type 顺序输出
    for page_dir in PAGE_DIRS:
        entries = pages.get(page_dir, [])
        label = TYPE_LABELS.get(page_dir.rstrip("s"), page_dir)
        lines.append(f"## {label} — {len(entries)} 页")
        lines.append("")

        if not entries:
            lines.append("_暂无页面_")
            lines.append("")
            continue

        # 字母序
        entries.sort(key=lambda p: p["title"])

        # 按 tag 首维度分组（与 MOC.md 的维度一致）
        groups = group_by_first_tag(entries)
        for group_name, group_entries in groups:
            if group_name:
                lines.append(f"### {group_name}")
            lines.append("| slug | 标题 | tags |")
            lines.append("|------|------|------|")
            for p in group_entries:
                tags_str = ", ".join(p["tags"][:5]) if p["tags"] else "-"
                lines.append(f"| {p['slug']} | {p['title']} | {tags_str} |")
            lines.append("")

        lines.append("")

    lines.append("---")
    lines.append(f"_自动生成于 {now} | `python tools/indexgen.py`_")
    lines.append("")

    return "\n".join(lines)


def group_by_first_tag(entries):
    """
    按首 tag 的首维度值分组。
    tag 格式：`维度/值`（如 `窑口/定窑`、`时代/宋代`）。
    无 tag 的归入 "未分类"。
    """
    groups = defaultdict(list)
    group_order = []

    for p in entries:
        if p["tags"]:
            first = p["tags"][0]
            if "/" in first:
                _, val = first.split("/", 1)
                group_name = val
            else:
                group_name = first
        else:
            group_name = "未分类"

        if group_name not in group_order:
            group_order.append(group_name)
        groups[group_name].append(p)

    # "未分类" 排最后
    if "未分类" in group_order:
        group_order.remove("未分类")
        group_order.append("未分类")

    return [(g, groups[g]) for g in group_order]


def main():
    dry_run = "--dry-run" in sys.argv
    root = None

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--root" and i < len(sys.argv) - 1:
            root = sys.argv[i + 1]
        elif arg == "--help" or arg == "-h":
            print(__doc__)
            return

    if root is None:
        root = find_root()

    wiki_base = os.path.join(root, WIKI_DIR)
    if not os.path.isdir(wiki_base):
        print(f"ERROR: wiki 目录不存在: {wiki_base}", file=sys.stderr)
        sys.exit(1)

    pages = collect_pages(root)
    total = sum(len(v) for v in pages.values())

    if total == 0:
        print("WARNING: 未找到任何有效 wiki 页面", file=sys.stderr)

    index_content = build_index(pages)

    if dry_run:
        print(index_content)
        print(f"\n# DRY RUN — 未写入文件")
        return

    outpath = os.path.join(root, INDEX_FILE)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(index_content)

    print(f"index.md written: {outpath} ({total} pages)")


if __name__ == "__main__":
    main()
