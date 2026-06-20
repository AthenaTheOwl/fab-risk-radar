# design — 0002-design

## shape

The v0.1 loop is fixture-first:

1. read `data/chip_graph_export.json`
2. select substrate and OSAT nodes
3. read `data/evidence/2026-06-substrate-osat.csv`
4. score each node with a deterministic rubric
5. write JSONL scores, JSONL evidence, and a markdown report
6. validate that every score has at least three evidence rows

## non-goals

- live scraping
- PDF rendering
- parquet output
- calibration backtest

Those belong after the report loop is stable.

