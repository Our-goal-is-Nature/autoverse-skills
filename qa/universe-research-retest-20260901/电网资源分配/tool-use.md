# tool-use

全部调用均为 `autoverse --json --quiet`。退出码均为 0，无错误码。

## 账户

```text
autoverse --json --quiet whoami
```

- year-from/year-to：无
- 返回：已登录（api_key），balance=665
- 退出码：0

## 主题检索（均带 --year-from 2022 --year-to 2026）

```text
autoverse --json --quiet search "power system resource allocation generation scheduling security-constrained optimal power flow review" --domain auto --year-from 2022 --year-to 2026 --type review --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：20；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "unit commitment generation scheduling economic dispatch power system" --domain auto --year-from 2022 --year-to 2026 --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：20；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "security-constrained optimal power flow SCOPF security-constrained economic dispatch SCED" --domain auto --year-from 2022 --year-to 2026 --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：15；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "distributed energy resources energy storage distribution network allocation" --domain auto --year-from 2022 --year-to 2026 --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：20；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "TSO-DSO coordination electricity market distributed flexibility" --domain auto --year-from 2022 --year-to 2026 --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：20；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "security-constrained unit commitment SCUC review renewable" --domain auto --year-from 2022 --year-to 2026 --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：20；年份 min/max：2022/2025
- 退出码：0

```text
autoverse --json --quiet search "optimal power flow OPF review power system AC DC" --domain auto --year-from 2022 --year-to 2026 --type review --limit 20
```

- year-from/year-to：有（2022–2026）
- 返回篇数：7；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "TSO DSO coordination flexibility market review" --domain auto --year-from 2022 --year-to 2026 --type review --limit 15
```

- year-from/year-to：有（2022–2026）
- 返回篇数：13；年份 min/max：2022/2026
- 退出码：0

```text
autoverse --json --quiet search "battery energy storage allocation distribution network optimal siting sizing" --domain auto --year-from 2022 --year-to 2026 --limit 15
```

- year-from/year-to：有（2022–2026）
- 返回篇数：15；年份 min/max：2022/2024
- 退出码：0

```text
autoverse --json --quiet search "security-constrained AC optimal power flow SCOPF N-1 contingency" --domain auto --year-from 2022 --year-to 2026 --limit 15
```

- year-from/year-to：有（2022–2026）
- 返回篇数：15；年份 min/max：2022/2024
- 退出码：0

```text
autoverse --json --quiet search "economic dispatch review power system renewable generation" --domain auto --year-from 2022 --year-to 2026 --type review --limit 15
```

- year-from/year-to：有（2022–2026）
- 返回篇数：15；年份 min/max：2022/2025
- 退出码：0

```text
autoverse --json --quiet search "distribution system operator transmission system operator coordinated market flexibility procurement" --domain auto --year-from 2022 --year-to 2026 --limit 15
```

- year-from/year-to：有（2022–2026）
- 返回篇数：15；年份 min/max：2022/2025
- 退出码：0

```text
autoverse --json --quiet search "active distribution network optimal power flow distributed generation energy storage" --domain auto --year-from 2022 --year-to 2026 --limit 15
```

- year-from/year-to：有（2022–2026）
- 返回篇数：15；年份 min/max：2022/2024
- 退出码：0

```text
autoverse --json --quiet search "security-constrained unit commitment transmission constraint N-1 reserve requirement" --domain auto --year-from 2022 --year-to 2026 --limit 12
```

- year-from/year-to：有（2022–2026）
- 返回篇数：12；年份 min/max：2022/2024
- 退出码：0

```text
autoverse --json --quiet search "TSO-DSO coordination common TSO-DSO market centralized decentralized" --domain auto --year-from 2022 --year-to 2026 --limit 12
```

- year-from/year-to：有（2022–2026）
- 返回篇数：12；年份 min/max：2022/2025
- 退出码：0

## 题名核验（均不带 --year-from / --year-to）

```text
autoverse --json --quiet search "State-of-the-art, challenges, and future trends in security constrained optimal power flow" --domain auto --limit 5
```

- year-from/year-to：无
- 返回篇数：5；年份 min/max：2011/2021
- 退出码：0
- 说明：命中 Capitanescu 等 2011，摘要为空，未纳入综述与证据表。

```text
autoverse --json --quiet search "Unit commitment a bibliographical survey Padhy" --domain auto --limit 5
```

- year-from/year-to：无
- 返回篇数：5；年份 min/max：2007/2022
- 退出码：0
- 说明：该次未以完整题名命中 Padhy 2004，随后改用完整题名再核。

```text
autoverse --json --quiet search "Coordination between transmission and distribution system operators in the electric sector: A conceptual framework" --domain auto --limit 5
```

- year-from/year-to：无
- 返回篇数：5；年份 min/max：2013/2020
- 退出码：0
- 说明：命中 Gerard 等 2017（题名作 electricity sector）。

```text
autoverse --json --quiet search "Unit Commitment—A Bibliographical Survey" --domain auto --limit 5
```

- year-from/year-to：无
- 返回篇数：5；年份 min/max：2004/2022
- 退出码：0
- 说明：命中 Padhy 2004，纳入。

```text
autoverse --json --quiet search "A computationally efficient mixed-integer linear formulation for the thermal unit commitment problem" --domain auto --limit 5
```

- year-from/year-to：无
- 返回篇数：5；年份 min/max：2006/2015
- 退出码：0
- 说明：命中 Carrión & Arroyo 2006，纳入。

```text
autoverse --json --quiet search "History of optimal power flow and formulations Cain O'Neill Castillo" --domain auto --limit 5
```

- year-from/year-to：无
- 返回篇数：5；年份 min/max：2014/2023
- 退出码：0
- 说明：未命中 Cain/O’Neill/Castillo 题录，未纳入。

## batch

标识文件：`/tmp/grid-resource-20260901/ids-grid-alloc-20260901.txt`（30 个 DOI）

```text
autoverse --json --quiet batch -f /tmp/grid-resource-20260901/ids-grid-alloc-20260901.txt
```

- year-from/year-to：无
- 返回：30 条全部成功（error 为空）
- 退出码：0
- 说明：其中 `doi:10.1016/j.ijepes.2022.108735` batch 后摘要为空，未写入综述与证据表。纳入 29 篇。

## 文末统计

- 纳入总篇数：29
- 2022–2026 篇数：26
- 基础论文题名：
  - Unit Commitment—A Bibliographical Survey
  - A Computationally Efficient Mixed-Integer Linear Formulation for the Thermal Unit Commitment Problem
  - Coordination between transmission and distribution system operators in the electricity sector: A conceptual framework
- 主题检索次数：15（全部带默认起止年 2022–2026）
- 题名核验次数：6
- batch 次数：1
- 是否改写默认起止年：否
- 调用次数：whoami 1 + search 21 + batch 1 = 23；错误码：无（全部退出码 0）
