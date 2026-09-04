from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import render_cites as rc

SCRIPTS = Path(__file__).resolve().parent
RENDER = SCRIPTS / "render_cites.py"

SAMPLE = {
    "request_id": "t",
    "data": {
        "items": [
            {
                "title": "First paper",
                "year": 2025,
                "venue": "Venue A",
                "authors": ["Ann Doe", "Ben Roe"],
                "publication_types": ["review"],
                "identifiers": {"doi": "https://doi.org/10.1/aaa"},
                "citation_counts": [{"provider": "semantic_scholar", "value": 3}],
            },
            {
                "title": "Second paper",
                "year": 2024,
                "venue": "Venue B",
                "first_author": "Cara Lee",
                "identifiers": {"pmid": "12345"},
            },
        ]
    },
}


def compile_text(draft: str, records: object) -> tuple[str, list[dict]]:
    if isinstance(records, list):
        loaded = records
    else:
        loaded = rc.load_records(json.dumps(records))
    return rc.compile_review(draft, loaded)


def test_doi_first_appearance_and_csv(tmp_path: Path) -> None:
    json_path = tmp_path / "hits.json"
    json_path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    draft = tmp_path / "draft.md"
    draft.write_text(
        "先引后一篇[@pmid:12345]，再引前一篇[@10.1/aaa]。再一起[@10.1/aaa; @pmid:12345]。\n",
        encoding="utf-8",
    )
    records = rc.load_records(json_path.read_text(encoding="utf-8"))
    text, ordered = rc.compile_review(draft.read_text(encoding="utf-8"), records)
    assert "[@" not in text
    assert "先引后一篇[1]，再引前一篇[2]。再一起[2, 1]。" in text
    assert ordered[0]["title"] == "Second paper"
    assert ordered[1]["title"] == "First paper"
    assert "[1] Cara Lee, Second paper." in text
    assert "https://doi.org/10.1/aaa" in text
    csv_path = tmp_path / "evidence.csv"
    rc.write_csv(csv_path, ordered)
    rows = csv_path.read_text(encoding="utf-8").splitlines()
    assert rows[0].startswith("题名,作者,年份")
    assert "Second paper" in rows[1]
    assert "First paper" in rows[2]
    assert rows[1].endswith(",")


def test_unknown_key_fails() -> None:
    records = rc.load_records(json.dumps(SAMPLE))
    try:
        rc.compile_review("错键[@10.9/zzz]\n", records)
    except SystemExit as exc:
        assert "unknown keys" in str(exc)
    else:
        raise AssertionError("expected SystemExit")


def test_doi_internal_semicolon_is_one_key() -> None:
    records = [{"title": "Semi", "identifiers": {"doi": "10.1000/abc;def"}}]
    text, ordered = compile_text("见[@10.1000/abc;def]。\n", records)
    assert "见[1]。" in text
    assert ordered[0]["title"] == "Semi"


def test_multi_cite_semicolon_at() -> None:
    records = [
        {"title": "A", "identifiers": {"doi": "10.1000/aaa"}},
        {"title": "B", "identifiers": {"doi": "10.1000/bbb"}},
    ]
    text, _ = compile_text("见[@10.1000/aaa; @10.1000/bbb]。\n", records)
    assert "见[1, 2]。" in text


def test_multi_cite_extra_spaces() -> None:
    records = [
        {"title": "A", "identifiers": {"doi": "10.1000/aaa"}},
        {"title": "B", "identifiers": {"doi": "10.1000/bbb"}},
    ]
    text, _ = compile_text("见[@10.1000/aaa;  @10.1000/bbb]。\n", records)
    assert "见[1, 2]。" in text


def test_top_level_doi_id_fallback() -> None:
    records = [{"title": "Top", "id": "doi:10.1000/x"}]
    text, ordered = compile_text("见[@10.1000/x]。\n", records)
    assert "见[1]。" in text
    assert ordered[0]["title"] == "Top"


def test_identifiers_doi_beats_top_level_id() -> None:
    records = [
        {
            "title": "Nested",
            "id": "doi:10.1000/other",
            "identifiers": {"doi": "10.1000/real"},
        }
    ]
    text, _ = compile_text("见[@10.1000/real]。\n", records)
    assert "见[1]。" in text
    try:
        compile_text("见[@10.1000/other]。\n", records)
    except SystemExit as exc:
        assert "unknown keys" in str(exc)
    else:
        raise AssertionError("top-level id must not override identifiers.doi")


def test_empty_identifiers_doi_falls_back() -> None:
    records = [
        {
            "title": "Empty doi",
            "id": "arxiv:1706.03762",
            "identifiers": {"doi": "", "arxiv": "1706.03762"},
        }
    ]
    text, ordered = compile_text("见[@arxiv:1706.03762]。\n", records)
    assert "见[1]。" in text
    assert ordered[0]["title"] == "Empty doi"


def test_arxiv_without_doi() -> None:
    records = [
        {
            "title": "Attention",
            "id": "arxiv:1706.03762",
            "identifiers": {"arxiv": "1706.03762", "semantic_scholar": "abc"},
            "citation_counts": [{"provider": "semantic_scholar", "value": 191116}],
        }
    ]
    text, ordered = compile_text("见[@arxiv:1706.03762]。\n", records)
    assert "见[1]。" in text
    assert rc.citation_count_of(ordered[0]) == "191116"


def test_doi_preferred_over_pmid() -> None:
    records = [
        {
            "title": "Both",
            "id": "doi:10.1093/bib/bbad467",
            "identifiers": {"doi": "10.1093/bib/bbad467", "pmid": "38189543"},
        }
    ]
    text, _ = compile_text("见[@10.1093/bib/bbad467]。\n", records)
    assert "见[1]。" in text


def test_citation_provider_order_stable() -> None:
    record = {
        "title": "Counts",
        "identifiers": {"doi": "10.1/c"},
        "citation_counts": [
            {"provider": "crossref", "value": 1},
            {"provider": "semantic_scholar", "value": 9},
        ],
    }
    flipped = {
        "title": "Counts",
        "identifiers": {"doi": "10.1/c"},
        "citation_counts": [
            {"provider": "semantic_scholar", "value": 9},
            {"provider": "crossref", "value": 1},
        ],
    }
    assert rc.citation_count_of(record) == "9"
    assert rc.citation_count_of(flipped) == "9"


def test_citation_openalex_only() -> None:
    record = {
        "title": "OA",
        "identifiers": {"doi": "10.1/o"},
        "citation_counts": [{"provider": "openalex", "value": 7133}],
    }
    assert rc.citation_count_of(record) == "7133"


def test_citation_pubmed_when_no_higher() -> None:
    record = {
        "title": "Med",
        "identifiers": {"pmid": "1"},
        "citation_counts": [{"provider": "pubmed", "value": 4}],
    }
    assert rc.citation_count_of(record) == "4"


def test_citation_empty_or_unknown_provider() -> None:
    assert rc.citation_count_of({"citation_counts": []}) == ""
    assert rc.citation_count_of({"citation_counts": [{"provider": "openalex"}]}) == ""
    assert rc.citation_count_of({"citation_counts": [{"provider": "elsevier", "value": 8}]}) == ""
    assert rc.citation_count_of({}) == ""


def test_citation_numeric_string_and_null_fallback() -> None:
    record = {
        "citation_counts": [
            {"provider": "semantic_scholar", "value": None},
            {"provider": "openalex", "value": "12"},
        ]
    }
    assert rc.citation_count_of(record) == "12"


def test_cli_from_other_cwd(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    json_path = tmp_path / "hits.json"
    json_path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    cwd = tmp_path / "research"
    cwd.mkdir()
    keys = subprocess.run(
        [sys.executable, str(RENDER), "--json", str(json_path), "--keys"],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "10.1/aaa" in keys.stdout
    draft = tmp_path / "draft.md"
    out = tmp_path / "out.md"
    csv_path = tmp_path / "out.csv"
    draft.write_text("见[@10.1/aaa]。\n", encoding="utf-8")
    compiled = subprocess.run(
        [
            sys.executable,
            str(RENDER),
            "--json",
            str(json_path),
            "--draft",
            str(draft),
            "--out",
            str(out),
            "--csv",
            str(csv_path),
        ],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "count 1" in compiled.stdout
    assert "[1]" in out.read_text(encoding="utf-8")
    assert "First paper" in csv_path.read_text(encoding="utf-8")


def test_search_items_are_top_level_papers() -> None:
    payload = {
        "data": {
            "items": [
                {
                    "title": "Search hit",
                    "id": "doi:10.1/hit",
                    "identifiers": {"doi": "10.1/hit", "openalex": "W1"},
                    "citation_counts": [{"provider": "openalex", "value": 5}],
                }
            ]
        }
    }
    text, ordered = compile_text("见[@10.1/hit]。\n", payload)
    assert "见[1]。" in text
    assert rc.citation_count_of(ordered[0]) == "5"


def run_all() -> None:
    from tempfile import TemporaryDirectory

    tests = [
        test_unknown_key_fails,
        test_doi_internal_semicolon_is_one_key,
        test_multi_cite_semicolon_at,
        test_multi_cite_extra_spaces,
        test_top_level_doi_id_fallback,
        test_identifiers_doi_beats_top_level_id,
        test_empty_identifiers_doi_falls_back,
        test_arxiv_without_doi,
        test_doi_preferred_over_pmid,
        test_citation_provider_order_stable,
        test_citation_openalex_only,
        test_citation_pubmed_when_no_higher,
        test_citation_empty_or_unknown_provider,
        test_citation_numeric_string_and_null_fallback,
        test_search_items_are_top_level_papers,
    ]
    with TemporaryDirectory() as folder:
        root = Path(folder)
        test_doi_first_appearance_and_csv(root)
        test_cli_from_other_cwd(root / "cli")
    for fn in tests:
        fn()
    print("ok", 2 + len(tests))


if __name__ == "__main__":
    run_all()
