from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.frr.evidence import evidence_by_node, load_evidence
from src.frr.graph import load_graph, select_slice
from src.frr.scoring import score_nodes
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


def test_report_rows_are_json_objects() -> None:
    rows = read_jsonl(ROOT / "data" / "scores" / "substrate-osat" / "2026-06.jsonl")
    assert rows
    assert all(0 <= row["disruption_probability_90d"] <= 1 for row in rows)

