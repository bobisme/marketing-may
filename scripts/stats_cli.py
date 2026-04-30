#!/usr/bin/env python3
"""
Marketing statistics helper for small teams.

Subcommands:
  sample-size  Required N per arm for an A/B test on a conversion-rate metric (two-proportion).
  srm          Sample-ratio mismatch chi-square check on observed vs expected split.
  bayes        Beta-binomial posterior P(B>A) and expected loss for low-traffic experiments.

Examples:
  python stats_cli.py sample-size --baseline 0.05 --mde 0.20 --power 0.8 --alpha 0.05
  python stats_cli.py srm --observed 4823,5202 --expected 0.5,0.5
  python stats_cli.py bayes --a 412/8000 --b 470/8000

References:
  - Two-proportion sample size: standard pooled normal-approximation formula.
  - SRM threshold: Microsoft ExP conservative default p < 0.0005 (chi^2 > 12.116 for 1 dof).
    Source: Microsoft Research, "Diagnosing Sample Ratio Mismatch in A/B Testing".
  - Bayesian Beta-Binomial: Beta(1+k, 1+n-k) posterior, Monte Carlo P(B>A) and E[loss].
"""

from __future__ import annotations

import argparse
import math
import random
import sys
from typing import List, Tuple


# ---- Inverse normal CDF (Beasley-Springer-Moro) ---------------------------

def normal_quantile(p: float) -> float:
    """Inverse standard normal CDF. Stable to ~1e-9."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0, 1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= phigh:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
               (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = math.sqrt(-2 * math.log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
            ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ---- Sample size ----------------------------------------------------------

def sample_size(baseline: float, mde_rel: float, power: float = 0.8,
                alpha: float = 0.05, two_sided: bool = True) -> int:
    """
    Required N per arm for a two-proportion conversion test.

    baseline: control conversion rate, e.g. 0.05.
    mde_rel:  minimum detectable RELATIVE lift, e.g. 0.20 for +20% (0.05 -> 0.06).
    power:    1 - beta. Default 0.8.
    alpha:    type-1 error. Default 0.05.
    two_sided: alpha is split if true (most common).
    """
    if not 0 < baseline < 1:
        raise ValueError("baseline must be in (0, 1)")
    p1 = baseline
    p2 = baseline * (1 + mde_rel)
    if not 0 < p2 < 1:
        raise ValueError("mde_rel pushes p2 outside (0, 1)")
    z_a = normal_quantile(1 - alpha / 2) if two_sided else normal_quantile(1 - alpha)
    z_b = normal_quantile(power)
    p_bar = (p1 + p2) / 2
    pooled = math.sqrt(2 * p_bar * (1 - p_bar))
    unpooled = math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    num = (z_a * pooled + z_b * unpooled) ** 2
    return math.ceil(num / (p2 - p1) ** 2)


# ---- Sample ratio mismatch -------------------------------------------------

# Microsoft ExP conservative threshold: p < 0.0005, ~ chi^2 > 12.116 for 1 dof.
# We compute p-value from chi^2 directly so the user can see it.
SRM_THRESHOLD_P = 0.0005


def chi_square_p_value_1dof(chi2: float) -> float:
    """Survival function for chi^2 with 1 dof. P(X > chi2) = 2 * (1 - Phi(sqrt(chi2)))."""
    if chi2 <= 0:
        return 1.0
    return 2.0 * (1.0 - normal_cdf(math.sqrt(chi2)))


def srm_check(observed: List[int], expected_share: List[float]) -> Tuple[float, float, str]:
    """
    Returns (chi^2, p-value, verdict).
    """
    if len(observed) != len(expected_share):
        raise ValueError("observed and expected_share must be same length")
    if abs(sum(expected_share) - 1.0) > 1e-6:
        raise ValueError("expected_share must sum to 1.0")
    total = sum(observed)
    if total == 0:
        raise ValueError("observed counts are all zero")
    expected = [s * total for s in expected_share]
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
    # Use 1 dof for 2-arm test; for k arms use k-1 (we approximate with 1 dof p-value
    # since SRM check is most common in 2-arm tests; flag k>2 via stderr below).
    p = chi_square_p_value_1dof(chi2)
    verdict = ("SRM detected (p < 0.0005, Microsoft ExP threshold) — "
               "investigate assignment, logging, bots, or redirect bias before trusting result.") \
        if p < SRM_THRESHOLD_P else \
        f"No SRM signal at p < {SRM_THRESHOLD_P} threshold (p = {p:.5f})."
    return chi2, p, verdict


# ---- Bayesian Beta-Binomial -----------------------------------------------

def parse_ratio(s: str) -> Tuple[int, int]:
    """Parse 'k/n' (e.g., '412/8000') into (k, n)."""
    if "/" not in s:
        raise ValueError(f"expected 'k/n', got {s!r}")
    k, n = s.split("/", 1)
    return int(k), int(n)


def bayes_beta_compare(a: Tuple[int, int], b: Tuple[int, int],
                       samples: int = 200_000, seed: int | None = None) -> dict:
    """
    Monte Carlo posterior comparison of two Beta-Binomial conversion rates.

    Prior: Beta(1, 1) (uniform). For low-N regimes Jeffreys prior Beta(0.5, 0.5)
    would be slightly more conservative; uniform is the most defensible default
    when reporting to a non-technical reader.

    Returns:
      p_b_beats_a   - P(rate_B > rate_A)
      lift_mean     - posterior mean of (B-A)/A
      lift_p05_p95  - 5th/95th percentile of relative lift
      expected_loss_b - E[max(rate_A - rate_B, 0)] in absolute conv rate (cost of choosing B if A is truly better)
    """
    if seed is not None:
        random.seed(seed)
    ka, na = a
    kb, nb = b
    if ka < 0 or na <= 0 or kb < 0 or nb <= 0 or ka > na or kb > nb:
        raise ValueError("a and b must satisfy 0 <= k <= n with n > 0")

    wins = 0
    lifts: List[float] = []
    loss_b_total = 0.0
    for _ in range(samples):
        # Beta(1+k, 1+n-k) is the Bayesian posterior under Beta(1,1) prior
        sa = random.betavariate(1 + ka, 1 + na - ka)
        sb = random.betavariate(1 + kb, 1 + nb - kb)
        if sb > sa:
            wins += 1
        if sa > 0:
            lifts.append((sb - sa) / sa)
        loss_b_total += max(sa - sb, 0.0)

    lifts.sort()
    p_b = wins / samples
    return {
        "p_b_beats_a": p_b,
        "control_rate_point": ka / na,
        "variant_rate_point": kb / nb,
        "lift_mean": sum(lifts) / len(lifts) if lifts else 0.0,
        "lift_p05": lifts[int(0.05 * len(lifts))] if lifts else 0.0,
        "lift_p95": lifts[int(0.95 * len(lifts))] if lifts else 0.0,
        "expected_loss_b_abs": loss_b_total / samples,
        "samples": samples,
    }


# ---- CLI ------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sample-size", help="Required N per arm for a conversion-rate A/B test.")
    s.add_argument("--baseline", type=float, required=True, help="baseline conversion rate, e.g. 0.05")
    s.add_argument("--mde", type=float, required=True, help="minimum detectable RELATIVE lift, e.g. 0.20 = +20%%")
    s.add_argument("--power", type=float, default=0.8)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--one-sided", action="store_true")

    r = sub.add_parser("srm", help="Sample ratio mismatch chi-square check.")
    r.add_argument("--observed", required=True, help="comma-separated counts, e.g. 4823,5202")
    r.add_argument("--expected", required=True, help="comma-separated shares, e.g. 0.5,0.5")

    b = sub.add_parser("bayes", help="Bayesian Beta-Binomial comparison for low-traffic tests.")
    b.add_argument("--a", required=True, help="control as k/n, e.g. 412/8000")
    b.add_argument("--b", required=True, help="variant as k/n, e.g. 470/8000")
    b.add_argument("--samples", type=int, default=200_000)
    b.add_argument("--seed", type=int, default=None)

    args = parser.parse_args()

    if args.cmd == "sample-size":
        try:
            n = sample_size(args.baseline, args.mde, args.power, args.alpha,
                            two_sided=not args.one_sided)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"Required N per arm: {n}")
        print(f"Total N (2 arms): {2 * n}")
        weeks_at = lambda traffic: math.ceil(2 * n / traffic) if traffic > 0 else None
        print()
        print("Reality check — weeks of testing at common weekly traffic levels:")
        for t in (1_000, 5_000, 20_000, 100_000):
            print(f"  {t:>7,} qualified visitors/week -> ~{weeks_at(t)} weeks")
        if 2 * n > 100_000:
            print()
            print("Note: this exceeds typical small-team traffic. Consider:")
            print("  1) Sharper qualitative tests (5-second, problem interview, fake door).")
            print("  2) A larger MDE — only test wins big enough to act on.")
            print("  3) Bayesian small-N approach: `stats_cli.py bayes` and stop when P(B>A) > 0.95.")
        return 0

    if args.cmd == "srm":
        try:
            obs = [int(x) for x in args.observed.split(",")]
            exp = [float(x) for x in args.expected.split(",")]
            chi2, p, verdict = srm_check(obs, exp)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"observed: {obs}")
        print(f"expected: {[round(s * sum(obs), 1) for s in exp]}")
        print(f"chi^2 = {chi2:.3f}")
        print(f"p-value (1 dof) ≈ {p:.5f}")
        print(verdict)
        if len(obs) > 2:
            print("Note: p-value uses 1-dof approximation; for k arms a chi^2 with k-1 dof is correct. "
                  "Treat this as directional for k>2.", file=sys.stderr)
        return 0

    if args.cmd == "bayes":
        try:
            a = parse_ratio(args.a)
            b_ = parse_ratio(args.b)
            result = bayes_beta_compare(a, b_, samples=args.samples, seed=args.seed)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        print(f"Control A: {a[0]}/{a[1]} = {result['control_rate_point']:.4f}")
        print(f"Variant B: {b_[0]}/{b_[1]} = {result['variant_rate_point']:.4f}")
        print(f"P(B > A)  ≈ {result['p_b_beats_a']:.4f}  ({result['samples']:,} samples)")
        print(f"Posterior relative lift: mean = {result['lift_mean']:+.2%}, "
              f"5–95% CrI = [{result['lift_p05']:+.2%}, {result['lift_p95']:+.2%}]")
        print(f"Expected loss if you pick B and A is truly better: "
              f"{result['expected_loss_b_abs']:.5f} abs conversion rate")
        # Decision aid
        if result["p_b_beats_a"] >= 0.95:
            print("Decision aid: P(B>A) ≥ 0.95 — ship B if guardrails are clean and SRM check passes.")
        elif result["p_b_beats_a"] <= 0.05:
            print("Decision aid: P(B>A) ≤ 0.05 — A is winning; do not ship B.")
        elif min(a[1], b_[1]) < 200:
            print("Decision aid: inconclusive AND sample sizes are small (<200/arm). "
                  "Collect more or rely on qualitative signal.")
        else:
            print("Decision aid: inconclusive. Continue collecting, or call it a tie and pick on cost/strategy.")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
