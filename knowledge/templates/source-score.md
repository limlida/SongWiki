---
source_score:
  authority: 0       # 0-5 权威性
  traceability: 0    # 0-5 可追溯性
  originality: 0     # 0-5 原始性
  completeness: 0    # 0-5 完整性
  currency: 0        # 0-5 时效性
  domain_fit: 0      # 0-5 领域适配度
  total: 0           # 平均分
  level: rejected    # strong | usable | weak | rejected
  risk_flags: []     # ocr_noise | missing_context | secondary_only | ...
  rationale: ""
---

> 注：v2 简化评分仅需 一手/二手/待验证 + 一句话理由。
> 六维评分保留用于 Lint 审计和来源质量评估。
