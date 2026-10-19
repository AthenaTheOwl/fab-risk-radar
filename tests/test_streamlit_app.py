import datetime
from datetime import date, timedelta
from pathlib import Path

import pytest

from src.frr.validation import read_jsonl

AppTest = pytest.importorskip("streamlit.testing.v1").AppTest

ROOT = Path(__file__).resolve().parents[1]

# The app renders the latest committed screen; its top row anchors the window.
LATEST = sorted((ROOT / "data" / "scores").glob("*/*.jsonl"))[-1]
TOP = max(read_jsonl(LATEST), key=lambda row: float(row["disruption_probability_90d"]))
AS_OF = date.fromisoformat(TOP["as_of"])
HORIZON = timedelta(days=TOP["horizon_days"])


@pytest.mark.parametrize(
    "today, label",
    [
        (AS_OF - timedelta(days=1), "not started"),
        (AS_OF, "within window"),
        (AS_OF + HORIZON - timedelta(days=1), "within window"),
        (AS_OF + HORIZON, "historical (horizon elapsed)"),
    ],
    ids=str,
)
def test_top_risk_box_carries_applicability_label(monkeypatch, today, label):
    class FixedDate(date):
        @classmethod
        def today(cls):
            return today

    # streamlit_app.py runs `from datetime import date` on each run.
    monkeypatch.setattr(datetime, "date", FixedDate)
    at = AppTest.from_file(str(ROOT / "streamlit_app.py")).run()
    assert not at.exception
    box = at.info[0].value
    assert "next 90 days" not in box
    assert f"window anchored at {TOP['as_of']}" in box
    assert f"applicability on {today.isoformat()}: {label}." in box
