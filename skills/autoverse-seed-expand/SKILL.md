---
name: autoverse-seed-expand
description: 用户已经给出一篇具体论文的题名、简称、DOI、PMID、PMCID、arXiv 或 Semantic Scholar ID，希望理解它的研究脉络、参考文献、后续引用或相关工作时使用。只有宽研究方向、没有具体种子时不要使用。
metadata:
  version: 0.1.0
---

# Autoverse Seed Expand

从一篇具体论文出发，帮助用户理解它从哪里来、后来影响了什么，以及哪些相关工作值得继续读。Agent 负责研究判断、联网核验、分析和表达；Autoverse 提供结构化论文身份与引文关系。

## 工作方式

- 先确认种子身份。稳定标识符适合 `resolve`；题名、简称或身份不确定时先 `search`，比较题名、作者和年份后再继续。
- 根据用户真正关心的问题探索上游参考、后续引用、相似论文或并行方法。可以调整查询、继续翻页、解析新发现的论文，也可以只深挖最有价值的一条线；不要为了凑齐固定结构机械调用所有方向。
- 使用 Agent 的原生网络搜索发现近期进展，并打开 DOI、出版社、会议、PubMed、arXiv 等官方页面核验关键论文。Autoverse 负责结构化发现与图谱，网络负责补充和核验，两者可以反复协作。
- 比较论文的研究问题、方法、数据、结论与局限，解释它们为什么相关，而不是把检索结果按排名堆成清单。

常用调用示例：

```text
autoverse --json --quiet resolve <prefixed-id>
autoverse --json --quiet search "<title or topic>"
autoverse --json --quiet related <seed-id> --via references
autoverse --json --quiet related <seed-id> --via cited-by
autoverse --json --quiet related <seed-id> --via similar
```

需要示例之外的参数或 CLI 排障时再读取 `autoverse-cli` 或命令帮助，不猜旗标。

## 证据与关系

明确区分两类关系：

- 已核验的引用关系可以画成连接两篇具体论文的实线，关系标签分别使用 `references` 或 `cited-by`，不拼接解释词；
- Agent 根据内容判断的方法相关、研究延续或应用分支使用虚线或分组，并明确这是分析关系，不冒充引用。

论文身份、标识符和关键结论应能回到实际读取的记录或官方页面。证据不足时保留不确定性，不为了让图完整而补造论文或关系。工具暂时不可用时可以继续利用其他可核验来源，但要如实说明证据范围，不能把模型记忆说成 Autoverse 图谱结果。

## 结果表达

按问题选择最有帮助的表达，不套固定模板。常见组合包括：

- 种子论文的一句话定位；
- 上游—种子—下游研究脉络；
- 核心论文比较表；
- 并行方法、时间线或建议阅读顺序；
- 关键分歧、证据空缺和适合继续追问的问题。

Mermaid 只在关系图确实能帮助理解时使用，内容密集时拆成几张小图。默认在对话中给出结果；用户要求简报、保存、导出或汇报材料时，再在指定位置生成相应文件，未指定格式时可使用 Markdown。正式交付写研究内容与证据边界，不展示命令和技术排障过程。
