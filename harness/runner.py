"""Run frozen test conversations against a published agent and save verbatim transcripts.

Usage (from work/):
  .venv/bin/python harness/runner.py --url https://<id>.run.agentplace.io --version v1 \
      [--set core|holdout|all|smoke] [--cases A-01,B-02] [--trials 3] [--concurrency 3]

Each (case, trial) is its own conversation with a fresh sessionId. Customer turns are sent in order,
exactly as written; {RUN} in a turn is replaced with a per-trial tag so inbox outcome checks can tell
runs apart. If any turn fails at the transport level, the whole trial is marked 'infra_error' and is
NOT retried mid-conversation (a retry could double-send a turn); re-run it with --cases.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import pathlib
import sys
import uuid

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from mcp_client import AgentMCP, MCPError  # noqa: E402

WORK = pathlib.Path(__file__).resolve().parent.parent
SETS = {"core": ["tests/core/*.yaml"], "holdout": ["tests/holdout/*.yaml"],
        "all": ["tests/core/*.yaml", "tests/holdout/*.yaml"], "smoke": ["tests/smoke/*.yaml"]}
FROZEN = ["tests/core/*.yaml", "tests/holdout/holdout.yaml", "tests/global_checks.yaml",
          "tests/JUDGE_CONTEXT.md", "TARGET_BEHAVIOUR.md"]


def load_cases(set_name: str, only: set[str] | None) -> list[dict]:
    cases = []
    for pattern in SETS[set_name]:
        for f in sorted(WORK.glob(pattern)):
            cases += yaml.safe_load(f.read_text())
    return [c for c in cases if not only or c["id"] in only]


def fingerprints() -> dict:
    out = {}
    for pattern in FROZEN:
        for f in sorted(WORK.glob(pattern)):
            out[str(f.relative_to(WORK))] = hashlib.sha256(f.read_bytes()).hexdigest()
    return out


def run_conversation(url: str, case: dict, trial: int, run_id: str, out_dir: pathlib.Path) -> dict:
    tag = f"{run_id.split('_')[0]}t{trial}{uuid.uuid4().hex[:4]}"
    conv_id = f"{run_id}-{case['id']}-t{trial}-{uuid.uuid4().hex[:6]}"
    rec = {"case": case["id"], "trial": trial, "conversation_id": conv_id, "run_tag": tag,
           "started": dt.datetime.now(dt.timezone.utc).isoformat(), "turns": [], "status": "ok"}
    client = AgentMCP(url)
    try:
        client.connect()
        for i, turn in enumerate(case["turns"], 1):
            msg = turn.replace("{RUN}", tag)
            r = client.ask(msg, conv_id)
            rec["turns"].append({"i": i, "customer": msg, **r})
            if r["is_error"]:
                rec["status"] = "agent_error"
    except (MCPError, OSError, TimeoutError) as e:
        rec["status"] = "infra_error"
        rec["error"] = f"{type(e).__name__}: {e}"
    rec["finished"] = dt.datetime.now(dt.timezone.utc).isoformat()
    (out_dir / f"{case['id']}__t{trial}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--set", default="core", choices=SETS)
    ap.add_argument("--cases", default="")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=3)
    a = ap.parse_args()

    only = {x.strip() for x in a.cases.split(",") if x.strip()} or None
    cases = load_cases(a.set, only)
    run_id = f"{a.version}_{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out_dir = WORK / "runs" / a.version / run_id / "transcripts"
    out_dir.mkdir(parents=True, exist_ok=True)

    info_client = AgentMCP(a.url)
    info_client.connect()
    meta = {"run_id": run_id, "version": a.version, "url": a.url, "set": a.set, "trials": a.trials,
            "cases": [c["id"] for c in cases], "agent_info": info_client.agent_info()["text"],
            "test_fingerprints": fingerprints(), "started": dt.datetime.now(dt.timezone.utc).isoformat()}
    (out_dir.parent / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    jobs = [(c, t) for c in cases for t in range(1, a.trials + 1)]
    print(f"{run_id}: {len(cases)} cases x {a.trials} trials = {len(jobs)} conversations, concurrency {a.concurrency}")
    done = 0
    with cf.ThreadPoolExecutor(max_workers=a.concurrency) as pool:
        futs = {pool.submit(run_conversation, a.url, c, t, run_id, out_dir): (c["id"], t) for c, t in jobs}
        for fut in cf.as_completed(futs):
            rec = fut.result()
            done += 1
            lat = sum(t.get("latency_s", 0) for t in rec["turns"])
            print(f"[{done}/{len(jobs)}] {rec['case']} t{rec['trial']} {rec['status']} ({len(rec['turns'])} turns, {lat:.0f}s)")
    meta["finished"] = dt.datetime.now(dt.timezone.utc).isoformat()
    (out_dir.parent / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
    print("transcripts:", out_dir)


if __name__ == "__main__":
    main()
