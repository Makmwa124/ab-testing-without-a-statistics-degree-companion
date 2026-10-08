"""Code from 04_sample_size of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

p = 0.03
for n in [1_000, 10_000, 40_000, 160_000]:
    se = np.sqrt(p * (1 - p) / n)
    print(f"n = {n:>7,}  SE = {se:.3%}")


from scipy.stats import norm

p1 = 0.03
p2 = p1 * 1.10
z_alpha = norm.ppf(1 - 0.05 / 2)
z_power = norm.ppf(0.80)
n = ((z_alpha + z_power) ** 2
     * (p1 * (1 - p1) + p2 * (1 - p2))
     / (p2 - p1) ** 2)
print(f"z_alpha = {z_alpha:.4f}, z_power = {z_power:.4f}")
print(f"Users per group: {np.ceil(n):,.0f}")


def n_per_group(p1, rel_mde, alpha=0.05, power=0.80):
    p2 = p1 * (1 + rel_mde)
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    var = p1 * (1 - p1) + p2 * (1 - p2)
    return int(np.ceil(z ** 2 * var / (p2 - p1) ** 2))

for mde in [0.05, 0.10, 0.15, 0.20, 0.30]:
    n = n_per_group(0.03, mde)
    print(f"MDE {mde:>4.0%}: {n:>9,} per group")


from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

h = proportion_effectsize(0.033, 0.03)
n_sm = NormalIndPower().solve_power(effect_size=h, alpha=0.05,
                                    power=0.80, ratio=1)
print(f"Cohen's h = {h:.4f}")
print(f"Users per group: {np.ceil(n_sm):,.0f}")


def days_needed(n_per_group, daily_users, groups=2):
    return int(np.ceil(n_per_group * groups / daily_users))

for mde in [0.10, 0.15, 0.20]:
    n = n_per_group(0.03, mde)
    print(f"MDE {mde:.0%}: {n:,} per group, "
          f"{days_needed(n, 3_400)} days")


def n_per_group_mean(sd, delta, alpha=0.05, power=0.80):
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return int(np.ceil(2 * z ** 2 * sd ** 2 / delta ** 2))

n_rev = n_per_group_mean(sd=74, delta=7.30 * 0.05)
print(f"Users per group: {n_rev:,}")
print(f"Days at 3,400 a day: {days_needed(n_rev, 3_400):,}")
