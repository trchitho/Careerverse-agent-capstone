"""Generate deterministic production-minded CareerVerse domain datasets."""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "app" / "data"
SAFETY_NOTE = (
    "This recommendation is educational guidance only and does not guarantee "
    "employment outcomes."
)
ROADMAP_SAFETY_NOTE = (
    "This roadmap is educational guidance only and should be adapted to the "
    "learner's context."
)


def slugify(value: str) -> str:
    """Convert a human-readable value to a stable snake_case identifier."""
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return normalized.strip("_")


def write_json(filename: str, payload: Any) -> None:
    """Write deterministic UTF-8 JSON using the required formatting."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / filename).open("w", encoding="utf-8", newline="\n") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")
