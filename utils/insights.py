import numpy as np
from datetime import datetime
from .translations import get_text

class InsightsGenerator:
    """Generates actionable insights and recommendations from yoga app analytics data."""
    
    def __init__(self):
        # Industry benchmarks based on AppsFlyer, Business of Apps, Adjust (2024-2025)
        # Source: Health & Fitness App Benchmarks Report 2025
        self.benchmarks = {
            # Retention benchmarks (fitness/yoga apps have lower retention than average apps)
            'retention_rate_excellent': 0.475,  # 47.5% - top performers (90-day retention)
            'retention_rate_good': 0.12,        # 12% - Day 7 retention (industry average)
            'retention_rate_average': 0.03,     # 3% - Day 30 retention (industry average)
            
            # Churn benchmarks
            'churn_rate_excellent': 0.13,       # 13% monthly churn (best-in-class, e.g., Headspace)
            'churn_rate_warning': 0.18,         # 18% monthly churn (industry average)
            'churn_rate_critical': 0.25,        # 25%+ monthly churn (needs immediate action)
            
            # Engagement benchmarks
            'engagement_time_excellent': 600,   # 10+ minutes (600+ seconds) - top apps
            'engagement_time_good': 450,        # 7.5 minutes (450 seconds) - industry average
            'engagement_time_minimum': 300,     # 5 minutes (300 seconds) - below this is concerning
            'engagement_rate_good': 0.25,       # 25% DAU/MAU - healthy engagement
            'engagement_rate_minimum': 0.20,    # 20% DAU/MAU - baseline
            
            # Feature adoption benchmarks
            'popup_conversion_good': 0.15,      # 15% popup CTR is good
            'popup_conversion_minimum': 0.05,   # 5% minimum acceptable CTR
            'ai_adoption_target': 0.49,         # 49% daily AI usage (2025 benchmark)
            'ai_adoption_minimum': 0.20,        # 20% minimum AI adoption
            
            # Workout/practice completion
            'practice_completion_good': 0.70,   # 70%+ completion boosts LTV by 43%
            'practice_completion_minimum': 0.50 # 50% minimum acceptable completion
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
        """Analyze user retention metrics using industry benchmarks (2024-2025)."""
        insights = []
        retention_rate = kpis.get('retention_rate', 0)
        churn_rate = kpis.get('churn_rate', 0)
        
        # Retention analysis (benchmarks: 47.5% excellent, 12% good, 3% average)
        if retention_rate >= self.benchmarks['retention_rate_excellent']:
            insights.append(("positive", f"Tỷ lệ giữ chân người dùng vượt trội {retention_rate:.1%} - thuộc top ứng dụng fitness (benchmark: 47.5%)"))
        elif retention_rate >= self.benchmarks['retention_rate_good']:
            insights.append(("positive", f"Tỷ lệ giữ chân tốt {retention_rate:.1%} - đạt chuẩn ngành fitness (Day 7: 12%)"))
        elif retention_rate >= self.benchmarks['retention_rate_average']:
            insights.append(("neutral", f"Tỷ lệ giữ chân {retention_rate:.1%} đạt trung bình ngành (Day 30: 3%) - có thể cải thiện"))
        else:
            insights.append(("negative", f"Tỷ lệ giữ chân thấp {retention_rate:.1%} - dưới chuẩn ngành 3%, cần hành động ngay"))
        
        # Churn analysis (benchmarks: 13% excellent, 18% warning, 25%+ critical)
        if churn_rate <= self.benchmarks['churn_rate_excellent']:
            insights.append(("positive", f"Tỷ lệ rời bỏ xuất sắc {churn_rate:.1%} - đạt chuẩn best-in-class như Headspace (13%)"))
        elif churn_rate <= self.benchmarks['churn_rate_warning']:
            insights.append(("neutral", f"Tỷ lệ rời bỏ {churn_rate:.1%} trong phạm vi chấp nhận được (trung bình ngành: 18%)"))
        elif churn_rate <= self.benchmarks['churn_rate_critical']:
            insights.append(("negative", f"Tỷ lệ rời bỏ cao {churn_rate:.1%} - vượt trung bình ngành 18%, cần cải thiện"))
        else:
            insights.append(("negative", f"Tỷ lệ rời bỏ rất cao {churn_rate:.1%} - vượt ngưỡng nguy hiểm 25%, cần hành động khẩn cấp"))
        
        return insights
    
    def _analyze_engagement(self, data, kpis, language='en'):
        """Analyze user engagement patterns using industry benchmarks (2024-2025)."""
        insights = []
        engagement_rate = kpis.get('engagement_rate', 0)
        avg_engage_time = data.get('avg_engage_time', 0)
        
        # Engagement rate analysis (benchmarks: 25% good, 20% minimum)
        if engagement_rate >= self.benchmarks['engagement_rate_good']:
            insights.append(("positive", f"Tỷ lệ tương tác xuất sắc {engagement_rate:.1%} - vượt chuẩn 25% DAU/MAU"))
        elif engagement_rate >= self.benchmarks['engagement_rate_minimum']:
            insights.append(("neutral", f"Tỷ lệ tương tác {engagement_rate:.1%} đạt mức baseline 20% - có thể cải thiện"))
        else:
            insights.append(("negative", f"Tỷ lệ tương tác {engagement_rate:.1%} dưới chuẩn 20% - cần tăng cường tương tác"))
        
        # Average engagement time analysis (benchmarks: 600s excellent, 450s good, 300s minimum)
        if avg_engage_time >= self.benchmarks['engagement_time_excellent']:
            insights.append(("positive", f"Thời gian tương tác vượt trội {avg_engage_time/60:.1f} phút - thuộc top apps (10+ phút)"))
        elif avg_engage_time >= self.benchmarks['engagement_time_good']:
            insights.append(("positive", f"Thời gian tương tác tốt {avg_engage_time/60:.1f} phút - đạt chuẩn ngành 7.5 phút"))
        elif avg_engage_time >= self.benchmarks['engagement_time_minimum']:
            insights.append(("neutral", f"Thời gian tương tác {avg_engage_time/60:.1f} phút - chấp nhận được nhưng cần cải thiện"))
        else:
            insights.append(("negative", f"Thời gian tương tác thấp {avg_engage_time/60:.1f} phút - dưới ngưỡng 5 phút"))
        
        # Analyze practice preferences
        practice_video = data.get('practice_with_video', 0)
        practice_ai = data.get('practice_with_ai', 0)
        total_practice = practice_video + practice_ai
        
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
        
        # AI chat adoption (benchmark: 49% daily usage in 2025)
        ai_adoption_rate = ai_chat / total_sessions
        if ai_adoption_rate >= self.benchmarks['ai_adoption_target']:
            insights.append(("positive", f"Việc áp dụng chat AI xuất sắc {ai_adoption_rate:.1%} - đạt chuẩn ngành 49% (2025)"))
        elif ai_adoption_rate >= self.benchmarks['ai_adoption_minimum']:
            insights.append(("neutral", f"Việc áp dụng chat AI {ai_adoption_rate:.1%} chấp nhận được - cần tăng lên mục tiêu 49%"))
        else:
            insights.append(("negative", f"Việc áp dụng chat AI thấp {ai_adoption_rate:.1%} - dưới ngưỡng 20%, cần quảng bá mạnh"))
        
        return insights
    
    def _analyze_popup_performance(self, data, language='en'):
        """Analyze popup effectiveness and user interaction using industry benchmarks."""
        insights = []
        
        popups_shown = data.get('show_popup', 0)
        detail_views = data.get('view_detail_popup', 0)
        popups_closed = data.get('close_popup', 0)
        
        if popups_shown > 0:
            conversion_rate = detail_views / popups_shown
            close_rate = popups_closed / popups_shown
            
            # Popup CTR analysis (benchmarks: 15% good, 5% minimum)
            if conversion_rate >= self.benchmarks['popup_conversion_good']:
                insights.append(("positive", f"Tỷ lệ chuyển đổi popup xuất sắc {conversion_rate:.1%} - vượt chuẩn 15%"))
            elif conversion_rate >= self.benchmarks['popup_conversion_minimum']:
                insights.append(("neutral", f"Tỷ lệ chuyển đổi popup {conversion_rate:.1%} chấp nhận được - cần cải thiện lên 15%"))
            else:
                insights.append(("negative", f"Tỷ lệ chuyển đổi popup thấp {conversion_rate:.1%} - dưới ngưỡng 5%, cần đổi nội dung"))
            
            if close_rate > 0.8:
                insights.append(("negative", f"Tỷ lệ đóng popup cao {close_rate:.1%} - người dùng thấy xâm phạm, giảm tần suất"))
            
        return insights
    
    def _generate_recommendations(self, data, kpis, language='en'):
        """Generate actionable recommendations based on data analysis."""
        recommendations = []
        
        # Retention recommendations (benchmark: 12% Day 7 retention)
        if kpis.get('retention_rate', 0) < self.benchmarks['retention_rate_good']:
            recommendations.append("Cải thiện trải nghiệm tuần đầu - người dùng hoạt động hàng ngày trong tuần 1 có khả năng ở lại cao hơn 80%")
            recommendations.append("Thêm tính năng social (+30% retention boost) - leaderboards, challenges, chia sẻ tiến độ")
            recommendations.append("Cá nhân hóa roadmap luyện tập dựa trên health survey và mục tiêu cá nhân")
        
        # Engagement time recommendations (benchmark: 450s/7.5 phút)
        avg_engage_time = data.get('avg_engage_time', 0)
        if avg_engage_time < self.benchmarks['engagement_time_good']:
            recommendations.append("Tăng thời gian tương tác lên 7.5 phút bằng workout dài hơn và progress tracking")
            recommendations.append("Thêm gamification (streaks, badges, challenges) để tăng tần suất luyện tập")
        
        # Engagement rate recommendations (benchmark: 25% DAU/MAU)
        if kpis.get('engagement_rate', 0) < self.benchmarks['engagement_rate_good']:
            recommendations.append("Gửi thông báo đẩy nhắc luyện tập vào thời điểm tối ưu (buổi sáng <5 phút, buổi tối ~12 phút)")
            recommendations.append("Tạo flexible weekly goals thay vì daily (Down Dog app: +20% retention ở 90 ngày)")
        
        # Feature usage recommendations
        roadmap_usage = data.get('view_roadmap', 0) / data.get('session_start', 1)
        if roadmap_usage < 0.2:
            recommendations.append("Làm nổi bật tính năng lộ trình trong hướng dẫn ứng dụng và menu chính")
        
        # AI adoption recommendations (benchmark: 49% daily usage)
        ai_usage = data.get('chat_ai', 0) / data.get('session_start', 1)
        if ai_usage < self.benchmarks['ai_adoption_target']:
            recommendations.append(f"Tăng AI adoption từ {ai_usage:.1%} lên 49% - quảng bá AI coaching với use cases cụ thể")
        
        # Popup recommendations (benchmark: 15% CTR good, 5% minimum)
        popup_conversion = data.get('view_detail_popup', 0) / max(data.get('show_popup', 1), 1)
        if popup_conversion < self.benchmarks['popup_conversion_minimum']:
            recommendations.append("Popup CTR rất thấp (<5%) - cần redesign hoàn toàn nội dung và timing")
        elif popup_conversion < self.benchmarks['popup_conversion_good']:
            recommendations.append("Kiểm tra A/B thời gian và nội dung popup để đạt 15% CTR")
            recommendations.append("Giảm tần suất popup để tránh mệt mỏi người dùng")
        
        return recommendations
    
    def _identify_opportunities(self, data, kpis, language='en'):
        """Identify growth opportunities and optimization areas based on industry benchmarks."""
        opportunities = []
        
        # High engagement, low retention opportunity
        engagement_rate = kpis.get('engagement_rate', 0)
        retention_rate = kpis.get('retention_rate', 0)
        if engagement_rate >= self.benchmarks['engagement_rate_minimum'] and retention_rate < self.benchmarks['retention_rate_good']:
            opportunities.append("Tương tác tốt nhưng giữ chân thấp - triển khai habit-forming features (streaks, social, flexible goals)")
        
        # AI adoption opportunity (benchmark: 49% daily usage)
        practice_video = data.get('practice_with_video', 0)
        practice_ai = data.get('practice_with_ai', 0)
        ai_chat = data.get('chat_ai', 0)
        total_sessions = data.get('session_start', 1)
        
        if practice_video > practice_ai * 3:
            opportunities.append("Người dùng video chiếm ưu thế - cross-promote AI coaching để đạt 49% adoption")
        
        if (ai_chat / total_sessions) < self.benchmarks['ai_adoption_minimum']:
            opportunities.append("AI adoption <20% - cơ hội lớn để giáo dục người dùng về AI coaching (benchmark: 49% năm 2025)")
        
        # Practice completion opportunity (benchmark: 70%+ boosts LTV by 43%)
        if practice_video + practice_ai > 0:
            view_exercise = data.get('view_exercise', 0)
            practice_completion_rate = (practice_video + practice_ai) / max(view_exercise, 1)
            if practice_completion_rate < self.benchmarks['practice_completion_good']:
                opportunities.append(f"Tỷ lệ hoàn thành luyện tập {practice_completion_rate:.1%} - tăng lên 70%+ có thể boost LTV 43%")
        
        # Content browsing vs practice gap
        exercise_views = data.get('view_exercise', 0)
        practice_sessions = practice_video + practice_ai
        if exercise_views > practice_sessions * 2:
            opportunities.append("Người dùng duyệt nhiều hơn thực hành - giảm friction để bắt đầu workout")
        
        # Health tracking expansion opportunity
        health_surveys = data.get('health_survey', 0)
        if health_surveys / total_sessions > 0.6:
            opportunities.append("Tương tác health survey cao (>60%) - mở rộng progress tracking và visualization")
        
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
