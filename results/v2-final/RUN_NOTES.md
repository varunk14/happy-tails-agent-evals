# Run notes

- D-07 t1-t3 hit transport timeouts (240 s, TimeoutError on read) during the main run; marked infra_error by the runner.
  Re-run on the same published agent 12 Nov 2026 (runs/v2final_rerun/v2final_rerun_20261112-104232), each reply ~12 s.
  The re-run transcripts replace the infra_error ones (originals kept in infra_replaced/). No other trial re-run.
- Process note: final-run graders A-g1 and B-g1 shared a scratch helper (/tmp/g1grade/add.py, a JSONL appender, no verdict content). Both output files were checked: 192 unique keys each, no duplicate or cross-written lines, so independence held.
