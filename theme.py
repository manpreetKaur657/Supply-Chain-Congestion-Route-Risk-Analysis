"""
Custom CSS for the Supply Chain Risk Command Deck.

Design direction: a night-shift port control-room, not a generic SaaS
dashboard. Deep navy background, steel-blue panels, hairline borders,
monospace figures (manifest/tracking-number feel), and a three-color
signal system (teal = clear, amber = watch, flare-orange = high risk)
that echoes real port/ops status lights rather than a decorative gradient.
"""

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #0A1220;
    --panel: #121D33;
    --panel-alt: #16233D;
    --border: #24344F;
    --text: #E8EDF5;
    --text-dim: #8296B8;
    --accent-high: #FF5A3C;
    --accent-med: #F0B429;
    --accent-low: #35D0B8;
    --accent-blue: #5B8DEF;
}

/* Base app */
.stApp {
    background: linear-gradient(180deg, #0A1220 0%, #0C1626 100%);
    color: var(--text);
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
#MainMenu, footer, header {visibility: hidden;}

/* Headings use the display face */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.01em;
}

/* Sidebar = "control panel" */
section[data-testid="stSidebar"] {
    background: #0D1830;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-dim);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Manifest header strip */
.manifest-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid var(--border);
    padding-bottom: 14px;
    margin-bottom: 22px;
}
.manifest-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--text);
    margin: 0;
}
.manifest-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-dim);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 4px;
}
.manifest-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent-low);
    border: 1px solid var(--accent-low);
    padding: 4px 10px;
    border-radius: 3px;
    letter-spacing: 0.05em;
}

/* KPI cards */
.kpi-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: wrap; }
.kpi-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-blue);
    border-radius: 5px;
    padding: 14px 18px;
    flex: 1;
    min-width: 150px;
}
.kpi-card.alert { border-left-color: var(--accent-high); }
.kpi-card.warn { border-left-color: var(--accent-med); }
.kpi-card.good { border-left-color: var(--accent-low); }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.66rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-dim);
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.65rem;
    font-weight: 600;
    color: var(--text);
}
.kpi-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    margin-top: 2px;
}

/* Section eyebrow labels */
.section-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent-blue);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 2px;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    margin-top: 0;
    margin-bottom: 14px;
}

/* Risk badges */
.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    padding: 3px 9px;
    border-radius: 3px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.risk-badge .dot { width: 7px; height: 7px; border-radius: 50%; }
.risk-badge.high { color: var(--accent-high); background: rgba(255,90,60,0.1); }
.risk-badge.high .dot { background: var(--accent-high); }
.risk-badge.medium { color: var(--accent-med); background: rgba(240,180,41,0.1); }
.risk-badge.medium .dot { background: var(--accent-med); }
.risk-badge.low { color: var(--accent-low); background: rgba(53,208,184,0.1); }
.risk-badge.low .dot { background: var(--accent-low); }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-dim);
    background: transparent;
    padding: 8px 14px;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-low) !important;
    border-bottom: 2px solid var(--accent-low) !important;
}

/* Panels around charts */
.chart-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 16px 18px 6px 18px;
    margin-bottom: 18px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 5px;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Metric widget override (used sparingly) */
[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text);
}
</style>
"""

# Shared color tokens for Plotly / Matplotlib / Seaborn so every chart
# library draws from the same palette as the CSS.
COLORS = {
    "bg": "#0A1220",
    "panel": "#121D33",
    "border": "#24344F",
    "text": "#E8EDF5",
    "text_dim": "#8296B8",
    "high": "#FF5A3C",
    "medium": "#F0B429",
    "low": "#35D0B8",
    "blue": "#5B8DEF",
}

RISK_COLOR_MAP = {"High": COLORS["high"], "Medium": COLORS["medium"], "Low": COLORS["low"]}
STATUS_COLOR_MAP = {"On Time": COLORS["low"], "Late": COLORS["high"]}

PLOTLY_LAYOUT = dict(
    paper_bgcolor=COLORS["panel"],
    plot_bgcolor=COLORS["panel"],
    font=dict(family="IBM Plex Mono, monospace", color=COLORS["text"], size=12),
    # NOTE: deliberately no top-level "title_font" here. Chart titles are
    # rendered via the custom HTML "section-title" header above each panel,
    # not Plotly's built-in title. Setting title_font without a title.text
    # makes Plotly's JS render the literal word "undefined" where the title
    # would go - this bit us once, don't reintroduce it.
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text_dim"])),
    xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], color=COLORS["text_dim"]),
    yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], color=COLORS["text_dim"]),
    margin=dict(l=10, r=10, t=40, b=10),
)


def style_fig(fig, height=380):
    """Apply the shared dark control-room theme to a Plotly figure."""
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig
