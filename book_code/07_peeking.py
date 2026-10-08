"""Code from 07_peeking of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

from scipy.stats import norm

def p_value(x_a, n_a, x_b, n_b):
    p_pool = (x_a + x_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (x_b / n_b - x_a / n_a) / se
    return 2 * (1 - norm.cdf(np.abs(z)))

rng = np.random.default_rng(2)
days, per_day, rate = 14, 1_700, 0.03
x_a = rng.binomial(per_day, rate, days).cumsum()
x_b = rng.binomial(per_day, rate, days).cumsum()
n = per_day * np.arange(1, days + 1)
for d in range(days):
    p = p_value(x_a[d], n[d], x_b[d], n[d])
    flag = "  <- 'significant'" if p < 0.05 else ""
    print(f"Day {d + 1:>2}: p = {p:.3f}{flag}")


def simulate(n_tests=5_000, days=14, per_day=1_700,
             rate=0.03, seed=1):
    rng = np.random.default_rng(seed)
    x_a = rng.binomial(per_day, rate, (n_tests, days)).cumsum(1)
    x_b = rng.binomial(per_day, rate, (n_tests, days)).cumsum(1)
    n = per_day * np.arange(1, days + 1)
    return p_value(x_a, n, x_b, n)

pvals = simulate()
patient = (pvals[:, -1] < 0.05).mean()
peeking = (pvals < 0.05).any(axis=1).mean()
print(f"Patient false positive rate: {patient:.1%}")
print(f"Daily peeking false positive rate: {peeking:.1%}")


pvals15 = simulate(days=15, seed=3)
looks = [2, 5, 8, 11, 14]          # days 3, 6, 9, 12, 15
naive = (pvals15[:, looks] < 0.05).any(axis=1).mean()
pocock = (pvals15[:, looks] < 0.0158).any(axis=1).mean()
print(f"5 looks at p < 0.05:   {naive:.1%} false positives")
print(f"5 looks at p < 0.0158: {pocock:.1%} false positives")


obf = np.array([0.000005, 0.0013, 0.0084, 0.0226, 0.0413])
hit = (pvals15[:, looks] < obf).any(axis=1).mean()
print(f"O'Brien-Fleming: {hit:.1%} false positives")
