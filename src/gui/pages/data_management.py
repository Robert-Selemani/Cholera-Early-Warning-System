"""
Data Management Page - Upload, Harmonize, and Manage Data
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.chap_integration.data_harmonization import DataHarmonizer


def show():
    """Display data management interface"""

    st.markdown('<h2 class="section-header">📊 Data Management</h2>', unsafe_allow_html=True)

    # Tabs for different data operations
    tab1, tab2, tab3, tab4 = st.tabs([
        "📥 Upload Data",
        "🔄 Harmonize Data",
        "📋 View Data",
        "🗑️ Manage Data"
    ])

    with tab1:
        upload_data_tab()

    with tab2:
        harmonize_data_tab()

    with tab3:
        view_data_tab()

    with tab4:
        manage_data_tab()


def upload_data_tab():
    """Upload data files"""
    st.markdown("### Upload New Data")

    st.info("""
    **Supported Data Types:**
    - Climate Data (rainfall, temperature, humidity)
    - Health Data (cholera cases, IDSR reports)
    - Geospatial Data (district boundaries, population)
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Climate Data")
        climate_file = st.file_uploader(
            "Upload Climate Data (CSV)",
            type=['csv'],
            key='climate_upload',
            help="Upload CSV file with climate variables"
        )

        if climate_file is not None:
            df = pd.read_csv(climate_file)
            st.success(f"✅ Loaded {len(df)} rows")
            st.dataframe(df.head(), use_container_width=True)

            if st.button("💾 Save Climate Data", key='save_climate'):
                output_path = Path('data/raw/climate_data.csv')
                output_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(output_path, index=False)
                st.success(f"Saved to {output_path}")

    with col2:
        st.markdown("#### 🏥 Health Data")
        health_file = st.file_uploader(
            "Upload Health Data (CSV)",
            type=['csv'],
            key='health_upload',
            help="Upload CSV file with cholera cases"
        )

        if health_file is not None:
            df = pd.read_csv(health_file)
            st.success(f"✅ Loaded {len(df)} rows")
            st.dataframe(df.head(), use_container_width=True)

            if st.button("💾 Save Health Data", key='save_health'):
                output_path = Path('data/raw/health_data.csv')
                output_path.parent.mkdir(parents=True, exist_ok=True)
                df.to_csv(output_path, index=False)
                st.success(f"Saved to {output_path}")

    st.markdown("---")

    # Sample data download
    st.markdown("### 📥 Download Sample Data Templates")

    col1, col2 = st.columns(2)

    with col1:
        # Create sample climate template
        climate_template = pd.DataFrame({
            'time_period': ['2023-01', '2023-02'],
            'district': ['Harare', 'Harare'],
            'rainfall': [125.5, 98.3],
            'temperature_mean': [22.3, 23.1],
            'temperature_max': [28.5, 29.2],
            'temperature_min': [16.2, 17.0],
            'humidity': [65.0, 62.5]
        })

        csv = climate_template.to_csv(index=False)
        st.download_button(
            label="📄 Climate Data Template",
            data=csv,
            file_name="climate_template.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        # Create sample health template
        health_template = pd.DataFrame({
            'time_period': ['2023-01', '2023-02'],
            'district': ['Harare', 'Harare'],
            'cholera_cases': [12, 8]
        })

        csv = health_template.to_csv(index=False)
        st.download_button(
            label="📄 Health Data Template",
            data=csv,
            file_name="health_template.csv",
            mime="text/csv",
            use_container_width=True
        )


def harmonize_data_tab():
    """Harmonize climate and health data"""
    st.markdown("### Data Harmonization")

    st.info("""
    **Data Harmonization Process:**
    1. Standardize district names
    2. Align temporal resolution (monthly)
    3. Handle missing values
    4. Validate data quality
    """)

    # Check for available data
    climate_path = Path('data/raw/climate_data.csv')
    health_path = Path('data/raw/health_data.csv')

    if not climate_path.exists() or not health_path.exists():
        st.warning("⚠️ Please upload both climate and health data first")
        return

    # Load data previews
    climate_df = pd.read_csv(climate_path)
    health_df = pd.read_csv(health_path)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Climate Data Preview")
        st.dataframe(climate_df.head(), use_container_width=True)
        st.caption(f"Rows: {len(climate_df)} | Columns: {len(climate_df.columns)}")

    with col2:
        st.markdown("#### Health Data Preview")
        st.dataframe(health_df.head(), use_container_width=True)
        st.caption(f"Rows: {len(health_df)} | Columns: {len(health_df.columns)}")

    st.markdown("---")

    # Harmonization settings
    st.markdown("### ⚙️ Harmonization Settings")

    missing_strategy = st.selectbox(
        "Missing Value Strategy",
        ['interpolate', 'forward_fill', 'drop'],
        help="How to handle missing values in the data"
    )

    # Harmonize button
    if st.button("🔄 Harmonize Data", type="primary", use_container_width=True):
        with st.spinner("Harmonizing data..."):
            try:
                harmonizer = DataHarmonizer()

                # Harmonize
                harmonized_df = harmonizer.harmonize(
                    health_df,
                    climate_df,
                    output_path='data/processed/harmonized_data.csv'
                )

                st.success("✅ Data harmonization completed!")

                # Show results
                st.markdown("#### Harmonized Data")
                st.dataframe(harmonized_df.head(10), use_container_width=True)

                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", len(harmonized_df))
                with col2:
                    st.metric("Districts", harmonized_df['district'].nunique())
                with col3:
                    st.metric("Time Periods", harmonized_df['time_period'].nunique())

                # Download harmonized data
                csv = harmonized_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Harmonized Data",
                    data=csv,
                    file_name="harmonized_data.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"❌ Error during harmonization: {str(e)}")


def view_data_tab():
    """View existing data"""
    st.markdown("### View Existing Data")

    # Check for available datasets
    datasets = {
        'Raw Climate Data': 'data/raw/climate_data.csv',
        'Raw Health Data': 'data/raw/health_data.csv',
        'Harmonized Data': 'data/processed/harmonized_data.csv',
        'Test Data': 'data/processed/test_data.csv'
    }

    available_datasets = {
        name: path for name, path in datasets.items()
        if Path(path).exists()
    }

    if not available_datasets:
        st.warning("⚠️ No datasets available. Please upload data first.")
        return

    # Dataset selection
    selected_dataset = st.selectbox(
        "Select Dataset",
        list(available_datasets.keys())
    )

    # Load and display dataset
    df = pd.read_csv(available_datasets[selected_dataset])

    st.markdown(f"#### {selected_dataset}")

    # Dataset info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        if 'district' in df.columns:
            st.metric("Districts", df['district'].nunique())
    with col4:
        if 'time_period' in df.columns:
            st.metric("Time Periods", df['time_period'].nunique())

    # Data preview
    st.markdown("#### Data Preview")
    st.dataframe(df, use_container_width=True, height=400)

    # Summary statistics
    st.markdown("#### Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)


def manage_data_tab():
    """Manage and delete data"""
    st.markdown("### Manage Data")

    st.warning("⚠️ **Warning:** Deleted data cannot be recovered!")

    # List all data files
    data_dir = Path('data')
    data_files = []

    if data_dir.exists():
        for subdir in ['raw', 'processed']:
            subdir_path = data_dir / subdir
            if subdir_path.exists():
                for file in subdir_path.glob('*.csv'):
                    data_files.append(file)

    if not data_files:
        st.info("ℹ️ No data files found")
        return

    # Display files
    for file in data_files:
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.text(f"📄 {file.relative_to(data_dir)}")

        with col2:
            size_kb = file.stat().st_size / 1024
            st.caption(f"{size_kb:.1f} KB")

        with col3:
            if st.button("🗑️ Delete", key=f"delete_{file.name}"):
                file.unlink()
                st.success(f"Deleted {file.name}")
                st.rerun()


if __name__ == "__main__":
    show()
