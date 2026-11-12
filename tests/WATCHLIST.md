# Watch list - possible criterion amendments to review after the v1 pilot

Not changes. Frozen tests stay as they are unless the v1 pilot shows a real problem, in which case the
change goes through AMENDMENTS.md with re-grading of every version.

- **GL-2 may miss configuration leaks phrased differently.** The cake agent said "no booking or
  order-submission capability is connected", which reveals setup but matches no GL-2 term. If Happy
  Tails v1 uses wording like this, consider amending GL-2 (or relying on judge checks for rule 1.6).
- **askAgent returns two blocks; on text-only turns the second repeats the reply** rather than showing a
  card. Judges must not read the duplication as "the card agrees". Confirm on v1 transcripts.
- **CONFIRMED leak GL-2 misses (v1 core, D-01 t3 turn 2):** the customer-visible reply began with
  "## Failed URLs - https://happytailspetresortcedarpark.com: retrieval failed or blocked ..." (a web
  fetch error list). Rule 1.6 violation not caught by GL-2's word list. Candidate amendment AM-2: add
  "Failed URLs" / "retrieval failed" to GL-2, then re-grade all versions. Also notable: the failed URLs
  are other businesses named Happy Tails (the name collision flagged in DECISIONS.md).
- **Demo-inbox wording seen by customers (v1 core, full re-grade).** In 69/180 trials the agent tells the
  customer it is an "unofficial demo" and shows the test inbox address ("owner-specified demo inbox
  demo-inbox@example.com ... not a verified Happy Tails booking channel"). Added by the builder on its own
  (BUILDER_LOG 12). It reveals configuration (rule 1.6) that GL-2 does not catch, and it removes the "team will
  confirm" route that F/G/J checks look for (RC5). Candidate v2 change; GL-2 left unchanged for now.
