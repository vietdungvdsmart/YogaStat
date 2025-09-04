import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime, timedelta
import numpy as np
from utils.data_processor import DataProcessor
from utils.charts import ChartGenerator
from utils.insights import InsightsGenerator

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

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'webhook_url' not in st.session_state:
    st.session_state.webhook_url = ""
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None

# Header
st.title("🧘‍♀️ Yoga App Analytics Dashboard")
st.markdown("*Visualize user engagement metrics and gain actionable insights for app optimization*")

# Webhook input section
st.header("📡 Data Source Configuration")
col1, col2 = st.columns([4, 1])

with col1:
    webhook_url = st.text_input(
        "Enter your n8n webhook URL:",
        value=st.session_state.webhook_url,
        placeholder="https://your-n8n-instance.com/webhook/yoga-analytics",
        help="Paste your n8n webhook URL that returns JSON data with yoga app metrics"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Fetch Data", type="primary"):
        if webhook_url:
            try:
                with st.spinner("Fetching data from webhook..."):
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
                            
                            # Show received data for debugging
                            with st.expander("🔍 Debug: Raw Response Data"):
                                st.json(data)
                            
                            # Validate and process data structure (handle both single object and array formats)
                            processor = DataProcessor()
                            processed_data = processor.process_webhook_data(data)
                            
                            if processed_data:
                                st.session_state.data = processed_data
                                st.session_state.webhook_url = webhook_url
                                st.success("✅ Data fetched successfully!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid data format received from webhook")
                                st.info("💡 Expected data format is shown below in the 'Expected Data Format' section.")
                                
                    except requests.exceptions.HTTPError as e:
                        if response and response.status_code == 404:
                            st.error("❌ Webhook not found (404). Please check:")
                            st.write("• Is your n8n workflow active and saved?")
                            st.write("• Does the webhook URL match exactly?")
                            st.write("• Try copying the webhook URL directly from n8n")
                        elif response and response.status_code == 500:
                            st.error("❌ Server error (500). Your n8n workflow might have an error.")
                        else:
                            st.error(f"❌ HTTP Error: {str(e)}")
                            
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection failed. Please check:")
                st.write("• Is your n8n instance running?")
                st.write("• Can you access the n8n URL in your browser?")
                st.write("• Check your internet connection")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The webhook might be taking too long to respond.")
            except json.JSONDecodeError as e:
                st.error("❌ Invalid JSON response from webhook")
                if response is not None:
                    st.write(f"Response content: {response.text[:500]}...")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
        else:
            st.error("❌ Please enter a webhook URL")

# Main dashboard
if st.session_state.data:
    webhook_data = st.session_state.data
    processor = DataProcessor()
    chart_gen = ChartGenerator()
    insights_gen = InsightsGenerator()
    
    # Check if we have time series data or single data point
    is_time_series = webhook_data.get('is_time_series', False)
    time_periods = webhook_data.get('time_periods', 1)
    all_periods = webhook_data.get('data', [])
    
    # Add date range filter for time series data
    if is_time_series and len(all_periods) > 1:
        st.subheader("📅 Date Range Filter")
        col1, col2, col3 = st.columns([2, 2, 1])
        
        # Parse dates from the time periods to get min/max dates
        def parse_date_range(time_str):
            """Parse date range from time string like '1/7/2025 - 7/7/2025'"""
            try:
                if ' - ' in time_str:
                    start_str, end_str = time_str.split(' - ')
                    from datetime import datetime
                    start_date = datetime.strptime(start_str.strip(), '%d/%m/%Y').date()
                    end_date = datetime.strptime(end_str.strip(), '%d/%m/%Y').date()
                    return start_date, end_date
                return None, None
            except:
                return None, None
        
        # Get all dates from periods
        all_dates = []
        for period in all_periods:
            start_date, end_date = parse_date_range(period.get('time', ''))
            if start_date and end_date:
                all_dates.extend([start_date, end_date])
        
        if all_dates:
            min_date = min(all_dates)
            max_date = max(all_dates)
            
            with col1:
                # Date range selector
                selected_start = st.date_input(
                    "Start Date:",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="filter_start_date"
                )
                
                selected_end = st.date_input(
                    "End Date:",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date,
                    key="filter_end_date"
                )
            
            with col2:
                # Preview filtered data count
                def date_ranges_intersect(start1, end1, start2, end2):
                    """Check if two date ranges intersect"""
                    return start1 <= end2 and start2 <= end1
                
                # Calculate preview of filtered periods
                preview_filtered = []
                for period in all_periods:
                    period_start, period_end = parse_date_range(period.get('time', ''))
                    if period_start and period_end:
                        if date_ranges_intersect(selected_start, selected_end, period_start, period_end):
                            preview_filtered.append(period)
                
                st.info(f"📊 Preview: {len(preview_filtered)} week(s) will be included")
                if len(preview_filtered) == 0:
                    st.warning("⚠️ No weeks match this date range")
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔄 Apply Filter", type="primary"):
                    # Apply the filter and store in session state
                    filtered_periods = []
                    for period in all_periods:
                        period_start, period_end = parse_date_range(period.get('time', ''))
                        if period_start and period_end:
                            if date_ranges_intersect(selected_start, selected_end, period_start, period_end):
                                filtered_periods.append(period)
                    
                    # Store filtered data in session state
                    if filtered_periods:
                        st.session_state.filtered_data = {
                            'is_time_series': True,
                            'time_periods': len(filtered_periods),
                            'data': filtered_periods,
                            'latest_period': filtered_periods[-1],
                            'aggregated': processor._aggregate_time_series_data(filtered_periods)
                        }
                        st.success(f"✅ Filter applied! Showing {len(filtered_periods)} week(s) of data.")
                        st.rerun()
                    else:
                        st.error("❌ No data matches selected range")
                
                if st.button("📊 Show All Data", type="secondary"):
                    st.session_state.filtered_data = None
                    st.success("✅ Showing all available data.")
                    st.rerun()
            
            # Use filtered data if available, otherwise use all data
            if st.session_state.filtered_data is not None:
                # Use the stored filtered data
                webhook_data = st.session_state.filtered_data
                filtered_periods = webhook_data.get('data', [])
                st.info(f"🎯 Currently showing filtered data: {len(filtered_periods)} week(s)")
            else:
                # No filter applied yet, use all data
                filtered_periods = all_periods
                st.info("📊 Showing all available data (no filter applied)")
        else:
            filtered_periods = all_periods
            st.warning("⚠️ Could not parse dates from time periods")
        
        
        st.divider()
    else:
        filtered_periods = all_periods
    
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
    else:
        # Fallback for Key Performance section if not enough periods
        key_performance_kpis = kpis
        key_performance_deltas = {}
    
    # KPI Section
    if is_time_series and len(filtered_periods) >= 2:
        st.header("📊 Key Performance")
        st.info(f"📅 Latest Week: {current_week_time} (vs Previous Week: {previous_week_time})")
    else:
        st.header("📊 Key Performance")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        delta_val = f"{key_performance_deltas.get('total_new_users', 0):+.1%}" if key_performance_deltas.get('total_new_users') else None
        st.metric(
            label="👥 Total New Users",
            value=f"{key_performance_kpis['total_new_users']:,}",
            delta=delta_val
        )
    
    with col2:
        delta_val = f"{key_performance_deltas.get('retention_rate', 0):+.1%}" if key_performance_deltas.get('retention_rate') else None
        st.metric(
            label="🔄 User Retention Rate",
            value=f"{key_performance_kpis['retention_rate']:.1%}",
            delta=delta_val
        )
    
    with col3:
        delta_val = f"{key_performance_deltas.get('churn_rate', 0):+.1%}" if key_performance_deltas.get('churn_rate') else None
        st.metric(
            label="📉 Churn Rate",
            value=f"{key_performance_kpis['churn_rate']:.1%}",
            delta=delta_val,
            delta_color="inverse"
        )
    
    with col4:
        delta_val = f"{key_performance_deltas.get('active_sessions', 0):+.1%}" if key_performance_deltas.get('active_sessions') else None
        st.metric(
            label="🎯 Active Sessions",
            value=f"{key_performance_kpis['active_sessions']:,}",
            delta=delta_val
        )
    
    with col5:
        delta_val = f"{key_performance_deltas.get('engagement_rate', 0):+.1%}" if key_performance_deltas.get('engagement_rate') else None
        st.metric(
            label="💪 Engagement Rate",
            value=f"{key_performance_kpis['engagement_rate']:.1%}",
            delta=delta_val
        )
    
    st.divider()
    
    # Charts Section
    st.header("📈 Analytics Overview")
    
    if is_time_series:
        # Time Series Charts for weekly data
        st.subheader("📊 Time Series Analysis")
        
        # Create time series chart using filtered data
        time_series_chart = chart_gen.create_time_series_chart(filtered_periods)
        st.plotly_chart(time_series_chart, use_container_width=True)
        
        # User Acquisition vs Churn over time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 User Flow Trends")
            flow_chart = chart_gen.create_user_flow_trends_chart(filtered_periods)
            st.plotly_chart(flow_chart, use_container_width=True)
        
        with col2:
            st.subheader("🏃‍♀️ Practice Trends")
            practice_trends_chart = chart_gen.create_practice_trends_chart(filtered_periods)
            st.plotly_chart(practice_trends_chart, use_container_width=True)
        
        st.divider()
        
        # Weekly breakdown using filtered data
        if len(filtered_periods) > 1:
            st.subheader("📅 Weekly Breakdown")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📈 Best Week (New Users):**")
                best_week = max(filtered_periods, key=lambda x: x.get('first_open', 0))
                st.write(f"Week: {best_week.get('time', 'N/A')}")
                st.write(f"New Users: {best_week.get('first_open', 0)}")
            
            with col2:
                st.markdown("**💪 Most Engaged Week:**")
                most_engaged = max(filtered_periods, key=lambda x: x.get('practice_with_video', 0) + x.get('practice_with_ai', 0))
                st.write(f"Week: {most_engaged.get('time', 'N/A')}")
                st.write(f"Practice Sessions: {most_engaged.get('practice_with_video', 0) + most_engaged.get('practice_with_ai', 0)}")
            
            with col3:
                st.markdown("**🤖 Top AI Week:**")
                top_ai = max(filtered_periods, key=lambda x: x.get('chat_ai', 0))
                st.write(f"Week: {top_ai.get('time', 'N/A')}")
                st.write(f"AI Interactions: {top_ai.get('chat_ai', 0)}")
    
    # Current period or aggregated charts
    col1, col2 = st.columns(2)
    
    with col1:
        chart_title = "👥 User Acquisition vs Churn" if not is_time_series else "👥 Overall User Metrics"
        st.subheader(chart_title)
        acquisition_chart = chart_gen.create_acquisition_churn_chart(aggregated_data)
        st.plotly_chart(acquisition_chart, use_container_width=True)
    
    with col2:
        chart_title = "🏃‍♀️ Practice Preferences" if not is_time_series else "🏃‍♀️ Total Practice Distribution"
        st.subheader(chart_title)
        practice_chart = chart_gen.create_practice_preferences_chart(aggregated_data)
        st.plotly_chart(practice_chart, use_container_width=True)
    
    # Feature Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📱 Feature Usage Analysis")
        feature_chart = chart_gen.create_feature_usage_chart(aggregated_data)
        st.plotly_chart(feature_chart, use_container_width=True)
    
    with col2:
        st.subheader("🤖 AI Engagement Metrics")
        ai_chart = chart_gen.create_ai_engagement_chart(aggregated_data)
        st.plotly_chart(ai_chart, use_container_width=True)
    
    # Popup Performance
    st.subheader("💬 Popup Performance Dashboard")
    col1, col2, col3 = st.columns(3)
    
    popup_metrics = processor.calculate_popup_metrics(aggregated_data)
    
    with col1:
        st.metric(
            label="👁️ Total Popups Shown",
            value=f"{popup_metrics['total_shown']:,}"
        )
    
    with col2:
        st.metric(
            label="🔍 Detail Views",
            value=f"{popup_metrics['detail_views']:,}"
        )
    
    with col3:
        st.metric(
            label="💯 Conversion Rate",
            value=f"{popup_metrics['conversion_rate']:.1%}"
        )
    
    popup_chart = chart_gen.create_popup_performance_chart(aggregated_data)
    st.plotly_chart(popup_chart, use_container_width=True)
    
    st.divider()
    
    # Insights Panel
    st.header("🧠 Insights & Recommendations")
    insights = insights_gen.generate_insights(aggregated_data, kpis)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Key Insights")
        for insight in insights['key_insights']:
            st.info(f"💡 {insight}")
    
    with col2:
        st.subheader("🚀 Recommendations")
        for recommendation in insights['recommendations']:
            st.success(f"✅ {recommendation}")
    
    # Feature Adoption Analysis
    st.subheader("📊 Feature Adoption Analysis")
    adoption_data = processor.calculate_feature_adoption(aggregated_data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏆 Most Used Features:**")
        for feature, usage in adoption_data['most_used'][:3]:
            st.write(f"• {feature}: {usage}")
    
    with col2:
        st.markdown("**📈 Growing Features:**")
        for feature, growth in adoption_data['growing'][:3]:
            st.write(f"• {feature}: +{growth:.1%}")
    
    with col3:
        st.markdown("**⚠️ Underutilized Features:**")
        for feature, usage in adoption_data['least_used'][:3]:
            st.write(f"• {feature}: {usage}")
    
    st.divider()
    
    # Export Section
    st.header("📤 Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Raw Data (CSV)"):
            csv_data = processor.export_to_csv(aggregated_data)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"yoga_app_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export KPIs (JSON)"):
            json_data = json.dumps(kpis, indent=2)
            st.download_button(
                label="Download KPIs",
                data=json_data,
                file_name=f"yoga_app_kpis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("🧠 Export Insights (TXT)"):
            insights_text = insights_gen.export_insights_text(insights)
            st.download_button(
                label="Download Insights",
                data=insights_text,
                file_name=f"yoga_app_insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

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
            # Create sample time series data matching your webhook format
            sample_time_series = [
                {"time": "1/7/2025 - 7/7/2025", "first_open": 25, "app_remove": 8, "session_start": 45, "app_open": 32, "login": 40, "view_exercise": 42, "health_survey": 38, "view_roadmap": 12, "practice_with_video": 22, "practice_with_ai": 18, "chat_ai": 15, "show_popup": 35, "view_detail_popup": 20, "close_popup": 28},
                {"time": "8/7/2025 - 14/7/2025", "first_open": 30, "app_remove": 5, "session_start": 52, "app_open": 28, "login": 35, "view_exercise": 38, "health_survey": 32, "view_roadmap": 8, "practice_with_video": 25, "practice_with_ai": 15, "chat_ai": 12, "show_popup": 40, "view_detail_popup": 25, "close_popup": 30},
                {"time": "15/7/2025 - 21/7/2025", "first_open": 20, "app_remove": 12, "session_start": 38, "app_open": 35, "login": 42, "view_exercise": 45, "health_survey": 35, "view_roadmap": 15, "practice_with_video": 28, "practice_with_ai": 22, "chat_ai": 18, "show_popup": 38, "view_detail_popup": 22, "close_popup": 32},
                {"time": "22/7/2025 - 28/7/2025", "first_open": 35, "app_remove": 6, "session_start": 48, "app_open": 40, "login": 38, "view_exercise": 40, "health_survey": 30, "view_roadmap": 18, "practice_with_video": 30, "practice_with_ai": 25, "chat_ai": 20, "show_popup": 42, "view_detail_popup": 28, "close_popup": 35}
            ]
            
            # Process the sample data using the new format
            processor = DataProcessor()
            processed_sample = processor.process_webhook_data(sample_time_series)
            
            st.session_state.data = processed_sample
            st.success("✅ Sample time series data loaded! You can now explore the dashboard with weekly data trends.")
            st.rerun()
    
    with col2:
        st.info("💡 **Tip:** Use sample data to explore dashboard features while setting up your webhook.")

# Sidebar with additional controls
with st.sidebar:
    st.title("🎛️ Dashboard Controls")
    
    if st.session_state.data:
        st.success("✅ Data Loaded")
        st.json(st.session_state.data)
        
        if st.button("🗑️ Clear Data"):
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
