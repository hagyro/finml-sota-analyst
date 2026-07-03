# Prompt 02 — Literature Synthesis & Gap Positioning

> **Purpose:** Produce a structured, honest map of the literature that positions the paper without over-claiming, and locates the precise gap it fills.
> **Use when:** Writing the related-literature section, or answering "how does this differ from [X]?"
> **Target standard:** 4* — engages the *frontier*, not a textbook; positions by contribution, not by chronology.

---

## How to use

Fill placeholders. Provide real references you have read; Econometron will organize and
pressure-test — it will **not** invent citations.

---

## Prompt

```
ROLE: Act as a field expert writing the "Related Literature" section of a 4* paper.
Organize by intellectual contribution, never as an annotated bibliography.

CONTEXT
- Paper's research question: {{one sentence}}
- Paper's claimed contribution: {{from Prompt 01}}
- Papers I have actually read (with 1-line takeaway each):
  {{list — author, year, finding, method}}
- Strands I suspect are relevant but haven't mapped: {{keywords / open questions}}

TASK

1. STRAND MAP
   Group the literature into 3–5 coherent strands. For each strand:
   - What question does the strand answer?
   - What is the current consensus / open tension?
   - Which 2–3 papers are the load-bearing citations?

2. FRONTIER LINE
   For each strand, state the single most recent/authoritative result this paper
   must beat, extend, or reconcile with.

3. GAP STATEMENT
   Write a precise gap: "Prior work establishes A and B, but not C because [data/
   identification/theory limitation]. This paper provides C by [approach]."
   - Distinguish a TRUE gap (unanswered) from a FALSE gap (answered elsewhere,
     I just haven't found it). Flag where I likely have a blind spot.

4. DIFFERENTIATION TABLE
   Build a compact table: rows = 4–6 closest papers; columns = {Question, Setting,
   Identification, Data, Key result, How THIS paper differs}. Keep each cell terse.

5. CITATION HYGIENE
   - List claims in my draft that currently lack a supporting citation.
   - Flag any citation I am at risk of mischaracterizing.
   - Never generate a reference you cannot verify; mark gaps as "[VERIFY]".

6. ONE-PARAGRAPH POSITIONING
   Draft the paragraph that will sit in the introduction, naming the 2–3 papers we
   are closest to and the one sentence that separates us from each.

CONSTRAINTS
- Absolutely no fabricated or half-remembered citations. When unsure, output "[VERIFY: ...]".
- Prefer "extends / reconciles / overturns" framing over "is related to".
```

---

## Quality bar

- [ ] Literature is grouped by contribution, not listed by year.
- [ ] Each strand names the single frontier paper we must engage.
- [ ] The differentiation table makes "how we differ" legible at a glance.
- [ ] Every unverifiable reference is flagged `[VERIFY]`, none invented.
