"""Append adjudicated verdicts (full blind re-grade, 12 Nov 2026) to a run's judge_results.jsonl and log them."""
import json, sys, pathlib
run = pathlib.Path(sys.argv[1]); items = json.loads(sys.argv[2])
with open(run/'judge_results.jsonl','a') as f, open('regrade/ADJUDICATIONS.md','a') as log:
    for key, verdict, reason in items:
        f.write(json.dumps({"key":key,"verdict":verdict,"reason":f"{reason} (full re-grade adjudication)"}, ensure_ascii=False)+"\n")
        log.write(f"| {key} | {verdict} | {reason} |\n")
print(len(items),'appended')
