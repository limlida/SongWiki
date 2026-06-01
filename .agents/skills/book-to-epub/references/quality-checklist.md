# 质检清单

epub-process 和 Reviewer 各自有检查机制，本清单作为补充参考。

## epub-process 自检

见 `epub-process/SKILL.md` → Pre-Delivery Checklist：
- 未删除原文信息
- 未改变核心观点与情绪
- 标题层级/列表/段落统一
- 重复内容已标注
- 不确定修复已用【待确认】

## Reviewer 12 项

见 `templates/reviewer-task.md`。

## 常见问题速查

| 问题 | 症状 | 定位 |
|------|------|------|
| 图片丢失 | EPUB 大小异常小（<1MB），`unzip -l` 无 images/ | Coordinator 构建阶段 |
| 标题混乱 | 目录条目数与正文 H2 数量不一致 | epub-process B 段 |
| 化学式残留 | 搜索到 `$\mathrm{` | epub-process D 段 |
| 图片断句 | 图片前后有 2-3 字孤立碎片 | epub-process C 段 |
| 缩进缺失 | 随机一段正文无全角空格开头 | epub-process D 段 |
