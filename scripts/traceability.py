from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.frr.validation import validate_traceability  # noqa: E402


def main() -> int:
    for score_path in (ROOT / "data" / "scores").glob("*/*.jsonl"):
        month = score_path.stem
        slice_name = score_path.parent.name
        validate_traceability(score_path, ROOT / "data" / "evidence" / f"{month}-{slice_name}.jsonl")
    print("traceability OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

