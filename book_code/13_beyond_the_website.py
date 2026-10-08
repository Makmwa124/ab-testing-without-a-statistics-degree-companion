"""Code from 13_beyond_the_website of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

rng = np.random.default_rng(13)
n = 60_000
send = rng.random(n) < 0.90
p_order = np.where(send, 0.026, 0.022)   # true rates
ordered = rng.random(n) < p_order

sent = ordered[send].mean()
held = ordered[~send].mean()
print(f"Sent: {send.sum():,} users, {sent:.2%} ordered")
print(f"Held back: {(~send).sum():,} users, {held:.2%} ordered")
print(f"Incremental orders per 1,000 sent: "
      f"{(sent - held) * 1000:.1f}")


from scipy import stats

rng = np.random.default_rng(21)
regions = pd.DataFrame({
    "region": [f"R{i:02d}" for i in range(20)],
    "size": rng.lognormal(5, 0.6, 20).round(),
})
regions["treated"] = rng.permutation([1] * 10 + [0] * 10)
noise = rng.normal(1, 0.06, (20, 2))
regions["before"] = (regions["size"] * noise[:, 0]).round()
uplift = 1 + 0.08 * regions["treated"]
regions["during"] = (regions["size"] * uplift
                     * noise[:, 1]).round()
regions["change"] = regions["during"] / regions["before"] - 1
print(regions.head(4).to_string(index=False))


t = regions[regions["treated"] == 1]
c = regions[regions["treated"] == 0]
naive = stats.ttest_ind(t["during"], c["during"],
                        equal_var=False)
print(f"Levels: treated {t['during'].mean():.0f}, "
      f"control {c['during'].mean():.0f}")
print(f"  p = {naive.pvalue:.2f}")
did = stats.ttest_ind(t["change"], c["change"],
                      equal_var=False)
print(f"Changes: treated {t['change'].mean():+.1%}, "
      f"control {c['change'].mean():+.1%}")
print(f"  p = {did.pvalue:.3f}")
