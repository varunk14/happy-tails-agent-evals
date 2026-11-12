# Test set FROZEN - 11 Nov 2026

Frozen after two pre-run reviews (tests/REVIEW.md). From here, any change to a case or criterion
goes through tests/AMENDMENTS.md (old text, new text, reason) and every version is re-graded.

SHA-256 fingerprints of the frozen files (re-run the command below to prove nothing changed silently):

```
a8491c50b31d9d179226568b2ae4b38c5ac50aeea3c4ac432a9e6050c8cd3c39  tests/core/A_should_answer.yaml
139a54e0f4b8af633194881018c864851632fb4ada8aa5f7a8596c662140fd5d  tests/core/B_unknown_prices.yaml
68d053d521dfae6b4e539650a1818e9cfe1a98950d967dcfe84eafa0b618dfaa  tests/core/C_stale_conflicting.yaml
b53e2c9881607d08ea7a6e559675649de67f2d1fcda4cfbd99df7af71ab82058  tests/core/D_discounts.yaml
02164e3a09b9b254c1b8f5cf763b6e7a716925f29afc0c193cfda1e75993278e  tests/core/E_eligibility.yaml
5f84762fef57b94d754863a2dfd778b1b0618a2eb15785831e7a4ce4c901358d  tests/core/F_booking_honesty.yaml
e4b8d46d3f427fe68c07670e7cb301f81214d8104d5ae9a6994844ef659245bd  tests/core/G_handoff.yaml
42ea2c8a6b5564bc62d71b4629835f715ced46aa10d967a273b3063d9aa9e696  tests/core/H_off_topic.yaml
3dd0674f724d822620f7d1d8269044a6103b0b2b40d143bf8f842f3c82991bc7  tests/core/I_missing_details.yaml
05377afbdd02bc4a811eca9e7193deb14cdb70c3b8499083c843f3849949daca  tests/core/J_pushed_off_task.yaml
465d41b69ba1c6e94fb6e23085dbcaa8b3c5250e5468bcb9c2e501c4fc5fc812  tests/core/K_authorization.yaml
0baba86dc2d02fd8b660f423698732bd01af6db96107e26f822a5357639fc0e0  tests/core/L_long_memory.yaml
08b097ab5c0282f42f92992c56984e144b95f8c6fbbb8c54522c5e09e948ec0d  tests/holdout/holdout.yaml
7bff9ce10b2fbb26da98963891b8b85df7242aec060fc1cb8d8db70159c9c965  tests/global_checks.yaml
01185b6b0785086fa1f28be22f65469673be9ebd1c0f66d21d24189ab86540c9  tests/JUDGE_CONTEXT.md
ecc278b3e8ab9587620a3f564c190e02ab8a29667c3d3508bda761dc66c0305e  TARGET_BEHAVIOUR.md
```

Verify: `shasum -a 256 -c <(sed -n "/^[0-9a-f]\{64\}/p" tests/FROZEN.md)`


Fingerprint for tests/global_checks.yaml updated 12 Nov 2026 by amendment AM-3 (tests/AMENDMENTS.md). All other files unchanged.
