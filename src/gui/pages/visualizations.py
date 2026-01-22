"""
Visualizations Page - Interactive Charts and Maps
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


def show():
    """Display visualizations interface"""

    st.markdown('<h2 class="section-header">📈 Data Visualizations</h2>', unsafe_allow_html=True)

    # Visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Time Series",
        "🗺️ Geographic",
        "🌡️ Climate Patterns",
        "📉 Trends & Correlations"
    ])

    with tab1:
        time_series_viz()

    with tab2:
        geographic_viz()

    with tab3:
        climate_viz()

    with tab4:
        trends_viz()


def time_series_viz():
    """Time series visualizations"""
    st.markdown("### 📊 Time Series Analysis")

    # Load data
    data_path = Path('data/processed/harmonized_data.csv')

    if not data_path.exists():
        st.info("ℹ️ No data available for visualization")
        return

    df = pd.read_csv(data_path)

    # District selection
    if 'district' in df.columns:
        selected_districts = st.multiselect(
            "Select Districts",
            df['district'].unique().tolist(),
            default=df['district'].unique()[:3].tolist()
        )

        df_filtered = df[df['district'].isin(selected_districts)]
    else:
        df_filtered = df

    # Cholera cases over time
    if 'cholera_cases' in df_filtered.columns and 'time_period' in df_filtered.columns:
        fig = px.line(
            df_filtered,
            x='time_period',
            y='cholera_cases',
            color='district' if 'district' in df_filtered.columns else None,
            title='Cholera Cases Over Time',
            labels={'cholera_cases': 'Cases', 'time_period': 'Time Period'}
        )

        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

    # Rainfall patterns
    if 'rainfall' in df_filtered.columns:
        fig = px.area(
            df_filtered,
            x='time_period',
            y='rainfall',
            color='district' if 'district' in df_filtered.columns else None,
            title='Rainfall Patterns',
            labels={'rainfall': 'Rainfall (mm)', 'time_period': 'Time Period'}
        )

        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)


def geographic_viz():
    """Geographic visualizations"""
    st.markdown("### 🗺️ Geographic Distribution")

    st.info("🚧 Interactive map visualization coming soon!")
    st.markdown("""
    **Planned Features:**
    - District-level choropleth maps
    - Risk heatmaps
    - Population density overlays
    - Water infrastructure mapping
    """)


def climate_viz():
    """Climate pattern visualizations"""
    st.markdown("### 🌡️ Climate Patterns")

    data_path = Path('data/processed/harmonized_data.csv')

    if not data_path.exists():
        st.info("ℹ️ No data available")
        return

    df = pd.read_csv(data_path)

    # Temperature vs rainfall
    if 'temperature_mean' in df.columns and 'rainfall' in df.columns:
        fig = px.scatter(
            df,
            x='temperature_mean',
            y='rainfall',
            color='cholera_cases' if 'cholera_cases' in df.columns else None,
            size='cholera_cases' if 'cholera_cases' in df.columns else None,
            title='Temperature vs Rainfall',
            labels={
                'temperature_mean': 'Mean Temperature (°C)',
                'rainfall': 'Rainfall (mm)',
                'cholera_cases': 'Cases'
            }
        )

        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    # Seasonal patterns
    if 'time_period' in df.columns and 'cholera_cases' in df.columns:
        df['month'] = pd.to_datetime(df['time_period']).dt.month

        monthly_avg = df.groupby('month')['cholera_cases'].mean().reset_index()

        fig = px.bar(
            monthly_avg,
            x='month',
            y='cholera_cases',
            title='Seasonal Pattern (Average Cases by Month)',
            labels={'month': 'Month', 'cholera_cases': 'Avg Cases'}
        )

        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)


def trends_viz():
    """Trends and correlations"""
    st.markdown("### 📉 Trends & Correlations")

    data_path = Path('data/processed/harmonized_data.csv')

    if not data_path.exists():
        st.info("ℹ️ No data available")
        return

    df = pd.read_csv(data_path)

    # Correlation matrix
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if numeric_cols:
        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            title='Correlation Matrix',
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )

        fig.update_layout(width=700, height=600)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    show()
