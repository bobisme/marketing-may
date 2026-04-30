# 06 — Funnel Metrics and Instrumentation Template

## Funnel definition

| Stage | Definition | Event(s) | Owner | Current baseline | Target |
|---|---|---|---|---:|---:|
| Visitor | | | | | |
| Qualified visitor | | | | | |
| Lead/signup | | | | | |
| Activation | | | | | |
| Qualified intent/PQL | | | | | |
| Conversion | | | | | |
| Retention | | | | | |
| Expansion | | | | | |
| Advocacy | | | | | |

## Event taxonomy

Naming convention: `object_action` or `verb_object`: __________________

| Event name | Stage | Definition | Trigger/firing condition | Required properties | User/account ID | Tool | QA status | Owner |
|---|---|---|---|---|---|---|---|---|
| page_view | Acquisition | | | source, campaign, path | user_id | | | |
| signup_started | Lead | | | CTA, page, plan | user_id | | | |
| activation_completed | Activation | | | use_case, segment | user_id/account_id | | | |
| qualified_intent_detected | PQL | | | criteria, score | account_id | | | |
| checkout_completed | Conversion | | | price, plan, coupon | user_id/account_id | | | |

## Activation event

| Candidate event | Why it indicates value | Time window | Predicts retention/conversion? | Instrumentation confidence | Selected? |
|---|---|---|---|---|---|
| | | | | | |

## PQL / qualification scoring

| Criterion | Points | Evidence/event | Notes |
|---|---:|---|---|
| ICP role/company | | | |
| Trigger/use case | | | |
| Activation completed | | | |
| Team invited/integration connected | | | |
| Usage threshold reached | | | |
| Pricing page viewed/demo requested | | | |
| Security/procurement page viewed | | | |

PQL threshold: ______ points.

## Attribution assumptions

| Assumption | Choice | Caveat |
|---|---|---|
| Lookback window | | |
| Attribution model | First / last / data-driven / blended | |
| Self-reported attribution | Yes / No | |
| Offline touches | Captured / missing | |
| Dark social/direct | How treated | |
| Revenue vs lead attribution | | |

## Dashboard minimum

- Qualified visitors by source.
- Signup/demo conversion by segment and source.
- Activation rate and time to value.
- Qualified intent/PQL rate.
- Demo-to-close or trial-to-paid.
- CAC/payback where possible.
- Retention by cohort.
- Top drop-off step.
- Guardrails: unsubscribe, spam complaints, refund/cancel, support tickets, billing complaints.
