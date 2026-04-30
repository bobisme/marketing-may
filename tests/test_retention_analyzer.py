"""
Tests for scripts/retention_analyzer.py.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from scripts.retention_analyzer import cohorted_retention, week_floor, week_index


def _ev(uid: str, event: str, t: datetime, **extra) -> dict:
    return {"user_id": uid, "event": event, "timestamp": t.strftime("%Y-%m-%dT%H:%M:%S"), **extra}


class TestWeekHelpers:
    def test_week_floor_returns_monday(self):
        # 2026-04-30 is a Thursday → week floor is 2026-04-27 (Monday)
        floored = week_floor(datetime(2026, 4, 30, 14, 30))
        assert floored == datetime(2026, 4, 27, 0, 0)

    def test_week_index_zero_for_same_week(self):
        start = datetime(2026, 4, 27)
        same_week = datetime(2026, 4, 30, 14, 0)
        assert week_index(start, same_week) == 0

    def test_week_index_one_for_next_week(self):
        start = datetime(2026, 4, 27)
        next_week = datetime(2026, 5, 4)
        assert week_index(start, next_week) == 1


class TestCohortedRetention:
    def _build_pmf_cohort(self, n: int, base: datetime, weeks: int) -> list:
        """Cohort with strong retention: high week-0, plateau ~30% by week 4+."""
        rows = []
        # Decay schedule that produces a plateau
        probs = [1.0, 0.6, 0.45, 0.36, 0.32, 0.31, 0.30, 0.30, 0.30]
        for i in range(n):
            uid = f"pmf_{i}"
            signup_t = base + timedelta(days=i % 5)  # spread across the week
            rows.append(_ev(uid, "signup_completed", signup_t))
            for w in range(weeks + 1):
                # Deterministic per-user: include user iff (i % 100) < probs[w]*100
                if (i % 100) < int(probs[min(w, len(probs) - 1)] * 100):
                    t = signup_t + timedelta(days=w * 7 + 1)
                    rows.append(_ev(uid, "activation_completed", t))
        return rows

    def test_basic_cohort_size_correct(self):
        rows = self._build_pmf_cohort(n=50, base=datetime(2026, 4, 27), weeks=4)
        out, _ = cohorted_retention(rows, "signup_completed", "activation_completed", weeks=4, group_by=None)
        assert len(out) >= 1  # at least one cohort
        assert int(out[0]["cohort_size"]) == 50

    def test_w0_higher_than_w_late(self):
        rows = self._build_pmf_cohort(n=100, base=datetime(2026, 4, 27), weeks=8)
        out, _ = cohorted_retention(rows, "signup_completed", "activation_completed", weeks=8, group_by=None)
        row = out[0]
        assert float(row["w0"]) > float(row["w8"])

    def test_no_value_event_means_zero_retention(self):
        # Users sign up but never fire value event.
        rows = []
        base = datetime(2026, 4, 27)
        for i in range(40):
            rows.append(_ev(f"u{i}", "signup_completed", base))
        out, _ = cohorted_retention(rows, "signup_completed", "activation_completed", weeks=4, group_by=None)
        assert all(float(out[0][f"w{w}"]) == 0.0 for w in range(5))

    def test_group_by_splits_cohorts(self):
        rows = []
        base = datetime(2026, 4, 27)
        # 30 users on organic, 30 on paid
        for i in range(30):
            rows.append(_ev(f"o{i}", "signup_completed", base, source="organic"))
            rows.append(_ev(f"o{i}", "activation_completed", base + timedelta(days=1), source="organic"))
            rows.append(_ev(f"p{i}", "signup_completed", base, source="paid"))
        out, _ = cohorted_retention(rows, "signup_completed", "activation_completed", weeks=2, group_by="source")
        groups = {r["group"] for r in out}
        assert {"organic", "paid"}.issubset(groups)

    def test_small_cohort_warning(self):
        # 5 users — should produce a "<30 users" warning
        rows = []
        base = datetime(2026, 4, 27)
        for i in range(5):
            rows.append(_ev(f"u{i}", "signup_completed", base))
        _, summary = cohorted_retention(rows, "signup_completed", "activation_completed", weeks=4, group_by=None)
        assert any("<30" in w for w in summary["warnings"])

    def test_invalid_user_skipped(self):
        # User with no signup event but with activation event should not appear.
        rows = [_ev("ghost", "activation_completed", datetime(2026, 4, 30))]
        out, _ = cohorted_retention(rows, "signup_completed", "activation_completed", weeks=4, group_by=None)
        assert out == []
