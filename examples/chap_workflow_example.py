"""
CHAP Workflow Example for Cholera Early Warning System

This script demonstrates the complete workflow for using CHAP
with the Cholera Early Warning System for Zimbabwe.

Workflow Steps:
1. Data Harmonization - Prepare climate and health data
2. Model Training - Train CHAP-compatible model
3. Prediction - Generate forecasts
4. Evaluation - Assess model performance
5. Visualization - Create forecast visualizations

Note: This is an example with synthetic data. Replace with real data for actual use.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.chap_integration.data_harmonization import DataHarmonizer


def generate_synthetic_data():
    """
    Generate synthetic climate and health data for demonstration
    Replace this with real data loading for actual use
    """
    print("Generating synthetic data for demonstration...")

    # Time periods: 3 years of monthly data
    dates = pd.date_range('2020-01', '2022-12', freq='MS')
    time_periods = dates.strftime('%Y-%m').tolist()

    # Zimbabwe districts
    districts = [
        'Harare', 'Bulawayo', 'Manicaland', 'Mashonaland East',
        'Mashonaland West', 'Midlands', 'Masvingo'
    ]

    # Generate data
    data = []

    for district in districts:
        for i, time_period in enumerate(time_periods):
            # Seasonal rainfall pattern (higher in Nov-Mar)
            month = i % 12 + 1
            is_rainy_season = month in [11, 12, 1, 2, 3]

            rainfall = (
                np.random.exponential(100 if is_rainy_season else 20) +
                np.random.normal(0, 20)
            )

            temperature_mean = 20 + 5 * np.sin(2 * np.pi * i / 12) + np.random.normal(0, 2)

            temperature_max = temperature_mean + np.random.uniform(5, 10)
            temperature_min = temperature_mean - np.random.uniform(5, 10)

            humidity = 60 + 20 * (1 if is_rainy_season else 0) + np.random.normal(0, 10)

            # Cholera cases correlated with rainfall (with lag)
            base_cases = 0
            if i > 0:
                prev_rainfall = data[-1]['rainfall']
                base_cases = max(0, (prev_rainfall - 50) / 10)

            cholera_cases = max(0, np.random.poisson(base_cases))

            data.append({
                'time_period': time_period,
                'district': district,
                'rainfall': max(0, rainfall),
                'temperature_mean': temperature_mean,
                'temperature_max': temperature_max,
                'temperature_min': temperature_min,
                'humidity': max(0, min(100, humidity)),
                'cholera_cases': cholera_cases
            })

    df = pd.DataFrame(data)

    # Split into training and test sets
    cutoff_date = '2022-06'
    train_df = df[df['time_period'] < cutoff_date].copy()
    test_df = df[df['time_period'] >= cutoff_date].copy()

    # Split into health and climate for harmonization demo
    health_df = train_df[['time_period', 'district', 'cholera_cases']]
    climate_df = train_df[[
        'time_period', 'district', 'rainfall',
        'temperature_mean', 'temperature_max', 'temperature_min', 'humidity'
    ]]

    return health_df, climate_df, train_df, test_df


def step1_data_harmonization():
    """Step 1: Harmonize climate and health data"""
    print("\n" + "="*70)
    print("STEP 1: DATA HARMONIZATION")
    print("="*70)

    # Generate synthetic data
    health_df, climate_df, train_df, test_df = generate_synthetic_data()

    # Create data directory if it doesn't exist
    data_dir = Path('data/processed')
    data_dir.mkdir(parents=True, exist_ok=True)

    # Save raw data
    health_df.to_csv(data_dir / 'health_data_raw.csv', index=False)
    climate_df.to_csv(data_dir / 'climate_data_raw.csv', index=False)

    # Harmonize data
    harmonizer = DataHarmonizer()
    harmonized_df = harmonizer.harmonize(
        health_df,
        climate_df,
        output_path=data_dir / 'harmonized_training_data.csv'
    )

    # Save test data
    test_df.to_csv(data_dir / 'test_data.csv', index=False)

    print(f"\n✓ Harmonized data saved to {data_dir / 'harmonized_training_data.csv'}")

    return harmonized_df, test_df


def step2_model_training():
    """Step 2: Train CHAP-compatible model"""
    print("\n" + "="*70)
    print("STEP 2: MODEL TRAINING")
    print("="*70)

    # Create models directory
    models_dir = Path('models/trained')
    models_dir.mkdir(parents=True, exist_ok=True)

    # Training command
    cmd = [
        'python', 'src/chap_integration/chap_train.py',
        'data/processed/harmonized_training_data.csv',
        'models/trained/cholera_model.pkl',
        '--config', 'config/chap_config.yaml'
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode == 0:
        print(f"\n✓ Model trained and saved to models/trained/cholera_model.pkl")
    else:
        print(f"\n✗ Training failed with error code {result.returncode}")

    return result.returncode == 0


def step3_generate_predictions():
    """Step 3: Generate predictions"""
    print("\n" + "="*70)
    print("STEP 3: GENERATE PREDICTIONS")
    print("="*70)

    # Create outputs directory
    outputs_dir = Path('outputs/forecasts')
    outputs_dir.mkdir(parents=True, exist_ok=True)

    # For prediction, we need historical data and future climate data
    # In this example, we'll use test data as "future" climate data
    test_df = pd.read_csv('data/processed/test_data.csv')
    historic_df = pd.read_csv('data/processed/harmonized_training_data.csv')

    # Save future climate data (without cholera_cases)
    future_climate = test_df.drop(columns=['cholera_cases'])
    future_climate.to_csv('data/processed/future_climate.csv', index=False)

    # Prediction command
    cmd = [
        'python', 'src/chap_integration/chap_predict.py',
        'models/trained/cholera_model.pkl',
        'data/processed/harmonized_training_data.csv',
        'data/processed/future_climate.csv',
        'outputs/forecasts/cholera_predictions.csv'
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode == 0:
        print(f"\n✓ Predictions saved to outputs/forecasts/cholera_predictions.csv")
    else:
        print(f"\n✗ Prediction failed with error code {result.returncode}")

    return result.returncode == 0


def step4_model_evaluation():
    """Step 4: Evaluate model performance"""
    print("\n" + "="*70)
    print("STEP 4: MODEL EVALUATION")
    print("="*70)

    # Create evaluation directory
    eval_dir = Path('models/evaluation')
    eval_dir.mkdir(parents=True, exist_ok=True)

    # Evaluation command
    cmd = [
        'python', 'src/chap_integration/chap_evaluate.py',
        'models/trained/cholera_model.pkl',
        'data/processed/test_data.csv',
        'models/evaluation/evaluation_metrics.json'
    ]

    print(f"\nRunning: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode == 0:
        print(f"\n✓ Evaluation metrics saved to models/evaluation/evaluation_metrics.json")
    else:
        print(f"\n✗ Evaluation failed with error code {result.returncode}")

    return result.returncode == 0


def step5_visualization():
    """Step 5: Visualize predictions"""
    print("\n" + "="*70)
    print("STEP 5: VISUALIZATION")
    print("="*70)

    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates

        # Load predictions
        predictions_df = pd.read_csv('outputs/forecasts/cholera_predictions.csv')

        # Load test data for comparison
        test_df = pd.read_csv('data/processed/test_data.csv')

        # Merge for comparison
        comparison_df = pd.merge(
            predictions_df,
            test_df[['time_period', 'district', 'cholera_cases']],
            on=['time_period', 'district'],
            how='left'
        )

        # Convert time_period to datetime for plotting
        comparison_df['date'] = pd.to_datetime(comparison_df['time_period'])

        # Create visualization for each district
        districts = comparison_df['district'].unique()[:3]  # First 3 districts

        fig, axes = plt.subplots(len(districts), 1, figsize=(12, 4*len(districts)))
        if len(districts) == 1:
            axes = [axes]

        for idx, district in enumerate(districts):
            district_data = comparison_df[comparison_df['district'] == district].sort_values('date')

            ax = axes[idx]

            # Plot actual cases
            ax.plot(
                district_data['date'],
                district_data['cholera_cases'],
                'o-',
                label='Actual Cases',
                color='red',
                linewidth=2
            )

            # Plot predicted mean
            ax.plot(
                district_data['date'],
                district_data['mean_prediction'],
                's-',
                label='Predicted Mean',
                color='blue',
                linewidth=2
            )

            # Plot prediction interval
            ax.fill_between(
                district_data['date'],
                district_data['q025_prediction'],
                district_data['q975_prediction'],
                alpha=0.3,
                color='blue',
                label='95% Prediction Interval'
            )

            ax.set_title(f'Cholera Forecasts - {district}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Time Period')
            ax.set_ylabel('Cholera Cases')
            ax.legend(loc='upper right')
            ax.grid(True, alpha=0.3)

            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        plt.tight_layout()

        # Save figure
        output_path = 'outputs/forecasts/cholera_forecast_visualization.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Visualization saved to {output_path}")

        plt.close()

    except ImportError:
        print("\n⚠ Matplotlib not available for visualization")
    except Exception as e:
        print(f"\n⚠ Visualization failed: {e}")


def main():
    """
    Run complete CHAP workflow
    """
    print("\n" + "="*70)
    print("CHAP WORKFLOW FOR CHOLERA EARLY WARNING SYSTEM")
    print("Zimbabwe and Southern Africa")
    print("="*70)

    # Run workflow steps
    try:
        # Step 1: Data Harmonization
        harmonized_df, test_df = step1_data_harmonization()

        # Step 2: Model Training
        training_success = step2_model_training()
        if not training_success:
            print("\n✗ Workflow stopped due to training failure")
            return

        # Step 3: Generate Predictions
        prediction_success = step3_generate_predictions()
        if not prediction_success:
            print("\n✗ Workflow stopped due to prediction failure")
            return

        # Step 4: Model Evaluation
        evaluation_success = step4_model_evaluation()

        # Step 5: Visualization
        step5_visualization()

        # Summary
        print("\n" + "="*70)
        print("WORKFLOW COMPLETE!")
        print("="*70)
        print("\nGenerated Files:")
        print("  - data/processed/harmonized_training_data.csv")
        print("  - models/trained/cholera_model.pkl")
        print("  - outputs/forecasts/cholera_predictions.csv")
        print("  - models/evaluation/evaluation_metrics.json")
        print("  - outputs/forecasts/cholera_forecast_visualization.png")
        print("\nNext Steps:")
        print("  1. Review evaluation metrics in models/evaluation/")
        print("  2. Examine predictions in outputs/forecasts/")
        print("  3. Use CHAP CLI for advanced operations:")
        print("     chap evaluate --model-name models/trained/cholera_model.pkl")
        print("\n")

    except Exception as e:
        print(f"\n✗ Workflow failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
