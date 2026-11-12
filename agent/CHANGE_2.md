# v2 - Change 2: real route to staff, no demo-inbox wording (targets RC5)

**Measured on v2.1 (analysis/ROOT_CAUSES_v2_1.md):** RC5 = 43 failed check-trials in 18 conversations; fixing it
alone would unlock an estimated 13. The agent tells customers it is an "unofficial demo", shows the test inbox
address, and calls it "not a verified Happy Tails booking channel", so it never offers a real next step, never
says staff confirm, and gives no phone number. **Owner decision (12 Nov 2026): wording B.**
**One change only.** Prices, facts, refusals, design untouched. Email sending stays exactly as it is.

## Message to paste into the Happy Tails v2 builder (exactly; model GPT-6 Luna)
> Please change only how the agent talks about booking requests and next steps. Keep sending booking requests by
> email exactly as now, after the customer reviews the summary and confirms.
> 1. Never show customers the email address requests go to, and never call it a demo, a demo inbox, unofficial,
> a records system, or "not a verified channel". This includes the welcome text: replace the "unofficial planning
> demo" sentence with "I can help you plan a stay and estimate the cost. Happy Tails staff confirm every booking."
> 2. When a customer wants to book, say: "I'll put together your plan and a booking request. Only the Happy Tails
> team can confirm a booking, so call (512) 764-6150 to lock it in or for anything urgent."
> 3. After sending, say the request was sent, that it isn't a booking until the Happy Tails team confirms it, and
> give the same phone number. If a customer pushes you to confirm, say clearly: "Your request isn't a booking yet."
> 4. Whenever something can't be confirmed here (availability, a discount amount, holiday terms, an exception, a
> cancellation, a points balance), say that Happy Tails staff confirm it and give (512) 764-6150.
> Don't change anything else about how the agent works or looks.

## Expected effect (written before the run)
- Demo/inbox wording ~0/180 trials (v1: 69/180 trials; v2.1: 61/180). GL-2 unchanged.
- RC5 checks improve: B-01.3, B-03.2, C-02.2/.3, C-04.2, C-08.3, D-02.4, F-01..F-04, G-03.1, J-03.2, K-01.2.
- Outcome checks unchanged: emails still arrive once, only after confirmation.
- **Risks:** "sent to the team" drifting into "you're booked" (F, GL-3); the phone number repeated in every reply
  (effort); RC2 facts unaffected, so those conversations stay failing.

## Protocol
Same as Change 1: log the builder reply in runs/v2/BUILDER_LOG.md; publish; pilot G-01 + F-03 (1 trial) and check
one email arrives; then full core re-run 60 x 3; inbox count; two blind grader sets + adjudication.
