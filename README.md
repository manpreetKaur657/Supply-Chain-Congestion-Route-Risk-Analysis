# Supply Chain Congestion and Route Risk Analysis

A Streamlit dashboard for exploring delay, cost, disruption and composite
route-risk patterns across your 6 active shipping lanes.

## Files
- `app.py` — the Streamlit app (run this)
- `data_utils.py` — feature engineering (route risk score, cost/kg, delay %, etc.)
- `theme.py` — shared CSS + color tokens used by every chart library
- `cleaned_supply_chain.csv` — your dataset (must stay in the same folder as `app.py`)
- `requirements.txt` — dependencies

## Run it locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
It'll open at `http://localhost:8501`.

## What's inside
- **Command Deck** — KPI strip, on-time/delay trend, status split, delay distribution
- **Route Risk** — a lane map colored by a composite risk score (geopolitical + weather +
  inflation, blended 45/35/20), risk ranking by route, geo-vs-weather scatter
- **Disruptions** — event breakdown, delay impact by disruption type, which lanes are
  exposed to which disruption, disruption timeline
- **Mitigation** — does re-routing / expedited freight actually cut delay vs standard
  shipping, and what does that cost
- **Cost & Mode** — cost distributions by mode, cost-per-kg by product category, lane economics
- **Data Explorer** — filtered table + CSV download

All filters in the sidebar (date range, route, mode, category, risk band, disrupted-only)
apply across every tab.

## Notes on the composite risk score
`Route_Risk_Score` (0–100) is engineered in `data_utils.py` from three existing
columns: `Geopolitical_Risk_Index` (already 0–1), `Weather_Severity_Index` (0–10,
min-max scaled), and `Inflation_Rate_Pct` (min-max scaled). Weights are 45/35/20 —
tune these in `engineer_features()` if you want geopolitical or weather risk to
dominate differently, or replace the linear blend with something learned from the
data (e.g. weight by each factor's correlation with actual delay).

## Extending it
- Swap the hardcoded `CITY_COORDS` in `data_utils.py` for a geocoding call if you
  add more lanes later
- The risk-score weights are a reasonable starting point, not a fitted model —
  worth validating against `Delay_Days` correlation before presenting it as
  authoritative
