# Tasks — 0001-foundation (fab-risk-radar)

Ordered for the first two to three PRs after this scaffold lands.

## PR 1 — graph import plus schema

- [ ] Add `pyproject.toml` with `networkx`, `polars`, `pyarrow`, `pydantic`, `jsonschema`, `jinja2`, `pytest`, `ruff`.
- [ ] Add `schemas/disruption-score.schema.json`.
- [ ] Add `schemas/evidence-item.schema.json`.
- [ ] Add `src/frr/graph/import_chip_map.py`.
- [ ] Add `tests/fixtures/chip_graph_export_small.json` (~20 nodes).
- [ ] Add `tests/test_import_chip_map.py`.
- [ ] Add `scripts/validate_schemas.py`.

## PR 2 — substrate + OSAT evidence plus scoring

- [ ] Add `src/frr/evidence/base.py` declaring `EvidenceItem` and the `IngestAdapter` protocol.
- [ ] Add `src/frr/evidence/substrate_ingest.py`.
- [ ] Add `src/frr/evidence/osat_ingest.py`.
- [ ] Add `src/frr/scoring/disruption_probability.py`.
- [ ] Add `src/frr/scoring/slice.py`.
- [ ] Add `decisions/DEC-FRR-001-evidence-rubric.md`.
- [ ] Add `tests/test_disruption_probability.py` with boundary cases.

## PR 3 — first report plus calibration

- [ ] Add `src/frr/render/report.py` plus the Jinja template.
- [ ] Add `src/frr/render/pdf.py`.
- [ ] Add `reports/2026-09-substrate-osat.md` (the first report).
- [ ] Add `eval/score_calibration.py` plus the 2024-2025 cohort fixture parquet.
- [ ] Add `scripts/voice_lint.py` and wire as gate on `reports/`.
- [ ] Add `scripts/traceability.py` enforcing the three-evidence rule.
