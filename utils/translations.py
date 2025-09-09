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
        
        # KPI section
        'key_performance_header': '📊 Key Performance',
        'latest_week': '📅 Latest Week: {current} (vs Previous Week: {previous})',
        'total_new_users': '👥 Total New Users',
        'user_retention_rate': '🔄 User Retention Rate',
        'churn_rate': '📉 Churn Rate',
        'active_sessions': '🎯 Active Sessions',
        'engagement_rate': '💪 Engagement Rate',
        
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
        'ai_engagement_metrics': '🤖 AI Engagement Metrics',
        
        # Popup performance
        'popup_performance_header': '💬 Popup Performance Dashboard',
        'total_popups_shown': '👁️ Total Popups Shown',
        'detail_views': '🔍 Detail Views',
        'conversion_rate': '💯 Conversion Rate',
        
        # Insights section
        'insights_header': '🧠 Insights & Recommendations',
        'overall_insights': '🌍 Overall Insights',
        'overall_insights_subtitle': '*Based on all available data*',
        'this_week_insights': '📅 This Week Insights',
        'this_week_insights_subtitle': '*Based on last 2 weeks*',
        'recommendations_header': '🚀 Recommendations',
        'key_insights_header': '🎯 Key Insights',
        
        # Feature adoption
        'feature_adoption_header': '📊 Feature Adoption Analysis',
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
        'debug_raw_response': '🔍 Debug: Raw Response Data'
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
        
        # KPI section
        'key_performance_header': '📊 Hiệu Suất Chính',
        'latest_week': '📅 Tuần Mới Nhất: {current} (so với Tuần Trước: {previous})',
        'total_new_users': '👥 Tổng Người Dùng Mới',
        'user_retention_rate': '🔄 Tỷ Lệ Giữ Chân Người Dùng',
        'churn_rate': '📉 Tỷ Lệ Rời Bỏ',
        'active_sessions': '🎯 Phiên Hoạt Động',
        'engagement_rate': '💪 Tỷ Lệ Tương Tác',
        
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
        'ai_engagement_metrics': '🤖 Chỉ Số Tương Tác AI',
        
        # Popup performance
        'popup_performance_header': '💬 Hiệu Suất Popup',
        'total_popups_shown': '👁️ Tổng Popup Hiển Thị',
        'detail_views': '🔍 Lượt Xem Chi Tiết',
        'conversion_rate': '💯 Tỷ Lệ Chuyển Đổi',
        
        # Insights section
        'insights_header': '🧠 Thông Tin Chi Tiết & Khuyến Nghị',
        'overall_insights': '🌍 Thông Tin Tổng Quan',
        'overall_insights_subtitle': '*Dựa trên tất cả dữ liệu có sẵn*',
        'this_week_insights': '📅 Thông Tin Tuần Này',
        'this_week_insights_subtitle': '*Dựa trên 2 tuần gần nhất*',
        'recommendations_header': '🚀 Khuyến Nghị',
        'key_insights_header': '🎯 Thông Tin Chính',
        
        # Feature adoption
        'feature_adoption_header': '📊 Phân Tích Chấp Nhận Tính Năng',
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
        'debug_raw_response': '🔍 Debug: Dữ Liệu Phản Hồi Thô'
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