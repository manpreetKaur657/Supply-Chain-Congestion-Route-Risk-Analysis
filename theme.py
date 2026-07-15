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
    --text-dim: #9FB0CC;
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
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent;
}
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"],
button[aria-label*="sidebar" i],
[data-testid="stSidebar"] [data-testid="baseButton-headerNoPadding"] {
    visibility: visible !important;
    opacity: 1 !important;
    display: flex !important;
    color: var(--text) !important;
    z-index: 999 !important;
}
[data-testid="stSidebarCollapseButton"] *,
[data-testid="stSidebarCollapsedControl"] *,
button[aria-label*="sidebar" i] * {
    color: var(--text) !important;
    fill: var(--text) !important;
    stroke: var(--text) !important;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.01em;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(
        180deg,
        #0D1830 0%,
        #101D35 45%,
        #0D1830 100%
    ) !important;

    border-right:1px solid rgba(91,141,239,.25);

    box-shadow:
        inset -1px 0 0 rgba(255,255,255,.03),
        8px 0 30px rgba(0,0,0,.25);
}
section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-dim);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] label {
    color: var(--text) !important;
    font-size: 0.82rem !important;
    opacity: 1 !important;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"]{
    margin-top:8px;
    margin-bottom:4px;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div{
    border-radius:8px !important;
    min-height:48px;
    transition:all .2s ease;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.03);
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover{
    border-color: var(--accent-blue) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text);
}

/* Sidebar header - replaces the emoji that rendered as a broken glyph
   (Space Grotesk has no emoji glyphs and fallback wasn't reliable across
   browsers) with a small CSS-drawn accent icon matching the main title. */
section[data-testid="stSidebar"] .sidebar-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text) !important;
    margin: 4px 0 4px 0;
    display: flex;
    align-items: center;
    gap: 9px;
}
section[data-testid="stSidebar"] .sidebar-title::before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 22px;
    background: var(--accent-low);
    border-radius: 2px;
    flex-shrink: 0;
}
section[data-testid="stSidebar"] .sidebar-subtitle {
    color: var(--text-dim) !important;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 10px 0;
}

/* Dividers between filter groups + a themed checkbox instead of the
   default browser-style box, requested as the remaining sidebar polish. */
section[data-testid="stSidebar"] .sidebar-divider {
    border-top: 1px solid var(--border);
    margin: 18px 0 16px 0;
    height: 0;
}
section[data-testid="stSidebar"] [data-testid="stCheckbox"] {
    margin-top: 0px;
    margin-bottom: 6px;
}
section[data-testid="stSidebar"] [data-testid="stCheckbox"] label span[data-baseweb="checkbox"] > div:first-child {
    background-color: var(--panel) !important;
    border-color: var(--accent-low) !important;
    border-width: 1.5px !important;
    border-radius: 4px !important;
}
section[data-testid="stSidebar"] [data-testid="stCheckbox"] input:checked ~ span[data-baseweb="checkbox"] > div:first-child {
    background-color: var(--accent-low) !important;
}
section[data-testid="stSidebar"] [data-testid="stCheckbox"] p {
    font-size: 0.82rem !important;
}

.manifest-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid var(--border);
    padding-bottom: 22px;
    margin-bottom: 30px;
}
.manifest-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.2rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin: 0;
    display: flex;
    align-items: stretch;
    gap: 12px;
    flex-shrink: 0;
}
.manifest-title::before {
    content: "";
    display: inline-block;
    width: 10px;
    background: var(--accent-low);
    border-radius: 2px;
    flex-shrink: 0;
}
.manifest-subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
    color: var(--text-dim);
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 6px;
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
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--text);
    white-space: nowrap;
}
.kpi-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    margin-top: 2px;
}

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

.stTabs [data-testid="stTab"] {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text) !important;
    opacity: 0.75;
    padding: 8px 14px;
}

.stTabs [data-testid="stTab"][aria-selected="true"] {
    color: var(--accent-low) !important;
    opacity: 1;
    border-bottom: 2px solid var(--accent-low) !important;
}

.stTabs [data-testid="stTab"][aria-selected="false"] {
    color: var(--text) !important;
    opacity: 0.75;
}

.chart-panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 16px 18px 6px 18px;
    margin-bottom: 18px;
}

[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 5px;
}

hr { border-color: var(--border) !important; }

[data-testid="stMetricValue"] {
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text);
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"],
section[data-testid="stSidebar"] [data-baseweb="input"] input,
section[data-testid="stSidebar"] [data-baseweb="base-input"],
section[data-testid="stSidebar"] [data-testid="stDateInput"] input,
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div {
    box-sizing: border-box !important;
    background-color: var(--panel) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}
span[data-baseweb="tag"],
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: var(--accent-blue) !important;
    border-color: var(--accent-blue) !important;
}
span[data-baseweb="tag"] * {
    color: #0A1220 !important;
}
div[data-baseweb="popover"] div[data-baseweb="menu"],
div[data-baseweb="popover"] ul,
div[data-baseweb="calendar"],
div[data-baseweb="calendar"] * {
    background-color: var(--panel) !important;
    color: var(--text) !important;
}
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li *,
div[data-baseweb="popover"] [role="option"],
div[data-baseweb="popover"] [role="option"] * {
    color: var(--text) !important;
    background-color: var(--panel) !important;
    opacity: 1 !important;
}
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] [role="option"]:hover {
    background-color: var(--panel-alt) !important;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stDownloadButton"] button,
[data-testid^="stBaseButton"],
button[kind="secondary"],
button[kind="primary"] {
    background-color: var(--panel) !important;
    color: var(--accent-low) !important;
    border: 1px solid var(--accent-low) !important;
    font-family: 'IBM Plex Mono', monospace;
    opacity: 1 !important;
}
.stButton > button *,
.stDownloadButton > button *,
[data-testid="stDownloadButton"] button *,
[data-testid^="stBaseButton"] * {
    color: var(--accent-low) !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid^="stBaseButton"]:hover {
    background-color: var(--accent-low) !important;
}
.stButton > button:hover *,
.stDownloadButton > button:hover *,
[data-testid="stDownloadButton"] button:hover *,
[data-testid^="stBaseButton"]:hover * {
    color: #0A1220 !important;
}
</style>
"""

COLORS = {
    "bg": "#0A1220",
    "panel": "#121D33",
    "border": "#24344F",
    "text": "#E8EDF5",
    "text_dim": "#9FB0CC",
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
    title=dict(text=""),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text_dim"])),
    xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], color=COLORS["text_dim"]),
    yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], color=COLORS["text_dim"]),
    margin=dict(l=10, r=10, t=40, b=10),
)


def style_fig(fig, height=380):
    """Apply the shared dark control-room theme to a Plotly figure."""
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig
