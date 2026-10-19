"""Write a non-sensitive example payload from the dataset's first row."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from zipfile import ZipFile

import pandas as pd

from backend.schema import FEATURES

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with ZipFile(ROOT / "covertype.zip") as archive:
        with archive.open("covtype.data.gz") as compressed:
            with gzip.GzipFile(fileobj=compressed) as source:
                row = pd.read_csv(source, header=None, nrows=1)
    payload = {feature: int(row.iloc[0, index]) for index, feature in enumerate(FEATURES)}
    sample_frame = row.iloc[:, : len(FEATURES)].copy()
    sample_frame.columns = FEATURES
    (ROOT / "data").mkdir(parents=True, exist_ok=True)
    sample_frame.to_csv(ROOT / "data" / "sample_inputs.csv", index=False)
    output = ROOT / "backend" / "test_payload.json"
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(payload)} predictors to {output}")


if __name__ == "__main__":
    main()
