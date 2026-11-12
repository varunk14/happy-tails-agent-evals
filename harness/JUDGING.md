# How judge checks are graded (decided 11 Nov 2026)

**Judge:** Claude (Opus 5.5) in the working Claude Code session, not an API script. Chosen by the owner.

## Protocol
1. `grade.py` writes every ungraded judge check to `judge_requests.jsonl`: the criterion (`pass`
   sentence), the turn it applies to, and the verbatim transcript (reply text + card text).
2. The judge reads `tests/JUDGE_CONTEXT.md` (fact sheet + grading notes) once per batch, then grades
   each request **against its `pass` sentence only**, writing one line per check to
   `judge_results.jsonl`: `{"key", "verdict": "PASS"|"FAIL", "reason"}`. One-sentence reasons that
   quote the transcript.
3. `grade.py` is re-run to merge the verdicts into the report.

## Guarding against self-grading bias
The same model wrote the criteria and grades them, so:
- **Strict reading**: the verdict follows the written criterion, not what the criterion was meant to say.
  If a criterion turns out ambiguous, that goes to `tests/AMENDMENTS.md`; it is not quietly reinterpreted.
- **Reasons quote evidence** from the transcript, so every verdict can be audited.
- **Calibration** (done 12 Nov 2026, see `calibration/CALIBRATION_REPORT.md`): a blind independent AI judge
  graded 30 stratified items: 93% agreement, kappa 0.86. Both disagreements exposed judge-1 leniency on
  two-part criteria; all such verdicts were then re-read strictly (21 corrected).
- **Same judge, same context, for every version**, so v1 and v2 are graded alike.

## Limits stated in the write-up
Grading in-session is less reproducible than a fixed API script with a pinned model and temperature.
The transcripts, criteria, verdicts and reasons are all saved, so anyone can re-grade them.
