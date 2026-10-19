from datetime import date
from pathlib import Path

import pytest

from src.frr.report import horizon_status
from src.frr.validation import read_jsonl

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_top_risk_box_carries_applicability_label():
    # The app renders the latest committed screen, labelled for today.
    latest = sorted((ROOT / "data" / "scores").glob("*/*.jsonl"))[-1]
    top = max(read_jsonl(latest), key=lambda row: float(row["disruption_probability_90d"]))
    status = horizon_status(top, date.today())
    label = "historical (horizon elapsed)" if status == "historical" else status.replace("_", " ")

    at = AppTest.from_file(str(ROOT / "streamlit_app.py")).run()
    assert not at.exception
    box = at.info[0].value
    assert "next 90 days" not in box
    assert f"window anchored at {top['as_of']}" in box
    assert f"applicability on {date.today()}: {label}" in box
