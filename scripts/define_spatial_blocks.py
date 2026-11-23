"""Land-fraction sensitivity and spatial blocks for the 200 m grid (MF-26 proposal).

Inputs (unchanged): derived/male_grid_200m.geojson, derived/grid_evidence.csv,
  derived/grid_evidence_records.csv
Outputs: derived/grid_blocks.csv, plus a printed summary used in reports/mf26_blocks_proposal.md
Positive-only evidence: unknown is never dry. Positive versions:
  a = status reported_flooding; b = a + pumping_only; c = a minus the construction-confounded cells.
Blocks: k-means (random_state=0) on cell centres in EPSG:32643, then repair so that every
location group is in one block and each block is contiguous (queen adjacency, over all 75 cells).
Run from the project root: python scripts/define_spatial_blocks.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

GRID = Path("derived/male_grid_200m.geojson")
EVID = Path("derived/grid_evidence.csv")
RECS = Path("derived/grid_evidence_records.csv")
OUT = Path("derived/grid_blocks.csv")
CUTS = {"lf010": 0.10, "lf025": 0.25, "lf050": 0.50}
LETTERS = "ABCDEFGH"

props = [f["properties"] for f in json.load(open(GRID))["features"]]
g = pd.DataFrame(props)[["cell_id", "easting_min", "northing_min", "land_fraction", "ward"]]
ev = pd.read_csv(EVID).set_index("cell_id")
g = g.sort_values("cell_id").reset_index(drop=True)
g["positive_a"] = g.cell_id.map(ev.status.eq("reported_flooding"))
g["positive_b"] = g.cell_id.map(ev.status.isin(["reported_flooding", "pumping_only"]))
g["positive_c"] = g.positive_a & ~g.cell_id.map(ev.stated_only_construction_confounded.eq("yes"))
for k, v in CUTS.items():
    g["kept_" + k] = g.land_fraction >= v

recs = pd.read_csv(RECS).dropna(subset=["location_group", "cell_id"])
groups = recs.groupby("location_group").cell_id.agg(lambda s: sorted(set(s)))
idx = {c: i for i, c in enumerate(g.cell_id)}
n = len(g)
ij = list(zip(g.easting_min // 200, g.northing_min // 200))
nbr = [[j for j in range(n) if j != i and abs(ij[i][0] - ij[j][0]) <= 1 and abs(ij[i][1] - ij[j][1]) <= 1]
       for i in range(n)]  # queen adjacency


def components(members):
    members, comps = set(members), []
    while members:
        stack, comp = [members.pop()], set()
        comp.add(stack[0])
        while stack:
            for j in nbr[stack.pop()]:
                if j in members:
                    members.discard(j)
                    comp.add(j)
                    stack.append(j)
        comps.append(comp)
    return comps


def repair(lab):
    """Make location groups single-block and blocks contiguous; deterministic."""
    lab = lab.copy()
    for _ in range(50):
        changed = False
        for cells in groups:  # a group goes to the block holding most of its cells (lowest id on ties)
            ii = [idx[c] for c in cells]
            vals, cnt = np.unique(lab[ii], return_counts=True)
            best = vals[cnt.argmax()]
            if any(lab[i] != best for i in ii):
                lab[ii] = best
                changed = True
        for b in np.unique(lab):
            comps = sorted(components(np.where(lab == b)[0]), key=lambda c: (-len(c), min(c)))
            for comp in comps[1:]:  # move stray pieces to the adjacent block they touch most
                touch = [lab[j] for i in comp for j in nbr[i] if lab[j] != b]
                if touch:
                    lab[list(comp)] = max(sorted(set(touch)), key=touch.count)
                    changed = True
        if not changed:
            break
    return lab


def summarise(lab, name):
    d = g.assign(b=lab)
    rows = []
    for b, s in d.groupby("b"):
        rows.append(dict(block=b, cells=len(s), a=int(s.positive_a.sum()), b_=int(s.positive_b.sum()),
                         c=int(s.positive_c.sum()),
                         ext_e=int(s.easting_min.max() - s.easting_min.min() + 200),
                         ext_n=int(s.northing_min.max() - s.northing_min.min() + 200)))
    return pd.DataFrame(rows)


XY = np.column_stack([g.easting_min + 100, g.northing_min + 100])
layouts = {}
for k in (4, 5, 6):
    km = KMeans(k, n_init=10, random_state=0).fit(XY)
    raw = km.labels_
    layouts[f"k{k}"] = repair(raw)
wards = g.ward.astype("category")
layouts["ward"] = repair(wards.cat.codes.to_numpy())

summ = {k: summarise(v, k) for k, v in layouts.items()}
# propose: most blocks holding a version-(a) positive, then closest to 5 blocks
def score(k):
    s = summ[k]
    return (-(s.a > 0).sum(), abs(len(s) - 5))
prop = min(["k4", "k5", "k6"], key=score)

def letters(lab):
    order = {b: LETTERS[i] for i, b in enumerate(sorted(set(lab), key=lambda b: (g.northing_min[lab == b].mean() * -1, g.easting_min[lab == b].mean())))}
    return np.array([order[b] for b in lab])

g["block_id"] = letters(layouts[prop])
g["block_id_ward"] = g.ward
for v in "abc":
    g["positive_" + v] = g["positive_" + v].map({True: "yes", False: "no"})
for k in CUTS:
    g["kept_" + k] = g["kept_" + k].map({True: "yes", False: "no"})
g[["cell_id", "ward", "land_fraction", "kept_lf010", "kept_lf025", "kept_lf050", "block_id",
   "block_id_ward", "positive_a", "positive_b", "positive_c"]].to_csv(OUT, index=False)

# --- Moran's I on the version-(a) indicator, kept cells (lf >= 0.25), queen weights; permutation p, seed 0
def moran(kept_mask, y):
    ids = np.where(kept_mask)[0]
    pos = {i: p for p, i in enumerate(ids)}
    W = np.zeros((len(ids), len(ids)))
    for i in ids:
        for j in nbr[i]:
            if j in pos:
                W[pos[i], pos[j]] = 1
    z = y[ids] - y[ids].mean()
    I = len(ids) / W.sum() * (z @ W @ z) / (z @ z)
    rng = np.random.default_rng(0)
    perm = [len(ids) / W.sum() * ((zp := rng.permutation(z)) @ W @ zp) / (z @ z) for _ in range(999)]
    return I, (1 + sum(p >= I for p in perm)) / 1000, len(ids)

# --- print summary
yv = {v: (g["positive_" + v] == "yes").to_numpy() for v in "abc"}
print("LAND FRACTION (cells kept; positives kept a/b/c)")
for lab, thr in [("none", 0.0)] + [(k, v) for k, v in CUTS.items()]:
    m = (g.land_fraction >= thr).to_numpy()
    print(lab, thr, m.sum(), [int((yv[v] & m).sum()) for v in "abc"])
    drop = g[~m & (yv["b"])]
    for _, r in drop.iterrows():
        print("   drops", r.cell_id, r.land_fraction, r.positive_a, r.positive_b, r.positive_c,
              ev.location_groups[r.cell_id], ev.status[r.cell_id])
for k, s in summ.items():
    print("\n", k, "blocks", len(s), "blocks with a>0:", int((s.a > 0).sum()), "b>0:", int((s.b_ > 0).sum()))
    print(s.to_string(index=False))
print("PROPOSED", prop)
I, p, m = moran(g.land_fraction.ge(0.25).to_numpy(), yv["a"].astype(float))
print("Moran I (a, lf>=0.25, queen)", round(I, 3), "perm p", p, "cells", m)
for r in sorted(g.northing_min.unique())[::-1]:
    print(r, "".join(next((b if g.land_fraction[i] >= .25 else b.lower()) for i, b in [(i, g.block_id[i])] ) if ((g.easting_min == e) & (g.northing_min == r)).any() and (i := g.index[(g.easting_min == e) & (g.northing_min == r)][0]) is not None else " " for e in sorted(g.easting_min.unique())))

# --- self-checks
out = pd.read_csv(OUT)
assert len(out) == 75 and out.cell_id.is_unique and set(out.cell_id) == set(g.cell_id)
assert out.block_id.notna().all()
for cells in groups:
    assert out.set_index("cell_id").block_id[cells].nunique() == 1, cells
lab = out.block_id.to_numpy()
for b in set(lab):
    assert len(components(np.where(lab == b)[0])) == 1, b
for k in CUTS:
    assert (out["kept_" + k] == "yes").sum() == (out.land_fraction >= CUTS[k]).sum()
assert (out.positive_a == "yes").sum() == 12 and (out.positive_b == "yes").sum() == 17 and (out.positive_c == "yes").sum() == 6
print("self-check ok")
