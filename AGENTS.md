# AGENTS.md — fab-risk-radar

Operating contract for AI agents (Claude, Codex, Cursor) working in
this repo. Conventions match the AthenaTheOwl portfolio so an agent
already trained on `chip-supply-chain-map` or `supplier-risk-rag-agent`
recognizes the shape.

## What this repo is

A monthly publication. The artifact is the checked-in report under
`reports/YYYY-MM-<slice>.md` plus the PDF render and the underlying
score parquet. The first slice is substrate plus advanced-packaging
OSAT. The graph itself lives in `chip-supply-chain-map`; this repo
imports an export of that graph and computes disruption probabilities
on top.

## Voice constraints

- No marketing words. The banned set will live in
  `scripts/voice_lint.py::BANNED_FAIL` once the lint script lands in
  spec 0002. Examples that always fail: leverage, demonstrate, seamless,
  cutting-edge, best-in-class, synergy.
- No antithetical reversals as a structural device.
- Plain assertions. Every probability claim carries an evidence
  citation. No "industry sources say" without a URL or filing.

## Gates

Will land in spec `0002-substrate-osat`. The intended chain:

- `voice_lint` on every report.
- `validate_schemas` on every disruption-score parquet.
- `traceability`: every score row has at least three evidence rows.
- `score_calibration`: Brier-score backtest against the 2024-2025
  disruption cohort must beat a flat-base-rate baseline.

## Out of scope

- Live dashboard. Monthly cadence only.
- Tier-1 coverage — Resilinc and Everstream already do that well.
  This repo lives below tier-1.
- Channel checks under NDA. Public sources only.
- Forecasts beyond 90 days from the report's `as_of` date.
