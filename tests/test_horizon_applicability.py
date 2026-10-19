from datetime import date

import pytest

from src.frr.report import horizon_status, render_summary


def test_window_boundary_is_exclusive_and_preserves_historical_value():
    row = {"as_of": "2026-06-30", "horizon_days": 90}
    assert horizon_status(row, date(2026, 6, 29)) == "not_started"
    assert horizon_status(row, date(2026, 9, 27)) == "within_window"
    assert horizon_status(row, date(2026, 9, 28)) == "historical"
    assert row == {"as_of": "2026-06-30", "horizon_days": 90}


def test_elapsed_screen_is_labeled_in_readable_output():
    row = {"as_of": "2026-06-30", "horizon_days": 90, "disruption_probability_90d": 0.5, "slice": "synthetic", "risk_band": "watch", "node_name": "synthetic", "region": "test", "evidence_ids": ["e"]}
    output = render_summary([row], [], evaluated_on=date(2026, 10, 18))
    assert "1/1 row(s) historical" in output
    assert "not calibrated live forecasts" in output


@pytest.mark.parametrize("horizon", [0, -1, True, 90.5, "90", float("nan")])
def test_invalid_horizon_cannot_appear_current(horizon):
    with pytest.raises(ValueError, match="positive"):
        horizon_status({"as_of": "2026-06-30", "horizon_days": horizon}, date(2026, 7, 1))
