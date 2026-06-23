"""FabRiskRADAR — live demo (Streamlit Community Cloud).

Mirrors `python frr.py show`: the committed ranked 90-day disruption screen for
tier-2/3 semiconductor nodes (ABF substrate + advanced-packaging OSAT). Reads the
committed score + evidence artifacts directly. No network, no secrets — runs
entirely off the committed fixtures under data/.

Deploy: Streamlit Community Cloud -> New app -> repo AthenaTheOwl/fab-risk-radar,
branch main, main file streamlit_app.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
SCORES_DIR = REPO / "data" / "scores"
EVIDENCE_DIR = REPO / "data" / "evidence"


def read_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def latest_scores() -> tuple[list[dict], str, str]:
    files = sorted(SCORES_DIR.glob("*/*.jsonl"))
    if not files:
        return [], "", ""
    path = files[-1]
    return read_jsonl(path), path.parent.name, path.stem


def load_evidence(slice_name: str, month: str) -> dict[str, dict]:
    path = EVIDENCE_DIR / f"{month}-{slice_name}.jsonl"
    if not path.exists():
        return {}
    return {str(item["evidence_id"]): item for item in read_jsonl(path)}


st.set_page_config(page_title="FabRiskRADAR — 90-day disruption screen", layout="wide")
st.title("FabRiskRADAR")
st.caption(
    "ranked 90-day disruption screen for tier-2/3 semiconductor nodes — ABF "
    "substrate and advanced-packaging OSAT — each score backed by three public "
    "evidence items."
)

scores, slice_name, month = latest_scores()
if not scores:
    st.warning("no committed scores found under data/scores/*/*.jsonl")
    st.stop()

evidence = load_evidence(slice_name, month)
ranked = sorted(
    scores, key=lambda r: float(r["disruption_probability_90d"]), reverse=True
)
as_of = str(ranked[0].get("as_of", "?"))
high = [r for r in ranked if str(r["risk_band"]) == "high"]

st.subheader(f"{slice_name} — as of {as_of}")

c1, c2, c3 = st.columns(3)
c1.metric("nodes scored", len(ranked))
c2.metric("high band", len(high))
c3.metric(
    "top probability",
    f"{float(ranked[0]['disruption_probability_90d']):.0%}",
    help="highest 90-day disruption probability in the screen",
)

bands = ["all"] + sorted({str(r["risk_band"]) for r in ranked})
band_pick = st.selectbox("filter by risk band", bands, index=0)
shown = ranked if band_pick == "all" else [r for r in ranked if str(r["risk_band"]) == band_pick]

st.dataframe(
    [
        {
            "rank": ranked.index(r) + 1,
            "probability": round(float(r["disruption_probability_90d"]), 3),
            "band": r.get("risk_band"),
            "node": r.get("node_name"),
            "region": r.get("region"),
            "kind": r.get("node_kind"),
            "evidence": len(r.get("evidence_ids", [])),
        }
        for r in shown
    ],
    use_container_width=True,
    hide_index=True,
)

top = ranked[0]
st.info(
    f"**top risk:** {top['node_name']} ({top['region']}) at "
    f"{float(top['disruption_probability_90d']):.0%} 90-day disruption probability "
    f"— higher probability = more likely to constrain capacity in the next 90 days."
)

with st.expander("evidence for the top-risk node"):
    if not evidence:
        st.caption("no evidence file alongside this screen.")
    for ev_id in top.get("evidence_ids", []):
        item = evidence.get(str(ev_id))
        if item is None:
            st.markdown(f"- `{ev_id}` (evidence row not found)")
            continue
        st.markdown(
            f"- **{item.get('source_kind')}**: {item.get('claim')}  \n"
            f"  source: {item.get('source_url')}"
        )

st.caption(
    "v0.1 ships one substrate-osat fixture month. scoring lives in `src/frr/`; "
    "this page reads the committed `data/scores/` + `data/evidence/` artifacts. "
    "repo: github.com/AthenaTheOwl/fab-risk-radar"
)
