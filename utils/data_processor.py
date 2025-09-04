import pandas as pd
import numpy as np
from datetime import datetime
import json

class DataProcessor:
    """Handles data processing, validation, and KPI calculations for yoga app analytics."""
    
    def __init__(self):
        self.required_fields = [
            'time', 'first_open', 'app_remove', 'session_start', 'app_open',
            'login', 'view_exercise', 'health_survey', 'view_roadmap',
            'practice_with_video', 'practice_with_ai', 'chat_ai',
            'show_popup', 'view_detail_popup', 'close_popup'
        ]
    
    def validate_data(self, data):
        """Validate that the webhook data contains all required fields."""
        if not isinstance(data, dict):
            return False
        
        missing_fields = [field for field in self.required_fields if field not in data]
        if missing_fields:
            return False
        
        # Check if numeric fields are actually numeric
        numeric_fields = [field for field in self.required_fields if field != 'time']
        for field in numeric_fields:
            try:
                float(data[field])
            except (ValueError, TypeError):
                return False
        
        return True
    
    def process_data(self, data):
        """Process raw webhook data into structured format."""
        processed = {}
        
        # Parse time period
        time_str = data.get('time', '')
        processed['time_period'] = time_str
        
        # Convert all numeric fields
        for field in self.required_fields:
            if field != 'time':
                processed[field] = float(data.get(field, 0))
        
        return processed
    
    def calculate_kpis(self, data):
        """Calculate key performance indicators from the data."""
        kpis = {}
        
        # Basic metrics
        kpis['total_new_users'] = int(data.get('first_open', 0))
        kpis['active_sessions'] = int(data.get('session_start', 0))
        kpis['total_app_opens'] = int(data.get('app_open', 0))
        kpis['app_removals'] = int(data.get('app_remove', 0))
        
        # Calculated metrics
        total_users = kpis['total_new_users'] + kpis['total_app_opens']
        
        # Retention Rate: (returning users / total new users) * 100
        if kpis['total_new_users'] > 0:
            kpis['retention_rate'] = kpis['total_app_opens'] / kpis['total_new_users']
        else:
            kpis['retention_rate'] = 0
        
        # Churn Rate: (app removals / total users) * 100
        if total_users > 0:
            kpis['churn_rate'] = kpis['app_removals'] / total_users
        else:
            kpis['churn_rate'] = 0
        
        # Engagement Rate: (practice sessions / total app opens) * 100
        practice_sessions = data.get('practice_with_video', 0) + data.get('practice_with_ai', 0)
        total_opens = kpis['total_new_users'] + kpis['total_app_opens']
        
        if total_opens > 0:
            kpis['engagement_rate'] = practice_sessions / total_opens
        else:
            kpis['engagement_rate'] = 0
        
        # Additional metrics
        kpis['total_logins'] = int(data.get('login', 0))
        kpis['practice_sessions'] = int(practice_sessions)
        kpis['ai_interactions'] = int(data.get('chat_ai', 0))
        
        return kpis
    
    def calculate_popup_metrics(self, data):
        """Calculate popup performance metrics."""
        metrics = {}
        
        metrics['total_shown'] = int(data.get('show_popup', 0))
        metrics['detail_views'] = int(data.get('view_detail_popup', 0))
        metrics['total_closed'] = int(data.get('close_popup', 0))
        
        # Conversion rate: (detail views / total shown) * 100
        if metrics['total_shown'] > 0:
            metrics['conversion_rate'] = metrics['detail_views'] / metrics['total_shown']
        else:
            metrics['conversion_rate'] = 0
        
        # Close rate: (total closed / total shown) * 100
        if metrics['total_shown'] > 0:
            metrics['close_rate'] = metrics['total_closed'] / metrics['total_shown']
        else:
            metrics['close_rate'] = 0
        
        return metrics
    
    def calculate_feature_adoption(self, data):
        """Calculate feature adoption metrics."""
        features = {
            'Exercise Views': data.get('view_exercise', 0),
            'Health Survey': data.get('health_survey', 0),
            'Roadmap Views': data.get('view_roadmap', 0),
            'Video Practice': data.get('practice_with_video', 0),
            'AI Practice': data.get('practice_with_ai', 0),
            'AI Chat': data.get('chat_ai', 0),
            'Login Events': data.get('login', 0)
        }
        
        # Sort features by usage
        sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)
        
        adoption_data = {
            'most_used': sorted_features[:3],
            'least_used': sorted_features[-3:],
            'growing': [],  # Would need historical data for actual growth calculation
            'total_features': len(features),
            'average_usage': np.mean(list(features.values()))
        }
        
        # Simulate growth data (in real scenario, would compare with historical data)
        for feature, usage in sorted_features:
            if usage > adoption_data['average_usage']:
                growth_rate = (usage - adoption_data['average_usage']) / adoption_data['average_usage']
                adoption_data['growing'].append((feature, growth_rate))
        
        return adoption_data
    
    def export_to_csv(self, data):
        """Export data to CSV format."""
        df = pd.DataFrame([data])
        return df.to_csv(index=False)
    
    def get_user_journey_data(self, data):
        """Calculate user journey flow data."""
        journey = {
            'first_open': data.get('first_open', 0),
            'login': data.get('login', 0),
            'view_exercise': data.get('view_exercise', 0),
            'practice_sessions': data.get('practice_with_video', 0) + data.get('practice_with_ai', 0),
            'ai_interactions': data.get('chat_ai', 0),
            'app_remove': data.get('app_remove', 0)
        }
        
        return journey
