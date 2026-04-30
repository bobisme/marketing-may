# Statistics Primer for Small Teams

Load when planning, refusing, or interpreting an A/B test, or when checking the integrity of a recently-shipped experiment.

## Quick reference — cite these by name in responses

| Rule | Threshold | Source |
|---|---|---|
| Frequentist sample size (two-prop) | `n ≈ ((z_{α/2}·√(2·p̄·(1-p̄)) + z_β·√(p₁(1-p₁)+p₂(1-p₂)))²) / (p₂-p₁)²` | `scripts/stats_cli.py sample-size` |
| **Refuse frequentist A/B if total N > 50,000** | switch to Bayesian sequential or qualitative tests | This file, "Decision" section |
| Bayesian ship rule | `P(B > A) ≥ 0.95` AND guardrails clean | `scripts/stats_cli.py bayes` |
| Bayesian keep-A rule | `P(B > A) ≤ 0.05` | same |
| **SRM threshold (Microsoft ExP)** | `p < 0.0005` (chi² > 12.116 for 1 dof) | Microsoft Research |
| Default α / power | 0.05 / 0.80 | Standard |
| Minimum useful MDE (relative) | 10–30%; <10% rarely worth small-team cost | This file |
| Tiny-sample warning | < 100 events/arm in Bayesian → posterior dominated by prior; treat as directional | This file |
| Test time-cap | If inconclusive at pre-set N or date, declare "no detectable lift" and move on | This file |

When sample-size math says "more weeks than the company will tolerate," the answer is not "run the test anyway." It is "this question is not A/B-testable at our traffic — pick a cheaper test or a bigger swing."

The skill's audience is technical founders and small teams. Their three most expensive statistics mistakes:

1. **Running A/B tests without enough traffic** — calling underpowered noise a "winner."
2. **Skipping the SRM check** — trusting a test where assignment was broken.
3. **Choosing significance over decision** — declaring a p-value without a decision rule.

This primer maps each problem to a tool and a default. Run `scripts/stats_cli.py` for the math.

## Decision: should we run a frequentist A/B test at all?

```text
Compute required N per arm with `stats_cli.py sample-size`.
├── Required N ≤ ~2 weeks of qualified traffic
│   └── Run the test. Pre-register threshold and decision rule.
├── Required N is 2–8 weeks
│   └── Run the test if the question is worth a month of traffic.
│       Otherwise, raise the MDE you'd act on, or pick a sharper test.
└── Required N > 8 weeks (typical for low-traffic indie teams)
    └── DO NOT A/B test this question. Use one of:
        - Sequential Bayesian: `stats_cli.py bayes`, stop at P(B>A) ≥ 0.95.
        - Qualitative tests: 5-second, problem interview, fake door.
        - Big-swing changes that don't need a test (clear improvement on principle).
```

Rule of thumb: if you wouldn't ship the change just because someone you trust pointed it out, the test isn't worth running with weak power either.

## Sample size — the formula and what it means

For a two-proportion conversion test:

```text
n_per_arm = ((z_{alpha/2} * sqrt(2 * p_bar * (1 - p_bar))
              + z_{beta}   * sqrt(p1*(1-p1) + p2*(1-p2)))^2)
            / (p2 - p1)^2

p_bar = (p1 + p2) / 2
p2 = p1 * (1 + MDE_rel)
```

Inputs you actually choose:

| Input | Common default | Notes |
|---|---|---|
| Baseline conversion `p1` | from your data | Use the cleanest 30-day window. |
| Minimum detectable effect (relative) | 10–30% | Below 10%: rarely worth detecting at small-team cost. |
| Power (1-β) | 0.80 | Lower power = more false negatives. |
| Significance α | 0.05 | Two-sided unless you really only care about one direction. |

Anti-pattern: setting MDE = 1% relative because you "want to detect any improvement." This makes the test impossibly expensive and produces underpowered results that get reported as wins anyway.

## Sample ratio mismatch (SRM) — a precondition, not a guardrail

SRM occurs when assignment doesn't actually produce the split you configured (e.g., you chose 50/50 but observed 5500/4500). Without an SRM check, the rest of your stats are suspect.

Microsoft's experimentation platform reports that **6–10% of A/B tests** have SRM. Common causes:

- Bot or pre-render traffic hitting only one variant.
- Redirect-induced loss in one arm.
- Logging filter that drops users in one arm.
- Sticky-bucket-then-reassign bug.
- Variant only renders on a subset of devices/browsers.

**Default threshold:** Microsoft ExP uses **p < 0.0005** (chi² > ~12.12 for 1 dof) for a 2-arm test. Lukas Vermeer's checker and most public guides use **p < 0.01** as a more permissive default. The conservative threshold is right when you'd rather investigate a false positive than ship a real bug.

```text
Run `stats_cli.py srm --observed N1,N2 --expected 0.5,0.5`.

p < 0.0005  → assume SRM. Find the cause before reading any other metric.
p ≥ 0.0005  → proceed to read the experiment, but log p in your post-test memo.
```

If SRM is detected, **diagnosis is harder than detection** — log every event, every redirect, every filter, and look for the smallest unit (variant × device × browser × geo) where the imbalance lives.

## Bayesian small-traffic mode

When a frequentist test would need months of traffic, switch frames. The Beta-Binomial model gives a posterior on each variant's true rate after every batch of users.

`stats_cli.py bayes` reports:

- `P(B > A)` — posterior probability that B's true rate exceeds A's.
- Posterior mean and 5–95% credible interval of relative lift.
- Expected loss if you ship B and A is truly better.

**Stopping rule defaults:**

| Threshold | Action |
|---|---|
| `P(B > A) ≥ 0.95` | Ship B (after SRM and guardrail check). |
| `P(B > A) ≤ 0.05` | Keep A. |
| Otherwise | Keep collecting. |

Caveats:

- Sequential peeking is allowed under Bayesian — that's the point — but a stopping threshold of 0.95 is not equivalent to frequentist α = 0.05. You're trading off type-1 error for the ability to make decisions early. Use `expected_loss` to size the bet, not just `P(B > A)`.
- Beta(1, 1) (uniform) prior is the default. With < 100 events per arm, the posterior is dominated by the prior — be honest that the test is directional, not conclusive.
- **Bayesian does not rescue you from SRM.** Always SRM-check first.

## Guardrails — what to track besides the headline metric

Every experiment should pre-register at least one guardrail metric. Common ones:

| Headline change | Guardrail |
|---|---|
| Pricing page test | Refunds, cancellations, support tickets, deal size |
| Onboarding test | Activation rate, support volume, NPS, retention by cohort |
| Hero rewrite | Bounce rate, demo-request rate, qualified-meeting rate |
| Outbound copy test | Reply quality (replies that book, not "unsubscribe") |
| Free-trial length | Trial-to-paid, paid retention at 90 days |

A "win" on the headline that degrades a guardrail is not a win.

## Decision rules, pre-registered

Write these BEFORE the test starts. Format:

```text
If [primary metric] reaches [threshold] AND [guardrail] does not degrade > [margin],
  we will [ship / keep / iterate].
If results are inconclusive after [date or sample],
  we will [stop / extend / pivot test].
```

Without pre-registration, "winning" is whatever shape the team wants after seeing the data.

## When NOT to use this primer

- **Volume-based metrics** (revenue per visitor, sessions per user) need different machinery — t-tests with log transforms or bootstrap. The CLI here is for proportions only.
- **Multi-arm tests** with > 2 variants need multiple comparisons correction (Bonferroni or sequential Holm). The CLI's SRM check approximates with 1 dof; for k arms run a proper chi-square at k-1 dof.
- **Causal/observational** questions ("did the new docs page cause growth?") need DiD, regression discontinuity, or matched cohorts — not A/B math.

## References

- Microsoft Research, "Diagnosing Sample Ratio Mismatch in A/B Testing" — source of the p < 0.0005 default and the 6–10% SRM prevalence figure.
- Kohavi, Tang, Xu, *Trustworthy Online Controlled Experiments* — guardrails, SRM, peeking, decision rules.
- Evan Miller, "Sample Size Calculator" and "Formulas for Bayesian A/B Testing" — formula sources.
- Optimizely Support, "Understand your Experiment Scorecard" — guardrail vs decision metric framing.
