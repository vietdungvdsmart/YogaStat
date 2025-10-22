# Yoga App Analytics Dashboard

## Overview

This is a Streamlit-based analytics dashboard designed to visualize user engagement metrics for a yoga exercise app. The dashboard integrates with n8n webhooks to fetch real-time analytics data and provides comprehensive insights into user behavior, retention, and feature usage. The application focuses on helping app developers and product managers understand user engagement patterns and make data-driven decisions for app optimization.

## Recent Changes

**October 22, 2025:**
- Redesigned "All Metrics (Last 7 Days)" section with grouped categories for better visual organization:
  - User Activity: New Users, Sessions, App Opens, Logins, Uninstalls
  - Practice & Engagement: Exercise Views, Video Practice, AI Practice, AI Chat, Avg. Engagement
  - Features & Content: Health Surveys, Roadmap Views, Store Views
  - Popup Performance: Shown, Details Viewed, Closed, CTR (calculated metric)
  - Monetization: In-App Purchases, Conversion Rate, Total Revenue Events
- Removed technical field names (first_open, app_remove, etc.) for cleaner user-friendly labels
- Added calculated metrics: Popup CTR and Conversion Rate for better insights
- Added bordered containers for each metric group for better visual separation and readability
- Fixed x-axis label overlap in all time-series charts:
  - Rotated labels -45 degrees for better readability
  - Implemented smart label spacing: shows every nth label based on data size (1-14 days: all labels, 15-30 days: every 3rd, >30 days: every 7th)
  - Reduced font size to 10px for cleaner appearance

**October 21, 2025:**
- Fixed numeric time field conversion: Dashboard now handles both string and numeric time formats (e.g., "20250217" and 20250217)
- Merged "Key Performance Indicators" and "Last Week Overview" sections into one unified section titled "Key Performance Indicators & Weekly Metrics" for cleaner UI
- Added visual hierarchy with subheaders: "Top 5 KPIs" displays the main 5 metrics, followed by "All Metrics (Last 7 Days)" showing all 17 metrics

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for rapid web application development
- **Visualization**: Plotly for interactive charts and graphs with yoga-inspired color scheme
- **Styling**: Custom CSS with modern, calming design using greens, blues, and purples
- **Layout**: Responsive grid layout optimized for both desktop and mobile viewing
- **State Management**: Streamlit session state for maintaining data and configuration across user interactions

### Data Processing Architecture
- **Modular Design**: Separated concerns into three main utility modules:
  - `DataProcessor`: Handles data validation, cleaning, and KPI calculations
  - `ChartGenerator`: Creates interactive visualizations with consistent styling
  - `InsightsGenerator`: Generates actionable insights and recommendations
- **Data Validation**: Comprehensive validation for webhook data including field presence and type checking
- **Real-time Processing**: Direct processing of webhook data without persistent storage
- **Multi-Country Accumulator**: Collects data from 3 sequential webhook calls (US, India, VN) with 60-second timeout
- **Loading State**: Simple loading indicator without detailed progression display
- **Timeout Handling**: Automatic termination and error display after 60 seconds if data incomplete

### Analytics Features
- **Unified KPI Section**: Combined display of top 5 KPIs and all 17 weekly metrics in one cohesive section
- **KPI Calculations**: Automated calculation of retention rates, churn rates, engagement metrics, and conversion rates
- **Last 7 Days Metrics**: Displays totals for all 17 metrics from the last 7 days of data with proper aggregation (avg_engage_time is averaged, all others are summed)
- **Comparative Analysis**: User acquisition vs churn visualization
- **Feature Usage Tracking**: Monitors adoption of video practice, AI features, and roadmap views
- **Popup Performance**: Tracks popup effectiveness and conversion rates
- **Insight Generation**: Automated recommendations based on predefined benchmarks and thresholds

### Design Patterns
- **Class-based Architecture**: Utility classes provide reusable functionality and maintain separation of concerns
- **Configuration-driven**: Color schemes and benchmarks defined as class properties for easy customization
- **Error Handling**: Comprehensive validation and error handling for webhook data
- **Responsive Design**: CSS grid layout with hover effects and smooth transitions

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for the dashboard interface
- **Plotly**: Interactive charting library for data visualization
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing for calculations
- **Requests**: HTTP library for webhook integration

### Data Integration
- **n8n Webhook**: Primary data source requiring webhook URL configuration
- **JSON Data Format**: Expects structured data with 17 predefined metrics including user engagement, feature usage, and popup interactions
- **Time Field Support**: Handles both string ("20250217") and numeric (20250217) formats for date fields
- **Real-time Data**: No database dependency - processes data directly from webhook responses
- **Multi-language Support**: Full support for English and Vietnamese throughout the interface

### Styling and UI
- **Custom CSS**: External stylesheet for yoga-inspired theming
- **Responsive Design**: Mobile-friendly layout with hover effects and animations
- **Color Scheme**: Predefined palette using calming colors appropriate for yoga/wellness applications