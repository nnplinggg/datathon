# EDA → Model Features, Business Insights & MCQ Answers

Generated from `eda_findings.md` | Date: 2026-04-24

---

## 1. Features from Non-Sales Tables Worth Adding to the Forecast Model

### High Value — Add Now

| Feature | Source Table | How to Derive |
|---------|-------------|---------------|
| `daily_sessions` (lag-1) | `web_traffic.csv` | Aggregate sessions by date; shift by 1 day |
| `unique_visitors` (lag-1) | `web_traffic.csv` | Same aggregation; correlated with sessions (r ≈ 0.32) |
| `is_holiday` + `days_to_holiday` | Derived (no table) | Vietnamese public holidays + Tết lookup; already coded in S2c cell |

### Medium Value — Worth the Compute

| Feature | Source Table | How to Derive |
|---------|-------------|---------------|
| `active_customers_trailing_90d` | `orders.csv` joined to `customers.csv` | Count distinct customers with an order in prior 90 days |
| `promotion_active` | `promotions.csv` | Binary flag: any active campaign on that date |

### Skip Entirely
Bounce rate, avg session duration, return rate, category mix, customer signup count — all near-zero signal for daily Revenue forecasting.

---

## 2. Top 5 Insights with the Strongest Business Case for Part 2

**1. Two-Regime Revenue Structure (Section 1)**
Revenue fell 45% from its 2016 peak (2.10B VND) and has been flat at ~1.0–1.2B since 2019. Any model trained naively on 2012–2022 will overpredict by treating the growth era as representative. This is the single most consequential finding for forecast accuracy.

**2. Holiday Lift of +23.7% (Section 2)**
A quantified, reproducible seasonal effect that can be directly encoded as a feature. The Tết window alone explains a large chunk of February's anomalous spike. This is concrete, actionable, and easy to defend in a report.

**3. 2.5× Monthly Swing — April–June Peak vs. Nov–Jan Trough (Section 2)**
The seasonality amplitude is large and consistent across years. Month-of-year is likely the single strongest predictor in any ML model. The rainy-season / fashion-cycle explanation gives it a clear business narrative.

**4. Revenue per Customer is Falling Despite 22× Signup Growth (Section 6)**
Customer acquisition is healthy; monetisation is not. More users, flat revenue signals eroding basket size or purchase frequency — a strategic alarm that adds depth to the report beyond just "revenue went down."

**5. Streetwear is 80% of Revenue (Section 3)**
The business is a one-category company in practice. This explains concentration risk and validates anchoring forecasts to Streetwear's cycle rather than modelling four categories separately.

---

## 3. MCQ Questions Directly Answerable from What We Already Ran

These can be answered with exact numbers from the notebook outputs — no additional analysis needed.

| MCQ Topic | Answer |
|-----------|--------|
| Peak revenue year | **2016** at 2.10B VND |
| Largest customer age segment | **25–34** (29.8%) |
| Top acquisition channel | **Organic search** (36,450 customers / ~30%) |
| #1 return reason | **Wrong size** (13,967 returns / 35% of all returns) |
| Return rate by category | All within 3.26–3.52%; Streetwear at 3.38% |
| Highest-revenue category | **Streetwear** at 12.56B VND (~80% of total) |
| Holiday revenue lift | **+23.7%** vs non-holiday days |
| Best day of week by revenue | **Wednesday** (4.7M VND avg) |
| Worst day of week by revenue | **Saturday** (3.9M VND avg) |
| Web traffic correlation with revenue | Sessions r ≈ **0.32**; bounce rate r ≈ **−0.02** |
| Number of product categories | **4** (Streetwear, Outdoor, Casual, GenZ) |
| Year with sharpest revenue drop | **2019** (−40% YoY) |

### Still Needs Analysis
MCQ questions touching **promotions**, **shipment performance**, **inventory**, **geography**, or **payment methods** require additional analysis — those tables were not covered in the shared EDA.
