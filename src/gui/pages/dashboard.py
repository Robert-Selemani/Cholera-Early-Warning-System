"""
Dashboard Page - Overview and Quick Stats
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from pathlib import Path


def show():
    """Display the main dashboard"""

    st.markdown('<h2 class="section-header">📊 System Overview</h2>', unsafe_allow_html=True)

    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🎯 Active Districts",
            value="8",
            delta="Monitoring",
            help="Number of districts currently monitored"
        )

    with col2:
        st.metric(
            label="🌡️ Climate Data Points",
            value="2,450",
            delta="+150 this month",
            help="Total climate observations in database"
        )

    with col3:
        st.metric(
            label="🔬 Trained Models",
            value="3",
            delta="1 active",
            help="Number of trained prediction models"
        )

    with col4:
        st.metric(
            label="⚠️ High Risk Districts",
            value="2",
            delta="Harare, Manicaland",
            delta_color="inverse",
            help="Districts with elevated cholera risk"
        )

    st.markdown("---")

    # Risk Alert Section
    st.markdown('<h2 class="section-header">⚠️ Current Risk Alerts</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        # Risk alerts
        st.markdown("""
        <div class="metric-card warning">
            <h3 style="color: #FC8170; margin-top: 0;">🔴 HIGH RISK: Harare</h3>
            <p><strong>Predicted Cases (next month):</strong> 45-65 cases (95% CI)</p>
            <p><strong>Risk Factors:</strong></p>
            <ul>
                <li>Heavy rainfall forecast (150mm expected)</li>
                <li>Peak rainy season (January)</li>
                <li>High-density suburbs vulnerable</li>
            </ul>
            <p><strong>Recommended Actions:</strong></p>
            <ul>
                <li>Pre-position water treatment supplies</li>
                <li>Activate health facility preparedness</li>
                <li>Enhance surveillance in Budiriro, Glen View</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card warning">
            <h3 style="color: #FC8170; margin-top: 0;">🟡 MODERATE RISK: Manicaland</h3>
            <p><strong>Predicted Cases (next month):</strong> 15-25 cases (95% CI)</p>
            <p><strong>Risk Factors:</strong></p>
            <ul>
                <li>Elevated rainfall (100mm expected)</li>
                <li>Rural water access challenges</li>
            </ul>
            <p><strong>Recommended Actions:</strong></p>
            <ul>
                <li>Monitor water source safety</li>
                <li>Strengthen community health education</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Risk summary
        st.markdown("""
        <div class="metric-card success">
            <h3 style="color: #4C7C83; margin-top: 0;">🟢 LOW RISK Districts</h3>
            <ul>
                <li>Mashonaland East</li>
                <li>Mashonaland West</li>
                <li>Midlands</li>
                <li>Masvingo</li>
                <li>Bulawayo</li>
                <li>Matabeleland North</li>
            </ul>
            <p style="margin-top: 1rem;"><strong>Status:</strong> Normal surveillance</p>
        </div>
        """, unsafe_allow_html=True)

        # Weather summary
        st.markdown("""
        <div class="metric-card">
            <h3 style="color: #4C7C83; margin-top: 0;">🌦️ Climate Outlook</h3>
            <p><strong>Current Season:</strong> Peak Rainy</p>
            <p><strong>Month:</strong> January 2026</p>
            <p><strong>Rainfall Forecast:</strong> Above normal</p>
            <p><strong>Temperature:</strong> 22-28°C</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Recent Predictions Chart
    st.markdown('<h2 class="section-header">📈 30-Day Cholera Forecast</h2>', unsafe_allow_html=True)

    # Generate sample forecast data
    dates = pd.date_range(start='2026-01-15', periods=30, freq='D')
    districts = ['Harare', 'Manicaland', 'Bulawayo']

    forecast_data = []
    for district in districts:
        if district == 'Harare':
            base = 50
        elif district == 'Manicaland':
            base = 20
        else:
            base = 5

        for date in dates:
            forecast_data.append({
                'Date': date,
                'District': district,
                'Predicted Cases': base + (date.day % 10) - 5,
                'Lower CI': base - 10,
                'Upper CI': base + 15
            })

    forecast_df = pd.DataFrame(forecast_data)

    # Create interactive line chart
    fig = px.line(
        forecast_df,
        x='Date',
        y='Predicted Cases',
        color='District',
        title='Cholera Case Predictions by District',
        labels={'Predicted Cases': 'Predicted Cases', 'Date': 'Date'},
        color_discrete_map={
            'Harare': '#FC8170',
            'Manicaland': '#46CBDE',
            'Bulawayo': '#D3F781'
        }
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="sans-serif", size=12, color="#000000"),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Recent Activity and System Status
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 class="section-header">📋 Recent Activity</h3>', unsafe_allow_html=True)

        activity_data = pd.DataFrame({
            'Timestamp': [
                '2026-01-22 09:15',
                '2026-01-22 08:30',
                '2026-01-21 16:45',
                '2026-01-21 14:20',
                '2026-01-20 11:00'
            ],
            'Activity': [
                '🔮 Forecast generated for Harare',
                '📊 Data harmonization completed',
                '🧮 Model training completed (RF)',
                '📥 Climate data updated',
                '📋 Evaluation metrics calculated'
            ]
        })

        st.dataframe(
            activity_data,
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.markdown('<h3 class="section-header">⚙️ System Status</h3>', unsafe_allow_html=True)

        status_data = pd.DataFrame({
            'Component': [
                'CHAP Platform',
                'Data Pipeline',
                'Prediction Engine',
                'DHIS2 Connection',
                'Climate Data API'
            ],
            'Status': [
                '✅ Online',
                '✅ Running',
                '✅ Ready',
                '⚠️ Not Configured',
                '✅ Connected'
            ],
            'Last Updated': [
                '2 min ago',
                '5 min ago',
                '15 min ago',
                'Never',
                '1 hour ago'
            ]
        })

        st.dataframe(
            status_data,
            hide_index=True,
            use_container_width=True
        )

    # Quick Actions
    st.markdown("---")
    st.markdown('<h2 class="section-header">⚡ Quick Actions</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📊 Upload New Data", use_container_width=True):
            st.switch_page("pages/data_management.py")

    with col2:
        if st.button("🧮 Train Model", use_container_width=True):
            st.switch_page("pages/model_training.py")

    with col3:
        if st.button("🔮 Generate Forecast", use_container_width=True):
            st.switch_page("pages/predictions.py")

    with col4:
        if st.button("📈 View Analytics", use_container_width=True):
            st.switch_page("pages/visualizations.py")


if __name__ == "__main__":
    show()
