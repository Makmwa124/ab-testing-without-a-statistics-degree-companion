"""Code from appendix_e_answers of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

import hashlib

def assign(user_id, experiment, treatment_share=0.5):
    key = f"{experiment}:{user_id}".encode()
    bucket = int(hashlib.md5(key).hexdigest(), 16) % 100
    if bucket < 100 * (1 - treatment_share):
        return "control"
    return "treatment"

users = [f"U{100000 + i}" for i in range(1_000)]
groups = pd.Series([assign(u, "hero-test") for u in users])
print(groups.value_counts())


from scipy.stats import norm

def n_per_group(p1, rel_mde, alpha=0.05, power=0.80):
    p2 = p1 * (1 + rel_mde)
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    var = p1 * (1 - p1) + p2 * (1 - p2)
    return int(np.ceil(z ** 2 * var / (p2 - p1) ** 2))

for mde in [0.10, 0.05]:
    n = n_per_group(0.05, mde)
    days = int(np.ceil(n * 2 / 2_000))
    weeks = int(np.ceil(days / 7))
    print(f"MDE {mde:.0%}: {n:,} per group, {days} days, "
          f"{weeks} weeks")


from statsmodels.stats.proportion import proportions_ztest

x_a, n_a, x_b, n_b = 600, 20_000, 680, 20_000
z, p = proportions_ztest([x_b, x_a], [n_b, n_a])
p_a, p_b = x_a / n_a, x_b / n_b
se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
d = p_b - p_a
print(f"p = {p:.4f}")
print(f"95% CI {d - 1.96 * se:+.3%} to {d + 1.96 * se:+.3%}")


from scipy import stats

bundle = pd.read_csv("data/bundle_offer.csv")
bundle["cap500"] = bundle["revenue"].clip(upper=500)
is_ctrl = bundle["group"] == "control"
print(bundle.groupby("group")["cap500"].agg(["mean", "std"])
      .round(2))
res = stats.ttest_ind(bundle.loc[~is_ctrl, "cap500"],
                      bundle.loc[is_ctrl, "cap500"],
                      equal_var=False)
print(f"p = {res.pvalue:.3f}")


from scipy.stats import norm

def p_value(x_a, n_a, x_b, n_b):
    p_pool = (x_a + x_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (x_b / n_b - x_a / n_a) / se
    return 2 * (1 - norm.cdf(np.abs(z)))

def simulate(n_tests=5_000, days=14, per_day=1_700,
             rate=0.03, seed=1):
    rng = np.random.default_rng(seed)
    x_a = rng.binomial(per_day, rate, (n_tests, days)).cumsum(1)
    x_b = rng.binomial(per_day, rate, (n_tests, days)).cumsum(1)
    n = per_day * np.arange(1, days + 1)
    return p_value(x_a, n, x_b, n)

pv = simulate()
two_looks = (pv[:, [6, 13]] < 0.05).any(axis=1).mean()
print(f"Two looks: {two_looks:.1%} false positives")


from statsmodels.stats.multitest import multipletests

pvals = [0.004, 0.019, 0.030, 0.20]
reject, p_adj, _, _ = multipletests(pvals, method="holm")
for p, r, a in zip(pvals, reject, p_adj):
    print(f"p = {p:.3f}  adjusted = {a:.3f}  significant: {r}")


from scipy import stats

print(stats.chisquare([50_840, 49_620]).pvalue)
total = 45_310 + 4_690
print(stats.chisquare([45_310, 4_690],
                      f_exp=[total * 0.9, total * 0.1]).pvalue)


ex = pd.read_csv("data/express_checkout.csv")
r = ex["revenue"].corr(ex["orders_prev_90d"])
print(f"r = {r:.3f}, variance cut = {r ** 2:.2%}")


from statsmodels.stats.proportion import proportions_ztest

ex = pd.read_csv("data/express_checkout.csv")
ret = ex[ex["new_customer"] == 0]
g = ret.groupby("group")["converted"].agg(["sum", "count"])
x_a, n_a = g.loc["control"]
x_b, n_b = g.loc["treatment"]
p_a, p_b = x_a / n_a, x_b / n_b
z, p = proportions_ztest([x_b, x_a], [n_b, n_a])
se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
d = p_b - p_a
print(f"Control {p_a:.2%}, treatment {p_b:.2%}, "
      f"lift {p_b / p_a - 1:+.1%}")
print(f"95% CI {d - 1.96 * se:+.2%} to {d + 1.96 * se:+.2%}, "
      f"p = {p:.3f}")
