# Design — 0001-foundation (fab-risk-radar)

## Shape

A monthly batch over the imported semis supply-chain graph. Two
ingest sources (substrate and OSAT) attach evidence to nodes. A
scoring pass emits a per-node disruption probability. A render pass
produces the markdown report and a PDF.

## Components

### Graph (`src/graph/`)

- `import_chip_map.py` — reads
  `data/chip_graph_export.json` produced by `chip-supply-chain-map`
  and converts it into a typed in-memory graph
  (`networkx.MultiDiGraph` plus typed node attributes). Nodes carry
  a `tier` field (1, 2, 3); edges carry a `flow_kind`
  (`material` | `equipment` | `service`).

### Evidence (`src/evidence/`)

- `substrate_ingest.py` — reads substrate-side filings, news, and
  trade-data exports under `data/raw/substrate/`. Emits
  `EvidenceItem` rows attached to substrate-related node IDs.
- `osat_ingest.py` — same shape for OSAT-side sources.
- `base.py` — declares the `EvidenceItem` model and the
  `IngestAdapter` protocol.

### Scoring (`src/scoring/`)

- `disruption_probability.py` — pure function:
  `disruption_probability(node, evidence_items, horizon_days)
  -> float`. v0 uses a documented weighted-rubric model. The rubric
  is owned by `DEC-FRR-001-evidence-rubric.md`.
- `slice.py` — selects the substrate-plus-OSAT subgraph from the
  imported graph.

### Render (`src/render/`)

- `report.py` — emits `reports/YYYY-MM-<slice>.md` from the scored
  parquet via a Jinja template at
  `src/render/templates/monthly_slice.md.j2`.
- `pdf.py` — wraps the markdown with a pandoc invocation; emits
  `reports/YYYY-MM-<slice>.pdf`.

### Eval (`eval/`)

- `score_calibration.py` — replays the scorer against the 2024-2025
  cohort; prints Brier score and the flat-base-rate baseline.

## Data flow

```
chip-supply-chain-map export ----> import_chip_map.py
                                          |
                                          v
                                   in-memory graph
                                          |
                          +---------------+----------------+
                          v                                v
                  substrate_ingest                  osat_ingest
                          |                                |
                          +---------------+----------------+
                                          v
                                evidence/*.parquet
                                          |
                                          v
                            disruption_probability.py
                                          |
                                          v
                        data/scores/substrate-osat/2026-09.parquet
                                          |
                          +---------------+----------------+
                          v                                v
                   render/report.py                render/pdf.py
                          |                                |
                          v                                v
              reports/2026-09-substrate-osat.md   reports/2026-09-substrate-osat.pdf
```

## Non-goals for 0001

- Tier-1 coverage.
- Real-time scoring.
- A web frontend. The static PDF and markdown are the artifact.
- Direct integration into a customer's procurement system.
