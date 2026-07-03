# Prompt 01 — Research Question & Contribution Framing

> **Purpose:** Turn a rough idea into a precisely-posed research question with a defensible, top-journal-worthy contribution ("the so-what test").
> **Use when:** At the very start of a project, or when a referee/editor writes "the contribution is unclear."
> **Target standard:** ABS/AJG 4* — the question must be *important*, *answerable*, and *novel*.

---

## How to use

Fill every `{{placeholder}}`. Delete guidance in brackets. Paste the completed block to Econometron.

---

## Prompt

```
ROLE: Act as a co-author and desk editor at a 4* (ABS/AJG) economics/finance/management
journal. Be a demanding but constructive critic. Do not flatter.

CONTEXT
- Working idea: {{one-paragraph description of the idea}}
- Field & sub-field: {{e.g., labor economics / firm-level productivity}}
- Setting & data available: {{country, period, unit of observation, key variables}}
- What motivated this: {{policy change / puzzle / theory tension / new data}}
- Closest 3–5 papers I know of: {{citations or short descriptions}}

TASK
Help me sharpen this into a publishable research question. Deliver:

1. RESEARCH QUESTION
   - State it in ONE sentence, in causal/estimand terms where relevant.
   - Give 2 alternative framings (narrower / broader) and recommend one.

2. THE ESTIMAND (if empirical)
   - Define the target parameter formally (e.g., ATT, LATE, elasticity).
   - State the population and margin it applies to.

3. CONTRIBUTION LEDGER — for each, be concrete and skeptical:
   - Empirical contribution: what new fact do we establish?
   - Methodological contribution: what do we do differently and why does it matter?
   - Theoretical/conceptual contribution: which mechanism or prediction do we test?
   - Policy/managerial relevance: who should change what decision?

4. THE "SO-WHAT" STRESS TEST
   - Steelman the strongest reason a referee rejects this as incremental.
   - Give my best rebuttal, or tell me honestly if the idea needs re-scoping.

5. POSITIONING SENTENCE
   - Draft the single "we are the first to ..." / "we show that ..." sentence that
     will anchor the introduction. Provide 3 variants at different ambition levels.

6. FEASIBILITY & RISK
   - What is the single biggest identification/data risk that could kill the paper?
   - What is the minimum viable version that still publishes?

CONSTRAINTS
- No fabricated citations. If you are unsure a paper exists, say so.
- Prefer precision over enthusiasm. Flag any claim that outruns the evidence.
```

---

## Quality bar (what "good" looks like)

- [ ] The question fits in one sentence and names the estimand.
- [ ] At least one contribution is *not* "we apply method X to setting Y."
- [ ] The strongest rejection reason is stated honestly, not strawmanned.
- [ ] A minimum-viable version exists that survives the biggest risk.
