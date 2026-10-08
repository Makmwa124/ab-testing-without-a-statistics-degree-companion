"""Code from 01_what_a_test_tells_you of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

weekly = pd.read_csv("data/weekly_conversion.csv")
print(weekly["conversion_rate"].describe().round(4))


weekly["change"] = weekly["conversion_rate"].diff()
biggest = weekly.loc[weekly["change"].abs().idxmax()]
print(biggest)


banner = pd.read_csv("data/delivery_banner.csv")
print(banner.head())
print(banner.shape)


summary = (banner.groupby("group")["converted"]
                 .agg(users="count", orders="sum", rate="mean"))
print(summary)


c = summary.loc["control", "rate"]
t = summary.loc["treatment", "rate"]
print(f"Absolute difference: {t - c:.4%}")
print(f"Relative lift:       {(t - c) / c:.1%}")


rng = np.random.default_rng(7)
control = banner[banner["group"] == "control"].copy()
for i in range(5):
    half = rng.random(len(control)) < 0.5
    a = control.loc[half, "converted"].mean()
    b = control.loc[~half, "converted"].mean()
    print(f"Split {i+1}: {a:.2%} vs {b:.2%}  gap {b-a:+.2%}")
