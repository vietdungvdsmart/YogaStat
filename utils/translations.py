"""Translation module for Yoga App Analytics Dashboard."""

TRANSLATIONS = {
    'en': {
        # Main headers
        'page_title': 'Yoga App Analytics Dashboard',
        'page_subtitle': 'Visualize user engagement metrics and gain actionable insights for app optimization',
        
        # Data source section
        'data_source_header': '📡 Data Source Configuration',
        'webhook_input_label': 'Enter your n8n webhook URL:',
        'webhook_placeholder': 'https://your-n8n-instance.com/webhook/yoga-analytics',
        'webhook_help': 'Paste your n8n webhook URL that returns JSON data with yoga app metrics',
        'fetch_data_button': '🔄 Fetch Data',
        
        # Status messages
        'fetching_data': 'Fetching data from webhook...',
        'data_fetched_success': '✅ Data fetched successfully!',
        'invalid_data_format': '❌ Invalid data format received from webhook',
        'webhook_not_found': '❌ Webhook not found (404). Please check:',
        'server_error': '❌ Server error (500). Your n8n workflow might have an error.',
        'connection_failed': '❌ Connection failed. Please check:',
        'request_timeout': '❌ Request timed out. The webhook might be taking too long to respond.',
        'invalid_json': '❌ Invalid JSON response from webhook',
        'enter_webhook_url': '❌ Please enter a webhook URL',
        
        # Date filter section
        'date_filter_header': '📅 Date Range Filter',
        'start_date_label': 'Start Date:',
        'end_date_label': 'End Date:',
        'apply_filter_button': '🔄 Apply Filter',
        'show_all_data_button': '📊 Show All Data',
        'filter_applied': '✅ Filter applied! Showing {count} week(s) of data.',
        'showing_all_data': '✅ Showing all available data.',
        'no_data_matches': '❌ No data matches selected range',
        'currently_showing_filtered': '🎯 Currently showing filtered data: {count} week(s)',
        'showing_all_available': '📊 Showing all available data (no filter applied)',
        'preview_weeks': '📊 Preview: {count} week(s) will be included',
        'no_weeks_match': '⚠️ No weeks match this date range',
        
        # KPI section (combined with Last Week Overview)
        'key_performance_header': '📊 Key Performance Indicators & Weekly Metrics',
        'kpi_overview_subheader': '🎯 Top 5 KPIs',
        'all_metrics_subheader': '📋 All Metrics (Last 7 Days)',
        'latest_week': '📅 Latest Week: {current} (vs Previous Week: {previous})',
        'total_new_users': '👥 Total New Users',
        'user_retention_rate': '🔄 User Retention Rate',
        'churn_rate': '📉 Churn Rate',
        'active_sessions': '🎯 Active Sessions',
        'engagement_rate': '💪 Engagement Rate',
        'avg_engagement_time': '⏱️ Avg. Engagement Time',
        
        # Country analytics
        'analytics': 'Analytics',
        'all_countries_analytics': 'All Countries Analytics',
        
        # Charts section
        'analytics_overview_header': '📈 Analytics Overview',
        'time_series_analysis': '📊 Time Series Analysis',
        'user_flow_trends': '👥 User Flow Trends',
        'practice_trends': '🏃‍♀️ Practice Trends',
        
        # Weekly breakdown
        'weekly_breakdown_header': '📅 Weekly Breakdown',
        'best_week_new_users': '**📈 Best Week (New Users):**',
        'most_engaged_week': '**💪 Most Engaged Week:**',
        'top_ai_week': '**🤖 Top AI Week:**',
        'week_label': 'Week:',
        'new_users_label': 'New Users:',
        'practice_sessions_label': 'Practice Sessions:',
        'ai_interactions_label': 'AI Interactions:',
        
        # Chart titles
        'user_acquisition_vs_churn': '👥 User Acquisition vs Churn',
        'overall_user_metrics': '👥 Overall User Metrics',
        'practice_preferences': '🏃‍♀️ Practice Preferences',
        'total_practice_distribution': '🏃‍♀️ Total Practice Distribution',
        'feature_usage_analysis': '📱 Feature Usage Analysis',
        'feature_adoption_analysis': '🎯 Feature Adoption Funnel',
        'feature_adoption_funnel_title': 'Feature Adoption Journey',
        'view_exercise_stage': 'View Exercise',
        'practice_video_stage': 'Practice with Video',
        'practice_ai_stage': 'Practice with AI',
        'chat_ai_stage': 'Chat with AI',
        'users_count': 'Users',
        'conversion_from_start': 'Conversion from View Exercise',
        'engagement_quality': '📊 Engagement Quality Score',
        'overall_engagement_score': '📊 Overall Engagement Score',
        'engagement_score': 'Engagement Score',
        'engagement_score_radar_title': 'Multi-Dimensional Engagement Analysis',
        'login_engagement': 'Login Activity',
        'health_awareness': 'Health Awareness',
        'content_exploration': 'Content Exploration',
        'ai_interaction': 'AI Interaction',
        'popup_responsiveness': 'Popup Response',
        'retention_strength': 'Retention Strength',
        'average_benchmark': 'Average Benchmark',
        'ai_engagement_metrics': '🤖 AI Engagement Metrics',
        
        # New chart titles and labels
        'user_activity_comparison_title': 'User Activity Comparison',
        'user_funnel_analysis_title': 'User Funnel Analysis',
        'churn_risk_indicator_title': 'Churn Risk Indicator',
        'churn_risk_explain_button': 'ℹ️ Explain',
        'churn_risk_explanation': '''**What this gauge measures:** The Churn Risk Indicator shows how likely users are to leave your app. It combines negative signals (app removals, notification dismissals) with positive signals (app opens, core actions, purchases) and engagement time into a single risk score.

**How it's calculated:** 
$$Risk = \\frac{(app\\_remove \\times 10) + (notification\\_dismiss \\times 1)}{(app\\_open \\times 1) + (CoreActions \\times 3) + (in\\_app\\_purchase \\times 10)} \\times \\frac{1}{avg\\_engage\\_time}$$

Where CoreActions = practice_with_video + practice_with_ai + chat_ai, and avg_engage_time is in minutes.

**Risk Zones:**
- **Low Risk (< 0.1):** 🟢 Healthy user engagement - users are active and engaged
- **Medium Risk (0.1 to 0.5):** 🟠 Needs attention - some negative signals, action recommended
- **High Risk (> 0.5):** 🔴 Urgent action needed - high risk of churn, immediate intervention required

**How to interpret:** Lower scores are better. A score below 0.1 indicates healthy engagement, while scores above 0.5 suggest you need to focus on reducing app removals, improving notification engagement, and increasing core user actions.''',
        'new_users': 'New Users',
        'active_sessions': 'Active Sessions',
        'total_practice': 'Total Practice',
        'risk_level_low': 'Low Risk',
        'risk_level_medium': 'Medium Risk',
        'risk_level_high': 'High Risk',
        
        # Popup performance
        'popup_performance_header': '💬 Popup Performance Dashboard',
        'total_popups_shown': '👁️ Total Popups Shown',
        'detail_views': '🔍 Detail Views',
        'conversion_rate': '💯 Conversion Rate',
        'notification_performance_header': '📣 Notification Engagement',
        'notification_chart_title': 'Notification & Banner Interactions',
        
        # Insights section
        'insights_header': '🧠 Insights & Recommendations',
        'overall_insights': '🌍 Overall Insights',
        'overall_insights_subtitle': '*Based on all available data*',
        'this_week_insights': '📅 This Week Insights',
        'this_week_insights_subtitle': '*Based on last 2 weeks*',
        'recommendations_header': '🚀 Recommendations',
        'key_insights_header': '🎯 Key Insights',
        
        # All Metrics (Last 7 Days) section labels
        'user_activity_group': '👥 User Activity',
        'new_users_metric': 'New Users',
        'sessions_metric': 'Sessions',
        'app_opens_metric': 'App Opens',
        'logins_metric': 'Logins',
        'uninstalls_metric': 'Uninstalls',
        
        'practice_engagement_group': '🏃‍♀️ Practice & Engagement',
        'exercise_views_metric': 'Exercise Views',
        'video_practice_metric': 'Video Practice',
        'ai_practice_metric': 'AI Practice',
        'ai_chat_metric': 'AI Chat',
        'avg_engagement_metric': 'Avg. Engagement',
        
        'features_content_group': '🎯 Features & Content',
        'health_surveys_metric': 'Health Surveys',
        'roadmap_views_metric': 'Roadmap Views',
        'store_views_metric': 'Store Views',
        
        'popup_performance_group': '💬 Popup Performance',
        'shown_metric': 'Shown',
        'details_viewed_metric': 'Details Viewed',
        'closed_metric': 'Closed',
        'ctr_metric': 'CTR',
        'notification_group': '📣 Notifications & Messaging',
        'notifications_received_metric': 'Notifications Received',
        'notifications_opened_metric': 'Notifications Opened',
        'notifications_dismissed_metric': 'Notifications Dismissed',
        'notification_clicks_metric': 'Notification Clicks',
        'banner_clicks_metric': 'Banner Clicks',
        'notification_open_rate_metric': 'Open Rate',
        'notification_dismiss_rate_metric': 'Dismiss Rate',
        'notification_click_rate_metric': 'Click-Through Rate',
        
        'monetization_group': '💰 Monetization',
        'in_app_purchases_metric': 'In-App Purchases',
        'conversion_rate_metric': 'Conversion Rate',
        'total_revenue_events_metric': 'Total Revenue Events',
        
        'showing_n_days_info': '📊 Showing data for {days} day(s). Need at least 7 days for full weekly overview.',
        
        # Feature adoption (now changed to performance)
        'feature_adoption_header': '📊 Feature Performance Analysis',
        'most_used_features': '**🏆 Most Used Features:**',
        'growing_features': '**📈 Growing Features:**',
        'underutilized_features': '**⚠️ Underutilized Features:**',
        
        # Export section
        'export_header': '📤 Export Data',
        'export_raw_data': '📊 Export Raw Data (CSV)',
        'download_csv': 'Download CSV',
        'export_insights': '🧠 Export Insights (TXT)',
        'download_insights': 'Download Insights',
        'export_summary': '📋 Export Summary Report',
        'download_summary': 'Download Summary',
        
        # Data format section
        'expected_data_format': '📋 Expected Data Format',
        'show_expected_format': 'Show Expected Data Format',
        'format_description': 'Your n8n webhook should return JSON data with the following structure:',
        
        # Language selector
        'language_selector': '🌍 Language / Ngôn ngữ',
        'english': 'English',
        'vietnamese': 'Tiếng Việt',
        
        # Debug section
        'debug_raw_response': '🔍 Debug: Raw Response Data',
        
        # Chart content
        'new_users': 'New Users',
        'app_removals': 'App Removals', 
        'returning_users': 'Returning Users',
        'user_category': 'User Category',
        'count': 'Count',
        'user_acquisition_vs_churn_title': 'User Acquisition vs Churn Analysis',
        'video_practice': 'Video Practice',
        'ai_practice': 'AI Practice', 
        'sessions': 'Sessions',
        'practice_session_preferences_title': 'Practice Session Preferences',
        'percentage': 'Percentage',
        'feature_usage_title': 'Feature Usage Distribution',
        'ai_engagement_title': 'AI Feature Engagement',
        'popup_performance_title': 'Popup Interaction Analysis',
        'week': 'Week',
        'metrics_trends_title': 'All Metrics Trends Over Time',
        'user_flow_trends_title': 'User Flow Trends',
        'churn': 'Churn',
        'practice_trends_title': 'Practice Session Trends',
        'popups_shown': 'Popups Shown',
        'popups_viewed': 'Popups Viewed',
        'interaction_rate': 'Interaction Rate',
        'day': 'Day',
        'date': 'Date',
        'person': 'person',
        'persons': 'persons',
        
        # Insights content
        'retention_excellent': 'Excellent user retention rate of {rate:.1%} - significantly higher than industry average',
        'retention_average': 'Average retention rate of {rate:.1%} - room for improvement', 
        'retention_low': 'Low retention rate of {rate:.1%} - requires immediate attention',
        'churn_high': 'High churn rate detected at {rate:.1%} - users leaving at concerning pace',
        'churn_acceptable': 'Churn rate of {rate:.1%} within acceptable range',
        'engagement_strong': 'Strong engagement rate of {rate:.1%} - users are actively practicing',
        'engagement_below_target': 'Engagement rate of {rate:.1%} below target - need to boost practice sessions',
        'video_preference': 'Users prefer guided video sessions over AI assistance',
        'ai_preference': 'Users are embracing AI-guided practice over traditional videos',
        'balanced_practice': 'Balanced usage between video and AI practice sessions',
        'exercise_content_popular': 'Exercise content very popular - users actively exploring workouts',
        'exercise_content_low': 'Low exercise content engagement - need to improve content discoverability',
        'roadmap_underused': 'Roadmap feature underutilized - users may not understand its value',
        'health_survey_high': 'High health survey completion rate - users care about health tracking',
        'ai_adoption_low': 'AI chat adoption at {rate:.1%} below target - need to promote AI features',
        'popup_conversion_excellent': 'Popup conversion rate of {rate:.1%} excellent - content is relevant',
        'popup_conversion_needs_improvement': 'Popup conversion rate of {rate:.1%} needs improvement - consider content relevance',
        'popup_close_rate_high': 'High popup close rate indicates users find them intrusive or irrelevant',
        
        # Recommendations
        'improve_onboarding': 'Implement improved onboarding process to increase user retention',
        'personalized_recommendations': 'Create personalized practice recommendations for new users',
        'add_gamification': 'Add gamification elements to increase practice session frequency',
        'push_notifications': 'Send push notifications to remind practice and maintain streaks',
        'highlight_roadmap': 'Highlight roadmap feature in app tutorial and main menu',
        'promote_ai_chat': 'Promote AI chat feature with tutorials and use cases',
        'ab_test_popup': 'A/B test popup timing and content to improve engagement',
        'reduce_popup_frequency': 'Reduce popup frequency to avoid user fatigue',
        
        # Opportunities
        'high_engagement_low_retention': 'High engagement but low retention - focus on habit formation features',
        'video_users_ai_benefit': 'Video users could benefit from AI personalization - cross-promote features',
        'browse_more_than_practice': 'Users browse more than they practice - simplify practice initiation',
        'high_health_survey_engagement': 'High health survey engagement - expand wellness tracking features',
        
        # Feature Performance (changed from adoption)
        'feature_performance_header': '📊 Feature Performance Analysis',
        
        # Weekly breakdown content
        'best_week_new_users_text': '**📈 Best Week (New Users):**',
        'most_engaged_week_text': '**💪 Most Engaged Week:**',
        'top_ai_week_text': '**🤖 Top AI Week:**',
        'week_colon': 'Week:',
        'new_users_colon': 'New Users:',
        'practice_sessions_colon': 'Practice Sessions:',
        'ai_interactions_colon': 'AI Interactions:',
        
        # Export buttons
        'export_kpis': '📈 Export KPIs (JSON)',
        'download_kpis': 'Download KPIs',
        'export_insights_txt': '🧠 Export Insights (TXT)',
        
        # Comparison Tab
        'comparison_tab_title': 'Period Comparison',
        'compare_by': 'Compare by:',
        'current_period': 'Current Period',
        'compare_to': 'Compare To',
        'generate_comparison': 'Generate Comparison Analysis',
        'period_comparison': 'Period Comparison',
        'trend_comparison': 'Trend Comparison',
        'comparison_summary': 'Comparison Summary',
        'detailed_metrics_comparison': 'Detailed Metrics Comparison',
        'change_abs': 'Change (Absolute)',
        'metrics': 'Metrics',
        'period_index': 'Period Index',
        'change_percent': 'Change %',
        'current': 'Current',
        'compare': 'Compare',
        'select_week': 'Select week:',
        'select_month': 'Select month:'
    },
    
    'vi': {
        # Main headers
        'page_title': 'Bảng Điều Khiển Phân Tích Ứng Dụng Yoga',
        'page_subtitle': 'Trực quan hóa các chỉ số tương tác người dùng và nhận thông tin chi tiết hữu ích để tối ưu hóa ứng dụng',
        
        # Data source section
        'data_source_header': '📡 Cấu Hình Nguồn Dữ Liệu',
        'webhook_input_label': 'Nhập URL webhook n8n của bạn:',
        'webhook_placeholder': 'https://your-n8n-instance.com/webhook/yoga-analytics',
        'webhook_help': 'Dán URL webhook n8n trả về dữ liệu JSON với các chỉ số ứng dụng yoga',
        'fetch_data_button': '🔄 Lấy Dữ Liệu',
        
        # Status messages
        'fetching_data': 'Đang lấy dữ liệu từ webhook...',
        'data_fetched_success': '✅ Lấy dữ liệu thành công!',
        'invalid_data_format': '❌ Định dạng dữ liệu không hợp lệ từ webhook',
        'webhook_not_found': '❌ Không tìm thấy webhook (404). Vui lòng kiểm tra:',
        'server_error': '❌ Lỗi máy chủ (500). Quy trình n8n của bạn có thể có lỗi.',
        'connection_failed': '❌ Kết nối thất bại. Vui lòng kiểm tra:',
        'request_timeout': '❌ Yêu cầu hết thời gian. Webhook có thể mất quá nhiều thời gian để phản hồi.',
        'invalid_json': '❌ Phản hồi JSON không hợp lệ từ webhook',
        'enter_webhook_url': '❌ Vui lòng nhập URL webhook',
        
        # Date filter section
        'date_filter_header': '📅 Bộ Lọc Khoảng Thời Gian',
        'start_date_label': 'Ngày Bắt Đầu:',
        'end_date_label': 'Ngày Kết Thúc:',
        'apply_filter_button': '🔄 Áp Dụng Bộ Lọc',
        'show_all_data_button': '📊 Hiển Thị Tất Cả Dữ Liệu',
        'filter_applied': '✅ Đã áp dụng bộ lọc! Hiển thị dữ liệu {count} tuần.',
        'showing_all_data': '✅ Hiển thị tất cả dữ liệu có sẵn.',
        'no_data_matches': '❌ Không có dữ liệu nào khớp với khoảng thời gian đã chọn',
        'currently_showing_filtered': '🎯 Hiện đang hiển thị dữ liệu đã lọc: {count} tuần',
        'showing_all_available': '📊 Hiển thị tất cả dữ liệu có sẵn (chưa áp dụng bộ lọc)',
        'preview_weeks': '📊 Xem trước: {count} tuần sẽ được bao gồm',
        'no_weeks_match': '⚠️ Không có tuần nào khớp với khoảng thời gian này',
        
        # KPI section (combined with Last Week Overview)
        'key_performance_header': '📊 Chỉ Số Hiệu Suất Chính & Số Liệu Tuần',
        'kpi_overview_subheader': '🎯 Top 5 KPI',
        'all_metrics_subheader': '📋 Tất Cả Số Liệu (7 Ngày Qua)',
        'latest_week': '📅 Tuần Mới Nhất: {current} (so với Tuần Trước: {previous})',
        'total_new_users': '👥 Tổng Người Dùng Mới',
        'user_retention_rate': '🔄 Tỷ Lệ Giữ Chân Người Dùng',
        'churn_rate': '📉 Tỷ Lệ Rời Bỏ',
        'active_sessions': '🎯 Phiên Hoạt Động',
        'engagement_rate': '💪 Tỷ Lệ Tương Tác',
        'avg_engagement_time': '⏱️ Thời Gian Tương Tác TB',
        
        # Country analytics
        'analytics': 'Phân Tích',
        'all_countries_analytics': 'Phân Tích Tất Cả Các Quốc Gia',
        
        # Charts section
        'analytics_overview_header': '📈 Tổng Quan Phân Tích',
        'time_series_analysis': '📊 Phân Tích Chuỗi Thời Gian',
        'user_flow_trends': '👥 Xu Hướng Luồng Người Dùng',
        'practice_trends': '🏃‍♀️ Xu Hướng Luyện Tập',
        
        # Weekly breakdown
        'weekly_breakdown_header': '📅 Phân Tích Theo Tuần',
        'best_week_new_users': '**📈 Tuần Tốt Nhất (Người Dùng Mới):**',
        'most_engaged_week': '**💪 Tuần Tương Tác Nhiều Nhất:**',
        'top_ai_week': '**🤖 Tuần AI Hàng Đầu:**',
        'week_label': 'Tuần:',
        'new_users_label': 'Người Dùng Mới:',
        'practice_sessions_label': 'Phiên Luyện Tập:',
        'ai_interactions_label': 'Tương Tác AI:',
        
        # Chart titles
        'user_acquisition_vs_churn': '👥 Thu Hút Người Dùng vs Rời Bỏ',
        'overall_user_metrics': '👥 Chỉ Số Người Dùng Tổng Thể',
        'practice_preferences': '🏃‍♀️ Sở Thích Luyện Tập',
        'total_practice_distribution': '🏃‍♀️ Phân Bố Luyện Tập Tổng Thể',
        'feature_usage_analysis': '📱 Phân Tích Sử Dụng Tính Năng',
        'feature_adoption_analysis': '🎯 Phễu Chấp Nhận Tính Năng',
        'feature_adoption_funnel_title': 'Hành Trình Chấp Nhận Tính Năng',
        'view_exercise_stage': 'Xem Bài Tập',
        'practice_video_stage': 'Tập Luyện Với Video',
        'practice_ai_stage': 'Tập Luyện Với AI',
        'chat_ai_stage': 'Trò Chuyện Với AI',
        'users_count': 'Người Dùng',
        'conversion_from_start': 'Tỷ Lệ Chuyển Đổi Từ Xem Bài Tập',
        'engagement_quality': '📊 Điểm Chất Lượng Tương Tác',
        'overall_engagement_score': '📊 Điểm Tương Tác Tổng Thể',
        'engagement_score': 'Điểm Tương Tác',
        'engagement_score_radar_title': 'Phân Tích Tương Tác Đa Chiều',
        'login_engagement': 'Hoạt Động Đăng Nhập',
        'health_awareness': 'Nhận Thức Sức Khỏe',
        'content_exploration': 'Khám Phá Nội Dung',
        'ai_interaction': 'Tương Tác AI',
        'popup_responsiveness': 'Phản Hồi Popup',
        'retention_strength': 'Độ Giữ Chân',
        'average_benchmark': 'Chuẩn Trung Bình',
        'ai_engagement_metrics': '🤖 Chỉ Số Tương Tác AI',
        
        # New chart titles and labels
        'user_activity_comparison_title': 'So Sánh Hoạt Động Người Dùng',
        'user_funnel_analysis_title': 'Phân Tích Phễu Người Dùng',
        'churn_risk_indicator_title': 'Chỉ Số Rủi Ro Rời Bỏ',
        'churn_risk_explain_button': 'ℹ️ Giải Thích',
        'churn_risk_explanation': '''**Chỉ số này đo lường:** Chỉ Số Rủi Ro Rời Bỏ cho thấy khả năng người dùng rời bỏ ứng dụng của bạn. Nó kết hợp các tín hiệu tiêu cực (gỡ cài đặt, từ chối thông báo) với các tín hiệu tích cực (mở ứng dụng, hành động cốt lõi, mua hàng) và thời gian tương tác thành một điểm rủi ro duy nhất.

**Cách tính toán:**
$$Risk = \\frac{(app\\_remove \\times 10) + (notification\\_dismiss \\times 1)}{(app\\_open \\times 1) + (CoreActions \\times 3) + (in\\_app\\_purchase \\times 10)} \\times \\frac{1}{avg\\_engage\\_time}$$

Trong đó CoreActions = practice_with_video + practice_with_ai + chat_ai, và avg_engage_time tính bằng phút.

**Các Vùng Rủi Ro:**
- **Rủi Ro Thấp (< 0.1):** 🟢 Tương tác người dùng tốt - người dùng đang hoạt động và gắn bó
- **Rủi Ro Trung Bình (0.1 đến 0.5):** 🟠 Cần chú ý - có một số tín hiệu tiêu cực, nên có hành động
- **Rủi Ro Cao (> 0.5):** 🔴 Cần hành động khẩn cấp - rủi ro rời bỏ cao, cần can thiệp ngay lập tức

**Cách hiểu:** Điểm số thấp hơn là tốt hơn. Điểm dưới 0.1 cho thấy tương tác tốt, trong khi điểm trên 0.5 cho thấy bạn cần tập trung vào việc giảm gỡ cài đặt, cải thiện tương tác thông báo và tăng các hành động cốt lõi của người dùng.''',
        'new_users': 'Người Dùng Mới',
        'active_sessions': 'Phiên Hoạt Động',
        'total_practice': 'Tổng Luyện Tập',
        'risk_level_low': 'Rủi Ro Thấp',
        'risk_level_medium': 'Rủi Ro Trung Bình',
        'risk_level_high': 'Rủi Ro Cao',
        
        # Popup performance
        'popup_performance_header': '💬 Hiệu Suất Popup',
        'total_popups_shown': '👁️ Tổng Popup Hiển Thị',
        'detail_views': '🔍 Lượt Xem Chi Tiết',
        'conversion_rate': '💯 Tỷ Lệ Chuyển Đổi',
        'notification_performance_header': '📣 Hiệu Suất Thông Báo',
        'notification_chart_title': 'Tương Tác Thông Báo & Banner',
        
        # Insights section
        'insights_header': '🧠 Thông Tin Chi Tiết & Khuyến Nghị',
        'overall_insights': '🌍 Thông Tin Tổng Quan',
        'overall_insights_subtitle': '*Dựa trên tất cả dữ liệu có sẵn*',
        'this_week_insights': '📅 Thông Tin Tuần Này',
        'this_week_insights_subtitle': '*Dựa trên 2 tuần gần nhất*',
        'recommendations_header': '🚀 Khuyến Nghị',
        'key_insights_header': '🎯 Thông Tin Chính',
        
        # All Metrics (Last 7 Days) section labels
        'user_activity_group': '👥 Hoạt Động Người Dùng',
        'new_users_metric': 'Người Dùng Mới',
        'sessions_metric': 'Phiên',
        'app_opens_metric': 'Mở Ứng Dụng',
        'logins_metric': 'Đăng Nhập',
        'uninstalls_metric': 'Gỡ Cài Đặt',
        
        'practice_engagement_group': '🏃‍♀️ Luyện Tập & Tương Tác',
        'exercise_views_metric': 'Lượt Xem Bài Tập',
        'video_practice_metric': 'Luyện Tập Video',
        'ai_practice_metric': 'Luyện Tập AI',
        'ai_chat_metric': 'Chat AI',
        'avg_engagement_metric': 'Tương Tác TB',
        
        'features_content_group': '🎯 Tính Năng & Nội Dung',
        'health_surveys_metric': 'Khảo Sát Sức Khỏe',
        'roadmap_views_metric': 'Lượt Xem Lộ Trình',
        'store_views_metric': 'Lượt Xem Cửa Hàng',
        
        'popup_performance_group': '💬 Hiệu Suất Popup',
        'shown_metric': 'Hiển Thị',
        'details_viewed_metric': 'Xem Chi Tiết',
        'closed_metric': 'Đóng',
        'ctr_metric': 'CTR',
        'notification_group': '📣 Thông Báo & Tin Nhắn',
        'notifications_received_metric': 'Thông Báo Đã Gửi',
        'notifications_opened_metric': 'Thông Báo Được Mở',
        'notifications_dismissed_metric': 'Thông Báo Bị Gỡ',
        'notification_clicks_metric': 'Nhấp Thông Báo',
        'banner_clicks_metric': 'Nhấp Banner',
        'notification_open_rate_metric': 'Tỷ Lệ Mở',
        'notification_dismiss_rate_metric': 'Tỷ Lệ Gỡ',
        'notification_click_rate_metric': 'Tỷ Lệ Nhấp',
        
        'monetization_group': '💰 Kiếm Tiền',
        'in_app_purchases_metric': 'Mua Trong Ứng Dụng',
        'conversion_rate_metric': 'Tỷ Lệ Chuyển Đổi',
        'total_revenue_events_metric': 'Tổng Sự Kiện Doanh Thu',
        
        'showing_n_days_info': '📊 Hiển thị dữ liệu cho {days} ngày. Cần ít nhất 7 ngày để có tổng quan đầy đủ theo tuần.',
        
        # Feature adoption (now changed to performance)
        'feature_adoption_header': '📊 Phân Tích Hiệu Suất Tính Năng',
        'most_used_features': '**🏆 Tính Năng Được Sử Dụng Nhiều Nhất:**',
        'growing_features': '**📈 Tính Năng Đang Phát Triển:**',
        'underutilized_features': '**⚠️ Tính Năng Chưa Được Sử Dụng Hiệu Quả:**',
        
        # Export section
        'export_header': '📤 Xuất Dữ Liệu',
        'export_raw_data': '📊 Xuất Dữ Liệu Thô (CSV)',
        'download_csv': 'Tải CSV',
        'export_insights': '🧠 Xuất Thông Tin Chi Tiết (TXT)',
        'download_insights': 'Tải Thông Tin Chi Tiết',
        'export_summary': '📋 Xuất Báo Cáo Tóm Tắt',
        'download_summary': 'Tải Tóm Tắt',
        
        # Data format section
        'expected_data_format': '📋 Định Dạng Dữ Liệu Mong Đợi',
        'show_expected_format': 'Hiển Thị Định Dạng Dữ Liệu Mong Đợi',
        'format_description': 'Webhook n8n của bạn nên trả về dữ liệu JSON với cấu trúc sau:',
        
        # Language selector
        'language_selector': '🌍 Language / Ngôn ngữ',
        'english': 'English',
        'vietnamese': 'Tiếng Việt',
        
        # Debug section
        'debug_raw_response': '🔍 Debug: Dữ Liệu Phản Hồi Thô',
        
        # Chart content
        'new_users': 'Người Dùng Mới',
        'app_removals': 'Xóa Ứng Dụng', 
        'returning_users': 'Người Dùng Quay Lại',
        'user_category': 'Danh Mục Người Dùng',
        'count': 'Số Lượng',
        'user_acquisition_vs_churn_title': 'Phân Tích Thu Hút vs Rời Bỏ Người Dùng',
        'video_practice': 'Luyện Tập Video',
        'ai_practice': 'Luyện Tập AI', 
        'sessions': 'Phiên',
        'practice_session_preferences_title': 'Sở Thích Phiên Luyện Tập',
        'percentage': 'Tỷ Lệ Phần Trăm',
        'feature_usage_title': 'Phân Bố Sử Dụng Tính Năng',
        'ai_engagement_title': 'Tương Tác Tính Năng AI',
        'popup_performance_title': 'Phân Tích Tương Tác Popup',
        'week': 'Tuần',
        'metrics_trends_title': 'Xu Hướng Tất Cả Chỉ Số Theo Thời Gian',
        'user_flow_trends_title': 'Xu Hướng Luồng Người Dùng',
        'churn': 'Rời Bỏ',
        'practice_trends_title': 'Xu Hướng Phiên Luyện Tập',
        'popups_shown': 'Popup Hiển Thị',
        'popups_viewed': 'Popup Được Xem',
        'interaction_rate': 'Tỷ Lệ Tương Tác',
        'day': 'Ngày',
        'date': 'Ngày Tháng',
        'person': 'người',
        'persons': 'người',
        
        # Feature Performance (changed from adoption)
        'feature_performance_header': '📊 Phân Tích Hiệu Suất Tính Năng',
        
        # Weekly breakdown content  
        'best_week_new_users_text': '**📈 Tuần Tốt Nhất (Người Dùng Mới):**',
        'most_engaged_week_text': '**💪 Tuần Tương Tác Nhiều Nhất:**',
        'top_ai_week_text': '**🤖 Tuần AI Hàng Đầu:**',
        'week_colon': 'Tuần:',
        'new_users_colon': 'Người Dùng Mới:',
        'practice_sessions_colon': 'Phiên Luyện Tập:',
        'ai_interactions_colon': 'Tương Tác AI:',
        
        # Export buttons
        'export_kpis': '📈 Xuất KPIs (JSON)',
        'download_kpis': 'Tải KPIs',
        'export_insights_txt': '🧠 Xuất Thông Tin Chi Tiết (TXT)',
        
        # Comparison Tab
        'comparison_tab_title': 'So Sánh Thời Kỳ',
        'compare_by': 'So sánh theo:',
        'current_period': 'Thời Kỳ Hiện Tại',
        'compare_to': 'So Sánh Với',
        'generate_comparison': 'Tạo Phân Tích So Sánh',
        'period_comparison': 'So Sánh Thời Kỳ',
        'trend_comparison': 'So Sánh Xu Hướng',
        'comparison_summary': 'Tóm Tắt So Sánh',
        'detailed_metrics_comparison': 'So Sánh Chi Tiết Các Chỉ Số',
        'change_abs': 'Thay Đổi Tuyệt Đối',
        'metrics': 'Chỉ Số',
        'period_index': 'Chỉ Số Thời Kỳ',
        'change_percent': 'Thay Đổi %',
        'current': 'Hiện Tại',
        'compare': 'So Sánh',
        'select_week': 'Chọn tuần:',
        'select_month': 'Chọn tháng:'
    }
}

def get_text(key, lang='en', **kwargs):
    """Get translated text for the given key and language."""
    text = TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))
    
    # Handle format strings with keyword arguments
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    
    return text

def get_language_options():
    """Get available language options for the selector."""
    return {
        'English': 'en',
        'Tiếng Việt': 'vi'
    }