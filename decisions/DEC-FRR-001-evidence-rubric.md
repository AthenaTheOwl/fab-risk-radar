---
id: DEC-FRR-001-evidence-rubric
spec: specs/0002-design/
requirement: R-FRR-014
date: 2026-06-20
status: approved
reversible: true
decision: |
  Use a deterministic evidence-mix rubric for the first substrate/OSAT
  disruption scores.
alternatives:
  - label: train a forecast model first
    rejected_because: |
      The repo does not yet have a labeled disruption cohort. A model would
      hide fixture assumptions behind a false precision layer.
  - label: publish unscored evidence only
    rejected_because: |
      The monthly artifact needs a ranking so a reader can act on the top
      constraints first.
rationale: |
  A simple rubric is auditable, stable under tests, and easy to replace after
  the calibration dataset lands.
evidence:
  - kind: spec
    ref: specs/0002-design/
rollback: |
  Replace the scoring function and regenerate the score JSONL once a calibrated
  model beats the rubric on a held-out disruption cohort.
---

