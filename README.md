# FabRiskRADAR

Monthly published report on tier-2 and tier-3 semiconductor disruption
risk. Substrate (ABF) and OSAT focus. Calibrated 90-day disruption
probability scores with three evidence items behind each score.

## What this is

The semis supply chain has a tier-N problem. Resilinc and Everstream
cover tier-1 with rigor; below that, the substrate, OSAT, and packaging
nodes that actually constrain 2026-2027 capacity sit in a gap. The
next squeeze after CoWoS is Ajinomoto ABF substrate plus advanced
packaging OSATs. Board-level questions about Taiwan and Korea trade
scenarios get answered with vibes because nobody publishes the graph.

FabRiskRADAR is the report. Monthly cadence. Top 20 tier-2/3 semis
nodes by disruption probability over the next 90 days. Three evidence
items per score, each with a public source. The first issue covers
ABF substrate plus advanced packaging OSATs.

Bucket: supply-chain. Category: supply-chain. Brand prefix: `FRR`.

## Who this is for

- Procurement and resilience leads at fabless semis design groups
  (AMD, Marvell, Broadcom, Apple SPG).
- Industrial OEMs that buy chips (auto Tier-1s, medical devices).
- Defense primes with semis exposure.

## Status

v0 scaffold. No implementation yet. The first PR after the scaffold
imports the chip-supply-chain-map graph export and lands the
disruption-probability schema; see `docs/first-pr.md`.

## How to run

Placeholder. Run commands will land in spec `0002-substrate-osat`.
The shape will be:

```powershell
uv sync
uv run frr import graph ../chip-supply-chain-map/exports/2026-08.json
uv run frr score --slice substrate-osat --as-of 2026-09-01
uv run frr render report --month 2026-09
uv run frr calibration --backtest 2024-2025
```

## Layout

```
fab-risk-radar/
  AGENTS.md
  LICENSE
  README.md
  specs/
    0001-foundation/
      requirements.md
      design.md
      tasks.md
      acceptance.md
  docs/
    first-pr.md
  src/
    scoring/            # disruption_probability.py
    evidence/           # substrate_ingest, osat_ingest
    graph/              # import from chip-supply-chain-map
    render/             # report template, pdf export
  data/
    chip_graph_export.json   # from chip-supply-chain-map
  reports/              # checked-in monthly PDF + markdown
  eval/                 # score_calibration.py, Brier backtest
  decisions/            # DEC-FRR-* architectural choices
```

## Compounds with

- `chip-supply-chain-map` is the underlying graph; this repo consumes
  its export.
- WaferToWatt cross-references accelerator commitments against the
  same node set.
- DemandStorm shares the HTS-code infrastructure.
- MultiTier PSI uses the same graph schema for sealed cross-OEM
  intersection queries.

## License

MIT. See [LICENSE](LICENSE).
