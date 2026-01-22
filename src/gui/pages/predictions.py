"""
Predictions Page - Generate Cholera Forecasts
"""

import streamlit as st
import pandas as pd
import subprocess
import plotly.express as px
from pathlib import Path


def show():
    """Display predictions interface"""

    st.markdown('<h2 class="section-header">🔮 Cholera Predictions</h2>', unsafe_allow_html=True)

    # Check for trained model
    models_dir = Path('models/trained')
    model_files = list(models_dir.glob('*.pkl')) if models_dir.exists() else []

    if not model_files:
        st.warning("⚠️ No trained models found. Please train a model first.")
        if st.button("Go to Model Training"):
            st.switch_page("pages/model_training.py")
        return

    # Model selection
    st.markdown("### 🎯 Select Model")

    selected_model = st.selectbox(
        "Trained Model",
        [m.stem for m in model_files],
        help="Select a trained model for prediction"
    )

    model_path = models_dir / f"{selected_model}.pkl"

    # Prediction settings
    st.markdown("---")
    st.markdown("### ⚙️ Prediction Settings")

    col1, col2 = st.columns(2)

    with col1:
        forecast_horizon = st.slider(
            "Forecast Horizon (months)",
            min_value=1,
            max_value=12,
            value=3,
            help="Number of months to forecast ahead"
        )

        districts = st.multiselect(
            "Target Districts",
            [
                'Harare', 'Bulawayo', 'Manicaland', 'Mashonaland East',
                'Mashonaland West', 'Midlands', 'Masvingo',
                'Matabeleland North', 'Matabeleland South'
            ],
            default=['Harare', 'Manicaland'],
            help="Select districts for forecasting"
        )

    with col2:
        start_month = st.date_input(
            "Start Month",
            help="Starting month for forecast"
        )

        include_uncertainty = st.checkbox(
            "Include Uncertainty Estimates",
            value=True,
            help="Show prediction intervals"
        )

    # Generate predictions button
    st.markdown("---")

    if st.button("🔮 Generate Predictions", type="primary", use_container_width=True):
        generate_predictions(model_path, forecast_horizon, districts, start_month)

    # Show existing predictions
    st.markdown("---")
    st.markdown("### 📊 Prediction Results")

    show_predictions()


def generate_predictions(model_path, horizon, districts, start_month):
    """Generate predictions"""

    # Check for required data
    historic_data = Path('data/processed/harmonized_data.csv')
    future_climate = Path('data/processed/future_climate.csv')

    if not historic_data.exists():
        st.error("❌ Historical data not found")
        return

    # For demo, use test data as future climate
    if not future_climate.exists():
        test_data = Path('data/processed/test_data.csv')
        if test_data.exists():
            df = pd.read_csv(test_data)
            df.drop(columns=['cholera_cases'], errors='ignore').to_csv(future_climate, index=False)

    predictions_path = Path('outputs/forecasts/cholera_predictions.csv')
    predictions_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        'python', 'src/chap_integration/chap_predict.py',
        str(model_path),
        str(historic_data),
        str(future_climate),
        str(predictions_path)
    ]

    with st.spinner("🔄 Generating predictions..."):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            st.success("✅ Predictions generated successfully!")

            with st.expander("📋 Prediction Output"):
                st.code(result.stdout)

        except subprocess.CalledProcessError as e:
            st.error("❌ Prediction failed!")
            st.code(e.stderr)


def show_predictions():
    """Display existing predictions"""

    predictions_path = Path('outputs/forecasts/cholera_predictions.csv')

    if not predictions_path.exists():
        st.info("ℹ️ No predictions available yet")
        return

    # Load predictions
    df = pd.read_csv(predictions_path)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Predictions", len(df))

    with col2:
        if 'district' in df.columns:
            st.metric("Districts", df['district'].nunique())

    with col3:
        if 'mean_prediction' in df.columns:
            st.metric("Avg Predicted Cases", f"{df['mean_prediction'].mean():.1f}")

    with col4:
        if 'mean_prediction' in df.columns:
            high_risk = (df['mean_prediction'] > 50).sum()
            st.metric("High Risk Periods", high_risk)

    # Visualization
    st.markdown("#### 📈 Forecast Visualization")

    if 'district' in df.columns and 'mean_prediction' in df.columns:
        fig = px.line(
            df,
            x='time_period',
            y='mean_prediction',
            color='district',
            title='Cholera Case Predictions by District',
            labels={'mean_prediction': 'Predicted Cases', 'time_period': 'Time Period'}
        )

        fig.update_layout(plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

    # Data table
    st.markdown("#### 📋 Prediction Data")
    st.dataframe(df, use_container_width=True, height=300)

    # Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Predictions",
        data=csv,
        file_name="cholera_predictions.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    show()
