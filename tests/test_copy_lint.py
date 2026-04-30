"""
Tests for scripts/copy_lint.py.

Asserts each rule fires on canonical bad input and stays silent on good input.
"""
from __future__ import annotations

from scripts.copy_lint import lint_text


def rules_fired(text: str) -> set[str]:
    return {f.rule for f in lint_text(text)}


class TestVagueAdjective:
    def test_classic_offenders_fire(self):
        for word in ["amazing", "powerful", "seamless", "world-class", "synergy", "innovative"]:
            assert "vague-adjective" in rules_fired(f"Our {word} platform helps you. Start now."), word

    def test_clean_text_no_fire(self):
        text = "Find broken Stripe webhooks within 30 seconds. Start a 14-day trial."
        assert "vague-adjective" not in rules_fired(text)


class TestUnsupportedClaim:
    def test_unsupported_superlative_fires(self):
        text = "We are the leading Stripe monitoring tool. Start a trial."
        assert "unsupported-claim" in rules_fired(text)

    def test_supported_with_number_does_not_fire(self):
        # Number nearby satisfies the proof window.
        text = "We are the #1 Stripe monitoring tool with 412 paying teams. Start a trial."
        assert "unsupported-claim" not in rules_fired(text)

    def test_supported_with_named_customer_does_not_fire(self):
        text = "Trusted by Acme Corp and Beta Industries — see the case study. Start a trial."
        # Named customer + "case study" should satisfy proof.
        assert "unsupported-claim" not in rules_fired(text)


class TestDarkPattern:
    def test_undated_urgency_fires(self):
        text = "Hurry, only 5 left! Limited time offer. Sign up now."
        rules = rules_fired(text)
        assert "dark-pattern" in rules

    def test_dated_urgency_allowed(self):
        text = "Sale ends March 15, 2026. Sign up now."
        # Should NOT flag dark-pattern because a real date is nearby.
        assert "dark-pattern" not in rules_fired(text)


class TestHiddenPrice:
    def test_starting_at_no_number_fires(self):
        text = "Starting at — talk to sales. Book a demo."
        assert "hidden-price" in rules_fired(text)

    def test_starting_at_with_number_clean(self):
        text = "Starting at $29/month for 100k events. Start a trial."
        assert "hidden-price" not in rules_fired(text)


class TestWeakSocialProof:
    def test_trusted_by_thousands_fires(self):
        text = "Trusted by thousands of companies. Start a trial."
        assert "weak-social-proof" in rules_fired(text)

    def test_specific_count_clean(self):
        text = "Trusted by over 412 SaaS teams. Start a trial."
        assert "weak-social-proof" not in rules_fired(text)


class TestMissingCTA:
    def test_no_cta_fires(self):
        text = "Our platform watches your webhooks. It alerts you when they fail."
        assert "missing-cta" in rules_fired(text)

    def test_cta_present_clean(self):
        text = "Our platform watches your webhooks. Start a free trial."
        assert "missing-cta" not in rules_fired(text)


class TestBuzzwordDensity:
    def test_high_density_fires(self):
        text = ("Our amazing, powerful, seamless, world-class, "
                "innovative, intuitive platform supercharges your workflow.")
        # 7+ vague words in ~15 words → very high density
        assert "buzzword-density" in rules_fired(text)

    def test_low_density_no_fire(self):
        # One vague adjective in a long body should not trigger buzzword-density
        # (vague-adjective will still fire for the single word).
        text = ("Find broken Stripe webhooks within 30 seconds of failure. "
                "Used by 412 teams including Acme Corp. Start a 14-day trial. "
                "We have one powerful feature: real-time replay.")
        assert "buzzword-density" not in rules_fired(text)


class TestLintIgnore:
    def test_inline_ignore_suppresses(self):
        # Without ignore: flag fires
        plain = "Our amazing platform. Start now."
        assert "vague-adjective" in rules_fired(plain)

        # With inline lint:ignore: suppressed
        text = "Our amazing platform. <!-- lint:ignore vague-adjective --> Start now."
        rules = rules_fired(text)
        assert "vague-adjective" not in rules

    def test_ignore_other_rules_unaffected(self):
        text = "Our amazing platform is the best. <!-- lint:ignore vague-adjective --> Start now."
        rules = rules_fired(text)
        # vague-adjective suppressed; unsupported-claim still fires
        assert "vague-adjective" not in rules
        assert "unsupported-claim" in rules
