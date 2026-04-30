"""
Tests for scripts/pricing_research_analyzer.py.

Includes the edge case I flagged in earlier analysis: grid_from_values
should not crash when min == max (single unique price in input).
"""
from __future__ import annotations

import math

import pytest

from scripts.pricing_research_analyzer import (
    as_float,
    grid_from_values,
    nearest_intersection,
    yes,
)


class TestAsFloat:
    def test_plain_number(self):
        assert as_float("42") == 42.0
        assert as_float("3.14") == 3.14

    def test_currency_strip(self):
        assert as_float("$29") == 29.0
        assert as_float("$1,299") == 1299.0

    def test_blank(self):
        assert as_float("") is None
        assert as_float("  ") is None

    def test_unparseable_default(self):
        assert as_float("custom", default=99.0) == 99.0
        assert as_float("contact us") is None


class TestYes:
    def test_truthy(self):
        for v in ["yes", "y", "Y", "true", "1", "buy", "would buy", "likely"]:
            assert yes(v), f"expected truthy: {v!r}"

    def test_falsy(self):
        for v in ["no", "n", "false", "0", "", "maybe"]:
            assert not yes(v), f"expected falsy: {v!r}"


class TestGridFromValues:
    def test_normal_range(self):
        grid = grid_from_values([10, 50], points=10)
        assert len(grid) == 10
        assert grid[0] == 10.0
        assert grid[-1] == 50.0

    def test_min_equals_max_returns_single_point(self):
        # Edge case: all respondents named the same price.
        grid = grid_from_values([29, 29, 29])
        assert grid == [29]

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            grid_from_values([])

    def test_only_none_raises(self):
        with pytest.raises(ValueError):
            grid_from_values([None, None])  # type: ignore[list-item]

    def test_handles_inf(self):
        # inf should be filtered out, not raise
        grid = grid_from_values([10, 20, float("inf")])
        assert grid[0] == 10.0
        assert grid[-1] == 20.0


class TestNearestIntersection:
    def test_intersect_in_middle(self):
        grid = [float(x) for x in range(0, 11)]
        a = [10.0, 8.0, 6.0, 4.0, 2.0, 0.0, -2.0, -4.0, -6.0, -8.0, -10.0]
        b = [-10.0, -8.0, -6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 8.0, 10.0]
        # They cross at index 5 (price 5).
        price, gap = nearest_intersection(grid, a, b)
        assert price == 5.0
        assert math.isclose(gap, 0.0, abs_tol=0.001)

    def test_single_point_grid_no_crash(self):
        # If grid has 1 point, intersection still works and returns that point.
        grid = [29.0]
        a = [0.5]
        b = [0.5]
        result = nearest_intersection(grid, a, b)
        assert result[0] == 29.0
