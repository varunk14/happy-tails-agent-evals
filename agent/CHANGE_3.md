# v2 - Change 3: answer from the published website (targets RC2, plus RC9 billing basis)

**Measured on v2.1:** RC2 = 56 failed check-trials in 20 conversations (unlocks ~13 alone); RC9 = 5 conversations.
Many missed facts were already in the attached rate sheet (vaccine record one week before arrival, no injections,
flea treatment at owner's expense), so this is mainly a behaviour change ("state what the site says"), plus the
other website pages as reference. **Not test-specific:** no test answers are written into the agent; the full site
is given and the 20 held-out tests check that the change generalises.

**Owner decision (12 Nov 2026):** Changes 2 and 3 go in back to back and are measured together (one core re-run +
the held-out run), to save rounds. Consequence, stated in the write-up: improvements are attributed by root-cause
category (RC5 checks vs RC2/RC9 checks are disjoint), not by a separate run per change.

## Message to paste into the Happy Tails v2 builder (after Change 2 is done; model GPT-6 Luna)
Attach: `work/knowledge/v2-upload-Happy Tails website (snapshot 11 Nov 2026).md`
> Attached is the full text of our current website. Please add it to what the agent knows and change only how the
> agent uses our published information:
> 1. When our website or rate sheet states a rule, price or policy, say it plainly as our policy. Don't say you
> "can't verify" or "can't confirm" something the website states. Only when the website doesn't cover something,
> say Happy Tails staff confirm it.
> 2. For a boarding estimate, count nights as check-out date minus check-in date and give the total straight away;
> mention that the resort bills by the day and staff confirm the final total. Don't ask the customer how many billed
> days to use.
> Don't change anything else about how the agent works, talks about booking requests, or looks.
