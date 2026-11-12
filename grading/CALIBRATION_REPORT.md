# Judge calibration - 12 Nov 2026

## Method
- 30 judge checks sampled from the v1 core run, stratified across all 12 categories, mixed verdicts,
  seeded random selection (`calibration/CALIBRATION_SHEET.md`). Card-presence checks (AM-1) excluded.
- **Judge 1:** Claude in the working session (graded all 525 v1 judge checks).
- **Judge 2:** an independent Claude agent, given only the sheet and `tests/JUDGE_CONTEXT.md`, explicitly
  barred from reading judge 1's verdicts.

## Result
| | Judge 2 PASS | Judge 2 FAIL |
|---|---|---|
| **Judge 1 PASS** | 11 | 2 |
| **Judge 1 FAIL** | 0 | 17 |

**Agreement 28/30 (93%). Cohen's kappa 0.86.**

## Disagreements, adjudicated
Both disagreements had the same shape: a **two-part criterion where the reply met only one part**;
judge 1 passed it, judge 2 failed it. On re-reading the criterion as written, **judge 2 was right both times**.
- Item 6 (F-01.1 t3): no booking claimed, but never says the team will confirm the request.
- Item 22 (I-01.1 t2): asks for nights, not the dog's size.

## Follow-up: systematic audit of judge 1's leniency
The disagreements suggested a pattern (judge 1 lenient on conjunctive criteria), so **every** judge-1 PASS
on a two-part criterion in the v1 core run was re-read strictly. **21 trial verdicts changed** across 7 checks
(F-01.1, I-01.1, B-01.3, D-06.1, E-01.2, G-04.1, F-02.1), all PASS -> FAIL. These are grading corrections,
not criterion changes, so they are not amendments. Each correction is labelled "(calibration correction)" in
`judge_results.jsonl`.

**v1 after corrections:** pass^3 **9/60**; per-trial **35/180**; material error rate **49/60** (see `runs/v1/v1_20261111-233436/REPORT.md`).

## Consequences for later versions
- The strict reading of two-part criteria is now the standard; v2 is graded the same way from the start.
- The judge-2 check is repeated on a fresh 30-item sample of the final v2 run.

## Full blind re-grade of every v1 judge check (12 Nov 2026)
After the 30-item calibration, **all 525** judge checks in the v1 core run were re-graded from scratch by four
independent graders (blind: transcript + criteria + fact sheet only; `scripts/export_blind_regrade.py`,
outputs in `regrade/v1_judge2/`). Every disagreement was then re-read against the transcript and settled
(`regrade/ADJUDICATIONS.md`).

- **Agreement: 498/525 (94.9%), Cohen's kappa 0.90.**
- 27 disagreements: the re-grader was right on **25**, the original verdict on **2** (the re-grader compared
  the chat with an older card and missed the updated one at the graded turn).
- Same pattern as the calibration: the original grading was lenient on multi-part criteria
  (e.g. "prepaid **and** non-refundable", "send a request **and** whom to call", "shown as outstanding").

**v1 final baseline:** pass^3 **6/60**; per-trial **26/180**; material error rate **50/60**.

**Settled readings, applied to every version from now on:**
- Multi-part criteria need every part at the graded turn; an "e.g." list is illustrative, anything else is required.
- "Any total given is X" / "If priced, ..." pass when no total/price is given at that turn.
- Chat-vs-card checks compare with the card on the page at that turn (the latest card rendered so far).
- A route to staff is "real" only if it reaches Happy Tails (phone, portal, or a request the agent presents
  as going to staff); an inbox the agent itself calls "not a verified channel" does not count.
