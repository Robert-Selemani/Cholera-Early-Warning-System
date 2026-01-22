"""
Settings Page - System Configuration
"""

import streamlit as st
import yaml
from pathlib import Path


def show():
    """Display settings interface"""

    st.markdown('<h2 class="section-header">⚙️ System Settings</h2>', unsafe_allow_html=True)

    # Settings tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔧 CHAP Configuration",
        "🌍 Geographic Settings",
        "📡 Data Sources",
        "ℹ️ About"
    ])

    with tab1:
        chap_settings()

    with tab2:
        geographic_settings()

    with tab3:
        data_sources_settings()

    with tab4:
        about_section()


def chap_settings():
    """CHAP configuration settings"""
    st.markdown("### 🔧 CHAP Platform Configuration")

    config_path = Path('config/chap_config.yaml')

    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    # Model settings
    st.markdown("#### Model Settings")

    col1, col2 = st.columns(2)

    with col1:
        model_type = st.selectbox(
            "Default Model Type",
            ['random_forest', 'gradient_boosting'],
            index=0 if config.get('model_type') == 'random_forest' else 1
        )

        n_estimators = st.number_input(
            "Number of Estimators",
            min_value=50,
            max_value=500,
            value=config.get('n_estimators', 200)
        )

    with col2:
        max_depth = st.number_input(
            "Maximum Depth",
            min_value=5,
            max_value=30,
            value=config.get('max_depth', 15)
        )

        random_state = st.number_input(
            "Random State",
            min_value=0,
            value=config.get('random_state', 42)
        )

    # Forecast settings
    st.markdown("---")
    st.markdown("#### Forecast Settings")

    col1, col2 = st.columns(2)

    with col1:
        forecast_horizon = st.number_input(
            "Default Forecast Horizon (months)",
            min_value=1,
            max_value=24,
            value=config.get('forecast_horizon', 12)
        )

    with col2:
        prediction_samples = st.number_input(
            "Prediction Samples",
            min_value=10,
            max_value=1000,
            value=config.get('prediction_samples', 100)
        )

    # Save button
    if st.button("💾 Save CHAP Configuration", type="primary"):
        new_config = {
            'model_type': model_type,
            'n_estimators': n_estimators,
            'max_depth': max_depth,
            'random_state': random_state,
            'forecast_horizon': forecast_horizon,
            'prediction_samples': prediction_samples,
            'lag_periods': config.get('lag_periods', [1, 2, 4, 8])
        }

        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w') as f:
            yaml.dump(new_config, f)

        st.success("✅ Configuration saved!")


def geographic_settings():
    """Geographic settings"""
    st.markdown("### 🌍 Geographic Configuration")

    # Zimbabwe districts
    st.markdown("#### Focus Districts")

    districts = [
        'Harare', 'Bulawayo', 'Manicaland', 'Mashonaland East',
        'Mashonaland West', 'Midlands', 'Masvingo',
        'Matabeleland North', 'Matabeleland South', 'Mashonaland Central'
    ]

    selected_districts = st.multiselect(
        "Active Districts for Monitoring",
        districts,
        default=['Harare', 'Manicaland', 'Mashonaland East']
    )

    # High-risk areas
    st.markdown("---")
    st.markdown("#### High-Risk Areas")

    st.info("""
    **Known Cholera Hotspots in Zimbabwe:**
    - Harare high-density suburbs (Budiriro, Glen View, Kuwadzana)
    - Flood-prone districts along major river systems
    - Areas with water infrastructure challenges
    """)

    # Rainy season
    st.markdown("---")
    st.markdown("#### Seasonal Configuration")

    st.markdown("**High-Risk Months (Rainy Season)**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        nov = st.checkbox("November", value=True)

    with col2:
        dec = st.checkbox("December", value=True)

    with col3:
        jan = st.checkbox("January", value=True)

    with col4:
        feb = st.checkbox("February", value=True)


def data_sources_settings():
    """Data sources configuration"""
    st.markdown("### 📡 Data Sources Configuration")

    # Climate data
    st.markdown("#### 🌡️ Climate Data Sources")

    climate_sources = {
        'CHIRPS': 'https://data.chc.ucsb.edu/products/CHIRPS-2.0/',
        'ERA5': 'https://cds.climate.copernicus.eu/',
        'Zimbabwe Met Services': 'Local weather station data',
        'DHIS2 Climate App': 'https://dhis2.org/climate/climate-data-app/',
        'WMO Zimbabwe': 'https://worldweather.wmo.int/en/country.html?countryCode=ZWE'
    }

    for source, url in climate_sources.items():
        st.markdown(f"- **{source}**: [{url}]({url})" if url.startswith('http') else f"- **{source}**: {url}")

    # Health data
    st.markdown("---")
    st.markdown("#### 🏥 Health Data Sources")

    st.markdown("""
    - **DHIS2**: District Health Information System 2
    - **IDSR**: Integrated Disease Surveillance and Response
    - **Ministry of Health and Child Care**: Cholera surveillance data
    - **WHO AFRO**: Regional data
    """)

    # Geospatial data
    st.markdown("---")
    st.markdown("#### 🗺️ Geospatial Data Sources")

    st.markdown("""
    - **ZINGSA GeoPortal**: [https://zimgeoportal.org.zw/](https://zimgeoportal.org.zw/)
    - **GADM**: Administrative boundaries
    - **WorldPop**: Population density estimates
    - **OpenStreetMap**: Infrastructure data
    """)

    # DHIS2 integration
    st.markdown("---")
    st.markdown("#### 🔗 DHIS2 Integration")

    dhis2_enabled = st.checkbox("Enable DHIS2 Integration", value=False)

    if dhis2_enabled:
        st.text_input("DHIS2 Server URL", placeholder="https://your-dhis2-instance.org")
        st.text_input("API Version", value="39")
        st.info("💡 Configure credentials in `.env` file")


def about_section():
    """About section"""
    st.markdown("### ℹ️ About Cholera Early Warning System")

    st.markdown("""
    ## Climate-Informed Decision Support Tool
    **For Zimbabwe and Southern Africa**

    ### Version Information
    - **Version**: 1.0.0
    - **Release Date**: January 2026
    - **Platform**: CHAP (Climate and Health Analysis Platform)

    ### Key Features
    - 🌡️ Real-time climate data integration
    - 📊 Epidemiological surveillance processing
    - 🧮 Predictive modeling using machine learning
    - 🗺️ Geographic risk mapping
    - ⚠️ Early warning alerts
    - 📈 Decision-support dashboards

    ### Geographic Coverage
    - **Primary**: District and provincial level in Zimbabwe
    - **Secondary**: Regional and cross-border level across Southern Africa

    ### Development Team
    Climate and Health Analytics

    ### Acknowledgments
    - Climate and health data providers
    - Zimbabwe Ministry of Health and Child Care
    - Zimbabwe Meteorological Services Department
    - Regional health authorities and climate centers
    - WHO AFRO
    - DHIS2 CHAP Platform
    - Research and humanitarian partners

    ### License
    Open Source - AGPL-3.0

    ### Support & Documentation
    - 📖 [Documentation](https://dhis2-chap.github.io/chap-core/)
    - 💻 [GitHub Repository](https://github.com/Robert-Selemani/Cholera-Early-Warning-System)
    - 🐛 [Report Issues](https://github.com/Robert-Selemani/Cholera-Early-Warning-System/issues)

    ### Data Sources
    - **GIS/Spatial**: [ZIMGEOPORTAL](https://zimgeoportal.org.zw/)
    - **Climate**: [DHIS2 Climate App](https://dhis2.org/climate/climate-data-app/)
    - **Weather**: [WMO Zimbabwe](https://worldweather.wmo.int/en/country.html?countryCode=ZWE)
    """)

    # System info
    st.markdown("---")
    st.markdown("### 💻 System Information")

    import sys
    import platform

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Python Version**: {sys.version.split()[0]}")
        st.markdown(f"**Platform**: {platform.system()} {platform.release()}")

    with col2:
        st.markdown(f"**Streamlit Version**: {st.__version__}")
        st.markdown(f"**CHAP Core**: Installed")


if __name__ == "__main__":
    show()
