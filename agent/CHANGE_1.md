# v2 - Change 1: replace the outdated rate sheet (targets RC1)

**Root cause targeted:** RC1 "Stale 2025 rate sheet beats the current website" - 37 of 60 conversations
affected in v1; fixing it alone would unlock an estimated 13 (after the full re-grade) (analysis/root_causes.py).
**One change only.** Nothing about policies, refusals, tone or design.

## Before you start (in Agentplace)
1. **Do not touch the v1 project.** v1 (https://qoyhkmwrdb93.run.agentplace.io) stays frozen as the "before".
2. In the project menu, choose **Duplicate**. Rename the copy "Happy Tails v2".
3. Open the **copy**. Check the model picker says **GPT-6 Luna**.

## Message to paste into the copy's builder (exactly)
> The rate sheet I attached earlier is last year's (2025) and is out of date. Please remove it and use
> this current rate sheet instead, attached. The prices and terms on our website are the current ones.
> Don't change anything else about how the agent works or looks.

**Attachment:** `work/knowledge/v2-upload-Happy Tails rate sheet (current Nov 2026).md` (the site's current
rates page, snapshot 11 Nov 2026).

## Protocol
- If the builder asks questions: answer only facts an owner knows; for rules, "Use what's on our website."
- Approve with the neutral option. Log every exchange in `runs/v2/BUILDER_LOG.md`.
- When the builder says it's done: **Publish** the copy (Public, sign-in off, duplication off) and send the URL.
- Record time of change. Then: full core re-run (60 x 3), same harness, same frozen tests.

## Expected effect (written BEFORE the run, so we can't fit the story afterwards)
- Most RC1 checks should flip to pass (prices $65 / $90 / $85, $350 pack, $120 puppy, no $161, no +$5).
- RC2 behaviour (saying "can't verify" policies) should mostly **not** change - it's a different cause.
- Risk: the current rates page also contains policy text (holiday terms, vaccines, meds), so some RC2
  checks may improve as a side effect. If so, we report it as a side effect of change 1, not hide it.
- Possible regression to watch: grooming "+" prices might now be quoted as fixed numbers.
