# Yoga App Analytics Dashboard

## Overview

This is a Streamlit-based analytics dashboard designed to visualize user engagement metrics for a yoga exercise app. The dashboard integrates with n8n webhooks to fetch real-time analytics data and provides comprehensive insights into user behavior, retention, and feature usage. The application focuses on helping app developers and product managers understand user engagement patterns and make data-driven decisions for app optimization.

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
- **KPI Calculations**: Automated calculation of retention rates, churn rates, engagement metrics, and conversion rates
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
- **JSON Data Format**: Expects structured data with 14 predefined metrics including user engagement, feature usage, and popup interactions
- **Real-time Data**: No database dependency - processes data directly from webhook responses

### Styling and UI
- **Custom CSS**: External stylesheet for yoga-inspired theming
- **Responsive Design**: Mobile-friendly layout with hover effects and animations
- **Color Scheme**: Predefined palette using calming colors appropriate for yoga/wellness applications