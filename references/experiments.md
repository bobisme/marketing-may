# Experiment Design

Load when designing tests, choosing experiment types, defining decision rules, or setting kill/pivot/narrow thresholds.

## Contents

- Experiment types
- Experiment plan table
- Good experiment rules
- Experiment priority score
- Kill/pivot/narrow rules

## Experiment types

| Test | Use when | Example | Main risk |
|---|---|---|---|
| Problem interview | Pain uncertain | 20 interviews about current workflow | Polite false positives |
| Switch interview | Existing users/customers | Why they switched from X | Recall bias |
| Smoke test | Demand uncertain | Landing page with CTA | Measures offer/page/channel together |
| Fake-door test | Feature/package uncertain | Button for unavailable feature | Trust damage if deceptive; disclose after click |
| Pricing page test | WTP/package uncertain | Show packages and collect demo/trial intent | Needs qualified traffic |
| Ad test | Message/channel uncertain | 3 pain angles to landing pages | Clicks can be shallow |
| Concierge test | Delivery uncertain | Manually deliver outcome | Service may not scale |
| Wizard-of-Oz | Automation uncertain | Manual backend behind product UX | Ethics and expectation management |
| Outbound campaign | Segment/trigger uncertain | 100 trigger-based emails | List quality confounds |
| Paid pilot | Economic value uncertain | Fixed-scope pilot | Delivery burden |

## Experiment plan table

Always use this table for experiments:

| Assumption | Hypothesis | Audience | Channel | Test | Metric | Threshold | Cost | Risk | Expected learning | Decision rule |
|---|---|---|---|---|---|---|---:|---|---|---|
| | | | | | | | | | | |

## Good experiment rules

- Test one primary uncertainty when possible.
- Define the unit: visitor, account, user, company, lead, or opportunity.
- Define the event before running the test.
- Include a guardrail metric.
- Use thresholds that map to a decision.
- Check sample ratio mismatch or equivalent assignment/logging issues for A/B tests.
- Do not peek, stop, or reinterpret without documenting the change.
- If sample size is too small, use the test for directional learning, not statistical proof.

## Experiment priority score

```text
Expected Learning Value =
P(decision changes) × Decision impact × Reversibility × Evidence quality
− Cost − Time − Risk − Trust damage
```

Prefer experiments that can invalidate a risky assumption quickly.

## Kill/pivot/narrow rules

Set rules before testing. Examples:

| Evidence | Default decision |
|---|---|
| 15–20 interviews, no repeated painful pattern | Narrow segment or change problem |
| Buyers describe pain but no workaround/current spend | Reframe as low-urgency or find stronger trigger |
| Strong pain but no reachable channel | Find partner/channel or pick another segment |
| High traffic but low qualified conversion | Fix segment/channel/copy before product changes |
| High activation but low retention | Product/value problem, not acquisition problem |
| High demo interest but no close | Pricing, proof, stakeholder, or sales process problem |
| Paid pilots succeed but no repeatability | Productized service, narrow ICP, or improve onboarding |
| CAC payback impossible at current price | Raise price, change ICP, reduce sales cost, or kill channel |
| Requires deception to convert | Stop; redesign offer and proof |
