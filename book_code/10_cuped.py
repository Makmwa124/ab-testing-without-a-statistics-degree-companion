"""Code from 10_cuped of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

from scipy import stats

pp = pd.read_csv("data/product_page.csv")
ctrl = pp[pp["group"] == "control"]
trt = pp[pp["group"] == "treatment"]

res = stats.ttest_ind(trt["spend"], ctrl["spend"],
                      equal_var=False)
lift = trt["spend"].mean() / ctrl["spend"].mean() - 1
print(f"Control {ctrl['spend'].mean():.2f}, "
      f"treatment {trt['spend'].mean():.2f}")
print(f"Lift {lift:+.1%}, p = {res.pvalue:.3f}")


print(pp[["pre_spend", "spend"]].describe().round(2))
r = pp["pre_spend"].corr(pp["spend"])
print(f"Correlation between before and during: {r:.2f}")


x, y = pp["pre_spend"], pp["spend"]
theta = np.cov(y, x)[0, 1] / x.var()
pp["spend_cuped"] = y - theta * (x - x.mean())
print(f"theta = {theta:.3f}")

var_cut = 1 - pp["spend_cuped"].var() / y.var()
print(f"Variance reduction: {var_cut:.0%}")

ctrl = pp[pp["group"] == "control"]
trt = pp[pp["group"] == "treatment"]
res_c = stats.ttest_ind(trt["spend_cuped"], ctrl["spend_cuped"],
                        equal_var=False)
ci = res_c.confidence_interval()
diff = trt["spend_cuped"].mean() - ctrl["spend_cuped"].mean()
rel = diff / ctrl["spend"].mean()
print(f"Difference {diff:.2f} ({rel:+.1%})")
print(f"p = {res_c.pvalue:.4f}")
print(f"95% CI {ci.low:.2f} to {ci.high:.2f}")


import statsmodels.formula.api as smf

model = smf.ols("spend ~ C(group) + pre_spend", data=pp).fit()
coef = model.params["C(group)[T.treatment]"]
pval = model.pvalues["C(group)[T.treatment]"]
print(f"Treatment effect {coef:.2f}, p = {pval:.4f}")
