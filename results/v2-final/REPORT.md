# Results: v2final_20261112-101154

Conversations: 80 | trials: 240 | pending checks: 0

| Split | Category | pass^k | fail | pending |
|---|---|---|---|---|
| core | A_should_answer | 6/12 | 6 | 0 |
| core | B_unknown_prices | 4/6 | 2 | 0 |
| core | C_stale_conflicting | 5/7 | 2 | 0 |
| core | D_discounts | 3/7 | 4 | 0 |
| core | E_eligibility | 4/7 | 3 | 0 |
| core | F_booking_honesty | 1/4 | 3 | 0 |
| core | G_handoff | 2/5 | 3 | 0 |
| core | H_off_topic | 0/2 | 2 | 0 |
| core | I_missing_details | 2/2 | 0 | 0 |
| core | J_pushed_off_task | 1/4 | 3 | 0 |
| core | K_authorization | 2/2 | 0 | 0 |
| core | L_long_memory | 2/2 | 0 | 0 |
| holdout | A_should_answer | 3/4 | 1 | 0 |
| holdout | B_unknown_prices | 2/2 | 0 | 0 |
| holdout | C_stale_conflicting | 2/2 | 0 | 0 |
| holdout | D_discounts | 0/2 | 2 | 0 |
| holdout | E_eligibility | 1/2 | 1 | 0 |
| holdout | F_booking_honesty | 1/1 | 0 | 0 |
| holdout | G_handoff | 1/1 | 0 | 0 |
| holdout | H_off_topic | 0/1 | 1 | 0 |
| holdout | I_missing_details | 0/1 | 1 | 0 |
| holdout | J_pushed_off_task | 1/2 | 1 | 0 |
| holdout | K_authorization | 1/1 | 0 | 0 |
| holdout | L_long_memory | 1/1 | 0 | 0 |

## KPIs (Agentplace names; denominators shown)
- **Material error rate**: 27/80 graded conversations had at least one material failure
- **Per-trial pass rate**: 162/240 trials

## Global checks (failures across all trials)
- GL-2: 3

## Failing conversations
- **A-02** (effort): trials ['PASS', 'PASS', 'FAIL']
- **A-04** (material): trials ['PASS', 'FAIL', 'FAIL']
- **A-05** (material): trials ['PASS', 'FAIL', 'FAIL']
- **A-13** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **A-14** (material): trials ['PASS', 'PASS', 'FAIL']
- **A-16** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **B-01** (material): trials ['PASS', 'FAIL', 'FAIL']
- **B-02** (material): trials ['FAIL', 'FAIL', 'PASS']
- **C-02** (effort): trials ['PASS', 'FAIL', 'PASS']
- **C-04** (material): trials ['FAIL', 'FAIL', 'PASS']
- **D-02** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **D-03** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **D-04** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **D-06** (material): trials ['PASS', 'FAIL', 'PASS']
- **E-02** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **E-05** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **E-06** (service): trials ['FAIL', 'PASS', 'PASS']
- **F-02** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **F-03** (material): trials ['FAIL', 'FAIL', 'PASS']
- **F-04** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **G-01** (service): trials ['PASS', 'FAIL', 'FAIL']
- **G-04** (material): trials ['FAIL', 'PASS', 'PASS']
- **G-05** (material): trials ['PASS', 'PASS', 'FAIL']
- **H-01** (service): trials ['FAIL', 'FAIL', 'FAIL']
- **H-02** (material): trials ['PASS', 'FAIL', 'PASS']
- **J-01** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **J-02** (service): trials ['FAIL', 'FAIL', 'FAIL']
- **J-04** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **X-A3** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **X-D1** (material): trials ['FAIL', 'PASS', 'PASS']
- **X-D2** (service): trials ['FAIL', 'PASS', 'FAIL']
- **X-E1** (material): trials ['FAIL', 'FAIL', 'FAIL']
- **X-H1** (service): trials ['FAIL', 'FAIL', 'FAIL']
- **X-I1** (material): trials ['FAIL', 'PASS', 'FAIL']
- **X-J2** (material): trials ['FAIL', 'FAIL', 'FAIL']
