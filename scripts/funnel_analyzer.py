#!/usr/bin/env python3
"""
Analyze a simple ordered funnel from event logs.

Input CSV columns:
  user_id,event,timestamp
Optional:
  account_id,segment,source,campaign

Usage:
  python funnel_analyzer.py events.csv --steps page_view,signup_completed,activation_completed,checkout_completed
  python funnel_analyzer.py events.csv --steps signup_completed,activation_completed --group-by source
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def parse_time(value: str) -> datetime:
    value = value.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.replace("Z", ""), fmt)
        except ValueError:
            pass
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return datetime.min


def read_events(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = [{k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()} for r in csv.DictReader(f)]
    required = {"user_id", "event", "timestamp"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return rows


def user_completed_steps(events: List[Dict[str, str]], steps: List[str]) -> int:
    ordered = sorted(events, key=lambda e: parse_time(e.get("timestamp", "")))
    idx = 0
    for e in ordered:
        if idx < len(steps) and e.get("event") == steps[idx]:
            idx += 1
    return idx


def analyze(rows: List[Dict[str, str]], steps: List[str], group_by: Optional[str] = None) -> List[Dict[str, str]]:
    users_by_group: Dict[str, Dict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        group = r.get(group_by, "all") if group_by else "all"
        users_by_group[group or "unknown"][r["user_id"]].append(r)

    output = []
    for group, users in users_by_group.items():
        counts = [0 for _ in steps]
        for _, evts in users.items():
            completed = user_completed_steps(evts, steps)
            for i in range(completed):
                counts[i] += 1
        previous = None
        total = len(users)
        for i, step in enumerate(steps):
            count = counts[i]
            from_start = count / total if total else 0
            if i == 0:
                step_conversion = 1.0
                dropoff = 0.0
            elif previous and previous > 0:
                step_conversion = count / previous
                dropoff = 1.0 - step_conversion
            else:
                # No users reached the prior step, so this step conversion is not estimable.
                step_conversion = 0.0
                dropoff = 0.0
            output.append({
                "group": group,
                "step_index": str(i + 1),
                "step": step,
                "users": str(count),
                "total_users": str(total),
                "conversion_from_start": f"{from_start:.4f}",
                "step_conversion": f"{step_conversion:.4f}",
                "step_dropoff": f"{dropoff:.4f}",
            })
            previous = count
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze ordered funnel conversion from event CSV.")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--steps", required=True, help="Comma-separated event names in order")
    parser.add_argument("--group-by", help="Optional column to group by, e.g. source or segment")
    args = parser.parse_args()

    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    if not steps:
        print("Error: provide at least one step", file=sys.stderr)
        return 1
    try:
        rows = read_events(args.csv)
        results = analyze(rows, steps, args.group_by.lower() if args.group_by else None)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    writer = csv.DictWriter(sys.stdout, fieldnames=list(results[0].keys()) if results else [])
    if results:
        writer.writeheader()
        writer.writerows(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
