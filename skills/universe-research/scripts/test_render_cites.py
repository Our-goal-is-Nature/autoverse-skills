from __future__ import annotations

import json
from pathlib import Path

import render_cites as rc

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


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as folder:
        test_doi_first_appearance_and_csv(Path(folder))
    test_unknown_key_fails()
    print("ok")
