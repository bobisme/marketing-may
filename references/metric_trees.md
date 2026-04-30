# Metric Trees by Business Model

Load when defining or auditing a north-star metric (NSM), input metric tree, or activation event. Pick the closest match below; adapt leaves; do not adopt all branches verbatim.

## What a metric tree is for

A metric tree maps how granular input metrics combine into focus metrics, which combine into the NSM. The tree has three jobs:

1. **Force a single NSM.** Teams that pick more than one optimize for none.
2. **Make the causal chain visible.** Each child should be a lever that meaningfully moves its parent.
3. **Tell you where to look first when the NSM moves.** A drop in the NSM is diagnosed by walking the tree.

## How to use the trees below

1. Find the model closest to yours.
2. Replace the leaves with metrics you can actually instrument.
3. For each branch, name an owner and a dashboard.
4. Cross-check against `references/funnel_analytics.md` for event taxonomy.
5. Pick the activation event from the matching row in `references/asset_patterns.md` — most teams' biggest leverage is here.

## NSM selection rules

A good NSM is:

- **Tied to delivered value**, not work-in-progress (e.g., "completed jobs" not "listings posted").
- **Countable per period**, not a ratio. Ratios go in the children.
- **Predictive of revenue or retention** within 1–2 cycles.
- **Movable by the team** — vanity metrics like "total signups ever" are off-limits.
- **One number** per company. Sub-orgs may have sub-NSMs that ladder up.

Reforge's frame is useful: NSMs cluster into acquisition-focused (marketplaces, network goods), retention-focused (most SaaS), and monetization-focused (payments, ads). Pick the cluster that drives your business model.

---

## Self-serve SaaS (flat or tiered)

**NSM:** Weekly Active Accounts with ≥ N value events
*Why:* signup is vanity; usage that produces value predicts retention and revenue.

```
NSM: Weekly Active Accounts (≥ N value events)
├── Activation rate (signup → first value event ≤ 7d)
│   ├── Time-to-value (median minutes from signup to first value event)
│   ├── Setup friction (errors, abandons, support contacts before value)
│   └── Onboarding completion rate
├── Trial-to-paid conversion
│   ├── Pricing-page visit rate (from active accounts)
│   ├── Demo / upgrade CTA CTR
│   └── Time from signup to upgrade decision
├── Retention (logo and revenue, monthly)
│   ├── Repeat value-event frequency
│   ├── Reactivation rate (dormant → active)
│   └── Cohort retention curve (track shape, not just w8 number)
└── Expansion
    ├── Seat additions per account per month
    └── Tier upgrades
```

Activation event candidate: per-product "first real output" — first usable artifact exported, first dashboard with real data, first integration connected with downstream usage.

Benchmarks (directional, 2026):
- Median activation rate: ~37.5% across SaaS
- Median free-to-paid: ~8% (15-20% for 14-day trials with no card)
- Trials WITH a defined activation event convert 2-3× higher than without

---

## Usage-based / API / AI-inference / data-infra

**NSM:** Weekly accounts with paid usage > $X
*Why:* call volume is too cheap; *paid* call volume measures landed value.

```
NSM: Weekly Accounts with Paid Usage > $X
├── First successful production-like call ≤ 7d (activation)
│   ├── Time-to-first-call from signup
│   ├── First-call success rate (not 4xx/5xx)
│   └── Docs / quickstart abandonment points
├── Spend ramp
│   ├── % accounts with WoW spend growth ≥ 20%
│   ├── Median time from first paid call to $100 spend
│   └── Endpoint breadth (different endpoints called per account)
├── Reliability / trust signals (guardrails)
│   ├── Error rate by tenant
│   ├── Spend cap hits / "bill shock" incidents
│   └── Support contacts per $1k spend
└── Expansion
    ├── New environments connected (staging → prod)
    └── Net spend retention by cohort
```

Watchout: "first call" is too easy as activation if your product's `hello_world` is trivial. Use first **production-like** call (real workload, real volume) as the bar.

---

## Two-sided marketplace

**NSM:** Successful matches per week per active demand user
*Why:* "transactions" without per-user normalization hides whether matches are concentrated in a few power users (fragile) or distributed (durable).

```
NSM: Successful Matches/Week/Active Demand User
├── Supply liquidity
│   ├── Utilization (jobs per active supplier per period)
│   ├── Median time-to-first-job for new suppliers
│   └── Density (active suppliers per geo × vertical)
├── Demand fulfillment
│   ├── Match rate (request → completed match in target window)
│   ├── Time-to-first-match
│   └── Bid / quote conversion
├── Repeat behavior
│   ├── Demand: bookings per cohort week
│   └── Supply: jobs per supplier per month
└── Take-rate health
    ├── Revenue per match
    ├── Disintermediation rate (off-platform messaging signals)
    └── Refund / dispute rate (guardrail)
```

Liquidity targets (directional, services):
- Demand match rate > 40% healthy; < 20% warning
- Supply utilization > 30% healthy; < 10% warning

If utilization or match rate is below the warning threshold, **adding demand makes the marketplace worse**, not better. See `marketplace_network.md`.

---

## Open-source-led commercial (PLG with OSS top of funnel)

**NSM:** Paid accounts with ≥ N seats activated
*Why:* OSS stars and downloads are loud but uncorrelated with revenue. Activated paid seats are the convertible asset.

```
NSM: Paid Accounts with ≥ N Seats Activated
├── OSS adoption (light signal)
│   ├── Real installs (vs star/download spam)
│   ├── First-week active install rate
│   └── Community engagement (issues, PRs, forum posts)
├── OSS → commercial intent signals
│   ├── SSO / audit log / RBAC docs viewed
│   ├── "Enterprise" / "team" page views from active OSS users
│   └── Self-host setup events that signal scale
├── Commercial activation
│   ├── First deploy with paid features enabled
│   ├── Second user invited
│   └── First integration connected
└── Expansion
    ├── Seat growth per account / month
    └── Premium feature adoption
```

Anti-pattern: equating GitHub stars with demand. Stars cost nothing and rarely predict revenue. Track real installs and team-feature usage instead.

---

## Course / community / cohort-based product

**NSM:** Cohort completion + post-cohort outcome event
*Why:* dropout is the killer; tying NSM to outcome (job change, deploy, asset shipped) blocks the "everyone bought, nobody finished" failure mode.

```
NSM: Cohort Completers with Outcome Event
├── Activation (Module-1 completion or first peer interaction)
│   ├── First-session attendance / first-module finish
│   └── First post / question asked
├── Cohort retention
│   ├── Week-over-week attendance
│   ├── Assignment / project submission rate
│   └── Drop-out triggers (which week, which content)
├── Outcome event
│   ├── Project shipped / portfolio updated / job change
│   └── Self-reported result + receipt (LinkedIn, repo, photo)
└── Referral / repeat
    ├── Net invites per active member
    └── Repeat enrollment rate (next cohort, sister course)
```

Watchout: vanity metric is "% who watched all videos." Real metric is what they did *with* the videos.

---

## B2B sales-led (mid-market, enterprise)

**NSM:** ARR closed-won from ICP-qualified pipeline
*Why:* pipeline from non-ICP closes at 1/4 the rate and churns at 3× — counting only ICP-qualified ARR as the NSM forces sales discipline.

```
NSM: ICP-Qualified ARR Closed-Won (rolling 90-day)
├── Pipeline quality
│   ├── ICP fit % (firmographic + technographic match)
│   ├── MQL → SQO conversion rate
│   └── Disqualified-out rate by stage (rising = ICP drift)
├── Velocity
│   ├── Days per stage
│   ├── Stalled-deal rate (no advance ≥ 21 days)
│   └── Sales cycle length by ACV band
├── Win rate
│   ├── By ICP segment
│   ├── By competitor faced
│   └── By proof asset attached (case study, ROI calc, security pack)
└── Net revenue retention
    ├── Logo retention (annual)
    ├── Expansion ARR (cross-sell, seats, usage)
    └── Down-sell / churn ARR
```

Watchout: "MQLs" is not the NSM. MQL inflation (lower bar) inflates pipeline without lifting close rates and quietly raises CAC. Hold the bar at *qualified* opportunities.

---

## E-commerce / D2C

**NSM:** Net revenue per cohort over rolling 12 months
*Why:* second-order revenue (repeat purchase + referral) is where DTC economics work or don't. First-order revenue alone is unprofitable for most categories at honest CAC.

```
NSM: Cohort Net Revenue (12-mo)
├── First-order acquisition
│   ├── Visits → purchase rate (by source)
│   ├── AOV
│   └── First-order CAC (channel-attributed)
├── Repeat purchase
│   ├── 30 / 60 / 90-day repeat rate by cohort
│   ├── Time to second purchase
│   └── Subscription / replenishment opt-in rate
├── Referral / earned
│   ├── Referrals per net new customer
│   └── UGC / review submission rate
└── Margin / refund (guardrail)
    ├── Gross margin % by cohort
    ├── Return rate
    └── Customer support cost per order
```

Watchout: optimizing AOV via discounts can erode gross margin AND repeat rate. Cohort net revenue catches this; AOV-only does not.

---

## Cross-model rules

1. **Pick the cluster first** (acquisition / retention / monetization), then the NSM.
2. **Children must be levers**, not synonyms. If two children always move together, one is redundant.
3. **Guardrails belong in the tree**, not as an afterthought. Refunds, support tickets, regret signals.
4. **Refresh the tree quarterly.** As the business matures, what predicts revenue changes.
5. **A growing NSM with a stalled child is an early warning** that the tree is wrong and the NSM will follow.

## When the tree disagrees with reality

If your NSM is up but revenue is flat — or NSM is flat but revenue is up — the tree is mis-specified. Revisit step 2 of the cross-model rules. The fix is rarely "add another metric"; it's "replace a parent with one that actually predicts revenue."
