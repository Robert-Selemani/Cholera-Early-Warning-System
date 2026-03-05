"""
Cholera Early Warning System - GUI Dashboard
Zimbabwe and Southern Africa

A comprehensive web-based interface for climate-informed cholera forecasting
using the CHAP (Climate and Health Analysis Platform) framework.
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Page configuration
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

# Open Graph / Social preview meta tags
st.markdown("""
    <meta property="og:type"        content="website" />
    <meta property="og:site_name"   content="Cholera Early Warning System" />
    <meta property="og:title"       content="Cholera Early Warning System – Zimbabwe & Southern Africa" />
    <meta property="og:description" content="Climate-informed cholera forecasting and early warning tool for Zimbabwe and Southern Africa. Powered by the CHAP framework — combining epidemiological data, climate indicators, and AI-driven risk models to support public health decision-making." />
    <meta property="og:image"       content="https://raw.githubusercontent.com/Robert-Selemani/Cholera-Early-Warning-System/main/docs/images/system-approach.jpeg" />
    <meta property="og:image:alt"   content="Cholera Early Warning System – system approach diagram" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />

    <meta name="twitter:card"        content="summary_large_image" />
    <meta name="twitter:title"       content="Cholera Early Warning System – Zimbabwe & Southern Africa" />
    <meta name="twitter:description" content="Climate-informed cholera forecasting and early warning tool for Zimbabwe and Southern Africa. Powered by the CHAP framework — combining epidemiological data, climate indicators, and AI-driven risk models to support public health decision-making." />
    <meta name="twitter:image"       content="https://raw.githubusercontent.com/Robert-Selemani/Cholera-Early-Warning-System/main/docs/images/system-approach.jpeg" />

    <meta name="description" content="Climate-informed cholera forecasting and early warning tool for Zimbabwe and Southern Africa. Powered by the CHAP framework — combining epidemiological data, climate indicators, and AI-driven risk models to support public health decision-making." />
""", unsafe_allow_html=True)

# Custom CSS for CSIDNET-inspired styling
st.markdown("""
<style>
    /* CSIDNET Color Palette */
    :root {
        --teal-button: #4C7C83;
        --teal-card: #033E45;
        --midnight: #020381;
        --lime-card: #D3F781;
        --aqua-card: #46CBDE;
        --salmon-card: #FC8170;
        --teal-light: #D0DADC;
        --lime-light: #EFF4E3;
        --aqua-light: #DAEEF1;
        --salmon-light: #F6E1DE;
        --off-white: #F4F4F4;
    }

    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, var(--teal-card) 0%, var(--teal-button) 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }

    .main-header p {
        color: var(--aqua-light);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }

    /* Card styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 5px solid var(--aqua-card);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }

    .metric-card.warning {
        border-left-color: var(--salmon-card);
    }

    .metric-card.success {
        border-left-color: var(--lime-card);
    }

    /* Button styling */
    .stButton>button {
        background-color: var(--midnight);
        color: white;
        border-radius: 5px;
        border: 1px solid rgba(0,0,0,0.1);
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: var(--teal-button);
        border-color: var(--teal-button);
        box-shadow: 0 4px 8px rgba(76,124,131,0.3);
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--teal-light);
    }

    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 5px solid var(--aqua-card);
    }

    /* Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Section headers */
    .section-header {
        color: var(--teal-card);
        border-bottom: 3px solid var(--aqua-card);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

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

# Page selection
page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Dashboard",
        "📊 Data Management",
        "🧮 Model Training",
        "🔮 Predictions",
        "📈 Visualizations",
        "📋 Evaluation",
        "⚙️ Settings"
    ],
    index=0
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
