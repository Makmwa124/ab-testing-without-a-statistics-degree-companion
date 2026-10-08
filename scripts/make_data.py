"""Generate the fictional Larkspur Outdoor experiment datasets (seeded)."""
import numpy as np, pandas as pd, hashlib, os
SEED1=int(os.environ.get("S1",4101));SEED3=int(os.environ.get("S3",4203));SEED6=int(os.environ.get("S6",4304))
from pathlib import Path
out = Path("data"); out.mkdir(parents=True, exist_ok=True)
start = pd.Timestamp("2026-03-02")  # a Monday

# 1. Delivery banner test (conversion), 14 days
rng = np.random.default_rng(SEED1)
n = 48_230
group = np.where(rng.random(n) < 0.5, "control", "treatment")
device = np.where(rng.random(n) < 0.62, "mobile", "desktop")
day = rng.integers(0, 14, n)
base = np.where(device == "mobile", 0.026, 0.040)
lift = np.where(group == "treatment", 1.12, 1.0)
conv = rng.random(n) < base * lift
df = pd.DataFrame({
    "user_id": [f"U{100000+i}" for i in range(n)],
    "first_seen": (start + pd.to_timedelta(day, "D")).strftime("%Y-%m-%d"),
    "group": group, "device": device, "converted": conv.astype(int)})
df.to_csv(out / "delivery_banner.csv", index=False)

# 2. Bundle offer test: revenue per visitor (skewed)
rng = np.random.default_rng(4102)
n = 30_000
group = np.where(rng.random(n) < 0.5, "control", "treatment")
p_buy = np.where(group == "treatment", 0.047, 0.045)
buy = rng.random(n) < p_buy
mu = np.where(group == "treatment", np.log(118), np.log(112))
val = np.where(buy, np.round(np.exp(rng.normal(mu, 0.75)), 2), 0.0)
# a few very big orders (team kits)
big = rng.choice(np.flatnonzero(buy), 6, replace=False)
val[big] = np.round(rng.uniform(2500, 6200, 6), 2)
pd.DataFrame({"user_id": [f"B{200000+i}" for i in range(n)], "group": group,
              "revenue": val}).to_csv(out / "bundle_offer.csv", index=False)

# 3. Product page test with pre-period spend (CUPED)
rng = np.random.default_rng(SEED3)
n = 20_000
group = np.where(rng.random(n) < 0.5, "control", "treatment")
loyal = rng.gamma(0.6, 60, n)                       # underlying spend propensity
pre = np.round(np.maximum(0, loyal * rng.lognormal(0, 0.35, n) - 8), 2)
effect = np.where(group == "treatment", 1.025, 1.0)
during = np.round(np.maximum(0, loyal * effect * rng.lognormal(0, 0.35, n) - 8), 2)
pd.DataFrame({"user_id": [f"P{300000+i}" for i in range(n)], "group": group,
              "pre_spend": pre, "spend": during}).to_csv(out / "product_page.csv", index=False)

# 4. Search redesign test with a sample ratio mismatch (bot filter dropped treatment users)
rng = np.random.default_rng(4104)
n = 41_000
group = np.where(rng.random(n) < 0.5, "control", "treatment")
keep = ~((group == "treatment") & (rng.random(n) < 0.045))
group = group[keep]; n2 = len(group)
conv = rng.random(n2) < np.where(group == "treatment", 0.052, 0.049)
pd.DataFrame({"user_id": [f"S{400000+i}" for i in range(n2)], "group": group,
              "converted": conv.astype(int)}).to_csv(out / "search_redesign.csv", index=False)

# 5. Homepage hero test with novelty effect: daily data
rng = np.random.default_rng(4105)
rows = []
for d in range(28):
    total = int(rng.normal(3000, 200))
    split = rng.binomial(total, 0.5)
    for g, visitors in [("control", split), ("treatment", total - split)]:
        ctr = 0.080 if g == "control" else 0.080 * (1 + 0.30 * np.exp(-d / 5) + 0.02)
        clicks = rng.binomial(visitors, ctr)
        rows.append({"date": (start + pd.Timedelta(days=63 + d)).strftime("%Y-%m-%d"),
                     "group": g, "visitors": visitors, "clicks": clicks})
pd.DataFrame(rows).to_csv(out / "hero_daily.csv", index=False)

# 6. Express checkout case study (Chapter 12)
rng = np.random.default_rng(SEED6)
n = 64_400
group = np.where(rng.random(n) < 0.5, "control", "treatment")
device = rng.choice(["mobile", "desktop", "tablet"], n, p=[0.60, 0.33, 0.07])
day = rng.integers(0, 21, n)
new_cust = rng.random(n) < 0.55
pre_orders = np.where(new_cust, 0, rng.poisson(1.6, n))
base = np.where(device == "mobile", 0.030, np.where(device == "desktop", 0.044, 0.035))
base = base * np.where(new_cust, 0.85, 1.0) * (1 + 0.12 * np.minimum(pre_orders, 5))
uplift = np.where((group == "treatment") & (device == "mobile"), 1.14,
         np.where(group == "treatment", 1.03, 1.0))
conv = rng.random(n) < base * uplift
aov = np.exp(rng.normal(np.log(128), 0.55, n))
revenue = np.where(conv, np.round(aov, 2), 0.0)
load = np.round(rng.gamma(9, 0.21, n) + np.where(group == "treatment", 0.05, 0), 2)
returned = np.where(conv, (rng.random(n) < np.where(group == "treatment", 0.081, 0.078)).astype(int), 0)
pd.DataFrame({"user_id": [f"E{500000+i}" for i in range(n)],
              "first_seen": (start + pd.Timedelta(days=35) + pd.to_timedelta(day, "D")).strftime("%Y-%m-%d"),
              "group": group, "device": device, "new_customer": new_cust.astype(int),
              "orders_prev_90d": pre_orders, "converted": conv.astype(int),
              "revenue": revenue, "returned": returned,
              "checkout_load_s": load}).to_csv(out / "express_checkout.csv", index=False)

# 7. Weekly sales history (why before/after fails)
rng = np.random.default_rng(4107)
wk = pd.date_range("2025-07-07", periods=26, freq="W-MON")
seas = 1 + 0.25 * np.sin((np.arange(26) - 4) / 26 * 2 * np.pi)
conv = np.round(0.031 * seas * rng.normal(1, 0.06, 26), 4)
pd.DataFrame({"week_starting": wk.strftime("%Y-%m-%d"), "visitors": rng.integers(21000, 26000, 26),
              "conversion_rate": conv}).to_csv(out / "weekly_conversion.csv", index=False)
print("done")

import sqlite3
con = sqlite3.connect(out / "larkspur.db")
for t in ["delivery_banner", "express_checkout"]:
    pd.read_csv(out / f"{t}.csv").to_sql(t, con, index=False, if_exists="replace")
con.close()
