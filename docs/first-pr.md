# First PR — fab-risk-radar

The literal first PR after the scaffold. Narrow scope: import the
graph, declare the schemas, and stand up the validation gate.

## Title

`feat(FRR): graph import plus disruption-score schema (PR 1)`

## Goal

Land the graph import from `chip-supply-chain-map`, the two JSON
schemas that constrain every downstream artifact, and the first gate
that enforces them.

## Files added

- `pyproject.toml` — deps: `networkx`, `polars`, `pyarrow`,
  `pydantic`, `jsonschema`, `jinja2`, `pytest`, `ruff`.
- `src/frr/__init__.py`
- `src/frr/graph/__init__.py`
- `src/frr/graph/import_chip_map.py` — reads
  `data/chip_graph_export.json`, returns a `networkx.MultiDiGraph`
  with typed node attributes (`tier`, `node_kind`, `region`,
  `aliases`) and typed edges (`flow_kind`, `share`).
- `schemas/disruption-score.schema.json` — v0 score row shape:
  `node_id`, `slice`, `as_of`, `horizon_days`,
  `disruption_probability`, `evidence_ids`.
- `schemas/evidence-item.schema.json` — `evidence_id`, `node_id`,
  `source_kind`, `source_url`, `extracted_on`, `claim`.
- `tests/fixtures/chip_graph_export_small.json` — twenty nodes,
  twenty-five edges, hand-curated. The schema mirrors a real export
  but the entities are obviously synthetic.
- `tests/test_import_chip_map.py` — asserts every node has the
  required attributes and every edge has a `flow_kind`.
- `tests/test_schemas_self.py` — validates each schema against
  JSON Schema 2020-12.
- `scripts/validate_schemas.py` — walks `schemas/` plus any
  `data/scores/**/*.parquet` and exits 1 on any mismatch.

## Files not in this PR

- Evidence ingest. PR 2.
- Scoring. PR 2.
- The first report. PR 3.
- The Brier-score calibration backtest. PR 3.
- The PDF renderer. PR 3.
- Any CI workflow.

## Verification

Reviewer runs:

```powershell
uv sync
uv run pytest
uv run python scripts/validate_schemas.py
```

Expected: all tests pass; `validate_schemas.py` exits 0.

## Review checklist

- [ ] Both schemas declare `$id` and `$schema`.
- [ ] The fixture has at least one node per tier (1, 2, 3).
- [ ] No real customer-side identifier is in the fixture.
- [ ] `pyproject.toml` pins lower bounds on every dep.
- [ ] No marketing words in any added markdown.

## After merge

PR 2 lands the substrate and OSAT ingest adapters and the scoring
function. PR 3 ships the first real report at
`reports/2026-09-substrate-osat.md`, the PDF render, and the
calibration backtest.
