import numpy as np
from datetime import datetime

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
    
    def generate_insights(self, data, kpis):
        """Generate comprehensive insights from the analytics data."""
        insights = {
            'key_insights': [],
            'recommendations': [],
            'alerts': [],
            'opportunities': []
        }
        
        # Analyze retention
        insights['key_insights'].extend(self._analyze_retention(kpis))
        
        # Analyze engagement
        insights['key_insights'].extend(self._analyze_engagement(data, kpis))
        
        # Analyze feature usage
        insights['key_insights'].extend(self._analyze_feature_usage(data))
        
        # Analyze popup performance
        insights['key_insights'].extend(self._analyze_popup_performance(data))
        
        # Generate recommendations
        insights['recommendations'].extend(self._generate_recommendations(data, kpis))
        
        # Identify opportunities
        insights['opportunities'].extend(self._identify_opportunities(data, kpis))
        
        return insights
    
    def _analyze_retention(self, kpis):
        """Analyze user retention metrics."""
        insights = []
        retention_rate = kpis.get('retention_rate', 0)
        churn_rate = kpis.get('churn_rate', 0)
        
        if retention_rate > self.benchmarks['retention_rate_good']:
            insights.append(f"Excellent user retention at {retention_rate:.1%} - significantly above industry average")
        elif retention_rate > 0.15:
            insights.append(f"Moderate retention rate of {retention_rate:.1%} - room for improvement")
        else:
            insights.append(f"Low retention rate of {retention_rate:.1%} - immediate attention needed")
        
        if churn_rate > self.benchmarks['churn_rate_warning']:
            insights.append(f"High churn rate of {churn_rate:.1%} detected - users are leaving at concerning rate")
        else:
            insights.append(f"Churn rate of {churn_rate:.1%} is within acceptable range")
        
        return insights
    
    def _analyze_engagement(self, data, kpis):
        """Analyze user engagement patterns."""
        insights = []
        engagement_rate = kpis.get('engagement_rate', 0)
        
        practice_video = data.get('practice_with_video', 0)
        practice_ai = data.get('practice_with_ai', 0)
        total_practice = practice_video + practice_ai
        
        if engagement_rate > self.benchmarks['engagement_rate_good']:
            insights.append(f"Strong engagement rate of {engagement_rate:.1%} - users are actively practicing")
        else:
            insights.append(f"Engagement rate of {engagement_rate:.1%} below target - need to boost practice sessions")
        
        # Analyze practice preferences
        if total_practice > 0:
            video_preference = practice_video / total_practice
            if video_preference > 0.7:
                insights.append("Users strongly prefer video-guided practice sessions over AI assistance")
            elif video_preference < 0.3:
                insights.append("Users are embracing AI-guided practice sessions over traditional videos")
            else:
                insights.append("Balanced usage between video and AI practice sessions")
        
        return insights
    
    def _analyze_feature_usage(self, data):
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
            insights.append("Exercise content is highly popular - users are actively exploring workouts")
        elif exercise_views / total_sessions < 0.3:
            insights.append("Low exercise content engagement - content discovery needs improvement")
        
        # Roadmap feature analysis
        if roadmap_views / total_sessions < 0.2:
            insights.append("Roadmap feature is underutilized - users may not understand its value")
        
        # Health survey completion
        if health_surveys / total_sessions > 0.7:
            insights.append("High health survey completion rate - users are engaged with wellness tracking")
        
        # AI chat adoption
        ai_adoption_rate = ai_chat / total_sessions
        if ai_adoption_rate < self.benchmarks['ai_adoption_target']:
            insights.append(f"AI chat adoption at {ai_adoption_rate:.1%} is below target - promote AI features")
        
        return insights
    
    def _analyze_popup_performance(self, data):
        """Analyze popup effectiveness and user interaction."""
        insights = []
        
        popups_shown = data.get('show_popup', 0)
        detail_views = data.get('view_detail_popup', 0)
        popups_closed = data.get('close_popup', 0)
        
        if popups_shown > 0:
            conversion_rate = detail_views / popups_shown
            close_rate = popups_closed / popups_shown
            
            if conversion_rate > self.benchmarks['popup_conversion_good']:
                insights.append(f"Popup conversion rate of {conversion_rate:.1%} is excellent - content is relevant")
            else:
                insights.append(f"Popup conversion rate of {conversion_rate:.1%} needs improvement - review content relevance")
            
            if close_rate > 0.8:
                insights.append("High popup close rate suggests users find them intrusive or irrelevant")
            
        return insights
    
    def _generate_recommendations(self, data, kpis):
        """Generate actionable recommendations based on data analysis."""
        recommendations = []
        
        # Retention recommendations
        if kpis.get('retention_rate', 0) < self.benchmarks['retention_rate_good']:
            recommendations.append("Implement onboarding flow improvements to boost user retention")
            recommendations.append("Create personalized practice recommendations for new users")
        
        # Engagement recommendations
        if kpis.get('engagement_rate', 0) < self.benchmarks['engagement_rate_good']:
            recommendations.append("Add gamification elements to increase practice session frequency")
            recommendations.append("Send push notifications for practice reminders and streaks")
        
        # Feature usage recommendations
        roadmap_usage = data.get('view_roadmap', 0) / data.get('session_start', 1)
        if roadmap_usage < 0.2:
            recommendations.append("Highlight roadmap feature in app tour and main navigation")
        
        ai_usage = data.get('chat_ai', 0) / data.get('session_start', 1)
        if ai_usage < 0.25:
            recommendations.append("Promote AI chat feature with guided tutorials and use cases")
        
        # Popup recommendations
        popup_conversion = data.get('view_detail_popup', 0) / max(data.get('show_popup', 1), 1)
        if popup_conversion < 0.15:
            recommendations.append("A/B test popup timing and content to improve engagement")
            recommendations.append("Reduce popup frequency to avoid user fatigue")
        
        return recommendations
    
    def _identify_opportunities(self, data, kpis):
        """Identify growth opportunities and optimization areas."""
        opportunities = []
        
        # High engagement, low retention opportunity
        if kpis.get('engagement_rate', 0) > 0.4 and kpis.get('retention_rate', 0) < 0.3:
            opportunities.append("High engagement but low retention - focus on habit formation features")
        
        # AI adoption opportunity
        practice_video = data.get('practice_with_video', 0)
        practice_ai = data.get('practice_with_ai', 0)
        if practice_video > practice_ai * 3:
            opportunities.append("Video users could benefit from AI personalization - cross-promote features")
        
        # Content expansion opportunity
        exercise_views = data.get('view_exercise', 0)
        practice_sessions = practice_video + practice_ai
        if exercise_views > practice_sessions * 2:
            opportunities.append("Users browse more than they practice - simplify practice initiation")
        
        # Health tracking opportunity
        health_surveys = data.get('health_survey', 0)
        total_users = kpis.get('total_new_users', 0) + kpis.get('total_app_opens', 0)
        if health_surveys / max(total_users, 1) > 0.6:
            opportunities.append("High health survey engagement - expand wellness tracking features")
        
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
