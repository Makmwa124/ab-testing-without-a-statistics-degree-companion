"""Code from 12_case_study of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

from scipy import stats
from scipy.stats import norm
from statsmodels.stats.proportion import proportions_ztest

def n_per_group(p1, rel_mde, alpha=0.05, power=0.80):
    p2 = p1 * (1 + rel_mde)
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    var = p1 * (1 - p1) + p2 * (1 - p2)
    return int(np.ceil(z ** 2 * var / (p2 - p1) ** 2))

n = n_per_group(0.035, 0.12)
print(f"{n:,} per group, {n * 2 / 3_100:.1f} days")


ex = pd.read_csv("data/express_checkout.csv",
                 parse_dates=["first_seen"])
print(ex["first_seen"].min().date(), "to",
      ex["first_seen"].max().date())

counts = ex["group"].value_counts().sort_index()
print(counts.to_dict())
print(f"SRM p-value: {stats.chisquare(counts).pvalue:.3f}")


daily = ex.groupby(["first_seen", "group"]).size().unstack()
print(daily.describe().loc[["min", "mean", "max"]].round(0))


print(pd.crosstab(ex["group"], ex["device"],
                  normalize="index").round(3))
pre = ex.groupby("group")[["new_customer", "orders_prev_90d"]]
print(pre.mean().round(3))


g = ex.groupby("group")["converted"].agg(["sum", "count"])
x_a, n_a = g.loc["control"]
x_b, n_b = g.loc["treatment"]
p_a, p_b = x_a / n_a, x_b / n_b

z, p = proportions_ztest([x_b, x_a], [n_b, n_a])
se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
low, high = (p_b - p_a) - 1.96 * se, (p_b - p_a) + 1.96 * se

print(f"Control {p_a:.3%}  Treatment {p_b:.3%}")
print(f"Lift {p_b - p_a:+.3%} ({p_b / p_a - 1:+.1%})")
print(f"p-value {p:.4f}")
print(f"95% CI {low:+.3%} to {high:+.3%}")
print(f"Relative CI {low / p_a:+.1%} to {high / p_a:+.1%}")


ex["week"] = (ex["first_seen"] - ex["first_seen"].min()).dt.days
ex["week"] = ex["week"] // 7 + 1
weekly = ex.groupby(["week", "group"])["converted"].mean()
weekly = weekly.unstack()
weekly["lift"] = weekly["treatment"] / weekly["control"] - 1
print(weekly.round(4))


load = ex.groupby("group")["checkout_load_s"]
print(load.mean().round(3))
ctrl = ex[ex["group"] == "control"]
trt = ex[ex["group"] == "treatment"]
res = stats.ttest_ind(trt["checkout_load_s"],
                      ctrl["checkout_load_s"], equal_var=False)
ci = res.confidence_interval()
print(f"Difference {ci.low:.3f} to {ci.high:.3f} s, "
      f"p = {res.pvalue:.1e}")


buyers = ex[ex["converted"] == 1]
r = buyers.groupby("group")["returned"].agg(["sum", "count"])
r["rate"] = r["sum"] / r["count"]
print(r.round(4))
ra, rb = r.loc["control", "rate"], r.loc["treatment", "rate"]
na_, nb_ = r["count"]
se_r = np.sqrt(ra * (1 - ra) / na_ + rb * (1 - rb) / nb_)
d_r = rb - ra
print(f"Difference {d_r:+.2%}, 95% CI "
      f"{d_r - 1.96 * se_r:+.2%} to {d_r + 1.96 * se_r:+.2%}")


rev = ex.groupby("group")["revenue"].mean()
print(rev.round(3))
res_rev = stats.ttest_ind(trt["revenue"], ctrl["revenue"],
                          equal_var=False)
lift_rev = rev["treatment"] / rev["control"] - 1
print(f"Revenue per user lift {lift_rev:+.1%}, "
      f"p = {res_rev.pvalue:.3f}")
aov = buyers.groupby("group")["revenue"].mean()
print(aov.round(2))


x = ex["orders_prev_90d"]
theta = np.cov(ex["converted"], x)[0, 1] / x.var()
adj = ex["converted"] - theta * (x - x.mean())
cut = 1 - adj.var() / ex["converted"].var()
print(f"Variance reduction: {cut:.1%}")


seg = (ex.groupby(["device", "group"])["converted"]
         .mean().unstack())
seg["lift"] = seg["treatment"] / seg["control"] - 1
print(seg.round(4))


def diff_and_se(d):
    s = d.groupby("group")["converted"].agg(["mean", "count"])
    pa, na = s.loc["control"]
    pb, nb = s.loc["treatment"]
    return pb - pa, np.sqrt(pa*(1-pa)/na + pb*(1-pb)/nb)

d_m, se_m = diff_and_se(ex[ex["device"] == "mobile"])
d_d, se_d = diff_and_se(ex[ex["device"] == "desktop"])
z_int = (d_m - d_d) / np.sqrt(se_m ** 2 + se_d ** 2)
p_int = 2 * (1 - norm.cdf(abs(z_int)))
print(f"Mobile {d_m:+.3%}, desktop {d_d:+.3%}, p = {p_int:.2f}")
