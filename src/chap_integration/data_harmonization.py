"""
Data Harmonization Module for CHAP Integration

This module provides tools to harmonize Zimbabwe health and climate data
into the format required by CHAP models.

The harmonization process includes:
1. Standardizing column names
2. Aligning temporal resolution (monthly aggregation)
3. Spatial alignment (district-level)
4. Handling missing values
5. Data validation
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import warnings


class DataHarmonizer:
    """
    Harmonize climate and health data for CHAP compatibility
    """

    def __init__(self):
        self.required_columns = [
            'time_period',
            'district',
            'rainfall',
            'temperature_mean',
            'cholera_cases'
        ]

        self.optional_columns = [
            'temperature_max',
            'temperature_min',
            'humidity',
            'population',
            'water_access',
            'sanitation_coverage'
        ]

    def harmonize_time_period(self, df, date_column='date', format='%Y-%m-%d'):
        """
        Convert dates to standardized time period format (YYYY-MM)

        Args:
            df: DataFrame with date column
            date_column: Name of date column
            format: Date format string

        Returns:
            DataFrame with time_period column
        """
        if date_column not in df.columns:
            raise ValueError(f"Date column '{date_column}' not found")

        # Convert to datetime
        df['date_parsed'] = pd.to_datetime(df[date_column], format=format, errors='coerce')

        # Extract year-month
        df['time_period'] = df['date_parsed'].dt.to_period('M').astype(str)

        # Remove temporary column
        df = df.drop(columns=['date_parsed'])

        return df

    def aggregate_to_monthly(self, df, time_column='time_period'):
        """
        Aggregate data to monthly resolution

        Args:
            df: DataFrame with sub-monthly data
            time_column: Name of time period column

        Returns:
            DataFrame aggregated to monthly level
        """
        if 'district' not in df.columns:
            raise ValueError("District column required for aggregation")

        # Define aggregation functions for different column types
        agg_functions = {}

        for col in df.columns:
            if col in [time_column, 'district']:
                continue
            elif 'rainfall' in col.lower():
                agg_functions[col] = 'sum'  # Sum rainfall
            elif 'temperature' in col.lower():
                agg_functions[col] = 'mean'  # Average temperature
            elif 'humidity' in col.lower():
                agg_functions[col] = 'mean'  # Average humidity
            elif 'cases' in col.lower():
                agg_functions[col] = 'sum'  # Sum cases
            elif 'population' in col.lower():
                agg_functions[col] = 'first'  # Take first value
            else:
                agg_functions[col] = 'mean'  # Default to mean

        # Group and aggregate
        df_monthly = df.groupby(['district', time_column]).agg(agg_functions).reset_index()

        return df_monthly

    def standardize_district_names(self, df, district_column='district'):
        """
        Standardize district names to match Zimbabwe administrative divisions

        Args:
            df: DataFrame with district column
            district_column: Name of district column

        Returns:
            DataFrame with standardized district names
        """
        if district_column not in df.columns:
            raise ValueError(f"District column '{district_column}' not found")

        # District name mappings (common variations to standard names)
        district_mappings = {
            # Harare
            'harare city': 'Harare',
            'harare urban': 'Harare',
            'harare': 'Harare',

            # Manicaland
            'manicaland': 'Manicaland',
            'mutare': 'Manicaland',
            'chimanimani': 'Manicaland',
            'chipinge': 'Manicaland',

            # Mashonaland Central
            'mashonaland central': 'Mashonaland Central',
            'mash central': 'Mashonaland Central',
            'bindura': 'Mashonaland Central',

            # Mashonaland East
            'mashonaland east': 'Mashonaland East',
            'mash east': 'Mashonaland East',
            'marondera': 'Mashonaland East',

            # Mashonaland West
            'mashonaland west': 'Mashonaland West',
            'mash west': 'Mashonaland West',
            'chinhoyi': 'Mashonaland West',

            # Matabeleland North
            'matabeleland north': 'Matabeleland North',
            'mat north': 'Matabeleland North',
            'hwange': 'Matabeleland North',

            # Matabeleland South
            'matabeleland south': 'Matabeleland South',
            'mat south': 'Matabeleland South',
            'beitbridge': 'Matabeleland South',

            # Midlands
            'midlands': 'Midlands',
            'gweru': 'Midlands',
            'kwekwe': 'Midlands',

            # Masvingo
            'masvingo': 'Masvingo',
            'chivi': 'Masvingo',

            # Bulawayo
            'bulawayo': 'Bulawayo',
            'bulawayo city': 'Bulawayo',
        }

        # Apply mappings (case-insensitive)
        df['district_lower'] = df[district_column].str.lower().str.strip()
        df['district'] = df['district_lower'].map(district_mappings)

        # For unmapped districts, use original name (capitalized)
        unmapped = df['district'].isna()
        df.loc[unmapped, 'district'] = df.loc[unmapped, district_column].str.title()

        # Remove temporary column
        df = df.drop(columns=['district_lower'])

        # Warn about unmapped districts
        unique_unmapped = df.loc[unmapped, district_column].unique()
        if len(unique_unmapped) > 0:
            warnings.warn(
                f"Unmapped districts found: {', '.join(unique_unmapped)}. "
                "Using original names."
            )

        return df

    def handle_missing_values(self, df, strategy='interpolate'):
        """
        Handle missing values in climate and health data

        Args:
            df: DataFrame with missing values
            strategy: Strategy for handling missingness ('interpolate', 'forward_fill', 'drop')

        Returns:
            DataFrame with handled missing values
        """
        if strategy == 'interpolate':
            # Interpolate climate variables by district
            climate_cols = [col for col in df.columns if any(
                term in col.lower() for term in ['rainfall', 'temperature', 'humidity']
            )]

            for col in climate_cols:
                df[col] = df.groupby('district')[col].transform(
                    lambda x: x.interpolate(method='linear', limit_direction='both')
                )

        elif strategy == 'forward_fill':
            # Forward fill within districts
            df = df.sort_values(['district', 'time_period'])
            df = df.groupby('district').ffill()

        elif strategy == 'drop':
            # Drop rows with any missing values
            df = df.dropna()

        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        return df

    def validate_data(self, df):
        """
        Validate harmonized data

        Args:
            df: Harmonized DataFrame

        Returns:
            Boolean indicating validation status and list of issues
        """
        issues = []

        # Check required columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            issues.append(f"Missing required columns: {missing_cols}")

        # Check for negative values in certain columns
        for col in ['rainfall', 'temperature_mean', 'cholera_cases']:
            if col in df.columns and (df[col] < 0).any():
                issues.append(f"Negative values found in {col}")

        # Check time period format
        if 'time_period' in df.columns:
            try:
                pd.to_datetime(df['time_period'], format='%Y-%m')
            except:
                issues.append("Invalid time_period format (expected YYYY-MM)")

        # Check for duplicates
        if 'district' in df.columns and 'time_period' in df.columns:
            duplicates = df.duplicated(subset=['district', 'time_period'], keep=False)
            if duplicates.any():
                n_dup = duplicates.sum()
                issues.append(f"Found {n_dup} duplicate district-time combinations")

        return len(issues) == 0, issues

    def harmonize(self, health_df, climate_df, output_path=None):
        """
        Complete harmonization workflow

        Args:
            health_df: DataFrame with health/cholera data
            climate_df: DataFrame with climate data
            output_path: Optional path to save harmonized data

        Returns:
            Harmonized DataFrame ready for CHAP models
        """
        print("Starting data harmonization...")

        # Merge health and climate data
        print("  Merging health and climate data...")
        merged_df = pd.merge(
            health_df,
            climate_df,
            on=['district', 'time_period'],
            how='outer'
        )

        # Standardize district names
        print("  Standardizing district names...")
        merged_df = self.standardize_district_names(merged_df)

        # Handle missing values
        print("  Handling missing values...")
        merged_df = self.handle_missing_values(merged_df, strategy='interpolate')

        # Sort by district and time
        merged_df = merged_df.sort_values(['district', 'time_period'])

        # Validate
        print("  Validating harmonized data...")
        is_valid, issues = self.validate_data(merged_df)

        if not is_valid:
            print("  Validation warnings:")
            for issue in issues:
                print(f"    - {issue}")

        # Save if path provided
        if output_path:
            print(f"  Saving to {output_path}...")
            merged_df.to_csv(output_path, index=False)

        print("Harmonization complete!")
        print(f"  Final dataset: {len(merged_df)} rows, {len(merged_df.columns)} columns")
        print(f"  Time range: {merged_df['time_period'].min()} to {merged_df['time_period'].max()}")
        print(f"  Districts: {merged_df['district'].nunique()}")

        return merged_df


def main():
    """Example usage of DataHarmonizer"""
    import argparse

    parser = argparse.ArgumentParser(description='Harmonize Zimbabwe health and climate data')
    parser.add_argument('health_data', type=str, help='Path to health/cholera data CSV')
    parser.add_argument('climate_data', type=str, help='Path to climate data CSV')
    parser.add_argument('output', type=str, help='Path to save harmonized data')

    args = parser.parse_args()

    # Load data
    health_df = pd.read_csv(args.health_data)
    climate_df = pd.read_csv(args.climate_data)

    # Harmonize
    harmonizer = DataHarmonizer()
    harmonized_df = harmonizer.harmonize(health_df, climate_df, args.output)


if __name__ == '__main__':
    main()
