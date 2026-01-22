"""
CHAP-Compatible Prediction Script for Cholera Early Warning System

This script generates cholera case predictions using a trained model
and future climate data, following CHAP conventions.

Usage:
    python chap_predict.py <model_path> <historic_data_csv> <future_data_csv> <output_csv>

Output Format:
    The predictions are saved as a CSV file with probabilistic forecasts
    (multiple samples representing uncertainty) following CHAP conventions.
"""

import argparse
import pandas as pd
import numpy as np
import joblib
import sys
from pathlib import Path


def prepare_prediction_features(historic_df, future_df, feature_names, config):
    """
    Prepare features for prediction using historic and future data

    Args:
        historic_df: DataFrame with historical data for creating lags
        future_df: DataFrame with future climate data
        feature_names: List of feature names from training
        config: Configuration dictionary

    Returns:
        X: Feature matrix for prediction
        prediction_df: DataFrame with time periods and districts
    """
    # Combine historic and future data for lag calculation
    combined_df = pd.concat([historic_df, future_df], ignore_index=True)

    # Sort by district and time
    combined_df = combined_df.sort_values(['district', 'time_period'])

    # Extract lag configuration
    lag_periods = config.get('lag_periods', [1, 2, 4])

    # Base climate features (without lag)
    base_features = [
        'rainfall',
        'temperature_mean',
        'temperature_max',
        'temperature_min',
        'humidity'
    ]

    # Create lag features
    for feature in base_features:
        if feature in combined_df.columns:
            for lag in lag_periods:
                lag_col = f'{feature}_lag_{lag}'
                combined_df[lag_col] = combined_df.groupby('district')[feature].shift(lag)

    # Filter to only future periods
    future_start_idx = len(historic_df)
    prediction_df = combined_df.iloc[future_start_idx:].copy()

    # Extract features in the same order as training
    available_features = [f for f in feature_names if f in prediction_df.columns]

    if len(available_features) != len(feature_names):
        missing = set(feature_names) - set(available_features)
        print(f"Warning: Missing features: {missing}")

    # Drop rows with NaN (from lagging)
    prediction_df = prediction_df.dropna(subset=available_features)

    X = prediction_df[available_features].values

    return X, prediction_df[['time_period', 'district']].reset_index(drop=True)


def generate_probabilistic_predictions(model, X, n_samples=100):
    """
    Generate probabilistic predictions

    Args:
        model: Trained model pipeline
        X: Feature matrix
        n_samples: Number of prediction samples for uncertainty quantification

    Returns:
        predictions: Array of shape (n_rows, n_samples) with probabilistic predictions
    """
    # Get base predictions
    base_predictions = model.predict(X)

    # Estimate prediction uncertainty
    # For tree-based models, we can use predictions from individual trees
    estimator = model.named_steps['model']

    if hasattr(estimator, 'estimators_'):
        # Random Forest or Gradient Boosting - use tree predictions for uncertainty
        tree_predictions = []

        for tree in estimator.estimators_[:min(n_samples, len(estimator.estimators_))]:
            if hasattr(tree, 'predict'):
                # Random Forest
                tree_pred = tree.predict(model.named_steps['scaler'].transform(X))
            else:
                # Gradient Boosting (need to use staged_predict)
                continue

            tree_predictions.append(tree_pred)

        if tree_predictions:
            predictions = np.array(tree_predictions).T
        else:
            # Fallback: use normal distribution around base prediction
            std_dev = np.std(base_predictions) * 0.2  # Assume 20% coefficient of variation
            predictions = np.random.normal(
                base_predictions[:, np.newaxis],
                std_dev,
                size=(len(base_predictions), n_samples)
            )
    else:
        # Fallback for other models
        std_dev = np.std(base_predictions) * 0.2
        predictions = np.random.normal(
            base_predictions[:, np.newaxis],
            std_dev,
            size=(len(base_predictions), n_samples)
        )

    # Ensure non-negative predictions (cholera cases can't be negative)
    predictions = np.maximum(predictions, 0)

    return predictions


def predict(model_path, historic_data_path, future_data_path, output_path):
    """
    Generate predictions using trained model

    Args:
        model_path: Path to trained model file
        historic_data_path: Path to historical data CSV
        future_data_path: Path to future climate data CSV
        output_path: Path to save predictions CSV
    """
    print(f"Loading model from {model_path}")
    model_data = joblib.load(model_path)

    pipeline = model_data['pipeline']
    feature_names = model_data['feature_names']
    config = model_data.get('config', {})

    print(f"Loading historical data from {historic_data_path}")
    historic_df = pd.read_csv(historic_data_path)

    print(f"Loading future climate data from {future_data_path}")
    future_df = pd.read_csv(future_data_path)

    print("Preparing prediction features...")
    X, meta_df = prepare_prediction_features(
        historic_df, future_df, feature_names, config
    )

    print(f"Generating predictions for {len(X)} time periods...")
    n_samples = config.get('prediction_samples', 100)
    predictions = generate_probabilistic_predictions(pipeline, X, n_samples)

    # Create output DataFrame in CHAP format
    output_df = meta_df.copy()

    # Add probabilistic predictions as separate columns
    for i in range(min(predictions.shape[1], 100)):  # Limit to 100 samples
        output_df[f'sample_{i}'] = predictions[:, i]

    # Add summary statistics
    output_df['mean_prediction'] = np.mean(predictions, axis=1)
    output_df['median_prediction'] = np.median(predictions, axis=1)
    output_df['std_prediction'] = np.std(predictions, axis=1)
    output_df['q025_prediction'] = np.percentile(predictions, 2.5, axis=1)
    output_df['q975_prediction'] = np.percentile(predictions, 97.5, axis=1)

    print(f"Saving predictions to {output_path}")
    output_df.to_csv(output_path, index=False)

    print("Prediction completed successfully")

    # Print summary
    print(f"\nPrediction Summary:")
    print(f"  Total predictions: {len(output_df)}")
    print(f"  Mean predicted cases: {output_df['mean_prediction'].mean():.2f}")
    print(f"  Median predicted cases: {output_df['median_prediction'].median():.2f}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate CHAP-compatible cholera predictions'
    )
    parser.add_argument(
        'model',
        type=str,
        help='Path to trained model file'
    )
    parser.add_argument(
        'historic_data',
        type=str,
        help='Path to historical data CSV'
    )
    parser.add_argument(
        'future_data',
        type=str,
        help='Path to future climate data CSV'
    )
    parser.add_argument(
        'out_file',
        type=str,
        help='Path to save predictions CSV'
    )

    args = parser.parse_args()

    try:
        predict(args.model, args.historic_data, args.future_data, args.out_file)
    except Exception as e:
        print(f"Error during prediction: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
