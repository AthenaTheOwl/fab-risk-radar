# Requirements — 0001-foundation (fab-risk-radar)

Brand prefix: `FRR`.

## Scope

The foundation spec names the graph import path, the disruption-score
schema, the evidence rubric, and the calibration discipline that
v0 must respect.

## Requirements

- R-FRR-001: The repo imports `data/chip_graph_export.json` from the
  `chip-supply-chain-map` repo via a documented schema. The import
  is a pure transform; no upstream rewrites.
- R-FRR-002: Every node in the imported graph that participates in a
  monthly report receives a `disruption_probability_90d` value in the
  closed interval [0.0, 1.0].
- R-FRR-003: Every score has at least three evidence items. Each
  evidence item has a `source_kind` (`filing` | `news` | `trade-data`
  | `imagery` | `manual`), a `source_url`, an `extracted_on` date,
  and a one-sentence `claim` field.
- R-FRR-004: The monthly report at `reports/YYYY-MM-<slice>.md` lists
  the top 20 nodes by `disruption_probability_90d`, each with the
  three evidence items inline.
- R-FRR-005: The report also includes a `## Methodology` section
  linking to the score schema, the calibration backtest, and the
  decision records that govern the rubric.
- R-FRR-006: A `score_calibration.py` script computes a Brier score
  against the 2024-2025 disruption cohort. The backtest must beat a
  flat-base-rate baseline; both numbers print in the same run.
- R-FRR-007: Score outputs persist as parquet at
  `data/scores/<slice>/<month>.parquet`. The parquet schema is
  declared at `schemas/disruption-score.schema.json`.
- R-FRR-008: A `voice_lint` pass runs against every checked-in
  report.
- R-FRR-009: A `traceability` script asserts every score row has at
  least three evidence rows. CI fails on any score with fewer.
- R-FRR-010: Decision records live under `decisions/DEC-FRR-NNN.md`.
  The first is `DEC-FRR-001-evidence-rubric.md`.
- R-FRR-011: The PDF render is reproducible: running the renderer
  twice on the same parquet produces byte-identical PDFs (modulo
  document timestamp, which is fixed by an `--as-of` flag).
- R-FRR-012: This repo does not call any private API or scraped
  source that violates a publisher's terms.
