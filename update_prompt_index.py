#!/usr/bin/env python3
"""
Generate prompts/prompts_index.json from front matters in docs/*/text.md.
Run this after a successful build to keep the prompt inventory in sync.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:  # pragma: no cover - handled at runtime
    sys.exit("PyYAML is required. Run `pip install pyyaml`.")

ROOT = Path(__file__).parent
DOCS_DIR = ROOT / "docs"
OUTPUT_PATH = ROOT / "prompts" / "prompts_index.json"

FIELDS = (
    "prompt",
    "resume",
    "langue",
    "niveau",
    "longueur",
    "genre",
    "drapeau",
    "voix_variant",
    "date_generation",
    "titre_nl",
    "mots_cles_nl",
)


def _strip_markdown_bold(text: str) -> str:
    """Remove simple * / ** markers that break YAML parsing."""

    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    return text


class NoTimestampSafeLoader(yaml.SafeLoader):
    pass


# Disable automatic timestamp -> datetime conversion to keep strings in JSON
for ch, resolvers in list(NoTimestampSafeLoader.yaml_implicit_resolvers.items()):
    NoTimestampSafeLoader.yaml_implicit_resolvers[ch] = [
        (tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:timestamp"
    ]


def extract_front_matter(path: Path) -> Dict[str, Any]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}

    front = _strip_markdown_bold(parts[1])

    try:
        data = yaml.load(front, Loader=NoTimestampSafeLoader)
    except yaml.YAMLError as exc:  # pragma: no cover - only logs
        print(f"Skipping {path}: invalid YAML front matter ({exc})", file=sys.stderr)
        return {}

    if not data:
        return {}

    # Normalize datetimes/dates to ISO strings for JSON serialization
    for key, value in list(data.items()):
        if isinstance(value, datetime):
            data[key] = value.isoformat(sep=" ", timespec="seconds")
        elif isinstance(value, date):
            data[key] = value.isoformat()

    return data


def build_record(text_path: Path) -> Dict[str, Any]:
    meta = extract_front_matter(text_path)
    record = {
        "id": text_path.parent.name,
        "source": str(text_path.relative_to(ROOT)),
    }
    for field in FIELDS:
        record[field] = meta.get(field)
    return record


def main() -> None:
    text_files = sorted(DOCS_DIR.glob("*/text.md"))
    records = [build_record(path) for path in text_files]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(records)} entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
