from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def validate_traceability(score_path: Path, evidence_path: Path) -> None:
    scores = read_jsonl(score_path)
    evidence = read_jsonl(evidence_path)
    evidence_ids = {str(item["evidence_id"]) for item in evidence}
    for row in scores:
        ids = row.get("evidence_ids", [])
        if not isinstance(ids, list) or len(ids) < 3:
            raise ValueError(f"{row.get('node_id')} has fewer than 3 evidence ids")
        missing = [item for item in ids if item not in evidence_ids]
        if missing:
            raise ValueError(f"{row.get('node_id')} references missing evidence {missing}")

