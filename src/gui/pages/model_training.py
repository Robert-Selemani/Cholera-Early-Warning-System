"""
Model Training Page - Train and Configure CHAP Models
"""

import streamlit as st
import subprocess
import yaml
from pathlib import Path


def show():
    """Display model training interface"""

    st.markdown('<h2 class="section-header">🧮 Model Training</h2>', unsafe_allow_html=True)

    # Check for training data
    train_data_path = Path('data/processed/harmonized_data.csv')

    if not train_data_path.exists():
        st.warning("⚠️ No training data found. Please harmonize data first.")
        if st.button("Go to Data Management"):
            st.switch_page("pages/data_management.py")
        return

    # Model configuration
    st.markdown("### ⚙️ Model Configuration")

    col1, col2 = st.columns(2)

    with col1:
        model_type = st.selectbox(
            "Model Type",
            ['random_forest', 'gradient_boosting'],
            help="Select the machine learning algorithm"
        )

        n_estimators = st.slider(
            "Number of Estimators",
            min_value=50,
            max_value=500,
            value=200,
            step=50,
            help="Number of trees in the forest"
        )

        max_depth = st.slider(
            "Maximum Depth",
            min_value=5,
            max_value=30,
            value=15,
            step=5,
            help="Maximum depth of trees"
        )

    with col2:
        st.markdown("#### Lag Periods (months)")
        lag_1 = st.checkbox("1 month", value=True)
        lag_2 = st.checkbox("2 months", value=True)
        lag_4 = st.checkbox("4 months (seasonal)", value=True)
        lag_8 = st.checkbox("8 months", value=False)

        # Build lag periods list
        lag_periods = []
        if lag_1: lag_periods.append(1)
        if lag_2: lag_periods.append(2)
        if lag_4: lag_periods.append(4)
        if lag_8: lag_periods.append(8)

        random_state = st.number_input(
            "Random State",
            min_value=0,
            max_value=999,
            value=42,
            help="Seed for reproducibility"
        )

    # Additional settings
    st.markdown("---")
    st.markdown("### 📋 Training Settings")

    col1, col2 = st.columns(2)

    with col1:
        model_name = st.text_input(
            "Model Name",
            value="cholera_model",
            help="Name for the trained model file"
        )

    with col2:
        prediction_samples = st.number_input(
            "Prediction Samples",
            min_value=10,
            max_value=1000,
            value=100,
            help="Number of samples for uncertainty quantification"
        )

    # Save configuration
    config = {
        'model_type': model_type,
        'n_estimators': n_estimators,
        'max_depth': max_depth,
        'lag_periods': lag_periods,
        'random_state': random_state,
        'prediction_samples': prediction_samples
    }

    # Display configuration
    with st.expander("📄 View Configuration"):
        st.json(config)

    st.markdown("---")

    # Training controls
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("🚀 Start Training", type="primary", use_container_width=True):
            train_model(train_data_path, model_name, config)

    with col2:
        if st.button("💾 Save Config", use_container_width=True):
            save_configuration(config)

    with col3:
        if st.button("📥 Load Config", use_container_width=True):
            load_configuration()

    # Training history
    st.markdown("---")
    st.markdown("### 📊 Training History")

    show_training_history()


def train_model(train_data_path, model_name, config):
    """Train the model"""

    # Save temporary config
    config_path = Path('config/temp_config.yaml')
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    model_path = Path(f'models/trained/{model_name}.pkl')
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Training command
    cmd = [
        'python', 'src/chap_integration/chap_train.py',
        str(train_data_path),
        str(model_path),
        '--config', str(config_path)
    ]

    with st.spinner("🔄 Training model... This may take a few minutes."):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )

            st.success("✅ Model training completed successfully!")

            # Show output
            with st.expander("📋 Training Output"):
                st.code(result.stdout)

            # Show model info
            st.info(f"📁 Model saved to: `{model_path}`")

        except subprocess.CalledProcessError as e:
            st.error(f"❌ Training failed!")
            st.code(e.stderr)


def save_configuration(config):
    """Save configuration"""
    config_path = Path('config/chap_config.yaml')

    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    st.success(f"✅ Configuration saved to {config_path}")


def load_configuration():
    """Load configuration"""
    config_path = Path('config/chap_config.yaml')

    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        st.success("✅ Configuration loaded")
        st.json(config)
    else:
        st.warning("⚠️ No saved configuration found")


def show_training_history():
    """Show training history"""

    models_dir = Path('models/trained')

    if not models_dir.exists():
        st.info("ℹ️ No trained models yet")
        return

    model_files = list(models_dir.glob('*.pkl'))

    if not model_files:
        st.info("ℹ️ No trained models yet")
        return

    # Display models
    import pandas as pd

    models_data = []
    for model_file in model_files:
        stat = model_file.stat()
        models_data.append({
            'Model Name': model_file.stem,
            'File Size': f"{stat.st_size / 1024:.1f} KB",
            'Created': pd.Timestamp.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
        })

    df = pd.DataFrame(models_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    show()
