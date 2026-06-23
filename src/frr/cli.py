from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evidence import evidence_by_node, load_evidence
from .graph import load_graph, select_slice
from .report import render_markdown, render_summary, write_jsonl
from .scoring import score_nodes
from .validation import read_jsonl, validate_traceability

ROOT = Path(__file__).resolve().parents[2]


def build_report(month: str, slice_name: str) -> tuple[Path, Path]:
    graph = load_graph(ROOT / "data" / "chip_graph_export.json")
    evidence_csv = ROOT / "data" / "evidence" / f"{month}-{slice_name}.csv"
    evidence = load_evidence(evidence_csv)
    nodes = select_slice(graph["nodes"], slice_name)
    scores = score_nodes(nodes, evidence_by_node(evidence), f"{month}-30")
    score_path = ROOT / "data" / "scores" / slice_name / f"{month}.jsonl"
    evidence_path = ROOT / "data" / "evidence" / f"{month}-{slice_name}.jsonl"
    report_path = ROOT / "reports" / f"{month}-{slice_name}.md"
    write_jsonl(score_path, [row.to_dict() for row in scores])
    write_jsonl(evidence_path, [item.to_dict() for item in evidence])
    render_markdown(report_path, scores, evidence)
    validate_traceability(score_path, evidence_path)
    return score_path, report_path


def validate_reports() -> None:
    for score_path in (ROOT / "data" / "scores").glob("*/*.jsonl"):
        month = score_path.stem
        slice_name = score_path.parent.name
        evidence_path = ROOT / "data" / "evidence" / f"{month}-{slice_name}.jsonl"
        validate_traceability(score_path, evidence_path)


def show_summary(slice_name: str = "substrate-osat", month: str = "2026-06") -> str:
    score_path = ROOT / "data" / "scores" / slice_name / f"{month}.jsonl"
    evidence_path = ROOT / "data" / "evidence" / f"{month}-{slice_name}.jsonl"
    scores = read_jsonl(score_path)
    evidence = read_jsonl(evidence_path)
    return render_summary(scores, evidence)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="frr")
    sub = parser.add_subparsers(dest="command", required=True)
    score = sub.add_parser("score")
    score.add_argument("--slice", default="substrate-osat")
    score.add_argument("--month", default="2026-06")
    sub.add_parser("validate")
    show = sub.add_parser("show", help="print the committed ranked disruption screen")
    show.add_argument("--slice", default="substrate-osat")
    show.add_argument("--month", default="2026-06")
    args = parser.parse_args(argv)
    if args.command == "show":
        print(show_summary(args.slice, args.month))
        return 0
    if args.command == "score":
        score_path, report_path = build_report(args.month, args.slice)
        print(
            json.dumps(
                {
                    "score_path": score_path.relative_to(ROOT).as_posix(),
                    "report_path": report_path.relative_to(ROOT).as_posix(),
                },
                sort_keys=True,
            )
        )
        return 0
    validate_reports()
    print("valid: reports")
    return 0

