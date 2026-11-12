"""Show pending judge checks grouped by conversation, so each transcript is read once.

Usage (from work/):
  .venv/bin/python harness/judge_view.py runs/<v>/<run_id> --list            # pending conversations
  .venv/bin/python harness/judge_view.py runs/<v>/<run_id> --case A-01       # all trials of one case
Verdicts are appended to <run>/judge_results.jsonl as {"key","verdict","reason"} (see JUDGING.md).
"""
import argparse, collections, json, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("run")
ap.add_argument("--list", action="store_true")
ap.add_argument("--case", default="")
ap.add_argument("--max-chars", type=int, default=1800)
a = ap.parse_args()
run = pathlib.Path(a.run)
done = set()
jr = run / "judge_results.jsonl"
if jr.exists():
    done = {json.loads(l)["key"] for l in jr.read_text().splitlines() if l.strip()}
reqs = [json.loads(l) for l in (run / "judge_requests.jsonl").read_text().splitlines() if l.strip()]
reqs = [r for r in reqs if r["key"] not in done]
by_conv = collections.OrderedDict()
for r in reqs:
    by_conv.setdefault(r["key"].split("::")[0], []).append(r)
if a.list:
    c = collections.Counter(k.split("__")[0] for k in by_conv)
    print(f"{len(reqs)} pending checks in {len(by_conv)} conversations")
    print(", ".join(f"{k}x{v}" for k, v in c.items()))
else:
    for conv, rs in by_conv.items():
        if a.case and not conv.startswith(a.case + "__"):
            continue
        print(f"\n======== {conv}")
        prev = None
        for line in rs[0]["transcript"].splitlines():
            if line == prev:          # drop exact duplicate blocks (reply repeated as card)
                continue
            prev = line
            print(line if len(line) <= a.max_chars else line[:a.max_chars] + " [...]")
        print("---- checks:")
        for r in rs:
            print(f"  {r['key']}  (at {r['at']})  {r['criterion']}")
