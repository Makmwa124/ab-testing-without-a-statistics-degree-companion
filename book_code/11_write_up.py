"""Code from 11_write_up of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

from scipy.stats import norm

x_a, n_a = 1_046, 30_150     # current provider
x_b, n_b = 1_031, 30_090     # cheaper provider
p_a, p_b = x_a / n_a, x_b / n_b
se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
diff = p_b - p_a
low_90 = diff - norm.ppf(0.95) * se
print(f"Difference: {diff:+.3%}")
print(f"Lower bound (one-sided 95%): {low_90:+.3%}")
print(f"Margin: -0.150%  Non-inferior: {low_90 > -0.0015}")
