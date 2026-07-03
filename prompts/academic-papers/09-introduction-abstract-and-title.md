# Prompt 09 — Introduction Funnel, Abstract & Title

> **Purpose:** Write the two things editors read first and most carefully — the introduction and the abstract — plus a title that earns a click.
> **Use when:** After results and robustness are stable; the introduction should be written (or rewritten) last.
> **Target standard:** 4* — the introduction follows the canonical funnel and delivers the result by paragraph three; the abstract is self-contained.

---

## Prompt

```
ROLE: Act as a co-author known for crisp introductions at 4* journals, and as the editor
who decides in 90 seconds whether to desk-reject. Write for a smart non-specialist.

CONTEXT
- Research question: {{one sentence, Prompt 01}}
- Contribution: {{Prompt 01}}
- Headline result in economic units: {{Prompt 07}}
- Identification in one clause: {{Prompt 04}}
- Closest papers we differentiate from: {{Prompt 02}}

TASK

1. TITLE
   - Propose 5 titles: 2 descriptive, 2 with a "hook", 1 question form.
   - Each ≤ 12 words, searchable, honest about what the paper shows. Recommend one.

2. ABSTRACT (self-contained, ~120–150 words)
   - Sentence structure: (i) the question/importance, (ii) the setting & data,
     (iii) the identification, (iv) the main result WITH magnitude, (v) mechanism/
     heterogeneity, (vi) the contribution/implication.
   - No undefined jargon, no citations, no "we investigate" filler.

3. INTRODUCTION (the funnel — draft ~5–7 paragraphs)
   - ¶1 THE HOOK: the big question and why it matters (a motivating fact/puzzle/stake).
   - ¶2 THE GAP: what we don't know and why prior work couldn't answer it (Prompt 02).
   - ¶3 THIS PAPER: what we do, the setting, and — crucially — the MAIN RESULT stated
     with magnitude. Do not make the reader wait.
   - ¶4 IDENTIFICATION: the source of variation and why it is credible, in plain words.
   - ¶5 MECHANISM & ROBUSTNESS: what's driving it and why we believe it.
   - ¶6 CONTRIBUTION: 2–3 sentences, each starting "We contribute to [strand] by ...".
   - ¶7 ROADMAP (optional, one line).

4. THE FIRST-SENTENCE TEST
   - Draft 3 opening sentences. Kill any that a referee has read a hundred times
     ("The relationship between X and Y has long interested economists").

5. CONSISTENCY PASS
   - Verify the number in the abstract, the intro, and the results section MATCH.
   - Flag any claim in the intro not backed by a result in the paper.

CONSTRAINTS
- The main result appears by the third paragraph, with its magnitude.
- The abstract must stand alone if read in a search-engine snippet.
- No over-claiming: the introduction may not promise more than the paper delivers.
```

---

## Quality bar

- [ ] The main result, with magnitude, appears by paragraph three of the intro.
- [ ] The abstract is self-contained and states the effect size.
- [ ] The opening sentence is not a cliché.
- [ ] Numbers match across abstract, intro, and results.
