# 操作日志
## [2026-06-10] ingest — 新见日本藏三方北宋官印考 Ingest 完成
- 1 source · 3 entities · 1 concept = 5 页
- entities: 雄勇上第一副指挥使朱记, 武卫第五十指挥第三都朱记, 广勇右第二军第七指挥使朱记
- concepts: 北宋禁军编制
- 武卫军募自河北诸州→与边防+定窑地理重叠
- 全库: 185 页（+6）
## [2026-06-10] ingest — 北宋河北边防建设研究 Ingest 完成
- 1 source · 9 entities · 5 concepts · 1 synthesis = 16 页
- entities: 北宋河北边防建设研究-全书结构, 塘泊防线, 何承矩, 澶渊之盟, 河北四路安抚使司, 料敌塔, 军事防御林, 地下长城, 杨延昭
- concepts: 北宋三线防御体系, 以步制骑, 河北乡兵, 守内虚外, 河北边防法规
- syntheses: 河北边防与定窑（跨陶瓷+军事 weaving）
- 回溯更新: entities/定窑.md（补充边防关联）
- 全库: 179 页（+17）
## [2026-06-09] lint-fix — 37条断链全部修复，健康分 0→100
- 5 别名修正 · 11 概念新建 · 10 实体新建
- 全库 162 页（+22）
## [2026-06-09] lint — 全库140页，健康分 0/100（37 broken-wikilink），其他规则全绿
- #1 frontmatter: 0 · #2 broken: 37 · #4 malform: 0 · #5 dup: 0 
- #6 empty: 0 · #7 summary: 0 · #8 orphan: 0 · #9 low-conf: 0
- #10 contradicted: 0 · #11 x-links: 0 · #13 candidates: 3
- 37 断链均为Ingest预留未建页或别名未设


## [2026-06-09] ingest | 参天台五台山记 — Batch 6 完成（+4页/全书30页封卷）
- entities/五台山.md、善慧大师.md
- concepts/陈咏剃度.md、印经院购经.md
- 六批30页：sources×1, entities×18, concepts×11
- 待建 30+ 实体/概念留待补课式 Ingest
- 全书六批29页：sources×1, entities×20, concepts×8
- 待建 30+ 实体/概念留待补课式 Ingest
- entities/大相国寺.md、传法院.md、开宝寺感慈塔.md
- concepts/宋神宗召见.md、佛牙.md
- entities/金山寺.md、僧伽大师.md
- concepts/汴河漕运.md、僧官制度.md
- sources/参天台五台山记.md ✅
- entities/成寻.md ✅
- entities/参天台五台山记-全书结构.md ✅
- index.md 已更新
- 全8卷约468节日记，分多批执行
- Batch 2 计划：第一（L5-L728）渡海入宋 → 明越杭

## [2026-06-09] citation-backfill | 陶瓷简史 — 行号回溯完成 ✅
- 全部 109 页知识页（50 entities + 59 concepts）已标注行号
- 总计约 500+ 条 citation，覆盖火/土/釉/形/彩/窑/艺七篇
- 零遗漏：grep -rL 验证通过
- sources/陶瓷简史.md converted_path 已更新为精确 .md 路径

## [2026-06-09] convert | 北宋河北边防建设研究 ✅
- 子代理完成：887行/162KB, 乱码率0%
- 待 boss 确认进 Ingest

## [2026-06-09] archive | 4 个 running 任务归档
- convert-2026-06-08-ceramic-history / ingest-*×2 / verify-* → done
- convert-2026-06-09-cantiantai 保留 running（待 boss 确认）

## [2026-06-08] 全量重置
- wiki/ tasks/ converted/ web-buffer/ 全部清空
- 五本书排队重新编译

## [2026-06-09] ingest | 陶瓷简史 — 全七篇完成，111 页

### 火篇（25 页: E8/C17）
entities: 仙人洞遗址, 陶维纳斯, 裴李岗文化, 仰韶文化, 半坡文化, 马家窑文化, 龙山文化, 大维德瓶
concepts: 平地堆烧法, 横穴窑, 竖穴窑, 龙窑, 馒头窑, 氧化焰与还原焰, 陶与瓷的界限, 妬器, 原始青瓷, 彩陶, 彩绘陶, 黑陶, 渗碳工艺, 匣钵, 覆烧, 叠烧, 支钉烧

### 土篇（17 页: E6/C11）
entities: 殷弘绪, 蒋祈, 7501瓷, 高岭土, 瓷石, 高岭村
concepts: 慢轮, 快轮与拉坯, 泥条盘筑法, 捏塑法, 利坯, 印坯, 注浆成形, 一元配方与二元配方, 莫来石, 玻璃相, 水碓

### 釉篇（18 页: E6/C12）
entities: 唐英, 何朝宗, 德化窑, 景德镇窑, 婺州窑, 陆羽
concepts: 釉, 石灰釉与石灰碱釉, 唐三彩, 化妆土, 青瓷, 白瓷, 青白瓷, 颜色釉, 结晶釉, 长石釉, 酱色釉, 黑釉

### 形篇（6 页: E2/C4）
entities: 鸡缸杯, 永乐压手杯
concepts: 托盏与盖碗, 煎茶法点茶法泡茶法, 梅瓶, 玉壶春瓶

### 彩篇（10 页: E3/C7）
entities: 长沙窑, 磁州窑, 鬼谷子下山大罐
concepts: 青花瓷, 分水技法, 苏麻离青, 釉下彩与釉上彩, 克拉克瓷, 红绿彩, 釉里红

### 窑篇—前半（15 页: E10/C5）
entities: 越窑, 邢窑, 秘色瓷, 汝窑, 官窑, 钧窑, 哥窑, 定窑, 龙泉窑, 建阳窑, 吉州窑
concepts: 五大名窑, 开片, 油滴与兔毫

### 窑篇—后半 + 紫玉金砂（9 页: E7/C2）
entities: 浮梁瓷局, 童宾, 珠山八友, 杜重远, 宜兴窑, 顾景舟, 陈曼生, 供春
concepts: 官搭民烧, 全手壶与半手壶

### 东学西渐（6 页: E3/C3）
entities: 李参平, 切恩豪斯, 伯特格尔
concepts: 乐烧, 骨瓷

### 艺篇（3 页: E2/C1）
entities: 各种釉彩大瓶, 郎世宁
concepts: 珐琅彩
跨章回溯: 唐英页大幅扩充

### 结构页（2 页）
sources/陶瓷简史, entities/陶瓷简史-全书结构

## [2026-06-09] 窑篇行号验证
- 10 页验证，修 24 处。根因: 图片行/空行导致 grep -n 偏移。
- 强制两步验证规则写入 KNOWLEDGE.md

## [2026-06-09] Schema 变更
- AGENTS.md: 第二大脑工作模型加非执行手册声明
- RULES.md: 知识库规则从 14 精简为 1
- KNOWLEDGE.md: 行号标注规则 + 三大操作任务模板引用 + 3条 🔴
- MEMORY.md: 常见错误 #8
- 新建模板: convert-task/ingest-task/query-task/lint-task

## [2026-06-09] convert | 参天台五台山记_白话译文
- 子代理完成：5,797 行/763KB，质量合格
- 待 boss 确认进 Ingest

## [2026-06-12] ingest — 从《营造法式》解析宋代建筑高度 Ingest 完成 ✅
- 1 source · 10 entities · 4 concepts · 1 synthesis = 16 页
- source: 营造法式建筑高度考
- entities: 营造法式, 李诫, 版门, 乌头门, 垒墙, 露墙, 抽紝墙, 露篱, 檐柱, 金柱
- concepts: 材分制, 宋代建筑三分法, 宋代台基制度, 宋代墙体高厚比
- syntheses: 宋代建筑高度游戏化应用（面向UnrealEngine的参数化规则）
- 首个建筑类来源，与已有宋代边防内容可交叉引用（版门/墙高→料敌塔/城池）
- 全库: 204 页（+16）
## [2026-06-12] query — 宋代普通百姓房屋游戏设计参数 ✅（事后补建）
- 11页 wiki 编织成可直接导入UE的参数卡
- 🔴 事故：违反RULES §27，exec Query前未建任务文件

## [2026-06-12] lint — 全库207页健康检查 | 29/100
- #2 broken-wikilink: 7条（5页），5个别名映射缺失
- #11 cross-links: 3页 wikilink不足阈值
- #12 excess-inferred: 5页无citation叙述段超2段
- #8 orphaned: 18页零backlink
- #9 low-confidence: 17页<0.5（建筑新页+单源，符合规则）
- 全绿规则：#1/#3/#4/#5/#6/#7/#10

## [2026-06-12] schema — Query / index / MOC 口径修复
- KNOWLEDGE.md：补 MOC.md 到目录树；统一 index.md/MOC.md 为 Ingest/Lint 后脚本刷新；Query 默认入口改为 retrieve.py，index.md 作为 fallback。
- AGENTS.md / CLAUDE.md / query-task.md：同步 Query 默认检索流程，明确 slug/title 唯一命中可直接读页面。
- 五大名窑：修正裸 tag `窑口` → `制度/窑口分类`；待脚本环境恢复后重生成 index.md / MOC.md。
- overview.md：更新为当前 206 页全景，补入参天台、河北边防、宋代建筑三块新域。
## [2026-06-15] lint — 全库217页健康检查 | 61/100
- 健康分 61（上次 12 日 29，+32）。无 error 项。
- #1 missing-frontmatter: 0 · #2 broken-wikilink: 0 · #5 dup: 0 · #6 empty: 0
- #8 orphaned: 19页 · #9 low-conf: 17页 · #11 cross-links: 3页
- #10 contradicted: 0 · #7 missing-summary: 0
- 自动合并: 石梁 → 石桥（5日龄重复页，0 backlink，内容已全覆）
- 全库: 217 → 216 页（-1 合并）

## [2026-06-12] ingest — 井陉窑报导 Ingest 完成
- 1 source · 4 entities · 5 concepts = 10 页
- source: 井陉窑报导（王思达，河北日报 2023）
- entities: 井陉窑, 孟繁峰, 天威军官瓶, 戳印点彩戳模
- concepts: 戳印点彩, 沥粉, 沥粉填嵌, 河北四大名窑, 滴点花斑
- 回溯更新: 定窑/邢窑/磁州窑（补井陉窑+河北四大名窑关联）
- 天威军官瓶与北宋边防重叠 → 后续可 weaving
- 全库: 206 → 216 页（+10）

## [2026-06-16] lint — 周审计，全库215页，健康分65/100
- 断链 1 条：鸡缸杯 [[斗彩]]→[[五彩与斗彩]] ✅ 自动修复
- #9 low-confidence: 17（营造法式体系 10 + 河北边防体系 2 + 其他）
- #11 schema-cross-links: 3（宋代建筑高度游戏化应用 0/3, 河北边防与定窑 0/3, 北宋禁军编制 1/2）
- #12 excess-inferred: 11（source 页 + 新 concept 页）
- 0 orphan · 0 duplicate · 0 contradicted
- 暗概念：壕寨制度(6)、南青北白(6)、延久四年(10) 建议关注
- 覆盖薄弱：唐代陶瓷 / 明清官窑 / 日本关联 / 考古遗址 / syntheses 仅2页
- 待办：大量页面缺少 created 字段，影响 age 判定
- 报告：knowledge/reports/lint-2026-06-16.json
