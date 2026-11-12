"""v2.1 failures by root cause (assigned from the adjudicated reasons, 12 Nov 2026) + counterfactual unlocks."""
import json, collections, sys, itertools
RC = {
 "RC5 No real route to staff (demo-inbox wording; never says staff confirm / phone)":
   "B-01.3 B-03.2 B-06.1 C-02.2 C-02.3 C-04.2 C-06.2 C-08.3 D-02.4 F-01.1 F-02.1 F-02.3 F-03.1 F-03.2 F-04.1 G-03.1 J-03.2 K-01.2 J-02.1 J-02.2 GL-2",
 "RC2 Published website facts missed or hedged": "A-02.2 A-05.2 A-12.1 A-12.3 A-13.1 A-16.1 B-05.1 B-06.2 D-01.1 D-02.1 D-02.3 D-04.1 D-06.1 D-06.3 D-07.1 D-07.2 E-01.1 E-01.2 E-02.1 E-05.1 E-06.1 G-04.1 J-01.3 F-02.2 H-02.3",
 "RC9 Asks 'how many billed days?' instead of pricing (unstable billing basis)": "A-03.1 A-03.2 A-03.3 A-14.3 C-05.3 E-04.3 E-06.3",
 "RC10 Holiday deposit over-applied (new sheet data)": "A-14.2",
 "RC3 Gives in / guesses under pressure": "B-02.4 A-02.3",
 "RC4 Off-task work": "H-01.1",
 "RC11 Vet advice / drops planning": "J-04.1 J-04.2 J-04.3",
 "RC8 Card out of sync with chat": "L-01.4 L-02.3",
 "RC12 Offers to show summary instead of showing it": "G-01.1 G-01.3 G-01.4",
}
C2R = {c: r for r, cs in RC.items() for c in cs.split()}
res = json.load(open(sys.argv[1] + '/results.json'))
fails = [c for c in res['checks'] if c['verdict'] == 'FAIL']
un = sorted({c['check'] for c in fails} - set(C2R))
if un: sys.exit(f'unmapped: {un}')
conv = collections.defaultdict(set); cnt = collections.Counter(); convs = collections.defaultdict(set)
for c in fails:
    r = C2R[c['check']]; k = c['key'].split('__')[0]; conv[k].add(r); cnt[r] += 1; convs[r].add(k)
print('| Root cause | Failed check-trials | Conversations | Unlocked alone |'); print('|---|---|---|---|')
for r in RC: print(f'| {r} | {cnt[r]} | {len(convs[r])} | {sum(1 for k,s in conv.items() if s=={r})} |')
for a, b in itertools.combinations(RC, 2):
    n = sum(1 for s in conv.values() if s <= {a, b})
    if n >= 15: print(f'pair {a[:4]}+{b[:4]}: {n}')
