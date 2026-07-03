# Prompt 04 — Identification Strategy Design

> **Purpose:** Design and stress-test the causal identification strategy — the single most scrutinized part of any 4* empirical paper.
> **Use when:** Before estimation, and whenever a referee questions endogeneity, selection, or "what is the source of variation?"
> **Target standard:** 4* — the identifying variation is *named*, the exogeneity argument is *explicit*, and every threat has a *test*.

---

## Prompt

```
ROLE: Act as the toughest empirical microeconomist on the referee panel. Assume
endogeneity until proven otherwise. Never assume away selection or reverse causality.

CONTEXT
- Estimand (target parameter): {{ATT / LATE / elasticity / ...}}
- Treatment / regressor of interest X: {{definition + how it varies}}
- Outcome Y: {{definition}}
- Proposed source of identifying variation: {{policy change / discontinuity /
  instrument / panel timing / shift-share / ...}}
- Data structure: {{cross-section / panel dims / repeated cross-sections}}
- Known confounders: {{list}}

TASK — follow the Goal → Estimand → Identification chain.

1. SOURCE OF VARIATION
   - In one sentence: "The causal effect is identified from variation in X driven by ___."
   - Classify the design: {DID / event study / IV / RDD / synthetic control /
     matching-on-observables / structural}. Justify the choice over the alternatives.

2. IDENTIFYING ASSUMPTIONS (formal)
   - State each assumption formally (e.g., parallel trends, exclusion, continuity,
     conditional independence, overlap).
   - For EACH: give the economic argument for why it holds HERE, and the observable
     implication that would let a skeptic check it.

3. THREATS TABLE
   Build a table: rows = {selection, reverse causality, omitted variables,
   anticipation, spillovers/SUTVA, measurement error, differential trends}.
   Columns = {Is it plausible here? | Direction of bias | Test/diagnostic | Fix}.

4. THE KILLER OBJECTION
   - State the single most damaging identification critique a referee will raise.
   - Give the best available response, or concede and propose a design change.

5. FALSIFICATION SUITE
   - Placebo tests (pre-period, unaffected outcomes, unaffected units).
   - Balance/continuity checks appropriate to the design.
   - A test whose failure would genuinely undermine the claim (not a soft check).

6. LATE/ATT INTERPRETATION
   - Whose effect is this? Name the compliers / treated subpopulation.
   - State the external-validity boundary explicitly.

CONSTRAINTS
- Be adversarial first, reassuring second. Rank threats by how likely they are to
  sink the paper, not by how easy they are to dismiss.
```

---

## Quality bar

- [ ] The identifying variation is nameable in one sentence.
- [ ] Every assumption has both an economic argument and an observable check.
- [ ] The single most damaging objection is stated and answered honestly.
- [ ] At least one falsification test could actually fail (not a soft check).
