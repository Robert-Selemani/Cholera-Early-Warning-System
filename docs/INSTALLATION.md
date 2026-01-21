# Installation Guide

## System Requirements

- Python 3.8 or higher
- 8GB RAM minimum (16GB recommended)
- 50GB disk space for data storage
- Linux, macOS, or Windows operating system

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CholeraEarlyWarningSystem
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate on Linux/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### 4. Configure the System

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit configuration file
nano config/config.yaml
```

Update the following settings:
- Database credentials
- Data source API keys
- Email/SMS notification settings
- Geographic coverage area

### 5. Set Up Database (Optional)

If using PostgreSQL:

```bash
# Create database
createdb cholera_ews

# Run migrations (if applicable)
python src/database/migrate.py
```

### 6. Download Initial Data

```bash
# Download climate data
python src/data_processing/download_climate_data.py

# Download administrative boundaries
python src/data_processing/download_boundaries.py
```

### 7. Verify Installation

```bash
# Run tests
pytest tests/

# Check system health
python -c "import src; print('Installation successful!')"
```

## Additional Setup

### API Keys

You'll need API keys for:
- Climate data sources (CHIRPS, ERA5)
- Notification services (optional)
- Mapping services (optional)

Add these to your `config/config.yaml` or `.env` file.

### Data Directory Structure

Ensure the following directories exist:
```
data/
├── raw/
├── processed/
├── climate/
├── epidemiological/
└── geospatial/
```

## Troubleshooting

### Common Issues

**Issue**: GDAL installation fails
```bash
# On Ubuntu/Debian
sudo apt-get install gdal-bin libgdal-dev

# On macOS
brew install gdal

# Then reinstall Python packages
pip install --upgrade --force-reinstall rasterio fiona geopandas
```

**Issue**: NetCDF4 library not found
```bash
# On Ubuntu/Debian
sudo apt-get install libnetcdf-dev

# On macOS
brew install netcdf
```

**Issue**: Memory errors during large data processing
- Increase system swap space
- Process data in smaller chunks
- Use cloud computing resources

## Next Steps

After installation, proceed to:
1. [Data Processing Guide](DATA_PROCESSING.md)
2. [Model Training Guide](MODEL_TRAINING.md)
3. [Dashboard Usage](DASHBOARD.md)
