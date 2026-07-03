# Academic Paper Prompt Library

A set of **10 reusable, ready-to-use prompts** for writing publication-grade
empirical economics / finance / management papers with Econometron.

These prompts are built to the standard of **4\* journals (ABS/AJG)**: rigorous
identification, honest inference, disciplined magnitudes, and referee-proof
robustness. Each one is designed to be dropped into Econometron (or any capable
Claude session), filled with `{{placeholders}}`, and reused across projects.

Every prompt inherits Econometron's operating framework:

> **Goal → Estimand → Identification → Estimation → Inference → Diagnostics → Robustness → Interpretation**

---

## The library

Follow the numbers — they trace the natural life-cycle of a paper.

| # | Prompt | Use it when you are... |
|---|--------|------------------------|
| 01 | [Research Question & Contribution](01-research-question-and-contribution.md) | Sharpening the idea and passing the "so-what" test |
| 02 | [Literature Synthesis & Gap](02-literature-synthesis-and-gap.md) | Mapping the frontier and locating the real gap |
| 03 | [Conceptual Framework & Hypotheses](03-conceptual-framework-and-hypotheses.md) | Deriving the mechanism and signed, testable predictions |
| 04 | [Identification Strategy](04-identification-strategy.md) | Designing and stress-testing causal identification |
| 05 | [Data & Measurement](05-data-and-measurement.md) | Building a reproducible sample and defending measures |
| 06 | [Empirical Specification & Inference](06-empirical-specification.md) | Choosing estimating equations and standard errors |
| 07 | [Results Narrative & Exhibits](07-results-narrative-and-exhibits.md) | Writing results with magnitudes and clean tables/figures |
| 08 | [Robustness & Threats to Validity](08-robustness-and-threats-to-validity.md) | Pre-empting referees with targeted checks |
| 09 | [Introduction, Abstract & Title](09-introduction-abstract-and-title.md) | Writing what the editor reads first |
| 10 | [Referee Response & Revision](10-referee-response-and-revision.md) | Turning an R&R into an acceptance |

---

## How to use a prompt

1. Open the file for the stage you're at.
2. Copy the block inside the fenced ` ``` ` code block.
3. Replace every `{{placeholder}}` with your specifics; delete bracketed guidance.
4. Paste it to Econometron. Read the **Quality bar** checklist at the bottom — it
   tells you what a strong answer must contain before you move on.

Prompts are composable: the output of one feeds the `{{placeholders}}` of the next
(e.g. the estimand from **04** flows into **06**; the headline result from **07**
flows into **09**).

---

## Design principles baked into every prompt

- **Adversarial before reassuring.** Identification and robustness prompts assume
  endogeneity and look for the killer objection first.
- **Magnitudes over stars.** Results are always reported in economic units.
- **Inference matches sampling.** Clustering and bootstrap are matched to how
  treatment was assigned, not to habit.
- **No fabricated citations, ever.** Unverifiable references are flagged `[VERIFY]`.
- **Honest reporting.** Borderline checks, unrun tests, and results that cut against
  the hypothesis are disclosed, never buried.

---

*Part of the [Econometron](../../README.md) project. Prompts only — no analysis is
run by opening this library.*
