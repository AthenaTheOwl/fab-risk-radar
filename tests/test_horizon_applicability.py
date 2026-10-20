import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

from src.frr import cli
from src.frr.cli import screen_as_of
from src.frr.report import horizon_status, render_summary

ROOT = Path(__file__).resolve().parents[1]


def test_window_boundary_is_exclusive_and_preserves_historical_value():
    row = {"as_of": "2026-06-30", "horizon_days": 90}
    assert horizon_status(row, date(2026, 6, 29)) == "not_started"
    assert horizon_status(row, date(2026, 9, 27)) == "within_window"
    assert horizon_status(row, date(2026, 9, 28)) == "historical"
    assert row == {"as_of": "2026-06-30", "horizon_days": 90}


def test_elapsed_screen_is_labeled_in_readable_output():
    row = {
        "as_of": "2026-06-30",
        "horizon_days": 90,
        "disruption_probability_90d": 0.5,
        "slice": "synthetic",
        "risk_band": "watch",
        "node_name": "synthetic",
        "region": "test",
        "evidence_ids": ["e"],
    }
    output = render_summary([row], [], evaluated_on=date(2026, 10, 18))
    assert "1/1 row(s) historical" in output
    assert "not calibrated probabilities" in output


def test_show_reports_a_rubric_score_not_a_percent_chance():
    result = _show("--evaluated-on", "2026-10-19")
    assert result.returncode == 0, result.stderr
    assert "  rank  score  band   node" in result.stdout
    assert (
        "top risk: Ibiden Ogaki ABF substrate cluster (Japan) at rubric score 0.58 "
        "for the 90-day window from 2026-06-30\n"
    ) in result.stdout
    assert "%" not in result.stdout
    assert "disruption probability" not in result.stdout


@pytest.mark.parametrize("horizon", [0, -1, True, 90.5, "90", float("nan")])
def test_invalid_horizon_cannot_appear_current(horizon):
    with pytest.raises(ValueError, match="positive"):
        horizon_status({"as_of": "2026-06-30", "horizon_days": horizon}, date(2026, 7, 1))


def _show(*args):
    return subprocess.run(
        [sys.executable, "-m", "frr", "show", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


@pytest.mark.parametrize(
    "evaluated_on, expected",
    [
        ("2026-06-29", "2026-06-29: 0/3 row(s) historical (horizon elapsed), 3/3 not started"),
        ("2026-07-15", "2026-07-15: 0/3 row(s) historical (horizon elapsed).\n"),
        ("2026-09-28", "2026-09-28: 3/3 row(s) historical (horizon elapsed).\n"),
    ],
)
def test_show_pins_evaluation_date(evaluated_on, expected):
    result = _show("--evaluated-on", evaluated_on)
    assert result.returncode == 0, result.stderr
    assert expected in result.stdout


@pytest.mark.parametrize("value", ["2026-13-01", "20261019", "2026-W43-1", "2026-6-30"])
def test_show_rejects_malformed_evaluation_date(value):
    result = _show("--evaluated-on", value)
    assert result.returncode == 2
    assert "expected YYYY-MM-DD" in result.stderr


@pytest.mark.parametrize(
    "month, expected",
    [
        ("2026-06", "2026-06-30"),
        ("2026-07", "2026-07-30"),
        ("2026-02", "2026-02-28"),
        ("2028-02", "2028-02-29"),
    ],
)
def test_screen_as_of_is_a_real_date(month, expected):
    assert screen_as_of(month) == expected


def test_build_report_writes_a_real_as_of_for_february(tmp_path, monkeypatch):
    (tmp_path / "data" / "evidence").mkdir(parents=True)
    shutil.copy(ROOT / "data" / "chip_graph_export.json", tmp_path / "data")
    shutil.copy(
        ROOT / "data" / "evidence" / "2026-06-substrate-osat.csv",
        tmp_path / "data" / "evidence" / "2026-02-substrate-osat.csv",
    )
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    score_path, _ = cli.build_report("2026-02", "substrate-osat")
    rows = [json.loads(line) for line in score_path.read_text(encoding="utf-8").splitlines()]
    assert rows
    assert {row["as_of"] for row in rows} == {"2026-02-28"}
