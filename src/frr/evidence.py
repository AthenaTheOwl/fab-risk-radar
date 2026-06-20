from __future__ import annotations

import csv
from pathlib import Path

from .models import EvidenceItem


def load_evidence(path: Path) -> list[EvidenceItem]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    items: list[EvidenceItem] = []
    for row in rows:
        items.append(
            EvidenceItem(
                evidence_id=row["evidence_id"],
                node_id=row["node_id"],
                source_kind=row["source_kind"],
                source_url=row["source_url"],
                extracted_on=row["extracted_on"],
                claim=row["claim"],
            )
        )
    return items


def evidence_by_node(items: list[EvidenceItem]) -> dict[str, list[EvidenceItem]]:
    grouped: dict[str, list[EvidenceItem]] = {}
    for item in items:
        grouped.setdefault(item.node_id, []).append(item)
    return grouped

