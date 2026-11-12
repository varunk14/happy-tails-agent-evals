"""Compare two blind grader sets on a run; print agreement and every disagreement."""
import json, sys
a_dir, b_dir, groups = sys.argv[1], sys.argv[2], sys.argv[3:]
def load(d, g): return {x['key']: x for x in (json.loads(l) for l in open(f'{d}/{g}.jsonl') if l.strip())}
tot = agree = 0
for g in groups:
    A, B = load(a_dir, g), load(b_dir, g)
    assert set(A) == set(B), (g, set(A) ^ set(B))
    dis = [k for k in A if A[k]['verdict'] != B[k]['verdict']]
    tot += len(A); agree += len(A) - len(dis)
    print(f'### {g}: {len(A)-len(dis)}/{len(A)} agree')
    for k in dis:
        print(f'- {k}\n    A {A[k]["verdict"]}: {A[k]["reason"]}\n    B {B[k]["verdict"]}: {B[k]["reason"]}')
print(f'TOTAL {agree}/{tot}')
