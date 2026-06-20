from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    node_id: str
    source_kind: str
    source_url: str
    extracted_on: str
    claim: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class ScoreRow:
    node_id: str
    node_name: str
    node_kind: str
    region: str
    slice: str
    as_of: str
    horizon_days: int
    disruption_probability_90d: float
    risk_band: str
    evidence_ids: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

