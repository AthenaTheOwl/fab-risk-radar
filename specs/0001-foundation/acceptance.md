# Acceptance — 0001-foundation (fab-risk-radar)

v0 is done when the following commands all succeed on a clean clone.

## Commands

```powershell
uv sync
uv run frr import graph tests/fixtures/chip_graph_export_small.json
uv run frr score --slice substrate-osat --as-of 2026-09-01
uv run frr render report --month 2026-09 --slice substrate-osat
uv run frr render pdf --month 2026-09 --slice substrate-osat
uv run python eval/score_calibration.py
uv run pytest
uv run python scripts/validate_schemas.py
uv run python scripts/voice_lint.py
uv run python scripts/traceability.py
```

## Gates that must pass

- All tests pass under `pytest`.
- `validate_schemas.py` exits 0 against
  `data/scores/substrate-osat/2026-09.parquet`.
- `traceability.py` exits 0: every score row has at least three
  evidence rows.
- `voice_lint.py` exits 0 against
  `reports/2026-09-substrate-osat.md`.
- `score_calibration.py` prints a Brier score strictly lower than
  the flat-base-rate baseline. Both numbers print in the same run.

## Artifacts produced

- `data/scores/substrate-osat/2026-09.parquet` validates against the
  disruption-score schema.
- `reports/2026-09-substrate-osat.md` exists and lints clean.
- `reports/2026-09-substrate-osat.pdf` is produced from the same
  parquet by the renderer.
- `decisions/DEC-FRR-001-evidence-rubric.md` is present and linked
  from the report.

## What v0 explicitly does not promise

- Coverage of slices other than substrate plus advanced-packaging OSAT.
- Tier-1 coverage.
- A live dashboard.
- A REST API. Consumers read the markdown, the PDF, and the parquet
  directly.
