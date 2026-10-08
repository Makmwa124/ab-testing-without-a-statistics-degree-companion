"""Code from 06_revenue of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

bundle = pd.read_csv("data/bundle_offer.csv")
print(bundle["revenue"].describe().round(2))
qs = bundle["revenue"].quantile([0.95, 0.99, 0.999])
print(qs.round(2))


print(bundle.nlargest(7, "revenue"))


from scipy import stats

ctrl = bundle.loc[bundle["group"] == "control", "revenue"]
trt = bundle.loc[bundle["group"] == "treatment", "revenue"]

res = stats.ttest_ind(trt, ctrl, equal_var=False)
diff = trt.mean() - ctrl.mean()
ci = res.confidence_interval(confidence_level=0.95)
print(f"Control {ctrl.mean():.2f}, treatment {trt.mean():.2f}")
print(f"Difference {diff:.2f} ({diff / ctrl.mean():+.1%})")
print(f"95% CI {ci.low:.2f} to {ci.high:.2f}")
print(f"p-value {res.pvalue:.3f}")


CAP = 1_000
bundle["revenue_capped"] = bundle["revenue"].clip(upper=CAP)

capped = bundle.groupby("group")["revenue_capped"]
print(capped.agg(["mean", "std"]).round(2))

is_ctrl = bundle["group"] == "control"
c_cap = bundle.loc[is_ctrl, "revenue_capped"]
t_cap = bundle.loc[~is_ctrl, "revenue_capped"]
res_c = stats.ttest_ind(t_cap, c_cap, equal_var=False)
ci_c = res_c.confidence_interval()
lift = t_cap.mean() / c_cap.mean() - 1
print(f"Lift {lift:+.1%}, 95% CI {ci_c.low:.2f} to "
      f"{ci_c.high:.2f}, p = {res_c.pvalue:.3f}")


rng = np.random.default_rng(11)
c_arr, t_arr = c_cap.to_numpy(), t_cap.to_numpy()
diffs = np.empty(2_000)
for i in range(2_000):
    c_s = rng.choice(c_arr, size=len(c_arr), replace=True)
    t_s = rng.choice(t_arr, size=len(t_arr), replace=True)
    diffs[i] = t_s.mean() - c_s.mean()
low, high = np.percentile(diffs, [2.5, 97.5])
print(f"Bootstrap 95% CI: {low:.2f} to {high:.2f}")
