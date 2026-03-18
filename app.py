"""
Cholera Early Warning System - GUI Dashboard
Zimbabwe and Southern Africa

A comprehensive web-based interface for climate-informed cholera forecasting
using the CHAP (Climate and Health Analysis Platform) framework.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

_OG_IMAGE = "https://raw.githubusercontent.com/Robert-Selemani/Cholera-Early-Warning-System/main/docs/images/system-approach.jpeg"
_OG_TITLE = "Cholera Early Warning System – Zimbabwe & Southern Africa"
_OG_DESC  = (
    "Climate-informed cholera forecasting and early warning tool for Zimbabwe "
    "and Southern Africa. Powered by the CHAP framework — combining "
    "epidemiological data, climate indicators, and AI-driven risk models to "
    "support public health decision-making."
)

# Page configuration – set_page_config writes og:title / og:description to <head>
st.set_page_config(
    page_title="Cholera Early Warning System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Robert-Selemani/Cholera-Early-Warning-System',
        'Report a bug': 'https://github.com/Robert-Selemani/Cholera-Early-Warning-System/issues',
        'About': '''
        ## Cholera Early Warning System

        Climate-Informed Decision Support Tool for Zimbabwe and Southern Africa

        **Version:** 1.0.0
        **Powered by:** CHAP (Climate and Health Analysis Platform)
        '''
    }
)

# Inject additional OG tags (image, type, twitter) into <head> via a hidden iframe
components.html(f"""
<!DOCTYPE html>
<html>
<head>
    <meta property="og:type"         content="website" />
    <meta property="og:site_name"    content="Cholera Early Warning System" />
    <meta property="og:title"        content="{_OG_TITLE}" />
    <meta property="og:description"  content="{_OG_DESC}" />
    <meta property="og:image"        content="{_OG_IMAGE}" />
    <meta property="og:image:alt"    content="Cholera Early Warning System – system approach diagram" />
    <meta property="og:image:width"  content="1200" />
    <meta property="og:image:height" content="630" />
    <meta name="twitter:card"        content="summary_large_image" />
    <meta name="twitter:title"       content="{_OG_TITLE}" />
    <meta name="twitter:description" content="{_OG_DESC}" />
    <meta name="twitter:image"       content="{_OG_IMAGE}" />
    <meta name="description"         content="{_OG_DESC}" />
    <script>
        // Hoist meta tags into the parent page's <head>
        const metas = document.head.querySelectorAll('meta');
        metas.forEach(m => {{
            try {{ window.parent.document.head.appendChild(m.cloneNode(true)); }} catch(e) {{}}
        }});
    </script>
</head>
<body></body>
</html>
""", height=0)

# ---------------------------------------------------------------------------
# Dark mode — default: follow OS/browser (prefers-color-scheme)
#             button:  cycle  system → dark → light → system
# ---------------------------------------------------------------------------
_dm = st.session_state.get("dark_mode", "system")  # "system" | "dark" | "light"

# CSS variables for each mode
_DARK_VARS = """
    --bg-main:      #0E1117;
    --bg-card:      #1A1D27;
    --bg-sidebar:   #161923;
    --text-primary: #FAFAFA;
    --text-muted:   #A0A8B8;
    --border-color: #2E3347;
    --header-bg1:   #022B30;
    --header-bg2:   #2E5D65;
    --section-col:  #46CBDE;
    --card-bg:      #1A1D27;
    --input-bg:     #1E2130;
"""
_LIGHT_VARS = """
    --bg-main:      #FFFFFF;
    --bg-card:      #FFFFFF;
    --bg-sidebar:   #D0DADC;
    --text-primary: #0E1117;
    --text-muted:   #6c757d;
    --border-color: #E0E0E0;
    --header-bg1:   #033E45;
    --header-bg2:   #4C7C83;
    --section-col:  #033E45;
    --card-bg:      #FFFFFF;
    --input-bg:     #F4F4F4;
"""

# Raw CSS rules only — no <style> tags here so they can be safely embedded
# anywhere without breaking the wrapping <style> block.
_BASE_RULES = """
/* ── App shell ────────────────────────────────────────────────────── */
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    transition: background-color 0.3s ease;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Main content text ────────────────────────────────────────────── */
.stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label, span {
    color: var(--text-primary) !important;
}

/* ── Inputs & selects ─────────────────────────────────────────────── */
input, textarea, select,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
.stSelectbox select {
    background-color: var(--input-bg) !important;
    color: var(--text-primary) !important;
    border-color: var(--border-color) !important;
}

/* ── Metric blocks ────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.75rem 1rem;
}

/* ── Dataframes / tables ──────────────────────────────────────────── */
[data-testid="stDataFrame"], .dataframe {
    background-color: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border-radius: 8px;
    overflow: hidden;
}

/* ── Expanders ────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
}

/* ── Alert / info boxes ───────────────────────────────────────────── */
.stAlert {
    border-radius: 8px;
    border-left: 5px solid var(--section-col);
}

/* ── Horizontal rules ─────────────────────────────────────────────── */
hr { border-color: var(--border-color) !important; }

/* ── Custom cards ─────────────────────────────────────────────────── */
.metric-card {
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 5px solid #46CBDE;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    margin: 1rem 0;
}
.metric-card.warning { border-left-color: #FC8170; }
.metric-card.success { border-left-color: #D3F781; }

/* ── Main header ──────────────────────────────────────────────────── */
.main-header {
    background: linear-gradient(135deg, var(--header-bg1) 0%, var(--header-bg2) 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.main-header h1 { color: white; margin: 0; font-size: 2.5rem; }
.main-header p  { color: #DAEEF1; margin: 0.5rem 0 0 0; font-size: 1.1rem; }

/* ── Section headers ──────────────────────────────────────────────── */
.section-header {
    color: var(--section-col);
    border-bottom: 3px solid #46CBDE;
    padding-bottom: 0.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

/* ── Buttons ──────────────────────────────────────────────────────── */
.stButton>button {
    background-color: #020381;
    color: white;
    border-radius: 5px;
    border: 1px solid rgba(0,0,0,0.1);
    font-weight: 500;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #4C7C83;
    border-color: #4C7C83;
    box-shadow: 0 4px 8px rgba(76,124,131,0.3);
}
"""

# Build a single <style> block with the correct :root vars + shared rules
if _dm == "system":
    _css = f"""<style>
@media (prefers-color-scheme: dark)  {{ :root {{ {_DARK_VARS}  }} }}
@media (prefers-color-scheme: light) {{ :root {{ {_LIGHT_VARS} }} }}
{_BASE_RULES}
</style>"""
elif _dm == "dark":
    _css = f"<style>:root {{ {_DARK_VARS} }}\n{_BASE_RULES}</style>"
else:
    _css = f"<style>:root {{ {_LIGHT_VARS} }}\n{_BASE_RULES}</style>"

st.markdown(_css, unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏥 Cholera Early Warning System</h1>
    <p>Climate-Informed Decision Support for Zimbabwe and Southern Africa</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

# Dark mode toggle button
_icons   = {"system": "🖥️ System", "dark": "🌙 Dark", "light": "☀️ Light"}
_next    = {"system": "dark", "dark": "light", "light": "system"}
_tooltip = {"system": "Following system theme — click for Dark", "dark": "Dark mode — click for Light", "light": "Light mode — click for System"}

if st.sidebar.button(f"{_icons[_dm]}", help=_tooltip[_dm], use_container_width=True):
    st.session_state["dark_mode"] = _next[_dm]
    st.rerun()

st.sidebar.markdown("---")

# Page selection — honour programmatic navigation via session state
_pages = [
    "🏠 Dashboard",
    "📊 Data Management",
    "🧮 Model Training",
    "🔮 Predictions",
    "📈 Visualizations",
    "📋 Evaluation",
    "⚙️ Settings"
]
_default_index = 0
if "page" in st.session_state and st.session_state["page"] in _pages:
    _default_index = _pages.index(st.session_state.pop("page"))

page = st.sidebar.radio(
    "Select Module",
    _pages,
    index=_default_index
)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
**CHAP Platform**
Climate and Health Analysis Platform

**Focus Areas:**
- Harare (High-density suburbs)
- Manicaland
- Mashonaland East/West
- Midlands
- Masvingo

**Rainy Season:** Nov-Mar
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Links")
st.sidebar.markdown("""
- [CHAP Documentation](https://dhis2-chap.github.io/chap-core/)
- [GitHub Repository](https://github.com/Robert-Selemani/Cholera-Early-Warning-System)
- [ZIMGEOPORTAL](https://zimgeoportal.org.zw/)
- [DHIS2 Climate](https://dhis2.org/climate/)
""")

# Route to appropriate page
if "Dashboard" in page:
    from src.gui.pages import dashboard
    dashboard.show()
elif "Data Management" in page:
    from src.gui.pages import data_management
    data_management.show()
elif "Model Training" in page:
    from src.gui.pages import model_training
    model_training.show()
elif "Predictions" in page:
    from src.gui.pages import predictions
    predictions.show()
elif "Visualizations" in page:
    from src.gui.pages import visualizations
    visualizations.show()
elif "Evaluation" in page:
    from src.gui.pages import evaluation
    evaluation.show()
elif "Settings" in page:
    from src.gui.pages import settings
    settings.show()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Powered by CHAP**")
    st.caption("Climate and Health Analysis Platform")

with col2:
    st.markdown("**Data Sources**")
    st.caption("CHIRPS, ERA5, DHIS2, Zimbabwe Met Services")

with col3:
    st.markdown("**Version 1.0.0**")
    st.caption("Last Updated: 2026-01")

st.markdown(
    "<div style='text-align:center; margin-top:0.5rem; color:var(--text-muted,#6c757d); font-size:0.85rem;'>"
    "Developed by <a href='https://www.linkedin.com/in/robert-selemani/' target='_blank' "
    "style='color:#0A66C2; text-decoration:none; font-weight:600;'>Robert Selemani</a>"
    "</div>",
    unsafe_allow_html=True
)
