# 检索能力讨论记录（2026-09-01）

对照：[25 条能力说明](../.cursor/projects/root-autoverse-skills/canvases/search-product-ideas.canvas.tsx) 的编号。  
参加人：产品（本对话）、对照 Linear 上 Xiyu Han（灵儿）已开工的导出。  
本次不包含：把下列结论写成新的 Linear Issue。

## 已对齐的结论

### 第 1 条：按文献角色过滤

学生指定只要试验、方法论文、数据集论文、综述或技术标准。CLI 按该角色过滤命中列表。

产品意见：可以做。该参数需要后端先暴露对应接口。优先级定为第二优先级。

### 第 2 条：把本次检索条件与命中列表写成文件

CLI 写入本次问句、过滤条件、命中篇数和每篇标识。Agent 保存该文件。

产品意见：可以纳入。必须先改 CLI。依赖条件：每一次检索都必须留下记录。没有检索记录，就没有可保存的文件。

### 第 3 条：判断一句论断能否被文献摘要支撑

产品意见：可以做。做成两个版本，都由 Skill 编排，不把「读摘要并下判断」做成后端黑盒。

1. 非语义版本。Agent 用现有 `search` 按关键词检索。Skill 读取命中篇目的摘要，判断该论断能否被摘要支撑。本版本只使用现有 `search` 命令，不增加新的 CLI 动词。
2. 语义版本。后端提供语义接口，计算论断与摘要（或篇目）的相似程度。Skill 调用新的 CLI 命令，或调用现有的 `related --via similar`。语义相似程度由接口计算；「这句话是否被这篇支撑」仍由 Agent 根据返回结果判断。



### 第 4 条与去重（两条不同的事）

第 4 条原文：CLI 把同一研究的预印本、正式发表文本和中英文题名归为一条工作。这是「同一研究的多个版本」，不是「多次 search 的结果合并去重」。

产品把第 4 条理解成去重，并讨论了多次检索之后的去重。产品认为：Agent 可以连续调用多次 `search`；CLI 实际保留下来的文本（产品所说的 TXT）必须始终是去重之后的列表。学生或 Agent 继续检索时，这份保留文本只追加尚未出现过的篇目。

设计尚未写进规格。待写清的内容：去重键用 DOI、还是题名加作者加年份、还是再加相似程度；这份保留文本属于一次对话、一次工作目录文件、还是 CLI 会话。

### 第 5 条：尚未覆盖的检索角度

「未检索角度」不是某一次 `search` 命令自己的生命周期。一次 `search` 只返回该问句的命中列表。

学生的一个研究问题通常需要 Agent 拆成多条问句，并多次调用 `search`。Skill 根据已经用过的问句和已经得到的命中，列出已经覆盖的角度和尚未覆盖的角度，并给出下一条问句。Agent 继续调用 `search` 填补尚未覆盖的角度。

产品意见：列出角度、填补角度由 Skill 完成。不增加 CLI 命令来管理这次研究的生命周期。

### 第 11 条：按开放获取链接过滤

产品意见：该条与下载全文有关。后续单独开下载板块时再写。本次不纳入检索命令。

预印本标识（第 12 条）产品尚未想好，本次不纳入。

### 导出 BibTeX / RIS / Markdown

产品意见：现在不新开「返回 bib 文件」的能力。

灵儿（Linear 上为 Xiyu Han）已经在做 [AUT-36](https://linear.app/autoversecn/issue/AUT-36/支持将检索-json-导出为-risbibtex-与-markdown)。该 Issue 状态为 In Review。实现方式：增加 `export` 动词；读取已有 `search` / `resolve` / `batch` 的 JSON；在本地组装 RIS、BibTeX 或 Markdown；不登录、不请求 `/v1`、不扣点。Pull request：[https://github.com/Our-goal-is-Nature/autoverse-cli/pull/3](https://github.com/Our-goal-is-Nature/autoverse-cli/pull/3) 。从 `.bib` 核验 DOI 是另一条 Issue：[AUT-24](https://linear.app/autoversecn/issue/AUT-24/支持从-bibtex-文件核验-doi)，状态为 Backlog。

### 第 16 条：两个年份区间对照（产品未听懂，此处写清）

Agent 使用同一条问句，指定两个年份闭区间，例如 2019–2021 与 2024–2026。CLI 分别检索，返回三份列表：前一区间的命中、后一区间的命中、只出现在后一区间的篇目。

学生看到的是两段时间内各有哪些篇目，以及后一段新出现了哪些篇目。Agent 不把该结果写成研究进展综述。

本次讨论未对该条表示纳入或不纳入。

### 第 18 条：删除与指定篇目过于相近的结果

产品意见：由 Skill 完成。Agent 根据学生否定的篇目，改写问句或从已有列表中去掉相近条目。不增加 CLI 参数 `--unlike`。

## 本次讨论未逐条表态的编号

6、7、8、9、10、13、14、15、17、19、20、21、22、23、24、25。

## 归纳：改 CLI、改 Skill、往后放

同时改 CLI，且依赖「每一次检索都留下记录」：第 2 条。多次 `search` 之后的去重，产品希望写进 CLI 保留下来的文本，设计未定。

第二优先级，且依赖后端接口：第 1 条。

只改 Skill，或 Skill 加现有命令：第 5 条；第 3 条的非语义版本；第 18 条。

Skill 加新命令或加现有 `similar`：第 3 条的语义版本。

不纳入本次、放到后续下载板块：第 11 条。预印本标识（第 12 条）未想好。导出 bib 不新开，跟 AUT-36。

第 16 条只完成了说明，未决定是否做。

## 2026-09-02：整体 SPC 讨论稿已锁定的选择

这份 SPC 是讨论稿。一份正文写三个方向；能做的段落以后再补验收，其余标后续版本。

1. 数据层「每天原数据更新」只作为运维指标，不写入面向 Agent 的 CLI 验收。
2. 「论文现有渠道覆盖是否向公众展示」本次不考虑。
3. 后端按文献类型、会议类型过滤，认 [AUT-12](https://linear.app/autoversecn/issue/AUT-12/完成检索网关-api-说明并确定部署位置) 已写的分面（OA、conference venue、期刊级别），后期随本地或混合检索网关对用户上线。
4. 检索记录只存在学生本机。一个含 `.autoverse/library.sqlite` 的目录是一个检索工作区。数据库只保存去重后的篇目，不保存每一次问句或命令。
5. 去重键：先 DOI；没有 DOI 再用 pmid、arxiv、pmcid。三者都没有则 `archive add` 拒绝写入，Agent 须先 `resolve` 或 `batch` 补标识。
6. `search` 成功不自动写库。Agent 必须再调用 `archive` 才写入。`archive` 用一条动词加子命令。初始化用 `archive init`，在当前目录创建 `.autoverse` 和空库。`archive` 全部 0 点，不请求 `/v1`。
7. `search`、`related`、`resolve`、`batch` 凡带题录的 JSON 都可以交给 `archive add`。学生或 Agent 可以按标识删除一篇。
8. `archive init` 不改 `.gitignore`。
9. 存档分析（支撑力度、未覆盖角度、跨年份对照）写进方向 3(d)，验收标后续版本。
10. 泛检索与入库检索共用同一条 `search`。差别只在事后是否调用 `archive`。
11. Skill 读取文件系统，判断是否存在 `.autoverse/library.sqlite`。CLI 不提供探测命令。不存在可唯一确定的工作区时，Agent 询问：新建子目录并在该子目录内 `archive init`，还是不持久化。Agent 不得在当前工作目录直接 `init`。已存在唯一工作区时，新对话不再询问是否继续，Agent 须提醒本次作用于哪一个检索工作区。学生要新增工作区时对 Agent 说明。未初始化时 `archive add` 必须失败。讨论稿不写安装 CLI 与安装 Skill 的关系。

讨论稿正文：[spc-search-workspace-archive.md](spc-search-workspace-archive.md)。

## 2026-09-02：第 5 节定稿

1. 第一版可见文件：`outline.md`、`queries.md`、`unused.md`、`export/`（含 `library.json` 与三种导出）。不要求 `tree.md`，不要求学生看见 `hits/`。
2. 交流 Skill 第一版不写 `.gitignore`。`archive init` 仍不改 `.gitignore`。
3. 维基百科只读目录和相近条目，用来生成研究角色与大纲节名。
4. STORM 的树对象、embedding 与 Qdrant 不进入 CLI。
5. 「一篇只挂一处」管的是 `outline.md`，不管库。库可以有很多篇。展开是入库后三选一（挂已有节 / 学生同意后加小节再挂 / 进 `unused.md`），不是往同一节底下无限追加。`similar` 只提供候选。



## 2026-09-02：讨论稿已写、实现规格仍须补的一句

`archive add` 遇到库中已有同一稳定标识符时，是保留旧行还是用新 JSON 覆盖字段。`archive list` 的 `--limit` 缺省与上限。直接子目录中存在两个检索工作区时，已规定 Agent 必须请学生指定。