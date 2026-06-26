# fab-risk-radar

A single substrate cluster in Ogaki, Japan carries a 58% chance of disrupting supply
in the next 90 days. Three other names sit behind it. fab-risk-radar publishes the
list, ranked, with the public filing behind each number.

## What it does

The semiconductor supply chain is watched closely at tier-1 and goes dark below it.
The substrate, OSAT, and packaging nodes that actually cap 2026-2027 capacity sit in
that dark. After CoWoS, the next squeeze is Ajinomoto ABF substrate and the advanced-
packaging OSATs, and the questions about Taiwan and Korea trade scenarios get answered
with a shrug because nobody publishes the graph.

fab-risk-radar publishes the graph. Each month it scores the top tier-2/3 nodes by
how likely they are to disrupt supply in the next 90 days, bands them high/watch, and
hangs three public evidence items off every score so the number is something you can
check instead of trust. The first issue covers ABF substrate plus advanced-packaging
OSATs.

## Try it

No args, read-only, offline. Prints the committed 2026-06 ranked screen:

```
$ python frr.py show
FabRiskRADAR - substrate-osat - 90-day disruption screen (as of 2026-06-30)
3 nodes scored, 2 in the high band. Higher probability = more likely to constrain capacity in the next 90 days.

  rank   prob  band   node
  ---- ------  ------ ----------------------------------------
  1     0.580  high   Ibiden Ogaki ABF substrate cluster (Japan)
  2     0.550  high   Unimicron Taoyuan substrate cluster (Taiwan)
  3     0.510  watch  ASE Kaohsiung advanced packaging (Taiwan)

top risk: Ibiden Ogaki ABF substrate cluster (Japan) at 58% 90-day disruption probability
  anchored on filing: https://www.ibiden.com/ir/library/
```

It tells a procurement lead which substrate/OSAT node to chase first this quarter,
ranked, with each score backed by three public evidence items.

## Live demo

An interactive web view of the same ranked screen `python frr.py show` prints, reading
the committed `data/scores/` + `data/evidence/` artifacts directly.

local:

```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

deploy: Streamlit Community Cloud -> New app -> repo `AthenaTheOwl/fab-risk-radar`,
branch `main`, main file `streamlit_app.py`.

<!-- live URL: https://<app>.streamlit.app -->

## How to run

```powershell
python frr.py show                                  # ranked screen from committed data
python frr.py score --slice substrate-osat --month 2026-06   # rebuild scores + report
python frr.py validate                              # check score-to-evidence traceability
```

Full prose report: `reports/2026-06-substrate-osat.md`.

## How it connects

The node set under all of these is one graph; fab-risk-radar scores the risk on it.

- [chip-supply-chain-map](https://github.com/AthenaTheOwl/chip-supply-chain-map) — the
  underlying graph this repo consumes as an export.
- [wafer-to-watt](https://github.com/AthenaTheOwl/wafer-to-watt) — cross-references
  accelerator commitments against the same nodes.
- [multitier-psi](https://github.com/AthenaTheOwl/multitier-psi) — runs sealed
  cross-OEM intersection queries over the same graph schema.

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

## License

MIT. See [LICENSE](LICENSE).
