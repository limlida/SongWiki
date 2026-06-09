# MEMORY.md — 跨会话持久记忆

> 新会话第一动作：读本文件 → 执行唤醒协议 → 再回答任何问题。

---

## 唤醒协议（每次新会话必须执行，不可跳过）

```text
1. 执行工具链检查：
   python3 .agents/skills/openclaw-knowledge-admin/scripts/bootstrap_toolchain.py --check

2. 读 wiki/index.md（获取全局地图，当前页数）

3. 读 wiki/log.md 最后 10 条（恢复工作记忆）

4. 检查 knowledge/tasks/ 是否有 running/pending 任务

5. 判断任务类型 → 需要时读 KNOWLEDGE.md / LARK.md / TOOLS.md

6. 开始执行
```

**铁律：完成以上 5 步之前，不得调用 web_search / exec / 浏览器 / MinerU / pdf-craft。**

---

## 知识库当前状态

- **总页数**：0 — 全量重置，重新编译中（2026-06-08）
- **排队来源**（5 本）：《陶瓷简史》《参天台五台山记》《参天台五台山记研究》《北宋河北边防建设研究》《日本藏三方北宋官印考》
- **当前任务**：`convert-2026-06-08-ceramic-history` — Step 2（vLLM 已启动，待执行转换）
- **活跃领域**：宋代全史（陶瓷/茶/社会生活/军事/宗教/交通/服饰等）

---

## 用户偏好

- 回答必须有出处标注（RULES.md §33）
- 新知识必须回写 wiki，不能只停留在聊天记录
- 飞书消息回复要简洁但不可省略依据和限制
- 先读 wiki 再做事，不要绕过知识库直接搜 web

---

## 常见错误（不要再犯）

1. ❌ 新会话跳过唤醒协议直接 web_search → ✅ 先读 index.md + log.md
2. ❌ 报告写完不写回 wiki → ✅ 建 synthesis 页 + 更新受影响的 entity/concept 页 + 追加 log.md
3. ❌ 回答不标注出处 → ✅ 每条事实断言标注 ✅wiki / 🌐web(URL) / ⚠️推测 / ❌删除
4. ❌ >10秒任务不先发回执 → ✅ 先写 tasks/ → 发回执 → 再执行
5. ❌ 工具找不到就重装 pip install / 重下载模型 → ✅ 先读 TOOLS.md 确认正确路径。所有工具链和模型已预装，不可用时报告 boss，不要自行安装
6. ❌ 页面不写 frontmatter 就提交 → ✅ 编译时填满 provenanceState / confidence / aliases / tags / contradictedBy
7. ❌ 直接覆写 wiki 页面 → ✅ 先写 .tmp → 校验 → rename 原子写入

---

## 待办

- [ ] 五本书全量重编译
