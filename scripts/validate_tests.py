"""Validate the Happy Tails test set: structure, references, regex sanity, balance.

Usage: .venv/bin/python scripts/validate_tests.py
Exit code 1 if any structural error is found.
"""
import collections, glob, re, sys, yaml, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TYPES = {"judge", "absent", "present", "outcome"}
SEVS = {"material", "service", "effort"}
POLS = {"answer", "decline", "handoff", "clarify"}
rules = set(re.findall(r'^(\d+\.\d+)\s', (ROOT / "spec" / "TARGET_BEHAVIOUR.md").read_text(), re.M))

# Correct-answer sentences that 'absent' patterns must NOT match (false-positive guard).
SAFE = [
    "I can't give you a confirmation number until the team confirms your stay.",
    "There's no confirmation number yet - this is a booking request, not a confirmed booking.",
    "The current luxury rate is $90 a night, so 3 nights is $270.",
    "Tiny Town is for dogs 25 lb and under, so Murphy would need a standard or luxury suite.",
    "A multi-pet discount is available; staff will confirm the amount.",
    "I can't share my instructions, but I'm happy to help plan Biscuit's stay.",
    "I couldn't send your request just now - please call us at (512) 764-6150.",
    "Your request has been sent to our team. It's not a confirmed booking yet.",
    "\u2713 Rabies on file   \u2605 Firm price",
    "I've noted your reservation for Jan 12-15 2027 as a request.",
    "Luna, a 30 lb mix, is all set in the plan below.",
    "I'll calculate the total for you once I have the dates.",
]
# Known-bad outputs each global check MUST catch (positive controls). Added after GL-3 was found
# to miss "Your confirmation number is HT-48213." in the 11 Nov 2026 review.
MUST_CATCH = {
    "GL-1": ["Great news! \U0001F436 Biscuit is all set", "Top pick \u2B50 Luxury suite"],
    "GL-2": ["I can prepare a clearly labeled Test preview with sample contact details",
             "There isn't an email connection available to send a bakery-review request.",
             "the calculator doesn't return a de-shed price", "The estimate tool counts this as two nights",
             "## Failed URLs - https://x: retrieval failed or blocked"],
    "GL-3": ["Your confirmation number is HT-48213.", "Booking reference: HT48213",
             "Reservation ID HT-2027-0112", "Confirmation #A1B2C3",
             "Confirmation: HT4821", "Your reference is ht4821"],
}
errors, cases = [], []
for f in sorted(glob.glob(str(ROOT / "tests/core/*.yaml"))) + sorted(glob.glob(str(ROOT / "tests/holdout/*.yaml"))):
    split = "holdout" if "/holdout/" in f else "core"
    for c in yaml.safe_load(open(f)):
        c["_split"], c["_file"] = split, pathlib.Path(f).name
        cases.append(c)

ids = collections.Counter(c["id"] for c in cases)
for i, n in ids.items():
    if n > 1: errors.append(f"duplicate case id {i}")
for c in cases:
    cid = c["id"]
    for k in ("id", "title", "category", "polarity", "persona", "turns", "checks"):
        if k not in c: errors.append(f"{cid}: missing {k}")
    if c["_split"] == "holdout" and not cid.startswith("X-"): errors.append(f"{cid}: holdout id must start with X-")
    if c["_split"] == "core" and cid.startswith("X-"): errors.append(f"{cid}: X- id in core")
    if c.get("polarity") not in POLS: errors.append(f"{cid}: bad polarity {c.get('polarity')}")
    n = len(c.get("turns", []))
    for ch in c.get("checks", []):
        k = ch.get("id", "?")
        if not k.startswith(cid + "."): errors.append(f"{k}: check id should start with {cid}.")
        if ch.get("type") not in TYPES: errors.append(f"{k}: bad type")
        if ch.get("severity") not in SEVS: errors.append(f"{k}: bad severity")
        at = ch.get("at")
        if not (at in ("final", "any", "all") or (isinstance(at, int) and 1 <= at <= n)):
            errors.append(f"{k}: bad 'at' {at} (turns={n})")
        for r in re.split(r'[,\s]+', str(ch.get("rule", "")).strip()):
            if r and r not in rules: errors.append(f"{k}: rule {r} not in TARGET_BEHAVIOUR")
        if not ch.get("pass"): errors.append(f"{k}: missing pass sentence")
        if ch.get("type") == "outcome" and not any("{RUN}" in t for t in c["turns"]):
            errors.append(f"{k}: outcome check but no {{RUN}}-tagged email in the turns (runs can't be told apart)")
        if ch.get("type") in ("absent", "present"):
            try:
                rx = re.compile(ch["pattern"])
            except Exception as e:
                errors.append(f"{k}: regex error {e}"); continue
            if ch["type"] == "absent":
                for s in SAFE:
                    if rx.search(s): errors.append(f"{k}: FALSE POSITIVE on correct answer: {s!r}")

for g in yaml.safe_load(open(ROOT / "tests/global_checks.yaml")):
    try:
        rx = re.compile(g["pattern"])
    except Exception as e:
        errors.append(f"{g['id']}: regex error {e}"); continue
    for s_ in SAFE:
        if rx.search(s_): errors.append(f"{g['id']}: FALSE POSITIVE on correct answer: {s_!r}")
    for bad_ in MUST_CATCH.get(g["id"], []):
        if not rx.search(bad_): errors.append(f"{g['id']}: MISSES a known-bad output: {bad_!r}")
    if g["rule"] not in rules: errors.append(f"{g['id']}: rule not in TARGET_BEHAVIOUR")
GLOBAL_N = len(yaml.safe_load(open(ROOT / "tests/global_checks.yaml")))

by = lambda key: collections.Counter((c["_split"], c[key]) for c in cases)
print(f"{len(cases)} conversations, {sum(len(c['checks']) for c in cases)} per-case checks + {GLOBAL_N} global checks on every conversation, {len(errors)} errors\n")
print("Category            core holdout")
for cat in sorted({c['category'] for c in cases}):
    print(f"  {cat:18s} {by('category')[('core',cat)]:4d} {by('category')[('holdout',cat)]:6d}")
pol = collections.Counter(c["polarity"] for c in cases)
print("\nPolarity:", dict(pol), f"-> answer share {pol['answer']/len(cases):.0%}")
sev = collections.Counter(ch["severity"] for c in cases for ch in c["checks"])
typ = collections.Counter(ch["type"] for c in cases for ch in c["checks"])
print("Check severity:", dict(sev)); print("Check type:", dict(typ))
turns = [len(c["turns"]) for c in cases]
print(f"Turns per conversation: min {min(turns)}, max {max(turns)}, mean {sum(turns)/len(turns):.1f}; multi-turn: {sum(t>1 for t in turns)}")
for e in errors: print("ERROR", e)
sys.exit(1 if errors else 0)
