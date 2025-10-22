import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import time
import numpy as np
from utils.data_processor import DataProcessor
from utils.charts import ChartGenerator
from utils.insights import InsightsGenerator
from utils.translations import get_text, get_language_options

# Page configuration
st.set_page_config(
    page_title="Yoga App Analytics Dashboard",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('styles/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

# Helper functions for multi-country data accumulation
def detect_country_from_data(data):
    """Detect which country this data represents based on patterns or explicit country field."""
    if isinstance(data, dict):
        # Check if there's an explicit country field
        if 'country' in data:
            return data['country']
        
        # Check for row_number field that might indicate sequence
        if 'row_number' in data:
            row_num = data.get('row_number', 1)
            # Map row numbers to countries based on n8n sequence
            country_map = {1: 'US', 2: 'India', 3: 'VN'}
            return country_map.get(row_num)
        
        # Try to infer from data patterns (first item = US, etc)
        return None
    
    return None

def process_n8n_array_format(data_array):
    """Process array format from n8n where each item represents a country."""
    countries_data = []
    
    for i, item in enumerate(data_array):
        # Detect country for this item
        country = detect_country_from_data(item)
        
        if not country:
            # Fallback: use position to determine country
            country_map = {0: 'US', 1: 'India', 2: 'VN'}
            country = country_map.get(i, f'Country_{i+1}')
        
        # Remove metadata fields and keep only metric data
        clean_data = {k: v for k, v in item.items() 
                     if k not in ['row_number', 'country'] and not k.startswith('_')}
        
        countries_data.append({
            'country': country,
            'data': [clean_data]  # Wrap in array for time-series format
        })
    
    return countries_data

def add_country_data(country, data):
    """Add data for a specific country to the accumulator."""
    if not st.session_state.country_accumulator['collecting']:
        # Start collecting
        st.session_state.country_accumulator['collecting'] = True
        st.session_state.country_accumulator['start_time'] = time.time()
        st.session_state.country_accumulator['data'] = {}
    
    # Store the country data
    st.session_state.country_accumulator['data'][country] = data
    
    # Check if we have all expected countries
    expected = set(st.session_state.country_accumulator['expected_countries'])
    received = set(st.session_state.country_accumulator['data'].keys())
    
    return expected.issubset(received)

def check_accumulator_timeout():
    """Check if accumulator has timed out and handle termination."""
    if not st.session_state.country_accumulator['collecting']:
        return False
    
    start_time = st.session_state.country_accumulator['start_time']
    timeout = st.session_state.country_accumulator['timeout_seconds']
    elapsed = time.time() - start_time
    
    return elapsed > timeout

def reset_accumulator():
    """Reset the accumulator state."""
    st.session_state.country_accumulator['data'] = {}
    st.session_state.country_accumulator['start_time'] = None
    st.session_state.country_accumulator['collecting'] = False

def process_accumulated_data():
    """Process all accumulated country data into final format."""
    accumulated_data = st.session_state.country_accumulator['data']
    
    # Convert to the expected format for DataProcessor
    country_array = []
    for country, data in accumulated_data.items():
        country_array.append({
            'country': country,
            'data': data if isinstance(data, list) else [data]
        })
    
    # Process using DataProcessor
    processor = DataProcessor()
    processed_data = processor.process_webhook_data(country_array)
    
    return processed_data

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'webhook_url' not in st.session_state:
    st.session_state.webhook_url = ""
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None


# Initialize multi-country accumulator session state
if 'country_accumulator' not in st.session_state:
    st.session_state.country_accumulator = {
        'data': {},  # Store data for each country
        'expected_countries': ['US', 'India', 'VN'],  # Expected countries
        'start_time': None,  # When collection started
        'timeout_seconds': 60,  # Wait max 60 seconds for all countries
        'collecting': False  # Whether we're currently collecting
    }
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Language selector
st.sidebar.subheader(get_text('language_selector', st.session_state.language))
language_options = get_language_options()
selected_language_display = st.sidebar.selectbox(
    "Select Language",
    options=list(language_options.keys()),
    index=list(language_options.values()).index(st.session_state.language)
)

selected_language = language_options[selected_language_display]
if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()

# Header
st.title(f"🧘‍♀️ {get_text('page_title', st.session_state.language)}")
st.markdown(f"*{get_text('page_subtitle', st.session_state.language)}*")

# Test mode for displaying only the three new charts
if st.sidebar.checkbox("📊 Test Mode - Show Only Three New Charts", value=False):
    if st.session_state.data:
        st.header("Testing Three New Charts")
        
        # Get the aggregated data
        from utils.data_processor import DataProcessor
        from utils.charts import ChartGenerator
        
        processor = DataProcessor()
        chart_gen = ChartGenerator()
        
        # Get All Countries data for testing
        countries_data = st.session_state.data
        webhook_data = countries_data.get('All Countries', None)
        
        if webhook_data:
            all_periods = webhook_data.get('data', [])
            aggregated_data = processor._aggregate_time_series_data(all_periods)
            
            # Display the three new charts
            st.subheader(f"1. {get_text('user_activity_comparison_title', st.session_state.language)}")
            user_activity_chart = chart_gen.create_user_activity_comparison(all_periods, st.session_state.language)
            st.plotly_chart(user_activity_chart, use_container_width=True)
            
            st.subheader(f"2. {get_text('user_funnel_analysis_title', st.session_state.language)}")
            funnel_chart = chart_gen.create_user_funnel_analysis(aggregated_data, st.session_state.language)
            st.plotly_chart(funnel_chart, use_container_width=True)
            
            st.subheader(f"3. {get_text('churn_risk_indicator_title', st.session_state.language)}")
            churn_risk_chart = chart_gen.create_churn_risk_indicator(aggregated_data, st.session_state.language)
            st.plotly_chart(churn_risk_chart, use_container_width=True)
            
            st.success("✅ All three charts are loaded and displaying data!")
        else:
            st.error("No All Countries data available")
    else:
        st.warning("No data loaded. Sample data should auto-load on refresh.")
    
    st.stop()  # Stop rendering the rest of the page

# Multi-country data collection status
if st.session_state.country_accumulator['collecting']:
    # Check for timeout
    if check_accumulator_timeout():
        # Timeout reached - show error and automatically reset
        st.error("❌ **Timeout Error:** Data collection failed after 60 seconds")
        st.warning("Not all countries were received. Please check your n8n workflow is sending data for all 3 countries.")
        reset_accumulator()  # Automatically reset
        if st.button("🔄 Try Again", key="reset_after_timeout", use_container_width=True):
            st.rerun()
        st.stop()  # Stop further processing
    else:
        # Show loading state (no detailed progress)
        start_time = st.session_state.country_accumulator['start_time']
        elapsed = int(time.time() - start_time)
        remaining_time = 60 - elapsed
        
        # Simple loading container
        loading_container = st.container()
        with loading_container:
            col1, col2 = st.columns([5, 1])
            with col1:
                # Loading spinner with message
                with st.spinner("Loading data from webhook..."):
                    st.empty()  # Placeholder for spinner animation
            with col2:
                # Just show time remaining
                st.metric("⏱️", f"{remaining_time}s")
        
        # Small cancel button
        if st.button("Cancel", key="cancel_loading", help="Cancel data collection"):
            reset_accumulator()
            st.rerun()
        
        st.divider()

# Webhook input section
st.header(get_text('data_source_header', st.session_state.language))
col1, col2 = st.columns([4, 1])

with col1:
    webhook_url = st.text_input(
        get_text('webhook_input_label', st.session_state.language),
        value=st.session_state.webhook_url,
        placeholder=get_text('webhook_placeholder', st.session_state.language),
        help=get_text('webhook_help', st.session_state.language)
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(get_text('fetch_data_button', st.session_state.language), type="primary"):
        if webhook_url:
            try:
                with st.spinner(get_text('fetching_data', st.session_state.language)):
                    # Add headers that n8n might expect
                    headers = {
                        'User-Agent': 'Yoga-Analytics-Dashboard/1.0',
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                    
                    # Try both GET and POST methods
                    st.info(f"🔗 Attempting to connect to: {webhook_url}")
                    
                    response = None
                    try:
                        # First try GET
                        response = requests.get(webhook_url, headers=headers, timeout=15)
                        if response.status_code == 405:  # Method not allowed
                            st.warning("⚠️ GET method not allowed, trying POST...")
                            # Try POST if GET fails
                            response = requests.post(webhook_url, headers=headers, json={}, timeout=15)
                        
                        response.raise_for_status()
                        
                        # Check if response is empty
                        if not response.content:
                            st.error("❌ Webhook returned empty response. Please check your n8n workflow configuration.")
                            st.info("💡 Make sure your n8n workflow has a 'Respond to Webhook' node that returns the required data format.")
                        else:
                            data = response.json()
                            
                            # Multi-country accumulator system
                            # Check if this is multi-country data (all at once) or single country
                            processor = DataProcessor()
                            
                            # Check for different data formats
                            if isinstance(data, list) and len(data) > 0:
                                first_item = data[0]
                                
                                # Case 1: Single-country request from n8n (array with 1 country object)
                                if len(data) == 1 and isinstance(first_item, dict) and 'country' in first_item:
                                    country = first_item['country']
                                    country_data = first_item['data']
                                    
                                    # Add to accumulator (silently - no UI updates)
                                    all_received = add_country_data(country, country_data)
                                    
                                    if all_received:
                                        # All countries received - process now
                                        st.success("✅ Data loaded successfully!")
                                        processed_data = process_accumulated_data()
                                        if processed_data:
                                            st.session_state.data = processed_data
                                            st.session_state.webhook_url = webhook_url
                                            reset_accumulator()
                                            st.success(get_text('data_fetched_success', st.session_state.language))
                                            st.balloons()  # Celebrate completion
                                        else:
                                            st.error("❌ Failed to process data")
                                            reset_accumulator()
                                    else:
                                        # Still waiting for more countries - don't show any details
                                        # Loading state is already shown in the accumulator status section above
                                        pass
                                
                                # Case 2: Complete multi-country format with explicit country field (3+ countries)
                                elif len(data) >= 3 and all(isinstance(item, dict) and 'country' in item for item in data):
                                    st.info("🔍 Detected complete multi-country format")
                                    processed_data = processor.process_webhook_data(data)
                                    if processed_data:
                                        st.session_state.data = processed_data
                                        st.session_state.webhook_url = webhook_url
                                        st.success(get_text('data_fetched_success', st.session_state.language))
                                        st.rerun()
                                    else:
                                        st.error(get_text('invalid_data_format', st.session_state.language))
                                        with st.expander("🔍 Debug: Show received data structure"):
                                            st.json(data[:2] if len(data) > 2 else data)  # Show first 2 items only
                                            st.info("Check if your data has 'time' field and required metrics fields")
                                
                                # Case 3: n8n array format (3 items, each is a country)
                                elif len(data) == 3 and all(isinstance(item, dict) for item in data):
                                    st.info("🔍 Detected n8n array format with 3 items - processing as multi-country data")
                                    
                                    # Convert n8n format to our expected format
                                    countries_data = process_n8n_array_format(data)
                                    processed_data = processor.process_webhook_data(countries_data)
                                    
                                    if processed_data:
                                        st.session_state.data = processed_data
                                        st.session_state.webhook_url = webhook_url
                                        st.success("✅ Processed 3-country data from n8n array format!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to process n8n array format")
                                
                                # Case 3: Legacy time-series format
                                else:
                                    # Try legacy processing
                                    processed_data = processor.process_webhook_data(data)
                                    if processed_data:
                                        st.session_state.data = processed_data
                                        st.session_state.webhook_url = webhook_url
                                        st.success(get_text('data_fetched_success', st.session_state.language))
                                        st.rerun()
                                    else:
                                        st.error(get_text('invalid_data_format', st.session_state.language))
                                        with st.expander("🔍 Debug: Show received data structure"):
                                            st.json(data[:2] if isinstance(data, list) and len(data) > 2 else data)
                                            st.info("Your data format doesn't match expected format. Check the 'Expected Data Format' section below for the correct structure.")
                            else:
                                # This might be single country data - use accumulator
                                country = detect_country_from_data(data)
                                
                                if country:
                                    # We detected a country - add to accumulator silently
                                    all_received = add_country_data(country, data)
                                    
                                    if all_received:
                                        # All countries received - process now
                                        st.success("✅ Data loaded successfully!")
                                        processed_data = process_accumulated_data()
                                        if processed_data:
                                            st.session_state.data = processed_data
                                            st.session_state.webhook_url = webhook_url
                                            reset_accumulator()
                                            st.success(get_text('data_fetched_success', st.session_state.language))
                                            st.balloons()
                                        else:
                                            st.error("❌ Failed to process data")
                                            reset_accumulator()
                                    else:
                                        # Still waiting - no detailed messages, loading state shown above
                                        pass
                                        
                                else:
                                    # Could not detect country - fail silently and show in loading state
                                    st.error("❌ Could not detect country from data format")
                                
                    except requests.exceptions.HTTPError as e:
                        if response and response.status_code == 404:
                            st.error(get_text('webhook_not_found', st.session_state.language))
                            st.write("• Is your n8n workflow active and saved?")
                            st.write("• Does the webhook URL match exactly?")
                            st.write("• Try copying the webhook URL directly from n8n")
                        elif response and response.status_code == 500:
                            st.error(get_text('server_error', st.session_state.language))
                        else:
                            st.error(f"❌ HTTP Error: {str(e)}")
                            
            except requests.exceptions.ConnectionError:
                st.error(get_text('connection_failed', st.session_state.language))
                st.write("• Is your n8n instance running?")
                st.write("• Can you access the n8n URL in your browser?")
                st.write("• Check your internet connection")
            except requests.exceptions.Timeout:
                st.error(get_text('request_timeout', st.session_state.language))
            except json.JSONDecodeError as e:
                st.error(get_text('invalid_json', st.session_state.language))
                if 'response' in locals() and response is not None:
                    st.write(f"Response content: {response.text[:500]}...")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        else:
            st.error(get_text('enter_webhook_url', st.session_state.language))

# Render dashboard function
def render_dashboard(webhook_data, country_name=""):
    """Render complete dashboard for given data and country."""
    processor = DataProcessor()
    chart_gen = ChartGenerator()
    insights_gen = InsightsGenerator()
    
    # Validate webhook_data
    if webhook_data is None:
        st.error("❌ No data available for this country/tab")
        return
    
    # Add country name to the header if specified
    if country_name and country_name != "All Countries":
        st.subheader(f"🌍 {country_name} Analytics")
    elif country_name == "All Countries":
        st.subheader(f"🌍 All Countries Analytics")
    
    # Check if we have time series data or single data point
    is_time_series = webhook_data.get('is_time_series', False)
    time_periods = webhook_data.get('time_periods', 1)
    all_periods = webhook_data.get('data', [])
    
    # Add Google Analytics-style date range filter
    if is_time_series and len(all_periods) > 1:
        from utils.date_filter import DateRangeFilter
        
        # Create unique filter for each country/tab
        filter_key_prefix = f"{country_name}_" if country_name else ""
        date_filter = DateRangeFilter(key_prefix=filter_key_prefix, data=all_periods)
        
        # Render the filter and get selected range
        st.subheader("📅 Date Range")
        selected_range = date_filter.render()
        
        # Filter the data based on selected range
        filtered_periods = date_filter.filter_data(all_periods, date_field='time')
        
        # Show filter status
        if filtered_periods:
            range_string = date_filter.get_range_string()
            st.success(f"📊 Showing data for: **{range_string}** ({len(filtered_periods)} data points)")
        else:
            st.warning("No data available for the selected date range")
            filtered_periods = []
        
        # Store daily data for Last Week Overview (before aggregation)
        filtered_periods_daily = filtered_periods.copy()
        
        # Adaptive aggregation: If more than 14 days, aggregate to weekly for charts
        if len(filtered_periods) > 14:
            st.info(f"📊 Data range > 14 days detected. Automatically aggregating {len(filtered_periods)} days into weekly periods for better visualization.")
            filtered_periods = processor.aggregate_to_weekly(filtered_periods)
            st.success(f"✅ Aggregated to {len(filtered_periods)} weekly periods for charts")
        
        st.divider()
    else:
        filtered_periods = all_periods
        filtered_periods_daily = all_periods
    
    # Use filtered data for calculations
    aggregated_data = webhook_data.get('aggregated', {}) if not is_time_series else processor._aggregate_time_series_data(filtered_periods)
    latest_data = filtered_periods[-1] if filtered_periods else webhook_data.get('latest_period', {})
    
    # Calculate KPIs from aggregated data (for all other sections)
    kpis = processor.calculate_kpis(aggregated_data)
    
    # Calculate week-over-week KPIs ONLY for the Key Performance section
    if is_time_series and len(filtered_periods) >= 2:
        wow_kpis = processor.calculate_week_over_week_kpis(filtered_periods)
        key_performance_kpis = wow_kpis['current']
        key_performance_deltas = wow_kpis['deltas']
        
        # Get the current and previous week time periods for display
        current_week_time = filtered_periods[-1].get('time', 'Current Week')
        previous_week_time = filtered_periods[-2].get('time', 'Previous Week')
        
        # Combined KPI & Weekly Metrics Section
        st.header(get_text('key_performance_header', st.session_state.language))
        st.info(get_text('latest_week', st.session_state.language, current=current_week_time, previous=previous_week_time))
    else:
        # Fallback for Key Performance section if not enough periods
        key_performance_kpis = kpis
        key_performance_deltas = {}
        
        # Combined KPI & Weekly Metrics Section
        st.header(get_text('key_performance_header', st.session_state.language))
    
    # Subheader for Top 5 KPIs
    st.subheader(get_text('kpi_overview_subheader', st.session_state.language))
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        delta_val = f"{key_performance_deltas.get('total_new_users', 0):+.1%}" if key_performance_deltas.get('total_new_users') else None
        st.metric(
            label=get_text('total_new_users', st.session_state.language),
            value=f"{key_performance_kpis['total_new_users']:,}",
            delta=delta_val
        )
    
    with col2:
        delta_val = f"{key_performance_deltas.get('retention_rate', 0):+.1%}" if key_performance_deltas.get('retention_rate') else None
        st.metric(
            label=get_text('user_retention_rate', st.session_state.language),
            value=f"{key_performance_kpis['retention_rate']:.1%}",
            delta=delta_val
        )
    
    with col3:
        delta_val = f"{key_performance_deltas.get('churn_rate', 0):+.1%}" if key_performance_deltas.get('churn_rate') else None
        st.metric(
            label=get_text('churn_rate', st.session_state.language),
            value=f"{key_performance_kpis['churn_rate']:.1%}",
            delta=delta_val,
            delta_color="inverse"
        )
    
    with col4:
        delta_val = f"{key_performance_deltas.get('active_sessions', 0):+.1%}" if key_performance_deltas.get('active_sessions') else None
        st.metric(
            label=get_text('active_sessions', st.session_state.language),
            value=f"{key_performance_kpis['active_sessions']:,}",
            delta=delta_val
        )
    
    with col5:
        delta_val = f"{key_performance_deltas.get('engagement_rate', 0):+.1%}" if key_performance_deltas.get('engagement_rate') else None
        st.metric(
            label=get_text('engagement_rate', st.session_state.language),
            value=f"{key_performance_kpis['engagement_rate']:.1%}",
            delta=delta_val
        )
    
    # Show All Metrics section - Show total metrics for last 7 days
    # Always use daily data (not aggregated weekly) for this section
    if is_time_series and len(filtered_periods_daily) >= 7:
        st.markdown("---")  # Visual separator
        st.subheader(get_text('all_metrics_subheader', st.session_state.language))
        
        # Get last 7 days of data from daily data
        last_7_days = processor.get_last_n_days(filtered_periods_daily, n=7)
        
        # Aggregate the 7 days
        last_week_total = {}
        for field in processor.required_fields + processor.optional_fields:
            if field == 'time':
                last_week_total[field] = f"{last_7_days[0].get('time', '')} - {last_7_days[-1].get('time', '')}"
            elif field == 'avg_engage_time':
                # Average engagement time
                values = [day.get(field, 0) for day in last_7_days if day.get(field, 0) > 0]
                last_week_total[field] = sum(values) / len(values) if values else 0
            else:
                # Sum all other fields
                last_week_total[field] = sum(day.get(field, 0) for day in last_7_days)
        
        # Display metrics grouped by category with containers and borders
        
        # User Activity Group
        with st.container(border=True):
            st.markdown("##### 👥 User Activity")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("New Users", f"{int(last_week_total.get('first_open', 0)):,}")
            with col2:
                st.metric("Sessions", f"{int(last_week_total.get('session_start', 0)):,}")
            with col3:
                st.metric("App Opens", f"{int(last_week_total.get('app_open', 0)):,}")
            with col4:
                st.metric("Logins", f"{int(last_week_total.get('login', 0)):,}")
            with col5:
                st.metric("Uninstalls", f"{int(last_week_total.get('app_remove', 0)):,}")
        
        # Practice & Engagement Group
        with st.container(border=True):
            st.markdown("##### 🏃‍♀️ Practice & Engagement")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Exercise Views", f"{int(last_week_total.get('view_exercise', 0)):,}")
            with col2:
                st.metric("Video Practice", f"{int(last_week_total.get('practice_with_video', 0)):,}")
            with col3:
                st.metric("AI Practice", f"{int(last_week_total.get('practice_with_ai', 0)):,}")
            with col4:
                st.metric("AI Chat", f"{int(last_week_total.get('chat_ai', 0)):,}")
            with col5:
                avg_time_formatted = processor.format_engagement_time(last_week_total.get('avg_engage_time', 0))
                st.metric("Avg. Engagement", avg_time_formatted)
        
        # Features & Content Group
        with st.container(border=True):
            st.markdown("##### 🎯 Features & Content")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Health Surveys", f"{int(last_week_total.get('health_survey', 0)):,}")
            with col2:
                st.metric("Roadmap Views", f"{int(last_week_total.get('view_roadmap', 0)):,}")
            with col3:
                st.metric("Store Views", f"{int(last_week_total.get('store_subscription', 0)):,}")
        
        # Popup Performance Group
        with st.container(border=True):
            st.markdown("##### 💬 Popup Performance")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Shown", f"{int(last_week_total.get('show_popup', 0)):,}")
            with col2:
                st.metric("Details Viewed", f"{int(last_week_total.get('view_detail_popup', 0)):,}")
            with col3:
                st.metric("Closed", f"{int(last_week_total.get('close_popup', 0)):,}")
            with col4:
                popup_ctr = (last_week_total.get('view_detail_popup', 0) / last_week_total.get('show_popup', 1)) * 100 if last_week_total.get('show_popup', 0) > 0 else 0
                st.metric("CTR", f"{popup_ctr:.1f}%")
        
        # Monetization Group
        with st.container(border=True):
            st.markdown("##### 💰 Monetization")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("In-App Purchases", f"{int(last_week_total.get('in_app_purchase', 0)):,}")
            with col2:
                conversion_rate = (last_week_total.get('in_app_purchase', 0) / last_week_total.get('store_subscription', 1)) * 100 if last_week_total.get('store_subscription', 0) > 0 else 0
                st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
            with col3:
                st.metric("Total Revenue Events", f"{int(last_week_total.get('in_app_purchase', 0) + last_week_total.get('store_subscription', 0)):,}")
    
    elif is_time_series and len(filtered_periods_daily) > 0:
        # If less than 7 days, show what we have with same beautiful design
        st.markdown("---")  # Visual separator
        st.subheader(get_text('all_metrics_subheader', st.session_state.language))
        st.info(f"📊 Showing data for {len(filtered_periods_daily)} day(s). Need at least 7 days for full weekly overview.")
        
        # Aggregate available days from daily data
        available_days = filtered_periods_daily
        days_total = {}
        for field in processor.required_fields + processor.optional_fields:
            if field == 'time':
                days_total[field] = f"{available_days[0].get('time', '')} - {available_days[-1].get('time', '')}"
            elif field == 'avg_engage_time':
                values = [day.get(field, 0) for day in available_days if day.get(field, 0) > 0]
                days_total[field] = sum(values) / len(values) if values else 0
            else:
                days_total[field] = sum(day.get(field, 0) for day in available_days)
        
        # User Activity Group
        with st.container(border=True):
            st.markdown("##### 👥 User Activity")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("New Users", f"{int(days_total.get('first_open', 0)):,}")
            with col2:
                st.metric("Sessions", f"{int(days_total.get('session_start', 0)):,}")
            with col3:
                st.metric("App Opens", f"{int(days_total.get('app_open', 0)):,}")
            with col4:
                st.metric("Logins", f"{int(days_total.get('login', 0)):,}")
            with col5:
                st.metric("Uninstalls", f"{int(days_total.get('app_remove', 0)):,}")
        
        # Practice & Engagement Group
        with st.container(border=True):
            st.markdown("##### 🏃‍♀️ Practice & Engagement")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Exercise Views", f"{int(days_total.get('view_exercise', 0)):,}")
            with col2:
                st.metric("Video Practice", f"{int(days_total.get('practice_with_video', 0)):,}")
            with col3:
                st.metric("AI Practice", f"{int(days_total.get('practice_with_ai', 0)):,}")
            with col4:
                st.metric("AI Chat", f"{int(days_total.get('chat_ai', 0)):,}")
            with col5:
                avg_time_formatted = processor.format_engagement_time(days_total.get('avg_engage_time', 0))
                st.metric("Avg. Engagement", avg_time_formatted)
        
        # Features & Content Group
        with st.container(border=True):
            st.markdown("##### 🎯 Features & Content")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Health Surveys", f"{int(days_total.get('health_survey', 0)):,}")
            with col2:
                st.metric("Roadmap Views", f"{int(days_total.get('view_roadmap', 0)):,}")
            with col3:
                st.metric("Store Views", f"{int(days_total.get('store_subscription', 0)):,}")
        
        # Popup Performance Group
        with st.container(border=True):
            st.markdown("##### 💬 Popup Performance")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Shown", f"{int(days_total.get('show_popup', 0)):,}")
            with col2:
                st.metric("Details Viewed", f"{int(days_total.get('view_detail_popup', 0)):,}")
            with col3:
                st.metric("Closed", f"{int(days_total.get('close_popup', 0)):,}")
            with col4:
                popup_ctr = (days_total.get('view_detail_popup', 0) / days_total.get('show_popup', 1)) * 100 if days_total.get('show_popup', 0) > 0 else 0
                st.metric("CTR", f"{popup_ctr:.1f}%")
        
        # Monetization Group
        with st.container(border=True):
            st.markdown("##### 💰 Monetization")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("In-App Purchases", f"{int(days_total.get('in_app_purchase', 0)):,}")
            with col2:
                conversion_rate = (days_total.get('in_app_purchase', 0) / days_total.get('store_subscription', 1)) * 100 if days_total.get('store_subscription', 0) > 0 else 0
                st.metric("Conversion Rate", f"{conversion_rate:.1f}%")
            with col3:
                st.metric("Total Revenue Events", f"{int(days_total.get('in_app_purchase', 0) + days_total.get('store_subscription', 0)):,}")
    
    # Add divider after the combined KPI section
    st.divider()
    
    # Charts Section
    st.header(get_text('analytics_overview_header', st.session_state.language))
    
    # Create unique key prefix for all charts
    chart_key_prefix = f"{country_name}_" if country_name else ""
    
    if is_time_series:
        # Time Series Charts for weekly data
        st.subheader(get_text('time_series_analysis', st.session_state.language))
        
        # Create time series chart using filtered data
        time_series_chart = chart_gen.create_time_series_chart(filtered_periods, st.session_state.language)
        st.plotly_chart(time_series_chart, use_container_width=True, key=f"{chart_key_prefix}time_series")
        
        # User Acquisition vs Churn over time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(get_text('user_flow_trends', st.session_state.language))
            flow_chart = chart_gen.create_user_flow_trends_chart(filtered_periods, st.session_state.language)
            st.plotly_chart(flow_chart, use_container_width=True, key=f"{chart_key_prefix}flow_trends")
        
        with col2:
            st.subheader(get_text('user_activity_comparison_title', st.session_state.language))
            user_activity_chart = chart_gen.create_user_activity_comparison(filtered_periods, st.session_state.language)
            st.plotly_chart(user_activity_chart, use_container_width=True, key=f"{chart_key_prefix}user_activity")
        
        st.divider()
        
        # Weekly breakdown using filtered data
        if len(filtered_periods) > 1:
            st.subheader(get_text('weekly_breakdown_header', st.session_state.language))
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(get_text('best_week_new_users_text', st.session_state.language))
                best_week = max(filtered_periods, key=lambda x: x.get('first_open', 0))
                st.write(f"{get_text('week_colon', st.session_state.language)} {best_week.get('time', 'N/A')}")
                st.write(f"{get_text('new_users_colon', st.session_state.language)} {best_week.get('first_open', 0)}")
            
            with col2:
                st.markdown(get_text('most_engaged_week_text', st.session_state.language))
                most_engaged = max(filtered_periods, key=lambda x: x.get('practice_with_video', 0) + x.get('practice_with_ai', 0))
                st.write(f"{get_text('week_colon', st.session_state.language)} {most_engaged.get('time', 'N/A')}")
                st.write(f"{get_text('practice_sessions_colon', st.session_state.language)} {most_engaged.get('practice_with_video', 0) + most_engaged.get('practice_with_ai', 0)}")
            
            with col3:
                st.markdown(get_text('top_ai_week_text', st.session_state.language))
                top_ai = max(filtered_periods, key=lambda x: x.get('chat_ai', 0))
                st.write(f"{get_text('week_colon', st.session_state.language)} {top_ai.get('time', 'N/A')}")
                st.write(f"{get_text('ai_interactions_colon', st.session_state.language)} {top_ai.get('chat_ai', 0)}")
    
    # Current period or aggregated charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Feature Adoption Funnel (replaced acquisition vs churn chart)
        chart_title = get_text('feature_adoption_analysis', st.session_state.language) if not is_time_series else get_text('overall_user_metrics', st.session_state.language)
        st.subheader(chart_title)
        feature_funnel_chart = chart_gen.create_feature_adoption_funnel(aggregated_data, st.session_state.language)
        st.plotly_chart(feature_funnel_chart, use_container_width=True, key=f"{chart_key_prefix}feature_funnel")
    
    with col2:
        st.subheader(get_text('user_funnel_analysis_title', st.session_state.language))
        funnel_chart = chart_gen.create_user_funnel_analysis(aggregated_data, st.session_state.language)
        st.plotly_chart(funnel_chart, use_container_width=True, key=f"{chart_key_prefix}user_funnel")
    
    # Feature Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text('feature_usage_analysis', st.session_state.language))
        feature_chart = chart_gen.create_feature_usage_chart(aggregated_data, st.session_state.language)
        st.plotly_chart(feature_chart, use_container_width=True, key=f"{chart_key_prefix}feature")
    
    with col2:
        st.subheader(get_text('churn_risk_indicator_title', st.session_state.language))
        churn_risk_chart = chart_gen.create_churn_risk_indicator(aggregated_data, st.session_state.language)
        st.plotly_chart(churn_risk_chart, use_container_width=True, key=f"{chart_key_prefix}churn_risk")
    
    # Popup Performance
    st.subheader(get_text('popup_performance_header', st.session_state.language))
    col1, col2, col3 = st.columns(3)
    
    popup_metrics = processor.calculate_popup_metrics(aggregated_data)
    
    with col1:
        st.metric(
            label=get_text('total_popups_shown', st.session_state.language),
            value=f"{popup_metrics['total_shown']:,}"
        )
    
    with col2:
        st.metric(
            label=get_text('detail_views', st.session_state.language),
            value=f"{popup_metrics['detail_views']:,}"
        )
    
    with col3:
        st.metric(
            label=get_text('conversion_rate', st.session_state.language),
            value=f"{popup_metrics['conversion_rate']:.1%}"
        )
    
    popup_chart = chart_gen.create_popup_performance_chart(aggregated_data, st.session_state.language)
    st.plotly_chart(popup_chart, use_container_width=True, key=f"{chart_key_prefix}popup")
    
    st.divider()
    
    # Insights Panel
    st.header(get_text('insights_header', st.session_state.language))
    
    # Prepare data for split insights
    if is_time_series and len(filtered_periods) >= 2:
        # Use filtered data for "Overall" and recent 2 weeks for "This Week"
        recent_periods = filtered_periods[-2:]
        recent_aggregated = processor._aggregate_time_series_data(recent_periods)
        recent_kpis = processor.calculate_kpis(recent_aggregated)
        
        # Generate split insights
        split_insights = insights_gen.generate_split_insights(
            overall_data=aggregated_data, 
            overall_kpis=kpis,
            recent_data=recent_aggregated,
            recent_kpis=recent_kpis,
            language=st.session_state.language
        )
        
        # Display split insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(get_text('overall_insights', st.session_state.language))
            st.markdown(f"*{get_text('overall_insights_subtitle', st.session_state.language)}*")
            for sentiment, insight in split_insights['overall']['key_insights']:
                if sentiment == "positive":
                    st.success(f"✅ {insight}")
                elif sentiment == "negative":
                    st.error(f"⚠️ {insight}")
                else:  # neutral
                    st.info(f"💡 {insight}")
        
        with col2:
            st.subheader(get_text('this_week_insights', st.session_state.language)) 
            st.markdown(f"*{get_text('this_week_insights_subtitle', st.session_state.language)}*")
            for sentiment, insight in split_insights['this_week']['key_insights']:
                if sentiment == "positive":
                    st.success(f"✅ {insight}")
                elif sentiment == "negative":
                    st.error(f"⚠️ {insight}")
                else:  # neutral
                    st.info(f"💡 {insight}")
        
        # Recommendations section (unified)
        st.subheader(get_text('recommendations_header', st.session_state.language))
        # Combine and deduplicate recommendations from both overall and recent insights
        all_recommendations = set()
        all_recommendations.update(split_insights['overall'].get('recommendations', []))
        all_recommendations.update(split_insights['this_week'].get('recommendations', []))
        
        for recommendation in sorted(all_recommendations):
            st.info(f"💡 {recommendation}")
    
    else:
        # Single period or no time series - use basic insights
        insights = insights_gen.generate_insights(aggregated_data, kpis, st.session_state.language)
        for sentiment, insight in insights['key_insights']:
            if sentiment == "positive":
                st.success(f"✅ {insight}")
            elif sentiment == "negative":
                st.error(f"⚠️ {insight}")
            else:  # neutral
                st.info(f"💡 {insight}")
        
        st.subheader(get_text('recommendations_header', st.session_state.language))
        for recommendation in insights.get('recommendations', []):
            st.info(f"💡 {recommendation}")
    
    st.divider()
    
    # Feature Performance Analysis Section
    st.header(get_text('feature_performance_header', st.session_state.language))
    
    adoption_data = processor.calculate_feature_adoption(aggregated_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(get_text('most_used_features', st.session_state.language))
        for feature, usage in adoption_data['most_used']:
            st.write(f"• {feature}: {usage}")
    
    with col2:
        st.markdown(get_text('growing_features', st.session_state.language))
        for feature, growth in adoption_data['growing'][:3]:
            st.write(f"• {feature}: +{growth:.1%}")
    
    with col3:
        st.markdown(get_text('underutilized_features', st.session_state.language))
        for feature, usage in adoption_data['least_used'][:3]:
            st.write(f"• {feature}: {usage}")
    
    st.divider()
    
    # Export Section
    st.header(get_text('export_header', st.session_state.language))
    col1, col2, col3 = st.columns(3)
    
    # Use unique keys for export buttons to avoid conflicts between tabs
    export_key_prefix = f"{country_name}_" if country_name else ""
    
    with col1:
        if st.button(get_text('export_raw_data', st.session_state.language), key=f"{export_key_prefix}export_csv"):
            csv_data = processor.export_to_csv(aggregated_data)
            st.download_button(
                label=get_text('download_csv', st.session_state.language),
                data=csv_data,
                file_name=f"yoga_app_analytics_{country_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key=f"{export_key_prefix}download_csv"
            )
    
    with col2:
        if st.button(get_text('export_kpis', st.session_state.language), key=f"{export_key_prefix}export_kpis"):
            json_data = json.dumps(kpis, indent=2)
            st.download_button(
                label=get_text('download_kpis', st.session_state.language),
                data=json_data,
                file_name=f"yoga_app_kpis_{country_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key=f"{export_key_prefix}download_kpis"
            )
    
    with col3:
        if st.button(get_text('export_insights_txt', st.session_state.language), key=f"{export_key_prefix}export_insights"):
            # Generate insights for export if not already available
            if 'insights' not in locals():
                insights = insights_gen.generate_insights(aggregated_data, kpis, st.session_state.language)
            insights_text = insights_gen.export_insights_text(insights)
            st.download_button(
                label="Download Insights",
                data=insights_text,
                file_name=f"yoga_app_insights_{country_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                key=f"{export_key_prefix}download_insights"
            )

# Main dashboard
if st.session_state.data:
    countries_data = st.session_state.data
    
    # Check if we have country-based data (new format)
    if isinstance(countries_data, dict) and any(key in ['US', 'India', 'VN', 'All Countries'] for key in countries_data.keys()):
        # New country-based format - create tabs
        available_countries = [key for key in countries_data.keys() if key != 'All Countries']
        available_countries.sort()  # Sort for consistent order
        
        # Create dropdown options with Vietnamese labels
        country_options = {}
        for country in available_countries:
            if country == 'US':
                country_options["🇺🇸 USA"] = country
            elif country == 'India':
                country_options["🇮🇳 Ấn Độ"] = country
            elif country == 'VN':
                country_options["🇻🇳 Việt Nam"] = country
            else:
                country_options[f"🌍 {country}"] = country
        
        # Add "All Countries" option if it exists
        if 'All Countries' in countries_data:
            country_options["🌎 Tổng Hợp"] = 'All Countries'
        
        # Initialize session state for country selection
        if 'selected_country' not in st.session_state:
            st.session_state.selected_country = list(country_options.values())[0]
        
        # Country selector dropdown
        st.subheader("🌍 Chọn Quốc Gia/Khu Vực")
        selected_display = st.selectbox(
            "Xem analytics cho:",
            options=list(country_options.keys()),
            index=list(country_options.values()).index(st.session_state.selected_country),
            key="country_selector"
        )
        
        # Update selected country
        selected_country = country_options[selected_display]
        st.session_state.selected_country = selected_country
        
        st.divider()
        
        # Render dashboard for selected country
        if selected_country in countries_data:
            render_dashboard(countries_data[selected_country], selected_country)
        else:
            st.error(f"❌ Không có dữ liệu cho {selected_display}")
    
    else:
        # Legacy format - render single dashboard
        render_dashboard(st.session_state.data)


else:
    # Empty state
    st.info("👆 Please enter your webhook URL and click 'Fetch Data' to begin analyzing your yoga app metrics.")
    
    # Show sample data structure and n8n setup guide
    with st.expander("📋 Expected Data Format"):
        st.code("""
{
  "time": "1/7/2025 - 7/7/2025",
  "first_open": 3,
  "app_remove": 5,
  "session_start": 9,
  "app_open": 6,
  "login": 9,
  "view_exercise": 9,
  "health_survey": 9,
  "view_roadmap": 1,
  "practice_with_video": 3,
  "practice_with_ai": 3,
  "chat_ai": 2,
  "show_popup": 9,
  "view_detail_popup": 9,
  "close_popup": 9
}
        """, language="json")
    
    with st.expander("🔧 n8n Webhook Setup Guide"):
        st.markdown("""
        **To set up your n8n webhook correctly:**
        
        1. **Create a new workflow** in your n8n instance
        2. **Add a Webhook node** as the trigger:
           - Set HTTP Method to `GET` or `POST`
           - Leave Authentication as `None`
           - Copy the generated webhook URL
        
        3. **Add your data source** (e.g., database query, API call, etc.)
        
        4. **Add a 'Respond to Webhook' node** at the end:
           - Set Response Code to `200`
           - Set Response Body to return the JSON data format shown above
        
        5. **Activate your workflow** (click the toggle switch)
        
        6. **Test the webhook** by visiting the URL in your browser - you should see the JSON response
        
        **Common Issues:**
        - ❌ Workflow not activated → Click the toggle to activate
        - ❌ Missing 'Respond to Webhook' node → Webhook will return empty response
        - ❌ Wrong data format → Check the expected format above
        - ❌ n8n Cloud URL format → Use the full webhook URL from n8n
        
        **Example n8n Cloud URL format:**
        `https://yourinstance.app.n8n.cloud/webhook/your-webhook-id`
        """)
    
    # Add test data button for demonstration
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🧪 Load Sample Data (for testing)"):
            # Create sample data in new country-based format (3 countries as webhook will send)
            sample_country_data = [
                {
                    "country": "US", 
                    "data": [
                        {"time": "07/10/2024", "first_open": 45, "app_remove": 12, "session_start": 85, "app_open": 62, "login": 75, "view_exercise": 82, "health_survey": 68, "view_roadmap": 22, "practice_with_video": 42, "practice_with_ai": 35, "chat_ai": 28, "show_popup": 65, "view_detail_popup": 38, "close_popup": 52},
                        {"time": "14/10/2024", "first_open": 52, "app_remove": 8, "session_start": 95, "app_open": 58, "login": 68, "view_exercise": 78, "health_survey": 62, "view_roadmap": 15, "practice_with_video": 48, "practice_with_ai": 32, "chat_ai": 25, "show_popup": 72, "view_detail_popup": 45, "close_popup": 58},
                        {"time": "21/10/2024", "first_open": 38, "app_remove": 18, "session_start": 72, "app_open": 65, "login": 78, "view_exercise": 85, "health_survey": 65, "view_roadmap": 28, "practice_with_video": 52, "practice_with_ai": 42, "chat_ai": 35, "show_popup": 68, "view_detail_popup": 42, "close_popup": 62},
                        {"time": "28/10/2024", "first_open": 48, "app_remove": 10, "session_start": 88, "app_open": 70, "login": 82, "view_exercise": 88, "health_survey": 72, "view_roadmap": 30, "practice_with_video": 55, "practice_with_ai": 45, "chat_ai": 38, "show_popup": 75, "view_detail_popup": 48, "close_popup": 65},
                        {"time": "04/11/2024", "first_open": 55, "app_remove": 7, "session_start": 92, "app_open": 75, "login": 85, "view_exercise": 90, "health_survey": 75, "view_roadmap": 32, "practice_with_video": 58, "practice_with_ai": 48, "chat_ai": 40, "show_popup": 78, "view_detail_popup": 50, "close_popup": 68},
                        {"time": "11/11/2024", "first_open": 60, "app_remove": 5, "session_start": 98, "app_open": 80, "login": 88, "view_exercise": 92, "health_survey": 78, "view_roadmap": 35, "practice_with_video": 62, "practice_with_ai": 52, "chat_ai": 42, "show_popup": 82, "view_detail_popup": 52, "close_popup": 70},
                        {"time": "18/11/2024", "first_open": 42, "app_remove": 15, "session_start": 75, "app_open": 68, "login": 72, "view_exercise": 80, "health_survey": 70, "view_roadmap": 25, "practice_with_video": 48, "practice_with_ai": 38, "chat_ai": 32, "show_popup": 70, "view_detail_popup": 45, "close_popup": 60}
                    ]
                },
                {
                    "country": "India", 
                    "data": [
                        {"time": "07/10/2024", "first_open": 32, "app_remove": 6, "session_start": 58, "app_open": 42, "login": 48, "view_exercise": 52, "health_survey": 45, "view_roadmap": 15, "practice_with_video": 28, "practice_with_ai": 22, "chat_ai": 18, "show_popup": 42, "view_detail_popup": 25, "close_popup": 35},
                        {"time": "14/10/2024", "first_open": 38, "app_remove": 4, "session_start": 65, "app_open": 38, "login": 42, "view_exercise": 48, "health_survey": 38, "view_roadmap": 8, "practice_with_video": 32, "practice_with_ai": 18, "chat_ai": 15, "show_popup": 48, "view_detail_popup": 28, "close_popup": 38},
                        {"time": "21/10/2024", "first_open": 28, "app_remove": 10, "session_start": 45, "app_open": 42, "login": 48, "view_exercise": 52, "health_survey": 42, "view_roadmap": 18, "practice_with_video": 35, "practice_with_ai": 25, "chat_ai": 22, "show_popup": 45, "view_detail_popup": 28, "close_popup": 38},
                        {"time": "28/10/2024", "first_open": 35, "app_remove": 5, "session_start": 60, "app_open": 45, "login": 52, "view_exercise": 55, "health_survey": 48, "view_roadmap": 20, "practice_with_video": 38, "practice_with_ai": 28, "chat_ai": 25, "show_popup": 50, "view_detail_popup": 32, "close_popup": 42},
                        {"time": "04/11/2024", "first_open": 40, "app_remove": 4, "session_start": 68, "app_open": 50, "login": 55, "view_exercise": 58, "health_survey": 50, "view_roadmap": 22, "practice_with_video": 42, "practice_with_ai": 32, "chat_ai": 28, "show_popup": 55, "view_detail_popup": 35, "close_popup": 45},
                        {"time": "11/11/2024", "first_open": 45, "app_remove": 3, "session_start": 72, "app_open": 55, "login": 60, "view_exercise": 62, "health_survey": 52, "view_roadmap": 25, "practice_with_video": 45, "practice_with_ai": 35, "chat_ai": 30, "show_popup": 58, "view_detail_popup": 38, "close_popup": 48},
                        {"time": "18/11/2024", "first_open": 30, "app_remove": 8, "session_start": 50, "app_open": 40, "login": 45, "view_exercise": 50, "health_survey": 43, "view_roadmap": 17, "practice_with_video": 30, "practice_with_ai": 24, "chat_ai": 20, "show_popup": 44, "view_detail_popup": 27, "close_popup": 36}
                    ]
                },
                {
                    "country": "VN", 
                    "data": [
                        {"time": "07/10/2024", "first_open": 18, "app_remove": 3, "session_start": 32, "app_open": 22, "login": 28, "view_exercise": 28, "health_survey": 25, "view_roadmap": 8, "practice_with_video": 15, "practice_with_ai": 12, "chat_ai": 10, "show_popup": 22, "view_detail_popup": 12, "close_popup": 18},
                        {"time": "14/10/2024", "first_open": 22, "app_remove": 2, "session_start": 38, "app_open": 18, "login": 25, "view_exercise": 25, "health_survey": 22, "view_roadmap": 5, "practice_with_video": 18, "practice_with_ai": 10, "chat_ai": 8, "show_popup": 28, "view_detail_popup": 15, "close_popup": 22},
                        {"time": "21/10/2024", "first_open": 15, "app_remove": 5, "session_start": 28, "app_open": 22, "login": 25, "view_exercise": 28, "health_survey": 22, "view_roadmap": 12, "practice_with_video": 20, "practice_with_ai": 15, "chat_ai": 12, "show_popup": 25, "view_detail_popup": 15, "close_popup": 20},
                        {"time": "28/10/2024", "first_open": 20, "app_remove": 2, "session_start": 35, "app_open": 25, "login": 30, "view_exercise": 32, "health_survey": 28, "view_roadmap": 10, "practice_with_video": 22, "practice_with_ai": 17, "chat_ai": 14, "show_popup": 30, "view_detail_popup": 18, "close_popup": 25},
                        {"time": "04/11/2024", "first_open": 25, "app_remove": 2, "session_start": 42, "app_open": 30, "login": 35, "view_exercise": 38, "health_survey": 32, "view_roadmap": 12, "practice_with_video": 25, "practice_with_ai": 20, "chat_ai": 16, "show_popup": 35, "view_detail_popup": 20, "close_popup": 28},
                        {"time": "11/11/2024", "first_open": 28, "app_remove": 1, "session_start": 48, "app_open": 35, "login": 38, "view_exercise": 42, "health_survey": 35, "view_roadmap": 15, "practice_with_video": 28, "practice_with_ai": 22, "chat_ai": 18, "show_popup": 38, "view_detail_popup": 22, "close_popup": 30},
                        {"time": "18/11/2024", "first_open": 16, "app_remove": 4, "session_start": 30, "app_open": 20, "login": 26, "view_exercise": 30, "health_survey": 24, "view_roadmap": 9, "practice_with_video": 16, "practice_with_ai": 13, "chat_ai": 11, "show_popup": 24, "view_detail_popup": 14, "close_popup": 19}
                    ]
                }
            ]
            
            # Process the sample data using the new country-based format
            processor = DataProcessor()
            processed_sample = processor.process_webhook_data(sample_country_data)
            
            st.session_state.data = processed_sample
            st.success("✅ Sample data với 3 countries (US, India, VN) đã được load! Bạn có thể test dropdown selector.")
            st.rerun()
    
    with col2:
        st.info("💡 **Tip:** Use sample data to explore dashboard features while setting up your webhook.")
        
        # Test accumulator system
        st.markdown("**🧪 Test Multi-Country Accumulator:**")
        st.caption("Simulate n8n single-country webhook calls")
        
        test_col1, test_col2, test_col3 = st.columns(3)
        
        with test_col1:
            if st.button("📨 Send US Request", key="test_us_request"):
                # Simulate n8n single-country format
                us_request = [
                    {
                        "country": "US",
                        "data": [
                            {"time": "11/08/2025 - 17/08/2025", "first_open": 45, "app_remove": 12, "session_start": 85, "app_open": 62, "login": 75, "view_exercise": 82, "health_survey": 68, "view_roadmap": 22, "practice_with_video": 42, "practice_with_ai": 35, "chat_ai": 28, "show_popup": 65, "view_detail_popup": 38, "close_popup": 52, "store_subscription": 5, "in_app_purchase": 2, "renew": 2, "revenue": 15000, "active_time": 800}
                        ]
                    }
                ]
                
                # Simulate webhook processing logic
                processor = DataProcessor()
                data = us_request
                first_item = data[0]
                
                if len(data) == 1 and isinstance(first_item, dict) and 'country' in first_item:
                    country = first_item['country']
                    country_data = first_item['data']
                    all_received = add_country_data(country, country_data)
                    st.info(f"✅ Added {country} data to accumulator")
                
                st.rerun()
        
        with test_col2:
            if st.button("📨 Send India Request", key="test_india_request"):
                # Simulate n8n single-country format
                india_request = [
                    {
                        "country": "India",
                        "data": [
                            {"time": "11/08/2025 - 17/08/2025", "first_open": 32, "app_remove": 6, "session_start": 58, "app_open": 42, "login": 48, "view_exercise": 52, "health_survey": 45, "view_roadmap": 15, "practice_with_video": 28, "practice_with_ai": 22, "chat_ai": 18, "show_popup": 42, "view_detail_popup": 25, "close_popup": 35, "store_subscription": 3, "in_app_purchase": 1, "renew": 1, "revenue": 8000, "active_time": 600}
                        ]
                    }
                ]
                
                # Simulate webhook processing logic
                processor = DataProcessor()
                data = india_request
                first_item = data[0]
                
                if len(data) == 1 and isinstance(first_item, dict) and 'country' in first_item:
                    country = first_item['country']
                    country_data = first_item['data']
                    all_received = add_country_data(country, country_data)
                    st.info(f"✅ Added {country} data to accumulator")
                
                st.rerun()
        
        with test_col3:
            if st.button("📨 Send VN Request", key="test_vn_request"):
                # Simulate n8n single-country format (same as user's data)
                vn_request = [
                    {
                        "country": "VN",
                        "data": [
                            {"time": "17/08/2025", "first_open": 35, "app_remove": 3, "session_start": 56, "app_open": 12, "login": 6, "view_exercise": 20, "health_survey": 12, "view_roadmap": 4, "practice_with_video": 10, "practice_with_ai": 4, "chat_ai": 10, "show_popup": 0, "view_detail_popup": 0, "close_popup": 0, "store_subscription": 3, "in_app_purchase": 1, "renew": 1, "revenue": 9000, "active_time": 505}
                        ]
                    }
                ]
                
                # Simulate webhook processing logic
                processor = DataProcessor()
                data = vn_request
                first_item = data[0]
                
                if len(data) == 1 and isinstance(first_item, dict) and 'country' in first_item:
                    country = first_item['country']
                    country_data = first_item['data']
                    all_received = add_country_data(country, country_data)
                    st.info(f"✅ Added {country} data to accumulator")
                    
                    if all_received:
                        # Auto-process when all received
                        processed_data = process_accumulated_data()
                        if processed_data:
                            st.session_state.data = processed_data
                            reset_accumulator()
                            st.success("🎉 All 3 countries collected and processed!")
                
                st.rerun()

# Sidebar with additional controls
@st.dialog("📊 Input Data (JSON)")
def show_input_dialog():
    """Display the current data in JSON format in a dialog."""
    if st.session_state.data:
        st.json(st.session_state.data)
    else:
        st.warning("No data available")

with st.sidebar:
    st.title("🎛️ Dashboard Controls")
    
    if st.session_state.data:
        st.success("✅ Data Loaded")
        
        # Show Input button - opens dialog
        if st.button("📊 Show Input", key="show_input_btn", use_container_width=True):
            show_input_dialog()
        
        if st.button("🗑️ Clear Data", key="clear_data_btn", use_container_width=True):
            st.session_state.data = None
            st.session_state.webhook_url = ""
            st.rerun()
    else:
        st.warning("⚠️ No data loaded")
    
    st.divider()
    
    st.markdown("### 📖 About")
    st.markdown("""
    This dashboard provides comprehensive analytics for yoga app user engagement:
    
    - **Real-time data** from n8n webhooks
    - **KPI tracking** for user retention
    - **Feature usage** analysis
    - **AI engagement** metrics
    - **Popup performance** monitoring
    - **Actionable insights** for optimization
    """)
    
    st.markdown("### 🎨 Theme")
    st.markdown("""
    - Primary: Soft Teal (#4FD1C7)
    - Secondary: Lavender (#B19CD9)
    - Accent: Sage Green (#87A96B)
    """)
