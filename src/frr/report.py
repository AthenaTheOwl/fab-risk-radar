from __future__ import annotations

import json
from pathlib import Path

from .models import EvidenceItem, ScoreRow


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def render_summary(scores: list[dict[str, object]], evidence: list[dict[str, object]]) -> str:
    """Build a ranked, human-readable summary from committed score + evidence rows."""
    evidence_by_id = {str(item["evidence_id"]): item for item in evidence}
    ranked = sorted(
        scores,
        key=lambda row: float(row["disruption_probability_90d"]),
        reverse=True,
    )
    as_of = str(ranked[0]["as_of"]) if ranked else "?"
    slice_name = str(ranked[0]["slice"]) if ranked else "?"
    high = [r for r in ranked if str(r["risk_band"]) == "high"]

    lines = [
        f"FabRiskRADAR - {slice_name} - 90-day disruption screen (as of {as_of})",
        f"{len(ranked)} nodes scored, {len(high)} in the high band. "
        "Higher probability = more likely to constrain capacity in the next 90 days.",
        "",
        f"  {'rank':<4} {'prob':>6}  {'band':<6} node",
        f"  {'-' * 4} {'-' * 6}  {'-' * 6} {'-' * 40}",
    ]
    for index, row in enumerate(ranked, start=1):
        prob = float(row["disruption_probability_90d"])
        band = str(row["risk_band"])
        name = str(row["node_name"])
        region = str(row["region"])
        lines.append(f"  {index:<4} {prob:>6.3f}  {band:<6} {name} ({region})")

    if ranked:
        top = ranked[0]
        first_id = list(top["evidence_ids"])[0]
        anchor = evidence_by_id.get(str(first_id))
        lines.append("")
        lines.append(f"top risk: {top['node_name']} ({top['region']}) at "
                     f"{float(top['disruption_probability_90d']):.0%} 90-day disruption probability")
        if anchor is not None:
            lines.append(f"  anchored on {anchor['source_kind']}: {anchor['source_url']}")

    return "\n".join(lines)


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
