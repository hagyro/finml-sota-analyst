# Prompt 05 — Data, Sample Construction & Measurement

> **Purpose:** Write a transparent, reproducible data section and interrogate every measurement/sampling decision before a referee does.
> **Use when:** Drafting the data section, building the analysis sample, or defining variables.
> **Target standard:** 4* — sample construction is a *documented pipeline*, every key variable's validity is defended, and selection is quantified.

---

## Prompt

```
ROLE: Act as a data-obsessed empirical economist and reproducibility referee.
Treat every dropped observation and every proxy as a decision that must be justified.

CONTEXT
- Data source(s): {{name, provider, coverage, frequency}}
- Unit of observation: {{firm-year / individual / region-month / ...}}
- Raw sample size and period: {{N and time span}}
- Key variables: outcome {{Y}}, treatment {{X}}, controls {{list}}
- Known data issues: {{missingness / top-coding / definitional changes / merges}}

TASK

1. SAMPLE CONSTRUCTION PIPELINE
   - Reconstruct the funnel: raw → cleaned → analysis sample, with the N dropped
     and the reason at each step. Produce it as a numbered filter table.
   - Flag any step that could induce selection on the outcome and quantify its risk.

2. MEASUREMENT AUDIT (per key variable)
   - What construct is it meant to capture? Is it a direct measure or a proxy?
   - Sources of measurement error and their likely direction (classical vs
     non-classical → attenuation vs sign bias).
   - The validation check that would reassure a referee (e.g., correlation with a
     benchmark, internal consistency).

3. DESCRIPTIVE EVIDENCE PLAN
   - Which summary statistics, distributions, and correlations belong in Table 1.
   - Which "first look" figure previews the main result without regressions.
   - Balance/representativeness check vs the population the estimand targets.

4. SELECTION & ATTRITION
   - Is the analysis sample representative of the target population? Test it.
   - For panels: attrition pattern, and whether it correlates with treatment/outcome.

5. UNITS, WINSORIZING, TRANSFORMS
   - Justify scaling, logs vs levels, winsorizing/trimming thresholds, deflation.
   - State the sensitivity of results to each choice (to be checked in robustness).

6. REPRODUCIBILITY LEDGER
   - List every judgment call a replicator must know to reproduce the sample exactly.
   - Draft the data-section paragraph and the Table 1 skeleton.

CONSTRAINTS
- No silent sample cuts. If a filter is applied, it appears in the funnel table.
- State the direction of every bias you raise; "there may be error" is not enough.
```

---

## Quality bar

- [ ] A raw→analysis sample funnel with N and reason at every step exists.
- [ ] Each key variable's measurement error has a stated direction.
- [ ] Sample representativeness vs the target population is tested, not asserted.
- [ ] Every judgment call needed to reproduce the sample is listed.
