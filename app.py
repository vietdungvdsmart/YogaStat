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
                    response = requests.get(webhook_url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Validate data structure
                    processor = DataProcessor()
                    if processor.validate_data(data):
                        st.session_state.data = data
                        st.session_state.webhook_url = webhook_url
                        st.success("✅ Data fetched successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid data format received from webhook")
                        
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Failed to fetch data: {str(e)}")
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON response from webhook")
        else:
            st.error("❌ Please enter a webhook URL")

# Main dashboard
if st.session_state.data:
    data = st.session_state.data
    processor = DataProcessor()
    chart_gen = ChartGenerator()
    insights_gen = InsightsGenerator()
    
    # Process data
    processed_data = processor.process_data(data)
    kpis = processor.calculate_kpis(data)
    
    # KPI Section
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="👥 Total New Users",
            value=f"{kpis['total_new_users']:,}",
            delta=f"{kpis.get('new_users_delta', 0):+.1%}" if kpis.get('new_users_delta') else None
        )
    
    with col2:
        st.metric(
            label="🔄 User Retention Rate",
            value=f"{kpis['retention_rate']:.1%}",
            delta=f"{kpis.get('retention_delta', 0):+.1%}" if kpis.get('retention_delta') else None
        )
    
    with col3:
        st.metric(
            label="📉 Churn Rate",
            value=f"{kpis['churn_rate']:.1%}",
            delta=f"{kpis.get('churn_delta', 0):+.1%}" if kpis.get('churn_delta') else None,
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="🎯 Active Sessions",
            value=f"{kpis['active_sessions']:,}",
            delta=f"{kpis.get('sessions_delta', 0):+.1%}" if kpis.get('sessions_delta') else None
        )
    
    with col5:
        st.metric(
            label="💪 Engagement Rate",
            value=f"{kpis['engagement_rate']:.1%}",
            delta=f"{kpis.get('engagement_delta', 0):+.1%}" if kpis.get('engagement_delta') else None
        )
    
    st.divider()
    
    # Charts Section
    st.header("📈 Analytics Overview")
    
    # User Acquisition vs Churn
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 User Acquisition vs Churn")
        acquisition_chart = chart_gen.create_acquisition_churn_chart(data)
        st.plotly_chart(acquisition_chart, use_container_width=True)
    
    with col2:
        st.subheader("🏃‍♀️ Practice Preferences")
        practice_chart = chart_gen.create_practice_preferences_chart(data)
        st.plotly_chart(practice_chart, use_container_width=True)
    
    # Engagement Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📱 Feature Usage Analysis")
        feature_chart = chart_gen.create_feature_usage_chart(data)
        st.plotly_chart(feature_chart, use_container_width=True)
    
    with col2:
        st.subheader("🤖 AI Engagement Metrics")
        ai_chart = chart_gen.create_ai_engagement_chart(data)
        st.plotly_chart(ai_chart, use_container_width=True)
    
    # Popup Performance
    st.subheader("💬 Popup Performance Dashboard")
    col1, col2, col3 = st.columns(3)
    
    popup_metrics = processor.calculate_popup_metrics(data)
    
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
    
    popup_chart = chart_gen.create_popup_performance_chart(data)
    st.plotly_chart(popup_chart, use_container_width=True)
    
    st.divider()
    
    # Insights Panel
    st.header("🧠 Insights & Recommendations")
    insights = insights_gen.generate_insights(data, kpis)
    
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
    adoption_data = processor.calculate_feature_adoption(data)
    
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
            csv_data = processor.export_to_csv(data)
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
    
    # Show sample data structure
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
