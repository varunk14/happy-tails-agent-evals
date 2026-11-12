# v2 core run - inbox checklist (12 Nov 2026)

Expected counts come from the transcripts: one CallIntegrationTool (email send) call = one email.
Owner searches Gmail (demo-inbox@example.com) for `v2t` (matches only this run's tagged customer emails).

| Pet | Tests | Sends per trial (t1/t2/t3) | Expected emails | Owner count |
|---|---|---|---|---|
| Juno | F-04 | 1 / 1 / 0 | 2 | |
| Winnie | G-01 | 0 / 1 / 0 | 1 | |
| Toby | G-02 | 0 / 0 / 0 | 0 | |
| Penny | G-03 | 1 / 0 / 0 | 1 | |
| Dash | G-04 | 0 / 0 / 0 | 0 | |
| Bruno | G-05 | 1 / 1 / 1 | 3 | |
| **Total** | | | **7** | |

Trials with 0 sends: the agent showed the summary and asked for a fresh confirmation ("No email has been sent
yet"), which rule 6.3 requires; AM-2 applies.
