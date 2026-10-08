"""Code from 02_choosing_metrics of A/B Testing Without a Statistics Degree.
Run from the companion folder so the data/ paths work."""
import sqlite3
import pandas as pd
import numpy as np
pd.set_option('display.width', 60)
pd.set_option('display.max_columns', 10)

bundle = pd.read_csv("data/bundle_offer.csv")
bundle["bought"] = bundle["revenue"] > 0
buyers = bundle[bundle["bought"]]

result = pd.DataFrame({
    "users": bundle.groupby("group").size(),
    "conversion": bundle.groupby("group")["bought"].mean(),
    "avg_order": buyers.groupby("group")["revenue"].mean(),
    "rev_per_user": bundle.groupby("group")["revenue"].mean(),
})
print(result.round(4))


sql = """
SELECT "group",
       COUNT(*)                          AS users,
       ROUND(AVG(converted * 1.0) * 100, 2) AS conv_pct,
       ROUND(AVG(revenue), 2)            AS rev_per_user,
       ROUND(SUM(revenue) * 1.0
             / SUM(converted), 2)        AS avg_order,
       ROUND(AVG(checkout_load_s), 3)    AS load_s
FROM express_checkout
GROUP BY "group";
"""
con = sqlite3.connect("data/larkspur.db")
print(pd.read_sql_query(sql, con).to_string(index=False))
