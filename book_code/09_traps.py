"""Code from 09_traps of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

from scipy import stats

search = pd.read_csv("data/search_redesign.csv")
counts = search["group"].value_counts().sort_index()
print(counts)
chi2, p = stats.chisquare(counts)
share = counts["treatment"] / counts.sum()
print(f"Treatment share: {share:.2%}")
print(f"SRM check: chi-square = {chi2:.1f}, p = {p:.5f}")


hero = pd.read_csv("data/hero_daily.csv", parse_dates=["date"])
days_in = (hero["date"] - hero["date"].min()).dt.days
hero["week"] = days_in // 7 + 1
cols = ["visitors", "clicks"]
weekly = hero.groupby(["week", "group"])[cols].sum()
ctr = (weekly["clicks"] / weekly["visitors"]).unstack()
ctr["lift"] = ctr["treatment"] / ctr["control"] - 1
print(ctr.round(4))


ramp = pd.DataFrame({
    "week":   ["1 (sale)", "1 (sale)", "2", "2"],
    "group":  ["control", "treatment", "control", "treatment"],
    "users":  [18_000, 2_000, 10_000, 10_000],
    "orders": [1_080, 130, 300, 330],
})
ramp["rate"] = ramp["orders"] / ramp["users"]
print(ramp.to_string(index=False))

total = ramp.groupby("group")[["users", "orders"]].sum()
total["rate"] = total["orders"] / total["users"]
print(total.round(4))
