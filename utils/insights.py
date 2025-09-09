import numpy as np
from datetime import datetime
from .translations import get_text

class InsightsGenerator:
    """Generates actionable insights and recommendations from yoga app analytics data."""
    
    def __init__(self):
        self.benchmarks = {
            'retention_rate_good': 0.3,      # 30% retention is considered good
            'churn_rate_warning': 0.2,       # 20% churn rate is concerning
            'engagement_rate_good': 0.4,     # 40% engagement is good
            'popup_conversion_good': 0.15,   # 15% popup conversion is good
            'ai_adoption_target': 0.25       # 25% AI adoption target
        }
    
    def generate_insights(self, data, kpis, language='en'):
        """Generate comprehensive insights from the analytics data."""
        insights = {
            'key_insights': [],
            'recommendations': [],
            'alerts': [],
            'opportunities': []
        }
        
        # Analyze retention (returns tuples with sentiment)
        insights['key_insights'].extend(self._analyze_retention(kpis, language))
        
        # Analyze engagement (returns tuples with sentiment)
        insights['key_insights'].extend(self._analyze_engagement(data, kpis, language))
        
        # Analyze feature usage (returns tuples with sentiment)
        insights['key_insights'].extend(self._analyze_feature_usage(data, language))
        
        # Analyze popup performance (returns tuples with sentiment)
        insights['key_insights'].extend(self._analyze_popup_performance(data, language))
        
        # Generate recommendations (still strings)
        insights['recommendations'].extend(self._generate_recommendations(data, kpis, language))
        
        # Identify opportunities (still strings)
        insights['opportunities'].extend(self._identify_opportunities(data, kpis, language))
        
        return insights
    
    def generate_split_insights(self, overall_data, overall_kpis, recent_data, recent_kpis, language='en'):
        """Generate insights split into 'Overall' and 'This Week' sections."""
        # Generate overall insights
        overall_insights = self.generate_insights(overall_data, overall_kpis, language)
        
        # Generate recent week insights
        recent_insights = self.generate_insights(recent_data, recent_kpis, language)
        
        return {
            'overall': {
                'key_insights': overall_insights['key_insights'],
                'recommendations': overall_insights['recommendations'],
                'opportunities': overall_insights['opportunities']
            },
            'this_week': {
                'key_insights': recent_insights['key_insights'],
                'recommendations': recent_insights['recommendations'],
                'opportunities': recent_insights['opportunities']
            }
        }
    
    def _analyze_retention(self, kpis, language='en'):
        """Analyze user retention metrics."""
        insights = []
        retention_rate = kpis.get('retention_rate', 0)
        churn_rate = kpis.get('churn_rate', 0)
        
        if retention_rate > self.benchmarks['retention_rate_good']:
            insights.append(("positive", f"Tỷ lệ giữ chân người dùng xuất sắc ở mức {retention_rate:.1%} - cao hơn đáng kể so với trung bình ngành"))
        elif retention_rate > 0.15:
            insights.append(("neutral", f"Tỷ lệ giữ chân ở mức trung bình {retention_rate:.1%} - có thể cải thiện"))
        else:
            insights.append(("negative", f"Tỷ lệ giữ chân thấp {retention_rate:.1%} - cần chú ý ngay lập tức"))
        
        if churn_rate > self.benchmarks['churn_rate_warning']:
            insights.append(("negative", f"Phát hiện tỷ lệ rời bỏ cao {churn_rate:.1%} - người dùng đang rời đi với tốc độ đáng lo ngại"))
        else:
            insights.append(("positive", f"Tỷ lệ rời bỏ {churn_rate:.1%} nằm trong phạm vi chấp nhận được"))
        
        return insights
    
    def _analyze_engagement(self, data, kpis, language='en'):
        """Analyze user engagement patterns."""
        insights = []
        engagement_rate = kpis.get('engagement_rate', 0)
        
        practice_video = data.get('practice_with_video', 0)
        practice_ai = data.get('practice_with_ai', 0)
        total_practice = practice_video + practice_ai
        
        if engagement_rate > self.benchmarks['engagement_rate_good']:
            insights.append(("positive", f"Tỷ lệ tương tác mạnh {engagement_rate:.1%} - người dùng đang tích cực luyện tập"))
        else:
            insights.append(("negative", f"Tỷ lệ tương tác {engagement_rate:.1%} dưới mục tiêu - cần tăng cường buổi luyện tập"))
        
        # Analyze practice preferences
        if total_practice > 0:
            video_preference = practice_video / total_practice
            if video_preference > 0.7:
                insights.append(("neutral", "Người dùng thích buổi luyện tập có hướng dẫn video hơn hỗ trợ AI"))
            elif video_preference < 0.3:
                insights.append(("positive", "Người dùng đang ưa chuộng buổi luyện tập có hướng dẫn AI hơn video truyền thống"))
            else:
                insights.append(("positive", "Sử dụng cân bằng giữa buổi luyện tập video và AI"))
        
        return insights
    
    def _analyze_feature_usage(self, data, language='en'):
        """Analyze feature adoption and usage patterns."""
        insights = []
        
        # Calculate feature utilization
        exercise_views = data.get('view_exercise', 0)
        roadmap_views = data.get('view_roadmap', 0)
        health_surveys = data.get('health_survey', 0)
        ai_chat = data.get('chat_ai', 0)
        
        total_sessions = data.get('session_start', 1)
        
        # Exercise content analysis
        if exercise_views / total_sessions > 0.8:
            insights.append(("positive", "Nội dung bài tập rất phổ biến - người dùng đang tích cực khám phá các bài tập"))
        elif exercise_views / total_sessions < 0.3:
            insights.append(("negative", "Tương tác với nội dung bài tập thấp - cần cải thiện khả năng khám phá nội dung"))
        
        # Roadmap feature analysis
        if roadmap_views / total_sessions < 0.2:
            insights.append(("negative", "Tính năng lộ trình được sử dụng ít - người dùng có thể không hiểu giá trị của nó"))
        
        # Health survey completion
        if health_surveys / total_sessions > 0.7:
            insights.append(("positive", "Tỷ lệ hoàn thành khảo sát sức khỏe cao - người dùng quan tâm đến theo dõi sức khỏe"))
        
        # AI chat adoption
        ai_adoption_rate = ai_chat / total_sessions
        if ai_adoption_rate < self.benchmarks['ai_adoption_target']:
            insights.append(("negative", f"Việc áp dụng chat AI ở mức {ai_adoption_rate:.1%} dưới mục tiêu - cần quảng bá tính năng AI"))
        
        return insights
    
    def _analyze_popup_performance(self, data, language='en'):
        """Analyze popup effectiveness and user interaction."""
        insights = []
        
        popups_shown = data.get('show_popup', 0)
        detail_views = data.get('view_detail_popup', 0)
        popups_closed = data.get('close_popup', 0)
        
        if popups_shown > 0:
            conversion_rate = detail_views / popups_shown
            close_rate = popups_closed / popups_shown
            
            if conversion_rate > self.benchmarks['popup_conversion_good']:
                insights.append(("positive", f"Tỷ lệ chuyển đổi popup {conversion_rate:.1%} xuất sắc - nội dung phù hợp"))
            else:
                insights.append(("negative", f"Tỷ lệ chuyển đổi popup {conversion_rate:.1%} cần cải thiện - xem xét tính phù hợp của nội dung"))
            
            if close_rate > 0.8:
                insights.append(("negative", "Tỷ lệ đóng popup cao cho thấy người dùng thấy chúng xâm phạm hoặc không phù hợp"))
            
        return insights
    
    def _generate_recommendations(self, data, kpis, language='en'):
        """Generate actionable recommendations based on data analysis."""
        recommendations = []
        
        # Retention recommendations
        if kpis.get('retention_rate', 0) < self.benchmarks['retention_rate_good']:
            recommendations.append("Thực hiện cải tiến quy trình giới thiệu để tăng khả năng giữ chân người dùng")
            recommendations.append("Tạo khuyến nghị luyện tập cá nhân hóa cho người dùng mới")
        
        # Engagement recommendations
        if kpis.get('engagement_rate', 0) < self.benchmarks['engagement_rate_good']:
            recommendations.append("Thêm yếu tố gamification để tăng tần suất buổi luyện tập")
            recommendations.append("Gửi thông báo đẩy để nhắc nhở luyện tập và duy trì chuỗi")
        
        # Feature usage recommendations
        roadmap_usage = data.get('view_roadmap', 0) / data.get('session_start', 1)
        if roadmap_usage < 0.2:
            recommendations.append("Làm nổi bật tính năng lộ trình trong hướng dẫn ứng dụng và menu chính")
        
        ai_usage = data.get('chat_ai', 0) / data.get('session_start', 1)
        if ai_usage < 0.25:
            recommendations.append("Quảng bá tính năng chat AI với hướng dẫn và các trường hợp sử dụng")
        
        # Popup recommendations
        popup_conversion = data.get('view_detail_popup', 0) / max(data.get('show_popup', 1), 1)
        if popup_conversion < 0.15:
            recommendations.append("Kiểm tra A/B thời gian và nội dung popup để cải thiện tương tác")
            recommendations.append("Giảm tần suất popup để tránh mệt mỏi người dùng")
        
        return recommendations
    
    def _identify_opportunities(self, data, kpis, language='en'):
        """Identify growth opportunities and optimization areas."""
        opportunities = []
        
        # High engagement, low retention opportunity
        if kpis.get('engagement_rate', 0) > 0.4 and kpis.get('retention_rate', 0) < 0.3:
            opportunities.append("Tương tác cao nhưng giữ chân thấp - tập trung vào tính năng hình thành thói quen")
        
        # AI adoption opportunity
        practice_video = data.get('practice_with_video', 0)
        practice_ai = data.get('practice_with_ai', 0)
        if practice_video > practice_ai * 3:
            opportunities.append("Người dùng video có thể hưởng lợi từ cá nhân hóa AI - quảng bá chéo tính năng")
        
        # Content expansion opportunity
        exercise_views = data.get('view_exercise', 0)
        practice_sessions = practice_video + practice_ai
        if exercise_views > practice_sessions * 2:
            opportunities.append("Người dùng duyệt nhiều hơn thực hành - đơn giản hóa việc bắt đầu luyện tập")
        
        # Health tracking opportunity
        health_surveys = data.get('health_survey', 0)
        total_users = kpis.get('total_new_users', 0) + kpis.get('total_app_opens', 0)
        if health_surveys / max(total_users, 1) > 0.6:
            opportunities.append("Tương tác khảo sát sức khỏe cao - mở rộng tính năng theo dõi sức khỏe")
        
        return opportunities
    
    def export_insights_text(self, insights):
        """Export insights as formatted text for download."""
        text_output = f"Yoga App Analytics Insights Report\n"
        text_output += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        text_output += "=" * 50 + "\n\n"
        
        text_output += "KEY INSIGHTS:\n"
        text_output += "-" * 20 + "\n"
        for insight in insights['key_insights']:
            text_output += f"• {insight}\n"
        
        text_output += "\nRECOMMENDATIONS:\n"
        text_output += "-" * 20 + "\n"
        for recommendation in insights['recommendations']:
            text_output += f"• {recommendation}\n"
        
        if insights.get('opportunities'):
            text_output += "\nOPPORTUNITIES:\n"
            text_output += "-" * 20 + "\n"
            for opportunity in insights['opportunities']:
                text_output += f"• {opportunity}\n"
        
        return text_output
    
    def calculate_health_score(self, data, kpis):
        """Calculate an overall app health score."""
        score = 0
        max_score = 100
        
        # Retention score (30 points)
        retention_rate = kpis.get('retention_rate', 0)
        score += min(30, retention_rate * 100)
        
        # Engagement score (25 points)
        engagement_rate = kpis.get('engagement_rate', 0)
        score += min(25, engagement_rate * 62.5)
        
        # Feature adoption score (20 points)
        total_sessions = data.get('session_start', 1)
        ai_adoption = data.get('chat_ai', 0) / total_sessions
        score += min(20, ai_adoption * 80)
        
        # Popup performance score (15 points)
        popup_conversion = data.get('view_detail_popup', 0) / max(data.get('show_popup', 1), 1)
        score += min(15, popup_conversion * 100)
        
        # Churn prevention score (10 points)
        churn_rate = kpis.get('churn_rate', 0)
        score += max(0, 10 - (churn_rate * 50))
        
        return min(score, max_score)
