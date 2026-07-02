from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.frr.evidence import evidence_by_node, load_evidence
from src.frr.graph import load_graph, select_slice
from src.frr.report import render_summary, write_jsonl
from src.frr.scoring import risk_band, score_nodes
from src.frr.validation import read_jsonl, validate_traceability

ROOT = Path(__file__).resolve().parents[1]


def test_graph_slice_selects_substrate_and_osat_nodes() -> None:
    graph = load_graph(ROOT / "data" / "chip_graph_export.json")
    nodes = select_slice(graph["nodes"], "substrate-osat")
    assert {node["node_kind"] for node in nodes} == {
        "abf-substrate",
        "advanced-packaging-osat",
    }


def test_scoring_requires_three_evidence_items() -> None:
    graph = load_graph(ROOT / "data" / "chip_graph_export.json")
    evidence = load_evidence(ROOT / "data" / "evidence" / "2026-06-substrate-osat.csv")
    scores = score_nodes(select_slice(graph["nodes"], "substrate-osat"), evidence_by_node(evidence), "2026-06-30")
    assert len(scores) == 3
    assert all(len(row.evidence_ids) >= 3 for row in scores)
    assert scores[0].disruption_probability_90d >= scores[-1].disruption_probability_90d


def test_cli_builds_report_and_jsonl() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "frr", "score", "--slice", "substrate-osat", "--month", "2026-06"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    score_path = ROOT / payload["score_path"]
    report_path = ROOT / payload["report_path"]
    assert score_path.is_file()
    assert report_path.is_file()
    validate_traceability(score_path, ROOT / "data" / "evidence" / "2026-06-substrate-osat.jsonl")


def test_cli_show_prints_ranked_summary() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "frr", "show"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    out = result.stdout
    assert "90-day disruption screen" in out
    assert "Ibiden Ogaki ABF substrate cluster" in out
    assert "top risk:" in out
    # ranked highest-probability node appears before lowest
    assert out.index("Ibiden Ogaki") < out.index("ASE Kaohsiung")


def test_report_rows_are_json_objects() -> None:
    rows = read_jsonl(ROOT / "data" / "scores" / "substrate-osat" / "2026-06.jsonl")
    assert rows
    assert all(0 <= row["disruption_probability_90d"] <= 1 for row in rows)


# The engine is fixture-backed in v0.1, so its output is a fixed golden master.
# These characterization tests pin the current numbers/bands so any change to the
# scoring weights, the band cutoffs, the traceability guard, or the summary count
# fails the suite instead of silently producing a different screen.

# probability -> expected band; locks both risk_band cutoffs (0.55 high, 0.35 watch).
_BAND_CASES = [
    (0.58, "high"),
    (0.55, "high"),
    (0.51, "watch"),
    (0.35, "watch"),
    (0.34, "low"),
]


@pytest.mark.parametrize("probability, expected", _BAND_CASES)
def test_risk_band_cutoffs_are_pinned(probability: float, expected: str) -> None:
    assert risk_band(probability) == expected


def _committed_scores() -> list:
    graph = load_graph(ROOT / "data" / "chip_graph_export.json")
    evidence = load_evidence(ROOT / "data" / "evidence" / "2026-06-substrate-osat.csv")
    return score_nodes(
        select_slice(graph["nodes"], "substrate-osat"),
        evidence_by_node(evidence),
        "2026-06-30",
    )


def test_score_nodes_pins_probability_and_band_per_node() -> None:
    # Golden master over SOURCE_WEIGHTS + NODE_BASE + risk_band for the
    # committed evidence set. Row order is by descending probability.
    scores = _committed_scores()
    actual = [
        (row.node_id, row.disruption_probability_90d, row.risk_band) for row in scores
    ]
    assert actual == [
        ("frr-node-abf-ibiden-ogaki", 0.58, "high"),
        ("frr-node-abf-unimicron-taoyuan", 0.55, "high"),
        ("frr-node-osat-ase-kaohsiung", 0.51, "watch"),
    ]


def test_committed_scores_match_engine_output() -> None:
    # The committed golden JSONL must equal what the engine produces today,
    # row-by-row on node_id -> probability + band.
    engine = {
        row.node_id: (row.disruption_probability_90d, row.risk_band)
        for row in _committed_scores()
    }
    committed = read_jsonl(ROOT / "data" / "scores" / "substrate-osat" / "2026-06.jsonl")
    assert {
        str(row["node_id"]): (row["disruption_probability_90d"], row["risk_band"])
        for row in committed
    } == engine


def test_validate_traceability_flags_missing_evidence(tmp_path: Path) -> None:
    score_path = tmp_path / "scores.jsonl"
    evidence_path = tmp_path / "evidence.jsonl"
    write_jsonl(
        score_path,
        [
            {
                "node_id": "frr-node-x",
                "evidence_ids": ["ev-1", "ev-2", "ev-missing"],
            }
        ],
    )
    write_jsonl(
        evidence_path,
        [{"evidence_id": "ev-1"}, {"evidence_id": "ev-2"}],
    )
    with pytest.raises(ValueError, match="ev-missing"):
        validate_traceability(score_path, evidence_path)


def test_summary_reports_two_high_band_nodes() -> None:
    scores = read_jsonl(ROOT / "data" / "scores" / "substrate-osat" / "2026-06.jsonl")
    evidence = read_jsonl(ROOT / "data" / "evidence" / "2026-06-substrate-osat.jsonl")
    summary = render_summary(scores, evidence)
    # Committed screen has exactly two 'high' band nodes.
    assert "2 in the high band" in summary

