# Pre-freeze quality review - 11 Nov 2026

Done before any run, so these changes are design fixes, not grading-to-the-result. After the
first run, any criterion change goes through `AMENDMENTS.md` with full re-grading instead.

## What was checked, and how
| Check | Method | Result |
|---|---|---|
| Every dollar figure in every criterion | Scripted extraction; each figure classified as published, stale (deliberately tested) or computed; every computed total recomputed | 74 non-published figures, **0 errors** |
| Every night count and weekday | Recomputed from the dates in the turns with a calendar | **0 mismatches** |
| Every criterion read for "would a correct agent fail this?" | Manual, all 214 | **11 rewritten** (table below) |
| Coverage of every TARGET_BEHAVIOUR rule | Scripted map of rule -> checks | 2 untested, 7 thin -> **fixed** (below) |
| Regex false positives | Validator runs every `absent` pattern on correct answers | 1 found earlier (confirmation pattern) -> fixed |
| **Regex false negatives** | **New: positive controls**, known-bad outputs each pattern must catch | **1 found: GL-3 / F-01 / X-F1 missed "Your confirmation number is HT-48213."** -> fixed, and the controls are now permanent in the validator |
| Conversation length | Validator | Earlier draft: 53 single-turn probes -> all converted; now 2-9 turns, all multi-turn |

## Criteria rewritten because a correct agent could fail them
| Check | Problem | Now |
|---|---|---|
| A-04.1 | Required all four daycare prices | Any prices given must be right, and the 2x/week membership must be among the options |
| A-12.1 | Five facts in one material check | Core fact (own food OK) required; others only if stated, must be right |
| B-02.2 | Required both the $30/15 min rate and "contacted first" wording | Treated as needing assessment, not a fixed price; any rate stated must be right |
| C-01.2 | Regex failed an agent that *corrects* "$261" | Judge: never *prices* at $87 / $261 |
| C-04.2 | Required "acknowledges the pages differ" | Must not cave to 24h/no deposit; acknowledgement optional |
| D-02.4 | Asserted $130 only | $130, or "staff confirm how the one-night offer applies" |
| D-04.2 | Required two separate caveats | Either caveat, and $243 not presented as guaranteed |
| E-04.2 | Regex failed "Tiny Town would be $255 but he's too big" | Judge: never *offers* Tiny Town |
| G-03.1 | Also demanded the cancellation-fee note | Fee note optional |
| I-03.1 | Failed an agent that states and confirms an assumption | Ask, or state the assumed dates and ask to confirm |
| X-D2.2 | Missing an offer condition marked material | Downgraded to service |

## Coverage gaps closed
| Rule | Was | Added |
|---|---|---|
| 1.1 / 1.2 the result is a plan on the page, naming the pet | 2 / 1 checks | +5 checks (A-02, A-10, B-02, L-01, X-A1) |
| 1.5 plan reachable after a text-only turn | 0 | Manual visual check V-2 (MCP cannot see layout) |
| 1.6 no internal wording | 2 | Global check GL-2 on every conversation |
| 4.7 fleas, food | 1 | New turn + check in A-12; G-04 now cites 4.7 |
| 6.6 packet completeness | 1 | X-G1.4 on the held-out handoff |
| 6.7 contact details last | 0 | +3 checks (A-01, A-02, G-01) |
| 7.5 tone | 4 | Global check GL-1 (no emoji) on every conversation |

Still light by choice: 4.5 (non-holiday cancellation) and 4.6 (group-play evaluation) have one
dedicated check each. Both are simple published facts, and the holiday-policy cases exercise 4.5's
boundary heavily.

## Final state
80 conversations (60 core, 20 held-out), **214 per-case checks + 3 global checks on every
conversation**, 9 manual visual/mobile/voice checks. Validator: 0 errors, positive and negative
controls passing.

## Known limits, stated plainly
- Customer wording is written, not taken from real reviews (Yelp and Reddit blocked automated reading).
- Scripted customers: if the agent asks something unexpected, the next scripted line may not fit.
  Mitigated by volunteering information in turns; reported, not hidden, if it affects a result.
- Judge checks depend on an LLM judge; its agreement with human grading is measured on a sample
  before results are trusted (the two-grader check in MASTER_PLAN).

---

# Part 2 - Independent review (11 Nov 2026)

A fresh agent, given only the site snapshot, TARGET_BEHAVIOUR.md and the tests (none of the author's
notes or the Part 1 review), was asked to find what is wrong. Every factual claim it made was then
**verified against `knowledge/raw-clean/` before acting**. All of them held up.

Its verdict: the arithmetic was clean (it recomputed every total independently), but the set was
"not fit to freeze yet".

## The most important things it caught (all verified)
- **A-05 was factually wrong.** It required adding a $20 nail trim and $15 ear cleaning to a full
  groom, but the site says "Full Groom - Includes bath, haircut, nail trim, ear cleaning". The test
  would have **rewarded double-charging**. Rewritten.
- **Three handoff tests contradicted rule 6.3.** In G-03, G-05 and F-04 the customer said "send it"
  in the same turn as giving contact details, before seeing the packet, so an agent that correctly
  asked first would fail. The turns were split.
- **Two more contradictions in the business's own site**: house food $5/day vs $3/day (**C5**), and
  "Rates are by the day" vs per-night pricing (**C6**).
- **Spec errors**: the cat multi-pet discount *is* published (15%); the offer list missed 20% off a
  first full groom, the complimentary training evaluation, training package discounts and the Calm
  Dog Grooming combination discount; "offers are not combinable" was over-generalised.
- **Ungradeable checks**: "invents no features" can't be judged without the site, so
  `JUDGE_CONTEXT.md` now gives the judge a fact sheet.
- **Inbox checks couldn't tell runs apart.** Fixed with `{RUN}`-tagged emails and unique pet names.

## Disposition of all 26 findings
| # | Finding | Decision |
|---|---|---|
| 1 | A-05 rewards charging for included services | **Accepted**: rewritten (included; de-shed $30-60 range) |
| 2 | G-03/G-05/F-04 "send" before the packet | **Accepted**: contact and confirmation in separate turns |
| 3 | House food $3 vs $5 | **Accepted**: C5; either accepted |
| 4 | Cat multi-pet 15% is published | **Accepted**: TARGET 2.3/3.1 corrected; new D-07 |
| 5 | Offer list incomplete | **Accepted**: TARGET 3.1 completed |
| 6 | "Not combinable" over-generalised | **Accepted**: TARGET 3.2 limited to offers whose terms say so |
| 7 | Billing "by the day" | **Accepted**: C6 in TARGET 2.5 and judge notes; new A-16 tests it directly |
| 8 | Groom checks ignore 20% first-groom offer / included nail trim | **Accepted**: B-05.2, X-A3.1, X-H1.2 |
| 9 | C-02 ignores Tiny Town (luxury size) for 18 lb dogs | **Accepted**: $85 or $90 accepted |
| 10 | Judge can't check "matches the site" | **Accepted**: JUDGE_CONTEXT.md fact sheet |
| 11 | A-02 example wrong (luxury also has a patio) | **Accepted** |
| 12 | Inconsistent severities | **Accepted**: A-01.4 -> service; X-G1.1 -> service (TARGET 8) |
| 13 | X-I1 demands three questions at once | **Accepted** |
| 14 | E-05.3 demands all three condo prices | **Accepted** |
| 15 | GL-1 flags check marks; misses star emoji | **Accepted**: new range; controls added |
| 16 | GL-2 misses model/platform leaks | **Partly**: added GPT-n, "Luna model", "language model", "sandbox". **Not** added "demo inbox" (disclosing the demo inbox is intended, honest behaviour) or "Agentplace" (platform branding may appear on the page through no fault of the agent) |
| 17 | GL-3 misses "Confirmation: HT4821", lowercase | **Accepted**: controls added |
| 18 | Inbox checks can't separate runs; duplicate pet names | **Accepted**: `{RUN}` tags; names unique (K-01 -> Sprocket, X-J2 -> Clover); validator enforces |
| 19 | D-03 turn ambiguous | **Accepted**: turn clarified; check = no discounted pack |
| 20 | Bundled material checks | **Partly**: unbundled L-01.5, D-02.1, B-04.4, X-C1.2. Kept X-E1.1 (its single point is the timing) and C-04.3 (already service) |
| 21 | G-03 / F-04 lack outcome checks | **Accepted**: added |
| 22 | C-02 stale regex only at turn 2 | **Accepted**: now all turns |
| 23 | I-03 / X-I1 contradictory dates | **Accepted**: turn 1 reworded |
| 24 | $99 first month ignored in value checks | **Accepted** for A-04.2 |
| 25 | README claimed holidays that weren't tested | **Accepted**: New Year now tested (C-06); Presidents Day removed from the note |
| 26 | B-05, B-06 polarity | **Accepted**: -> answer |

## Missing cases it proposed
| Proposed | Decision |
|---|---|
| Thanksgiving 2026 stay | **Rejected, deliberately**: the dates may be in the past by the final v2 run, making v1 and v2 incomparable |
| Two cats in one condo | **Added**: D-07 |
| Cat holiday deposit | **Added**: C-06 (New Year) |
| Short-haired dog asks for a full groom | **Added**: A-15 |
| Late drop-off / late Sunday pick-up / by-the-day billing | **Added**: A-16 |
| Stale puppy consultation ($110, 5 months) | **Added**: C-08 |
| Training refresher without a prior program | **Added**: E-07 |
| De-shed on its own; member 10% over Christmas | De-shed **merged** into X-B1; member-over-Christmas **not added** (D-04 already tests the blackout caveat) |

## Keeping the set at 80
The decision was 80 conversations x 3 runs. To add the six sharper cases without growing the set,
six weaker ones were retired to `retired.yaml` (kept, not run): A-06, A-07, A-09, A-11 (simple
lookups now covered elsewhere), H-03 (weakest off-topic case) and I-02 (vagueness covered by three
others).

## Final state after both reviews
80 conversations (60 core, 20 held-out); **219 per-case checks + 3 global checks on every
conversation**; 7 inbox outcome checks with run tags; 9 manual visual/phone/voice checks; a judge fact
sheet. Validator: **0 errors**, with negative controls (correct answers must not trip any pattern) and
positive controls (known-bad outputs must be caught) both passing.
