from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).parents[1]
SKILLS_ROOT = ROOT / "skills"
MANIFEST_PATH = ROOT / "manifest.json"
SEMVER = re.compile(r"\d+\.\d+\.\d+")


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise AssertionError("SKILL.md frontmatter is not closed")
    return parts[1]


def field(block: str, name: str) -> str:
    match = re.search(rf"(?m)^{re.escape(name)}:\s*(.+?)\s*$", block)
    if not match:
        raise AssertionError(f"missing frontmatter field: {name}")
    return match.group(1).strip().strip('"\'')


def metadata_version(block: str) -> str:
    match = re.search(r"(?m)^\s{2}version:\s*(.+?)\s*$", block)
    if not match:
        raise AssertionError("missing frontmatter metadata.version")
    return match.group(1).strip().strip('"\'')


def validate_links(skill_file: Path, text: str) -> None:
    for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#")):
            continue
        path = (skill_file.parent / target.split("#", 1)[0]).resolve()
        if not path.exists():
            raise AssertionError(f"missing local reference from {skill_file}: {target}")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert SEMVER.fullmatch(manifest["version"])
    assert manifest["requires_cli"]

    folders = {path.parent.name for path in SKILLS_ROOT.glob("*/SKILL.md")}
    versions = manifest["skills"]
    assert set(versions) == folders, (set(versions), folders)

    for name, expected_version in sorted(versions.items()):
        skill_file = SKILLS_ROOT / name / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        block = frontmatter(text)
        assert field(block, "name") == name
        assert field(block, "description")
        assert metadata_version(block) == expected_version
        assert SEMVER.fullmatch(expected_version)
        assert "TODO" not in text
        validate_links(skill_file, text)

    print(
        json.dumps(
            {
                "ok": True,
                "pack": manifest["name"],
                "version": manifest["version"],
                "skills": sorted(versions),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
