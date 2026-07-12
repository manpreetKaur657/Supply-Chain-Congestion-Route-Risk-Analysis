"""
Data loading and feature engineering for the Supply Chain Congestion &
Route Risk dashboard. Kept separate from app.py so the transformation
logic is testable and doesn't get lost inside UI code.
"""

import pandas as pd
import numpy as np

# Fixed set of hub coordinates -> only 6 origins / 6 destinations in the
# dataset, so this is hand-mapped rather than geocoded on the fly.
CITY_COORDS = {
    "Shanghai, CN":   (31.2304, 121.4737),
    "Los Angeles, US": (34.0522, -118.2437),
    "Tokyo, JP":      (35.6762, 139.6503),
    "Singapore, SG":  (1.3521, 103.8198),
    "Shenzhen, CN":   (22.5431, 114.0579),
    "Rotterdam, NL":  (51.9244, 4.4777),
    "Santos, BR":     (-23.9608, -46.3339),
    "Hamburg, DE":    (53.5511, 9.9937),
    "New York, US":   (40.7128, -74.0060),
    "Mumbai, IN":     (19.0760, 72.8777),
    "Felixstowe, UK": (51.9639, 1.3518),
}


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return engineer_features(df)


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- Dates ---
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b %Y")
    df["Quarter"] = df["Order_Date"].dt.to_period("Q").astype(str)
    df["Year_Month"] = df["Order_Date"].dt.to_period("M").dt.to_timestamp()

    # --- Route identifiers ---
    df["Route"] = df["Origin_City"] + " → " + df["Destination_City"]
    df["Origin_Lat"] = df["Origin_City"].map(lambda c: CITY_COORDS.get(c, (None, None))[0])
    df["Origin_Lon"] = df["Origin_City"].map(lambda c: CITY_COORDS.get(c, (None, None))[1])
    df["Dest_Lat"] = df["Destination_City"].map(lambda c: CITY_COORDS.get(c, (None, None))[0])
    df["Dest_Lon"] = df["Destination_City"].map(lambda c: CITY_COORDS.get(c, (None, None))[1])

    # --- Delay / schedule features ---
    df["Schedule_Buffer_Days"] = df["Scheduled_Lead_Time_Days"] - df["Base_Lead_Time_Days"]
    df["Delay_Pct_of_Planned"] = np.where(
        df["Scheduled_Lead_Time_Days"] > 0,
        (df["Delay_Days"] / df["Scheduled_Lead_Time_Days"]) * 100,
        0,
    )
    df["Is_Late"] = df["Delivery_Status"].eq("Late")

    # --- Disruption flags ---
    df["Is_Disrupted"] = df["Disruption_Event"].notna()
    df["Disruption_Event_Clean"] = df["Disruption_Event"].fillna("No Disruption")

    # --- Cost features ---
    df["Cost_per_Kg"] = df["Shipping_Cost_USD"] / df["Order_Weight_Kg"].replace(0, np.nan)

    # --- Composite route risk score (0-100) ---
    # Geopolitical_Risk_Index is already 0-1, Weather_Severity_Index 0-10,
    # Inflation_Rate_Pct roughly -1 to 8. Min-max normalize the latter two
    # so all three sit on comparable 0-1 scales before weighting.
    geo_norm = df["Geopolitical_Risk_Index"].clip(0, 1)
    weather_norm = (df["Weather_Severity_Index"] / 10).clip(0, 1)
    infl_min, infl_max = df["Inflation_Rate_Pct"].min(), df["Inflation_Rate_Pct"].max()
    infl_norm = ((df["Inflation_Rate_Pct"] - infl_min) / (infl_max - infl_min)).clip(0, 1)

    df["Route_Risk_Score"] = (
        0.45 * geo_norm + 0.35 * weather_norm + 0.20 * infl_norm
    ) * 100

    def risk_band(score):
        if score >= 66:
            return "High"
        elif score >= 40:
            return "Medium"
        return "Low"

    df["Risk_Band"] = df["Route_Risk_Score"].apply(risk_band)

    return df


def kpi_summary(df: pd.DataFrame) -> dict:
    total_orders = len(df)
    on_time_rate = (df["Delivery_Status"].eq("On Time").mean() * 100) if total_orders else 0
    avg_delay = df["Delay_Days"].mean() if total_orders else 0
    p90_delay = df["Delay_Days"].quantile(0.9) if total_orders else 0
    total_cost = df["Shipping_Cost_USD"].sum() if total_orders else 0
    avg_risk = df["Route_Risk_Score"].mean() if total_orders else 0
    disrupted_rate = df["Is_Disrupted"].mean() * 100 if total_orders else 0

    return {
        "total_orders": total_orders,
        "on_time_rate": on_time_rate,
        "avg_delay": avg_delay,
        "p90_delay": p90_delay,
        "total_cost": total_cost,
        "avg_risk": avg_risk,
        "disrupted_rate": disrupted_rate,
    }
