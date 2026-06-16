# 任务总账

> Append-only。新事件追加新行，不修改旧行。按时间正序。
> 最后更新：2026-06-09

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
| 17:18 | convert-2026-06-08-ceramic-history | convert | 陶瓷简史 | done | ✅ 转换+Ingest完成(111页) |
| 10:50 | convert-2026-06-09-cantiantai | convert | 参天台五台山记 | done | 287页, 5.8k行, 乱码率<5%, 待boss确认 |
| 11:38 | verify-2026-06-09-klin-chapter | verify | 陶瓷简史 | done | 窑篇行号验证, 10页修24处 |
| 11:44 | ingest-2026-06-09-ceramic-history-klin-art | ingest | 陶瓷简史 | done | 窑篇后半+艺篇+东学西渐 |
| 11:46 | ingest-2026-06-09-ceramic-klin-art | ingest | 陶瓷简史 | done | 同上(重复) |
| 16:00 | convert-2026-06-09-beisong-defense | convert | 北宋河北边防建设研究 | done | ✅ 887行/162KB, 乱码率0%, 待boss确认 |
| 16:05 | citation-backfill-2026-06-09-ceramic-history | verify | 陶瓷简史 | done | ✅ 行号回溯, 109/109页完成 |
（新任务从下一行开始追加）
| 09:44 | convert-2026-06-12-yingzaofashi-gaodu | convert | 从《营造法式》解析宋代建筑高度 | running:Step1 |
| 10:01 | convert-2026-06-12-yingzaofashi-gaodu | convert | 从《营造法式》解析宋代建筑高度 | done | 质量5/5通过 |
| 10:01 | ingest-2026-06-12-yingzaofashi-gaodu | ingest | 从《营造法式》解析宋代建筑高度 | done | 16页（1s+10e+4c+1sy） |
| 10:33 | query-2026-06-12-song-commoner-house | query | 宋代普通百姓房屋设计 | done | 事后补建 🔴 |
| 10:50 | lint-2026-06-12 | lint | 全库207页 | review | 健康分29/100, 7 error + 43 warning |
