# CHAP Usage Guide
## Climate and Health Analysis Platform for Cholera Early Warning

This guide provides detailed instructions for using CHAP (Climate and Health Analysis Platform) with the Cholera Early Warning System for Zimbabwe and Southern Africa.

## Table of Contents
1. [Overview](#overview)
2. [Data Preparation](#data-preparation)
3. [Model Training](#model-training)
4. [Generating Predictions](#generating-predictions)
5. [Model Evaluation](#model-evaluation)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

## Overview

CHAP is an open-source platform for climate-health modeling that provides:
- **Standardized Data Pipelines**: Automated harmonization of climate and health data
- **Model Orchestration**: Framework for training and deploying predictive models
- **Hyperparameter Tuning**: Automated optimization of model parameters
- **DHIS2 Integration**: Native connection to national health information systems
- **Rigorous Evaluation**: Comprehensive validation metrics

### Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Climate Data  │────▶│  Harmonization   │────▶│  CHAP Models    │
│   (CHIRPS, ERA5)│     │   (by Region/    │     │  (Random Forest,│
└─────────────────┘     │    Time Period)  │     │   Gradient Boost)│
                         └──────────────────┘     └─────────────────┘
┌─────────────────┐             │                        │
│   Health Data   │─────────────┘                        ▼
│ (DHIS2, IDSR)   │                              ┌─────────────────┐
└─────────────────┘                              │  Probabilistic  │
                                                  │   Predictions   │
                                                  └─────────────────┘
                                                          │
                                                          ▼
                                                  ┌─────────────────┐
                                                  │   Evaluation &  │
                                                  │   Visualization │
                                                  └─────────────────┘
```

## Data Preparation

### Required Data Format

CHAP expects harmonized data in CSV format with the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `time_period` | string | Year-month format | `2023-01` |
| `district` | string | District name | `Harare` |
| `rainfall` | float | Rainfall in mm | `125.5` |
| `temperature_mean` | float | Mean temperature °C | `22.3` |
| `temperature_max` | float | Max temperature °C | `28.5` |
| `temperature_min` | float | Min temperature °C | `16.2` |
| `humidity` | float | Relative humidity % | `65.0` |
| `cholera_cases` | int | Cholera case count | `12` |

### Data Harmonization

Use the `DataHarmonizer` class to prepare your data:

```python
from src.chap_integration.data_harmonization import DataHarmonizer
import pandas as pd

# Load raw data
health_df = pd.read_csv('data/raw/cholera_cases.csv')
climate_df = pd.read_csv('data/raw/climate_data.csv')

# Initialize harmonizer
harmonizer = DataHarmonizer()

# Harmonize data
harmonized_df = harmonizer.harmonize(
    health_df,
    climate_df,
    output_path='data/processed/harmonized_data.csv'
)
```

### Data Sources for Zimbabwe

**Climate Data:**
- **CHIRPS**: Climate Hazards Group InfraRed Precipitation with Station data
- **ERA5**: European Centre for Medium-Range Weather Forecasts reanalysis
- **Zimbabwe Met Services**: Local weather station data
- **DHIS2 Climate Data App**: https://dhis2.org/climate/climate-data-app/

**Health Data:**
- **DHIS2**: District Health Information System 2
- **IDSR**: Integrated Disease Surveillance and Response reports
- **Ministry of Health and Child Care**: Cholera surveillance data

**Geospatial Data:**
- **ZINGSA GeoPortal**: https://zimgeoportal.org.zw/
- **GADM**: Administrative boundaries
- **WorldPop**: Population density estimates

## Model Training

### Configuration

Edit `config/chap_config.yaml` to customize model settings:

```yaml
model_type: random_forest
n_estimators: 200
max_depth: 15
lag_periods: [1, 2, 4, 8]
```

### Training Command

```bash
python src/chap_integration/chap_train.py \
  data/processed/harmonized_data.csv \
  models/trained/cholera_model.pkl \
  --config config/chap_config.yaml
```

### Training Output

The training script will:
1. Load and validate the training data
2. Create lag features for temporal patterns
3. Train the specified model (Random Forest or Gradient Boosting)
4. Save the trained model with metadata
5. Display feature importance rankings

Example output:
```
Loading training data from data/processed/harmonized_data.csv
Preparing features...
Training random_forest model with 2450 samples and 24 features
Saving trained model to models/trained/cholera_model.pkl
Training completed successfully

Top 10 Most Important Features:
                    feature  importance
         rainfall_lag_1        0.185
    temperature_mean_lag_2    0.142
                  rainfall    0.128
         rainfall_lag_2        0.115
            humidity_lag_1    0.098
...
```

## Generating Predictions

### Prediction Input Requirements

Predictions require:
1. **Trained model**: Output from training step
2. **Historical data**: Past observations for lag feature calculation
3. **Future climate data**: Forecasted or projected climate variables

### Prediction Command

```bash
python src/chap_integration/chap_predict.py \
  models/trained/cholera_model.pkl \
  data/processed/historical_data.csv \
  data/processed/future_climate.csv \
  outputs/forecasts/predictions.csv
```

### Prediction Output

The output CSV contains probabilistic predictions:

| Column | Description |
|--------|-------------|
| `time_period` | Forecast period |
| `district` | District name |
| `sample_0` to `sample_99` | Individual prediction samples |
| `mean_prediction` | Mean of all samples |
| `median_prediction` | Median of all samples |
| `std_prediction` | Standard deviation |
| `q025_prediction` | 2.5th percentile (lower bound of 95% CI) |
| `q975_prediction` | 97.5th percentile (upper bound of 95% CI) |

### Interpreting Predictions

```python
import pandas as pd

# Load predictions
predictions = pd.read_csv('outputs/forecasts/predictions.csv')

# High-risk districts (mean prediction > 50 cases)
high_risk = predictions[predictions['mean_prediction'] > 50]

# Districts with high uncertainty
uncertain = predictions[predictions['std_prediction'] > 20]

# Visualize for a specific district
harare = predictions[predictions['district'] == 'Harare']
print(harare[['time_period', 'mean_prediction', 'q025_prediction', 'q975_prediction']])
```

## Model Evaluation

### Evaluation Command

```bash
python src/chap_integration/chap_evaluate.py \
  models/trained/cholera_model.pkl \
  data/processed/test_data.csv \
  models/evaluation/metrics.json
```

### Evaluation Metrics

The evaluation produces:

**Regression Metrics:**
- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Squared Error
- **R²**: Coefficient of determination
- **MAPE**: Mean Absolute Percentage Error
- **Correlation**: Pearson correlation coefficient
- **Bias**: Average prediction bias

**Detection Metrics** (outbreak vs no outbreak):
- **Accuracy**: Overall correct predictions
- **Precision**: Positive predictive value
- **Recall**: Sensitivity
- **F1 Score**: Harmonic mean of precision and recall
- **Specificity**: True negative rate

### Example Metrics Output

```json
{
  "model_type": "random_forest",
  "n_test_samples": 490,
  "n_features": 24,
  "metrics": {
    "mae": 8.45,
    "rmse": 12.32,
    "r2": 0.68,
    "correlation": 0.83,
    "accuracy": 0.78,
    "precision": 0.72,
    "recall": 0.81,
    "f1_score": 0.76
  }
}
```

## Advanced Features

### Using MLflow for Experiment Tracking

CHAP integrates with MLflow for tracking experiments:

```python
import mlflow

# Start MLflow tracking
mlflow.set_tracking_uri("./mlruns")
mlflow.set_experiment("cholera_early_warning_zimbabwe")

# Train with MLflow tracking
with mlflow.start_run():
    mlflow.log_param("model_type", "random_forest")
    mlflow.log_param("n_estimators", 200)

    # Train model...

    mlflow.log_metric("mae", 8.45)
    mlflow.log_metric("r2", 0.68)
```

### Hyperparameter Tuning

CHAP provides built-in hyperparameter optimization:

```bash
chap evaluate-hpo \
  --train-data data/processed/harmonized_data.csv \
  --do-hpo true \
  --n-trials 50
```

### DHIS2 Integration

To integrate with DHIS2 for data retrieval:

```yaml
# config/chap_config.yaml
dhis2:
  enabled: true
  server_url: https://your-dhis2-instance.org
  api_version: 39
  credentials_file: .env
```

Create `.env` file:
```
DHIS2_USERNAME=your_username
DHIS2_PASSWORD=your_password
```

### Cross-Validation

For more robust evaluation:

```python
from sklearn.model_selection import cross_val_score
import joblib

# Load model
model_data = joblib.load('models/trained/cholera_model.pkl')
pipeline = model_data['pipeline']

# Perform cross-validation
scores = cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_absolute_error')
print(f"Cross-validation MAE: {-scores.mean():.2f} (+/- {scores.std():.2f})")
```

## Troubleshooting

### Common Issues

**Issue: "chap: command not found"**
- Solution: Ensure CHAP is installed: `pip install chap-core`
- Solution: Activate virtual environment: `source venv/bin/activate`

**Issue: Missing columns in data**
- Solution: Check data format matches requirements
- Solution: Use `DataHarmonizer` to standardize column names

**Issue: "No climate features found in data"**
- Solution: Ensure at least one of: rainfall, temperature_mean, temperature_max, temperature_min, humidity is present
- Solution: Check for typos in column names

**Issue: High prediction error**
- Solution: Try different model types (random_forest vs gradient_boosting)
- Solution: Increase lag periods in configuration
- Solution: Add more historical training data
- Solution: Check for data quality issues

**Issue: Negative cholera case predictions**
- Solution: Predictions are automatically clipped to non-negative values
- Solution: Consider using log-transformation for highly skewed distributions

### Getting Help

- **CHAP Documentation**: https://dhis2-chap.github.io/chap-core/
- **CHAP GitHub**: https://github.com/dhis2-chap/chap-core
- **DHIS2 Community**: https://community.dhis2.org/
- **Project Issues**: https://github.com/Robert-Selemani/Cholera-Early-Warning-System/issues

## References

1. DHIS2 CHAP Platform: https://chap.dhis2.org/
2. CHAP Minimalist Example: https://github.com/dhis2-chap/minimalist_example
3. CHAP CLI Setup: https://dhis2-chap.github.io/chap-core/chap-cli/chap-core-cli-setup.html
4. Zimbabwe GeoPortal: https://zimgeoportal.org.zw/
5. DHIS2 Climate Data App: https://dhis2.org/climate/climate-data-app/
