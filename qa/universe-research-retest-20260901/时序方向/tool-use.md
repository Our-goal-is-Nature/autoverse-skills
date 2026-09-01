# tool-use 记录（时序方向，2026-09-01）

## 账户

```text
autoverse --json --quiet whoami
```

- 是否带 year-from/year-to：否
- 返回篇数：不适用
- 返回年份 min/max：不适用
- 退出码：0

## 主题检索（均带默认起止年 2022–2026）

### 1

```text
autoverse --json --quiet search "time series forecasting survey review computer science" --domain computer_science --year-from 2022 --year-to 2026 --type review --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2022 / 2026
- 退出码：0

### 2

```text
autoverse --json --quiet search "long-term time series forecasting Transformer PatchTST iTransformer" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2022 / 2026
- 退出码：0

### 3

```text
autoverse --json --quiet search "time series forecasting DLinear linear model MLP TSMixer" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2023 / 2026
- 退出码：0

### 4

```text
autoverse --json --quiet search "time series foundation model TimesFM Chronos Moirai Time-LLM zero-shot forecasting" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2023 / 2026
- 退出码：0

### 5

```text
autoverse --json --quiet search "time series forecasting benchmark dataset evaluation GIFT-Eval Time-Series-Library" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2022 / 2026
- 退出码：0

### 6

```text
autoverse --json --quiet search "Are Transformers Effective for Time Series Forecasting DLinear evaluation leakage" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2023 / 2026
- 退出码：0

### 7

```text
autoverse --json --quiet search "TimesNet Chronos Amazon time series Moirai Uni2TS foundation forecasting" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：0
- 返回年份 min/max：无
- 退出码：1
- 错误码：ALL_SOURCES_UNAVAILABLE（retryable）

### 8（对第 7 次按可重试规则重试一次）

```text
autoverse --json --quiet search "TimesNet Chronos Amazon time series Moirai Uni2TS foundation forecasting" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：0
- 返回年份 min/max：无
- 退出码：1
- 错误码：ALL_SOURCES_UNAVAILABLE（retryable；此后停止该查询）

### 9

```text
autoverse --json --quiet search "TimesNet time series analysis temporal 2D variation forecasting" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2022 / 2026
- 退出码：0

### 10

```text
autoverse --json --quiet search "DLinear Are Transformers Effective for Time Series Forecasting long-term" --domain computer_science --year-from 2022 --year-to 2026 --limit 20
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：20
- 返回年份 min/max：2022 / 2026
- 退出码：0

### 11

```text
autoverse --json --quiet search "graph neural network time series forecasting multivariate imputation classification" --domain computer_science --year-from 2022 --year-to 2026 --limit 15
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：15
- 返回年份 min/max：2022 / 2025
- 退出码：0

### 12

```text
autoverse --json --quiet search "TFB fair benchmarking time series forecasting information leakage evaluation protocol" --domain computer_science --year-from 2022 --year-to 2026 --limit 15
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：15
- 返回年份 min/max：2024 / 2026
- 退出码：0

### 13

```text
autoverse --json --quiet search "Informer Autoformer N-BEATS time series forecasting long-term" --domain computer_science --year-from 2022 --year-to 2026 --limit 15
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：15
- 返回年份 min/max：2022 / 2026
- 退出码：0

### 14

```text
autoverse --json --quiet search "Time-LLM Time Series Forecasting by Reprogramming Large Language Models" --domain computer_science --year-from 2022 --year-to 2026 --limit 10
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：10
- 返回年份 min/max：2024 / 2026
- 退出码：0

### 15

```text
autoverse --json --quiet search "Time-LLM reprogramming large language models time series Jin Wen" --domain computer_science --year-from 2022 --year-to 2026 --limit 10
```

- 是否带 year-from/year-to：是（2022–2026）
- 返回篇数：10
- 返回年份 min/max：2024 / 2026
- 退出码：0

## 核验用题名检索（不带 year-from / year-to）

### 16

```text
autoverse --json --quiet search "Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting" --domain computer_science --limit 5
```

- 是否带 year-from/year-to：否
- 返回篇数：5
- 返回年份 min/max：2020 / 2023
- 退出码：0
- 核验对象：Haoyi Zhou 等，Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting，2021，AAAI

### 17

```text
autoverse --json --quiet search "Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting" --domain computer_science --limit 5
```

- 是否带 year-from/year-to：否
- 返回篇数：5
- 返回年份 min/max：2021 / 2023
- 退出码：0
- 核验对象：Haixu Wu 等，Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting，2021

## batch

### 18

```text
autoverse --json --quiet batch -f /tmp/ts-research-20260901/batch-ids-20260901.txt
```

- 是否带 year-from/year-to：否
- 提交标识数：29
- 返回成功篇数：28
- 失败：1（`doi:10.48550/arxiv.2510.13654`，条目错误码 BATCH_ITEM_ERROR / not_found；未引用）
- 成功条目年份 min/max：2021 / 2025
- 退出码：0

## 文末统计

- 纳入总篇数：28
- 2022–2026 篇数：26
- 基础论文篇数与题名：2；Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting；Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting
- 主题检索次数：15（其中 2 次为同一查询的失败与一次重试）
- 核验用题名检索次数：2
- batch 次数：1
- 是否改写了默认起止年：否
