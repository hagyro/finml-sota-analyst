# Prompt 03 — Conceptual Framework & Testable Hypotheses

> **Purpose:** Derive a clean mechanism (theory or conceptual framework) and translate it into sharp, falsifiable, pre-registered-quality hypotheses with signed predictions.
> **Use when:** Building the theory/framework section, or when a referee says "the hypotheses are ad hoc / unmotivated."
> **Target standard:** 4* — predictions are *derived*, not decorated; each hypothesis maps to a testable coefficient.

---

## Prompt

```
ROLE: Act as a theorist-empiricist hybrid building the conceptual framework of a 4* paper.
Every empirical prediction must be traceable to an assumption.

CONTEXT
- Research question: {{one sentence}}
- Outcome(s) Y: {{definition}}
- Key regressor / treatment X: {{definition}}
- Candidate mechanism(s): {{narrative of why X affects Y}}
- Theory tradition to build on: {{e.g., search frictions / agency / real options}}
- Available moderators / heterogeneity dimensions: {{list}}

TASK

1. MECHANISM STATEMENT
   - State the causal chain X → M → Y in words, naming the mediating channel M.
   - List the minimal assumptions needed for the chain to operate.

2. MODEL SKETCH (choose the lightest sufficient formalism)
   - Either a compact model (agents, objective, constraints, comparative static),
     or a formal conceptual framework if a full model is overkill.
   - Derive the sign of dY/dX and state what governs its magnitude.

3. HYPOTHESES (numbered, signed, testable)
   - H1 (main effect): direction + the coefficient that tests it.
   - H2–H3 (mechanism / mediation): what pattern confirms M is the channel.
   - H4+ (heterogeneity): where the effect should be larger/smaller and WHY.
   For each: state the empirical coefficient, its predicted sign, and the finding
   that would FALSIFY it.

4. RIVAL EXPLANATIONS
   - List 2–3 alternative mechanisms that predict the same main effect.
   - For each, give the distinguishing test that separates it from ours.

5. THREATS TO THE FRAMEWORK
   - Which assumption is most fragile? What happens to predictions if it fails?

6. FRAMEWORK-TO-EMPIRICS BRIDGE
   - Produce a table linking each hypothesis → specification → coefficient → predicted
     sign → falsification outcome. This becomes the backbone of the results section.

CONSTRAINTS
- No hand-waving: if a prediction cannot be signed, say so and explain why.
- Keep the formalism as light as the argument allows; rigor over decoration.
```

---

## Quality bar

- [ ] Every hypothesis names the exact coefficient that tests it and its sign.
- [ ] At least one rival mechanism has an explicit distinguishing test.
- [ ] Each hypothesis states what result would *falsify* it.
- [ ] A hypothesis→specification→coefficient bridge table exists.
