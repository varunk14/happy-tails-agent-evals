"""Append judge verdicts compactly. Used by the in-session judge (see JUDGING.md).

record(run_dir, "A-01", {"A-01.1": ("FFF", "reason for all trials"),
                         "A-01.4": ("PPF", ["t1 reason", "t2 reason", "t3 reason"])})
Verdict string: one letter per trial in trial order, P = PASS, F = FAIL.
"""
import json, pathlib

def record(run_dir, case, spec):
    out = pathlib.Path(run_dir) / "judge_results.jsonl"
    lines = []
    for check, (verdicts, reasons) in spec.items():
        for i, v in enumerate(verdicts, 1):
            reason = reasons[i - 1] if isinstance(reasons, list) else reasons
            lines.append(json.dumps({"key": f"{case}__t{i}::{check}",
                                     "verdict": {"P": "PASS", "F": "FAIL"}[v], "reason": reason}, ensure_ascii=False))
    with out.open("a") as f:
        f.write("\n".join(lines) + "\n")
    return len(lines)
