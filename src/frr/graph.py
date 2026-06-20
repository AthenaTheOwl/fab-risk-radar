from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_graph(path: Path) -> dict[str, list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = data.get("nodes")
    edges = data.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("graph export must contain nodes and edges lists")
    for node in nodes:
        for field in ("node_id", "name", "tier", "node_kind", "region"):
            if field not in node:
                raise ValueError(f"node missing {field}: {node}")
    for edge in edges:
        for field in ("source", "target", "flow_kind"):
            if field not in edge:
                raise ValueError(f"edge missing {field}: {edge}")
    return {"nodes": nodes, "edges": edges}


def select_slice(nodes: list[dict[str, Any]], slice_name: str) -> list[dict[str, Any]]:
    if slice_name != "substrate-osat":
        raise ValueError("v0.1 supports only substrate-osat")
    return [
        node
        for node in nodes
        if node["node_kind"] in {"abf-substrate", "advanced-packaging-osat"}
    ]

