# Prompt 08 — Robustness Protocol & Threats to Validity

> **Purpose:** Design a robustness section that pre-empts referee objections — chosen ex ante, targeted at real threats, not a wall of near-identical regressions.
> **Use when:** After the main result stands; before submission; and in any revise-and-resubmit.
> **Target standard:** 4* — each check maps to a *named* threat and could plausibly *change the conclusion*.

---

## Prompt

```
ROLE: Act as the robustness designer and the harshest referee simultaneously. A good
robustness check is one that COULD overturn the result — not one guaranteed to confirm it.

CONTEXT
- Main result & preferred spec: {{estimate, from Prompts 06–07}}
- Identifying assumptions: {{from Prompt 04}}
- Design: {{DID / IV / RDD / panel / ...}}
- Known vulnerabilities: {{the killer objection from Prompt 04}}

TASK

1. THREAT-TO-CHECK MAP
   For each threat to validity, prescribe the specific check that addresses it:
   - Identification threats → the falsification/placebo that targets each assumption.
   - Specification sensitivity → alternative FE, controls, functional form, sample.
   - Inference concerns → alternative clustering, wild bootstrap, randomization inference.
   - Measurement → alternative variable definitions / proxies.
   - Outliers/influence → trimming, winsorizing, leave-one-out (unit/period/cluster).
   Present as a table: {Threat | Check | What result would DISCONFIRM the paper}.

2. DESIGN-SPECIFIC BATTERY (pick what applies)
   - DID: pre-trends/event study, alternative control groups, Callaway-Sant'Anna vs
     TWFE, Goodman-Bacon decomposition, Rambachan-Roth sensitivity.
   - IV: weak-IV-robust CIs (Anderson-Rubin), Conley et al. plausible-exogeneity,
     subset-of-instruments, overid test with caveats.
   - RDD: bandwidth sensitivity, polynomial order, density (McCrary), covariate
     continuity, donut hole, placebo cutoffs.
   - Panel: dynamic-panel bias, alternative FE structures, serial-correlation-robust SEs.

3. SENSITIVITY, NOT JUST BINARY
   - Where possible, quantify HOW MUCH an assumption must fail to overturn the result
     (Oster δ for selection on unobservables; breakdown point; e-values).

4. RANKING
   - Rank all proposed checks by (a) how likely the referee is to demand it and
     (b) how likely it is to actually change the answer. Do the high-high ones first.

5. HONEST FRAGILITY REPORT
   - State plainly which checks the result passes cleanly, which are borderline, and
     which you have not yet been able to run. No selective reporting.

CONSTRAINTS
- A robustness table of 12 confirmations that all address the same trivial threat is
  worth less than 3 checks that each attack a different real vulnerability.
- Report checks that weaken the result, with interpretation, not only the clean ones.
```

---

## Quality bar

- [ ] Every check maps to a named threat and states what would disconfirm the paper.
- [ ] At least one sensitivity check quantifies the breakdown point (e.g., Oster δ).
- [ ] Checks are ranked by referee-demand × answer-changing potential.
- [ ] Borderline or unrun checks are disclosed, not hidden.
