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
| `search` | 1；expanded 2；cursor 0 | query、domain、mode、year、type、limit、cursor | PaperCard 列表、next_cursor |
| `resolve` | 1 | prefixed identifier | PaperDetail |
| `batch` | 1/调用 | `-f/--file`，1–50 ID | identifier + PaperCard/error |
| `authors` | 1 | name | AuthorCard 列表 |
| `related` | 1/via/page；DOI 内嵌 resolve 另 1 | identifier、via、limit、offset | PaperCard 列表、via、seed、next_offset |

## Search

首屏：

```text
autoverse --json --quiet search "<query>" --limit 20
```

`--domain`：`auto|medicine|computer_science`

`--mode`：`auto|relevance|systematic|expanded`

`--type`：`journal_article|review|meta_analysis|clinical_trial|case_report`，可重复。

翻页：

```text
autoverse --json --quiet search --cursor <token> --limit 20
```

cursor 模式禁止 query、domain、mode、year 和 type。token 不透明。

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
- DOI 或含斜杠 ID 先 resolve，再选 path-safe ID；
- 裸数字拒绝；
- 结果剥除 contexts/intents/is_influential；
- 503 不降级 search。

## PaperCard

```json
{
  "id": "doi:10.x/y",
  "title": "Paper title",
  "year": 2025,
  "venue": "Journal",
  "first_author": "A. Smith",
  "author_count": 4,
  "identifiers": {"doi": "10.x/y", "pmid": "123"},
  "abstract": "..."
}
```

`PaperDetail` 只额外增加 `authors:string[]` 与 `publication_types:string[]`。

默认不返回 route、source_status、usage、sources、provenance、conflicts、citation_counts、subjects、OA 细节或 Provider 原始对象。

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
