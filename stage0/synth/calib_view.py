"""Print viability-only fields of calibration runs (no emergence metrics, by design)."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(HERE, "results", sys.argv[1] + "__*.json"))):
    r = json.load(open(f))
    s = r["series"]
    pick = [s[i] for i in sorted(set([0, len(s)//4, len(s)//2, 3*len(s)//4, len(s)-1]))]
    row = " | ".join(f"t={p['t_s']:.0f} n={p['n']} E={p.get('energy',0):.2f} cen={p.get('centroid_hz',0):.0f}Hz" for p in pick)
    print(f"{r['condition']:14s} s{r['seed']} births={r['births']} deaths={r['deaths']} {r['elapsed_s']}s :: {row}")
