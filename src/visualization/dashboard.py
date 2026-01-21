"""
Interactive dashboard for Cholera Early Warning System
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


# Initialize Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Cholera Early Warning System"
)

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Climate-Informed Cholera Early Warning System",
                   className="text-center mb-4 mt-4"),
            html.H4("Zimbabwe and Southern Africa",
                   className="text-center text-muted mb-4")
        ])
    ]),

    # Control Panel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Controls", className="card-title"),
                    html.Label("Select Region:"),
                    dcc.Dropdown(
                        id='region-dropdown',
                        options=[
                            {'label': 'Zimbabwe', 'value': 'ZW'},
                            {'label': 'Mozambique', 'value': 'MZ'},
                            {'label': 'Zambia', 'value': 'ZM'},
                            {'label': 'Malawi', 'value': 'MW'},
                            {'label': 'South Africa', 'value': 'ZA'}
                        ],
                        value='ZW',
                        className="mb-3"
                    ),
                    html.Label("Date Range:"),
                    dcc.DatePickerRange(
                        id='date-range',
                        start_date=datetime.now() - timedelta(days=90),
                        end_date=datetime.now(),
                        className="mb-3"
                    ),
                    dbc.Button("Update Dashboard", id="update-btn",
                              color="primary", className="w-100")
                ])
            ])
        ], width=3),

        # Main Content
        dbc.Col([
            # Alert Summary Cards
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Current Risk Level"),
                            html.H3(id="current-risk", className="text-warning")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Active Alerts"),
                            html.H3(id="active-alerts")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Cases (7 days)"),
                            html.H3(id="recent-cases")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H6("Forecast Accuracy"),
                            html.H3(id="forecast-accuracy")
                        ])
                    ])
                ], width=3),
            ], className="mb-4"),

            # Risk Map
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Geographic Risk Map"),
                            dcc.Graph(id='risk-map')
                        ])
                    ])
                ])
            ], className="mb-4"),

            # Time Series Plots
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Risk Trend"),
                            dcc.Graph(id='risk-trend')
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Climate Factors"),
                            dcc.Graph(id='climate-factors')
                        ])
                    ])
                ], width=6),
            ], className="mb-4"),

            # Forecast
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("4-Week Risk Forecast"),
                            dcc.Graph(id='forecast-plot')
                        ])
                    ])
                ])
            ])
        ], width=9)
    ])
], fluid=True)


# Callbacks
@app.callback(
    [Output('current-risk', 'children'),
     Output('active-alerts', 'children'),
     Output('recent-cases', 'children'),
     Output('forecast-accuracy', 'children'),
     Output('risk-map', 'figure'),
     Output('risk-trend', 'figure'),
     Output('climate-factors', 'figure'),
     Output('forecast-plot', 'figure')],
    [Input('update-btn', 'n_clicks')],
    [State('region-dropdown', 'value'),
     State('date-range', 'start_date'),
     State('date-range', 'end_date')]
)
def update_dashboard(n_clicks, region, start_date, end_date):
    """
    Update all dashboard components

    Args:
        n_clicks: Number of button clicks
        region: Selected region
        start_date: Start date
        end_date: End date

    Returns:
        Tuple of updated components
    """
    # Placeholder implementation - replace with actual data loading
    current_risk = "MODERATE"
    active_alerts = "3"
    recent_cases = "42"
    forecast_accuracy = "87%"

    # Create placeholder figures
    risk_map = go.Figure()
    risk_trend = go.Figure()
    climate_factors = go.Figure()
    forecast_plot = go.Figure()

    return (current_risk, active_alerts, recent_cases, forecast_accuracy,
            risk_map, risk_trend, climate_factors, forecast_plot)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
