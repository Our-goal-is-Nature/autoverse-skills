"""把草稿里的 [@doi] 按首次出现编成 [n]，并写出综述与证据表。"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

CITE = re.compile(r"\[@([^]]+)]")
DOI_PREFIXES = ("https://doi.org/", "http://doi.org/", "doi:")


def one_line(value: object) -> str:
    return " ".join(str(value).replace("\r", "\n").splitlines()).strip()


def bare_doi(value: str) -> str:
    doi = value.strip()
    for prefix in DOI_PREFIXES:
        if doi.lower().startswith(prefix):
            return doi[len(prefix) :].strip()
    return doi


def normalize_key(raw: str) -> str:
    key = raw.strip()
    if key.lower().startswith("pmid:"):
        return "pmid:" + key.split(":", 1)[1].strip()
    if key.lower().startswith("arxiv:"):
        return "arxiv:" + key.split(":", 1)[1].strip()
    return bare_doi(key).lower()


def authors_of(record: dict[str, Any]) -> list[str]:
    raw = record.get("authors")
    if isinstance(raw, list):
        names = [one_line(item) for item in raw if isinstance(item, str) and one_line(item)]
        if names:
            return names
    first = record.get("first_author")
    if isinstance(first, str) and first.strip():
        return [one_line(first)]
    return []


def year_of(record: dict[str, Any]) -> str:
    year = record.get("year")
    if isinstance(year, bool) or year is None:
        return ""
    if isinstance(year, (int, float)):
        return str(int(year))
    return one_line(year)


def identifiers_of(record: dict[str, Any]) -> dict[str, str]:
    raw = record.get("identifiers")
    if not isinstance(raw, dict):
        raw = {}
    out: dict[str, str] = {}
    if raw.get("doi"):
        out["doi"] = bare_doi(str(raw["doi"]))
    if raw.get("pmid"):
        out["pmid"] = str(raw["pmid"]).strip()
    if raw.get("arxiv"):
        out["arxiv"] = str(raw["arxiv"]).strip()
    paper_id = record.get("id")
    if isinstance(paper_id, str) and paper_id.startswith("arxiv:") and "arxiv" not in out:
        out["arxiv"] = paper_id.split(":", 1)[1]
    return out


def cite_key(record: dict[str, Any]) -> str | None:
    ids = identifiers_of(record)
    if ids.get("doi"):
        return ids["doi"].lower()
    if ids.get("pmid"):
        return f"pmid:{ids['pmid']}"
    if ids.get("arxiv"):
        return f"arxiv:{ids['arxiv']}"
    return None


def display_key(record: dict[str, Any]) -> str:
    ids = identifiers_of(record)
    if ids.get("doi"):
        return ids["doi"]
    if ids.get("pmid"):
        return f"pmid:{ids['pmid']}"
    if ids.get("arxiv"):
        return f"arxiv:{ids['arxiv']}"
    return ""


def paper_from_item(item: object) -> dict[str, Any] | None:
    if not isinstance(item, dict):
        return None
    paper = item.get("paper") if isinstance(item.get("paper"), dict) else item
    if not isinstance(paper, dict):
        return None
    title = one_line(paper.get("title") or "")
    if not title:
        return None
    record = dict(paper)
    record["title"] = title
    return record


def load_records(text: str) -> list[dict[str, Any]]:
    obj = json.loads(text)
    items: list[object]
    if isinstance(obj, dict):
        data = obj.get("data")
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            items = data["items"]
        elif isinstance(data, dict) and data.get("title"):
            items = [data]
        elif isinstance(obj.get("items"), list):
            items = obj["items"]
        elif obj.get("title"):
            items = [obj]
        else:
            raise ValueError("unrecognized JSON shape")
    elif isinstance(obj, list):
        items = obj
    else:
        raise ValueError("unrecognized JSON shape")
    records: list[dict[str, Any]] = []
    for item in items:
        paper = paper_from_item(item)
        if paper is not None:
            records.append(paper)
    return records


def index_records(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for record in records:
        key = cite_key(record)
        if key and key not in index:
            index[key] = record
    return index


def cite_tokens(blob: str) -> list[str]:
    return [part.strip() for part in blob.split(";") if part.strip()]


def first_keys(draft: str) -> list[str]:
    seen: list[str] = []
    for match in CITE.finditer(draft):
        for token in cite_tokens(match.group(1)):
            key = normalize_key(token.lstrip("@"))
            if key and key not in seen:
                seen.append(key)
    return seen


def replace_cites(draft: str, number: dict[str, int]) -> str:
    def repl(match: re.Match[str]) -> str:
        nums = [str(number[normalize_key(token.lstrip("@"))]) for token in cite_tokens(match.group(1))]
        return "[" + ", ".join(nums) + "]"

    return CITE.sub(repl, draft)


def doi_or_url(record: dict[str, Any]) -> str:
    ids = identifiers_of(record)
    if ids.get("doi"):
        return f"https://doi.org/{ids['doi']}"
    if ids.get("pmid"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{ids['pmid']}/"
    if ids.get("arxiv"):
        return f"https://arxiv.org/abs/{ids['arxiv']}"
    return ""


def publication_type_of(record: dict[str, Any]) -> str:
    types = record.get("publication_types")
    if isinstance(types, list):
        names = [one_line(item) for item in types if isinstance(item, str) and one_line(item)]
        if names:
            return names[0]
    return ""


def citation_count_of(record: dict[str, Any]) -> str:
    counts = record.get("citation_counts")
    if isinstance(counts, list):
        for item in counts:
            if isinstance(item, dict) and item.get("value") is not None:
                return str(item["value"])
    return ""


def ref_line(n: int, record: dict[str, Any]) -> str:
    authors = ", ".join(authors_of(record))
    title = record["title"]
    venue = one_line(record.get("venue") or "")
    year = year_of(record)
    url = doi_or_url(record)
    ids = identifiers_of(record)
    head = ", ".join(part for part in (authors, title) if part)
    tail = ", ".join(part for part in (venue, year) if part)
    line = f"[{n}] {head}"
    if tail:
        line += ". " + tail
    if url:
        line += ". " + url
    elif ids.get("arxiv"):
        line += f". arXiv:{ids['arxiv']}"
    return line


def csv_row(record: dict[str, Any]) -> dict[str, str]:
    return {
        "题名": record["title"],
        "作者": ", ".join(authors_of(record)),
        "年份": year_of(record),
        "会议或期刊": one_line(record.get("venue") or ""),
        "DOI 或 URL": doi_or_url(record),
        "文献类型": publication_type_of(record),
        "被引次数": citation_count_of(record),
        "与本问题相关的要点": "",
    }


def compile_review(draft: str, records: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    index = index_records(records)
    keys = first_keys(draft)
    missing = [key for key in keys if key not in index]
    if missing:
        raise SystemExit("unknown keys: " + ", ".join(missing))
    number = {key: i for i, key in enumerate(keys, 1)}
    body = replace_cites(draft, number)
    if "[@" in body:
        raise SystemExit("unparsed [@] remains")
    ordered = [index[key] for key in keys]
    refs = "\n\n".join(ref_line(i, record) for i, record in enumerate(ordered, 1))
    text = body.rstrip() + "\n\n## 参考文献\n\n" + refs + "\n"
    return text, ordered


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fieldnames = [
        "题名",
        "作者",
        "年份",
        "会议或期刊",
        "DOI 或 URL",
        "文献类型",
        "被引次数",
        "与本问题相关的要点",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(csv_row(record))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile [@doi] draft against search/batch JSON into numbered review and evidence table."
    )
    parser.add_argument("--json", required=True, type=Path, dest="json_path")
    parser.add_argument("--draft", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--csv", type=Path)
    parser.add_argument("--keys", action="store_true", help="Print cite keys and titles, then exit.")
    args = parser.parse_args()
    records = load_records(args.json_path.read_text(encoding="utf-8"))
    if args.keys:
        for record in records:
            key = display_key(record)
            if key:
                print(f"{key}\t{record['title']}")
        return
    if args.draft is None or args.out is None:
        raise SystemExit("--draft and --out are required unless --keys")
    text, ordered = compile_review(args.draft.read_text(encoding="utf-8"), records)
    args.out.write_text(text, encoding="utf-8")
    if args.csv is not None:
        write_csv(args.csv, ordered)
    print("wrote", args.out, "count", len(ordered))


if __name__ == "__main__":
    main()
