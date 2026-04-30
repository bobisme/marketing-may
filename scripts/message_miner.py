#!/usr/bin/env python3
"""
Mine voice-of-customer text for repeated language, pains, outcomes, objections, triggers, and alternatives.

Usage:
  python message_miner.py sample_voc.txt
  python message_miner.py ./reviews_directory --top 30 --out voc_report.md

No external dependencies.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, List, Dict, Tuple

STOPWORDS = set("""
a an and are as at be but by for from has have how i if in is it its of on or our that the their them then there they this to was we were what when where who why will with you your about after also can could did do does doing done get got had into just like make many more most much not now only over so some than too use used using very want wanted would
""".split())

CATEGORIES = {
    "pain": ["frustrat", "annoy", "slow", "hard", "confusing", "manual", "waste", "broken", "expensive", "error", "bug", "pain", "hate", "stuck", "miss", "risk"],
    "outcome": ["save", "faster", "easy", "automate", "increase", "reduce", "better", "ship", "launch", "grow", "revenue", "accurate", "confidence", "visibility"],
    "objection": ["too expensive", "price", "cost", "trust", "security", "privacy", "not sure", "hard to switch", "migration", "support", "setup", "learning curve"],
    "trigger": ["when", "after", "before", "deadline", "launch", "hiring", "funding", "audit", "incident", "migration", "renewal", "new role", "regulation"],
    "alternative": ["spreadsheet", "excel", "google sheets", "manual", "agency", "consultant", "internal", "open source", "zapier", "notion", "airtable", "slack", "email"],
    "proof": ["case study", "testimonial", "review", "benchmark", "demo", "example", "sample", "security", "certified", "trusted", "customer"],
}


def read_text(path: Path) -> str:
    if path.is_dir():
        parts = []
        for p in sorted(path.glob("**/*")):
            if p.is_file() and p.suffix.lower() in {".txt", ".md", ".csv"}:
                parts.append(p.read_text(encoding="utf-8", errors="ignore"))
        return "\n".join(parts)
    return path.read_text(encoding="utf-8", errors="ignore")


def sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.strip()) > 20]


def tokenize(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9'_-]+", text.lower())
    return [w.strip("'_- ") for w in words if w not in STOPWORDS and len(w) > 2]


def ngrams(tokens: List[str], n: int) -> Iterable[str]:
    for i in range(len(tokens) - n + 1):
        gram = tokens[i:i+n]
        if all(t not in STOPWORDS for t in gram):
            yield " ".join(gram)


def classify(sent_list: List[str]) -> Dict[str, List[str]]:
    buckets: Dict[str, List[str]] = defaultdict(list)
    for s in sent_list:
        low = s.lower()
        for cat, needles in CATEGORIES.items():
            if any(n in low for n in needles):
                buckets[cat].append(s)
    return buckets


def report(text: str, top: int) -> str:
    toks = tokenize(text)
    counts = Counter(toks)
    bigrams = Counter(ngrams(toks, 2))
    trigrams = Counter(ngrams(toks, 3))
    sent_list = sentences(text)
    buckets = classify(sent_list)

    lines = ["# Voice-of-Customer Message Mining Report", ""]
    lines.append("## Top terms")
    for term, c in counts.most_common(top):
        lines.append(f"- {term}: {c}")
    lines.append("\n## Top 2-word phrases")
    for term, c in bigrams.most_common(top):
        lines.append(f"- {term}: {c}")
    lines.append("\n## Top 3-word phrases")
    for term, c in trigrams.most_common(top):
        lines.append(f"- {term}: {c}")

    for cat in ["pain", "outcome", "objection", "trigger", "alternative", "proof"]:
        lines.append(f"\n## Candidate {cat} language")
        examples = buckets.get(cat, [])[:top]
        if not examples:
            lines.append("- No obvious examples found.")
        for s in examples:
            lines.append(f"- {s}")

    lines.append("\n## Copy implications")
    lines.append("- Convert the most repeated pain phrases into problem-section copy.")
    lines.append("- Convert outcome phrases into hero/subhead/value bullets.")
    lines.append("- Convert objections into FAQ and proof requirements.")
    lines.append("- Convert alternatives into comparison copy and switching-path assets.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Mine customer/review text for repeated marketing language.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: path not found: {args.path}", file=sys.stderr)
        return 1
    text = read_text(args.path)
    if not text.strip():
        print("Error: no text found", file=sys.stderr)
        return 1
    output = report(text, args.top)
    if args.out:
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
