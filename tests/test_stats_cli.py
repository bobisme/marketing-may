"""
Tests for scripts/stats_cli.py.

Reference values:
- sample_size for p1=0.05, mde_rel=0.20, power=0.8, alpha=0.05 (two-sided)
  → ~8158 per arm. Using a wide range because different calculators (Evan Miller,
    Statsig, Optimizely) differ slightly based on pooled vs unpooled variance.
- SRM: chi^2 > ~12.12 corresponds to Microsoft's p < 0.0005 threshold.
"""
from __future__ import annotations

import math
import pytest

from scripts.stats_cli import (
    bayes_beta_compare,
    chi_square_p_value_1dof,
    normal_cdf,
    normal_quantile,
    sample_size,
    srm_check,
)


class TestNormal:
    def test_quantile_known_values(self):
        assert math.isclose(normal_quantile(0.975), 1.96, abs_tol=0.01)
        assert math.isclose(normal_quantile(0.5), 0.0, abs_tol=0.01)
        assert math.isclose(normal_quantile(0.84), 0.994, abs_tol=0.01)

    def test_quantile_invalid_raises(self):
        with pytest.raises(ValueError):
            normal_quantile(0.0)
        with pytest.raises(ValueError):
            normal_quantile(1.0)

    def test_cdf_known_values(self):
        assert math.isclose(normal_cdf(0.0), 0.5, abs_tol=0.001)
        assert math.isclose(normal_cdf(1.96), 0.975, abs_tol=0.001)
        assert math.isclose(normal_cdf(-1.96), 0.025, abs_tol=0.001)


class TestSampleSize:
    def test_canonical_5pct_baseline_20pct_mde(self):
        n = sample_size(0.05, 0.20, power=0.8, alpha=0.05)
        # Pooled-formula yields ~8158; allow tolerance for variant calculators.
        assert 7000 < n < 9500, f"expected ~8158, got {n}"

    def test_larger_baseline_smaller_n(self):
        n_small = sample_size(0.05, 0.20)
        n_large = sample_size(0.20, 0.20)
        assert n_large < n_small

    def test_smaller_mde_larger_n(self):
        n_easy = sample_size(0.10, 0.50)
        n_hard = sample_size(0.10, 0.05)
        assert n_hard > n_easy * 50  # ~100x more data for 10x smaller effect

    def test_one_sided_smaller_n(self):
        n_two = sample_size(0.05, 0.20, two_sided=True)
        n_one = sample_size(0.05, 0.20, two_sided=False)
        assert n_one < n_two

    def test_invalid_baseline(self):
        with pytest.raises(ValueError):
            sample_size(0.0, 0.2)
        with pytest.raises(ValueError):
            sample_size(1.0, 0.2)

    def test_mde_pushes_p2_outside(self):
        with pytest.raises(ValueError):
            sample_size(0.5, 1.5)  # p2 = 1.25, invalid


class TestSRM:
    def test_clean_split(self):
        chi2, p, verdict = srm_check([4980, 5020], [0.5, 0.5])
        assert chi2 < 1.0
        assert p > 0.5
        assert "No SRM signal" in verdict

    def test_broken_split(self):
        chi2, p, verdict = srm_check([5500, 4500], [0.5, 0.5])
        assert chi2 > 12.12  # Microsoft p<0.0005 threshold
        assert p < 0.0005
        assert "SRM detected" in verdict

    def test_uneven_expected_clean(self):
        chi2, p, _ = srm_check([1000, 9000], [0.1, 0.9])
        assert chi2 < 1.0
        assert p > 0.5

    def test_zero_total_raises(self):
        with pytest.raises(ValueError):
            srm_check([0, 0], [0.5, 0.5])

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError):
            srm_check([100, 100], [0.5, 0.5, 0.0])

    def test_expected_share_not_summing_to_1_raises(self):
        with pytest.raises(ValueError):
            srm_check([100, 100], [0.5, 0.6])

    def test_chi2_pvalue_consistency(self):
        # chi^2 = 0 → p = 1
        assert math.isclose(chi_square_p_value_1dof(0.0), 1.0, abs_tol=0.001)
        # chi^2 = 3.84 (alpha=0.05 critical) → p ≈ 0.05
        assert math.isclose(chi_square_p_value_1dof(3.84), 0.05, abs_tol=0.005)


class TestBayes:
    def test_clear_winner(self):
        # B is clearly better: 5.9% vs 5.15% on 8000/arm
        result = bayes_beta_compare((412, 8000), (470, 8000), samples=20_000, seed=42)
        assert result["p_b_beats_a"] > 0.95

    def test_clear_loser(self):
        result = bayes_beta_compare((470, 8000), (412, 8000), samples=20_000, seed=42)
        assert result["p_b_beats_a"] < 0.05

    def test_tie(self):
        result = bayes_beta_compare((400, 8000), (400, 8000), samples=20_000, seed=42)
        assert 0.4 < result["p_b_beats_a"] < 0.6

    def test_seed_determinism(self):
        r1 = bayes_beta_compare((100, 1000), (110, 1000), samples=10_000, seed=99)
        r2 = bayes_beta_compare((100, 1000), (110, 1000), samples=10_000, seed=99)
        assert r1["p_b_beats_a"] == r2["p_b_beats_a"]

    def test_low_n_inconclusive(self):
        # 12/200 vs 18/200 — directionally B but should not be near 1.0
        result = bayes_beta_compare((12, 200), (18, 200), samples=20_000, seed=42)
        assert 0.7 < result["p_b_beats_a"] < 0.95

    def test_invalid_inputs_raise(self):
        with pytest.raises(ValueError):
            bayes_beta_compare((10, 0), (5, 100))  # n=0
        with pytest.raises(ValueError):
            bayes_beta_compare((50, 10), (5, 100))  # k > n

    def test_credible_interval_bounds(self):
        result = bayes_beta_compare((100, 1000), (130, 1000), samples=20_000, seed=42)
        assert result["lift_p05"] < result["lift_mean"] < result["lift_p95"]
