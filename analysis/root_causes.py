"""Group v1 failures by root cause (not symptom) and estimate what fixing each cause would move.

Each failed check is assigned ONE primary root cause, decided while grading the transcripts
(reasons in runs/<v>/<run>/judge_results.jsonl). Counterfactual: a conversation is 'unlocked' by a cause
if every check it failed (in any trial) belongs to that cause.
Usage: .venv/bin/python analysis/root_causes.py runs/v1/<run_id>
"""
import collections, json, sys, pathlib

RC = {
 "RC1 Stale 2025 rate sheet beats the current website": """A-05.3 A-01.1 A-01.2 A-02.1 A-02.3 A-02.4 A-04.1 A-05.1 A-08.1 A-08.4 A-10.1 A-10.2 A-12.2 A-13.3 A-14.3
   A-16.3 B-02.1 B-03.2 B-03.3 B-04.1 B-04.2 B-05.2 B-05.4 B-06.3 C-01.1 C-01.2 C-01.3 C-02.1 C-02.2 C-02.3 C-03.1 C-03.2
   C-03.3 C-05.3 C-06.1 C-08.1 C-08.2 D-01.2 D-03.3 D-04.1 D-05.2 D-05.3 D-07.2 E-04.3 E-05.3 E-06.3 E-07.3 G-01.4 H-01.2
   I-01.1 I-03.2 I-03.3 J-01.1 J-01.4 L-01.2 L-02.1 L-02.2 L-02.3""",
 "RC2 Website facts not used: says 'can't verify' what the site states": """A-04.3 D-06.3 E-01.3 H-02.3 A-02.2 A-03.1 A-03.2 A-03.3 A-05.2 A-12.3
   A-13.1 A-14.1 A-16.1 A-16.2 B-03.1 B-05.1 B-06.1 B-06.2 C-06.2 D-01.1 D-02.1 D-02.3 D-02.4 D-04.2 D-06.1 D-06.2 D-07.1
   E-01.1 E-01.2 E-02.1 E-03.1 E-04.1 E-05.1 E-06.1 F-02.2 G-04.1 I-01.3 J-01.3 L-01.1""",
 "RC3 Gives in under pressure or a false premise": "B-01.2 B-02.4 B-04.4 C-04.2",
 "RC4 Does off-task work": "H-01.1",
 "RC5 No next step / no route to staff": "J-02.2 J-03.2 F-01.1 B-01.3 F-02.1 F-02.3 F-03.1 F-03.2 J-04.2 K-01.2",
 "RC6 Internal wording shown to customers": "GL-2",
 "RC7 Reasoning slip": "A-04.2",
 "RC8 Plan card missing or out of sync with the chat": "A-10.4 L-01.4",
 "RC9 Gives veterinary care advice": "J-04.1 J-04.3",
}
CHECK2RC = {c: rc for rc, cs in RC.items() for c in cs.split()}

run = pathlib.Path(sys.argv[1])
res = json.loads((run / "results.json").read_text())
fails = [c for c in res["checks"] if c["verdict"] == "FAIL"]
unmapped = sorted({c["check"] for c in fails} - set(CHECK2RC))
if unmapped: sys.exit(f"unmapped failed checks: {unmapped}")

by_rc = collections.defaultdict(list)
conv_rcs = collections.defaultdict(set)
sev = collections.defaultdict(collections.Counter)
for c in fails:
    rc = CHECK2RC[c["check"]]
    by_rc[rc].append(c)
    conv_rcs[c["key"].split("__")[0]].add(rc)
    sev[rc][c["severity"]] += 1
flaky = collections.Counter()
per_check_trials = collections.defaultdict(set)
for c in fails: per_check_trials[c["check"]].add(c["key"].split("__t")[1][0])
for chk, ts in per_check_trials.items():
    if len(ts) < 3: flaky[CHECK2RC[chk]] += 1

graded = [cid for cid, r in res["cases"].items() if r["verdict"] != "PENDING"]
passing = [cid for cid in graded if res["cases"][cid]["verdict"] == "PASS"]
lines = ["# v1 failures by root cause", "",
         f"Graded conversations: {len(graded)} (pass^3: {len(passing)}). Failed check-trials: {len(fails)}.", "",
         "| Root cause | Failed check-trials | Material | Conversations affected | Unlocked if only this is fixed | Checks that failed in only 1-2 of 3 trials |",
         "|---|---|---|---|---|---|"]
for rc in RC:
    affected = [cid for cid, s in conv_rcs.items() if rc in s]
    unlocked = [cid for cid, s in conv_rcs.items() if s == {rc} and cid in graded]
    lines.append(f"| {rc} | {len(by_rc[rc])} | {sev[rc]['material']} | {len(affected)} | {len(unlocked)} | {flaky[rc]} |")
pair = [cid for cid, s in conv_rcs.items() if s <= {list(RC)[0], list(RC)[1]} and cid in graded]
lines += ["", f"Unlocked if RC1 **and** RC2 are both fixed: **{len(pair)}** conversations.",
          f"Conversations failing for one cause only: {sum(1 for s in conv_rcs.values() if len(s)==1)}; for two or more: {sum(1 for s in conv_rcs.values() if len(s)>1)}."]
out = "\n".join(lines) + "\n"
(run / "ROOT_CAUSES.md").write_text(out); print(out)
