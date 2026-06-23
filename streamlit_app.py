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
import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parent
SCORES_DIR = REPO / "data" / "scores"
EVIDENCE_DIR = REPO / "data" / "evidence"

# make the real package importable on Streamlit Cloud (src/ layout)
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from src.frr.models import EvidenceItem  # noqa: E402
from src.frr.scoring import (  # noqa: E402
    NODE_BASE,
    SOURCE_WEIGHTS,
    risk_band,
    score_node,
)


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

st.divider()
st.header("score a node yourself")
st.caption(
    "this drives the real engine — `src/frr/scoring.py:score_node` — not a lookup. "
    "set the node kind, tier, and the public evidence you have; the same function "
    "the monthly screen uses recomputes the 90-day disruption probability live."
)

kinds = list(NODE_BASE)
source_kinds = list(SOURCE_WEIGHTS)

ic1, ic2 = st.columns(2)
with ic1:
    pick_kind = st.selectbox(
        "node kind",
        kinds,
        help="abf-substrate carries a higher base than advanced-packaging-osat",
    )
    pick_tier = st.slider(
        "tier",
        min_value=1,
        max_value=4,
        value=2,
        help="lower tier (closer to 1) adds more probability — bigger upstream chokepoint",
    )
with ic2:
    st.markdown("**evidence you've gathered** (need at least 3; first 5 count)")
    chosen: list[str] = []
    for i in range(5):
        default = source_kinds[i % len(source_kinds)] if i < 3 else "(none)"
        sel = st.selectbox(
            f"evidence #{i + 1} source kind",
            ["(none)"] + source_kinds,
            index=(["(none)"] + source_kinds).index(default),
            key=f"ev_kind_{i}",
        )
        if sel != "(none)":
            chosen.append(sel)

if len(chosen) < 3:
    st.warning(
        f"the engine requires at least 3 evidence items — you have {len(chosen)}. "
        "add more to score."
    )
else:
    node = {
        "node_id": "frr-node-user",
        "name": "your node",
        "node_kind": pick_kind,
        "region": "user-supplied",
        "tier": pick_tier,
    }
    user_evidence = [
        EvidenceItem(
            evidence_id=f"user-ev-{i}",
            node_id="frr-node-user",
            source_kind=kind,
            source_url="user-supplied",
            extracted_on=as_of,
            claim="user-supplied",
        )
        for i, kind in enumerate(chosen)
    ]
    row = score_node(node, user_evidence, as_of)

    band_color = {"high": "🔴", "watch": "🟠", "low": "🟢"}.get(row.risk_band, "")
    rc1, rc2 = st.columns(2)
    rc1.metric(
        "90-day disruption probability",
        f"{row.disruption_probability_90d:.0%}",
    )
    rc2.metric("risk band", f"{band_color} {row.risk_band}")

    base = NODE_BASE.get(pick_kind, 0.20)
    source_score = sum(SOURCE_WEIGHTS.get(k, 0.02) for k in chosen[:5])
    tier_score = max(0.0, (4 - int(pick_tier)) * 0.03)
    st.markdown("**why** (the additive terms `score_node` summed, capped at 0.85):")
    st.dataframe(
        [
            {"term": f"base ({pick_kind})", "contribution": round(base, 3)},
            {
                "term": f"evidence ({', '.join(chosen[:5])})",
                "contribution": round(source_score, 3),
            },
            {"term": f"tier {pick_tier} bonus", "contribution": round(tier_score, 3)},
            {
                "term": "= probability (min(0.85, sum))",
                "contribution": row.disruption_probability_90d,
            },
        ],
        use_container_width=True,
        hide_index=True,
    )
    bands_ladder = "low < 0.35 ≤ watch < 0.55 ≤ high"
    st.caption(
        f"`risk_band({row.disruption_probability_90d}) = {risk_band(row.disruption_probability_90d)}`"
        f" — ladder: {bands_ladder}"
    )

st.caption(
    "v0.1 ships one substrate-osat fixture month. scoring lives in `src/frr/`; "
    "this page reads the committed `data/scores/` + `data/evidence/` artifacts and "
    "drives `src/frr/scoring.py` live in the section above. "
    "repo: github.com/AthenaTheOwl/fab-risk-radar"
)
