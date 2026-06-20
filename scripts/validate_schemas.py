from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[object]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    try:
        import jsonschema
    except ImportError as exc:
        raise SystemExit("jsonschema is required") from exc
    for schema_path in (ROOT / "schemas").glob("*.schema.json"):
        jsonschema.validators.validator_for(load_json(schema_path)).check_schema(load_json(schema_path))
    score_schema = load_json(ROOT / "schemas" / "disruption-score.schema.json")
    evidence_schema = load_json(ROOT / "schemas" / "evidence-item.schema.json")
    for path in (ROOT / "data" / "scores").glob("*/*.jsonl"):
        for row in read_jsonl(path):
            jsonschema.validate(row, score_schema)
    for path in (ROOT / "data" / "evidence").glob("*.jsonl"):
        for row in read_jsonl(path):
            jsonschema.validate(row, evidence_schema)
    print("validate_schemas OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

