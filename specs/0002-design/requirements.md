# requirements — 0002-design

## scope

v0.1 ships one monthly substrate/OSAT disruption report from committed
fixture data. It proves the graph, evidence, scoring, report, and
traceability loop before live source ingest.

## requirements

- R-FRR-013: The CLI scores the `substrate-osat` slice for one month
  with `python -m frr score --slice substrate-osat --month 2026-06`.
- R-FRR-014: Each score row has a probability in `[0, 1]`, a risk band,
  and at least three evidence ids.
- R-FRR-015: Evidence rows use public URLs and include a dated claim.
- R-FRR-016: The report renders to `reports/2026-06-substrate-osat.md`.
- R-FRR-017: `python -m frr validate`, `scripts/validate_schemas.py`,
  and `scripts/traceability.py` fail on missing evidence.

