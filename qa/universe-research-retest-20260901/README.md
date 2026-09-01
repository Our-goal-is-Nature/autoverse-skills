# 2026-09-01 三科复测

三组 Agent 均按 `skills/universe-research/SKILL.md` 现网条文执行。测试日期为 2026-09-01。默认起始年为 2022，默认结束年为 2026。三组均未改写起止年。主题检索均同时写入 `--year-from 2022` 与 `--year-to 2026`。基础论文均先在默认时间范围内的综述或摘要中发现候选，再用完整题名、不带起止年的 `search` 核验后纳入。

本目录只存放复测交稿，不改 Skill 条文。

## 时序方向（计算机科学）

- 综述、证据表、tool-use 分别见 `时序方向/`。
- 纳入 28 篇。年份范围为 2021–2025。2022–2026 年共 26 篇，占 26/28。
- 基础论文 2 篇：Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting；Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting。
- 主题检索 15 次，全部带默认起止年。其中 2 次返回 `ALL_SOURCES_UNAVAILABLE`，按规则重试一次后停止。
- 题名核验 2 次。`batch` 1 次：29 条中 28 条成功；`doi:10.48550/arxiv.2510.13654` 返回 `not_found`，未写入综述。
- `--domain computer_science`。未改写起止年。

## 前列腺癌通路（医学）

- 综述、证据表、tool-use 分别见 `前列腺癌通路/`。
- 纳入 29 篇。年份范围为 2011–2026。2022–2026 年共 26 篇，占 26/29。
- 基础论文 3 篇：Reciprocal Feedback Regulation of PI3K and Androgen Receptor Signaling in PTEN-Deficient Prostate Cancer（2011）；AR-V7 and Resistance to Enzalutamide and Abiraterone in Prostate Cancer（2014）；DNA-Repair Defects and Olaparib in Metastatic Prostate Cancer（2015）。
- 主题检索 17 次，全部带默认起止年。8 次返回 `ALL_SOURCES_UNAVAILABLE`。未调用医学补充 api。
- 题名核验 3 次。`batch` 1 次，29/29 通过。
- `--domain medicine`。未改写起止年。综述不构成个体诊疗建议。

## 电网资源分配（工科）

- 综述、证据表、tool-use 分别见 `电网资源分配/`。
- 纳入 29 篇。年份范围为 2004–2026。2022–2026 年共 26 篇，占 26/29。
- 基础论文 3 篇：Unit Commitment—A Bibliographical Survey；A Computationally Efficient Mixed-Integer Linear Formulation for the Thermal Unit Commitment Problem；Coordination between transmission and distribution system operators in the electricity sector: A conceptual framework。
- 主题检索 15 次，全部带默认起止年。题名核验 6 次。`batch` 1 次，30 条均成功；其中 `doi:10.1016/j.ijepes.2022.108735` 摘要为空，未写入综述。
- `--domain auto`。未自造 `--domain engineering`。未改写起止年。

## 与条文的对照

三组均满足：主题检索带默认起止年；未说明原因则不扩大时间范围；基础论文先发现再核验；文献来源写出默认与实际起止年、默认范围内篇数、核验后纳入的基础论文篇数。
