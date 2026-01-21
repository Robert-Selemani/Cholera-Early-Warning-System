# Data Sources

## Climate Data

### 1. CHIRPS (Climate Hazards Group InfraRed Precipitation with Station data)
- **Variable**: Precipitation
- **Temporal Resolution**: Daily
- **Spatial Resolution**: 0.05° (~5km)
- **Coverage**: 1981-present
- **URL**: https://www.chc.ucsb.edu/data/chirps
- **Format**: NetCDF, GeoTIFF

### 2. ERA5 (ECMWF Reanalysis v5)
- **Variables**:
  - 2m temperature
  - Relative humidity
  - Wind speed
  - Soil moisture
- **Temporal Resolution**: Hourly
- **Spatial Resolution**: 0.25° (~25km)
- **Coverage**: 1940-present
- **URL**: https://cds.climate.copernicus.eu/
- **Format**: NetCDF (GRIB)

### 3. NOAA Climate Indices
- **Variables**:
  - El Niño Southern Oscillation (ENSO)
  - Indian Ocean Dipole (IOD)
  - Southern Oscillation Index (SOI)
- **Temporal Resolution**: Monthly
- **Coverage**: 1950-present
- **URL**: https://psl.noaa.gov/data/climateindices/

## Epidemiological Data

### 1. National Surveillance Systems
- **Source**: Zimbabwe Ministry of Health and Child Care
- **Variables**:
  - Cholera case counts
  - Deaths
  - Age groups
  - Geographic location
- **Temporal Resolution**: Weekly
- **Format**: CSV, Excel

### 2. WHO AFRO
- **Source**: World Health Organization African Region
- **Variables**:
  - Cholera outbreaks
  - Regional statistics
  - Disease trends
- **URL**: https://www.afro.who.int/health-topics/cholera
- **Format**: PDF reports, API

### 3. ProMED-mail
- **Source**: International Society for Infectious Diseases
- **Content**: Disease outbreak reports
- **URL**: https://promedmail.org/

## Geospatial Data

### 1. GADM (Database of Global Administrative Areas)
- **Content**: Administrative boundaries
- **Levels**: Country, province, district
- **URL**: https://gadm.org/
- **Format**: Shapefile, GeoPackage

### 2. WorldPop
- **Variable**: Population density
- **Temporal Resolution**: Annual
- **Spatial Resolution**: 100m
- **URL**: https://www.worldpop.org/
- **Format**: GeoTIFF

### 3. OpenStreetMap
- **Content**:
  - Water sources
  - Healthcare facilities
  - Transportation networks
  - Settlements
- **URL**: https://www.openstreetmap.org/
- **Format**: Shapefile, PBF

### 4. WASH Infrastructure
- **Sources**:
  - JMP (Joint Monitoring Programme)
  - National water authorities
- **Variables**:
  - Water access
  - Sanitation coverage
  - Treatment facilities

## Remote Sensing Data

### 1. MODIS (Moderate Resolution Imaging Spectroradiometer)
- **Variables**:
  - NDVI (vegetation)
  - Land surface temperature
  - Water extent
- **Temporal Resolution**: Daily/8-day
- **Spatial Resolution**: 250m-1km
- **URL**: https://modis.gsfc.nasa.gov/

### 2. Sentinel-2
- **Variables**: Multispectral imagery
- **Temporal Resolution**: 5 days
- **Spatial Resolution**: 10-60m
- **URL**: https://sentinel.esa.int/

## Data Access

### API Access
Many data sources provide API access. Store API keys in:
```
config/config.yaml
```

### Manual Downloads
For sources without APIs:
1. Download data manually
2. Place in appropriate `data/raw/` subdirectory
3. Run processing scripts

### Automated Updates
Set up cron jobs or scheduled tasks for:
- Daily climate data updates
- Weekly surveillance data ingestion
- Monthly climate index updates

## Data Quality

### Quality Checks
- Missing value detection
- Outlier identification
- Temporal consistency
- Spatial consistency
- Cross-validation with alternative sources

### Data Validation Scripts
```bash
python src/data_processing/validate_climate.py
python src/data_processing/validate_epi_data.py
```

## Citation Requirements

When using this system, please cite the appropriate data sources:
- CHIRPS: Funk et al. (2015)
- ERA5: Hersbach et al. (2020)
- WorldPop: Tatem (2017)
- Additional citations in CITATIONS.md
