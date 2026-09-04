# 综述引用格式

Agent 撰写综述草稿时阅读本文件。编号与参考文献由 `scripts/render_cites.py` 生成，Agent 不得手写 `[1]`，也不得手写「参考文献」。

## 标准写法

一篇：

```text
…该试验改善了无进展生存[@10.1056/NEJMoa1911440]。
```

同处多篇，用分号：

```text
…两条通路相互反馈[@10.1016/j.ccr.2011.04.008; @10.1002/pros.24372]。
```

键只用已核验 JSON 里的 DOI，去掉 `https://doi.org/`。没有 DOI 时依次用 `pmid:数字` 或 `arxiv:编号`：

```text
[@pmid:35657152]
[@arxiv:1706.03762]
```

不要写 `\cite{…}`，不要写导出 BibTeX 自动生成的 `[@pitakaso2025…]` 那种键，不要在草稿正文写 `[1]`。

列出本题可用的键：

```text
python "<本技能包根目录>/scripts/render_cites.py" --json <batch或search的JSON> --keys
```

本技能包根目录是含 `SKILL.md` 的 `universe-research` 目录。不要依赖当前工作目录恰好是该目录。

同处多篇只把 `; @`（分号后可有空格再写 `@`）当成分隔。DOI 内部的分号不是分隔符。

## 编译

```text
python "<本技能包根目录>/scripts/render_cites.py" --json <batch或search的JSON> --draft <综述草稿.md> --out <综述.md> --csv <证据表.csv>
```

脚本按正文**第一次出现**把 `[@…]` 换成 `[1]`、`[2]`、`[1, 2]`，并写出「参考文献」。证据表前七列按同一编号从 JSON 灌入；「与本问题相关的要点」留空，Agent 按 `[n]` 填写。JSON 里有、草稿没引用的篇目不进入交稿。键不在 JSON 里则失败，不编造题录。
