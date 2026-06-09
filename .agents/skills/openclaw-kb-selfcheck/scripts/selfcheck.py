#!/usr/bin/env python3
"""OpenClaw knowledge-base self-check (read-only).

Scans knowledge/ for the most common ways ingestion goes wrong:
structure gaps, experimental files leaking in, wiki/index/log out of sync
with reality, non-conforming task files, and ingest tasks stuck without
their six required artifacts. Reports only; never modifies files.

Usage:
    python selfcheck.py [--root PATH] [--json]

Exit code: 0 if no FAIL-level findings, 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# scripts -> openclaw-kb-selfcheck -> skills -> .agents -> <root>
DEFAULT_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_DIRS = [
    "knowledge/raw",
    "knowledge/converted",
    "knowledge/web-buffer",
    "knowledge/inbox",
    "knowledge/domains",
    "knowledge/wiki",
    "knowledge/wiki/sources",
    "knowledge/wiki/entities",
    "knowledge/wiki/concepts",
    "knowledge/wiki/syntheses",
    "knowledge/reports",
    "knowledge/tasks/pending",
    "knowledge/tasks/running",
    "knowledge/tasks/review",
    "knowledge/tasks/done",
    "knowledge/tasks/failed",
    "knowledge/templates",
]

REQUIRED_FILES = ["knowledge/wiki/index.md", "knowledge/wiki/log.md"]

# Tool-internal / intermediate artifacts that belong in experiments/, not knowledge/.
EXPERIMENT_GLOBS = [
    "*_middle.json",
    "*_model.json",
    "*_content_list.json",
    "*_content_list_v2.json",
]
SCRIPT_SUFFIXES = {".py", ".sh", ".ipynb"}

class Report:
    def __init__(self) -> None:
        self.findings: list[tuple[str, str, str]] = []  # (level, area, message)

    def add(self, level: str, area: str, message: str) -> None:
        self.findings.append((level, area, message))

    def fail(self, area: str, message: str) -> None:
        self.add("FAIL", area, message)

    def warn(self, area: str, message: str) -> None:
        self.add("WARN", area, message)

    def ok(self, area: str, message: str) -> None:
        self.add("OK", area, message)

    @property
    def has_fail(self) -> bool:
        return any(f[0] == "FAIL" for f in self.findings)


def rel(root: Path, p: Path) -> str:
    try:
        return p.relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def check_structure(root: Path, r: Report) -> None:
    for d in REQUIRED_DIRS:
        if not (root / d).is_dir():
            r.fail("structure", f"缺少目录 {d}/")
    for f in REQUIRED_FILES:
        if not (root / f).is_file():
            r.fail("structure", f"缺少文件 {f}")


def check_experiment_leak(root: Path, r: Report) -> None:
    scan_dirs = [root / "knowledge" / "inbox", root / "knowledge" / "converted"]
    leaked: list[str] = []
    for base in scan_dirs:
        if not base.exists():
            continue
        for pat in EXPERIMENT_GLOBS:
            leaked += [rel(root, p) for p in base.rglob(pat)]
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in SCRIPT_SUFFIXES:
                leaked.append(rel(root, p))
    for path in sorted(set(leaked)):
        r.warn("experiment-leak", f"试验/中间产物应移到 experiments/：{path}")


def list_wiki_md(root: Path, sub: str) -> list[Path]:
    d = root / "knowledge" / "wiki" / sub
    return [p for p in d.glob("*.md")] if d.exists() else []


def section_block(text: str, section: str) -> str:
    pat = re.compile(
        rf"^##\s*{re.escape(section)}.*?(?=^##\s+|\Z)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    m = pat.search(text)
    return m.group(0) if m else ""


def check_overview_exists(root: Path, r: Report) -> None:
    overview = root / "knowledge" / "wiki" / "overview.md"
    if not overview.is_file():
        r.warn("structure", "缺少 knowledge/wiki/overview.md（建议创建占位大纲）")


def check_index_sync(root: Path, r: Report) -> None:
    index = root / "knowledge" / "wiki" / "index.md"
    if not index.is_file():
        return
    text = index.read_text(encoding="utf-8", errors="replace")
    sources = list_wiki_md(root, "sources")
    entities = list_wiki_md(root, "entities")
    concepts = list_wiki_md(root, "concepts")
    syntheses = list_wiki_md(root, "syntheses")

    checks = [
        ("sources", sources),
        ("entities", entities),
        ("concepts", concepts),
        ("syntheses", syntheses),
    ]
    for section, files in checks:
        if not files:
            continue
        block = section_block(text, section)
        if not block:
            r.fail("index-sync", f"index.md 缺少 {section} 分区标题")
            continue

        if re.search(r"[—-]\s*0\s*页", block, flags=re.IGNORECASE):
            r.fail("index-sync", f"index.md 的 {section} 区仍写 0 页，但实际有 {len(files)} 个页面")
            continue
        if "待收录" in block:
            r.warn("index-sync", f"index.md 的 {section} 区仍写「待收录」，建议更新为实际页面列表")

        m = re.search(r"[—-]\s*(\d+)\s*页", block)
        if m:
            declared = int(m.group(1))
            actual = len(files)
            if declared != actual:
                r.warn("index-sync", f"index.md 的 {section} 区页数声明={declared}，实际={actual}")


def check_log_sync(root: Path, r: Report) -> None:
    log = root / "knowledge" / "wiki" / "log.md"
    if not log.is_file():
        return
    text = log.read_text(encoding="utf-8", errors="replace")
    tasks = list((root / "knowledge" / "tasks").rglob("*")) if (root / "knowledge" / "tasks").exists() else []
    task_files = [p for p in tasks if p.is_file()]
    if "暂无正式知识库操作记录" in text and task_files:
        r.fail("log-sync", f"log.md 写「暂无记录」，但 tasks/ 已有 {len(task_files)} 个任务文件")


def check_task_format(root: Path, r: Report) -> None:
    tasks_root = root / "knowledge" / "tasks"
    if not tasks_root.exists():
        return
    for p in tasks_root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() == ".json":
            r.warn("task-format", f"任务用 JSON 不符合模板（应为 checklist 风格 .md）：{rel(root, p)}")
            continue
        if p.suffix.lower() != ".md":
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "task-id" not in text:
            r.warn("task-format", f"任务缺少 task-id 元信息：{rel(root, p)}")
        if "- [ ]" not in text and "- [x]" not in text and "- [X]" not in text:
            r.warn("task-format", f"任务缺少 checklist 复选框：{rel(root, p)}")
        if p.name != "index.md":
            m = re.search(r"task-id[：:]\s*([a-z]+-\d{4}-\d{2}-\d{2}-[a-z0-9-]+)", text, re.IGNORECASE)
            if m is None:
                r.warn("task-format", f"任务 task-id 格式异常（建议 <type>-YYYY-MM-DD-<slug>）：{rel(root, p)}")


def check_stuck_ingests(root: Path, r: Report) -> None:
    running = root / "knowledge" / "tasks" / "running"
    if not running.exists():
        return
    sources_exist = bool(list_wiki_md(root, "sources"))
    for p in running.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"task-id[：:]\s*([a-z]+-\d{4}-\d{2}-\d{2}-[a-z0-9-]+)", text, re.IGNORECASE)
        tid = m.group(1) if m else p.stem
        if not tid.startswith("ingest-"):
            continue
        # Six-item completion proxy: a running ingest with no source summary anywhere.
        if not sources_exist:
            r.warn(
                "stuck-ingest",
                f"running 任务 {tid} 仍在进行，但 sources/ 为空（收录链未走完，符合预期则忽略）",
            )


def infer_running_step(task_text: str) -> str | None:
    matches = list(re.finditer(r"^##\s*Step\s*(\d+)\s*:", task_text, flags=re.MULTILINE))
    if not matches:
        return None
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(task_text)
        block = task_text[start:end]
        if "- [ ]" in block:
            return f"Step{m.group(1)}"
    return f"Step{matches[-1].group(1)}"


def parse_task_index_statuses(index_text: str) -> dict[str, str]:
    status_by_task: dict[str, str] = {}
    for line in index_text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5:
            continue
        task_id = cells[1]
        status = cells[4]
        if task_id and task_id != "task-id" and status and status != "状态":
            status_by_task[task_id] = status
    return status_by_task


def check_task_index_sync(root: Path, r: Report) -> None:
    tasks_root = root / "knowledge" / "tasks"
    index_file = tasks_root / "index.md"
    if not index_file.is_file():
        r.warn("task-index-sync", "缺少 knowledge/tasks/index.md")
        return

    index_text = index_file.read_text(encoding="utf-8", errors="replace")
    status_by_task = parse_task_index_statuses(index_text)

    for state_dir in ("pending", "running", "review", "done", "failed"):
        d = tasks_root / state_dir
        if not d.exists():
            continue
        for p in d.glob("*.md"):
            if p.name == "index.md":
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            m = re.search(r"task-id[：:]\s*([a-z]+-\d{4}-\d{2}-\d{2}-[a-z0-9-]+)", text, re.IGNORECASE)
            task_id = m.group(1) if m else p.stem

            indexed = status_by_task.get(task_id)
            if indexed is None:
                r.warn("task-index-sync", f"tasks/index.md 缺少任务记录：{task_id}")
                continue

            if state_dir == "running":
                if not indexed.startswith("running:"):
                    r.warn("task-index-sync", f"{task_id} 位于 running/，但总账状态为 {indexed}")
                    continue
                expected = infer_running_step(text)
                if expected is not None and indexed != f"running:{expected}":
                    r.warn("task-index-sync", f"{task_id} 当前应为 running:{expected}，但总账记录为 {indexed}")
            elif state_dir == "pending" and indexed != "pending":
                r.warn("task-index-sync", f"{task_id} 位于 pending/，但总账状态为 {indexed}")
            elif state_dir == "done" and indexed != "done":
                r.warn("task-index-sync", f"{task_id} 位于 done/，但总账状态为 {indexed}")
            elif state_dir == "review" and not indexed.startswith("review"):
                r.warn("task-index-sync", f"{task_id} 位于 review/，但总账状态为 {indexed}")
            elif state_dir == "failed" and not indexed.startswith("failed"):
                r.warn("task-index-sync", f"{task_id} 位于 failed/，但总账状态为 {indexed}")


def run(root: Path) -> Report:
    r = Report()
    check_structure(root, r)
    check_overview_exists(root, r)
    check_experiment_leak(root, r)
    check_index_sync(root, r)
    check_log_sync(root, r)
    check_task_format(root, r)
    check_stuck_ingests(root, r)
    check_task_index_sync(root, r)
    if not r.findings:
        r.ok("all", "未发现问题")
    return r


def print_text(root: Path, r: Report) -> None:
    order = {"FAIL": 0, "WARN": 1, "OK": 2}
    icon = {"FAIL": "[FAIL]", "WARN": "[WARN]", "OK": "[ OK ]"}
    counts = {"FAIL": 0, "WARN": 0, "OK": 0}
    print(f"知识库自检：{root}")
    print("-" * 60)
    for level, area, msg in sorted(r.findings, key=lambda f: (order[f[0]], f[1])):
        counts[level] += 1
        print(f"{icon[level]} {area}: {msg}")
    print("-" * 60)
    print(f"FAIL={counts['FAIL']}  WARN={counts['WARN']}  OK={counts['OK']}")
    if counts["FAIL"]:
        print("结论：未通过，需修复 FAIL 项。")
    elif counts["WARN"]:
        print("结论：通过但有待整理（WARN）。")
    else:
        print("结论：通过。")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="OpenClaw knowledge-base self-check (read-only)")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="workspace root (auto-detected)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args(argv)

    root = args.root.resolve()
    r = run(root)

    if args.json:
        print(json.dumps(
            {"root": str(root), "findings": [
                {"level": lv, "area": a, "message": m} for lv, a, m in r.findings
            ]},
            ensure_ascii=False, indent=2,
        ))
    else:
        print_text(root, r)

    return 1 if r.has_fail else 0


if __name__ == "__main__":
    sys.exit(main())
