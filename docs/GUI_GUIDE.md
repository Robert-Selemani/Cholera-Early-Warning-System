# Cholera Early Warning System - GUI Guide

## Web-Based Dashboard for Climate-Informed Disease Forecasting

This guide explains how to use the graphical user interface (GUI) for the Cholera Early Warning System.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Dashboard Overview](#dashboard-overview)
3. [Module Guides](#module-guides)
4. [Color Scheme](#color-scheme)
5. [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Launching the GUI

Start the Streamlit application:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### First-Time Setup

1. Upload sample data (Data Management module)
2. Harmonize the data
3. Train a model (Model Training module)
4. Generate predictions (Predictions module)

## Dashboard Overview

The main dashboard provides:
- **System Overview**: Key metrics and active district monitoring
- **Risk Alerts**: Current high-risk districts with recommendations
- **30-Day Forecast**: Cholera case predictions visualization
- **Recent Activity**: System events and updates
- **System Status**: Component health checks
- **Quick Actions**: One-click navigation to common tasks

### Key Metrics

- **Active Districts**: Number of districts being monitored
- **Climate Data Points**: Total observations in database
- **Trained Models**: Available prediction models
- **High Risk Districts**: Areas with elevated cholera risk

## Module Guides

### 📊 Data Management

Upload, harmonize, and manage your data:

**Upload Data Tab:**
- Upload climate data (CSV format)
- Upload health/cholera data (CSV format)
- Download sample templates

**Required CSV Format:**

**Climate Data:**
```csv
time_period,district,rainfall,temperature_mean,temperature_max,temperature_min,humidity
2023-01,Harare,125.5,22.3,28.5,16.2,65.0
```

**Health Data:**
```csv
time_period,district,cholera_cases
2023-01,Harare,12
```

**Harmonize Data Tab:**
- Merge climate and health datasets
- Standardize district names
- Handle missing values
- Validate data quality

**View Data Tab:**
- Browse existing datasets
- View summary statistics
- Download processed data

**Manage Data Tab:**
- Delete unnecessary files
- Free up storage space

### 🧮 Model Training

Train CHAP-compatible prediction models:

**Configuration Options:**
- **Model Type**: Random Forest or Gradient Boosting
- **Number of Estimators**: 50-500 trees
- **Maximum Depth**: 5-30 levels
- **Lag Periods**: 1, 2, 4, or 8 months
- **Random State**: Seed for reproducibility

**Training Process:**
1. Configure model parameters
2. Click "Start Training"
3. Wait for completion (may take minutes)
4. Review feature importance

**Trained Models:**
- Saved in `models/trained/`
- Can be reused for predictions
- Track training history

### 🔮 Predictions

Generate cholera forecasts:

**Settings:**
- **Select Model**: Choose trained model
- **Forecast Horizon**: 1-12 months
- **Target Districts**: Select one or more
- **Start Month**: Beginning of forecast period
- **Include Uncertainty**: Show 95% confidence intervals

**Prediction Output:**
- Probabilistic forecasts (100 samples)
- Mean predicted cases
- Confidence intervals (2.5% - 97.5%)
- Interactive visualizations
- Downloadable CSV files

### 📈 Visualizations

Interactive data exploration:

**Time Series Tab:**
- Cholera cases over time
- Rainfall patterns
- Multi-district comparisons

**Geographic Tab:**
- District-level maps (coming soon)
- Risk heatmaps
- Infrastructure overlays

**Climate Patterns Tab:**
- Temperature vs rainfall scatter plots
- Seasonal patterns
- Monthly averages

**Trends & Correlations Tab:**
- Correlation matrices
- Feature relationships

### 📋 Evaluation

Assess model performance:

**Metrics Provided:**

**Regression Metrics:**
- **MAE**: Mean Absolute Error
- **RMSE**: Root Mean Squared Error
- **R²**: Coefficient of Determination (0-1, higher is better)
- **Correlation**: Pearson correlation coefficient

**Detection Metrics:**
- **Accuracy**: Overall correct predictions
- **Precision**: Positive predictive value
- **Recall**: Sensitivity (outbreak detection rate)
- **F1 Score**: Harmonic mean of precision/recall
- **Specificity**: True negative rate

**Performance Interpretation:**
- R² ≥ 0.7: Excellent
- R² = 0.5-0.7: Good
- R² = 0.3-0.5: Moderate
- R² < 0.3: Poor (consider retraining)

### ⚙️ Settings

Configure system parameters:

**CHAP Configuration:**
- Default model settings
- Forecast parameters
- Feature engineering options

**Geographic Settings:**
- Active monitoring districts
- High-risk area definitions
- Rainy season months

**Data Sources:**
- Climate data providers
- Health data systems
- Geospatial data sources
- DHIS2 integration

**About:**
- Version information
- System requirements
- Support resources

## Color Scheme

The GUI uses a color palette inspired by CSIDNET:

### Primary Colors
- **Teal**: #4C7C83 (Buttons, headers)
- **Teal Dark**: #033E45 (Cards, emphasis)
- **Midnight**: #020381 (Primary actions)

### Secondary Colors
- **Lime**: #D3F781 (Success states)
- **Aqua**: #46CBDE (Information, accents)
- **Salmon**: #FC8170 (Warnings, high risk)

### Background Colors
- **Off-White**: #F4F4F4 (Main background)
- **White**: #FFFFFF (Cards, containers)

### Usage
- **High Risk Alerts**: Salmon card with red border
- **Moderate Risk**: Yellow/orange indicators
- **Low Risk**: Green/lime indicators
- **Information**: Aqua blue cards

## Troubleshooting

### Common Issues

**Issue: "Module not found" error**
- Solution: Ensure all dependencies installed: `pip install -r requirements.txt`

**Issue: GUI doesn't load**
- Solution: Check that streamlit is installed: `pip install streamlit`
- Solution: Try: `streamlit run app.py --server.port 8502`

**Issue: Data upload fails**
- Solution: Check CSV format matches template
- Solution: Ensure required columns present
- Solution: Check for special characters in district names

**Issue: Model training fails**
- Solution: Verify harmonized data exists
- Solution: Check data has no missing required columns
- Solution: Review training output for specific errors

**Issue: Predictions show errors**
- Solution: Ensure model is trained
- Solution: Verify test/future data format
- Solution: Check lag periods match training configuration

### Performance Tips

1. **Large Datasets**: Consider filtering to recent years
2. **Slow Training**: Reduce number of estimators or max depth
3. **Memory Issues**: Process districts separately
4. **Browser Performance**: Use Chrome or Firefox for best results

### Getting Help

- **Documentation**: See `docs/CHAP_USAGE.md`
- **Issues**: Report at GitHub Issues
- **CHAP Help**: https://dhis2-chap.github.io/chap-core/

## Keyboard Shortcuts

- **`Ctrl/Cmd + K`**: Focus search (if enabled)
- **`R`**: Rerun application
- **`C`**: Clear cache
- **`Ctrl/Cmd + R`**: Refresh browser

## Best Practices

1. **Regular Data Updates**: Upload new data monthly
2. **Model Retraining**: Retrain models quarterly
3. **Evaluation**: Check metrics after each training
4. **Backup**: Download processed data regularly
5. **Documentation**: Note configuration changes

## Examples

### Complete Workflow

1. **Upload Data**
   - Go to Data Management
   - Upload climate data CSV
   - Upload health data CSV

2. **Harmonize**
   - Switch to Harmonize tab
   - Select interpolation for missing values
   - Click "Harmonize Data"

3. **Train Model**
   - Go to Model Training
   - Select Random Forest
   - Set estimators to 200
   - Click "Start Training"

4. **Generate Forecast**
   - Go to Predictions
   - Select trained model
   - Set horizon to 3 months
   - Click "Generate Predictions"

5. **Evaluate**
   - Go to Evaluation
   - Select model
   - Click "Run Evaluation"
   - Review R² and MAE metrics

6. **Visualize**
   - Go to Visualizations
   - Explore time series
   - Check seasonal patterns

## Reference

### Data Requirements

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| time_period | string | Yes | YYYY-MM format |
| district | string | Yes | District name |
| rainfall | float | Yes | Rainfall (mm) |
| temperature_mean | float | Yes | Mean temp (°C) |
| cholera_cases | int | Yes | Case count |
| humidity | float | No | Relative humidity (%) |
| temperature_max | float | No | Max temp (°C) |
| temperature_min | float | No | Min temp (°C) |

### Supported File Formats

- **Input**: CSV (comma-separated values)
- **Output**: CSV, JSON
- **Models**: PKL (pickle format)
- **Configs**: YAML

### System Requirements

- **Python**: 3.8+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for data and models
- **Browser**: Chrome, Firefox, Safari, Edge (latest versions)
- **Screen**: 1280x720 minimum resolution

## Additional Resources

- [CHAP Documentation](https://dhis2-chap.github.io/chap-core/)
- [GitHub Repository](https://github.com/Robert-Selemani/Cholera-Early-Warning-System)
- [Zimbabwe GeoPortal](https://zimgeoportal.org.zw/)
- [DHIS2 Climate Tools](https://dhis2.org/climate/)
