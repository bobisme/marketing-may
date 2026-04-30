#!/usr/bin/env python3
"""
Score and rank an outbound account list against a weighted ICP definition.

Inputs:
  - accounts.csv: rows of accounts with columns matching the criteria you score on.
  - icp.json:     ICP weights and criteria (see schema below).

ICP file shape:
{
  "criteria": [
    {"field": "industry",       "kind": "exact",    "match": "B2B SaaS",          "weight": 5},
    {"field": "headcount",      "kind": "range",    "match": [10, 200],            "weight": 5},
    {"field": "tech_stack",     "kind": "contains", "match": "Stripe",             "weight": 4},
    {"field": "country",        "kind": "in",       "match": ["US", "CA", "UK"],   "weight": 2},
    {"field": "trigger_funding","kind": "trigger_present",                          "weight": 4,
                                "recency_days": 90, "recency_field": "trigger_funding_date"}
  ],
  "negatives": [
    {"field": "industry", "kind": "in", "match": ["consulting", "agency"], "penalty": 3}
  ],
  "tier_thresholds": {"A": 0.75, "B": 0.50}
}

Score: sum of matched weights minus matched penalties, normalized to 0-1.

Usage:
  python outbound_list_scorer.py accounts.csv --icp icp.json
  python outbound_list_scorer.py accounts.csv --icp icp.json --top 50 --tier A
  python outbound_list_scorer.py accounts.csv --icp icp.json --json
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# --- Helpers ---------------------------------------------------------------

def parse_date(value: str) -> Optional[datetime]:
    if not value:
        return None
    v = value.strip().replace("Z", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    return None


def normalize(s: str) -> str:
    return (s or "").strip().lower()


def to_float(s: str) -> Optional[float]:
    if s is None or s == "":
        return None
    cleaned = s.replace(",", "").replace("$", "").strip()
    # Handle suffixes like "10k", "$1.5M", etc.
    suffix = cleaned[-1:].lower() if cleaned else ""
    multiplier = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}.get(suffix)
    if multiplier:
        try:
            return float(cleaned[:-1]) * multiplier
        except ValueError:
            return None
    try:
        return float(cleaned)
    except ValueError:
        return None


# --- Criterion evaluation --------------------------------------------------

def matches_exact(row_value: str, target: Any) -> bool:
    return normalize(row_value) == normalize(str(target))


def matches_contains(row_value: str, target: Any) -> bool:
    return normalize(str(target)) in normalize(row_value)


def matches_in(row_value: str, target: Any) -> bool:
    if not isinstance(target, list):
        return False
    return normalize(row_value) in {normalize(str(x)) for x in target}


def matches_range(row_value: str, target: Any) -> bool:
    if not isinstance(target, list) or len(target) != 2:
        return False
    num = to_float(row_value)
    if num is None:
        return False
    return float(target[0]) <= num <= float(target[1])


def matches_trigger_present(row_value: str, recency_check: bool, row: Dict[str, str],
                            recency_field: Optional[str], recency_days: Optional[int],
                            now: datetime) -> bool:
    """A trigger is "present" if the field is non-empty and (optionally) within recency window."""
    v = normalize(row_value)
    if not v or v in ("no", "0", "false", "none", "n/a"):
        return False
    if not recency_check:
        return True
    if not recency_field or not recency_days:
        return True  # no recency constraint defined
    ts = parse_date(row.get(recency_field, "") or row.get(recency_field.lower(), ""))
    if ts is None:
        return False
    return (now - ts).days <= recency_days


def evaluate_criterion(c: Dict[str, Any], row: Dict[str, str], now: datetime) -> Tuple[bool, str]:
    field = c.get("field", "").lower()
    raw = row.get(field, "") or ""
    kind = c.get("kind", "exact")
    target = c.get("match")
    if kind == "exact":
        ok = matches_exact(raw, target)
    elif kind == "contains":
        ok = matches_contains(raw, target)
    elif kind == "in":
        ok = matches_in(raw, target)
    elif kind == "range":
        ok = matches_range(raw, target)
    elif kind == "trigger_present":
        ok = matches_trigger_present(
            raw, recency_check=("recency_days" in c),
            row=row,
            recency_field=c.get("recency_field"),
            recency_days=c.get("recency_days"),
            now=now,
        )
    else:
        ok = False
    short = (raw[:40] + "…") if len(raw) > 40 else raw
    return ok, short


# --- Scoring ---------------------------------------------------------------

def score_row(row: Dict[str, str], icp: Dict[str, Any], now: datetime) -> Dict[str, Any]:
    criteria: List[Dict[str, Any]] = icp.get("criteria", [])
    negatives: List[Dict[str, Any]] = icp.get("negatives", [])

    max_positive = sum(float(c.get("weight", 1)) for c in criteria) or 1.0

    earned = 0.0
    penalty = 0.0
    reasons: List[str] = []

    for c in criteria:
        ok, short = evaluate_criterion(c, row, now)
        w = float(c.get("weight", 1))
        if ok:
            earned += w
            reasons.append(f"+{w:g} {c['field']}={short}")
        else:
            reasons.append(f"  0  {c['field']}={short or '∅'}")

    for n in negatives:
        ok, short = evaluate_criterion(n, row, now)
        p = float(n.get("penalty", 1))
        if ok:
            penalty += p
            reasons.append(f"-{p:g} (NEG) {n['field']}={short}")

    raw_score = earned - penalty
    normalized = max(0.0, raw_score / max_positive)

    tier_thresholds = icp.get("tier_thresholds", {"A": 0.75, "B": 0.50})
    if normalized >= tier_thresholds.get("A", 0.75):
        tier = "A"
    elif normalized >= tier_thresholds.get("B", 0.50):
        tier = "B"
    else:
        tier = "C"

    return {
        **row,
        "_score": round(raw_score, 2),
        "_score_pct": round(normalized * 100, 1),
        "_tier": tier,
        "_why": "; ".join(reasons),
    }


# --- IO --------------------------------------------------------------------

def read_accounts(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [
            {(k or "").strip().lower(): (v.strip() if isinstance(v, str) else v)
             for k, v in r.items()}
            for r in csv.DictReader(f)
        ]


def main() -> int:
    p = argparse.ArgumentParser(description="Score and rank an outbound account list against an ICP.")
    p.add_argument("csv", type=Path, help="accounts CSV")
    p.add_argument("--icp", type=Path, required=True, help="ICP weights JSON")
    p.add_argument("--top", type=int, default=0, help="show only top N rows")
    p.add_argument("--tier", choices=["A", "B", "C"], help="filter to specific tier")
    p.add_argument("--threshold", type=float, default=0.0, help="drop rows below score (0-1 normalized)")
    p.add_argument("--json", action="store_true", help="emit JSON instead of CSV")
    p.add_argument("--now", help="override 'today' for trigger recency tests, e.g. 2026-04-30")
    args = p.parse_args()

    try:
        icp = json.loads(args.icp.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading ICP file: {e}", file=sys.stderr)
        return 2

    if not icp.get("criteria"):
        print("Error: ICP file must contain 'criteria' array", file=sys.stderr)
        return 2

    now = parse_date(args.now) if args.now else datetime.now(timezone.utc).replace(tzinfo=None)
    if now is None:
        print(f"Error: cannot parse --now {args.now!r}", file=sys.stderr)
        return 2

    try:
        rows = read_accounts(args.csv)
    except Exception as e:
        print(f"Error reading accounts CSV: {e}", file=sys.stderr)
        return 2

    if not rows:
        print("No accounts in CSV.", file=sys.stderr)
        return 1

    scored = [score_row(r, icp, now) for r in rows]
    scored.sort(key=lambda r: r["_score"], reverse=True)

    if args.threshold:
        scored = [r for r in scored if r["_score_pct"] >= args.threshold * 100]
    if args.tier:
        scored = [r for r in scored if r["_tier"] == args.tier]
    if args.top:
        scored = scored[: args.top]

    if not scored:
        print("No rows match filters.", file=sys.stderr)
        return 1

    # Summary to stderr
    tiers = {"A": 0, "B": 0, "C": 0}
    for r in scored:
        tiers[r["_tier"]] += 1
    print(f"Scored {len(rows)} accounts. After filters: {len(scored)} "
          f"(A={tiers['A']}, B={tiers['B']}, C={tiers['C']}).", file=sys.stderr)

    if args.json:
        print(json.dumps(scored, indent=2, default=str))
    else:
        # Put score columns first
        head_fields = ["_score_pct", "_tier", "_score", "_why"]
        rest = [k for k in scored[0].keys() if k not in head_fields]
        fields = head_fields + rest
        w = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(scored)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
