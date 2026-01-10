#!/usr/bin/env python3
"""
Generate a simple one-liner list from prompts_index.json.
Output: prompts/PROMPTS.txt with format: NIVEAU | PROMPT
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent
INDEX_PATH = ROOT / "prompts" / "prompts_index.json"
OUTPUT_PATH = ROOT / "prompts" / "PROMPTS.txt"

if not INDEX_PATH.exists():
    print(f"❌ {INDEX_PATH} not found. Run `python3 update_prompt_index.py` first.")
    exit(1)

records = json.loads(INDEX_PATH.read_text(encoding="utf-8"))

# Sort by date_generation (descending, most recent first)
records.sort(key=lambda r: r.get("date_generation") or "", reverse=True)

lines = []
for record in records:
    niveau = record.get("niveau") or "?"
    prompt = record.get("prompt") or record.get("resume") or "?"
    lines.append(f"{niveau} | {prompt}")

OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
print(f"✅ {len(lines)} prompts -> {OUTPUT_PATH}")
