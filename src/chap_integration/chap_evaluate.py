"""
CHAP-Compatible Evaluation Script for Cholera Early Warning System

This script evaluates model performance using CHAP-standard metrics
for disease forecasting evaluation.

Usage:
    python chap_evaluate.py <model_path> <test_data_csv> <metrics_output_path>
"""

import argparse
import pandas as pd
import numpy as np
import joblib
import json
import sys
from pathlib import Path
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)


def prepare_test_features(df, feature_names, config):
    """
    Prepare features for evaluation

    Args:
        df: DataFrame with test data
        feature_names: List of feature names from training
        config: Configuration dictionary

    Returns:
        X: Feature matrix
        y: True target values
    """
    # Extract lag configuration
    lag_periods = config.get('lag_periods', [1, 2, 4])

    # Sort by district and time
    df = df.sort_values(['district', 'time_period'])

    # Base climate features
    base_features = [
        'rainfall',
        'temperature_mean',
        'temperature_max',
        'temperature_min',
        'humidity'
    ]

    # Create lag features
    for feature in base_features:
        if feature in df.columns:
            for lag in lag_periods:
                lag_col = f'{feature}_lag_{lag}'
                df[lag_col] = df.groupby('district')[feature].shift(lag)

    # Drop rows with NaN
    df = df.dropna()

    # Extract features and target
    X = df[feature_names].values
    y = df['cholera_cases'].fillna(0).values

    return X, y


def calculate_metrics(y_true, y_pred):
    """
    Calculate comprehensive evaluation metrics

    Args:
        y_true: True values
        y_pred: Predicted values

    Returns:
        Dictionary of metrics
    """
    metrics = {}

    # Regression metrics
    metrics['mae'] = mean_absolute_error(y_true, y_pred)
    metrics['rmse'] = np.sqrt(mean_squared_error(y_true, y_pred))
    metrics['r2'] = r2_score(y_true, y_pred)

    # MAPE (with protection against division by zero)
    non_zero_mask = y_true > 0
    if non_zero_mask.sum() > 0:
        metrics['mape'] = mean_absolute_percentage_error(
            y_true[non_zero_mask],
            y_pred[non_zero_mask]
        )
    else:
        metrics['mape'] = None

    # Correlation
    metrics['correlation'] = np.corrcoef(y_true, y_pred)[0, 1]

    # Bias
    metrics['bias'] = np.mean(y_pred - y_true)

    # Detection metrics (treating >0 cases as outbreak)
    y_true_binary = (y_true > 0).astype(int)
    y_pred_binary = (y_pred > 0).astype(int)

    # True Positives, False Positives, True Negatives, False Negatives
    tp = np.sum((y_true_binary == 1) & (y_pred_binary == 1))
    fp = np.sum((y_true_binary == 0) & (y_pred_binary == 1))
    tn = np.sum((y_true_binary == 0) & (y_pred_binary == 0))
    fn = np.sum((y_true_binary == 1) & (y_pred_binary == 0))

    # Detection metrics
    metrics['accuracy'] = (tp + tn) / len(y_true) if len(y_true) > 0 else 0
    metrics['precision'] = tp / (tp + fp) if (tp + fp) > 0 else 0
    metrics['recall'] = tp / (tp + fn) if (tp + fn) > 0 else 0
    metrics['f1_score'] = (
        2 * metrics['precision'] * metrics['recall'] /
        (metrics['precision'] + metrics['recall'])
        if (metrics['precision'] + metrics['recall']) > 0 else 0
    )

    # Specificity
    metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0

    return metrics


def evaluate(model_path, test_data_path, metrics_output_path):
    """
    Evaluate model performance

    Args:
        model_path: Path to trained model file
        test_data_path: Path to test data CSV
        metrics_output_path: Path to save evaluation metrics
    """
    print(f"Loading model from {model_path}")
    model_data = joblib.load(model_path)

    pipeline = model_data['pipeline']
    feature_names = model_data['feature_names']
    config = model_data.get('config', {})

    print(f"Loading test data from {test_data_path}")
    test_df = pd.read_csv(test_data_path)

    print("Preparing test features...")
    X_test, y_test = prepare_test_features(test_df, feature_names, config)

    print(f"Generating predictions for {len(X_test)} samples...")
    y_pred = pipeline.predict(X_test)

    print("Calculating metrics...")
    metrics = calculate_metrics(y_test, y_pred)

    # Add metadata
    evaluation_results = {
        'model_type': model_data.get('model_type', 'unknown'),
        'n_test_samples': len(y_test),
        'n_features': len(feature_names),
        'metrics': metrics
    }

    # Save metrics
    print(f"Saving metrics to {metrics_output_path}")

    # Save as JSON
    with open(metrics_output_path, 'w') as f:
        json.dump(evaluation_results, f, indent=2)

    # Also save as CSV for easy viewing
    csv_path = Path(metrics_output_path).with_suffix('.csv')
    metrics_df = pd.DataFrame([metrics])
    metrics_df.to_csv(csv_path, index=False)

    print("\nEvaluation Metrics:")
    print("=" * 50)
    print(f"  Model Type: {evaluation_results['model_type']}")
    print(f"  Test Samples: {evaluation_results['n_test_samples']}")
    print(f"  Features: {evaluation_results['n_features']}")
    print("\nRegression Metrics:")
    print(f"  MAE:  {metrics['mae']:.4f}")
    print(f"  RMSE: {metrics['rmse']:.4f}")
    print(f"  R²:   {metrics['r2']:.4f}")
    if metrics['mape'] is not None:
        print(f"  MAPE: {metrics['mape']:.4f}")
    print(f"  Correlation: {metrics['correlation']:.4f}")
    print(f"  Bias: {metrics['bias']:.4f}")
    print("\nDetection Metrics (outbreak vs no outbreak):")
    print(f"  Accuracy:    {metrics['accuracy']:.4f}")
    print(f"  Precision:   {metrics['precision']:.4f}")
    print(f"  Recall:      {metrics['recall']:.4f}")
    print(f"  F1 Score:    {metrics['f1_score']:.4f}")
    print(f"  Specificity: {metrics['specificity']:.4f}")

    print("\nEvaluation completed successfully")


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate CHAP-compatible cholera prediction model'
    )
    parser.add_argument(
        'model',
        type=str,
        help='Path to trained model file'
    )
    parser.add_argument(
        'test_data',
        type=str,
        help='Path to test data CSV'
    )
    parser.add_argument(
        'metrics_file',
        type=str,
        help='Path to save evaluation metrics'
    )

    args = parser.parse_args()

    try:
        evaluate(args.model, args.test_data, args.metrics_file)
    except Exception as e:
        print(f"Error during evaluation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
