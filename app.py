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
            st.plotly_chart(user_activity_chart, width="stretch")
            
            st.subheader(f"2. {get_text('user_funnel_analysis_title', st.session_state.language)}")
            funnel_chart = chart_gen.create_user_funnel_analysis(aggregated_data, st.session_state.language)
            st.plotly_chart(funnel_chart, width="stretch")
            
            st.subheader(f"3. {get_text('churn_risk_indicator_title', st.session_state.language)}")
            churn_risk_chart = chart_gen.create_churn_risk_indicator(aggregated_data, st.session_state.language)
            st.plotly_chart(churn_risk_chart, width="stretch")
            
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
        if st.button("🔄 Try Again", key="reset_after_timeout", width="stretch"):
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

# Dialog functions
@st.dialog("ℹ️ Churn Risk Indicator Explanation")
def show_churn_risk_explanation(language='en'):
    """Display the churn risk indicator explanation in a dialog."""
    from utils.translations import get_text
    st.markdown(get_text('churn_risk_explanation', language))

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
            st.markdown(f"##### {get_text('user_activity_group', st.session_state.language)}")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric(get_text('new_users_metric', st.session_state.language), f"{int(last_week_total.get('first_open', 0)):,}")
            with col2:
                st.metric(get_text('sessions_metric', st.session_state.language), f"{int(last_week_total.get('session_start', 0)):,}")
            with col3:
                st.metric(get_text('app_opens_metric', st.session_state.language), f"{int(last_week_total.get('app_open', 0)):,}")
            with col4:
                st.metric(get_text('logins_metric', st.session_state.language), f"{int(last_week_total.get('login', 0)):,}")
            with col5:
                st.metric(get_text('uninstalls_metric', st.session_state.language), f"{int(last_week_total.get('app_remove', 0)):,}")
        
        # Practice & Engagement Group
        with st.container(border=True):
            st.markdown(f"##### {get_text('practice_engagement_group', st.session_state.language)}")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric(get_text('exercise_views_metric', st.session_state.language), f"{int(last_week_total.get('view_exercise', 0)):,}")
            with col2:
                st.metric(get_text('video_practice_metric', st.session_state.language), f"{int(last_week_total.get('practice_with_video', 0)):,}")
            with col3:
                st.metric(get_text('ai_practice_metric', st.session_state.language), f"{int(last_week_total.get('practice_with_ai', 0)):,}")
            with col4:
                st.metric(get_text('ai_chat_metric', st.session_state.language), f"{int(last_week_total.get('chat_ai', 0)):,}")
            with col5:
                avg_time_formatted = processor.format_engagement_time(last_week_total.get('avg_engage_time', 0))
                st.metric(get_text('avg_engagement_metric', st.session_state.language), avg_time_formatted)
        
        # Features & Content Group
        with st.container(border=True):
            st.markdown(f"##### {get_text('features_content_group', st.session_state.language)}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('health_surveys_metric', st.session_state.language), f"{int(last_week_total.get('health_survey', 0)):,}")
            with col2:
                st.metric(get_text('roadmap_views_metric', st.session_state.language), f"{int(last_week_total.get('view_roadmap', 0)):,}")
            with col3:
                st.metric(get_text('store_views_metric', st.session_state.language), f"{int(last_week_total.get('store_subscription', 0)):,}")
        
        # Popup Performance Group - HIDDEN
        # with st.container(border=True):
        #     st.markdown(f"##### {get_text('popup_performance_group', st.session_state.language)}")
        #     col1, col2, col3, col4 = st.columns(4)
        #     with col1:
        #         st.metric(get_text('shown_metric', st.session_state.language), f"{int(last_week_total.get('show_popup', 0)):,}")
        #     with col2:
        #         st.metric(get_text('details_viewed_metric', st.session_state.language), f"{int(last_week_total.get('view_detail_popup', 0)):,}")
        #     with col3:
        #         st.metric(get_text('closed_metric', st.session_state.language), f"{int(last_week_total.get('close_popup', 0)):,}")
        #     with col4:
        #         popup_ctr = (last_week_total.get('view_detail_popup', 0) / last_week_total.get('show_popup', 1)) * 100 if last_week_total.get('show_popup', 0) > 0 else 0
        #         st.metric(get_text('ctr_metric', st.session_state.language), f"{popup_ctr:.1f}%")

        # Notification & Messaging Group
        notif_receive = last_week_total.get('notification_receive', 0)
        notif_open = last_week_total.get('notification_open', 0)
        notif_dismiss = last_week_total.get('notification_dismiss', 0)
        notif_click = last_week_total.get('click_notification', 0)
        banner_click = last_week_total.get('click_banner', 0)
        
        open_rate = (notif_open / notif_receive * 100) if notif_receive > 0 else 0
        dismiss_rate = (notif_dismiss / notif_receive * 100) if notif_receive > 0 else 0
        click_rate = (notif_click / notif_receive * 100) if notif_receive > 0 else 0
        
        with st.container(border=True):
            st.markdown(f"##### {get_text('notification_group', st.session_state.language)}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(get_text('notifications_received_metric', st.session_state.language), f"{int(notif_receive):,}")
            with col2:
                st.metric(get_text('notifications_opened_metric', st.session_state.language), f"{int(notif_open):,}")
            with col3:
                st.metric(get_text('notifications_dismissed_metric', st.session_state.language), f"{int(notif_dismiss):,}")
            with col4:
                st.metric(get_text('notification_clicks_metric', st.session_state.language), f"{int(notif_click):,}")
            
            row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
            with row2_col1:
                st.metric(get_text('banner_clicks_metric', st.session_state.language), f"{int(banner_click):,}")
            with row2_col2:
                st.metric(get_text('notification_open_rate_metric', st.session_state.language), f"{open_rate:.1f}%")
            with row2_col3:
                st.metric(get_text('notification_dismiss_rate_metric', st.session_state.language), f"{dismiss_rate:.1f}%")
            with row2_col4:
                st.metric(get_text('notification_click_rate_metric', st.session_state.language), f"{click_rate:.1f}%")
        
        # Monetization Group
        with st.container(border=True):
            st.markdown(f"##### {get_text('monetization_group', st.session_state.language)}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('in_app_purchases_metric', st.session_state.language), f"{int(last_week_total.get('in_app_purchase', 0)):,}")
            with col2:
                conversion_rate = (last_week_total.get('in_app_purchase', 0) / last_week_total.get('store_subscription', 1)) * 100 if last_week_total.get('store_subscription', 0) > 0 else 0
                st.metric(get_text('conversion_rate_metric', st.session_state.language), f"{conversion_rate:.1f}%")
            with col3:
                st.metric(get_text('total_revenue_events_metric', st.session_state.language), f"{int(last_week_total.get('in_app_purchase', 0) + last_week_total.get('store_subscription', 0)):,}")
    
    elif is_time_series and len(filtered_periods_daily) > 0:
        # If less than 7 days, show what we have with same beautiful design
        st.markdown("---")  # Visual separator
        st.subheader(get_text('all_metrics_subheader', st.session_state.language))
        st.info(get_text('showing_n_days_info', st.session_state.language).format(days=len(filtered_periods_daily)))
        
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
            st.markdown(f"##### {get_text('user_activity_group', st.session_state.language)}")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric(get_text('new_users_metric', st.session_state.language), f"{int(days_total.get('first_open', 0)):,}")
            with col2:
                st.metric(get_text('sessions_metric', st.session_state.language), f"{int(days_total.get('session_start', 0)):,}")
            with col3:
                st.metric(get_text('app_opens_metric', st.session_state.language), f"{int(days_total.get('app_open', 0)):,}")
            with col4:
                st.metric(get_text('logins_metric', st.session_state.language), f"{int(days_total.get('login', 0)):,}")
            with col5:
                st.metric(get_text('uninstalls_metric', st.session_state.language), f"{int(days_total.get('app_remove', 0)):,}")
        
        # Practice & Engagement Group
        with st.container(border=True):
            st.markdown(f"##### {get_text('practice_engagement_group', st.session_state.language)}")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric(get_text('exercise_views_metric', st.session_state.language), f"{int(days_total.get('view_exercise', 0)):,}")
            with col2:
                st.metric(get_text('video_practice_metric', st.session_state.language), f"{int(days_total.get('practice_with_video', 0)):,}")
            with col3:
                st.metric(get_text('ai_practice_metric', st.session_state.language), f"{int(days_total.get('practice_with_ai', 0)):,}")
            with col4:
                st.metric(get_text('ai_chat_metric', st.session_state.language), f"{int(days_total.get('chat_ai', 0)):,}")
            with col5:
                avg_time_formatted = processor.format_engagement_time(days_total.get('avg_engage_time', 0))
                st.metric(get_text('avg_engagement_metric', st.session_state.language), avg_time_formatted)
        
        # Features & Content Group
        with st.container(border=True):
            st.markdown(f"##### {get_text('features_content_group', st.session_state.language)}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('health_surveys_metric', st.session_state.language), f"{int(days_total.get('health_survey', 0)):,}")
            with col2:
                st.metric(get_text('roadmap_views_metric', st.session_state.language), f"{int(days_total.get('view_roadmap', 0)):,}")
            with col3:
                st.metric(get_text('store_views_metric', st.session_state.language), f"{int(days_total.get('store_subscription', 0)):,}")
        
        # Popup Performance Group - HIDDEN
        # with st.container(border=True):
        #     st.markdown(f"##### {get_text('popup_performance_group', st.session_state.language)}")
        #     col1, col2, col3, col4 = st.columns(4)
        #     with col1:
        #         st.metric(get_text('shown_metric', st.session_state.language), f"{int(days_total.get('show_popup', 0)):,}")
        #     with col2:
        #         st.metric(get_text('details_viewed_metric', st.session_state.language), f"{int(days_total.get('view_detail_popup', 0)):,}")
        #     with col3:
        #         st.metric(get_text('closed_metric', st.session_state.language), f"{int(days_total.get('close_popup', 0)):,}")
        #     with col4:
        #         popup_ctr = (days_total.get('view_detail_popup', 0) / days_total.get('show_popup', 1)) * 100 if days_total.get('show_popup', 0) > 0 else 0
        #         st.metric(get_text('ctr_metric', st.session_state.language), f"{popup_ctr:.1f}%")

        # Notification & Messaging Group
        notif_receive = days_total.get('notification_receive', 0)
        notif_open = days_total.get('notification_open', 0)
        notif_dismiss = days_total.get('notification_dismiss', 0)
        notif_click = days_total.get('click_notification', 0)
        banner_click = days_total.get('click_banner', 0)
        
        open_rate = (notif_open / notif_receive * 100) if notif_receive > 0 else 0
        dismiss_rate = (notif_dismiss / notif_receive * 100) if notif_receive > 0 else 0
        click_rate = (notif_click / notif_receive * 100) if notif_receive > 0 else 0
        
        with st.container(border=True):
            st.markdown(f"##### {get_text('notification_group', st.session_state.language)}")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(get_text('notifications_received_metric', st.session_state.language), f"{int(notif_receive):,}")
            with col2:
                st.metric(get_text('notifications_opened_metric', st.session_state.language), f"{int(notif_open):,}")
            with col3:
                st.metric(get_text('notifications_dismissed_metric', st.session_state.language), f"{int(notif_dismiss):,}")
            with col4:
                st.metric(get_text('notification_clicks_metric', st.session_state.language), f"{int(notif_click):,}")
            
            row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
            with row2_col1:
                st.metric(get_text('banner_clicks_metric', st.session_state.language), f"{int(banner_click):,}")
            with row2_col2:
                st.metric(get_text('notification_open_rate_metric', st.session_state.language), f"{open_rate:.1f}%")
            with row2_col3:
                st.metric(get_text('notification_dismiss_rate_metric', st.session_state.language), f"{dismiss_rate:.1f}%")
            with row2_col4:
                st.metric(get_text('notification_click_rate_metric', st.session_state.language), f"{click_rate:.1f}%")
        
        # Monetization Group
        with st.container(border=True):
            st.markdown(f"##### {get_text('monetization_group', st.session_state.language)}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('in_app_purchases_metric', st.session_state.language), f"{int(days_total.get('in_app_purchase', 0)):,}")
            with col2:
                conversion_rate = (days_total.get('in_app_purchase', 0) / days_total.get('store_subscription', 1)) * 100 if days_total.get('store_subscription', 0) > 0 else 0
                st.metric(get_text('conversion_rate_metric', st.session_state.language), f"{conversion_rate:.1f}%")
            with col3:
                st.metric(get_text('total_revenue_events_metric', st.session_state.language), f"{int(days_total.get('in_app_purchase', 0) + days_total.get('store_subscription', 0)):,}")
    
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
        st.plotly_chart(time_series_chart, width="stretch", key=f"{chart_key_prefix}time_series")
        
        # User Acquisition vs Churn over time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(get_text('user_flow_trends', st.session_state.language))
            flow_chart = chart_gen.create_user_flow_trends_chart(filtered_periods, st.session_state.language)
            st.plotly_chart(flow_chart, width="stretch", key=f"{chart_key_prefix}flow_trends")
        
        with col2:
            st.subheader(get_text('user_activity_comparison_title', st.session_state.language))
            user_activity_chart = chart_gen.create_user_activity_comparison(filtered_periods, st.session_state.language)
            st.plotly_chart(user_activity_chart, width="stretch", key=f"{chart_key_prefix}user_activity")
        
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
        st.plotly_chart(feature_funnel_chart, width="stretch", key=f"{chart_key_prefix}feature_funnel")
    
    with col2:
        st.subheader("⏱️ Average Engagement Time Trends")
        engagement_chart = chart_gen.create_engagement_time_trends(filtered_periods, st.session_state.language)
        st.plotly_chart(engagement_chart, width="stretch", key=f"{chart_key_prefix}engagement_trends")
    
    # Feature Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(get_text('feature_usage_analysis', st.session_state.language))
        feature_chart = chart_gen.create_feature_usage_chart(aggregated_data, st.session_state.language)
        st.plotly_chart(feature_chart, width="stretch", key=f"{chart_key_prefix}feature")
    
    with col2:
        col_title, col_button = st.columns([4, 1])
        with col_title:
            st.subheader(get_text('churn_risk_indicator_title', st.session_state.language))
        with col_button:
            st.markdown("<br>", unsafe_allow_html=True)  # Align button with title
            explain_key = f"{chart_key_prefix}explain_churn_risk"
            if st.button(get_text('churn_risk_explain_button', st.session_state.language), key=explain_key):
                show_churn_risk_explanation(st.session_state.language)
        churn_risk_chart = chart_gen.create_churn_risk_indicator(aggregated_data, st.session_state.language)
        st.plotly_chart(churn_risk_chart, width="stretch", key=f"{chart_key_prefix}churn_risk")
    
    # Popup Performance - HIDDEN
    # st.subheader(get_text('popup_performance_header', st.session_state.language))
    # col1, col2, col3 = st.columns(3)
    # 
    # popup_metrics = processor.calculate_popup_metrics(aggregated_data)
    # 
    # with col1:
    #     st.metric(
    #         label=get_text('total_popups_shown', st.session_state.language),
    #         value=f"{popup_metrics['total_shown']:,}"
    #     )
    # 
    # with col2:
    #     st.metric(
    #         label=get_text('detail_views', st.session_state.language),
    #         value=f"{popup_metrics['detail_views']:,}"
    #     )
    # 
    # with col3:
    #     st.metric(
    #         label=get_text('conversion_rate', st.session_state.language),
    #         value=f"{popup_metrics['conversion_rate']:.1%}"
    #     )
    # 
    # popup_chart = chart_gen.create_popup_performance_chart(aggregated_data, st.session_state.language)
    # st.plotly_chart(popup_chart, width="stretch", key=f"{chart_key_prefix}popup")

    # Notification metrics & chart
    st.subheader(get_text('notification_performance_header', st.session_state.language))
    notif_metrics = processor.calculate_notification_metrics(aggregated_data)
    n_col1, n_col2, n_col3, n_col4, n_col5 = st.columns(5)
    with n_col1:
        st.metric(get_text('notifications_received_metric', st.session_state.language), f"{notif_metrics['notification_receive']:,}")
    with n_col2:
        st.metric(get_text('notifications_opened_metric', st.session_state.language), f"{notif_metrics['notification_open']:,}")
    with n_col3:
        st.metric(get_text('notifications_dismissed_metric', st.session_state.language), f"{notif_metrics['notification_dismiss']:,}")
    with n_col4:
        st.metric(get_text('notification_clicks_metric', st.session_state.language), f"{notif_metrics['click_notification']:,}")
    with n_col5:
        st.metric(get_text('banner_clicks_metric', st.session_state.language), f"{notif_metrics['banner_clicks']:,}")

    rate_col1, rate_col2, rate_col3 = st.columns(3)
    with rate_col1:
        st.metric(get_text('notification_open_rate_metric', st.session_state.language), f"{notif_metrics['open_rate']*100:.1f}%")
    with rate_col2:
        st.metric(get_text('notification_dismiss_rate_metric', st.session_state.language), f"{notif_metrics['dismiss_rate']*100:.1f}%")
    with rate_col3:
        st.metric(get_text('notification_click_rate_metric', st.session_state.language), f"{notif_metrics['click_through_rate']*100:.1f}%")

    notification_chart = chart_gen.create_notification_performance_chart(aggregated_data, st.session_state.language)
    st.plotly_chart(notification_chart, width="stretch", key=f"{chart_key_prefix}notification")
    
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
        
        # Create tabs for Analytics and Comparison
        tab1, tab2 = st.tabs(["📊 Analytics", "📈 Comparison"])
        
        with tab1:
            # Render dashboard for selected country
            if selected_country in countries_data:
                render_dashboard(countries_data[selected_country], selected_country)
            else:
                st.error(f"❌ Không có dữ liệu cho {selected_display}")
        
        with tab2:
            st.header(f"📈 {get_text('period_comparison', st.session_state.language)}")
            st.markdown(f"*{get_text('compare_by', st.session_state.language)} Day/Week/Month*")
            
            if selected_country in countries_data:
                webhook_data = countries_data[selected_country]
                all_periods = webhook_data.get('data', [])
                
                if all_periods and len(all_periods) > 0:
                    from utils.date_filter import DateRangeFilter
                    
                    # Granularity selector
                    main_filter = DateRangeFilter(key_prefix="comparison_main_", data=all_periods)
                    granularity = main_filter.get_granularity_selector()
                    
                    st.markdown("---")
                    
                    # Date range controls (UI adapts to granularity)
                    date_filter = DateRangeFilter(key_prefix="comparison_", data=all_periods)
                    current_range, compare_range = date_filter.render_comparison_controls(granularity)
                    
                    st.markdown("---")
                    
                    # Filter and aggregate data
                    from utils.data_processor import DataProcessor
                    from utils.charts import ChartGenerator
                    
                    processor = DataProcessor()
                    chart_gen = ChartGenerator()
                    
                    # Filter data manually based on the returned date ranges
                    current_start, current_end = current_range
                    compare_start, compare_end = compare_range
                    
                    # Filter current period data
                    current_filtered = []
                    for item in all_periods:
                        try:
                            item_date = datetime.strptime(item.get('time', ''), '%d/%m/%Y').date()
                            if current_start <= item_date <= current_end:
                                current_filtered.append(item)
                        except (ValueError, TypeError):
                            continue
                    
                    # Filter comparison period data
                    compare_filtered = []
                    for item in all_periods:
                        try:
                            item_date = datetime.strptime(item.get('time', ''), '%d/%m/%Y').date()
                            if compare_start <= item_date <= compare_end:
                                compare_filtered.append(item)
                        except (ValueError, TypeError):
                            continue
                    
                    if current_filtered and compare_filtered:
                        # Aggregate by granularity
                        current_aggregated = processor.aggregate_by_granularity(current_filtered, granularity)
                        compare_aggregated = processor.aggregate_by_granularity(compare_filtered, granularity)
                        
                        # Display Period Comparison chart (full width)
                        st.subheader(f"📊 {get_text('period_comparison', st.session_state.language)}")
                        comparison_chart = chart_gen.create_period_comparison_chart(
                            current_aggregated,
                            compare_aggregated,
                            granularity,
                            st.session_state.language
                        )
                        st.plotly_chart(comparison_chart, width="stretch")
                        
                        # Summary metrics
                        st.subheader(f"📋 {get_text('comparison_summary', st.session_state.language)}")
                        
                        comparison_metrics = processor.calculate_period_comparison(current_aggregated, compare_aggregated)
                        
                        # Top 4 KPIs in columns
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            new_users = comparison_metrics.get('first_open', {})
                            st.metric(
                                "New Users",
                                f"{new_users.get('current', 0):,.0f}",
                                f"{new_users.get('change_pct', 0):+.1f}%"
                            )
                        
                        with col2:
                            sessions = comparison_metrics.get('session_start', {})
                            st.metric(
                                "Sessions",
                                f"{sessions.get('current', 0):,.0f}",
                                f"{sessions.get('change_pct', 0):+.1f}%"
                            )
                        
                        with col3:
                            practice = comparison_metrics.get('practice_with_video', {})
                            st.metric(
                                "Video Practice",
                                f"{practice.get('current', 0):,.0f}",
                                f"{practice.get('change_pct', 0):+.1f}%"
                            )
                        
                        with col4:
                            ai_practice = comparison_metrics.get('practice_with_ai', {})
                            st.metric(
                                "AI Practice",
                                f"{ai_practice.get('current', 0):,.0f}",
                                f"{ai_practice.get('change_pct', 0):+.1f}%"
                            )
                        
                        st.markdown("---")
                        
                        # Detailed Metrics Comparison Table (grouped by categories)
                        st.subheader(f"📊 {get_text('detailed_metrics_comparison', st.session_state.language)}")
                        
                        # User Activity Group
                        with st.container(border=True):
                            st.markdown("##### 👥 User Activity")
                            col1, col2, col3, col4, col5 = st.columns(5)
                            
                            with col1:
                                metric_data = comparison_metrics.get('first_open', {})
                                st.metric(
                                    "New Users",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col2:
                                metric_data = comparison_metrics.get('session_start', {})
                                st.metric(
                                    "Sessions",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col3:
                                metric_data = comparison_metrics.get('app_open', {})
                                st.metric(
                                    "App Opens",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col4:
                                metric_data = comparison_metrics.get('login', {})
                                st.metric(
                                    "Logins",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col5:
                                metric_data = comparison_metrics.get('app_remove', {})
                                st.metric(
                                    "Uninstalls",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%",
                                    delta_color="inverse"
                                )
                        
                        # Practice & Engagement Group
                        with st.container(border=True):
                            st.markdown("##### 🏃‍♀️ Practice & Engagement")
                            col1, col2, col3, col4, col5 = st.columns(5)
                            
                            with col1:
                                metric_data = comparison_metrics.get('view_exercise', {})
                                st.metric(
                                    "Exercise Views",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col2:
                                metric_data = comparison_metrics.get('practice_with_video', {})
                                st.metric(
                                    "Video Practice",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col3:
                                metric_data = comparison_metrics.get('practice_with_ai', {})
                                st.metric(
                                    "AI Practice",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col4:
                                metric_data = comparison_metrics.get('chat_ai', {})
                                st.metric(
                                    "AI Chat",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col5:
                                metric_data = comparison_metrics.get('avg_engage_time', {})
                                current_time_formatted = processor.format_engagement_time(metric_data.get('current', 0))
                                st.metric(
                                    "Avg. Engagement",
                                    current_time_formatted,
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                        
                        # Features & Content Group
                        with st.container(border=True):
                            st.markdown("##### 🎯 Features & Content")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                metric_data = comparison_metrics.get('health_survey', {})
                                st.metric(
                                    "Health Surveys",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col2:
                                metric_data = comparison_metrics.get('view_roadmap', {})
                                st.metric(
                                    "Roadmap Views",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col3:
                                metric_data = comparison_metrics.get('store_subscription', {})
                                st.metric(
                                    "Store Views",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                        
                        # Popup Performance Group - HIDDEN
                        # with st.container(border=True):
                        #     st.markdown("##### 💬 Popup Performance")
                        #     col1, col2, col3, col4 = st.columns(4)
                        #     
                        #     with col1:
                        #         metric_data = comparison_metrics.get('show_popup', {})
                        #         st.metric(
                        #             "Shown",
                        #             f"{metric_data.get('current', 0):,.0f}",
                        #             f"{metric_data.get('change_pct', 0):+.1f}%"
                        #         )
                        #     
                        #     with col2:
                        #         metric_data = comparison_metrics.get('view_detail_popup', {})
                        #         st.metric(
                        #             "Details Viewed",
                        #             f"{metric_data.get('current', 0):,.0f}",
                        #             f"{metric_data.get('change_pct', 0):+.1f}%"
                        #         )
                        #     
                        #     with col3:
                        #         metric_data = comparison_metrics.get('close_popup', {})
                        #         st.metric(
                        #             "Closed",
                        #             f"{metric_data.get('current', 0):,.0f}",
                        #             f"{metric_data.get('change_pct', 0):+.1f}%"
                        #         )
                        #     
                        #     with col4:
                        #         # Calculate CTR for current and compare periods
                        #         show_current = comparison_metrics.get('show_popup', {}).get('current', 0)
                        #         view_current = comparison_metrics.get('view_detail_popup', {}).get('current', 0)
                        #         ctr_current = (view_current / show_current * 100) if show_current > 0 else 0
                        #         
                        #         show_compare = comparison_metrics.get('show_popup', {}).get('compare', 0)
                        #         view_compare = comparison_metrics.get('view_detail_popup', {}).get('compare', 0)
                        #         ctr_compare = (view_compare / show_compare * 100) if show_compare > 0 else 0
                        #         
                        #         ctr_change = ctr_current - ctr_compare
                        #         st.metric(
                        #             "CTR",
                        #             f"{ctr_current:.1f}%",
                        #             f"{ctr_change:+.1f}pp"
                        #         )
                        
                        # Monetization Group
                        with st.container(border=True):
                            st.markdown("##### 💰 Monetization")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                metric_data = comparison_metrics.get('in_app_purchase', {})
                                st.metric(
                                    "In-App Purchases",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                            
                            with col2:
                                # Calculate Conversion Rate for current and compare periods
                                purchases_current = comparison_metrics.get('in_app_purchase', {}).get('current', 0)
                                users_current = comparison_metrics.get('first_open', {}).get('current', 0)
                                conv_current = (purchases_current / users_current * 100) if users_current > 0 else 0
                                
                                purchases_compare = comparison_metrics.get('in_app_purchase', {}).get('compare', 0)
                                users_compare = comparison_metrics.get('first_open', {}).get('compare', 0)
                                conv_compare = (purchases_compare / users_compare * 100) if users_compare > 0 else 0
                                
                                conv_change = conv_current - conv_compare
                                st.metric(
                                    "Conversion Rate",
                                    f"{conv_current:.2f}%",
                                    f"{conv_change:+.2f}pp"
                                )
                            
                            with col3:
                                metric_data = comparison_metrics.get('total_revenue_events', {})
                                st.metric(
                                    "Revenue Events",
                                    f"{metric_data.get('current', 0):,.0f}",
                                    f"{metric_data.get('change_pct', 0):+.1f}%"
                                )
                        
                    else:
                        st.warning("⚠️ Please ensure both current and comparison periods have valid data.")
                else:
                    st.warning("⚠️ No data available for comparison. Please fetch data first.")
            else:
                st.error("❌ Selected country data not found.")
    
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
        if st.button("📊 Show Input", key="show_input_btn", width="stretch"):
            show_input_dialog()
        
        if st.button("🗑️ Clear Data", key="clear_data_btn", width="stretch"):
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
