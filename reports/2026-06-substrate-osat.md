# FabRiskRADAR substrate-osat report - 2026-06

Ranked 90-day disruption view for ABF substrate and advanced-packaging OSAT nodes.
Scores are fixture-backed in v0.1 and require three public evidence items per node.

## ranked nodes

### 1. Ibiden Ogaki ABF substrate cluster (Japan)

- probability: 0.580
- band: high
- node kind: abf-substrate
- evidence:
  - filing: Management materials continue to call out IC package substrate demand and capacity investment. (https://www.ibiden.com/ir/library/)
  - trade-data: Japan electronics-materials trade data is a monitoring input for substrate bottlenecks. (https://www.meti.go.jp/english/statistics/)
  - manual: Industry supply-chain mapping treats advanced substrates as a packaging constraint. (https://www.semiconductors.org/strengthening-the-global-semiconductor-supply-chain-in-an-uncertain-era/)

### 2. Unimicron Taoyuan substrate cluster (Taiwan)

- probability: 0.550
- band: high
- node kind: abf-substrate
- evidence:
  - filing: Investor materials report substrate demand as a main business driver. (https://www.unimicron.com/investors/financial-reports/)
  - news: Advanced packaging demand raises dependency on substrate and package assembly inputs. (https://www.tsmc.com/english/dedicatedFoundry/technology/3DFabric)
  - manual: Substrate concentration remains a supply-chain monitoring point. (https://www.semiconductors.org/strengthening-the-global-semiconductor-supply-chain-in-an-uncertain-era/)

### 3. ASE Kaohsiung advanced packaging (Taiwan)

- probability: 0.510
- band: watch
- node kind: advanced-packaging-osat
- evidence:
  - filing: ASE filings are the public anchor for advanced-packaging capacity monitoring. (https://www.aseglobal.com/investor-relations/financial-information)
  - news: 3D packaging demand increases load on OSAT and package-test capacity. (https://www.tsmc.com/english/dedicatedFoundry/technology/3DFabric)
  - manual: Packaging capacity is a named semiconductor supply-chain constraint. (https://www.semiconductors.org/strengthening-the-global-semiconductor-supply-chain-in-an-uncertain-era/)

## methodology

The v0.1 rubric combines node type, tier, and evidence-source mix. It is a deterministic screening score, not a forecast model.

- schema: `schemas/disruption-score.schema.json`
- evidence schema: `schemas/evidence-item.schema.json`
- decision: `decisions/DEC-FRR-001-evidence-rubric.md`
