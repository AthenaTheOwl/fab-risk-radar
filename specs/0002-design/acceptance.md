# acceptance — 0002-design

The v0.1 increment is accepted when:

- `python -m frr score --slice substrate-osat --month 2026-06` writes
  a score JSONL and report.
- `python -m frr validate` prints `valid: reports`.
- `python scripts/validate_schemas.py` passes.
- `python scripts/traceability.py` passes.
- `python -m pytest tests/ -q` passes.

