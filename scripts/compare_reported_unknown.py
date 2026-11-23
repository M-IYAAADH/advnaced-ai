"""MF-30: descriptive comparison of cells with reports vs cells with no report (unknown).
No model is fitted. Positive-only evidence: unknown is never dry. Run from the repo root."""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "derived/mf30"; os.makedirs(OUT, exist_ok=True)
EXC = "G333600_461800"  # MF-26 keep-by-exception (West Park STO)
ATTRS = ["fabdem_mean_m", "fabdem_p10_m", "building_coverage_google075", "worldcover_builtup_share",
         "road_density_vehicular_m_per_km2", "dist_land_centroid_to_coast_m"]
LAB = {"fabdem_mean_m": "FABDEM mean elevation (m, relative)", "fabdem_p10_m": "FABDEM 10th percentile elevation (m, relative)",
       "building_coverage_google075": "Google building coverage (share of land area)",
       "worldcover_builtup_share": "WorldCover built-up share",
       "road_density_vehicular_m_per_km2": "Vehicular road density (m per km2)",
       "dist_land_centroid_to_coast_m": "Distance, land centroid to coast (m)"}
FAB = [a for a in ATTRS if a.startswith("fabdem")]

ev = pd.read_csv("derived/grid_evidence.csv"); at = pd.read_csv("derived/grid_attributes.csv")
bl = pd.read_csv("derived/grid_blocks.csv")
d = ev.merge(at.drop(columns=["ward", "land_fraction"]), on="cell_id").merge(bl[["cell_id", "kept_lf025"]], on="cell_id")
d["main"] = (d.kept_lf025 == "yes") | (d.cell_id == EXC)
conf = d.stated_only_construction_confounded == "yes"; pump = d.routine_pump_site == "yes"
rep = d.status == "reported_flooding"; unk = d.status == "unknown"
V = {  # version -> (reported mask, unknown mask)
    "V1_stated": (rep, unk),
    "V2_stated_plus_pumping": (rep | (d.status == "pumping_only"), unk),
    "V3_stated_excl_confounded": (rep & ~conf, unk & ~conf),
    "V4_V1_excl_routine_pump_sites": (rep & ~pump, unk),
}
SETS = {"main_lf025_plus_exception": d.main, "no_cutoff": pd.Series(True, index=d.index)}

def stats(x):
    return dict(n=len(x), median=x.median(), q25=x.quantile(.25), q75=x.quantile(.75), min=x.min(), max=x.max()) if len(x) else dict(n=0, median=np.nan, q25=np.nan, q75=np.nan, min=np.nan, max=np.nan)

rows = []; dropped = {}
for sn, sm in SETS.items():
    for vn, (r, u) in V.items():
        for a in ATTRS:
            for flt in (["excl_zero_share_gt_0.1", "all_cells"] if a in FAB else ["all_cells"]):
                ok = sm & (d.fabdem_zero_share <= 0.1 if flt.startswith("excl") else True)
                xr, xu = d.loc[ok & r, a].dropna(), d.loc[ok & u, a].dropna()
                sr, su = stats(xr), stats(xu)
                inside = float(((xr >= su["q25"]) & (xr <= su["q75"])).mean()) if len(xr) and len(xu) else np.nan
                row = dict(cell_set=sn, version=vn, attribute=a, fabdem_filter=flt)
                row.update({f"reported_{k}": v for k, v in sr.items()}); row.update({f"unknown_{k}": v for k, v in su.items()})
                row["median_diff_reported_minus_unknown"] = sr["median"] - su["median"]
                row["share_reported_cells_inside_unknown_IQR"] = inside
                rows.append(row)
        if sn.startswith("main"):
            dropped[vn] = (int((sm & r & (d.fabdem_zero_share > .1)).sum()), int((sm & u & (d.fabdem_zero_share > .1)).sum()))
gs = pd.DataFrame(rows); gs.to_csv(f"{OUT}/group_summary.csv", index=False)

# ward table (main set; FABDEM medians exclude zero-share cells)
m = d[d.main]; mf = m[m.fabdem_zero_share <= 0.1]; wr = []
for w, g in m.groupby("ward"):
    row = dict(ward=w, cells_kept=len(g))
    for s in ["reported_flooding", "pumping_only", "designated", "unknown"]: row[f"cells_{s}"] = int((g.status == s).sum())
    row["cells_V1"] = int(V["V1_stated"][0][g.index].sum()); row["cells_V3"] = int(V["V3_stated_excl_confounded"][0][g.index].sum())
    for a in ATTRS: row[f"median_{a}"] = (mf if a in FAB else m).loc[lambda t: t.ward == w, a].median()
    wr.append(row)
wt = pd.DataFrame(wr); wt.to_csv(f"{OUT}/ward_table.csv", index=False)

# figures (main set; FABDEM panels exclude zero-share cells)
GC = {"reported": "#c0392b", "unknown (no report)": "#555555"}
rng = np.random.default_rng(0)
for a in ATTRS:
    base = m if a not in FAB else mf
    fig, axs = plt.subplots(1, 2, figsize=(9, 4.6), sharey=True)
    for ax, vn in zip(axs, ["V1_stated", "V3_stated_excl_confounded"]):
        r, u = V[vn]
        for i, (g, msk) in enumerate([("reported", r), ("unknown (no report)", u)]):
            x = base.loc[base.index.isin(d.index[msk]), a].dropna()
            ax.boxplot(x, positions=[i], widths=.5, showfliers=False)
            ax.scatter(i + rng.uniform(-.15, .15, len(x)), x, s=22, color=GC[g], alpha=.8, zorder=3)
            ax.text(i, 1.01, f"n={len(x)}", transform=ax.get_xaxis_transform(), ha="center", fontsize=9)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["reported", "unknown\n(no report)"])
        ax.set_title("V1: stated reports" if vn == "V1_stated" else "V3: stated, excl. construction-confounded", fontsize=10, pad=18)
    axs[0].set_ylabel(LAB[a])
    fig.suptitle(f"{LAB[a]}: cells with reports vs unknown (no report)\n(each dot = one 200 m cell; 57-cell main set; unknown is not dry)", fontsize=10)
    fig.tight_layout(); fig.savefig(f"{OUT}/strip_{a}.png", dpi=200); plt.close(fig)

fig, ax = plt.subplots(figsize=(7.5, 5.5))
mk = [("unknown", "o", "#aaaaaa", "unknown (no report)"), ("pumping_only", "s", "#e69f00", "pumping only"),
      ("designated", "D", "#009e73", "designated"), ("reported_flooding", "o", "#c0392b", "reported (stated)")]
for s, mm, c, l in mk:
    t = mf[mf.status == s]; ax.scatter(t.dist_land_centroid_to_coast_m, t.fabdem_p10_m, marker=mm, c=c, s=45, label=f"{l} (n={len(t)})", edgecolors="k", linewidths=.3)
t = mf[mf.stated_only_construction_confounded == "yes"]
ax.scatter(t.dist_land_centroid_to_coast_m, t.fabdem_p10_m, marker="o", s=130, facecolors="none", edgecolors="k", linewidths=1.5, label=f"construction-confounded (n={len(t)})")
t = mf[mf.routine_pump_site == "yes"]
ax.scatter(t.dist_land_centroid_to_coast_m, t.fabdem_p10_m, marker="x", s=70, c="b", label=f"routine pump site (n={len(t)})")
ax.set_xlabel("Distance, land centroid to coast (m)"); ax.set_ylabel("FABDEM 10th percentile elevation (m, relative)")
ax.set_title("Cells with reports and unknown (no report) cells: elevation vs distance to coast\n(main set, cells with FABDEM zero share > 0.1 left out; unknown is not dry)", fontsize=10)
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(f"{OUT}/scatter_elev_coast.png", dpi=200); plt.close(fig)

# self-checks
for vn, (r, u) in V.items():
    assert not (r & u).any(), vn
    assert (d.loc[r, "status"] != "unknown").all()
    assert (d.loc[d.main & r, "status"] != "unknown").all() and (d.loc[u, "status"] == "unknown").all()
    for sn, sm in SETS.items():
        for a in ATTRS[2:]:
            g = gs[(gs.cell_set == sn) & (gs.version == vn) & (gs.attribute == a)].iloc[0]
            assert g.reported_n == (sm & r & d[a].notna()).sum() and g.unknown_n == (sm & u & d[a].notna()).sum()
assert not (V["V3_stated_excl_confounded"][0] & conf).any() and not (V["V3_stated_excl_confounded"][1] & conf).any()
assert not (V["V4_V1_excl_routine_pump_sites"][0] & pump).any()
for a in ATTRS: assert os.path.exists(f"{OUT}/strip_{a}.png")
assert os.path.exists(f"{OUT}/scatter_elev_coast.png")

# report
def g(vn, a, f=None, sn="main_lf025_plus_exception"):
    f = f or ("excl_zero_share_gt_0.1" if a in FAB else "all_cells")
    return gs[(gs.cell_set == sn) & (gs.version == vn) & (gs.attribute == a) & (gs.fabdem_filter == f)].iloc[0]
def cnt(vn, sm=d.main): r, u = V[vn]; return int((sm & r).sum()), int((sm & u).sum())
des = d[d.status == "designated"].iloc[0]
L = []
L.append("# MF-30: cells with reports vs cells with no report (unknown)\n")
L.append("**Descriptive only. No model was fitted, scored or ranked.** All numbers come from `scripts/compare_reported_unknown.py` (outputs in `derived/mf30/`).\n")
L.append("## 1. Purpose\nDescribe how cells of the 200 m Malé grid that have a flood report differ in simple terrain and built-environment attributes from cells with no report. Evidence is positive-only: a cell with no report is **unknown**, not dry. Counts are reports, not flood frequency, and nothing here ranks cells or wards.\n")
L.append(f"## 2. Data and cell set\nInputs: `grid_evidence.csv`, `grid_attributes.csv`, `grid_blocks.csv`, `ward_evidence_summary.csv`. Main cell set: land fraction >= 0.25 plus the MF-26 exception cell {EXC} = **{int(d.main.sum())} of {len(d)} cells** (sensitivity: no cutoff, all {len(d)}). FABDEM comparisons leave out cells with exact-zero pixel share > 0.1 (likely the inherited sea mask); this drops "
         + ", ".join(f"{vn.split('_')[0]} {a} reported / {b} unknown" for vn, (a, b) in dropped.items()) + " cells. Results with those cells kept are in `group_summary.csv` (fabdem_filter = all_cells). "
         f"The designated cell ({des.cell_id}, {des.ward}) is kept out of both groups in every version.\n")
L.append("## 3. Method\nFour versions, always unknown as the comparison group:\n- V1 stated flooding vs unknown.\n- V2 stated + pumping-only vs unknown.\n- V3 stated, excluding the 6 construction-confounded cells (RF071 only, issue E5); confounded cells left out of both groups.\n- V4 V1 without the two routine pump-site cells (IGMH, West Park/STO).\n"
         "Per group: n, median, IQR, min, max, difference in medians, and the share of reported cells whose value lies inside the unknown group's IQR. The groups are biased samples (reports cluster at arterials and landmarks), so differences describe these cells only.\n")
L.append("## 4. Key tables (main cell set)\n### Cells per group\n| Version | Reported | Unknown |\n|---|---|---|")
for vn in V: a, b = cnt(vn); L.append(f"| {vn} | {a} | {b} |")
L.append(f"\nNo-cutoff sensitivity: " + "; ".join(f"{vn.split('_')[0]} {cnt(vn, SETS['no_cutoff'])[0]} / {cnt(vn, SETS['no_cutoff'])[1]}" for vn in V) + " (reported / unknown).\n")
L.append("### Medians (reported / unknown), n after FABDEM filter\n| Attribute | V1 | V3 | V4 |\n|---|---|---|---|")
for a in ATTRS:
    c = []
    for vn in ["V1_stated", "V3_stated_excl_confounded", "V4_V1_excl_routine_pump_sites"]:
        x = g(vn, a); c.append(f"{x.reported_median:.3g} / {x.unknown_median:.3g} (n {int(x.reported_n)}/{int(x.unknown_n)})")
    L.append(f"| {a} | " + " | ".join(c) + " |")
L.append("\n### Overlap: share of V1 reported cells inside the unknown IQR\n| Attribute | V1 | V3 | Reported range (V1) | Unknown range |\n|---|---|---|---|---|")
for a in ATTRS:
    x, y = g("V1_stated", a), g("V3_stated_excl_confounded", a)
    L.append(f"| {a} | {x.share_reported_cells_inside_unknown_IQR:.2f} | {y.share_reported_cells_inside_unknown_IQR:.2f} | {x.reported_min:.3g} to {x.reported_max:.3g} | {x.unknown_min:.3g} to {x.unknown_max:.3g} |")
L.append("\n### Wards (main set; not a ranking)\n| Ward | Cells kept | Reported | Pumping only | Designated | Unknown | V1 | V3 |\n|---|---|---|---|---|---|---|---|")
for _, w in wt.iterrows(): L.append(f"| {w.ward} | {w.cells_kept} | {w.cells_reported_flooding} | {w.cells_pumping_only} | {w.cells_designated} | {w.cells_unknown} | {w.cells_V1} | {w.cells_V3} |")
L.append("\nWard medians are in `ward_table.csv`.\n")
x1 = {a: g("V1_stated", a) for a in ATTRS}; x3 = {a: g("V3_stated_excl_confounded", a) for a in ATTRS}
L.append("## 5. What the figures show\n`strip_<attribute>.png` plots each cell as a dot, reported vs unknown (no report), for V1 (left) and V3 (right), with boxes for median and IQR. "
         "`scatter_elev_coast.png` plots FABDEM 10th percentile elevation against distance to coast, with marker shapes for status, rings for confounded cells and crosses for routine pump sites.\n"
         "In words, for V1 the reported cells have median " + "; ".join(f"{a} {x1[a].reported_median:.3g} against {x1[a].unknown_median:.3g}" for a in ATTRS) + ". "
         "For V3 the reported-cell medians are " + "; ".join(f"{a} {x3[a].reported_median:.3g} against {x3[a].unknown_median:.3g}" for a in ATTRS) + ". "
         "Where the share inside the unknown IQR is high (table above) the groups overlap on that attribute; where it is low they separate in these cells.\n")
L.append("## 6. Limits\n- Positive-only evidence: unknown cells include cells that flooded without a report, so differences may be understated or biased.\n- Reporting favours arterials and landmarks, so reported cells are not a random sample.\n- Pump sites: pumping-only and routine pump-site records reflect where pumps are stationed (V2 and V4 show the effect).\n"
         f"- Six cells are confounded: their only stated flooding is RF071 (30 Jul 2026, blamed on pumps not yet commissioned, E5). V3 therefore has {cnt('V3_stated_excl_confounded')[0]} reported cells in the main set ({g('V3_stated_excl_confounded','fabdem_p10_m').reported_n:.0f} with FABDEM), so medians are very unstable.\n"
         "- FABDEM is relative only, not surveyed, with known bias; exact zeros are likely sea mask. WorldCover built-up share is near saturation on land, so it separates little. Building coverage is one source (Google, confidence >= 0.75).\n"
         "- The four OSM wards are not checked against a Council map; ward rows describe small n and are not comparable by size.\n- Differences are descriptive and not tested for any population.\n")
L.append("## 7. For MF-50\nFacts only: see the overlap table for which attributes separate or overlap between the groups, and the V3 and V4 columns for how the picture changes when confounded cells or routine pump sites are removed. Use the MF-50 draft for any modelling decision.\n")
open("reports/mf30_reported_vs_unknown.md", "w").write("\n".join(L))
print("ok", {vn: cnt(vn) for vn in V}, dropped)
