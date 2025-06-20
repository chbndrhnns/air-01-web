"""Streamlit frontend for the salary calculator application."""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import sys
import os

# Add the parent directory to sys.path to import shared modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import SalaryEntry, SalaryStats

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="IT Salary Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}

.subtitle {
    font-size: 1.2rem;
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
}

.stats-container {
    display: flex;
    justify-content: space-around;
    margin: 2rem 0;
}

.stat-box {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem;
}

.stat-value {
    font-size: 2rem;
    font-weight: bold;
    color: #1f77b4;
}

.stat-label {
    font-size: 0.9rem;
    color: #666;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


def fetch_data(endpoint: str, params: Dict[str, Any] = None) -> Any:
    """Fetch data from the API endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to the API server. Please make sure the backend is running on port 8000.")
        st.stop()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API request failed: {str(e)}")
        return None


def display_stats(stats: Dict[str, Any]) -> None:
    """Display salary statistics in a formatted layout."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Average Salary",
            value=f"${stats['average_salary']:,.0f}K",
            delta=None
        )

    with col2:
        st.metric(
            label="Median Salary",
            value=f"${stats['median_salary']:,.0f}K",
            delta=None
        )

    with col3:
        st.metric(
            label="Salary Range",
            value=f"${stats['min_salary']}K - ${stats['max_salary']}K",
            delta=None
        )

    with col4:
        st.metric(
            label="Sample Size",
            value=f"{stats['count']:,} responses",
            delta=None
        )


def create_salary_histogram(salary_data: List[Dict[str, Any]]) -> go.Figure:
    """Create a histogram of salary distribution."""
    salaries = [entry['value'] for entry in salary_data]

    fig = go.Figure(data=[
        go.Histogram(
            x=salaries,
            nbinsx=30,
            marker_color='#1f77b4',
            opacity=0.7,
            name='Salary Distribution'
        )
    ])

    fig.update_layout(
        title="Salary Distribution",
        xaxis_title="Salary (in thousands USD)",
        yaxis_title="Number of Responses",
        template="plotly_white",
        height=400
    )

    return fig


def create_experience_boxplot(salary_data: List[Dict[str, Any]]) -> go.Figure:
    """Create a box plot of salaries by experience level."""
    df = pd.DataFrame(salary_data)

    fig = px.box(
        df,
        x='category',
        y='value',
        title="Salary Distribution by Experience Level",
        labels={'category': 'Experience Level', 'value': 'Salary (in thousands USD)'},
        template="plotly_white"
    )

    fig.update_layout(height=400)
    return fig


def main():
    """Main Streamlit application."""

    # Header
    st.markdown('<h1 class="main-header">💰 IT Salary Calculator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Based on JetBrains Developer Ecosystem Survey 2024</p>', unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.header("🔍 Filters")

    # Load filter options
    countries = fetch_data("countries")
    if not countries:
        return

    # Country filter
    country_options = ["All Countries"] + countries
    selected_country = st.sidebar.selectbox("Country", country_options)
    country_param = None if selected_country == "All Countries" else selected_country

    # Language filter
    languages = fetch_data("languages", {"country": country_param})
    if languages:
        language_options = ["All Languages"] + languages
        selected_language = st.sidebar.selectbox("Programming Language", language_options)
        language_param = None if selected_language == "All Languages" else selected_language
    else:
        language_param = None

    # Experience filter
    experience_levels = fetch_data("experience-levels", {
        "country": country_param,
        "language": language_param
    })
    if experience_levels:
        experience_options = ["All Experience Levels"] + experience_levels
        selected_experience = st.sidebar.selectbox("Experience Level", experience_options)
        experience_param = None if selected_experience == "All Experience Levels" else selected_experience
    else:
        experience_param = None

    # Apply filters button
    if st.sidebar.button("🔄 Apply Filters", type="primary"):
        st.rerun()

    # Main content
    with st.spinner("Loading salary data..."):
        # Get salary statistics
        params = {
            "country": country_param,
            "language": language_param,
            "experience": experience_param
        }

        stats = fetch_data("salary-stats", params)
        salary_data = fetch_data("salary-data", params)

        if stats and salary_data:
            # Display statistics
            st.subheader("📊 Salary Statistics")
            display_stats(stats)

            # Display visualizations
            col1, col2 = st.columns(2)

            with col1:
                fig_hist = create_salary_histogram(salary_data)
                st.plotly_chart(fig_hist, use_container_width=True)

            with col2:
                fig_box = create_experience_boxplot(salary_data)
                st.plotly_chart(fig_box, use_container_width=True)

            # Data details section
            with st.expander("📋 View Raw Data"):
                df = pd.DataFrame(salary_data)
                st.dataframe(df, use_container_width=True)

                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"salary_data_{selected_country}_{selected_language}_{selected_experience}.csv",
                    mime="text/csv"
                )

        else:
            st.warning("⚠️ No data available for the selected filters. Please try different filter combinations.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>"
        "Data source: JetBrains Developer Ecosystem Survey 2024 | "
        "Built with ❤️ using Streamlit and FastAPI"
        "</p>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()