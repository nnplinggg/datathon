"""
End-to-end forecasting pipeline.
Reads data/sales.csv → writes outputs/submission.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR   = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

TRAIN_FILE  = DATA_DIR / "sales.csv"
TEST_FILE   = DATA_DIR / "sample_submission.csv"
OUT_FILE    = OUTPUT_DIR / "submission.csv"


# ── 1. Load ──────────────────────────────────────────────────────────────────

train = pd.read_csv(TRAIN_FILE, parse_dates=["Date"])
test  = pd.read_csv(TEST_FILE,  parse_dates=["Date"])

print(f"Train: {train.shape}  {train['Date'].min().date()} → {train['Date'].max().date()}")
print(f"Test : {test.shape}   {test['Date'].min().date()} → {test['Date'].max().date()}")


# ── 2. Feature engineering ───────────────────────────────────────────────────

train["year"]  = train["Date"].dt.year
train["month"] = train["Date"].dt.month
train["day"]   = train["Date"].dt.day

annual = train.groupby("year")[["Revenue", "COGS"]].sum()

# Geometric-mean YoY growth (2013–2022)
full = annual.loc[2013:2022]
growth_rev  = (1 + full["Revenue"].pct_change().dropna()).prod() ** (1 / (len(full) - 1))
growth_cogs = (1 + full["COGS"].pct_change().dropna()).prod()    ** (1 / (len(full) - 1))
print(f"YoY growth  Revenue: {growth_rev:.4f}  COGS: {growth_cogs:.4f}")

# Normalised seasonal profile per (month, day)
annual_means = train.groupby("year")[["Revenue", "COGS"]].transform("mean")
train["rev_norm"]  = train["Revenue"] / annual_means["Revenue"]
train["cogs_norm"] = train["COGS"]    / annual_means["COGS"]

seasonal = (
    train.groupby(["month", "day"])[["rev_norm", "cogs_norm"]]
    .mean()
    .reset_index()
)


# ── 3. Predict ───────────────────────────────────────────────────────────────

# Base level: 2022 daily mean
base_rev  = annual.loc[2022, "Revenue"] / 365
base_cogs = annual.loc[2022, "COGS"]    / 365

test = test.copy()
test["month"] = test["Date"].dt.month
test["day"]   = test["Date"].dt.day
test["year"]  = test["Date"].dt.year
test["years_ahead"] = test["year"] - 2022

test = test.merge(seasonal, on=["month", "day"], how="left")
test["rev_norm"]  = test["rev_norm"].fillna(1.0)
test["cogs_norm"] = test["cogs_norm"].fillna(1.0)

test["Revenue"] = (base_rev  * growth_rev**test["years_ahead"]  * test["rev_norm"]).round(2)
test["COGS"]    = (base_cogs * growth_cogs**test["years_ahead"] * test["cogs_norm"]).round(2)


# ── 4. Validate (2021–2022 hold-out) ─────────────────────────────────────────

val = train[train["year"].isin([2021, 2022])].copy()
val = val.merge(seasonal, on=["month", "day"], how="left")
val["rev_norm"]  = val["rev_norm"].fillna(1.0)
val["cogs_norm"] = val["cogs_norm"].fillna(1.0)
val["years_ahead"] = val["year"] - 2022
val["Revenue_pred"] = base_rev  * growth_rev**val["years_ahead"]  * val["rev_norm"]
val["COGS_pred"]    = base_cogs * growth_cogs**val["years_ahead"] * val["cogs_norm"]

mape = lambda a, p: (np.abs(a - p) / a).mean() * 100
print(f"Validation MAPE  Revenue: {mape(val['Revenue'], val['Revenue_pred']):.2f}%")
print(f"Validation MAPE  COGS   : {mape(val['COGS'],    val['COGS_pred']):.2f}%")


# ── 5. Export ─────────────────────────────────────────────────────────────────

submission = test[["Date", "Revenue", "COGS"]].copy()
submission["Date"] = submission["Date"].dt.strftime("%Y-%m-%d")
submission.to_csv(OUT_FILE, index=False)
print(f"Saved {len(submission)} rows → {OUT_FILE}")
