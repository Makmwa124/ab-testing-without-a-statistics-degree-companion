"""Code from 03_randomisation of A/B Testing Without a Statistics Degree.
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

for uid in ["U100000", "U100004", "U100005", "U100000"]:
    print(uid, assign(uid, "delivery-banner"))


users = [f"U{100000 + i}" for i in range(10_000)]
groups = pd.Series([assign(u, "delivery-banner")
                    for u in users], name="banner")
print(groups.value_counts())


groups2 = pd.Series([assign(u, "search-redesign")
                     for u in users], name="search")
print(pd.crosstab(groups, groups2))


banner = pd.read_csv("data/delivery_banner.csv")
mix = pd.crosstab(banner["group"], banner["device"],
                  normalize="index")
print(mix.round(4))


from scipy import stats

counts = banner["group"].value_counts().sort_index()
expected = [counts.sum() / 2] * 2
chi2, p = stats.chisquare(counts, f_exp=expected)
print(counts.to_dict())
print(f"chi-square = {chi2:.2f}, p = {p:.3f}")
