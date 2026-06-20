from __future__ import annotations

import json
from pathlib import Path

from .models import EvidenceItem, ScoreRow


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def render_markdown(path: Path, scores: list[ScoreRow], evidence: list[EvidenceItem]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    evidence_by_id = {item.evidence_id: item for item in evidence}
    lines = [
        f"# FabRiskRADAR substrate-osat report - {scores[0].as_of[:7]}",
        "",
        "Ranked 90-day disruption view for ABF substrate and advanced-packaging OSAT nodes.",
        "Scores are fixture-backed in v0.1 and require three public evidence items per node.",
        "",
        "## ranked nodes",
        "",
    ]
    for index, row in enumerate(scores, start=1):
        lines.extend(
            [
                f"### {index}. {row.node_name} ({row.region})",
                "",
                f"- probability: {row.disruption_probability_90d:.3f}",
                f"- band: {row.risk_band}",
                f"- node kind: {row.node_kind}",
                "- evidence:",
            ]
        )
        for evidence_id in row.evidence_ids:
            item = evidence_by_id[evidence_id]
            lines.append(f"  - {item.source_kind}: {item.claim} ({item.source_url})")
        lines.append("")
    lines.extend(
        [
            "## methodology",
            "",
            "The v0.1 rubric combines node type, tier, and evidence-source mix. "
            "It is a deterministic screening score, not a forecast model.",
            "",
            "- schema: `schemas/disruption-score.schema.json`",
            "- evidence schema: `schemas/evidence-item.schema.json`",
            "- decision: `decisions/DEC-FRR-001-evidence-rubric.md`",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
