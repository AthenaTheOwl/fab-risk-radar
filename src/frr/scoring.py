from __future__ import annotations

from typing import Any

from .models import EvidenceItem, ScoreRow

SOURCE_WEIGHTS = {
    "filing": 0.08,
    "trade-data": 0.07,
    "manual": 0.05,
    "news": 0.04,
    "imagery": 0.04,
}

NODE_BASE = {
    "abf-substrate": 0.32,
    "advanced-packaging-osat": 0.28,
}


def risk_band(probability: float) -> str:
    if probability >= 0.55:
        return "high"
    if probability >= 0.35:
        return "watch"
    return "low"


def score_node(node: dict[str, Any], evidence: list[EvidenceItem], as_of: str) -> ScoreRow:
    if len(evidence) < 3:
        raise ValueError(f"{node['node_id']} has fewer than 3 evidence items")
    base = NODE_BASE.get(str(node["node_kind"]), 0.20)
    source_score = sum(SOURCE_WEIGHTS.get(item.source_kind, 0.02) for item in evidence[:5])
    tier_score = max(0.0, (4 - int(node["tier"])) * 0.03)
    probability = min(0.85, round(base + source_score + tier_score, 3))
    return ScoreRow(
        node_id=str(node["node_id"]),
        node_name=str(node["name"]),
        node_kind=str(node["node_kind"]),
        region=str(node["region"]),
        slice="substrate-osat",
        as_of=as_of,
        horizon_days=90,
        disruption_probability_90d=probability,
        risk_band=risk_band(probability),
        evidence_ids=[item.evidence_id for item in evidence],
    )


def score_nodes(
    nodes: list[dict[str, Any]], evidence_by_node_id: dict[str, list[EvidenceItem]], as_of: str
) -> list[ScoreRow]:
    rows = [
        score_node(node, evidence_by_node_id.get(str(node["node_id"]), []), as_of)
        for node in nodes
    ]
    return sorted(rows, key=lambda row: row.disruption_probability_90d, reverse=True)

