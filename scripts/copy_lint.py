#!/usr/bin/env python3
"""
Lint marketing copy against the empirical-marketing quality checklist.

Catches:
  - Vague adjectives that signal nothing ("powerful", "seamless", "world-class").
  - Unsupported superlative claims with no number, named customer, or proof nearby.
  - Dark-pattern urgency / scarcity language without a real date.
  - Missing call-to-action verbs.
  - Hidden price signals ("starting at" with no number).
  - Weak social-proof phrasing ("trusted by thousands" without a count).
  - Buzzword density (signal-to-noise floor).

Usage:
  python copy_lint.py landing.md
  python copy_lint.py --dir copy/
  python copy_lint.py landing.md --json

Suppress an individual finding by appending a comment on the same line:
  Our amazing platform.   <!-- lint:ignore vague-adjective -->

Exit code: 0 if no findings, 1 if findings, 2 on error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List


# --- Patterns ---------------------------------------------------------------

VAGUE_ADJECTIVES = [
    # The classics that copywriting guides flag in 2026.
    "amazing", "powerful", "seamless", "robust", "world.?class", "next.?gen",
    "cutting.?edge", "revolutionary", "game.?changing", "innovative", "synergy",
    "leverage", "premier", "leading edge", "best.?in.?class", "all.?in.?one",
    "intuitive", "user.?friendly", "scalable solutions?", "enterprise.?grade",
    "state.?of.?the.?art", "frictionless", "effortless", "delightful",
    "supercharge", "reimagined", "unleash", "elevate your", "transform your",
]
VAGUE_RE = re.compile(r"\b(?:" + "|".join(VAGUE_ADJECTIVES) + r")\b", re.IGNORECASE)

# Superlative / authority claims that need substantiation.
SUPERLATIVE_RE = re.compile(
    r"\b(guaranteed|fastest|safest|cheapest|best|leading|top.?rated|"
    r"#\s*1|number one|industry.?leading|trusted by (?:thousands|millions)|"
    r"loved by (?:thousands|millions)|millions of users)\b",
    re.IGNORECASE,
)

# Dark-pattern urgency. We allow it only if a real date or specific number follows nearby.
URGENCY_RE = re.compile(
    r"\b(only \d+ left|hurry|act now|limited time|expires in|"
    r"selling fast|don'?t miss out|last chance)\b",
    re.IGNORECASE,
)
_MONTHS = (r"(?:January|February|March|April|May|June|July|August|"
           r"September|October|November|December|"
           r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)")
DATE_NEAR_RE = re.compile(
    r"\b(?:" + _MONTHS + r"\s+\d{1,2}(?:,\s*\d{4})?|"
    r"\d{4}-\d{2}-\d{2}|"
    r"\d{1,2}/\d{1,2}/\d{2,4}|"
    r"by \d{1,2}(?::\d{2})?\s*(?:am|pm))\b",
)

# CTA verbs we accept as valid imperative actions.
CTA_VERB_RE = re.compile(
    r"\b(book|start|try|get|see|request|join|sign up|sign-up|signup|"
    r"download|claim|talk|schedule|demo|buy|order|create|build|launch|"
    r"watch|view|read|learn how|read the|reserve|install)\b",
    re.IGNORECASE,
)

# "Starting at" with no number nearby.
HIDDEN_PRICE_RE = re.compile(r"starting at(?!\s*(?:\$|€|£|¥|just|only)?\s*\d)", re.IGNORECASE)

# "Trusted by thousands" with no count.
WEAK_SOCIAL_PROOF_RE = re.compile(
    r"\b(trusted|loved|chosen|used) by (?!\d|over\s*\d|more than\s*\d)\w+",
    re.IGNORECASE,
)

# Lint suppression: <!-- lint:ignore <rule> --> or # lint:ignore <rule>
# Non-greedy capture so the trailing `-->` doesn't get eaten as part of a rule name.
IGNORE_RE = re.compile(
    r"(?:<!--|#|//)\s*lint:ignore\s+(.+?)\s*(?:-->|$)",
    re.IGNORECASE | re.MULTILINE,
)


# --- Findings ---------------------------------------------------------------

@dataclass
class Finding:
    file: str
    line: int
    rule: str
    snippet: str
    fix: str

    def fmt(self) -> str:
        return f"{self.file}:{self.line}: {self.rule}: '{self.snippet}' — {self.fix}"


# --- Per-line linters -------------------------------------------------------

PROOF_NEAR_WINDOW = 120  # chars

def _has_proof_near(text: str, idx_start: int, idx_end: int) -> bool:
    """Return True if a number, currency, named customer, or 'case study' appears nearby."""
    lo = max(0, idx_start - PROOF_NEAR_WINDOW)
    hi = min(len(text), idx_end + PROOF_NEAR_WINDOW)
    window = text[lo:hi]
    if re.search(r"\d", window):
        return True
    if re.search(r"\bcase study\b|\bcase-study\b", window, re.IGNORECASE):
        return True
    # Named entity heuristic: ≥ 2 consecutive Capitalized words (e.g., "Acme Corp")
    if re.search(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b", window):
        return True
    return False


def lint_text(text: str, file: str = "<text>") -> List[Finding]:
    findings: List[Finding] = []
    lines = text.splitlines()

    # Pre-build ignored set per line
    ignores_by_line: dict[int, set[str]] = {}
    for i, line in enumerate(lines, start=1):
        for m in IGNORE_RE.finditer(line):
            rules = {r.strip() for r in m.group(1).split(",") if r.strip()}
            ignores_by_line[i] = rules

    def emit(line_no: int, rule: str, snippet: str, fix: str):
        if rule in ignores_by_line.get(line_no, set()):
            return
        findings.append(Finding(file=file, line=line_no, rule=rule, snippet=snippet, fix=fix))

    # Per-line scans
    for i, line in enumerate(lines, start=1):
        for m in VAGUE_RE.finditer(line):
            emit(i, "vague-adjective", m.group(0),
                 "quantify (numbers, named customer, time saved) or remove")

        for m in SUPERLATIVE_RE.finditer(line):
            # Check for proof in the same paragraph (~120 char window)
            if not _has_proof_near(line, m.start(), m.end()):
                emit(i, "unsupported-claim", m.group(0),
                     "add a number, named customer, or case study within the same section, or weaken to a testable promise")

        for m in URGENCY_RE.finditer(line):
            window = line[max(0, m.start()-60): m.end()+60]
            if not DATE_NEAR_RE.search(window):
                emit(i, "dark-pattern", m.group(0),
                     "remove the urgency or attach a real date / specific count")

        if HIDDEN_PRICE_RE.search(line):
            emit(i, "hidden-price", "starting at",
                 "show the actual entry price; 'starting at' with no number signals hiding")

        for m in WEAK_SOCIAL_PROOF_RE.finditer(line):
            emit(i, "weak-social-proof", m.group(0),
                 "specify the count ('over 3,800 teams') or name a customer")

    # Whole-text scans
    if not CTA_VERB_RE.search(text):
        findings.append(Finding(file=file, line=0, rule="missing-cta",
                                snippet="(whole document)",
                                fix="no imperative call-to-action verb found in the entire document"))

    # Buzzword density: vague adjectives per 100 words. > 1.5 is high.
    word_count = max(1, len(re.findall(r"\b\w+\b", text)))
    vague_count = len(VAGUE_RE.findall(text))
    if vague_count >= 3 and (vague_count / word_count) * 100 > 1.5:
        findings.append(Finding(
            file=file, line=0, rule="buzzword-density",
            snippet=f"{vague_count} vague adjectives in {word_count} words "
                    f"({(vague_count/word_count)*100:.1f} per 100 words)",
            fix="cut by ~half; replace with concrete buyer language from interviews/reviews",
        ))

    return findings


# --- File walking -----------------------------------------------------------

LINTABLE_SUFFIXES = {".md", ".txt", ".html", ".mdx"}


def iter_files(path: Path, recursive: bool) -> Iterable[Path]:
    if path.is_file():
        yield path
        return
    if not path.is_dir():
        return
    pattern = "**/*" if recursive else "*"
    for p in sorted(path.glob(pattern)):
        if p.is_file() and p.suffix.lower() in LINTABLE_SUFFIXES:
            yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint marketing copy against quality checklist.")
    parser.add_argument("path", type=Path, help="file or directory")
    parser.add_argument("--dir", action="store_true",
                        help="treat path as a directory and lint all .md/.txt/.html (recursive)")
    parser.add_argument("--json", action="store_true", help="output JSON instead of text")
    parser.add_argument("--rule", action="append", default=None,
                        help="only show findings for this rule (repeatable)")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"Error: path not found: {args.path}", file=sys.stderr)
        return 2

    files = list(iter_files(args.path, recursive=args.dir or args.path.is_dir()))
    if not files:
        print(f"No lintable files found at {args.path}", file=sys.stderr)
        return 2

    all_findings: List[Finding] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            print(f"{f}: skipped ({e})", file=sys.stderr)
            continue
        findings = lint_text(text, file=str(f))
        if args.rule:
            findings = [x for x in findings if x.rule in set(args.rule)]
        all_findings.extend(findings)

    if args.json:
        print(json.dumps([asdict(x) for x in all_findings], indent=2))
    else:
        for x in all_findings:
            print(x.fmt())
        if all_findings:
            print(f"\n{len(all_findings)} finding(s) across {len(files)} file(s).", file=sys.stderr)
        else:
            print(f"Clean: 0 findings across {len(files)} file(s).", file=sys.stderr)

    return 1 if all_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
