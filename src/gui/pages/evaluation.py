"""
Evaluation Page - Model Performance Metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import time
import joblib
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def show():
    """Display evaluation interface"""

    st.markdown('<h2 class="section-header">📋 Model Evaluation</h2>', unsafe_allow_html=True)

    # Check for trained models
    models_dir = Path('models/trained')
    model_files = list(models_dir.glob('*.pkl')) if models_dir.exists() else []

    if not model_files:
        st.warning("⚠️ No trained models found")
        return

    # Model selection
    st.markdown("### 🎯 Select Model to Evaluate")

    selected_model = st.selectbox(
        "Trained Model",
        [m.stem for m in model_files]
    )

    model_path = models_dir / f"{selected_model}.pkl"

    # Evaluation controls
    st.markdown("---")

    col1, col2 = st.columns([3, 1])

    with col1:
        test_data_path = st.text_input(
            "Test Data Path",
            value="data/processed/test_data.csv",
            help="Path to test dataset"
        )

    with col2:
        if st.button("🧪 Run Evaluation", type="primary", use_container_width=True):
            run_evaluation(model_path, test_data_path)

    # Show evaluation results
    st.markdown("---")
    show_evaluation_results()


def run_evaluation(model_path, test_data_path):
    """Run model evaluation"""

    if not Path(test_data_path).exists():
        st.error(f"❌ Test data not found: {test_data_path}")
        return

    metrics_path = Path('models/evaluation/evaluation_metrics.json')
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.spinner("🔄 Evaluating model... This takes 10 seconds."):
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
            status_text.text("Loading test data...")
            test_df = pd.read_csv(test_data_path)
            train_df = pd.read_csv('data/processed/harmonized_data.csv')
            time.sleep(2)
            progress_bar.progress(40)

            # Step 3: Prepare features (2 seconds)
            status_text.text("Preparing features...")
            df = pd.concat([train_df, test_df], ignore_index=True)
            df = df.sort_values(['district', 'time_period'])

            lag_periods = config.get('lag_periods', [1, 2, 4])
            base_features = ['rainfall', 'temperature_mean', 'temperature_max', 'temperature_min', 'humidity']

            for feature in base_features:
                if feature in df.columns:
                    for lag in lag_periods:
                        lag_col = f'{feature}_lag_{lag}'
                        df[lag_col] = df.groupby('district')[feature].shift(lag)

            test_periods = test_df['time_period'].unique()
            df = df[df['time_period'].isin(test_periods)]
            df = df.dropna()

            X_test = df[[f for f in feature_names if f in df.columns]].values
            y_test = df['cholera_cases'].fillna(0).values
            time.sleep(2)
            progress_bar.progress(60)

            # Step 4: Generate predictions (2 seconds)
            status_text.text("Generating predictions...")
            y_pred = pipeline.predict(X_test)
            time.sleep(2)
            progress_bar.progress(80)

            # Step 5: Calculate metrics (2 seconds)
            status_text.text("Calculating metrics...")
            metrics = {}
            metrics['mae'] = float(mean_absolute_error(y_test, y_pred))
            metrics['rmse'] = float(np.sqrt(mean_squared_error(y_test, y_pred)))
            metrics['r2'] = float(r2_score(y_test, y_pred))
            metrics['correlation'] = float(np.corrcoef(y_test, y_pred)[0, 1]) if len(y_test) > 1 else 0.0
            metrics['bias'] = float(np.mean(y_pred - y_test))

            # Detection metrics
            y_true_binary = (y_test > 0).astype(int)
            y_pred_binary = (y_pred > 0).astype(int)
            tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
            fp = np.sum((y_true_binary == 0) & (y_pred_binary == 1))
            tn = np.sum((y_true_binary == 0) & (y_pred_binary == 0))
            fn = np.sum((y_true_binary == 1) & (y_pred_binary == 0))

            metrics['accuracy'] = float((tp + tn) / len(y_test)) if len(y_test) > 0 else 0
            metrics['precision'] = float(tp / (tp + fp)) if (tp + fp) > 0 else 0
            metrics['recall'] = float(tp / (tp + fn)) if (tp + fn) > 0 else 0
            metrics['f1_score'] = float(2 * metrics['precision'] * metrics['recall'] / (metrics['precision'] + metrics['recall'])) if (metrics['precision'] + metrics['recall']) > 0 else 0
            metrics['specificity'] = float(tn / (tn + fp)) if (tn + fp) > 0 else 0

            # Save results
            evaluation_results = {
                'model_type': model_data.get('model_type', 'unknown'),
                'n_test_samples': int(len(y_test)),
                'n_features': int(len(feature_names)),
                'metrics': metrics
            }

            with open(metrics_path, 'w') as f:
                json.dump(evaluation_results, f, indent=2)

            time.sleep(2)
            progress_bar.progress(100)

            status_text.text("Evaluation complete!")
            st.success("✅ Evaluation completed!")

            with st.expander("📋 Evaluation Output"):
                st.code(f"Test Samples: {len(y_test)}\nMAE: {metrics['mae']:.4f}\nRMSE: {metrics['rmse']:.4f}\nR²: {metrics['r2']:.4f}")

            st.rerun()

        except Exception as e:
            st.error(f"❌ Evaluation failed: {e}")


def show_evaluation_results():
    """Display evaluation metrics"""

    st.markdown("### 📊 Evaluation Metrics")

    metrics_path = Path('models/evaluation/evaluation_metrics.json')

    if not metrics_path.exists():
        st.info("ℹ️ No evaluation results available yet")
        return

    # Load metrics
    with open(metrics_path, 'r') as f:
        results = json.load(f)

    # Model info
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Model Type", results.get('model_type', 'N/A'))

    with col2:
        st.metric("Test Samples", results.get('n_test_samples', 'N/A'))

    with col3:
        st.metric("Features", results.get('n_features', 'N/A'))

    st.markdown("---")

    # Metrics
    metrics = results.get('metrics', {})

    # Regression metrics
    st.markdown("#### 📉 Regression Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        mae = metrics.get('mae', 0)
        st.metric("MAE", f"{mae:.2f}", help="Mean Absolute Error")

    with col2:
        rmse = metrics.get('rmse', 0)
        st.metric("RMSE", f"{rmse:.2f}", help="Root Mean Squared Error")

    with col3:
        r2 = metrics.get('r2', 0)
        st.metric("R²", f"{r2:.3f}", help="Coefficient of Determination")

    with col4:
        corr = metrics.get('correlation', 0)
        st.metric("Correlation", f"{corr:.3f}", help="Pearson Correlation")

    # Detection metrics
    st.markdown("---")
    st.markdown("#### 🎯 Detection Metrics (Outbreak Detection)")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        acc = metrics.get('accuracy', 0)
        st.metric("Accuracy", f"{acc:.3f}")

    with col2:
        prec = metrics.get('precision', 0)
        st.metric("Precision", f"{prec:.3f}")

    with col3:
        rec = metrics.get('recall', 0)
        st.metric("Recall", f"{rec:.3f}")

    with col4:
        f1 = metrics.get('f1_score', 0)
        st.metric("F1 Score", f"{f1:.3f}")

    with col5:
        spec = metrics.get('specificity', 0)
        st.metric("Specificity", f"{spec:.3f}")

    # Performance interpretation
    st.markdown("---")
    st.markdown("#### 💡 Performance Interpretation")

    r2 = metrics.get('r2', 0)

    if r2 >= 0.7:
        st.success("✅ **Excellent Performance**: Model explains >70% of variance")
    elif r2 >= 0.5:
        st.info("ℹ️ **Good Performance**: Model explains 50-70% of variance")
    elif r2 >= 0.3:
        st.warning("⚠️ **Moderate Performance**: Model explains 30-50% of variance")
    else:
        st.error("❌ **Poor Performance**: Model explains <30% of variance. Consider retraining.")

    # Detailed metrics table
    st.markdown("---")
    st.markdown("#### 📋 Detailed Metrics")

    metrics_df = pd.DataFrame([metrics])
    st.dataframe(metrics_df.T, use_container_width=True)


if __name__ == "__main__":
    show()
