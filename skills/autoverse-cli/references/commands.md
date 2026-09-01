# CLI Commands and Machine Contract

只在用户询问具体命令、参数、返回字段、点数或错误恢复时读取。

## 全局语法

```text
autoverse [--json] [--quiet] [--api-base URL] [--api-key KEY] [--profile NAME] <command> ...
```

全局旗标必须放在动词前。Agent 固定使用 `--json --quiet`。

## 账户族

| 命令 | 点数 | 机器 data |
|---|---:|---|
| `login` | 0 | `{status,email}` |
| `logout` | 0 | `{status}` |
| `whoami` | 0 | `{identity,email,balance}` |
| `usage` | 0 | `{balance,prices}` |
| `topup` | 0 | `{account_email,packs}` |

`login --no-browser` 会在等待回调时向终端展示授权 URL，只用于人读模式；不得与 `--json` 组合。

## 文献原子族

| 命令 | 点数 | 主要参数 | 机器 data |
|---|---:|---|---|
| `search` | 1；expanded 2；cursor 0 | query、domain、mode、year-from、year-to、type、limit、cursor | PaperCard 列表、next_cursor |
| `resolve` | 1 | prefixed identifier | PaperDetail |
| `batch` | 1/调用 | `-f/--file`，1–50 ID | identifier + PaperDetail/error |
| `authors` | 1 | name | 完整 AuthorCard 列表 |
| `related` | 1/via/page；DOI 内嵌 resolve 另 1 | identifier、via、limit、offset | PaperCard 列表、via、seed、next_offset |

## Search

首屏：

```text
autoverse --json --quiet search "<query>" --limit 20
```

`--domain`：`auto|medicine|computer_science`

`--mode`：`auto|relevance|systematic|expanded`

`--year-from`、`--year-to`：闭区间年份。不要使用已移除的 `--year`。

`--type`：`journal_article|review|meta_analysis|clinical_trial|case_report`，可重复。

翻页：

```text
autoverse --json --quiet search --cursor <token> --limit 20
```

cursor 模式禁止 query、domain、mode、year-from、year-to 和 type。token 不透明。

## Resolve and Batch

`resolve` 接受 `doi:`、`pmid:`、`pmcid:`、`arxiv:`。

`batch` 文件支持路径或 `--file -` 从 stdin 读取。文件必须 UTF-8、一行一个 ID、1–50 条。

## Related

```text
autoverse --json --quiet related <prefixed-id> --via references|cited-by|similar --limit 20
```

- `references` / `cited-by` 支持 `--offset`；
- `similar` 固定 source=recent，禁止 offset；
- pmid 直接变成 `PMID:<digits>`；
- semantic_scholar 使用 paperId；
- `s2:<digits>` 变成 `CorpusId:<digits>`；
- `pmcid:PMC10328000` 与 `pmcid:10328000` 都变成 `PMCID:10328000`；
- DOI 或含斜杠 ID 先 resolve，再选 path-safe ID；
- 裸数字拒绝；
- `references` / `cited-by` 在上游提供引用边信息时保留 `relation.contexts/intents/is_influential`；没有边信息时省略 `relation`；`similar` 不产生 `relation`；
- 503 不降级 search。

## PaperCard / PaperDetail

```json
{
  "id": "doi:10.x/y",
  "title": "Paper title",
  "year": 2025,
  "publication_date": "2025-06-30",
  "venue": "Journal",
  "venue_type": "journal",
  "venue_issn": "1234-5678",
  "first_author": "A. Smith",
  "author_count": 4,
  "authors": ["A. Smith", "B. Jones"],
  "author_details": [{"name":"A. Smith","sequence":1,"author_id":"a1","orcid":null,"affiliations":[]}],
  "publication_types": ["review"],
  "identifiers": {"doi": "10.x/y", "pmid": "123"},
  "abstract": "...",
  "citation_counts": [{"provider":"openalex","value":42}],
  "open_access": {"is_oa":true,"status":"gold","url":"https://...","license":"cc-by","provider":"openalex"},
  "subjects": ["oncology"]
}
```

`search`、`resolve`、`batch` 和 `related` 使用同一公开科研字段集合（上表全部字段）。`batch.items[].paper` 与 `resolve.data` 保持一致；`search.data.items[]` 与 `related.data.items[]` 也使用同一形状。被引按来源分别返回，不合成单一数字。

`authors` 额外返回 aliases、paper_count、citation_counts、h_index 与 external_ids。`related` 的 `references` / `cited-by` 条目在上游提供引用边字段时附加 `relation`（包含 `contexts`、`intents`、`is_influential`）；`similar` 不附加 `relation`。没有引用边信息时省略该键，不返回空的伪关系。

默认不返回 route、source_status、usage、sources、provenance、conflicts 或 Provider 原始对象。高级原始调试才使用 `api`。

## Error Codes

| code | Agent 行为 |
|---|---|
| `INVALID_SESSION` / `INVALID_API_KEY` | 登录或检查明确提供的 CI Key |
| `INSUFFICIENT_CREDITS` | usage/topup，停止 |
| `QUERY_REQUIRED` | 首屏补 query |
| `CURSOR_OPTION_CONFLICT` | cursor 页移除 query/filter |
| `LIMIT_OUT_OF_RANGE` | 改为 1–50 |
| `INVALID_DOMAIN/MODE/PUBLICATION_TYPE` | 使用 help 枚举 |
| `INPUT_FILE_NOT_FOUND/NOT_READABLE/NOT_UTF8/EMPTY` | 修正输入 |
| `BATCH_LIMIT_EXCEEDED` | 拆成最多 50 条 |
| `RELATED_ID_PREFIX_REQUIRED/INVALID/UNUSABLE` | 使用 path-safe prefixed ID |
| `RELATED_OFFSET_NOT_SUPPORTED` | similar 移除 offset |
| `REQUEST_OUTCOME_UNKNOWN` | 查 usage，不重发 |
| `ALL_SOURCES_UNAVAILABLE` | 按 retryable 最多一次，然后停口 |

## Escape Hatch

```text
autoverse --json --quiet api -X GET /v1/...
```

只在用户明确要求高级原始 API 调试时使用；普通调用优先精选动词。
原始成功响应可以是 JSON 对象或数组；CLI 会保持对象，并把顶层数组放入 `data`。
