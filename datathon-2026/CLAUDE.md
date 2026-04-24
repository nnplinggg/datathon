# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Competition Task

**Sales Forecasting Datathon 2026** — predict daily `Revenue` and `COGS` for every date from `2023-01-01` through `2024-07-01` (~550 rows). Training data covers 2012–2022 in `data/sales.csv`. Evaluation metric is **MAPE** (Mean Absolute Percentage Error).

Submission format mirrors `data/sample_submission.csv`: three columns — `Date` (YYYY-MM-DD), `Revenue`, `COGS`. Output goes to `outputs/submission.csv`.

## Critical

- NEVER use Revenue/COGS from test period as features. Instant disqualification.
- Revenue peaked 2016 (~2.1B), declined to plateau ~1.0-1.2B in 2019-2022.
- Baseline notebook assumes growth - IT IS WRONG. Do not use it as-is.
- random_state=42 everywhere.

## Data Files

| File | Description |
|------|-------------|
| `data/sales.csv` | Daily Revenue + COGS, 2012–2022 (training target) |
| `data/sample_submission.csv` | Test date range with placeholder predictions |
| `data/orders.csv` / `order_items.csv` | Transaction-level order data |
| `data/customers.csv` | Customer attributes |
| `data/products.csv` | Product catalogue |
| `data/inventory.csv` | Stock levels |
| `data/shipments.csv` | Shipment records |
| `data/payments.csv` | Payment transactions |
| `data/returns.csv` | Return records |
| `data/reviews.csv` | Customer reviews |
| `data/promotions.csv` | Promotion/campaign metadata |
| `data/web_traffic.csv` | Daily web traffic signals |
| `data/geography.csv` | Geographic dimension |

All CSVs are gitignored — do not commit them.

## Team Workflow

| Who | File | Scope |
|-----|------|-------|
| Teammate 1 | `notebooks/mcq.ipynb` | MCQ analysis |
| Teammate 2 | `notebooks/eda.ipynb` | Exploratory data analysis |
| Claude | `src/forecast.py` | End-to-end forecasting pipeline |

## Running the Pipeline

```bash
# Install dependencies (once)
pip install pandas numpy scikit-learn matplotlib

# Run the forecasting pipeline → writes outputs/submission.csv
python datathon-2026/src/forecast.py

# Launch notebooks
jupyter notebook datathon-2026/notebooks/
```

## Forecasting Architecture

`src/forecast.py` is a single-file pipeline with these stages:

1. **Load** — reads `data/sales.csv` (train) and `data/sample_submission.csv` (test dates)
2. **Feature engineering** — calendar features (day-of-year, month, weekday), YoY growth rates, normalised seasonal profile per (month, day)
3. **Model** — baseline uses geometric-mean YoY growth × seasonal profile; extend here with ML models (XGBoost, Prophet, SARIMA)
4. **Evaluate** — MAPE on a held-out validation window (2021–2022)
5. **Export** — writes `Date,Revenue,COGS` to `outputs/submission.csv`

The baseline notebook in `data/baseline.ipynb` documents the original seasonal-average approach and serves as a reference for expected MAPE.
