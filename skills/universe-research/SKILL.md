---
name: universe-research
description: 用户要对计算机科学、医学或工科问题做文献研究、撰写综述并交出证据表时使用。用户已给出一篇具体论文或一位作者、并要沿引文或著作扩展时不要使用。
metadata:
  version: 0.3.1
---

# Universe Research

帮助学生就计算机科学、医学或工科问题完成文献检索并撰写综述。Agent 负责判断学科、拟定检索式、比较文献并撰写正文。Autoverse 负责检索与核验篇目。Agent 不另编写检索程序。

文献检索与核验的执行面是 `autoverse`。命令、参数、错误码以 [../autoverse-cli/references/commands.md](../autoverse-cli/references/commands.md) 为准。Agent 不臆测选项名称，不得直接请求 HTTP，也不得自行翻阅 OpenAPI 选择路径。

发现与认篇优先使用精选动词：

```text
autoverse --json --quiet search "<research question>" --domain <见对应 reference>
autoverse --json --quiet resolve <prefixed-id>
autoverse --json --quiet batch -f <本次任务标识文件>
```

精选动词缺少必要字段时，只可使用下列共用路径；医学还可使用医学 reference 明确列出的两个补充路径。未列出的 `/v1` 路径不得调用。

```text
autoverse --json --quiet api -X GET /v1/papers/search
autoverse --json --quiet api -X GET /v1/papers/resolve
autoverse --json --quiet api -X POST /v1/papers/batch
autoverse --json --quiet api -X GET /v1/semantic-scholar/native/graph/paper/{paper_id}
autoverse --json --quiet api -X GET /v1/usage
```

学科专有的检索角度、别名、`search --domain`、主题组织与学科用词，分别写在 [references/computer-science.md](references/computer-science.md)、[references/medicine.md](references/medicine.md) 与 [references/engineering.md](references/engineering.md)。学科 reference 只补充上述内容，不改写本文件的近五年、奠基、题名检索与核验规则。Agent 在检索开始前判定学科，并先读对应 reference。Agent 不得把某一学科的检索角度套到另一学科。医学补充路径只写在医学 reference 中。

行文与术语：撰写正文前阅读 [references/chinese-academic-prose.md](references/chinese-academic-prose.md) 与 [references/chinese-academic-terms.md](references/chinese-academic-terms.md)。引用键与编译见 [references/citations.md](references/citations.md)。

## 做法

- 检索开始前，Agent 须确认 Autoverse 已登录。未登录时，Agent 停止检索，告知用户登录后再继续。Agent 不要代为打开登录流程。
- Agent 先判定本题属于计算机科学、医学或工科。用户已说明学科时，Agent 不再追问。学科无法由题目判定时，Agent 只问一个简短问题。Agent 读完对应 reference 后再检索。
- 主题检索以近五年为主，题目的奠基研究仍纳入。摘要为空的篇目不得据以写结论。Agent 的交付物为：综述（`.md`）与证据表（`.csv`），不交 PDF。
- Agent 按该学科 reference 中的检索角度拆开总问题。各角度分别检索。宽检索式噪声大、或要把某一已知工作找回来时，改用完整题名检索，不加年份窗。Agent 先按 DOI 去重；没有 DOI 时，只有题名、主要作者和年份均一致才视为同一工作。该学科 reference 列出的别名均须纳入检索式。同一工作的预印本与正式发表文本并列时，Agent 只保留正式发表。
- Agent 用 Autoverse 多次检索。Agent 依结果修改检索式。Agent 不得以调用次数或检索排序代替对文献的判断。
- Agent 查找文献时，先用 Autoverse 检索。网页检索与出版方、会议、PubMed 或 arXiv 等官方页面，可用于补充检索，并核对该页上已经写出的题录。
- Agent 核验题录时，把拟写入综述或证据表的标识写入系统临时目录中的本次任务文件（文件名含任务短名或日期，不用固定名 `ids.txt`），用 `batch` 一次核验。Agent 不要对每篇单独核验。网页不能证明两篇论文之间的参考文献关系或后续引用关系。写入综述或证据表的 DOI、PMID、PMCID 或 arXiv 编号，须通过 `batch` 核验。核验不上的篇目，Agent 不得当作已引用文献。`batch` 成功但题名、作者或摘要与拟引工作不一致的条目，Agent 剔除。`batch` 成功包须保存为 JSON，供编译引用。
- Agent 纳入文献，直到已返回的文献足以比较各研究的结论，并写明一致、分歧或证据不足。Agent 不为凑篇数而纳入与本题无关的文献。检索或点数不足时，Agent 在文献来源中说明实际覆盖范围，不得把未经检索的内容写为文献结论。



## 引证与依据

综述中的论断与文献要点，须能回到已核验且摘要非空的篇目。摘要只支持摘要所能支持的判断。Agent 不得编造 DOI、PMID、arXiv 编号、题名或研究结论。

题录中的短摘要仅供筛选。Agent 撰写前须阅读完整摘要及已返回字段。作者、年份、会议或期刊取自 Autoverse 已返回的题录。检索结果若只给出第一作者，Agent 用 `batch` 取全作者。被引次数、文献类型：已返回则采用。仍缺的栏留空。Agent 不写「未返回」。Agent 不按被引排序。

摘要为空的篇目可以写入本次任务的标识文件并纳入一次 `batch`。`batch` 成功则可以进入证据表与参考文献；要点栏留空。主题各节与讨论不得根据该篇写该文做了什么、证明了什么、与谁一致或分歧。Agent 不得为补摘要再次对该篇调用 `resolve` 或 `batch`。

无合法开放获取全文时，判断止于摘要。Agent 不得绕过订阅或付费墙。

依据不足或文献结论不一致时，Agent 在讨论中写明，不得抹平。

医学综述不构成个体诊疗建议。Agent 只在对话中说明这一点。Agent 不把该说明写进综述标题或开篇。

## 综述体例

综述按可单独阅读的该学科学术综述来写，不按作业说明来写。标题用「综述」，不用「叙事综述」。需要与系统综述对举时，Agent 在文献来源中写「叙述性综述」。行文与各节职责见 [references/chinese-academic-prose.md](references/chinese-academic-prose.md)。专有名词首次出现见 [references/chinese-academic-terms.md](references/chinese-academic-terms.md)。

固定大纲，节名用中文，不用 Intro、Background：

1. **引言**：用户题目里的对象，以及本文比较的范围。不先定义整个学科。
2. **文献来源**：检索途径（Autoverse 文献检索；若使用了官方页面补充，一并写明来源）、时限、别名如何纳入、纳入篇数、判断依据摘要。不写命令名，不写核验题录过程。文献来源中的学科表述以对应 reference 为准。
3. **主题各节**：按对应 reference 中的主题组织。不要按单篇罗列。不要每节套「一致之处 / 分歧与限度」。
4. **讨论**：集中写研究间的一致、分歧与证据不足。
5. **结语**
6. **参考文献**（由脚本写入，Agent 不写这一节）

草稿正文用标准引用：论断后写 `[@DOI]`，多篇写作 `[@DOI1; @DOI2]`，格式见 [references/citations.md](references/citations.md)。Agent 不手写 `[1]`，不手写文末参考文献。写完后运行：

```text
python scripts/render_cites.py --json <batch成功包> --draft <综述草稿.md> --out <综述.md> --csv <证据表.csv>
```

脚本按首次出现连续编号。交稿综述、文末参考文献与证据表第 *n* 行必须是该脚本的输出，三处顺序一致。交稿正文不写 `doi:…` 或 `[@…]`。Agent 只在脚本写出的证据表上填写「要点」。

参考文献著录由脚本从 JSON 灌入：作者，题名，会议或期刊，年份，DOI 或 URL。预印本无正式发表且无 DOI 时写 arXiv 编号。作者缺则从作者栏起写，该栏留空。

综述正文不得出现：交付、约定、用户要求、调研、证据表、标识符、未返回、已核对篇目、`resolve`、`batch`、Autoverse 命令、拆分的研究问题。一致与分歧写入讨论，不作各节小标题。

学科禁用的硬译以对应 reference 为准。

## 交稿

Agent 交下列两件。保存位置以用户指定为准。用户未指定时，Agent 将文件写在当前工作目录，并在对话中告知路径。Agent 不交 PDF。

- 综述（`.md`）：`render_cites.py` 编好的文稿，按「综述体例」。
- 证据表（`.csv`）：同一脚本按同一编号写出；列题名、作者、年份、会议或期刊、DOI 或 URL、文献类型、被引次数、与本问题相关的要点。前七列不得手改。缺项留空。摘要为空的篇目要点栏留空。
