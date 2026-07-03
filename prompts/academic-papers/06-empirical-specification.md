# Prompt 06 — Empirical Specification & Inference

> **Purpose:** Pin down the estimating equations, functional form, fixed effects, and — critically — the inference procedure, with every choice justified.
> **Use when:** Moving from identification to estimation; writing the "Empirical Strategy" and "Econometric Specification" subsections.
> **Target standard:** 4* — the specification maps 1:1 to the estimand, and standard errors match the sampling process.

---

## Prompt

```
ROLE: Act as an econometrician who has refereed for the top field journals. Match the
estimator to the estimand, and match the standard errors to how the data were sampled.

CONTEXT
- Estimand: {{from Prompt 04}}
- Design: {{DID / IV / RDD / panel FE / ...}}
- Data: {{unit, panel dims, N, T, number of clusters}}
- Outcome, treatment, controls: {{Y, X, W}}
- Sources of dependence: {{serial correlation / spatial / clustered assignment}}

TASK — follow Estimation → Inference → Diagnostics.

1. BASELINE ESTIMATING EQUATION
   - Write it formally, defining every term, subscript, and fixed effect.
   - State what identifies the coefficient of interest given the FE structure.
   - Justify functional form (linear / log / Poisson-PPML / probit) for the outcome.

2. SPECIFICATION LADDER
   - Column 1 (raw) → ... → Column k (fully saturated). For each added block of
     controls/FE, state what confound it absorbs and what it must NOT absorb (bad
     controls / over-controlling for mechanism).

3. INFERENCE (the part referees fail papers on)
   - Correct level of clustering, justified by the level of treatment assignment.
   - Small-cluster problem? If # clusters is few, prescribe wild cluster bootstrap
     or randomization inference and say which.
   - Multiple hypothesis testing: if many outcomes/subgroups, prescribe correction
     (Romano-Wolf / sharpened q-values) and pre-specify the primary outcome.

4. FIXED EFFECTS & INCIDENTAL PARAMETERS
   - Check for Nickell bias (dynamic panels), separation (nonlinear FE), and
     collinearity of FE with the treatment. Prescribe fixes.

5. DIAGNOSTICS TO REPORT
   - The 3–4 diagnostics that must accompany the main table (e.g., first-stage F,
     pre-trend test, overlap, residual checks).

6. SPECIFICATION PRE-COMMITMENT
   - Declare the ONE preferred specification ex ante and why, so the result is not
     a max over specifications. List which choices go to robustness (Prompt 08).

CONSTRAINTS
- Never cluster at a level finer than treatment assignment.
- Do not add controls that are outcomes of the treatment (post-treatment bias).
- If N-clusters is small, do NOT default to conventional cluster-robust SEs.
```

---

## Quality bar

- [ ] Every term in the estimating equation is defined; the FE structure is explicit.
- [ ] Clustering level matches the level of treatment assignment, with justification.
- [ ] Small-cluster and multiple-testing issues are addressed, not ignored.
- [ ] One preferred specification is pre-committed; the rest are robustness.
