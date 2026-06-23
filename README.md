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


v0.1 shipped and runs end to end. The entry command `python frr.py validate` runs. See `specs/0002-design/` for the v0.1 scope and `STATUS.md` (where present) for the current state and next-feature queue.

## try it

No args, read-only, offline. Prints the committed 2026-06 ranked screen:

```
$ python frr.py show
FabRiskRADAR - substrate-osat - 90-day disruption screen (as of 2026-06-30)
3 nodes scored, 2 in the high band. Higher probability = more likely to constrain capacity in the next 90 days.

  rank   prob  band   node
  1     0.580  high   Ibiden Ogaki ABF substrate cluster (Japan)
  2     0.550  high   Unimicron Taoyuan substrate cluster (Taiwan)
  3     0.510  watch  ASE Kaohsiung advanced packaging (Taiwan)

top risk: Ibiden Ogaki ABF substrate cluster (Japan) at 58% 90-day disruption probability
```

It tells a procurement lead which substrate/OSAT node to chase first this quarter, ranked, with each score backed by three public evidence items.

## How to run

```powershell
python frr.py show                                  # ranked screen from committed data
python frr.py score --slice substrate-osat --month 2026-06   # rebuild scores + report
python frr.py validate                              # check score-to-evidence traceability
```

Full prose report: `reports/2026-06-substrate-osat.md`.

## live demo

interactive web view of the same ranked screen `python frr.py show` prints,
reading the committed `data/scores/` + `data/evidence/` artifacts directly.

local:

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

deploy: Streamlit Community Cloud -> New app -> repo `AthenaTheOwl/fab-risk-radar`,
branch `main`, main file `streamlit_app.py`.

<!-- live URL: https://<app>.streamlit.app -->


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
