# 讨论稿：检索工作区与本地篇目库

本文是讨论稿，不是已立项的实现规格。一份正文写三个方向。方向三中可以写清命令合同的部分，后续再补实现验收。方向一、方向二和方向三的存档分析标为后续版本。

本文不创建 Linear Issue。

对照：

- 现网 CLI 精选动词：`search`、`resolve`、`batch`、`related`；导出见 [AUT-36](https://linear.app/autoversecn/issue/AUT-36/支持将检索-json-导出为-risbibtex-与-markdown)
- 本地或混合检索分面见 [AUT-12](https://linear.app/autoversecn/issue/AUT-12/完成检索网关-api-说明并确定部署位置)
- 先前讨论记录：[discussion-search-capabilities-2026-09-01.md](discussion-search-capabilities-2026-09-01.md)

**描述**

学生或通用 Agent 在本机一个项目目录里做文献检索。学生可以选择只使用现网 `search` 取得题录 JSON，不在磁盘上保存篇目。学生也可以建立一个检索工作区：Agent 在当前工作目录下新建一个子目录，在该子目录内执行 `archive init`，之后把已核验的题录写入该子目录下的 SQLite 数据库。同一工作区内多次入库按稳定标识符去重，数据库只保存去重后的篇目。Agent 不撰写综述正文。

应用场景：学生在 Cursor 或同类 Agent 中提出科研检索。Agent 根据文件系统判断当前是否已有检索工作区，向学生说明本次命令作用于哪一个工作区，并在学生同意持久化后调用 `archive`。

---



## 1. 方向一：数据层



### 1.1 原数据按日更新

湖数据与索引的按日更新属于运维指标。该指标不写入面向 Agent 的 CLI 验收标准。本文不规定负责人、滞后时限，以及学生是否能读取「索引更新日期」。

### 1.2 渠道覆盖

本文不讨论上游渠道覆盖，也不规定学生或 Agent 是否能按渠道过滤命中列表。

**本次不包含（方向一）**

按日更新的值班规则；渠道清单；在 CLI 或站点上展示渠道名称。

---



## 2. 方向二：后端过滤

后端按文献类型、会议类型或同等分面过滤命中列表。本文认 [AUT-12](https://linear.app/autoversecn/issue/AUT-12/完成检索网关-api-说明并确定部署位置) 已经写明的分面：开放获取（OA）、会议 venue、期刊级别。这些分面在本地检索或混合检索对用户主链路开放之后上线。

现网 `search` 已有参数 `--type`，取值为 `journal_article`、`review`、`meta_analysis`、`clinical_trial`、`case_report`。AUT-12 分面与 `--type` 是否并存、是否替换，本文不定。期刊级别不是期刊分区。CLI 现网约定不提供期刊分区。开放获取分面与后续下载能力的验收边界，本文不定。

**验收标准（方向二）**

- [ ] 无。本方向在讨论稿中只引用 AUT-12，不增加 CLI 参数，不增加 `/v1` 路径。

**本次不包含（方向二）**

在用户主链路启用 Catalog 或混合检索；为 `search` 增加 venue 或期刊级别参数；把期刊级别写成分区；知网或 Web of Science。

---



## 3. 方向三：检索工作区与本地篇目库



### 3.1 名词


| 术语    | 含义                                                                                               |
| ----- | ------------------------------------------------------------------------------------------------ |
| 工作目录  | Agent 执行 CLI 时的当前工作目录（process working directory）。                                                |
| 检索工作区 | 一个文件系统目录。该目录下存在名为 `.autoverse` 的子目录，并且 `.autoverse` 内存在 SQLite 数据库文件。                            |
| 泛检索   | 调用 `search`（或 `related`、`resolve`、`batch`）并取得 JSON，不调用 `archive add`。                            |
| 入库    | 调用 `archive add`，把题录写入当前检索工作区的 SQLite 数据库。                                                       |
| 稳定标识符 | 带前缀的 DOI、PMID、arXiv 编号或 PMCID，例如 `doi:10.x/y`、`pmid:123`、`arxiv:1706.03762`、`pmcid:PMC10328000`。 |


一个检索工作区对应磁盘上的一个目录。检索记录只保存在该目录的本机文件中。Autoverse 账户与远程服务不保存该库。

### 3.2 目录与数据库文件

CLI 只把下列路径认作已初始化的检索工作区：当前工作目录下存在目录 `.autoverse/`，且其中存在文件 `library.sqlite`。

`.autoverse/library.sqlite` 是 SQLite 数据库。第一版只保存去重后的篇目。数据库不保存每一次检索的问句、命令行、时间戳或当次命中条数。

`archive init` 在当前工作目录创建 `.autoverse/` 和空的 `library.sqlite`。`archive init` 不创建、不修改 `.gitignore`。

当前工作目录不存在 `.autoverse/library.sqlite` 时，`archive add`、`archive list`、`archive remove` 必须失败。CLI 不得在此时自动执行 `archive init`。

### 3.3 Agent 如何判断已有检索工作区

Skill 读取文件系统。CLI 不提供用于探测 `.autoverse` 是否存在的命令。

Agent 按下列顺序检查：

1. 当前工作目录下是否存在 `.autoverse/library.sqlite`。
2. 若第 1 步不存在：当前工作目录的直接子目录中，有多少个目录各自包含 `.autoverse/library.sqlite`。

第 1 步成立时，本次命令默认作用于当前工作目录所表示的检索工作区。Agent 必须用该目录的路径告诉学生：本次检索与入库作用于哪一个检索工作区。Agent 不得再次询问「是否继续使用已有工作区」。Agent 必须告诉学生：若要新增一个检索工作区，学生直接对 Agent 说明即可。

第 1 步不成立、第 2 步恰好得到一个子目录时，Agent 把该子目录当作已有检索工作区，用该子目录的路径提醒学生，并在后续 `archive` 调用中把工作目录设为该子目录。

第 1 步不成立、第 2 步得到两个或更多子目录时，Agent 必须请学生指定本次作用于哪一个检索工作区。Agent 不得自行选择。

第 1 步与第 2 步都不成立时，Agent 必须询问学生：是新建一个子目录并在该子目录内执行 `archive init`，还是不持久化、只做泛检索。学生选择不持久化时，Agent 只调用 `search`（或同等精选动词），不调用 `archive init`，不调用 `archive add`。学生选择持久化时，见 3.4。

同一工作目录在新的一条 Agent 对话中再次使用，并且第 1 步或第 2 步已经能确定唯一检索工作区时，Agent 不询问是否继续。Agent 仍须提醒本次作用于哪一个检索工作区。

### 3.4 新建检索工作区

学生要求持久化、且当前不存在可唯一确定的检索工作区时，或者学生要求新增一个检索工作区时，Agent 必须先在当前工作目录下新建一个子目录，再在该子目录内执行 `archive init`。Agent 不得在当前工作目录直接执行 `archive init`。

子目录名称由学生指定。学生未指定时，Agent 询问名称，不得自行命名后创建。

创建完成后，Agent 把后续 `archive` 命令的工作目录设为该子目录。`search` 与 `archive` 仍是两条命令：`search` 的工作目录不要求等于检索工作区；`archive add` 的工作目录必须等于该检索工作区，否则命令失败。

### 3.5 泛检索与入库使用同一条 `search`

泛检索与入库检索都调用现网 `search`。两条路径的差别只在于：Agent 是否在 `search` 成功之后调用 `archive add`。

`search` 成功不写入 `library.sqlite`。`related`、`resolve`、`batch` 成功也不写入。Agent 必须再调用 `archive add` 才入库。学生已经确认使用某一检索工作区之后，每一次需要入库的 `search` 仍须再调用 `archive add`。

### 3.6 `archive` 动词

命令名：`archive`  
点数：0。该动词只读写本机文件，不请求 `/v1`，不校验会话，不产生 `INVALID_SESSION`、`INVALID_API_KEY`、`INSUFFICIENT_CREDITS`。

全局旗标仍放在动词前。Agent 固定使用 `--json --quiet`。

```text
autoverse --json --quiet archive init
autoverse --json --quiet archive add -f <json文件>
autoverse --json --quiet archive add --file -
autoverse --json --quiet archive list [--limit N]
autoverse --json --quiet archive remove <稳定标识符>
```

`init`、`add`、`list`、`remove` 是同一条动词的子命令，不拆成四条顶层动词。

`--json` 成功时，stdout 只有一行 `{request_id,data}`，`request_id` 为 `null`。失败时 stdout 为空，stderr 只有一行 `{error:{code,message,request_id,retryable}}`，`request_id` 为 `null`，`retryable` 为 `false`。用法或输入错误退出 2；运行时错误退出 1。

#### `archive init`

当前工作目录已存在 `.autoverse/library.sqlite` 时，`archive init` 失败，错误码为 `ARCHIVE_ALREADY_INITIALIZED`。

当前工作目录不存在该文件时，CLI 创建 `.autoverse/` 与空的 `library.sqlite`。`data` 至少包含工作区目录的绝对路径与数据库文件的绝对路径。

#### `archive add`

`-f` / `--file` 必填。路径或 `-` 表示标准输入。文件必须是 UTF-8。

输入 JSON 的识别顺序与 [cli-export-ris-bibtex.md](cli-export-ris-bibtex.md) 中 `export` 的输入形状相同：

1. `{ "data": { "items": [ ... ] } }`
2. `{ "data": { "title": "...", ... } }` 且 `data` 没有 `items`
3. `{ "items": [ ... ] }`
4. 题录数组
5. 单篇题录（根上有 `title`）

`items[]` 每条：有 `paper` 且 `paper` 有非空 `title` 则用 `paper`；否则条目自身有非空 `title` 则用条目；只有 `error`、没有非空标题的条目计入跳过，不写入数据库。

当前工作目录不存在 `.autoverse/library.sqlite` 时，`archive add` 失败，错误码为 `ARCHIVE_NOT_INITIALIZED`。CLI 不创建目录，不创建数据库。

每一条拟写入的题录必须至少具备一个稳定标识符。检查顺序：`identifiers.doi` 或 `id` 为 `doi:` 前缀；否则 `identifiers.pmid` 或 `pmid:`；否则 `identifiers` 中的 arXiv 编号或 `arxiv:`；否则 `identifiers.pmcid` 或 `pmcid:`。四者都不存在时，该条不得写入，该条计入失败项；若输入中没有任何一条可写入，整次命令失败，错误码为 `ARCHIVE_IDENTIFIER_REQUIRED`。Agent 必须先对该篇调用 `resolve` 或 `batch` 补齐稳定标识符，再重新 `archive add`。

去重键与检查顺序相同。数据库中已存在相同稳定标识符的篇目时，CLI 不插入第二行。已有行的字段是否用新 JSON 覆盖，本文不定，实现规格须另写一句。

`data` 至少包含：`added`（新插入的篇数）、`duplicate`（因去重未插入的篇数）、`skipped`（无标题或仅有 error 的条数）、`rejected`（无稳定标识符的条数）。

#### `archive list`

当前工作目录不存在 `.autoverse/library.sqlite` 时失败，错误码为 `ARCHIVE_NOT_INITIALIZED`。

成功时 `data.items` 为篇目数组。字段集合与现网 PaperCard 公开科研字段相同；库中缺失的字段留空，不编造。默认顺序为入库时间升序。第一版不提供按问句过滤。`--limit` 缺省与上限本文不定，实现规格须补数字。

#### `archive remove`

参数为一条稳定标识符。当前工作目录不存在数据库时失败，错误码为 `ARCHIVE_NOT_INITIALIZED`。库中没有该标识符时失败，错误码为 `ARCHIVE_PAPER_NOT_FOUND`。成功时删除该篇目所在行。`data` 至少包含被删除的稳定标识符。

数据库不保存检索问句，因此删除一篇不会改写「某一次检索记录」。库中只少这一篇。

### 3.7 Skill 须完成的动作

Agent 在调用 `archive add` 之前，必须已经把工作目录设为 3.3 所确定的那个检索工作区，或者学生已明确选择泛检索。

Agent 在新的一条对话开始、并且已经确定唯一检索工作区时，必须用该工作区的目录路径提醒学生。Agent 不询问是否继续使用该工作区。

学生要求新增检索工作区时，Agent 按 3.4 新建子目录并 `archive init`，然后提醒学生：本次之后的入库作用于新目录。

Agent 不得根据篇目库撰写综述正文。

### 3.8 按主题精选入库（后续版本）

第一版中，凡经 `archive add` 成功写入的篇目，都属于该检索工作区。本文不另设精选表，不要求学生再标记一次。

后续版本可以规定：学生或 Agent 按主题从篇目库中再选出一个子集。规则未写。

### 3.9 存档分析（后续版本）

下列三项写入方向名称，本讨论稿不写命令、不写 JSON 字段、不写验收勾选：

1. 判断篇目摘要对某一论断的支撑力度。
2. 判断尚未覆盖的检索角度。
3. 对库中篇目做跨年份对照。

跨年份对照是读取库中已有篇目按年份分组，还是对同一问句再次调用两次 `search`，本文不定。

**验收标准（方向三，讨论稿可测部分）**

- [ ] `archive init` 在空目录创建 `.autoverse/library.sqlite`；在已初始化目录再次执行则失败，错误码为 `ARCHIVE_ALREADY_INITIALIZED`
- [ ] 当前目录未初始化时，`add` / `list` / `remove` 失败，错误码为 `ARCHIVE_NOT_INITIALIZED`，并且不创建 `.autoverse`
- [ ] `archive add -f` 能读取与 `export` 相同的五种 JSON 形状；`search`、`related`、`resolve`、`batch` 的题录均可作为输入
- [ ] 无稳定标识符的条目不写入；全部条目均无稳定标识符时整次失败，错误码为 `ARCHIVE_IDENTIFIER_REQUIRED`
- [ ] 同一稳定标识符第二次 `add` 不产生第二行；`data.duplicate` 增加
- [ ] `archive remove` 按稳定标识符删除一行；不存在则 `ARCHIVE_PAPER_NOT_FOUND`
- [ ] `archive` 各子命令成功时不请求 `/v1`、不扣点、`request_id` 为 `null`
- [ ] Skill 正文写明：用文件系统判断 `.autoverse`；未初始化时询问新建子目录并 init 或不持久化；已初始化时不询问是否继续，只提醒路径；新增工作区时新建子目录再 init
- [ ] Skill 正文写明：`search` 成功不等于入库；入库必须再调用 `archive add`

**本次不包含（方向三）**

服务端保存篇目库；在 Autoverse 账户之间同步库；`search` 成功后自动入库；未初始化时自动 `init`；保存每一次检索的问句与命令；按相似程度去重；无稳定标识符时用题名合并；修改 `.gitignore`；`archive status` 或任何仅用于探测目录的 CLI 命令；存档分析的 CLI 动词；精选表；综述正文；期刊分区；下载全文。

---



## 4. 三个方向在讨论稿中的位置


| 方向      | 讨论稿写什么                          | 实现验收                  |
| ------- | ------------------------------- | --------------------- |
| 数据层     | 按日更新属于运维指标；渠道覆盖不讨论              | 无                     |
| 后端过滤    | 引用 AUT-12 分面；与现网 `--type` 的关系不定 | 无                     |
| 工作区与篇目库 | 目录约定、`archive` 合同、Skill 如何询问与提醒 | 第 3 节验收标准；存档分析与精选入库除外 |
| 交流 Skill 与可见文件 | 第 5 节已定稿：可见文件、挂篇与 `similar` | 实现规格另写；`tree.md` 为后续版本 |


后续讨论只在本文追加段落，不另起一份总稿。拆成 Linear Issue 须在讨论结束并且用户明确要求之后进行。

---



## 5. 交流 Skill 与工作区可见文件（2026-09-02 定稿）

本节把 STORM 的提问与组织做法接到第 3 节已经写明的检索工作区上。第 3 节的 CLI 合同不改：`archive` 仍只读写 `.autoverse/library.sqlite`，数据库仍只保存去重后的篇目，不保存问句。`archive init` 仍不创建、不修改 `.gitignore`。Agent 仍不撰写综述正文。STORM 的树对象、embedding 与 Qdrant 不进入 CLI。

交流 Skill（interact）调用现网命令，并维护 5.3 列出的可见文件。

### 5.1 两条执行面


| 谁        | 做什么                                                                                                       | 不做什么                                  |
| -------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| CLI      | `search` / `related` / `resolve` / `batch` 取题录；`archive` 去重入库；`export` 把已有 JSON 组装成 RIS、BibTeX 或 Markdown | 不提问；不写大纲；不拆同义词；不读维基百科；不调用本机大模型        |
| 交流 Skill | 拆研究角色与子问句、调用 `search`、核验后入库、更新大纲、向学生给出 A/B/C/D 选项                                                         | 不另写检索程序；不把维基百科条目写成已引用文献；摘要为空的篇目不得据以作答 |


一次交流的结果是**可编辑大纲**，可以理解成 deep-research-review。

### 5.2 整条链（已定）

1. Skill 按 3.3 判断检索工作区。需要持久化时按 3.4 新建子目录并 `archive init`。
2. 热身（可选）：用维基百科或已核验综述的章节结构，写出三到五个研究角色。维基百科只用于找视角和节名。
3. 把学生的一句问题展开成多条检索问句。展开必须改变检索对象（方法、数据、对照、局限）或换成该学科 reference 已列出的别名；不得只改无意义的同义词。
4. Agent 对这些问句分别调用 `search`（现网没有并发动词；并发是 Agent 多次调用）。每一问 1 点。
5. 拟纳入大纲或拟作答的标识写入本次任务文件，调用 `batch`。核验不上的不得当作已引用。
6. 学生已确认该工作区时，再调用 `archive add`。`search` 成功不等于入库。
7. 用当次 `search` JSON，或用 `archive list` 写出的 JSON，调用 `export`，得到学生能打开的 Markdown / RIS / BibTeX。
8. 更新工作区根下的可编辑大纲 outline.md：每节挂稳定标识符。没有挂上篇目的节不得写成已有文献支持。
9. 对照大纲已挂标识与库中篇目，列出已入库、摘要非空、但尚未挂到任何一节的篇目，并据此写出「下一问」。
10. 用 Agent 已有的向学生提问的能力，给出 A/B/C/D。A/B/C 是本轮角色或角度；**D 固定为从未引用命中抽出的下一问**。学生也可自写问句。
11. 学生选定后回到第 3 步。作答只使用已核验且摘要非空的篇目；摘要撑不住则写「根据已返回摘要无法回答」。

### 5.3 学生看见的目录（已定）

检索工作区是 3.4 新建的那个子目录。学生打开的是这个目录，不是只打开 `.autoverse`。

第一版学生必须看见、且交流 Skill 必须维护：

```text
<学生指定的子目录>/
  outline.md                 # 可编辑大纲；每节列出稳定标识符
  queries.md                 # 已用问句、研究角色、学科别名
  unused.md                  # 已入库但未挂到大纲的篇目，以及据此写出的下一问
  export/library.json        # archive list 写出的题录，供 export 读取
  export/papers.md
  export/papers.ris
  export/papers.bib
  .autoverse/library.sqlite  # CLI 篇目库；学生一般不打开
```

第一版不要求 `tree.md`。第一版不要求学生看见 `hits/`。Skill 在入库后调用 `archive list`，写成 `export/library.json`，再对这份文件调用 `export`。本节不增加 `archive export` 动词。

`.autoverse/` 只给 CLI。`outline.md`、`queries.md`、`unused.md`、`export/` 在根下，学生可以用编辑器改大纲。

### 5.4 交流 Skill 怎么迭代这些文件


| 轮次 | Skill 改哪些文件 | 仍不改 |
| --- | --- | --- |
| 第 0 轮：建工作区 | 空的 `outline.md`、`queries.md`、`unused.md`；按 3.4 `archive init` | 综述正文 |
| 第 1 轮：拆问并检索 | 追加 `queries.md`；`archive add`；更新 `export/` | `.autoverse` 的库结构 |
| 第 2 轮：交大纲 | 重写或补 `outline.md`；按已挂标识更新 `unused.md` | 不把未挂篇目写成节内结论 |
| 第 3 轮：给学生选项 | 把 A/B/C/D 写入对话；D 的问句同时写入 `unused.md` | 不代替学生选定 |
| 后续轮 | 学生改大纲或选 D 之后，只更新被改到的节、问句和导出 | 不重建整个库 |

`tree.md` 是后续版本：大纲用顺了，再从 `outline.md` 的节名收成分类树。第一版的挂篇与展开只写在 `outline.md` 与 `unused.md` 上，见 5.8.4。

### 5.5 `.gitignore`

第 3 节已锁定：`archive init` 不创建、不修改 `.gitignore`。本节不推翻这一句。

交流 Skill 第一版也不写入 `.gitignore`。学生自行决定是否把子目录纳入版本库。等 `export/` 或从 `archive list` 写出的 JSON 已经能单独恢复题录之后，再讨论 Skill 是否只忽略 `.autoverse/`。

### 5.6 维基百科

已定：Agent 只读取维基百科的目录和相近条目，用来生成研究角色与大纲节名。

不允许：把维基百科条目写入 `archive`；把维基百科 URL 当作稳定标识符；把维基百科句子写入证据表或综述参考文献。网页不能证明两篇论文之间的参考文献关系或后续引用关系。写入大纲或作答的文献标识仍须通过 `batch`。

### 5.7 与第 3 节「本次不包含」的关系

本节不要求改 `archive` 合同，不要求 `search` 自动入库，不要求 CLI 提问，不要求本机大模型。若要把「多条问句一次检索并去重」做成 CLI 动词，须另开讨论，不从交流 Skill 里发明命令名。

**本节已定**

- 第一版可见文件按 5.3：`outline.md`、`queries.md`、`unused.md`、`export/`。不要求 `tree.md`，不要求学生看见 `hits/`。
- 交流 Skill 第一版不写 `.gitignore`。
- 维基百科只读目录和相近条目，用来生成研究角色与大纲节名。
- STORM 的树对象、embedding 与 Qdrant 不进入 CLI。篇目只在 `library.sqlite`。语义近邻走现网 `related --via similar`。

### 5.8 `tree.md` 与 `similar`（第一版对着大纲做；树为后续版本）

Co-STORM 的概念树是进程内的 `KnowledgeNode`：节点只保存信息编号，正文存在另一张表；新材料靠大模型逐层选择 `insert` / `step` / `create`，并用 embedding 余弦相似度排序；节点过满时 `reorganize()` 再拆。这一套依赖本机或远程写模型与编码器，不进入 Autoverse。

第一版没有 `tree.md`。语义近邻对着 `outline.md` 已挂的一篇和 `unused.md` 里的一篇来做。后续版本若增加 `tree.md`，文件仍由交流 Skill 读写，不是 CLI 动词，也不写入 `library.sqlite`。现网没有「读树」或「按节检索」的命令。`related --via similar` 一次只接受**一篇**已核验种子，返回上游认为相近的题录，不读 Markdown，不写 Markdown。

#### 5.8.1 文件规则与样例

标题行是节名。列表项只允许一条稳定标识符，行首用 `- `。同一标识在整份 `outline.md` 里只出现一次。题名、作者、年份、摘要、问句、维基百科 URL 都不写在大纲的列表里。空节可以暂时没有列表项；没有挂篇的节不得写成已有文献支持。

`#` 是题目，与子目录名称对应，根下不挂篇。`##`、`###` 是节。引言、结语、讨论可以有节名，但第一版这三节不挂篇，篇目挂在主题各节。

第一版学生改的是 `outline.md`，不是 `tree.md`。样例如下。标识均为示意；实现与验收须换成该工作区 `archive list` 里真实存在的标识。

`outline.md`：

```markdown
# Transformer 注意力

## 奠基
- arxiv:1706.03762

## 方法
- doi:10.18653/v1/N19-1423

## 评价
```

同一工作区的 `unused.md`（库中有、大纲上没有）：

```markdown
# 未挂到大纲的篇目

## 篇目
- doi:10.1016/j.specom.2025.103242

## 下一问
语音情感识别里的多维注意力，和大纲「方法」一节是同一条技术线，还是另一类任务？
```

学生可以改节名、把某一行从 `unused.md` 剪到 `outline.md` 的某一节下。Skill 下一轮以磁盘文件为准，并核对这些标识是否仍在 `archive list` 中。大纲里出现库中没有的标识，Skill 删除该行并提醒，不补造题录。

后续版本的 `tree.md` 从这份大纲的节名生成，规则仍是：标题是节点，列表项只挂稳定标识符。第一版不生成该文件。

#### 5.8.2 现网 `related --via similar` 怎么调用

没有名为 `similar` 的顶层动词。命令是 `related`，`--via similar`。

```text
autoverse --json --quiet related arxiv:1706.03762 --via similar --limit 20
```

合同与 [../skills/autoverse-cli/references/commands.md](../skills/autoverse-cli/references/commands.md) 中 Related 一节相同，写进交流 Skill 时必须遵守：

1. 参数是一篇带前缀的稳定标识符，不是节名，不是 `outline.md` 或 `tree.md` 的路径，不是问句。
2. `--via similar` 固定 source=recent，禁止 `--offset`。一次调用只有一页。需要更多篇时，换另一篇种子再调用，不得假装翻页。
3. 含斜杠的 DOI 须先 `resolve`，再用返回的 path-safe 标识调用 `related`。裸数字拒绝。
4. 成功时 `data.items` 是 PaperCard 数组。`similar` 不附加 `relation`。返回顺序不是「重要性」，也不是「应挂到树上的顺序」。
5. 点数：每次 `related` 计 1 点；DOI 若先 `resolve` 另计 1 点。`search` 成功或 `related` 成功都不写入 `library.sqlite`，须再 `archive add`。
6. 503 不降级为 `search`。

`outline.md` 每一节每一轮最多选**一篇**已挂、摘要非空的代表作当种子，不要对节下每一篇都打 `similar`。

#### 5.8.3 `similar` 对第一版大纲能起什么作用

CLI 不改 `outline.md`。Skill 读返回的 `items`，核验、入库，再向学生提议改大纲或 `unused.md`。作用只有下面三件。

**作用一：沿着大纲里已有的一篇，给同一节找候选。**

学生或 Agent 指定「奠基」下的 `arxiv:1706.03762`。Agent 调用 5.8.2 的命令。对返回标识做 `batch`。摘要为空的条目可以入库，但不得据以写下一问或节内结论。已在大纲上的标识丢弃。其余经学生同意后 `archive add`，默认提议挂到种子所在节（样例里是「奠基」）；学生也可以改挂到「方法」或写入 `unused.md`。

这一步增加的是**候选篇**，不是把「奠基」一节自动写长。不证明返回篇是种子的参考文献或后续引用。要把引用关系写成已核验，须另走 `--via references` 或 `--via cited-by`，并遵守 seed-expand 的反查规则。

**作用二：给 `unused.md` 里的一篇建议落点。**

对 `doi:10.1016/j.specom.2025.103242` 调用 `related --via similar`。若返回标识里有已经出现在 `outline.md` 某一节下的篇（例如命中了「方法」下的 `doi:10.18653/v1/N19-1423`），Skill 只向学生建议：「这篇与大纲「方法」一节已有篇相近」。学生同意后，把该行从 `unused.md` 移到「方法」。返回列表与大纲没有任何交集时，Skill 不得按模型记忆选一节，须保持未挂，或把该次 `similar` 的问法写成 D 选项。

这一步是用「种子的相近篇 ∩ 大纲已挂标识」做落点提示。现网 `similar` 不能输入「方法」两个字。

**作用三：为 D 选项提供下一问的种子。**

`similar` 返回、已核验、摘要非空、且尚未出现在 `outline.md` 与当次入库提议中的篇，可以写进 `unused.md` 的「下一问」。问句须能回到这些摘要。摘要撑不住则写「根据已返回摘要无法回答」，不写进 D。

**明确做不到的事。**

| 有人可能以为 CLI 能做 | 现网实际 |
| --- | --- |
| `related outline.md --via similar` 或传入 `tree.md` | 不能。输入必须是一篇带前缀标识 |
| 按节名「方法」做语义检索 | 节名走 `search`，不走 `similar` |
| 一次传入一节下的多篇 | 一次只有一篇种子 |
| 比较库内两篇是否相近 | `similar` 问的是上游索引里与种子相近的篇，不是本机库内配对 |
| 自动改写 `outline.md` | 只有 Skill 在学生同意后改文件 |
| 用 `similar` 证明引用 | `similar` 不产生 `relation`，不能写成参考文献或后续引用 |
| 翻页取「更相似」的后面几页 | 禁止 `--offset` |

#### 5.8.4 一篇只挂一处，篇数变多时怎么展开

这句话管的是 `outline.md` 这份 Markdown，**不管** `library.sqlite`。库里可以有几十、几百篇；`archive list` 与 `export/` 才是全库。大纲只挂准备写进综述的那一部分。其余已入库的标识写在 `unused.md`，不要为了「树要完整」把全库抄进大纲。

**一篇只挂一处。** 同一个稳定标识符在 `outline.md` 里只出现在一个 `##` 或 `###` 下面。一篇既像「方法」又像「评价」时，第一版挂到更贴近当前写作的那一节，另一节不重复写这一行。学生可以改挂。Skill 发现同一标识出现两次，须删掉后出现的那一行并提醒。未挂的篇只留在 `unused.md`，也不要在未挂清单里写两遍。

**展开不是往同一节底下无限追加。** 新篇的来源是 `search` 或 `related --via similar`。入库之后只做三选一，写回文件：

1. 挂到已有的一节（该节因此多一行标识）；
2. 学生同意后，在该节下新增一个 `###` 小节，再挂到小节里；
3. 写入 `unused.md`，不进大纲。

`similar` 只提供候选名单。Skill 不得因为一次返回了十几篇，就把它们全部写进种子所在节。默认：提议挂代表作所在节的至多若干篇（具体篇数实现规格再定），其余进 `unused.md`，由学生下轮再选。

**某一节显得太长时。** 第一版不设硬上限，也不自动拆节。学生说某一节太长，或 Skill 看到某一节已挂篇数明显多于其他节时，向学生提议拆成 `###` 小节，并把原节下的标识挪到小节里。不得自行重写整份大纲。拆节不是再打一遍 `similar`。

后续版本的 `tree.md` 沿用同一条「一篇只挂一处」：分类树可以比大纲多挂一些库内篇，但同一标识在树上仍只出现一次。第一版不写该文件。

**本次不包含。** 把树或大纲节名存进 SQLite；`archive` 增加按节列出的参数；`related` 接受文件或节名；本机 embedding；自动拆节。

### 5.9 评估：树对象、embedding 与项目内向量库（已定：不进 CLI）

STORM 仓库里有两套互不相同的向量用法，不能当成一件事搬进 CLI。


| 原仓库部分                                                   | 向量算什么     | 存在哪               | 还依赖什么                                      |
| ------------------------------------------------------- | --------- | ----------------- | ------------------------------------------ |
| `KnowledgeBase.get_knowledge_base_structure_embedding`  | 节点路径那几行字  | 进程内存；LiteLLM 磁盘缓存 | OpenAI / Azure 的 `text-embedding-3-small`  |
| `InsertInformation` / `ExpandNodeModule` / `reorganize` | 不存向量      | 无                 | **大模型**逐层决定 insert / step / create，并给子节点起名 |
| `VectorRM`                                              | 用户自备文档的正文 | 本机或云端 Qdrant      | HuggingFace 本机 embedding（cpu / cuda / mps） |


把「内存对象加 embedding」放进 CLI、把向量库存进检索工作区，只覆盖上表第一行的存储形态，**不能**得到 STORM 的自动挂篇。自动挂篇的核心是大模型，不是向量库。

**树对象进 CLI。** 技术上可以把节点表和「节点—稳定标识符」表写进 `.autoverse/`。产品上会和 5.8 抢源：学生改 `tree.md` 与 CLI 改库必须规定以谁为准。第 3 节已定数据库只存去重篇目。树进库等于改这一句。现网 CLI 也不创建工作区笔记。结论：对象可以序列化，但第一版不值得放进 `archive`。

**节点路径 embedding。** STORM 每次只编码当前树的几十行路径，用来给「挂到哪」排序。这个量级不需要 Qdrant。若以后要给 Agent 候选节点，用后端已有语义口或 `related --via similar` 即可。CLI 在本机调 OpenAI embedding 会引入第二套密钥，和现网只认 Autoverse 登录冲突；本机 HuggingFace 与「不调用本机大模型」冲突。

**篇目摘要向量进项目。** 和 [AUT-20](https://linear.app/autoversecn/issue/AUT-20/完成-cos-去重全量索引与语义检索)、讨论记录第 3 条语义版本、现网 `related --via similar` 重复。学生一个工作区通常是几十到几百篇，不是百万向量。若以后要在本机对「本库篇目」做近邻，应由 Autoverse 后端按已核验摘要出向量，CLI 只缓存；不宜在项目里起 Qdrant 或本机编码器。缓存文件须进 `.gitignore` 讨论，第一版尚未写 `.gitignore`。

**Qdrant + 本机 HuggingFace（VectorRM）进项目。** 不可行。那是用自备 CSV 正文替代网页检索，不是篇目库。依赖 torch / 设备 / 模型文件，违反本机大模型边界，也另开一条文献发现入口。

**整套挂篇逻辑进 CLI。** 不可行。`insert` / `step` / `create` 与 `reorganize` 必须调用大模型。CLI 现网不调用任何写模型。把决策放进 CLI 会变成后端黑盒，与第 3 条「判断仍由 Agent 做」不一致。

**结论（已定）。** 第一版不写 `tree.md`。篇目只在 `library.sqlite`。不在检索工作区建立向量库，不把 STORM 的树对象或 embedding 放进 CLI。语义近邻走现网 `related --via similar`。挂到哪一节由交流 Skill 按 5.8.4 写回 `outline.md` 或 `unused.md`。

