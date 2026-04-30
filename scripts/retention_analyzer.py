#!/usr/bin/env python3
"""
Compute cohort retention curves from event logs.

Cohort = users grouped by the calendar week they fired the cohort-entry event
(default: signup_completed). Retention week N = share of that cohort that fired
the value event in week N after entry.

Input CSV columns:
  user_id, event, timestamp [, segment, source, plan, ...]

Usage:
  python retention_analyzer.py events.csv --value-event activation_completed
  python retention_analyzer.py events.csv --value-event order_placed --weeks 12
  python retention_analyzer.py events.csv --value-event repeat_login --group-by source

Output: CSV with one row per cohort × group, columns w0..wN as retention rates.
Plus a curve-shape diagnosis at the bottom (printed to stderr) using Andrew Chen
retention-curve heuristics: steep drop / flattening / plateau / declining.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# --- Time parsing ----------------------------------------------------------

def parse_ts(value: str) -> datetime:
    """Tolerant timestamp parser. Returns datetime.min for unparseable values."""
    if not value:
        return datetime.min
    v = value.strip().replace("Z", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except (ValueError, TypeError):
        return datetime.min


def week_floor(t: datetime) -> datetime:
    """Floor a datetime to the start (Monday 00:00) of its calendar week."""
    return (t - timedelta(days=t.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)


def week_index(start: datetime, t: datetime) -> int:
    """Number of full weeks between start and t. start is week 0."""
    return (t - start).days // 7


# --- Core analysis ---------------------------------------------------------

def read_events(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = [
            {(k or "").strip().lower(): (v.strip() if isinstance(v, str) else v)
             for k, v in r.items()}
            for r in csv.DictReader(f)
        ]
    if not rows:
        raise ValueError("CSV is empty")
    required = {"user_id", "event", "timestamp"}
    missing = required - set(rows[0].keys())
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return rows


def cohorted_retention(rows: List[Dict[str, str]], first_event: str, value_event: str,
                       weeks: int, group_by: Optional[str]) -> Tuple[List[Dict[str, str]], Dict]:
    """
    Returns (rows, summary) where rows is one dict per cohort × group with
    cohort_size and w0..wN retention rates.
    """
    # Group events by user
    by_user: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_user[r["user_id"]].append(r)

    # Identify cohort per user (week of first_event)
    cohort_users: Dict[Tuple[str, str], set] = defaultdict(set)  # (group, cohort_iso) -> users
    user_cohort: Dict[str, Tuple[Tuple[str, str], datetime]] = {}
    for uid, evts in by_user.items():
        evts.sort(key=lambda e: parse_ts(e.get("timestamp", "")))
        signup = next((e for e in evts if e.get("event") == first_event), None)
        if not signup:
            continue
        signup_t = parse_ts(signup["timestamp"])
        if signup_t == datetime.min:
            continue
        cohort_start = week_floor(signup_t)
        group = (signup.get(group_by, "all") if group_by else "all") or "unknown"
        ckey = (group, cohort_start.date().isoformat())
        cohort_users[ckey].add(uid)
        user_cohort[uid] = (ckey, cohort_start)

    # Bucket value-event firings by cohort × week
    cohort_week_users: Dict[Tuple[str, str], Dict[int, set]] = defaultdict(lambda: defaultdict(set))
    for uid, evts in by_user.items():
        if uid not in user_cohort:
            continue
        ckey, cohort_start = user_cohort[uid]
        for e in evts:
            if e.get("event") != value_event:
                continue
            t = parse_ts(e.get("timestamp", ""))
            if t == datetime.min:
                continue
            w = week_index(cohort_start, t)
            if 0 <= w <= weeks:
                cohort_week_users[ckey][w].add(uid)

    # Build output rows
    out: List[Dict[str, str]] = []
    small_cohorts = 0
    for ckey in sorted(cohort_users):
        group, cohort_iso = ckey
        size = len(cohort_users[ckey])
        if size < 30:
            small_cohorts += 1
        row: Dict[str, str] = {
            "group": group,
            "cohort_start": cohort_iso,
            "cohort_size": str(size),
        }
        for w in range(weeks + 1):
            users = cohort_week_users[ckey].get(w, set())
            row[f"w{w}"] = f"{len(users)/size:.3f}" if size else "0.000"
        out.append(row)

    # Summary diagnosis
    summary = diagnose(out, weeks, small_cohorts)
    return out, summary


# --- Curve shape diagnosis -------------------------------------------------

def diagnose(rows: List[Dict[str, str]], weeks: int, small_cohorts: int) -> Dict:
    """Andrew-Chen-flavored curve shape diagnosis, aggregated across cohorts."""
    if not rows:
        return {"verdict": "no cohorts", "warnings": []}

    # Aggregate retention rate per week, weighted by cohort size
    avg_by_week: List[float] = []
    for w in range(weeks + 1):
        total_users = 0
        retained = 0.0
        for r in rows:
            size = int(r["cohort_size"])
            rate = float(r[f"w{w}"])
            total_users += size
            retained += rate * size
        avg_by_week.append(retained / total_users if total_users else 0.0)

    warnings = []
    if small_cohorts:
        warnings.append(f"{small_cohorts} cohort(s) have <30 users — those rows are noisy.")

    if weeks < 4:
        verdict = "horizon too short to diagnose curve shape (need ≥ 4 weeks)"
    else:
        w0 = avg_by_week[0]
        w_early = avg_by_week[min(2, weeks)]   # week 2
        w_mid = avg_by_week[min(4, weeks)]     # week 4
        w_late = avg_by_week[weeks]            # last week
        # Heuristics — directional, not statistical
        if w0 == 0:
            verdict = "no week-0 retention recorded; check value-event definition"
        elif w_late >= 0.25 and (w_late >= 0.9 * w_mid):
            verdict = ("plateau (flat curve after initial drop) — strong PMF signal. "
                       "Late-week retention ≥ 25% with negligible decay across mid→late.")
        elif w_late >= 0.9 * w_mid and w_late < 0.25:
            verdict = ("flattening but low (<25%) — niche audience or weak repeat trigger; "
                       "consider narrower ICP or stronger retention loop.")
        elif w_late < 0.5 * w_early:
            verdict = ("declining (non-flattening) — no core audience yet. "
                       "Either pre-PMF or activation event is not the value event.")
        else:
            verdict = "mixed: gradual decline, not yet plateaued. Watch the next 2-4 weeks."

    return {
        "avg_retention_by_week": [round(x, 4) for x in avg_by_week],
        "verdict": verdict,
        "warnings": warnings,
        "cohorts": len(rows),
    }


# --- CLI ---------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Cohort retention analyzer.")
    p.add_argument("csv", type=Path, help="events CSV with user_id, event, timestamp")
    p.add_argument("--value-event", required=True,
                   help="event name that signals repeat value (e.g. activation_completed, order_placed)")
    p.add_argument("--first-event", default="signup_completed",
                   help="event defining cohort entry (default: signup_completed)")
    p.add_argument("--weeks", type=int, default=8,
                   help="retention horizon in weeks (default: 8)")
    p.add_argument("--group-by", help="optional column for cohort segmentation (e.g. source, plan)")
    args = p.parse_args()

    try:
        rows = read_events(args.csv)
        out, summary = cohorted_retention(
            rows, args.first_event, args.value_event,
            args.weeks, args.group_by.lower() if args.group_by else None
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not out:
        print(f"No cohorts found for first_event={args.first_event!r}.", file=sys.stderr)
        return 1

    # Write CSV to stdout
    fields = list(out[0].keys())
    w = csv.DictWriter(sys.stdout, fieldnames=fields)
    w.writeheader()
    w.writerows(out)

    # Diagnosis to stderr
    print("", file=sys.stderr)
    print(f"--- Diagnosis ({summary['cohorts']} cohort(s), {args.weeks}-week horizon) ---",
          file=sys.stderr)
    print(f"avg retention by week: {summary['avg_retention_by_week']}", file=sys.stderr)
    print(f"verdict: {summary['verdict']}", file=sys.stderr)
    for warn in summary["warnings"]:
        print(f"warning: {warn}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
