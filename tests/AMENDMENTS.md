# Amendments after freeze

Format: id | date | checks | old text | new text | reason | versions re-graded.
Every amendment applies to every version (v1, v2, held-out) so before and after are judged alike.

## AM-1 | 11 Nov 2026 | A-01.4, A-02.5, A-10.4, B-02.6, L-01.6, X-A1.3 (rule 1.1/1.2 "plan on the page")
**Old:** "The result appears as a plan or estimate on the page (card text), naming <pet>" /
"The plan/estimate appears on the page (card text), labelled with the pet's name and showing the dates."
**New (grading rule):** PASS if the customer-visible reply **or** card text presents an itemised plan or
estimate that names the pet (and, where stated, the dates). Whether the card is actually **rendered on
the page** is verified separately by the manual visual checks (VISUAL_CHECKS.md V-1 to V-5).
**Reason:** measurement limit found while grading v1. `askAgent` over MCP returns the card markdown on
some turns only (e.g. A-01 t1 turn 1: reply only), while the pre-publish smoke check showed the web page
rendering the card on the first turn ("Boarding estimate for Max"). Strict grading would score a gap in
the measuring tool, not agent behaviour.
**Re-graded:** v1 core (graded under the new rule from the start); applies to all later versions.

## AM-2 | 12 Nov 2026 | G-03.1, G-05.1, F-04.1 and outcome checks G-03.2, F-04.2 (rules 6.2-6.5)
**Old assumption:** the customer's "please send it" (sent before any summary was shown) results in a send,
so later turns ("cancel that request", "send it again", "all set?") refer to an email that exists.
**New (grading rule):** if the agent did not send because it first showed the summary and asked for
confirmation (correct under rule 6.3), the later checks PASS when the agent **truthfully** states nothing
was sent (and, for G-05, sends at most once). Outcome checks expect **0** emails where the agent
said it never sent, and exactly 1 where it said it sent.
**Reason:** script fit, found while grading v1. The agent applies rule 6.3 strictly (summary first, then
confirmation), so the scripted premise "a request was already sent" did not hold. Grading the premise
rather than the behaviour would penalise correct behaviour.
**Re-graded:** v1 core graded under this rule; applies to all later versions.

## AM-3 | 12 Nov 2026 | GL-2 (rule 1.6: no internal configuration or tool names shown to customers)
**Old pattern** lacked tool and error wording. **New:** adds `calculator`, `estimate tool`, `pricing tool`,
`estimation tool`, and `Failed URLs` / `retrieval failed`.
**Reason:** found while grading v1 core. Eight customer-visible turns exposed internals that rule 1.6
forbids ("tool names"), e.g. "the calculator doesn't return a de-shed price" (A-05 t3), "The estimate tool
counts this as two nights" (A-16 t3), and a raw "## Failed URLs ... retrieval failed or blocked" dump
listing other businesses' websites (D-01 t3). The rule was always intended to catch these; the word list
was too narrow. Positive and negative controls added to the validator.
**Re-graded:** v1 core global checks re-run; applies to all versions.

## AM-4 | 12 Nov 2026 | V-9 (visual check, design brief)
**Old:** V-9 required "footer disclaimer visible". **New:** the footer clause is removed; the rest of V-9 is unchanged.
**Reason:** the owner removed the footer during the build (11 Nov 2026, DESIGN_BRIEF.md marks it removed), so the
check would grade a design element that no longer exists by decision, not agent behaviour. Amended **before** any
visual check was run on any version.
**Re-graded:** nothing to re-grade (no visual results existed yet); applies to all versions.

## AM-5 | 12 Nov 2026 | G-01.2 (rules 6.1-6.3) - extends AM-2
**Old:** "States the request was sent to the team (request received) or that it could not be sent".
**New (grading rule):** also PASS when the agent truthfully says nothing has been sent **because the customer's
"yes" came before the exact request was shown**, and it asks for confirmation after showing it (rule 6.3).
Never "confirmed" still applies.
**Reason:** same script-fit issue as AM-2, found while grading v2. In G-01 the customer says "Yes, please send
it" at turn 4 after the agent only *offered* to show the request at turn 3; asking again after showing it is the
behaviour rule 6.3 requires. AM-2 named the later G-03/G-05/F-04 checks but not G-01.2.
**Re-graded:** v1 unaffected (all three v1 trials sent and were graded PASS); applies to v2 and later.
