# EDA Findings — Sales Forecasting Datathon 2026

Generated from `notebooks/eda_shared.ipynb` | Date: 2026-04-24

---

## Section 1 — Revenue Trend

**Descriptive — What the data shows**
- Annual revenue grew rapidly from 0.74B VND (2012, partial year) to a peak of **2.10B VND in 2016**, then fell sharply to ~1.05–1.17B VND by 2019–2022 — a ~45% decline from peak that has since plateaued.
- The 30-day rolling average confirms two distinct regimes: a growth phase (2012–2016) and a flat-to-declining plateau (2019–2022), with 2017–2018 as a transitional drawdown period.
- Year-on-year growth was +124% (2012→2013), +13% (2013→2014), then turned negative from 2017 onward; the 2019 drop (−40%) was the sharpest single-year decline.

**Diagnostic — Why it might be happening**
- The 2016 peak aligns with Vietnam's e-commerce boom period; the subsequent decline likely reflects market saturation, increased competition, or a strategic pivot away from volume-driven growth.
- The sharp 2019 drop may coincide with macroeconomic headwinds or a product-mix shift — worth cross-referencing with category data (Section 3 shows Streetwear dominance, which could have hit a ceiling).
- The 2019–2022 plateau (~1.0–1.2B) suggests the business found a new equilibrium rather than continuing to decline, possibly supported by loyal repeat customers.

**Prescriptive — What we should do about it**
- **Do not extrapolate the 2012–2016 growth trend into the forecast period.** The test window (2023–2024) should be modeled against the 2019–2022 plateau regime, not the growth era.
- Use a **regime-aware model**: fit separate trend components for pre/post 2018, or weight recent years (2019–2022) more heavily in training.
- Consider a structural break at 2017–2018 as an explicit feature (binary flag) to help tree-based models learn the regime shift.

---

## Section 2 — Seasonality

**Descriptive — What the data shows**
- **Monthly pattern**: revenue peaks in April–June (avg 6.4–6.6M VND/day) and troughs in November–January (avg 2.5–2.6M VND/day) — a 2.5× swing between peak and trough months. February is an anomalous secondary peak (3.5M) driven by Tết.
- **Day-of-week pattern**: Wednesday is the top-performing day (4.7M VND avg) and Saturday is the weakest (3.9M), with a mid-week peak and a consistent weekend dip. The spread across days is modest (~20%).
- **Holiday lift**: Vietnamese public holidays (±3 days window around Tết, Reunification Day, Labour Day, National Day) generate a **+23.7% revenue lift** over non-holiday days.

**Diagnostic — Why it might be happening**
- The April–June peak likely reflects spring/summer consumer spending cycles, back-to-school, and possibly fashion season for the core Streetwear category. Vietnam's rainy season (May–Nov in the south) may suppress Outdoor category sales later in the year.
- The mid-week (Wed/Thu) peak over weekends is counterintuitive for retail — it may reflect B2B-adjacent orders or office delivery preferences that concentrate purchases Tuesday–Thursday.
- Tết (late Jan / early Feb) drives the February secondary bump; the Jan trough reflects pre-Tết consumer caution followed by a surge in the holiday window itself.

**Prescriptive — What we should do about it**
- Encode **month-of-year** and **day-of-week** as features (or Fourier terms for smooth cyclical encoding) — these explain a large portion of variance.
- Build a **Vietnamese holiday feature**: binary flag + days-to/from nearest major holiday, especially capturing the ±3-day Tết window.
- Normalise the seasonal profile by **recent-year revenue level** (2019–2022 average) to avoid the model inheriting the inflated amplitude of the 2014–2016 peak years.

---

## Section 3 — Category Analysis

**Descriptive — What the data shows**
- **Streetwear dominates completely**: 12.56B VND in cumulative order-level revenue (~80% of total), dwarfing Outdoor (2.35B), Casual (0.44B), and GenZ (0.33B). Only 4 categories exist in the catalogue.
- At the segment level, revenue is more evenly distributed: Everyday (32.8%), Balanced (31.3%), Performance (14.6%), and Activewear (12.3%) together account for ~91%, with Premium, All-weather, Trendy, and Standard making up the remainder.
- The GenZ category, despite having a name suggesting growth potential, is the lowest-revenue category at 0.33B — less than 3% of total.

**Diagnostic — Why it might be happening**
- Streetwear's dominance likely reflects the company's core brand identity and its alignment with Vietnam's young, urban demographic (25–34 age cohort is the largest customer segment per Section 6).
- The Everyday + Balanced segment concentration (~64% combined) suggests the business serves middle-market volume buyers rather than premium niches — consistent with the ~1.0–1.2B revenue plateau (volume business, not margin-led).
- GenZ category underperformance may reflect late market entry, weaker brand recognition, or the product failing to differentiate from Streetwear in buyers' minds.

**Prescriptive — What we should do about it**
- Category mix is relatively stable and concentrated, so **category-level features are low-signal for daily Revenue forecasting** — the aggregate is overwhelmingly Streetwear-driven.
- Monitor whether Streetwear share changes in the 2023–2024 test period; any shift toward GenZ or Casual would change the revenue mix and potentially the seasonal pattern.
- For COGS forecasting, the segment margin profile (Performance/Activewear likely have different COGS ratios than Everyday/Balanced) may be a useful derived feature if segment-level cost data is available.

---

## Section 4 — Returns

**Descriptive — What the data shows**
- Return rates are **uniformly low and similar across all categories**: GenZ (3.52%), Outdoor (3.45%), Streetwear (3.38%), Casual (3.26%) — a narrow 0.26 percentage-point range.
- **Wrong size** is overwhelmingly the #1 return reason at 13,967 returns (35% of all returns), followed by defective (8,020 / 20%), not as described (7,035 / 18%), changed mind (6,931 / 17%), and late delivery (3,986 / 10%).
- Total returns in the dataset: 39,939 records across all years, representing a low-single-digit return rate against 714,669 order items.

**Diagnostic — Why it might be happening**
- The dominance of "wrong size" returns (35%) is characteristic of apparel e-commerce globally — customers cannot try on items before purchasing, and sizing standards vary across brands and product lines.
- The near-identical return rates across categories (3.26–3.52%) suggest returns are driven by the shopping channel and product type (clothing), not by category-specific quality differences.
- Late delivery returns at 10% indicate logistics is a meaningful, addressable pain point — not just product-fit issues.

**Prescriptive — What we should do about it**
- Return volume is too small (~3.5% of order items) to materially impact daily Revenue forecasting — returns do not need to be a primary feature in the model.
- However, if returns data is available for early 2023, a **return-rate lag feature** could help refine COGS estimates (returns reduce effective COGS).
- The "wrong size" signal is a product/UX issue; recommend size guide improvements or virtual try-on — outside the forecasting scope but relevant to the MCQ analysis.

---

## Section 5 — Web Traffic vs Revenue

**Descriptive — What the data shows**
- Sessions, unique visitors, and page views are **moderately positively correlated with Revenue** (Pearson r ≈ 0.32 for all three), indicating web traffic volume is a useful but incomplete predictor of daily sales.
- Bounce rate (r = −0.021) and average session duration (r = −0.026) are **near-zero correlated with Revenue** — engagement quality metrics do not predict revenue on a daily basis.
- Web traffic data covers 2013–2022 (3,652 days); the scatter of sessions vs. revenue is coloured by year and shows that the relationship has weakened in recent years as revenue declined while traffic may have remained stable or grown.

**Diagnostic — Why it might be happening**
- The moderate r ~0.32 (not high) suggests that traffic drives revenue but with significant noise — many high-traffic days don't convert, possibly due to promotions, browsing-only behaviour, or mobile sessions that don't complete purchases.
- The near-zero correlation with bounce rate and session duration likely reflects that users who are going to buy already know what they want (low session duration, quick purchase) — so engagement metrics don't discriminate buyers from non-buyers.
- The weakening sessions-revenue relationship over time is consistent with the post-2016 revenue decline despite presumably maintained marketing spend — conversion rate or basket size declined.

**Prescriptive — What we should do about it**
- Include **daily sessions / unique visitors as a lag-1 or same-day feature** in the ML model — the r ~0.32 is weak but non-trivial and free signal.
- Do **not** use bounce rate or avg session duration as features — they add noise without predictive value.
- Web traffic data is available through 2022 only; for the 2023–2024 test period, traffic must be **extrapolated or excluded**. Safest approach: use traffic-derived features only in training, or forecast traffic itself as a secondary model input.

---

## Section 6 — Customer Base

**Descriptive — What the data shows**
- New customer signups grew **monotonically and rapidly** from 957 (2012) to 21,103 (2022) — roughly 22× growth over 10 years, with consistent year-on-year acceleration of ~2,000 new customers per year.
- **Organic search** is the dominant acquisition channel (36,450 customers, ~30%), followed by social media (24,448 / 20%) and paid search (24,285 / 20%); email campaigns (14,674 / 12%) and referral (12,270 / 10%) are secondary.
- The customer base skews **millennial-heavy**: 25–34 is the largest age cohort (29.8%), followed by 35–44 (26.2%) and 45–54 (19.0%). Under-25 (14.0%) and 55+ (11.0%) are the smallest segments.

**Diagnostic — Why it might be happening**
- Monotonic signup growth despite flat/declining revenue (post-2019) implies **revenue per customer is falling** — the business is growing its user base but extracting less value per user, either through smaller basket sizes, lower purchase frequency, or higher churn.
- Organic search dominance suggests strong SEO and brand recognition built up over years, reducing dependence on paid acquisition. Social media's equal weight to paid search may reflect Vietnam's high social media penetration (TikTok, Facebook).
- The 25–44 concentration (56% combined) aligns perfectly with the Streetwear category — this is the core demographic for fashion-forward urban apparel in Vietnam.

**Prescriptive — What we should do about it**
- The rising customer count with flat revenue is a key structural insight: **forecast should not assume revenue grows proportionally with customer growth** — the revenue-per-customer trend is declining and should anchor the 2023–2024 prediction at the 2019–2022 plateau level.
- Customer cohort features (e.g., active customers in trailing 90 days) could be strong predictors if order-date data is joined to customers — worth computing as a feature if time permits.
- The organic search dominance means **no paid-traffic shock risk** in the near term; forecasts don't need to model sudden traffic drops from ad budget cuts.

---

## Summary for Forecasting Pipeline

| Signal | Use in model? | Notes |
|--------|--------------|-------|
| Month-of-year seasonality | Yes | Strongest predictor; use Fourier or one-hot |
| Day-of-week | Yes | 20% swing; Wednesday peak |
| Vietnamese holiday flag | Yes | +23.7% lift; especially Tết window |
| Regime break (post-2018) | Yes | Weight 2019-2022 data more heavily |
| Web sessions (lag-1) | Optional | r≈0.32; only available through 2022 |
| Category/segment features | Low priority | Revenue is ~80% Streetwear; low marginal value |
| Return rate | No | ~3.5%; negligible daily signal |
| Customer count growth | No | Decoupled from revenue post-2019 |
