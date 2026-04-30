"""
Tests for scripts/funnel_analyzer.py.

The crucial invariant: a user only counts at step N if they completed steps 1..N
in chronological order. Out-of-order events should NOT credit later steps.
"""
from __future__ import annotations

from scripts.funnel_analyzer import user_completed_steps


def _e(event: str, ts: str) -> dict:
    return {"event": event, "timestamp": ts}


class TestUserCompletedSteps:
    def test_in_order_full_funnel(self):
        events = [
            _e("page_view", "2026-01-01T10:00:00"),
            _e("signup", "2026-01-01T10:05:00"),
            _e("activation", "2026-01-02T09:00:00"),
        ]
        n = user_completed_steps(events, ["page_view", "signup", "activation"])
        assert n == 3

    def test_partial_funnel(self):
        events = [
            _e("page_view", "2026-01-01T10:00:00"),
            _e("signup", "2026-01-01T10:05:00"),
        ]
        n = user_completed_steps(events, ["page_view", "signup", "activation"])
        assert n == 2

    def test_out_of_order_does_not_credit_later_step(self):
        # Activation fired before signup - should NOT credit step 2.
        events = [
            _e("page_view", "2026-01-01T10:00:00"),
            _e("activation", "2026-01-01T10:01:00"),  # before signup
            _e("signup", "2026-01-01T10:05:00"),
        ]
        n = user_completed_steps(events, ["page_view", "signup", "activation"])
        # Should count: page_view ok, signup ok (after page_view), activation ok (after signup chronologically? No — activation is at 10:01, signup is at 10:05)
        # Sort by timestamp: page_view, activation, signup → walk: page_view matches step 1, activation doesn't match step 2 (signup), signup matches step 2. Done. n=2.
        assert n == 2

    def test_no_matching_events(self):
        events = [_e("other", "2026-01-01T10:00:00")]
        assert user_completed_steps(events, ["page_view"]) == 0

    def test_empty_events(self):
        assert user_completed_steps([], ["page_view"]) == 0

    def test_repeated_event_only_counts_once(self):
        events = [
            _e("page_view", "2026-01-01T10:00:00"),
            _e("page_view", "2026-01-01T10:01:00"),
            _e("signup", "2026-01-01T10:05:00"),
        ]
        n = user_completed_steps(events, ["page_view", "signup"])
        assert n == 2

    def test_step_skipped_does_not_advance(self):
        # User did page_view and activation but never signup.
        events = [
            _e("page_view", "2026-01-01T10:00:00"),
            _e("activation", "2026-01-02T09:00:00"),
        ]
        n = user_completed_steps(events, ["page_view", "signup", "activation"])
        assert n == 1  # only page_view counts
