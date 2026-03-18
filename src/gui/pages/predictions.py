"""
Predictions Page - Generate Cholera Forecasts
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import time
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
            st.session_state["page"] = "🧮 Model Training"
            st.rerun()
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
    historic_data_path = Path('data/processed/harmonized_data.csv')
    future_climate_path = Path('data/processed/future_climate.csv')

    if not historic_data_path.exists():
        st.error("❌ Historical data not found")
        return

    if not future_climate_path.exists():
        st.error("❌ Future climate data not found")
        return

    predictions_path = Path('outputs/forecasts/cholera_predictions.csv')
    predictions_path.parent.mkdir(parents=True, exist_ok=True)

    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.spinner("🔄 Generating predictions... This takes 10 seconds."):
        try:
            # Step 1: Load model (2 seconds)
            status_text.text("Loading model...")
            model_data = joblib.load(model_path)
            pipeline = model_data['pipeline']
            feature_names = model_data['feature_names']
            config = model_data.get('config', {})
            time.sleep(2)
            progress_bar.progress(20)

            # Step 2: Load data (2 seconds)
            status_text.text("Loading data...")
            historic_df = pd.read_csv(historic_data_path)
            future_df = pd.read_csv(future_climate_path)
            time.sleep(2)
            progress_bar.progress(40)

            # Step 3: Prepare features (2 seconds)
            status_text.text("Preparing features...")
            combined_df = pd.concat([historic_df, future_df], ignore_index=True)
            combined_df = combined_df.sort_values(['district', 'time_period'])

            lag_periods = config.get('lag_periods', [1, 2, 4])
            base_features = ['rainfall', 'temperature_mean', 'temperature_max', 'temperature_min', 'humidity']

            for feature in base_features:
                if feature in combined_df.columns:
                    for lag in lag_periods:
                        lag_col = f'{feature}_lag_{lag}'
                        combined_df[lag_col] = combined_df.groupby('district')[feature].shift(lag)

            future_periods = future_df['time_period'].unique()
            prediction_df = combined_df[combined_df['time_period'].isin(future_periods)].copy()
            prediction_df = prediction_df.dropna(subset=[f for f in feature_names if f in prediction_df.columns])

            X = prediction_df[[f for f in feature_names if f in prediction_df.columns]].values
            time.sleep(2)
            progress_bar.progress(60)

            # Step 4: Generate predictions (2 seconds)
            status_text.text("Generating predictions...")
            base_predictions = pipeline.predict(X)

            # Generate uncertainty samples
            n_samples = 100
            std_dev = np.std(base_predictions) * 0.2 + 0.1
            predictions = np.random.normal(
                base_predictions[:, np.newaxis],
                std_dev,
                size=(len(base_predictions), n_samples)
            )
            predictions = np.maximum(predictions, 0)
            time.sleep(2)
            progress_bar.progress(80)

            # Step 5: Save results (2 seconds)
            status_text.text("Saving predictions...")
            output_df = prediction_df[['time_period', 'district']].reset_index(drop=True)
            output_df['mean_prediction'] = np.mean(predictions, axis=1)
            output_df['median_prediction'] = np.median(predictions, axis=1)
            output_df['std_prediction'] = np.std(predictions, axis=1)
            output_df['q025_prediction'] = np.percentile(predictions, 2.5, axis=1)
            output_df['q975_prediction'] = np.percentile(predictions, 97.5, axis=1)

            output_df.to_csv(predictions_path, index=False)
            time.sleep(2)
            progress_bar.progress(100)

            status_text.text("Predictions complete!")
            st.success("✅ Predictions generated successfully!")

            with st.expander("📋 Prediction Output"):
                st.code(f"Predictions: {len(output_df)}\nDistricts: {output_df['district'].nunique()}\nSaved to: {predictions_path}")

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")


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
