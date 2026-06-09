# 任务总账

> Append-only。新事件追加新行，不修改旧行。按时间正序。
> 最后更新：2026-06-08

## 图例

- 状态：`pending` = 排队 · `running:<步骤>` = 执行中 · `done` = 完成 · `failed:<步骤>:<原因>` = 失败已回退
- 类型：`convert` = PDF转换 · `ingest` = 知识收录 · `lint` = 认知审计 · `query` = 查询归档

## 状态机

```
pending ──→ running ──→ done
              ↓
           failed（任一步骤失败 → 原子回退）
              ↓
           pending（boss 指令重试）
```

**铁律：文件所在目录 = 任务真实状态。**

## 总账

| 时间 | task-id | 类型 | 来源 | 状态 | 详情 |
|------|---------|------|------|------|------|
| 17:18 | convert-2026-06-08-ceramic-history | convert | 陶瓷简史 | running:Step1 | 48MB PDF |
（新任务从下一行开始追加）
