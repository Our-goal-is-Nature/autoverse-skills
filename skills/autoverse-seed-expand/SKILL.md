---
name: autoverse-seed-expand
description: 用户已经给出一篇具体论文的题名、简称、DOI、PMID、PMCID、arXiv 或 Semantic Scholar ID，或给出作者姓名、ORCID，希望理解该论文的参考文献、后续引用与相关工作，或查找该作者的其他著作时使用。用户只有较宽的研究方向、尚未给出具体论文或作者时不要使用。
metadata:
  version: 0.3.1
---

# Autoverse Seed Expand

帮助学生从一篇给定论文或一位给定作者出发，梳理该研究的参考文献、后续引用、相近工作或该作者的其他著作，并写出文稿与证据表。Agent 负责提出问题、拟定检索式、比较文献并撰写正文。Autoverse 负责检索、认篇与核验题录。Agent 不另编写检索程序。

## 做法

- 检索开始前，Agent 先运行 `autoverse --json --quiet whoami`。该命令能返回已登录账户或平台密钥时，Agent 方可继续。该命令返回 `NOT_AUTHENTICATED` 或显示未登录时，Agent 停止检索，告知用户执行 `autoverse login` 或设置 `AUTOVERSE_API_KEY`，待用户确认后再继续。Agent 不要代为打开登录流程。
- Agent 先确认用户要的是沿一篇给定论文扩展引文，或沿一位给定作者查找著作，而不是撰写文献综述，也不是整理开题前的研究认识。用户未说明的范围，Agent 按下列默认继续，并在对话中说明所用默认。Agent 不必为已给出的信息再问一轮。
- 默认如下。Agent 以近五年文献为主，题目的奠基研究仍纳入。Agent 只依据摘要作判断。Agent 交文稿（`.md`）与证据表（`.csv`），不交 PDF。
- 用户给出 DOI、PMID、PMCID、arXiv 编号或 Semantic Scholar ID 时，Agent 用 `resolve` 认篇。用户只给出题名、简称，或篇目身份尚不确定时，Agent 先用 `search` 检索，比较题名、作者和年份后再认篇。用户给出作者姓名时，Agent 用 `authors` 认人，比较返回的作者记录后再继续。用户给出 ORCID 时，Agent 仍用姓名调用 `authors`，并在对话中用该 ORCID 核对作者身份。Agent 不得臆造 `authors` 的其他旗标。用户先给出一篇论文、再要求查看该文作者的其他著作时，Agent 先认篇，从 `resolve` 或 `batch` 取得作者姓名，再用 `authors` 认人，然后检索该作者的其他著作。
- 出发对象为论文时，Agent 按用户关心的问题分别检索参考文献、后续引用或相近工作。出发对象为作者时，Agent 先确认作者身份，再检索该作者的著作，并对有价值的篇目继续检索参考文献、后续引用或相近工作。同名作者尚未分辨清楚时，Agent 先核对该作者的所属机构、合作者或代表作。Agent 不得把不同人的著作写成同一份名单。Agent 依检索结果修改检索式。Agent 不得以调用次数或检索排序代替对文献的判断。
- 除下列示例外的参数，或命令不能执行时，Agent 再读取 `autoverse-cli` 或命令说明。Agent 不臆测选项名称。
- Agent 发现文献、认篇与认人只走下列 Autoverse 命令。Agent 不得把网页检索或其他站点当作发现文献的入口。Agent 不得打开出版页补题录。
- Agent 纳入两篇及以上时，把标识写入 `ids.txt`，用 `batch` 一次认篇。Agent 不要对每篇单独 `resolve`。

常用调用：

```text
autoverse --json --quiet whoami
autoverse --json --quiet search "<title or topic>"
autoverse --json --quiet authors "<author name>"
autoverse --json --quiet resolve <prefixed-id>
autoverse --json --quiet batch -f ids.txt
autoverse --json --quiet related <seed-id> --via references
autoverse --json --quiet related <seed-id> --via cited-by
autoverse --json --quiet related <seed-id> --via similar
```

精选命令未返回被引次数或题录细节时，Agent 只可用下列路径，经 `api` 调用。与精选命令重复时，Agent 仍用精选命令。未列出的路径，Agent 不得调用。Agent 不得直接请求 HTTP。Agent 不得自行查阅 OpenAPI。

```text
autoverse --json --quiet api -X GET /v1/papers/search
autoverse --json --quiet api -X GET /v1/papers/resolve
autoverse --json --quiet api -X POST /v1/papers/batch
autoverse --json --quiet api -X GET /v1/semantic-scholar/native/graph/paper/{paper_id}
autoverse --json --quiet api -X GET /v1/usage
```

## 引证与依据

文稿中的论断与文献要点，须能回到 Autoverse 已核验的篇目。摘要只支持摘要所能支持的判断。写入文稿或证据表的标识符须经 `resolve` 或 `batch` 认篇。认不上的篇目，Agent 不得当作已引用文献。Agent 不得编造 PMID、DOI、题名、作者或研究结论。

题录中的短摘要仅供筛选。Agent 撰写前须阅读完整摘要及已返回字段。作者、年份、会议或期刊取自 `search`、`resolve` 或 `batch`。`search` 若只给出第一作者，Agent 用 `resolve` 或 `batch` 取全作者。被引次数、文献类型：精选命令已给出则采用，未给出再用上列 `api`。仍缺的栏留空。Agent 不写「未返回」。Agent 不打开网页补填。Agent 不按被引排序。

无合法开放获取全文时，判断止于摘要。Agent 不得绕过订阅或付费墙。

Autoverse 已返回的引用关系，Agent 可以写为两篇具体论文之间的参考文献关系或后续引用关系，并分别使用 `references` 与 `cited-by` 标明。Agent 根据摘要内容判断的相近工作、研究延续或同一作者的后续著作，须写明这是内容上的相关，不得写成已经核验的引用。依据不足或文献结论不一致时，Agent 在讨论中写明，不得抹平。检索暂时不可用时，Agent 在文献来源中说明覆盖范围，不得把未经检索的内容写为文献结论。

## 文稿体例

文稿按可单独阅读的学术叙述来写，不按作业说明来写。出发对象为论文时，标题用「研究脉络」。出发对象为作者时，标题用「著作述要」。节名用中文，不用 Intro、Background。

固定大纲：

1. **引言**：本文从哪一篇论文或哪一位作者出发、本文回答什么、下文按何主题组织。
2. **文献来源**：检索途径（Autoverse 文献检索）、时限、纳入篇数、判断依据摘要。不写命令名，不写认篇或认人过程。
3. **主题各节**：出发对象为论文时，按参考文献、后续引用或研究问题组织。出发对象为作者时，按该作者的研究线索组织。不要按单篇罗列。不要每节套「一致之处 / 分歧与限度」。
4. **讨论**：集中写研究间的一致、分歧与证据不足。
5. **结语**
6. **参考文献**

正文用顺序编码：论断后标 `[1]`，按首次出现连续编号，多篇写作 `[1, 4, 7]`。文末参考文献与编号一一对应。证据表第 *n* 行即 `[n]`，三处顺序必须一致。正文不写 `doi:…` 或 `arxiv:…` 串。

参考文献尽量写：作者，题名，会议或期刊，年份，DOI 或 URL。预印本无正式发表时写 arXiv 编号。作者缺则从作者栏起写，该栏留空。

文稿正文不得出现：交付、约定、用户要求、调研、证据表、标识符、未返回、已核对篇目、`resolve`、`batch`、`authors`、Autoverse 命令、拆分的研究问题。一致与分歧写入讨论，不作各节小标题。

英文术语按学术中文来写，不要按英文原词硬译。例如：参考文献，不用「上游」；后续引用，不用「下游」；预印本，不用「预打印」。

关系图仅在确能说明两篇论文之间的参考文献或后续引用时使用。内容密集时，Agent 将关系图拆成几张。

## 交稿

Agent 在对话中说明结论与依据的限度，并交下列两件。保存位置以用户指定为准。用户未指定时，Agent 将文件写在当前工作目录，并在对话中告知路径。Agent 不交 PDF。

- 文稿（`.md`）：按「文稿体例」。
- 证据表（`.csv`）：每行一篇，列顺序与参考文献编号相同；列题名、作者、年份、会议或期刊、DOI 或 URL、文献类型、被引次数、与本问题相关的要点。缺项留空。

成稿只写研究内容与依据的限度。
