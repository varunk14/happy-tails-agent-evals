# Harness changelog
The harness is code and may be fixed; the tests (tests/FROZEN.md) may not, except via AMENDMENTS.md.

- **11 Nov 2026, after the v1 pilot**: `askAgent` returns reply text, card text **and** the agent's
  internal tool results (`[Tool Result: calculate_happy_tails_estimate]`, `filesystem` reading SKILL.md,
  `web_search`, Gmail tool schemas). The customer never sees these. Grading now uses only
  customer-visible blocks (`visible()` in grade.py), matching the frozen tests' definition ("the agent's
  text and card"). Tool results stay in the transcripts as evidence. No test was changed.
