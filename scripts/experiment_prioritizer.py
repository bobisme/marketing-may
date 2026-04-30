#!/usr/bin/env python3
"""
Prioritize marketing experiments by expected learning value.

Input CSV columns (case-insensitive; missing numeric columns default to 3):
experiment, assumption, impact, confidence, reach, learning, strategic_fit, speed, cost, risk, trust_risk

Score:
((impact * confidence * reach * learning * strategic_fit * speed) / ((1 + cost) * (1 + risk + trust_risk)))

Usage:
  python experiment_prioritizer.py experiments.csv --out ranked.csv
  python experiment_prioritizer.py experiments.csv --json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

NUMERIC_DEFAULTS = {
    "impact": 3.0,
    "confidence": 3.0,
    "reach": 3.0,
    "learning": 3.0,
    "strategic_fit": 3.0,
    "speed": 3.0,
    "cost": 3.0,
    "risk": 3.0,
    "trust_risk": 0.0,
}


def normalize_row(row: Dict[str, str]) -> Dict[str, Any]:
    normalized = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}
    for col, default in NUMERIC_DEFAULTS.items():
        raw = normalized.get(col, "")
        try:
            normalized[col] = float(raw) if raw not in (None, "") else default
        except ValueError:
            normalized[col] = default
    normalized.setdefault("experiment", normalized.get("test", "Untitled experiment"))
    normalized.setdefault("assumption", "")
    return normalized


def score(row: Dict[str, Any]) -> float:
    numerator = (
        row["impact"]
        * row["confidence"]
        * row["reach"]
        * row["learning"]
        * row["strategic_fit"]
        * row["speed"]
    )
    denominator = (1.0 + row["cost"]) * (1.0 + row["risk"] + row["trust_risk"])
    return numerator / denominator if denominator else 0.0


def decision_hint(row: Dict[str, Any]) -> str:
    if row["trust_risk"] >= 4:
        return "Redesign: high trust/ethics risk"
    if row["risk"] >= 5 and row["confidence"] <= 2:
        return "De-risk before running"
    if row["learning"] >= 4 and row["cost"] <= 2:
        return "Run early"
    if row["cost"] >= 5 and row["confidence"] <= 2:
        return "Avoid until evidence improves"
    return "Candidate"


def read_csv(path: Path) -> List[Dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        rows = [normalize_row(r) for r in reader]
    for r in rows:
        r["score"] = round(score(r), 4)
        r["decision_hint"] = decision_hint(r)
    return sorted(rows, key=lambda r: r["score"], reverse=True)


def write_csv(rows: List[Dict[str, Any]], path: Path | None) -> None:
    field_order = [
        "score",
        "decision_hint",
        "experiment",
        "assumption",
        "impact",
        "confidence",
        "reach",
        "learning",
        "strategic_fit",
        "speed",
        "cost",
        "risk",
        "trust_risk",
    ]
    extra = sorted({k for r in rows for k in r.keys()} - set(field_order))
    fields = field_order + extra
    out = path.open("w", newline="", encoding="utf-8") if path else sys.stdout
    try:
        writer = csv.DictWriter(out, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if path:
            out.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank marketing experiments by expected learning value.")
    parser.add_argument("csv", type=Path, help="Input CSV")
    parser.add_argument("--out", type=Path, help="Output CSV path")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of CSV")
    args = parser.parse_args()

    try:
        rows = read_csv(args.csv)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        write_csv(rows, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
