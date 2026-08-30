---
name: universe-research
description: 用户要对计算机科学、医学或工科问题做文献研究、撰写综述并交出证据表时使用。用户已给出一篇具体论文或一位作者、并要沿引文或著作扩展时不要使用。
metadata:
  version: 0.1.0
---

# Universe Research

帮助学生就计算机科学、医学或工科问题完成文献检索并撰写综述。Agent 负责判断学科、提出研究问题、拟定检索式、比较文献并撰写正文。Autoverse 负责检索与核验篇目。Agent 不另编写检索程序。

学科专有的检索角度、别名、`search --domain`、补充 `api` 路径、主题组织与用词，分别写在 [references/computer-science.md](references/computer-science.md)、[references/medicine.md](references/medicine.md) 与 [references/engineering.md](references/engineering.md)。Agent 在检索开始前判定学科，并先读对应 reference。Agent 不得把某一学科的检索角度套到另一学科。

## 做法

- 检索开始前，Agent 先运行 `autoverse --json --quiet whoami`。该命令能返回已登录账户或平台密钥时，Agent 方可继续。该命令返回 `NOT_AUTHENTICATED` 或显示未登录时，Agent 停止检索，告知用户执行 `autoverse login` 或设置 `AUTOVERSE_API_KEY`，待用户确认后再继续。Agent 不要代为打开登录流程。
- Agent 先判定本题属于计算机科学、医学或工科。用户已说明学科时，Agent 不再追问。学科无法由题目判定时，Agent 只问一个简短问题。Agent 读完对应 reference 后再检索。
- Agent 先确认用户要的是文献研究，而不是沿一篇已有论文或一位作者扩展引文。用户未说明的范围，Agent 按下列默认继续，并在对话中说明所用默认。Agent 不必为已给出的信息再问一轮。
- 默认如下。Agent 以近五年文献为主，题目的奠基研究仍纳入。Agent 约纳入 25–40 篇，分若干检索式完成。Agent 只依据摘要作判断。Agent 交综述（`.md`）与证据表（`.csv`），不交 PDF。
- Agent 按该学科 reference 中的检索角度拆开总问题。各角度分别检索。Agent 先按 DOI、再按题名去重。该学科 reference 列出的别名均须纳入检索式。同一工作的预印本与正式发表文本并列时，Agent 只保留正式发表。
- Agent 用 Autoverse 多次检索并核验篇目。Agent 依结果修改检索式。Agent 不得以调用次数或检索排序代替对文献的判断。
- 除本文件与对应 reference 已列出的参数外，或命令不能执行时，Agent 再读取 `autoverse-cli` 或命令说明。Agent 不膮测选项名称。
- Agent 发现文献与核验题录只走本文件与对应 reference 列出的 Autoverse 命令。Agent 不得把网页检索、会议主页或其他站点当作发现文献的入口。Agent 不得打开出版页补题录。
- Agent 纳入两篇及以上时，把标识写入 `ids.txt`，用 `batch` 一次核验题录。Agent 不要对每篇单独 `resolve`。

常用调用：

```text
autoverse --json --quiet whoami
autoverse --json --quiet search "<research question>" --domain <见对应 reference>
autoverse --json --quiet search "<research question>" --domain <见对应 reference> --type review
autoverse --json --quiet resolve <prefixed-id>
autoverse --json --quiet batch -f ids.txt
```

精选命令未返回被引次数或题录细节时，Agent 只可用本文件与对应 reference 列出的路径，经 `api` 调用。与精选命令重复时，Agent 仍用精选命令。未列出的路径，Agent 不得调用。Agent 不得直接请求 HTTP。Agent 不得自行查阅 OpenAPI。

各学科共用的路径如下。医学补充路径只写在医学 reference 中。

```text
autoverse --json --quiet api -X GET /v1/papers/search
autoverse --json --quiet api -X GET /v1/papers/resolve
autoverse --json --quiet api -X POST /v1/papers/batch
autoverse --json --quiet api -X GET /v1/semantic-scholar/native/graph/paper/{paper_id}
autoverse --json --quiet api -X GET /v1/usage
```

## 引证与依据

综述中的论断与文献要点，须能回到 Autoverse 已核验的篇目。摘要只支持摘要所能支持的判断。写入综述或证据表的标识符须经 `resolve` 或 `batch` 核验题录。核验不上的篇目，Agent 不得当作已引用文献。Agent 不得编造 DOI、PMID、arXiv 编号、题名或研究结论。

题录中的短摘要仅供筛选。Agent 撰写前须阅读完整摘要及已返回字段。作者、年份、会议或期刊取自 `search`、`resolve` 或 `batch`。`search` 若只给出第一作者，Agent 用 `resolve` 或 `batch` 取全作者。被引次数、文献类型：精选命令已给出则采用，未给出再用上列 `api` 或该学科 reference 列出的补充路径。仍缺的栏留空。Agent 不写「未返回」。Agent 不打开网页补填。Agent 不按被引排序。

无合法开放获取全文时，判断止于摘要。Agent 不得绕过订阅或付费墙。

依据不足或文献结论不一致时，Agent 在讨论中写明，不得抹平。检索暂时不可用时，Agent 在文献来源中说明覆盖范围，不得把未经检索的内容写为文献结论。

医学综述不构成个体诊疗建议。Agent 只在对话中说明这一点。Agent 不把该说明写进综述标题或开篇。

## 综述体例

综述按可单独阅读的该学科学术综述来写，不按作业说明来写。标题用「综述」，不用「叙事综述」。需要与系统综述对举时，Agent 在文献来源中写「叙述性综述」。

固定大纲，节名用中文，不用 Intro、Background：

1. **引言**：为何需要综述、本文回答什么、下文按何主题组织。
2. **文献来源**：检索途径（Autoverse 文献检索）、时限、别名如何纳入、纳入篇数、判断依据摘要。不写命令名，不写核验题录过程。文献来源中的学科表述以对应 reference 为准。
3. **主题各节**：按对应 reference 中的主题组织。不要按单篇罗列。不要每节套「一致之处 / 分歧与限度」。
4. **讨论**：集中写研究间的一致、分歧与证据不足。
5. **结语**
6. **参考文献**

正文用顺序编码：论断后标 `[1]`，按首次出现连续编号，多篇写作 `[1, 4, 7]`。文末参考文献与编号一一对应。证据表第 *n* 行即 `[n]`，三处顺序必须一致。正文不写 `doi:…` 或 `arxiv:…` 串。

参考文献尽量写：作者，题名，会议或期刊，年份，DOI 或 URL。预印本无正式发表时写 arXiv 编号。作者缺则从作者栏起写，该栏留空。学科专有的著录要求以对应 reference 为准。

综述正文不得出现：交付、约定、用户要求、调研、证据表、标识符、未返回、已核对篇目、`resolve`、`batch`、Autoverse 命令、拆分的研究问题。一致与分歧写入讨论，不作各节小标题。

英文术语按学术中文来写，不要按英文原词硬译。各学科禁用的硬译以对应 reference 为准。

## 交稿

Agent 交下列两件。保存位置以用户指定为准。用户未指定时，Agent 将文件写在当前工作目录，并在对话中告知路径。Agent 不交 PDF。

- 综述（`.md`）：按「综述体例」。
- 证据表（`.csv`）：每行一篇，列顺序与参考文献编号相同；列题名、作者、年份、会议或期刊、DOI 或 URL、文献类型、被引次数、与本问题相关的要点。缺项留空。

成稿只写研究内容与依据的限度。
