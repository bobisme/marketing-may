"""
Tests for scripts/outbound_list_scorer.py — focuses on recency-bounded triggers
and negative penalties, the two pieces most likely to silently misbehave.
"""
from __future__ import annotations

from datetime import datetime

from scripts.outbound_list_scorer import (
    matches_in,
    matches_range,
    matches_trigger_present,
    score_row,
)


def _icp(criteria=None, negatives=None, tier_thresholds=None):
    return {
        "criteria": criteria or [],
        "negatives": negatives or [],
        "tier_thresholds": tier_thresholds or {"A": 0.70, "B": 0.45},
    }


class TestMatchers:
    def test_in_match_case_insensitive(self):
        assert matches_in("US", ["us", "ca"])
        assert matches_in("us", ["US", "CA"])
        assert not matches_in("FR", ["US", "CA"])

    def test_range_matches(self):
        assert matches_range("85", [10, 200])
        assert not matches_range("5", [10, 200])
        assert not matches_range("not a number", [10, 200])

    def test_range_with_suffixes(self):
        # 1.5M should parse as 1_500_000
        assert matches_range("1.5M", [1_000_000, 5_000_000])
        assert matches_range("10k", [5_000, 50_000])


class TestTriggerRecency:
    def test_recent_trigger_within_window(self):
        now = datetime(2026, 4, 30)
        row = {"trigger_funding": "Series A", "trigger_funding_date": "2026-03-15"}
        assert matches_trigger_present("Series A", recency_check=True, row=row,
                                       recency_field="trigger_funding_date",
                                       recency_days=90, now=now)

    def test_old_trigger_outside_window_does_not_match(self):
        now = datetime(2026, 4, 30)
        row = {"trigger_funding": "Series A", "trigger_funding_date": "2025-10-01"}
        assert not matches_trigger_present("Series A", recency_check=True, row=row,
                                           recency_field="trigger_funding_date",
                                           recency_days=90, now=now)

    def test_no_recency_check_passes_with_value(self):
        now = datetime(2026, 4, 30)
        row = {"trigger_funding": "Series A"}
        assert matches_trigger_present("Series A", recency_check=False, row=row,
                                       recency_field=None, recency_days=None, now=now)

    def test_empty_value_never_matches(self):
        now = datetime(2026, 4, 30)
        row = {}
        assert not matches_trigger_present("", recency_check=False, row=row,
                                           recency_field=None, recency_days=None, now=now)

    def test_falsy_strings_never_match(self):
        now = datetime(2026, 4, 30)
        row = {}
        for v in ["no", "false", "0", "none", "n/a"]:
            assert not matches_trigger_present(v, recency_check=False, row=row,
                                               recency_field=None, recency_days=None, now=now), v


class TestScoreRow:
    def test_perfect_match_100_pct(self):
        icp = _icp(criteria=[
            {"field": "industry", "kind": "exact", "match": "B2B SaaS", "weight": 5},
            {"field": "country", "kind": "in", "match": ["US"], "weight": 2},
        ])
        row = {"industry": "B2B SaaS", "country": "US"}
        result = score_row(row, icp, datetime(2026, 4, 30))
        assert result["_score_pct"] == 100.0
        assert result["_tier"] == "A"

    def test_no_match_zero_score(self):
        icp = _icp(criteria=[
            {"field": "industry", "kind": "exact", "match": "Fintech", "weight": 5},
        ])
        row = {"industry": "Logistics"}
        result = score_row(row, icp, datetime(2026, 4, 30))
        assert result["_score_pct"] == 0.0
        assert result["_tier"] == "C"

    def test_negative_penalty_demotes_tier(self):
        icp = _icp(
            criteria=[{"field": "industry", "kind": "exact", "match": "B2B SaaS", "weight": 5}],
            negatives=[{"field": "industry", "kind": "in", "match": ["consulting"], "penalty": 10}],
        )
        # Match the criteria AND hit the negative — score is negative, normalized to 0.
        row = {"industry": "B2B SaaS"}  # only matches positive
        good = score_row(row, icp, datetime(2026, 4, 30))
        assert good["_tier"] == "A"

        bad_row = {"industry": "consulting"}  # hits negative, no positive
        bad = score_row(bad_row, icp, datetime(2026, 4, 30))
        assert bad["_score"] < 0
        # Normalized score floors at 0
        assert bad["_score_pct"] == 0.0

    def test_recency_excluded_trigger_not_credited(self):
        # Series A funded 6 months ago — outside 90-day window → no credit
        icp = _icp(criteria=[
            {"field": "trigger_funding", "kind": "trigger_present", "weight": 4,
             "recency_days": 90, "recency_field": "trigger_funding_date"},
        ])
        row = {"trigger_funding": "Series A", "trigger_funding_date": "2025-10-01"}
        result = score_row(row, icp, datetime(2026, 4, 30))
        # No credit — score should be 0.
        assert result["_score"] == 0
        assert "  0  trigger_funding=Series A" in result["_why"]

    def test_recency_within_window_credited(self):
        icp = _icp(criteria=[
            {"field": "trigger_funding", "kind": "trigger_present", "weight": 4,
             "recency_days": 90, "recency_field": "trigger_funding_date"},
        ])
        row = {"trigger_funding": "Series A", "trigger_funding_date": "2026-03-15"}
        result = score_row(row, icp, datetime(2026, 4, 30))
        assert result["_score"] == 4
        assert "+4 trigger_funding=Series A" in result["_why"]

    def test_tier_thresholds_respected(self):
        icp = _icp(
            criteria=[
                {"field": "f1", "kind": "exact", "match": "x", "weight": 5},
                {"field": "f2", "kind": "exact", "match": "x", "weight": 5},
            ],
            tier_thresholds={"A": 0.80, "B": 0.40},
        )
        # 5/10 = 50% → B tier
        b_row = {"f1": "x", "f2": "y"}
        assert score_row(b_row, icp, datetime(2026, 4, 30))["_tier"] == "B"
        # 10/10 = 100% → A tier
        a_row = {"f1": "x", "f2": "x"}
        assert score_row(a_row, icp, datetime(2026, 4, 30))["_tier"] == "A"
        # 0/10 = 0% → C tier
        c_row = {"f1": "y", "f2": "y"}
        assert score_row(c_row, icp, datetime(2026, 4, 30))["_tier"] == "C"
