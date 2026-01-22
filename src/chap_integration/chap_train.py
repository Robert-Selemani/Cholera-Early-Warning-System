"""
CHAP-Compatible Training Script for Cholera Early Warning System

This script trains a cholera prediction model using climate and epidemiological data
following CHAP (Climate and Health Analysis Platform) conventions.

Usage:
    python chap_train.py <train_data_csv> <output_model_path> [--config <config_file>]

Expected CSV columns:
    - time_period: Date or time period identifier
    - district: District name or code
    - rainfall: Rainfall amount (mm)
    - temperature_mean: Mean temperature (°C)
    - temperature_max: Maximum temperature (°C)
    - temperature_min: Minimum temperature (°C)
    - humidity: Relative humidity (%)
    - cholera_cases: Number of cholera cases (target variable)
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import yaml
import sys
from pathlib import Path


def load_config(config_path):
    """Load CHAP configuration file"""
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def prepare_features(df, config):
    """
    Prepare features for training

    Args:
        df: DataFrame with raw data
        config: Configuration dictionary

    Returns:
        X: Feature matrix
        y: Target vector
        feature_names: List of feature names
    """
    # Define climate and environmental features
    climate_features = [
        'rainfall',
        'temperature_mean',
        'temperature_max',
        'temperature_min',
        'humidity'
    ]

    # Filter to only available features
    available_features = [f for f in climate_features if f in df.columns]

    if not available_features:
        raise ValueError(
            f"No climate features found in data. Expected: {climate_features}"
        )

    # Create lag features if configured
    lag_periods = config.get('lag_periods', [1, 2, 4])

    # Add lag features
    for feature in available_features:
        for lag in lag_periods:
            lag_col = f'{feature}_lag_{lag}'
            df[lag_col] = df.groupby('district')[feature].shift(lag)
            available_features.append(lag_col)

    # Drop rows with NaN values created by lagging
    df = df.dropna()

    # Extract features and target
    X = df[available_features].values
    y = df['cholera_cases'].fillna(0).values

    return X, y, available_features


def train_model(train_data_path, output_model_path, config_path=None):
    """
    Train cholera prediction model

    Args:
        train_data_path: Path to training data CSV
        output_model_path: Path to save trained model
        config_path: Path to configuration file
    """
    print(f"Loading training data from {train_data_path}")
    df = pd.read_csv(train_data_path)

    # Load configuration
    config = load_config(config_path)
    model_type = config.get('model_type', 'random_forest')

    print(f"Preparing features...")
    X, y, feature_names = prepare_features(df, config)

    print(f"Training {model_type} model with {X.shape[0]} samples and {X.shape[1]} features")

    # Select model based on configuration
    if model_type == 'random_forest':
        estimator = RandomForestRegressor(
            n_estimators=config.get('n_estimators', 100),
            max_depth=config.get('max_depth', 10),
            min_samples_split=config.get('min_samples_split', 5),
            random_state=config.get('random_state', 42),
            n_jobs=-1
        )
    elif model_type == 'gradient_boosting':
        estimator = GradientBoostingRegressor(
            n_estimators=config.get('n_estimators', 100),
            max_depth=config.get('max_depth', 5),
            learning_rate=config.get('learning_rate', 0.1),
            random_state=config.get('random_state', 42)
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")

    # Create pipeline with scaling
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', estimator)
    ])

    # Train model
    pipeline.fit(X, y)

    # Save model and metadata
    model_data = {
        'pipeline': pipeline,
        'feature_names': feature_names,
        'model_type': model_type,
        'config': config
    }

    print(f"Saving trained model to {output_model_path}")
    joblib.dump(model_data, output_model_path)

    print("Training completed successfully")

    # Print feature importance if available
    if hasattr(pipeline.named_steps['model'], 'feature_importances_'):
        importances = pipeline.named_steps['model'].feature_importances_
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)

        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10).to_string(index=False))


def main():
    parser = argparse.ArgumentParser(
        description='Train CHAP-compatible cholera prediction model'
    )
    parser.add_argument(
        'train_data',
        type=str,
        help='Path to training data CSV file'
    )
    parser.add_argument(
        'model',
        type=str,
        help='Path to save the trained model'
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Path to CHAP configuration file'
    )

    args = parser.parse_args()

    try:
        train_model(args.train_data, args.model, args.config)
    except Exception as e:
        print(f"Error during training: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
