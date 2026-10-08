"""Code from 08_multiple_comparisons of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

for m in [1, 5, 10, 20, 50]:
    print(f"{m:>2} comparisons: {1 - 0.95 ** m:.0%}")


from statsmodels.stats.proportion import proportions_ztest

rng = np.random.default_rng(3)
n = 20_000
pvals = []
for metric in range(20):
    a = rng.binomial(n, 0.03)
    b = rng.binomial(n, 0.03)
    pvals.append(proportions_ztest([b, a], [n, n])[1])
pvals = np.array(pvals)
print(np.round(np.sort(pvals)[:5], 4))
print(f"'Significant' at 0.05: {(pvals < 0.05).sum()} of 20")


from statsmodels.stats.multitest import multipletests

for method in ["bonferroni", "holm", "fdr_bh"]:
    reject, p_adj, _, _ = multipletests(pvals, alpha=0.05,
                                        method=method)
    print(f"{method:<10} significant: {reject.sum()}  "
          f"smallest adjusted p = {p_adj.min():.3f}")


from scipy.stats import norm

def n_per_group(p1, rel_mde, alpha=0.05, power=0.80):
    p2 = p1 * (1 + rel_mde)
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    var = p1 * (1 - p1) + p2 * (1 - p2)
    return int(np.ceil(z ** 2 * var / (p2 - p1) ** 2))

ab = n_per_group(0.03, 0.10) * 2
abcde = n_per_group(0.03, 0.10, alpha=0.05 / 4) * 5
print(f"A/B, 2 groups:      {ab:>8,} users")
print(f"A/B/C/D/E, 5 groups: {abcde:>7,} users")
print(f"Ratio: {abcde / ab:.1f}x")


banner = pd.read_csv("data/delivery_banner.csv")
first = pd.to_datetime(banner["first_seen"])
banner["weekday"] = first.dt.day_name()

rows = []
for (dev, day), seg in banner.groupby(["device", "weekday"]):
    g = seg.groupby("group")["converted"].agg(["sum", "count"])
    _, p = proportions_ztest(g["sum"][::-1], g["count"][::-1])
    rate = g["sum"] / g["count"]
    lift = rate["treatment"] / rate["control"] - 1
    rows.append({"device": dev, "weekday": day[:3],
                 "users": g["count"].sum(),
                 "lift": lift, "p": p})
segs = pd.DataFrame(rows).sort_values("p")
print(segs.head(6).round(3).to_string(index=False))


_, p_holm, _, _ = multipletests(segs["p"], method="holm")
segs["p_holm"] = p_holm
print(segs.head(3).round(3).to_string(index=False))


def diff_and_se(seg):
    g = seg.groupby("group")["converted"].agg(["mean", "count"])
    pa, na = g.loc["control"]
    pb, nb = g.loc["treatment"]
    se = np.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb)
    return pb - pa, se

is_desk = banner["device"] == "desktop"
d_desk, se_desk = diff_and_se(banner[is_desk])
d_mob, se_mob = diff_and_se(banner[~is_desk])
z = (d_mob - d_desk) / np.sqrt(se_desk ** 2 + se_mob ** 2)
p = 2 * (1 - norm.cdf(abs(z)))
print(f"Desktop: {d_desk:+.3%}  Mobile: {d_mob:+.3%}")
print(f"Difference between segments: p = {p:.2f}")
