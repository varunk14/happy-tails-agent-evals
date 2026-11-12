# Happy Tails agent evals

Test set, harness and results for a customer-facing planning agent I built on
[Agentplace](https://agentplace.io) for Happy Tails Pet Resort in Cedar Park, Texas. The agent helps
pet owners plan boarding, daycare, grooming and training, gives estimates from the resort's published
prices, and emails a booking request for staff to confirm. It runs on GPT-6 Luna.

This is an independent project. I am not affiliated with Happy Tails, and the agent is not their
official booking channel. Booking requests from the tests went to a test inbox, never to the resort.

- v1 (before): https://qoyhkmwrdb93.run.agentplace.io
- v2 (after): https://dt6irinn7a8z.run.agentplace.io

## Results

Each conversation was run three times. A conversation counts as passed only if every check passes in
all three runs (pass^3), so a reply that is right once and wrong twice still fails.

| Test set | Metric | v1 | v2 |
|---|---|---|---|
| Core (60 conversations) | Passed in all 3 runs | 6 | 32 |
| | Runs passed (of 180) | 25 | 119 |
| | Conversations with a material error | 51 | 22 |
| Held-out (20 conversations) | Passed in all 3 runs | 1 | 13 |
| | Runs passed (of 60) | 5 | 43 |
| | Conversations with a material error | 16 | 5 |

The held-out set was written with the core set, run once on v1 and then sealed. Nobody looked at it
while v2 was being fixed, so the v2 held-out score is the honest measure of whether the fixes generalise.
An intermediate version (v2.1, rate sheet fix only) scored 17/60 on the core set. Full table:
[analysis/FINAL_RESULTS.md](analysis/FINAL_RESULTS.md).

## What the tests cover

80 multi-turn conversations, written and frozen before the agent was built. Twelve categories:
questions the agent should simply answer, prices it must not invent, the resort's own conflicting or
outdated pages, discounts, eligibility, honesty about bookings, handoff to staff, off-topic requests,
missing details, attempts to push it off task (fake managers, prompt injection, a "vet" role-play),
other customers' data, and long conversations where earlier details must hold.

Every check is binary and tied to a written rule in [spec/TARGET_BEHAVIOUR.md](spec/TARGET_BEHAVIOUR.md).
There are three kinds:

- **Pattern checks** run automatically (for example: no emoji, no internal tool names, no made-up
  confirmation numbers). Each pattern has positive and negative controls in the validator.
- **Judged checks** need reading, such as "gives $195 for three nights" or "says staff confirm the
  holiday terms". Two independent graders scored every judged check without seeing each other's work.
  Disagreements were settled against the transcript. Agreement was 97% on the final run, and every
  decision is logged in [grading/ADJUDICATIONS.md](grading/ADJUDICATIONS.md).
- **Outcome checks** confirm the email actually arrived (exactly once, only after the customer said yes,
  never when they said no). Each test customer's email address carries a run tag, so I counted the
  messages in the test inbox by hand.

Criteria changes made after a run started are recorded in [tests/AMENDMENTS.md](tests/AMENDMENTS.md),
and every version was re-scored under the same wording.

## What changed between v1 and v2

Each change was a plain-language instruction to the Agentplace builder, logged with the builder's reply
in [agent/](agent/). Root causes were measured before each change, along with how many conversations a
fix should unlock.

1. **Current rate sheet.** v1 had last year's prices and quoted them with confidence. This was the
   largest single cause of failures (37 of 60 conversations).
2. **A real next step.** v1 told customers it was an unofficial demo and showed them an inbox address.
   v2 says what it can do, that Happy Tails staff confirm every booking, and gives the resort's number.
3. **Use what the website says.** v2 has the full current site text and states published policy
   directly instead of saying it "can't verify" it. It prices stays from the dates instead of asking the
   customer how many billed days to use.

Changes 2 and 3 were applied together and measured in one run. They touch different checks, so their
effects can still be separated by root cause, but not perfectly.

## What still fails

- The vaccine record must reach the resort a week before arrival. v2 often leaves this out.
- Asked about a limping dog, it still gives care advice instead of one line pointing to a vet.
- It is not consistent about whether Christmas dates fall under the holiday policy.
- After a text-only answer, the plan card is not shown again.
- Fixing the rate sheet made it mention the holiday deposit "in case" ordinary late-January dates
  count as a holiday.

Visual checks are in [visual/VISUAL_RESULTS.md](visual/VISUAL_RESULTS.md). Phone layout and voice mode
were not tested.

## Repository layout

```
tests/      the 80 conversations (core/, holdout/), global checks, judge fact sheet, amendments
spec/       the behaviour rules every check cites, and the design brief
harness/    MCP client, runner and grader
scripts/    test validator and grading tools
results/    transcripts, verdicts and reports for each run
grading/    blind grader output, adjudications, judge calibration
analysis/   root-cause grouping and version comparisons
agent/      builder messages, builder logs, version history
visual/     manual UI checks with screenshots
```

## Running it

Python 3.11+ and PyYAML. Every published Agentplace agent exposes an MCP endpoint, which the harness
uses to hold real multi-turn conversations.

```bash
pip install -r requirements.txt
python scripts/validate_tests.py
python harness/runner.py --url https://dt6irinn7a8z.run.agentplace.io --version mytest --set core --trials 3
python harness/grade.py runs/mytest/<run_id>
```

`grade.py` scores the pattern checks and writes the judged checks to `judge_requests.jsonl`.
Verdicts go back into `judge_results.jsonl` (see [harness/JUDGING.md](harness/JUDGING.md)), and
inbox results go in `outcomes.yaml`.

## Limits

- The graders were LLMs. A blind 30-item calibration and the two-grader setup catch a lot, but both
  graders can share a blind spot.
- Prices and policies are from the resort's website as of 11 November 2026.
- The agent is not deterministic. Three runs per conversation make the scores fairer, but a rerun will
  not match exactly.
- Transcripts omit raw tool output and use a placeholder for the test inbox address.
