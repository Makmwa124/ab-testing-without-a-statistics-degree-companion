"""Code from 05_reading_results of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

from scipy.stats import norm

banner = pd.read_csv("data/delivery_banner.csv")
g = banner.groupby("group")["converted"].agg(["sum", "count"])
x_a, n_a = g.loc["control"]
x_b, n_b = g.loc["treatment"]

p_a, p_b = x_a / n_a, x_b / n_b
p_pool = (x_a + x_b) / (n_a + n_b)
se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
z = (p_b - p_a) / se
p_value = 2 * (1 - norm.cdf(abs(z)))

print(f"Control {p_a:.3%}  Treatment {p_b:.3%}")
print(f"Difference {p_b - p_a:.3%}, SE {se:.4%}")
print(f"z = {z:.3f}, p-value = {p_value:.4f}")


from statsmodels.stats.proportion import proportions_ztest

z_sm, p_sm = proportions_ztest([x_b, x_a], [n_b, n_a])
print(f"z = {z_sm:.3f}, p-value = {p_sm:.4f}")


se_diff = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
diff = p_b - p_a
low, high = diff - 1.96 * se_diff, diff + 1.96 * se_diff
print(f"Difference: {diff:.3%}")
print(f"95% CI: {low:.3%} to {high:.3%}")
print(f"Relative: {low / p_a:.1%} to {high / p_a:.1%}")


from statsmodels.stats.proportion import (
    confint_proportions_2indep)

low_r, high_r = confint_proportions_2indep(
    x_b, n_b, x_a, n_a, compare="ratio")
print(f"Ratio CI: {low_r:.3f} to {high_r:.3f}")


banner["day"] = pd.to_datetime(banner["first_seen"])
week1 = banner[banner["day"] < "2026-03-09"]
g1 = week1.groupby("group")["converted"].agg(["sum", "count"])
z1, p1 = proportions_ztest(g1["sum"][::-1], g1["count"][::-1])
r = g1["sum"] / g1["count"]
print(r.round(4).to_dict())
print(f"p-value after week 1: {p1:.3f}")


rng = np.random.default_rng(42)
draws_a = rng.beta(1 + x_a, 1 + n_a - x_a, 200_000)
draws_b = rng.beta(1 + x_b, 1 + n_b - x_b, 200_000)
prob = (draws_b > draws_a).mean()
print(f"P(treatment beats control) = {prob:.3f}")
