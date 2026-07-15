"""
Supply Chain Congestion & Route Risk — Command Deck
A Streamlit dashboard for exploring delay, cost, disruption and
composite route-risk patterns across 6 global shipping lanes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from data_utils import load_data, kpi_summary, CITY_COORDS
from theme import CSS, COLORS, RISK_COLOR_MAP, STATUS_COLOR_MAP, style_fig

# ---------------------------------------------------------------- CONFIG
st.set_page_config(
    page_title="Supply Chain Congestion and Route Risk",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS, unsafe_allow_html=True)

sns.set_style("darkgrid", {
    "axes.facecolor": COLORS["panel"],
    "figure.facecolor": COLORS["panel"],
    "grid.color": COLORS["border"],
})
plt.rcParams.update({
    "figure.facecolor": COLORS["panel"],
    "axes.facecolor": COLORS["panel"],
    "axes.edgecolor": COLORS["border"],
    "axes.labelcolor": COLORS["text"],
    "text.color": COLORS["text"],
    "xtick.color": COLORS["text"],
    "ytick.color": COLORS["text"],
    "grid.color": COLORS["border"],
    "font.family": "monospace",
    "axes.grid": True,
    "grid.alpha": 0.4,
    "legend.labelcolor": COLORS["text"],
})

@st.cache_data
def get_data():
    return load_data("cleaned_supply_chain.csv")

df_raw = get_data()

if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True


def _toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open


toggle_col, _ = st.columns([0.08, 0.92])
with toggle_col:
    st.button(
        "☰ Filters" if not st.session_state.sidebar_open else "✕ Hide",
        on_click=_toggle_sidebar,
        key="sidebar_toggle_btn",
        help="Show or hide the filter sidebar",
    )

if st.session_state.sidebar_open:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            margin-left: 0 !important;
            transform: none !important;
            width: 21rem !important;
            min-width: 21rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<style>[data-testid="stSidebar"] { display: none !important; }</style>',
        unsafe_allow_html=True,
    )

date_min, date_max = df_raw["Order_Date"].min().date(), df_raw["Order_Date"].max().date()
routes = sorted(df_raw["Route"].unique())
modes = sorted(df_raw["Transportation_Mode"].unique())
categories = sorted(df_raw["Product_Category"].unique())
risk_bands = ["Low", "Medium", "High"]

if st.session_state.sidebar_open:
    st.sidebar.markdown(
        "<p class='sidebar-title'>Command Filters</p>"
        "<p class='sidebar-subtitle'>Configure the operational view below.</p>",
        unsafe_allow_html=True,
    )
    st.sidebar.checkbox("Disrupted orders only", value=False, key="only_disrupted_cb")
    st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.sidebar.date_input(
        "Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max,
        key="date_range_input",
    )
    st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.sidebar.multiselect("Route (blank = all)", routes, default=[], key="sel_routes")
    st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.sidebar.multiselect("Transport mode", modes, default=[], key="sel_modes")
    st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.sidebar.multiselect("Product category", categories, default=[], key="sel_categories")
    st.sidebar.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.sidebar.multiselect("Risk band", risk_bands, default=[], key="sel_risk")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"<span style='font-family:IBM Plex Mono, monospace; font-size:0.7rem; color:{COLORS['text_dim']};'>"
        f"Dataset: {len(df_raw):,} orders · {date_min} — {date_max}</span>",
        unsafe_allow_html=True,
    )

date_range = st.session_state.get("date_range_input", (date_min, date_max))
sel_routes = st.session_state.get("sel_routes", [])
sel_modes = st.session_state.get("sel_modes", [])
sel_categories = st.session_state.get("sel_categories", [])
sel_risk = st.session_state.get("sel_risk", [])
only_disrupted = st.session_state.get("only_disrupted_cb", False)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_min, date_max

route_filter = df_raw["Route"].isin(sel_routes) if sel_routes else True
mode_filter = df_raw["Transportation_Mode"].isin(sel_modes) if sel_modes else True
category_filter = df_raw["Product_Category"].isin(sel_categories) if sel_categories else True
risk_filter = df_raw["Risk_Band"].isin(sel_risk) if sel_risk else True

mask = (
    (df_raw["Order_Date"].dt.date >= start_date)
    & (df_raw["Order_Date"].dt.date <= end_date)
    & route_filter
    & mode_filter
    & category_filter
    & risk_filter
)
df = df_raw[mask].copy()
if only_disrupted:
    df = df[df["Is_Disrupted"]]

st.markdown(
    f"""
    <div class="manifest-header">
        <div> 
            <p class="manifest-title">Supply Chain Congestion and Route Risk</p>
            <p class="manifest-subtitle">Congestion &amp; route risk monitor · 6 active lanes</p>
        </div>
        <div class="manifest-tag">● LIVE FILTER: {len(df):,} ORDERS</div>
    </div>
    """,
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("No orders match the current filters. Widen a filter in the sidebar.")
    st.stop()

k = kpi_summary(df)


def kpi_card(label, value, sub="", kind=""):
    cls = f"kpi-card {kind}".strip()
    return (f'<div class="{cls}"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>')


on_time_kind = "good" if k["on_time_rate"] >= 85 else ("warn" if k["on_time_rate"] >= 70 else "alert")
risk_kind = "good" if k["avg_risk"] < 40 else ("warn" if k["avg_risk"] < 66 else "alert")

cards_html = "<div class='kpi-row'>" + "".join([
    kpi_card("Total Orders", f"{k['total_orders']:,}", "in current filter"),
    kpi_card("On-Time Rate", f"{k['on_time_rate']:.1f}%", "target ≥ 90%", on_time_kind),
    kpi_card("Avg Delay", f"{k['avg_delay']:.2f} Days", f"P90 = {k['p90_delay']:.0f}d"),
    kpi_card("Total Shipping Cost", f"${k['total_cost']/1e6:.2f}M", "sum of filtered orders"),
    kpi_card("Avg Route Risk Score", f"{k['avg_risk']:.1f}/100", "geo + weather + inflation", risk_kind),
    kpi_card("Disruption Rate", f"{k['disrupted_rate']:.1f}%", "of filtered orders",
              "alert" if k["disrupted_rate"] > 20 else ""),
]) + "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

tab_overview, tab_risk, tab_disrupt, tab_mitig, tab_cost, tab_data = st.tabs(
    ["Command Deck", "Route Risk", "Disruptions", "Mitigation", "Cost & Mode", "Data Explorer"]
)

with tab_overview:
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Trend</p><p class='section-title'>On-Time Rate & Avg Delay Over Time</p>",
                    unsafe_allow_html=True)
        monthly = df.groupby("Year_Month").agg(
            on_time_rate=("Delivery_Status", lambda s: (s == "On Time").mean() * 100),
            avg_delay=("Delay_Days", "mean"),
            orders=("Order_ID", "count"),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly["Year_Month"], y=monthly["on_time_rate"], name="On-Time Rate (%)",
            mode="lines+markers", line=dict(color=COLORS["low"], width=2), yaxis="y1",
        ))
        fig.add_trace(go.Bar(
            x=monthly["Year_Month"], y=monthly["avg_delay"], name="Avg Delay (days)",
            marker_color=COLORS["blue"], opacity=0.5, yaxis="y2",
        ))
        fig.update_layout(
            yaxis=dict(title="On-Time Rate (%)", gridcolor=COLORS["border"]),
            yaxis2=dict(title="Avg Delay (days)", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", y=1.15),
        )
        st.plotly_chart(style_fig(fig, 340), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Status</p><p class='section-title'>Delivery Status Split</p>",
                    unsafe_allow_html=True)
        status_counts = df["Delivery_Status"].value_counts().reset_index()
        status_counts.columns = ["Delivery_Status", "count"]
        fig = px.pie(
            status_counts, names="Delivery_Status", values="count", hole=0.62,
            color="Delivery_Status", color_discrete_map=STATUS_COLOR_MAP,
        )
        fig.update_traces(textfont=dict(family="IBM Plex Mono"), textinfo="percent+label")
        st.plotly_chart(style_fig(fig, 340), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Distribution</p><p class='section-title'>Delay Days Distribution</p>",
                    unsafe_allow_html=True)
        fig = px.histogram(df, x="Delay_Days", nbins=21, color_discrete_sequence=[COLORS["blue"]])
        fig.update_layout(bargap=0.1)
        st.plotly_chart(style_fig(fig, 300), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Volume</p><p class='section-title'>Orders by Product Category</p>",
                    unsafe_allow_html=True)
        cat_counts = df["Product_Category"].value_counts().reset_index()
        cat_counts.columns = ["Product_Category", "count"]
        fig = px.bar(
            cat_counts.sort_values("count"), x="count", y="Product_Category", orientation="h",
            color_discrete_sequence=[COLORS["low"]],
        )
        st.plotly_chart(style_fig(fig, 300), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_risk:
    st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
    st.markdown("<p class='section-eyebrow'>Geography</p><p class='section-title'>Active Lanes by Composite Risk Score</p>",
                unsafe_allow_html=True)

    lane_risk = df.groupby(["Route", "Origin_City", "Destination_City"]).agg(
        risk=("Route_Risk_Score", "mean"), orders=("Order_ID", "count")
    ).reset_index()

    fig = go.Figure()
    for _, row in lane_risk.iterrows():
        o_lat, o_lon = CITY_COORDS[row["Origin_City"]]
        d_lat, d_lon = CITY_COORDS[row["Destination_City"]]
        color = COLORS["high"] if row["risk"] >= 66 else (COLORS["medium"] if row["risk"] >= 40 else COLORS["low"])
        fig.add_trace(go.Scattergeo(
            lat=[o_lat, d_lat], lon=[o_lon, d_lon], mode="lines",
            line=dict(width=2 + row["orders"] / lane_risk["orders"].max() * 4, color=color),
            opacity=0.8, name=row["Route"], showlegend=False,
            hovertext=f"{row['Route']}<br>Risk: {row['risk']:.1f}<br>Orders: {row['orders']}",
            hoverinfo="text",
        ))
    all_cities = pd.concat([
        df[["Origin_City"]].rename(columns={"Origin_City": "city"}),
        df[["Destination_City"]].rename(columns={"Destination_City": "city"}),
    ])["city"].unique()
    fig.add_trace(go.Scattergeo(
        lat=[CITY_COORDS[c][0] for c in all_cities], lon=[CITY_COORDS[c][1] for c in all_cities],
        text=all_cities, mode="markers+text", textposition="top center",
        textfont=dict(size=9, color=COLORS["text_dim"], family="IBM Plex Mono"),
        marker=dict(size=7, color=COLORS["text"], line=dict(width=1, color=COLORS["border"])),
        showlegend=False, hoverinfo="text",
    ))
    fig.update_geos(
        projection_type="natural earth", bgcolor=COLORS["panel"],
        landcolor="#1A2740", oceancolor=COLORS["panel"], showocean=True,
        lakecolor=COLORS["panel"], countrycolor=COLORS["border"], coastlinecolor=COLORS["border"],
    )
    st.plotly_chart(style_fig(fig, 440), use_container_width=True)
    st.markdown(
        "<p class='kpi-sub'> · Line thickness = order volume · Color = risk band "
        "(<span style='color:%s'>low</span> / <span style='color:%s'>medium</span> / "
        "<span style='color:%s'>high</span>)</p>" % (COLORS["low"], COLORS["medium"], COLORS["high"]),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Ranking</p><p class='section-title'>Avg Risk Score by Route</p>",
                    unsafe_allow_html=True)
        lr_sorted = lane_risk.sort_values("risk")
        fig = px.bar(
            lr_sorted, x="risk", y="Route", orientation="h",
            color="risk", color_continuous_scale=[COLORS["low"], COLORS["medium"], COLORS["high"]],
        )
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_fig(fig, 340), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Composition</p><p class='section-title'>Geopolitical vs Weather Risk</p>",
                    unsafe_allow_html=True)
        fig = px.scatter(
            df.sample(min(2000, len(df)), random_state=42),
            x="Geopolitical_Risk_Index", y="Weather_Severity_Index",
            color="Risk_Band", color_discrete_map=RISK_COLOR_MAP,
            opacity=0.55, hover_data=["Route"],
        )
        st.plotly_chart(style_fig(fig, 340), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab_disrupt:
    disrupted_df = df[df["Is_Disrupted"]]
    col1, col2 = st.columns([1, 1.3])

    with col1:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Breakdown</p><p class='section-title'>Disruption Events</p>",
                    unsafe_allow_html=True)
        if disrupted_df.empty:
            st.info("No disruption events in the current filter.")
        else:
            dc = disrupted_df["Disruption_Event"].value_counts().reset_index()
            dc.columns = ["Disruption_Event", "count"]
            fig = px.bar(
                dc.sort_values("count"), x="count", y="Disruption_Event", orientation="h",
                color_discrete_sequence=[COLORS["high"]],
            )
            st.plotly_chart(style_fig(fig, 300), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Impact</p><p class='section-title'>Avg Delay Days by Disruption Type</p>",
                    unsafe_allow_html=True)
        if disrupted_df.empty:
            st.info("No disruption events in the current filter.")
        else:
            imp = df.groupby("Disruption_Event_Clean")["Delay_Days"].mean().reset_index().sort_values("Delay_Days")
            fig = px.bar(
                imp, x="Delay_Days", y="Disruption_Event_Clean", orientation="h",
                color_discrete_sequence=[COLORS["blue"]],
            )
            st.plotly_chart(style_fig(fig, 300), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
    st.markdown("<p class='section-eyebrow'>Exposure</p><p class='section-title'>Which Lanes Are Exposed to Which Disruption</p>",
                unsafe_allow_html=True)
    if disrupted_df.empty:
        st.info("No disruption events in the current filter.")
    else:
        cross = pd.crosstab(disrupted_df["Route"], disrupted_df["Disruption_Event"])
        fig, ax = plt.subplots(figsize=(9, 3.2))
        sns.heatmap(
            cross, annot=True, fmt="d", cmap=sns.color_palette(
                [COLORS["panel"], COLORS["medium"], COLORS["high"]], as_cmap=True
            ), linewidths=0.5, linecolor=COLORS["border"], cbar=False, ax=ax,
            annot_kws={"color": COLORS["text"], "fontsize": 8},
        )
        ax.tick_params(labelsize=8)
        plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
        ax.set_facecolor(COLORS["panel"])
        fig.patch.set_facecolor(COLORS["panel"])
        st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
    st.markdown("<p class='section-eyebrow'>Timeline</p><p class='section-title'>Disruption Events Over Time</p>",
                unsafe_allow_html=True)
    if disrupted_df.empty:
        st.info("No disruption events in the current filter.")
    else:
        monthly_disrupt = disrupted_df.groupby(["Year_Month", "Disruption_Event"]).size().reset_index(name="count")
        fig = px.area(
            monthly_disrupt, x="Year_Month", y="count", color="Disruption_Event",
            color_discrete_sequence=[COLORS["high"], COLORS["medium"], COLORS["blue"]],
        )
        st.plotly_chart(style_fig(fig, 320), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_mitig:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Effectiveness</p><p class='section-title'>Avg Delay by Mitigation Action</p>",
                    unsafe_allow_html=True)
        mit = df.groupby("Mitigation_Action_Taken")["Delay_Days"].mean().reset_index().sort_values("Delay_Days")
        fig = px.bar(
            mit, x="Delay_Days", y="Mitigation_Action_Taken", orientation="h",
            color="Mitigation_Action_Taken",
            color_discrete_sequence=[COLORS["low"], COLORS["medium"], COLORS["high"]],
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, 320), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Trade-off</p><p class='section-title'>Cost vs Delay by Mitigation Action</p>",
                    unsafe_allow_html=True)
        trade = df.groupby("Mitigation_Action_Taken").agg(
            avg_delay=("Delay_Days", "mean"), avg_cost=("Shipping_Cost_USD", "mean"), n=("Order_ID", "count")
        ).reset_index()
        fig = px.scatter(
            trade, x="avg_delay", y="avg_cost", size="n", color="Mitigation_Action_Taken",
            text="Mitigation_Action_Taken",
            color_discrete_sequence=[COLORS["low"], COLORS["medium"], COLORS["high"]],
        )
        fig.update_traces(textposition="top center", textfont=dict(size=9))
        fig.update_layout(showlegend=False, xaxis_title="Avg Delay (days)", yaxis_title="Avg Shipping Cost ($)")
        st.plotly_chart(style_fig(fig, 320), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-eyebrow'>Deep Dive</p><p class='section-title'>"
        "On Disrupted Orders Only: Does the Mitigation Action Actually Cut Delay?</p>",
        unsafe_allow_html=True,
    )
    disrupted_df = df[df["Is_Disrupted"]]
    if disrupted_df.empty:
        st.info("No disruption events in the current filter.")
    else:
        fig, ax = plt.subplots(figsize=(9, 3.5))
        order = disrupted_df.groupby("Mitigation_Action_Taken")["Delay_Days"].median().sort_values().index
        sns.boxplot(
            data=disrupted_df, x="Delay_Days", y="Mitigation_Action_Taken", order=order,
            hue="Mitigation_Action_Taken", legend=False,
            palette=[COLORS["low"], COLORS["medium"], COLORS["high"]], ax=ax,
        )
        ax.set_facecolor(COLORS["panel"])
        fig.patch.set_facecolor(COLORS["panel"])
        ax.tick_params(labelsize=9)
        st.pyplot(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_cost:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Distribution</p><p class='section-title'>Shipping Cost by Mode (log scale)</p>",
                    unsafe_allow_html=True)
        fig = px.box(
            df, x="Transportation_Mode", y="Shipping_Cost_USD", color="Transportation_Mode",
            color_discrete_sequence=[COLORS["blue"], COLORS["medium"]], log_y=True, points=False,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig, 340), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
        st.markdown("<p class='section-eyebrow'>Efficiency</p><p class='section-title'>Cost per Kg by Product Category</p>",
                    unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4.2))
        order = df.groupby("Product_Category")["Cost_per_Kg"].median().sort_values().index
        sns.boxplot(
            data=df, x="Cost_per_Kg", y="Product_Category", order=order,
            color=COLORS["low"], ax=ax, fliersize=2,
        )
        ax.set_facecolor(COLORS["panel"])
        fig.patch.set_facecolor(COLORS["panel"])
        ax.tick_params(labelsize=9)
        st.pyplot(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
    st.markdown("<p class='section-eyebrow'>Lane Economics</p><p class='section-title'>Avg Shipping Cost by Route</p>",
                unsafe_allow_html=True)
    route_cost = df.groupby("Route").agg(
        avg_cost=("Shipping_Cost_USD", "mean"), avg_weight=("Order_Weight_Kg", "mean"), n=("Order_ID", "count")
    ).reset_index()
    fig = px.bar(
        route_cost.sort_values("avg_cost"), x="avg_cost", y="Route", orientation="h",
        color_discrete_sequence=[COLORS["blue"]],
    )
    st.plotly_chart(style_fig(fig, 300), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab_data:
    st.markdown("<div class='chart-panel'>", unsafe_allow_html=True)
    st.markdown("<p class='section-eyebrow'>Manifest</p><p class='section-title'>Filtered Order Records</p>",
                unsafe_allow_html=True)
    display_cols = [
        "Order_ID", "Order_Date", "Route", "Transportation_Mode", "Product_Category",
        "Delivery_Status", "Delay_Days", "Disruption_Event", "Route_Risk_Score", "Risk_Band",
        "Shipping_Cost_USD", "Mitigation_Action_Taken",
    ]
    st.dataframe(df[display_cols].sort_values("Order_Date", ascending=False), use_container_width=True, height=430)
    csv = df[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data as CSV", csv, "filtered_supply_chain.csv", "text/csv")
    st.markdown("</div>", unsafe_allow_html=True)
