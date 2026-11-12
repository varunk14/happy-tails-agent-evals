"""Compare two graded runs: pass^3, per-trial, material error rate, per category, and per-check flips."""
import json, sys, collections
a, b = sys.argv[1], sys.argv[2]
ra, rb = (json.load(open(f'{x}/results.json')) for x in (a, b))
def summ(r):
    c = r['cases']
    return dict(p3=sum(v['verdict']=='PASS' for v in c.values()), pend=sum(v['verdict']=='PENDING' for v in c.values()),
                pt=sum(v['per_trial_pass'] for v in c.values()), n=len(c),
                mat=sum(1 for k in c if any(ch['verdict']=='FAIL' and ch['severity']=='material' for ch in r['checks'] if ch['key'].startswith(k+'__'))))
for name, r in (('A', ra), ('B', rb)): print(name, summ(r))
cat = collections.defaultdict(lambda: [0,0,0,0])
for k in ra['cases']:
    cc = k[0]; cat[cc][0] += ra['cases'][k]['verdict']=='PASS'; cat[cc][1] += rb['cases'][k]['verdict']=='PASS'
    cat[cc][2] += ra['cases'][k]['per_trial_pass']; cat[cc][3] += rb['cases'][k]['per_trial_pass']
print('cat  p3 A->B   trials A->B')
for cc in sorted(cat): print(cc, cat[cc][0], '->', cat[cc][1], '   ', cat[cc][2], '->', cat[cc][3])
fa = collections.Counter(ch['check'] for ch in ra['checks'] if ch['verdict']=='FAIL')
fb = collections.Counter(ch['check'] for ch in rb['checks'] if ch['verdict']=='FAIL')
print('\nNEW or WORSE failures in B (check: A->B):')
for k in sorted(set(fb)):
    if fb[k] > fa.get(k,0): print(f'  {k}: {fa.get(k,0)}->{fb[k]}')
print('\nFIXED (fully) in B:', sorted(k for k in fa if k not in fb))
print('\nStill failing in both:', sorted(k for k in fa if k in fb and fb[k] <= fa[k]))
