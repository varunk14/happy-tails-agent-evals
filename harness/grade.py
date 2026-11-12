"""Grade a run: deterministic checks now, judge and inbox checks from their result files.

Usage (from work/):  .venv/bin/python harness/grade.py runs/<version>/<run_id>

Inputs in the run folder:
  transcripts/*.json          from runner.py
  judge_results.jsonl         optional; one {"key","verdict":"PASS"|"FAIL","reason"} per judge check
  outcomes.yaml               optional; manual inbox verification: {"<case>__t<k>::<check_id>": PASS|FAIL}
Outputs:
  judge_requests.jsonl        every judge check still to grade (key, criterion, transcript)
  outcomes_todo.md            inbox checks to verify by hand
  results.json, REPORT.md     per check, per trial, per case (pass^k), per category, KPIs
A check with no result yet is PENDING; a case with any PENDING check is reported as pending, never as passed.
"""
from __future__ import annotations

import collections
import json
import pathlib
import re
import sys

import yaml

WORK = pathlib.Path(__file__).resolve().parent.parent


def load_cases() -> dict[str, dict]:
    out = {}
    for pattern in ("tests/core/*.yaml", "tests/holdout/*.yaml", "tests/smoke/*.yaml"):
        for f in sorted(WORK.glob(pattern)):
            for c in yaml.safe_load(f.read_text()):
                c["_split"] = f.parent.name
                out[c["id"]] = c
    return out


TOOL_PREFIX = "[Tool Result"


def visible(blocks: list[str]) -> list[str]:
    """What the customer actually sees: reply text and card text. askAgent also returns the agent's
    internal tool results ("[Tool Result: name] ..."), which the customer never sees; those are
    kept in the transcript as evidence but are never graded (fixed after the v1 pilot, 11 Nov 2026)."""
    return [b for b in blocks if not b.startswith(TOOL_PREFIX)]


def tools_used(blocks: list[str]) -> list[str]:
    return [re.match(r"\[Tool Result: ([^\]]+)\]", b).group(1) for b in blocks if b.startswith(TOOL_PREFIX)]


def replies_for(at, turns: list[dict]) -> list[tuple[int, str]]:
    """Customer-visible agent output (reply text + card text) for the turns a check applies to."""
    allr = [(t["i"], "\n".join(visible(t.get("blocks", [])))) for t in turns]
    if at in ("all", "any"):
        return allr
    if at == "final":
        return allr[-1:]
    return [r for r in allr if r[0] == at]


def render_transcript(rec: dict) -> str:
    lines = []
    for t in rec["turns"]:
        lines.append(f"CUSTOMER (turn {t['i']}): {t['customer']}")
        for b in visible(t.get("blocks", [])):
            lines.append(f"AGENT (turn {t['i']}): {b}")
    return "\n".join(lines)


def main(run_dir: pathlib.Path) -> None:
    cases = load_cases()
    globals_ = yaml.safe_load((WORK / "tests/global_checks.yaml").read_text())
    judge_results = {}
    jr = run_dir / "judge_results.jsonl"
    if jr.exists():
        for line in jr.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                judge_results[d["key"]] = d
    outcomes = yaml.safe_load((run_dir / "outcomes.yaml").read_text()) if (run_dir / "outcomes.yaml").exists() else {}
    outcomes = outcomes or {}

    rows, judge_reqs, todo = [], [], []
    trials = collections.defaultdict(list)
    for tf in sorted((run_dir / "transcripts").glob("*.json")):
        rec = json.loads(tf.read_text())
        case = cases[rec["case"]]
        tkey = f"{rec['case']}__t{rec['trial']}"
        if rec["status"] == "infra_error":
            trials[rec["case"]].append({"trial": rec["trial"], "status": "INFRA", "checks": []})
            continue
        results = []
        for ch in case["checks"] + [dict(g, at="all") for g in globals_]:
            key = f"{tkey}::{ch['id']}"
            sel = replies_for(ch["at"], rec["turns"])
            if ch["type"] in ("absent", "present"):
                rx = re.compile(ch["pattern"])
                hits = [i for i, txt in sel if rx.search(txt)]
                ok = (not hits) if ch["type"] == "absent" else bool(hits)
                verdict, why = ("PASS" if ok else "FAIL"), (f"matched in turn(s) {hits}" if hits else "no match")
            elif ch["type"] == "judge":
                r = judge_results.get(key)
                verdict, why = (r["verdict"], r.get("reason", "")) if r else ("PENDING", "awaiting judge")
                if not r:
                    judge_reqs.append({"key": key, "case": rec["case"], "check": ch["id"], "at": ch["at"],
                                       "criterion": ch["pass"], "transcript": render_transcript(rec)})
            else:  # outcome
                v = outcomes.get(key)
                verdict, why = (v, "verified in inbox") if v else ("PENDING", "verify in demo inbox")
                if not v:
                    todo.append(f"- [ ] `{key}` (run tag **{rec['run_tag']}**): {ch['pass']}")
            res = {"key": key, "check": ch["id"], "type": ch["type"], "severity": ch["severity"],
                   "verdict": verdict, "why": why, "global": ch["id"].startswith("GL-")}
            results.append(res)
            rows.append(res)
        status = ("FAIL" if any(r["verdict"] == "FAIL" for r in results)
                  else "PENDING" if any(r["verdict"] == "PENDING" for r in results) else "PASS")
        latency = sum(t.get("latency_s", 0) for t in rec["turns"])
        trials[rec["case"]].append({"trial": rec["trial"], "status": status, "checks": results, "latency_s": latency})

    # case level: pass^k = every trial passes
    case_res = {}
    for cid, ts in trials.items():
        st = [t["status"] for t in ts]
        if "FAIL" in st:
            v = "FAIL"
        elif "PENDING" in st or "INFRA" in st:
            v = "PENDING"
        else:
            v = "PASS"
        failed = [r for t in ts for r in t["checks"] if r["verdict"] == "FAIL"]
        worst = next((s for s in ("material", "service", "effort") if any(r["severity"] == s for r in failed)), None)
        case_res[cid] = {"verdict": v, "trials": st, "worst_severity": worst,
                         "per_trial_pass": sum(s == "PASS" for s in st), "n_trials": len(st)}

    (run_dir / "judge_requests.jsonl").write_text("".join(json.dumps(j, ensure_ascii=False) + "\n" for j in judge_reqs))
    (run_dir / "outcomes_todo.md").write_text("# Inbox checks to verify\n\n" + ("\n".join(todo) or "None.") + "\n")
    (run_dir / "results.json").write_text(json.dumps({"cases": case_res, "checks": rows}, indent=2))

    # report
    by_cat = collections.defaultdict(lambda: collections.Counter())
    for cid, r in case_res.items():
        by_cat[(cases[cid]["_split"], cases[cid]["category"])][r["verdict"]] += 1
    graded = [r for r in case_res.values() if r["verdict"] != "PENDING"]
    material = [r for r in graded if r["worst_severity"] == "material"]
    trial_all = [s for r in case_res.values() for s in r["trials"]]
    lines = [f"# Results: {run_dir.name}", "",
             f"Conversations: {len(case_res)} | trials: {len(trial_all)} | pending checks: {len(judge_reqs) + len(todo)}", "",
             "| Split | Category | pass^k | fail | pending |", "|---|---|---|---|---|"]
    for (split, cat), c in sorted(by_cat.items()):
        n = sum(c.values())
        lines.append(f"| {split} | {cat} | {c['PASS']}/{n} | {c['FAIL']} | {c['PENDING']} |")
    if graded:
        lines += ["", "## KPIs (Agentplace names; denominators shown)",
                  f"- **Material error rate**: {len(material)}/{len(graded)} graded conversations had at least one material failure",
                  f"- **Per-trial pass rate**: {trial_all.count('PASS')}/{len(trial_all)} trials"]
    glob_fail = collections.Counter(r["check"] for r in rows if r["global"] and r["verdict"] == "FAIL")
    lines += ["", "## Global checks (failures across all trials)"] + [f"- {k}: {v}" for k, v in sorted(glob_fail.items())] + (["- none"] if not glob_fail else [])
    lines += ["", "## Failing conversations"] + [f"- **{cid}** ({r['worst_severity']}): trials {r['trials']}"
                                                  for cid, r in sorted(case_res.items()) if r["verdict"] == "FAIL"]
    (run_dir / "REPORT.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\njudge checks queued: {len(judge_reqs)} -> {run_dir/'judge_requests.jsonl'}; inbox checks: {len(todo)}")


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]).resolve())
