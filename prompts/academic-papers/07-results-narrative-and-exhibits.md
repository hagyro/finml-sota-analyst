# Prompt 07 — Results Narrative, Tables & Figures

> **Purpose:** Turn estimates into a disciplined results section — publication-grade exhibits plus prose that reports magnitudes and economic meaning, never just significance stars.
> **Use when:** Writing the results section and designing Table 2+ / main figures.
> **Target standard:** 4* — every number is interpreted in economic units; the main result is legible from one figure.

---

## Prompt

```
ROLE: Act as a co-author writing the results section of a 4* paper and as a table/figure
designer. Report effect SIZES and economic meaning first, statistical significance second.

CONTEXT
- Preferred specification & estimate(s): {{coefficient, SE, N, from Prompt 06}}
- Outcome units and baseline mean: {{so effects can be scaled}}
- Hypotheses being tested: {{H1..Hk from Prompt 03}}
- Additional results: {{mechanism, heterogeneity, dose-response}}

TASK

1. MAIN RESULT PARAGRAPH
   - Lead with the point estimate in ECONOMIC terms: "% of a SD", "% of the mean",
     "$ per unit", elasticity. Then the CI, then significance.
   - Explicitly link the coefficient back to H1 (confirm / reject / nuance).
   - State whether the magnitude is economically large, plausible, and consistent
     with the framework — and benchmark it against a comparable estimate in the field.

2. MAIN TABLE DESIGN
   - Draft the specification-ladder table (Prompt 06's columns) with proper notes:
     dependent variable, FE rows, controls indicator, clustering, N, R²/within-R²,
     mean of Y. Stars defined; SEs in parentheses; units stated.
   - Keep it self-contained: a reader should understand it from the title + notes.

3. HEADLINE FIGURE
   - Specify the ONE figure that makes the result visible without a regression
     (event-study plot with CIs / RD plot / binscatter / dose-response). Give axes,
     units, CI level, and what the reader should conclude at a glance.

4. MECHANISM & HETEROGENEITY RESULTS
   - Report the tests that distinguish the proposed channel from rivals (Prompt 03).
   - Present heterogeneity as tests of signed predictions, not a fishing expedition.

5. MAGNITUDE DISCIPLINE
   - Convert every headline coefficient into an interpretable quantity.
   - Flag any result that is statistically significant but economically trivial,
     and any that is large but imprecise.

6. HONEST REPORTING
   - Report results that cut against the hypothesis, not only confirmatory ones.
   - Note where precision is the binding constraint vs where the effect is truly null.

CONSTRAINTS
- No "significant at 5%" without the magnitude beside it.
- Tables and figures must be self-explanatory. No orphan coefficients in prose.
- Do not describe a p=0.11 result as "marginally significant" — report the CI.
```

---

## Quality bar

- [ ] The headline number appears in economic units before any significance claim.
- [ ] The main table is self-contained (a reader needs only title + notes).
- [ ] One figure conveys the result without a regression.
- [ ] Results against the hypothesis are reported, not buried.
