"""
Evaluation Page - Model Performance Metrics
"""

import streamlit as st
import pandas as pd
import json
import subprocess
from pathlib import Path


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

    cmd = [
        'python', 'src/chap_integration/chap_evaluate.py',
        str(model_path),
        test_data_path,
        str(metrics_path)
    ]

    with st.spinner("🔄 Evaluating model..."):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)

            st.success("✅ Evaluation completed!")

            with st.expander("📋 Evaluation Output"):
                st.code(result.stdout)

            st.rerun()

        except subprocess.CalledProcessError as e:
            st.error("❌ Evaluation failed!")
            st.code(e.stderr)


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
