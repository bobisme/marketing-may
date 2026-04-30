#!/usr/bin/env python3
"""
Analyze directional pricing research.

Subcommands:
  vanwestendorp: CSV with columns too_cheap, cheap, expensive, too_expensive
  gabor: CSV with columns price, would_buy; optional segment

Examples:
  python pricing_research_analyzer.py vanwestendorp sample_pricing_vanwestendorp.csv
  python pricing_research_analyzer.py gabor gabor.csv --segment segment
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Any


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [{k.strip().lower(): v.strip() for k, v in row.items()} for row in csv.DictReader(f)]


def as_float(value: str, default: float | None = None) -> float | None:
    if value is None or value == "":
        return default
    cleaned = value.replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return default


def yes(value: str) -> bool:
    return str(value).strip().lower() in {"yes", "y", "true", "1", "buy", "would buy", "likely"}


def grid_from_values(values: Iterable[float], points: int = 200) -> List[float]:
    vals = [v for v in values if v is not None and math.isfinite(v)]
    if not vals:
        raise ValueError("No numeric prices found")
    lo, hi = min(vals), max(vals)
    if lo == hi:
        return [lo]
    step = (hi - lo) / (points - 1)
    return [lo + i * step for i in range(points)]


def nearest_intersection(grid: List[float], a: List[float], b: List[float]) -> Tuple[float, float]:
    idx = min(range(len(grid)), key=lambda i: abs(a[i] - b[i]))
    return round(grid[idx], 2), round(abs(a[idx] - b[idx]), 4)


def vanwestendorp(path: Path) -> Dict[str, Any]:
    rows = read_rows(path)
    required = ["too_cheap", "cheap", "expensive", "too_expensive"]
    for col in required:
        if col not in rows[0]:
            raise ValueError(f"Missing column: {col}")

    data = {col: [as_float(r.get(col, "")) for r in rows] for col in required}
    n = len(rows)
    grid = grid_from_values(v for vals in data.values() for v in vals if v is not None)

    # Curves are approximations for directional use.
    # At price p:
    # too_cheap = share whose too-cheap threshold is >= p
    # cheap = share whose bargain/cheap threshold is >= p
    # expensive = share whose expensive threshold is <= p
    # too_expensive = share whose too-expensive threshold is <= p
    curves = {}
    curves["too_cheap"] = [sum(1 for v in data["too_cheap"] if v is not None and v >= p) / n for p in grid]
    curves["cheap"] = [sum(1 for v in data["cheap"] if v is not None and v >= p) / n for p in grid]
    curves["expensive"] = [sum(1 for v in data["expensive"] if v is not None and v <= p) / n for p in grid]
    curves["too_expensive"] = [sum(1 for v in data["too_expensive"] if v is not None and v <= p) / n for p in grid]

    opp, opp_gap = nearest_intersection(grid, curves["too_cheap"], curves["too_expensive"])
    idp, idp_gap = nearest_intersection(grid, curves["cheap"], curves["expensive"])
    pmc, pmc_gap = nearest_intersection(grid, curves["too_cheap"], curves["expensive"])
    pme, pme_gap = nearest_intersection(grid, curves["cheap"], curves["too_expensive"])

    return {
        "method": "van_westendorp_directional",
        "respondents": n,
        "optimal_price_point_opp": opp,
        "indifference_price_point_idp": idp,
        "point_of_marginal_cheapness_pmc": pmc,
        "point_of_marginal_expensiveness_pme": pme,
        "acceptable_range_directional": [min(pmc, pme), max(pmc, pme)],
        "intersection_gaps": {"opp": opp_gap, "idp": idp_gap, "pmc": pmc_gap, "pme": pme_gap},
        "caution": "Directional only. Validate with behavioral tests, paid pilots, and segment-level analysis.",
    }


def gabor(path: Path, segment_col: str | None = None) -> Dict[str, Any]:
    rows = read_rows(path)
    if not rows:
        raise ValueError("No rows")
    if "price" not in rows[0] or "would_buy" not in rows[0]:
        raise ValueError("CSV must include price and would_buy columns")

    groups: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in rows:
        segment = r.get(segment_col.lower(), "all") if segment_col else "all"
        groups[segment or "unknown"].append(r)

    results = {}
    for segment, grows in groups.items():
        by_price: Dict[float, List[bool]] = defaultdict(list)
        for r in grows:
            price = as_float(r.get("price", ""))
            if price is None:
                continue
            by_price[price].append(yes(r.get("would_buy", "")))
        price_rows = []
        for price in sorted(by_price):
            responses = by_price[price]
            p_buy = sum(responses) / len(responses)
            price_rows.append({
                "price": price,
                "responses": len(responses),
                "purchase_probability": round(p_buy, 4),
                "revenue_index": round(price * p_buy, 4),
            })
        best = max(price_rows, key=lambda r: r["revenue_index"]) if price_rows else None
        results[segment] = {"price_curve": price_rows, "revenue_maximizing_price_directional": best}

    return {
        "method": "gabor_granger_directional",
        "segments": results,
        "caution": "Survey WTP is weaker than purchase behavior. Validate with paid pilots, deposits, or pricing-page behavior.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze pricing research CSVs.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    vw = sub.add_parser("vanwestendorp", help="Analyze Van Westendorp CSV")
    vw.add_argument("csv", type=Path)
    gg = sub.add_parser("gabor", help="Analyze Gabor-Granger CSV")
    gg.add_argument("csv", type=Path)
    gg.add_argument("--segment", help="Optional segment column")
    args = parser.parse_args()

    try:
        if args.cmd == "vanwestendorp":
            result = vanwestendorp(args.csv)
        else:
            result = gabor(args.csv, args.segment)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
