import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import re

class DataProcessor:
    """Handles data processing, validation, and KPI calculations for yoga app analytics.
    
    Field Descriptions (all metrics use unit 'person' except avg_engage_time):
    - first_open: New user opens app for the first time
    - app_remove: User uninstalls app
    - session_start: A session starts
    - app_open: User opens app again (returning user)
    - login: User logs in
    - view_exercise: User views the yoga exercise on the app
    - health_survey: User finishes the app health survey
    - view_roadmap: User views the app's recommended exercise roadmap
    - practice_with_video: User practices with app's exercise video
    - practice_with_ai: User practices using AI feature
    - chat_ai: User chats with the AI in app
    - show_popup: Popup shows to user
    - view_detail_popup: User clicks on popup
    - close_popup: User closes popup without clicking it
    - store_subscription: User views package in the store
    - in_app_purchase: User placing order (not real order yet)
    - avg_engage_time: Average engagement time per user (in seconds)
    """
    
    def __init__(self):
        self.required_fields = [
            'time', 'first_open', 'app_remove', 'session_start', 'app_open',
            'login', 'view_exercise', 'health_survey', 'view_roadmap',
            'practice_with_video', 'practice_with_ai', 'chat_ai',
            'show_popup', 'view_detail_popup', 'close_popup'
        ]
        
        # Additional optional fields
        self.optional_fields = [
            'store_subscription', 'in_app_purchase', 'avg_engage_time'
        ]
        
        # Field normalization mapping
        self.field_mapping = {
            'in_app_purchasse': 'in_app_purchase',  # Fix typo in field name
            'buy_package': 'in_app_purchase',       # Alternative field name
            'AvgEngagementTime': 'avg_engage_time',  # Normalize field name
            'avgEngagementTime': 'avg_engage_time',  # Alternative format
        }
    
    def convert_date_format(self, date_str):
        """Convert date from YYYYmmdd format to dd/mm/YYYY format.
        
        Args:
            date_str: Date string in YYYYmmdd format
            
        Returns:
            Date string in dd/mm/YYYY format
        """
        if not date_str or not isinstance(date_str, str):
            return date_str
        
        # Check if it's already in dd/mm/YYYY format
        if re.match(r'\d{2}/\d{2}/\d{4}', date_str):
            return date_str
        
        # Check if it's in YYYYmmdd format (8 digits)
        if re.match(r'^\d{8}$', date_str):
            try:
                # Parse YYYYmmdd format
                year = date_str[:4]
                month = date_str[4:6]
                day = date_str[6:8]
                
                # Convert to dd/mm/YYYY format
                return f"{day}/{month}/{year}"
            except (ValueError, IndexError):
                return date_str
        
        # If it doesn't match either format, return as-is
        return date_str
    
    def format_engagement_time(self, seconds):
        """Format engagement time from seconds to readable format.
        
        Args:
            seconds: Engagement time in seconds
            
        Returns:
            Formatted string like "5m 30s" or "1h 20m"
        """
        if not seconds or seconds == 0:
            return "0s"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 and hours == 0:  # Only show seconds if less than an hour
            parts.append(f"{secs}s")
        
        return " ".join(parts) if parts else "0s"
    
    def aggregate_to_weekly(self, daily_data):
        """Aggregate daily data into weekly periods (7-day periods).
        
        Args:
            daily_data: List of daily data records
            
        Returns:
            List of weekly aggregated data
        """
        if not daily_data:
            return []
        
        weekly_data = []
        current_week = []
        week_start = None
        
        for i, day_record in enumerate(daily_data):
            if len(current_week) == 0:
                week_start = day_record.get('time', '')
            
            current_week.append(day_record)
            
            # When we have 7 days or it's the last record
            if len(current_week) == 7 or i == len(daily_data) - 1:
                # Aggregate the week
                aggregated = {}
                week_end = current_week[-1].get('time', '')
                aggregated['time'] = f"{week_start} - {week_end}"
                
                # Sum numeric fields, average avg_engage_time
                for field in self.required_fields + self.optional_fields:
                    if field == 'time':
                        continue
                    elif field == 'avg_engage_time':
                        # Average engagement time across the week
                        values = [item.get(field, 0) for item in current_week if item.get(field, 0) > 0]
                        aggregated[field] = sum(values) / len(values) if values else 0
                    else:
                        # Sum all other numeric fields
                        aggregated[field] = sum(item.get(field, 0) for item in current_week)
                
                weekly_data.append(aggregated)
                current_week = []
        
        return weekly_data
    
    def get_last_n_days(self, data_list, n=7):
        """Get the last N days of data from the data list.
        
        Args:
            data_list: List of data records
            n: Number of days to retrieve (default 7)
            
        Returns:
            List of last N days data
        """
        if not data_list or len(data_list) == 0:
            return []
        
        # Return the last n records (or all if less than n)
        return data_list[-n:] if len(data_list) >= n else data_list
    
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
    
    def process_webhook_data(self, raw_data):
        """Process webhook data in new country-based format or legacy formats."""
        try:
            # Check if data is country-based array format
            if isinstance(raw_data, list) and len(raw_data) > 0:
                # Check if this is the new country-based format
                first_item = raw_data[0]
                if isinstance(first_item, dict) and 'country' in first_item and 'data' in first_item:
                    return self._process_country_data(raw_data)
                else:
                    # Legacy time-series array format
                    return self._process_legacy_array(raw_data)
            
            # Check if data is a single object (original format)
            elif isinstance(raw_data, dict):
                return self._process_single_object(raw_data)
            
            return None
            
        except Exception:
            return None
    
    def _aggregate_time_series_data(self, data_list):
        """Aggregate time series data for overall metrics."""
        if not data_list:
            return {}
        
        aggregated = {}
        
        # Sum all numeric fields across time periods
        for field in self.required_fields + self.optional_fields:
            if field == 'time':
                # Combine time periods
                first_time = data_list[0].get('time', '')
                last_time = data_list[-1].get('time', '')
                aggregated['time'] = f"Total: {first_time.split(' - ')[0]} - {last_time.split(' - ')[-1]}"
            elif field == 'avg_engage_time':
                # Average engagement time across all periods
                values = [item.get(field, 0) for item in data_list if item.get(field, 0) > 0]
                aggregated[field] = sum(values) / len(values) if values else 0
            else:
                # Sum numeric values
                total = sum(item.get(field, 0) for item in data_list)
                aggregated[field] = total
        
        return aggregated
    
    def calculate_day_over_day_kpis(self, data_list):
        """Calculate KPIs comparing the two most recent days."""
        if not data_list or len(data_list) < 2:
            # If less than 2 days, return current day only
            current_day = data_list[-1] if data_list else {}
            return {
                'current': self.calculate_kpis(current_day),
                'previous': {},
                'deltas': {}
            }
        
        # Get the two most recent days
        current_day = data_list[-1]
        previous_day = data_list[-2]
        
        # Calculate KPIs for both days
        current_kpis = self.calculate_kpis(current_day)
        previous_kpis = self.calculate_kpis(previous_day)
        
        # Calculate percentage changes
        deltas = {}
        for key in current_kpis:
            if key in previous_kpis and previous_kpis[key] > 0:
                change = (current_kpis[key] - previous_kpis[key]) / previous_kpis[key]
                deltas[key] = change
            else:
                deltas[key] = 0
        
        return {
            'current': current_kpis,
            'previous': previous_kpis,
            'deltas': deltas
        }
    
    def calculate_week_over_week_kpis(self, data_list):
        """Calculate KPIs comparing the two most recent weeks."""
        if not data_list or len(data_list) < 2:
            # If less than 2 weeks, return current week only
            current_week = data_list[-1] if data_list else {}
            return {
                'current': self.calculate_kpis(current_week),
                'previous': {},
                'deltas': {}
            }
        
        # Get the two most recent weeks
        current_week = data_list[-1]
        previous_week = data_list[-2]
        
        # Calculate KPIs for both weeks
        current_kpis = self.calculate_kpis(current_week)
        previous_kpis = self.calculate_kpis(previous_week)
        
        # Calculate percentage changes
        deltas = {}
        for key in current_kpis:
            if key in previous_kpis and previous_kpis[key] > 0:
                change = (current_kpis[key] - previous_kpis[key]) / previous_kpis[key]
                deltas[key] = change
            else:
                deltas[key] = 0
        
        return {
            'current': current_kpis,
            'previous': previous_kpis,
            'deltas': deltas
        }
    
    def process_data(self, data):
        """Process raw webhook data into structured format."""
        processed = {}
        
        # Parse time period
        time_str = data.get('time', '')
        processed['time_period'] = time_str
        
        # Convert all numeric fields
        for field in self.required_fields + self.optional_fields:
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
        kpis['avg_engagement_time'] = data.get('avg_engage_time', 0)
        
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
    
    def _process_country_data(self, country_array):
        """Process new country-based data format."""
        countries_data = {}
        all_time_periods = {}  # For aggregating across countries
        
        for country_obj in country_array:
            country = country_obj.get('country', 'Unknown')
            country_data = country_obj.get('data', [])
            
            # Normalize and validate each time period data
            normalized_data = []
            for item in country_data:
                normalized_item = self._normalize_fields(item)
                if self._validate_data_relaxed(normalized_item):
                    normalized_data.append(normalized_item)
            
            if normalized_data:
                # Store individual country data
                countries_data[country] = {
                    'is_time_series': True,
                    'time_periods': len(normalized_data),
                    'data': normalized_data,
                    'latest_period': normalized_data[-1],
                    'aggregated': self._aggregate_time_series_data(normalized_data)
                }
                
                # Collect data for aggregation across countries
                for item in normalized_data:
                    time_key = item.get('time', 'Unknown')
                    if time_key not in all_time_periods:
                        all_time_periods[time_key] = item.copy()
                    else:
                        # Sum numeric fields across countries for same time period
                        for field, value in item.items():
                            if field != 'time' and isinstance(value, (int, float)):
                                if field == 'avg_engage_time':
                                    # For average engagement time, we need to average properly
                                    # Store count to calculate weighted average
                                    count_key = f'{field}_count'
                                    if count_key not in all_time_periods[time_key]:
                                        all_time_periods[time_key][count_key] = 1
                                    all_time_periods[time_key][count_key] += 1
                                    all_time_periods[time_key][field] = (
                                        (all_time_periods[time_key].get(field, 0) * (all_time_periods[time_key][count_key] - 1) + value) 
                                        / all_time_periods[time_key][count_key]
                                    )
                                else:
                                    all_time_periods[time_key][field] = all_time_periods[time_key].get(field, 0) + value
        
        # Create "All Countries" aggregated data
        if all_time_periods:
            aggregated_periods = list(all_time_periods.values())
            # Clean up count fields used for averaging
            for period in aggregated_periods:
                keys_to_remove = [k for k in period.keys() if k.endswith('_count')]
                for k in keys_to_remove:
                    del period[k]
            
            countries_data['All Countries'] = {
                'is_time_series': True,
                'time_periods': len(aggregated_periods),
                'data': aggregated_periods,
                'latest_period': aggregated_periods[-1] if aggregated_periods else {},
                'aggregated': self._aggregate_time_series_data(aggregated_periods)
            }
        
        return countries_data
    
    def _process_legacy_array(self, data_array):
        """Process legacy time-series array format."""
        valid_data = []
        for item in data_array:
            if self.validate_data(item):
                valid_data.append(item)
        
        if not valid_data:
            return None
        
        return {
            'is_time_series': True,
            'time_periods': len(valid_data),
            'data': valid_data,
            'latest_period': valid_data[-1],
            'aggregated': self._aggregate_time_series_data(valid_data)
        }
    
    def _process_single_object(self, data_obj):
        """Process single object format."""
        if self.validate_data(data_obj):
            return {
                'is_time_series': False,
                'time_periods': 1,
                'data': [data_obj],
                'latest_period': data_obj,
                'aggregated': data_obj
            }
        return None
    
    def _normalize_fields(self, data):
        """Normalize field names across different data sources."""
        normalized = {}
        for key, value in data.items():
            # Apply field mapping
            new_key = self.field_mapping.get(key, key)
            
            # Convert date format for time field
            if new_key == 'time' and isinstance(value, str):
                normalized[new_key] = self.convert_date_format(value)
            else:
                normalized[new_key] = value
        return normalized
    
    def _validate_data_relaxed(self, data):
        """Relaxed validation that allows for additional fields in new format."""
        if not isinstance(data, dict):
            return False
        
        # Check if we have the essential fields (time is required)
        if 'time' not in data:
            return False
        
        # Check if we have at least some core numeric fields
        core_fields = ['first_open', 'session_start', 'app_open']
        has_core = any(field in data for field in core_fields)
        
        if not has_core:
            return False
        
        # Validate numeric fields that are present
        for field, value in data.items():
            if field != 'time' and field != 'row_number':  # Skip non-numeric fields
                try:
                    float(value)
                except (ValueError, TypeError):
                    # If it's not numeric but it's not a required field, it's okay
                    if field in self.required_fields:
                        return False
        
        return True
