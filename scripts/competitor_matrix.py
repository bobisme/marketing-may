#!/usr/bin/env python3
"""
Summarize competitor research into category norms and whitespace prompts.

Input CSV suggested columns:
competitor,url,category,icp,hero,pricing_model,entry_price,free_trial,proof,cta,trust_assets,channels,strengths,weaknesses,gaps

Usage:
  python competitor_matrix.py competitors.csv --out competitor_summary.md
"""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return [{(k or "").strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in r.items()} for r in csv.DictReader(f)]


def split_tokens(value: str) -> List[str]:
    return [x.strip().lower() for x in (value or "").replace(";", ",").split(",") if x.strip()]


def numeric_price(value: str) -> Optional[float]:
    if not value:
        return None
    cleaned = value.lower().replace("$", "").replace(",", "").replace("/mo", "").replace("month", "").strip()
    if "custom" in cleaned or "contact" in cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def summarize(rows: List[Dict[str, str]]) -> str:
    lines = ["# Competitive Intelligence Summary", ""]
    lines.append(f"Competitors analyzed: {len(rows)}")

    for field in ["category", "pricing_model", "free_trial", "cta"]:
        counts = Counter((r.get(field, "") or "unknown").lower() for r in rows)
        lines.append(f"\n## {field.replace('_', ' ').title()} norms")
        for val, c in counts.most_common(10):
            lines.append(f"- {val or 'blank'}: {c}")

    prices = [p for r in rows for p in [numeric_price(r.get("entry_price", ""))] if p is not None]
    if prices:
        lines.append("\n## Entry price directional stats")
        lines.append(f"- Min: {min(prices):.2f}")
        lines.append(f"- Median: {statistics.median(prices):.2f}")
        lines.append(f"- Max: {max(prices):.2f}")

    token_fields = ["proof", "trust_assets", "channels", "gaps", "weaknesses"]
    for field in token_fields:
        counts = Counter()
        for r in rows:
            counts.update(split_tokens(r.get(field, "")))
        lines.append(f"\n## Common {field.replace('_', ' ')}")
        if counts:
            for val, c in counts.most_common(15):
                lines.append(f"- {val}: {c}")
        else:
            lines.append("- No data")

    lines.append("\n## Whitespace prompts")
    prompts = [
        "Which high-pain segment is not named explicitly in competitor heroes?",
        "Which proof asset is missing across the category: benchmark, case study, security page, ROI calculator, sample output?",
        "Which current alternative do competitors ignore: spreadsheet, agency, internal build, manual process, open source?",
        "Is pricing hidden because value is complex, or because vendors avoid transparency? Could transparent entry pricing become a wedge?",
        "Which onboarding friction appears repeatedly in reviews or docs? Can we remove it with templates, concierge setup, or migration support?",
        "Which channel is underused but reachable for this ICP?",
        "Which objection appears on sales calls but not on competitor pages?",
    ]
    for p in prompts:
        lines.append(f"- {p}")

    lines.append("\n## Recommended next artifact")
    lines.append("Fill templates/04_positioning_messaging_copy.md and templates/05_pricing_packaging_offer.md using the gaps above.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize competitor matrix CSV.")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    rows = read_rows(args.csv)
    output = summarize(rows)
    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
