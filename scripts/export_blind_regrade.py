"""Export every judge check of a run as blind packets (transcript + criteria, no verdicts) for an independent re-grade."""
import json, pathlib, sys, collections
sys.path.insert(0, "harness")
import grade
run = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
cases = grade.load_cases()
groups = {"g1": "AB", "g2": "CDE", "g3": "FGH", "g4": "IJKL", "g5": "X"}
buf = collections.defaultdict(list); n = collections.Counter()
for tf in sorted((run / "transcripts").glob("*.json")):
    rec = json.loads(tf.read_text())
    if rec["status"] == "infra_error": continue
    case = cases[rec["case"]]
    js = [c for c in case["checks"] if c["type"] == "judge"]
    if not js: continue
    g = next(k for k, v in groups.items() if rec["case"][0] in v)
    tkey = f"{rec['case']}__t{rec['trial']}"
    lines, prev = [], None
    for l in grade.render_transcript(rec).splitlines():
        if l != prev: lines.append(l)
        prev = l
    buf[g].append(f"\n======== {tkey}  ({case.get('title','')})\n" + "\n".join(lines) + "\n---- checks:\n" +
                  "\n".join(f"  {tkey}::{c['id']}  (at turn {c['at']})  {c['pass']}" for c in js))
    n[g] += len(js)
for g, parts in buf.items():
    (out / f"{g}.txt").write_text("".join(parts)); print(g, n[g], "checks", len(parts), "transcripts")
