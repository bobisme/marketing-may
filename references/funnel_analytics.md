# Funnel Analytics & Instrumentation

Load when defining a funnel, choosing an activation event, designing event taxonomy, stating attribution assumptions, or building a metric tree.

## Contents

- Funnel model
- Activation event selection
- Event taxonomy rules
- Attribution assumptions
- Metric tree

## Funnel model

Use the simplest funnel that matches the business model.

| Stage | Question | Example events |
|---|---|---|
| Acquisition | How did they arrive? | `page_view`, `ad_click`, `source_captured` |
| Problem fit | Did they engage with relevant pain? | `use_case_viewed`, `roi_calculator_used` |
| Lead intent | Did they request value? | `signup_started`, `demo_requested`, `lead_magnet_downloaded` |
| Activation | Did they reach first value? | Product-specific "aha" event |
| Qualified intent | Are they likely to buy? | `integration_connected`, `team_invited`, `usage_threshold_reached` |
| Conversion | Did they pay/commit? | `checkout_completed`, `contract_signed`, `pilot_paid` |
| Retention | Do they keep receiving value? | Repeat activation, usage frequency, renewal |
| Expansion | Do they grow? | `seat_added`, `usage_expanded`, `upgrade_completed` |
| Advocacy | Do they create pull? | `referral_sent`, `review_submitted`, `case_study_agreed` |

## Activation event selection

An activation event must be:

- Meaningful: reflects first real value, not setup trivia.
- Predictive: correlates with retention, conversion, or expansion.
- Timely: happens early enough to optimize onboarding.
- Buyer-specific: can differ by segment.
- Instrumentable: reliably captured with properties.

Examples:

| Product type | Weak activation | Better activation |
|---|---|---|
| AI writing tool | Account created | First usable draft exported/shared |
| Analytics SaaS | Script installed | First dashboard with real event data viewed |
| Dev API | API key created | First successful production-like API call |
| Marketplace | Signup | First completed transaction or qualified match |
| Course/community | Joined | Completed first module and posted intro/question |
| Agency/consulting | Call booked | Paid diagnostic completed with accepted plan |

## Event taxonomy rules

- Use consistent names: `object_action` or `verb_object`; do not mix styles.
- Use account/company ID for B2B, not only user ID.
- Add properties: segment, plan, source, campaign, role, company_size, use_case, price_shown, CTA, experiment_variant.
- Separate marketing, product, billing, and sales events but join them by user/account.
- Keep a tracking plan with owner, definition, firing condition, and QA status.
- Audit events monthly; remove duplicates and ambiguous events.

## Attribution assumptions

Attribution is a decision aid, not reality. Always state:

- Lookback window.
- First-touch, last-touch, data-driven, or blended model.
- Offline touches not captured.
- Self-reported attribution question.
- Dark social/direct traffic caveats.
- Whether channel credit is assigned to lead creation, qualified lead, activation, opportunity, or revenue.

## Metric tree

```text
Revenue / Mission Metric
├── Acquisition quality
│   ├── ICP-qualified visitors/leads
│   └── Cost per qualified intent
├── Activation
│   ├── Activation rate
│   └── Time to value
├── Conversion
│   ├── Trial-to-paid / demo-to-close
│   └── Sales cycle length
├── Retention
│   ├── Repeat value event rate
│   └── Churn / renewal
└── Expansion
    ├── Seat/usage growth
    └── Referral/review rate
```
