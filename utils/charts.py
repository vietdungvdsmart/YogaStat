import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from .translations import get_text

class ChartGenerator:
    """Generates interactive charts for the yoga app analytics dashboard.
    
    Field Descriptions (for hover templates and labels):
    - first_open: New user opens app for the first time (unit: person/persons)
    - app_remove: User uninstalls app (unit: person/persons)
    - session_start: A session starts (unit: person/persons)
    - app_open: User opens app again (unit: person/persons)
    - login: User logs in (unit: person/persons)
    - view_exercise: User views yoga exercise (unit: person/persons)
    - health_survey: User finishes health survey (unit: person/persons)
    - view_roadmap: User views recommended roadmap (unit: person/persons)
    - practice_with_video: User practices with video (unit: person/persons)
    - practice_with_ai: User practices with AI (unit: person/persons)
    - chat_ai: User chats with AI (unit: person/persons)
    - show_popup: Popup shows to user (unit: person/persons)
    - view_detail_popup: User clicks on popup (unit: person/persons)
    - close_popup: User closes popup without clicking (unit: person/persons)
    - store_subscription: User views store package (unit: person/persons)
    - in_app_purchase: User places order (unit: person/persons)
    - avg_engage_time: Average engagement time per user (unit: seconds)
    """
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#4FD1C7',
            'secondary': '#B19CD9',
            'accent': '#87A96B',
            'success': '#48BB78',
            'warning': '#ED8936',
            'error': '#F56565',
            'text': '#2D3748'
        }
    
    def get_time_granularity(self, time_series_data):
        """Determine if data should be displayed as daily or weekly.
        
        Returns:
            tuple: (is_daily: bool, x_axis_label: str, period_count: int)
        """
        if not time_series_data:
            return (True, 'Day', 0)
        
        period_count = len(time_series_data)
        
        # If 14 or fewer periods, assume daily and show as daily
        # If more than 14 periods, aggregate to weekly
        is_daily = period_count <= 14
        x_axis_label = 'Day' if is_daily else 'Week'
        
        return (is_daily, x_axis_label, period_count)
    
    def get_y_axis_label(self, metric_type='count', language='en'):
        """Get appropriate y-axis label based on metric type.
        
        Args:
            metric_type: Type of metric ('count', 'time', 'percentage')
            language: Language code
        
        Returns:
            str: Y-axis label
        """
        if metric_type == 'count':
            return get_text('persons', language)
        elif metric_type == 'time':
            return 'Time (seconds)'
        elif metric_type == 'percentage':
            return 'Percentage (%)'
        else:
            return get_text('persons', language)
    
    def create_feature_adoption_funnel(self, data, language='en'):
        """Create a funnel chart showing feature adoption progression."""
        # Calculate funnel stages - from viewing to practicing
        stages = [
            (get_text('view_exercise_stage', language), data.get('view_exercise', 0)),
            (get_text('practice_video_stage', language), data.get('practice_with_video', 0)),
            (get_text('practice_ai_stage', language), data.get('practice_with_ai', 0)),
            (get_text('chat_ai_stage', language), data.get('chat_ai', 0))
        ]
        
        # Create funnel visualization
        fig = go.Figure(go.Funnel(
            y=[stage[0] for stage in stages],
            x=[stage[1] for stage in stages],
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.85,
            marker={
                "color": [self.color_scheme['primary'], 
                         self.color_scheme['secondary'],
                         self.color_scheme['accent'],
                         self.color_scheme['success']],
                "line": {"width": 2, "color": "white"}
            },
            connector={"line": {"color": "rgb(63, 63, 63)", "width": 1}},
            hovertemplate='<b>%{y}</b><br>' +
                         get_text('users_count', language) + ': %{x}<br>' +
                         get_text('conversion_from_start', language) + ': %{percentInitial}<br>' +
                         '<extra></extra>'
        ))
        
        fig.update_layout(
            title=get_text('feature_adoption_funnel_title', language),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_engagement_score_radar(self, data, language='en'):
        """Create a radar chart showing multi-dimensional engagement scores."""
        # Calculate engagement scores (normalized to 0-100)
        total_sessions = max(data.get('session_start', 1), 1)  # Avoid division by zero
        
        categories = [
            get_text('login_engagement', language),
            get_text('health_awareness', language),
            get_text('content_exploration', language),
            get_text('ai_interaction', language),
            get_text('popup_responsiveness', language),
            get_text('retention_strength', language)
        ]
        
        # Calculate scores based on ratios
        scores = [
            min((data.get('login', 0) / total_sessions) * 100, 100),  # Login rate
            min((data.get('health_survey', 0) / total_sessions) * 100, 100),  # Health survey completion
            min(((data.get('view_exercise', 0) + data.get('view_roadmap', 0)) / (total_sessions * 2)) * 100, 100),  # Content exploration
            min(((data.get('chat_ai', 0) + data.get('practice_with_ai', 0)) / (total_sessions * 2)) * 100, 100),  # AI interaction
            min((data.get('view_detail_popup', 0) / max(data.get('show_popup', 1), 1)) * 100, 100),  # Popup engagement
            min(((data.get('app_open', 0) - data.get('app_remove', 0)) / max(data.get('first_open', 1), 1)) * 100, 100)  # Retention
        ]
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name=get_text('engagement_score', language),
            fillcolor='rgba(79, 209, 199, 0.3)',
            line=dict(color=self.color_scheme['primary'], width=2),
            marker=dict(size=8, color=self.color_scheme['primary']),
            hovertemplate='<b>%{theta}</b><br>Score: %{r:.1f}/100<extra></extra>'
        ))
        
        # Add reference line (average expectation at 50%)
        fig.add_trace(go.Scatterpolar(
            r=[50] * len(categories),
            theta=categories,
            fill=None,
            name=get_text('average_benchmark', language),
            line=dict(color='gray', width=1, dash='dash'),
            showlegend=True,
            hoverinfo='skip'
        ))
        
        fig.update_layout(
            title=get_text('engagement_score_radar_title', language),
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickmode='array',
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['0', '25', '50', '75', '100']
                )
            ),
            showlegend=True,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_feature_usage_chart(self, data, language='en'):
        """Create a horizontal bar chart for feature usage."""
        features = {
            'Exercise Views': data.get('view_exercise', 0),
            'Health Survey': data.get('health_survey', 0),
            'Roadmap Views': data.get('view_roadmap', 0),
            'Login Events': data.get('login', 0)
        }
        
        sorted_features = sorted(features.items(), key=lambda x: x[1])
        feature_names = [item[0] for item in sorted_features]
        feature_values = [item[1] for item in sorted_features]
        
        fig = go.Figure(data=[
            go.Bar(
                y=feature_names,
                x=feature_values,
                orientation='h',
                marker_color=self.color_scheme['accent'],
                text=feature_values,
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Usage: %{x}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Feature Usage Distribution",
            xaxis_title=get_text('count', language),
            yaxis_title="Features",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_ai_engagement_chart(self, data, language='en'):
        """Create a gauge chart for AI engagement."""
        ai_practice = data.get('practice_with_ai', 0)
        ai_chat = data.get('chat_ai', 0)
        total_ai = ai_practice + ai_chat
        total_sessions = data.get('session_start', 1)  # Avoid division by zero
        
        ai_engagement_rate = (total_ai / total_sessions) * 100 if total_sessions > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = ai_engagement_rate,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': get_text('ai_engagement_title', language) + " (%)"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': self.color_scheme['secondary']},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "gray"},
                    {'range': [50, 75], 'color': self.color_scheme['primary']},
                    {'range': [75, 100], 'color': self.color_scheme['success']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_popup_performance_chart(self, data, language='en'):
        """Create a funnel chart for popup performance."""
        stages = [get_text('popups_shown', language), get_text('popups_viewed', language), 'Popups Closed']
        values = [
            data.get('show_popup', 0),
            data.get('view_detail_popup', 0),
            data.get('close_popup', 0)
        ]
        
        fig = go.Figure(go.Funnel(
            y = stages,
            x = values,
            textposition = "inside",
            textinfo = "value+percent initial",
            marker = {"color": [self.color_scheme['primary'], self.color_scheme['success'], self.color_scheme['warning']]},
            connector = {"line": {"color": "royalblue", "dash": "solid", "width": 2}},
            hovertemplate='<b>%{y}</b><br>Count: %{x}<br>Conversion: %{percentInitial}<extra></extra>'
        ))
        
        fig.update_layout(
            title=get_text('popup_performance_title', language),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_engagement_timeline_chart(self, data):
        """Create a timeline chart showing engagement patterns."""
        # This would be more meaningful with historical data
        # For now, create a simple comparison chart
        
        engagement_metrics = {
            'Practice Sessions': data.get('practice_with_video', 0) + data.get('practice_with_ai', 0),
            'Content Views': data.get('view_exercise', 0) + data.get('view_roadmap', 0),
            'AI Interactions': data.get('chat_ai', 0),
            'Health Surveys': data.get('health_survey', 0)
        }
        
        fig = go.Figure()
        
        metrics = list(engagement_metrics.keys())
        values = list(engagement_metrics.values())
        
        fig.add_trace(go.Scatter(
            x=metrics,
            y=values,
            mode='lines+markers',
            line=dict(color=self.color_scheme['primary'], width=3),
            marker=dict(size=10, color=self.color_scheme['secondary']),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Engagement Metrics Overview",
            xaxis_title="Metric Type",
            yaxis_title="Count",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_user_journey_sankey(self, data):
        """Create a Sankey diagram for user journey flow."""
        # Define the flow nodes
        nodes = [
            "First Open",     # 0
            "Login",          # 1
            "View Exercise",  # 2
            "Practice",       # 3
            "AI Chat",        # 4
            "App Remove"      # 5
        ]
        
        # Define the flows (source, target, value)
        flows = [
            (0, 1, data.get('login', 0)),           # First open to login
            (1, 2, data.get('view_exercise', 0)),   # Login to exercise view
            (2, 3, data.get('practice_with_video', 0) + data.get('practice_with_ai', 0)),  # Exercise to practice
            (3, 4, data.get('chat_ai', 0)),         # Practice to AI chat
            (0, 5, data.get('app_remove', 0))       # First open to removal
        ]
        
        # Filter out zero flows
        valid_flows = [(s, t, v) for s, t, v in flows if v > 0]
        
        if valid_flows:
            source = [flow[0] for flow in valid_flows]
            target = [flow[1] for flow in valid_flows]
            value = [flow[2] for flow in valid_flows]
            
            fig = go.Figure(data=[go.Sankey(
                node = dict(
                    pad = 15,
                    thickness = 20,
                    line = dict(color = "black", width = 0.5),
                    label = nodes,
                    color = self.color_scheme['primary']
                ),
                link = dict(
                    source = source,
                    target = target,
                    value = value,
                    color = 'rgba(79, 209, 199, 0.4)'
                )
            )])
            
            fig.update_layout(
                title_text="User Journey Flow",
                font_size=10,
                height=400
            )
            
            return fig
        
        # Return empty chart if no valid flows
        return go.Figure().add_annotation(
            text="No user journey data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font=dict(size=16)
        )
    
    def create_time_series_chart(self, time_series_data, language='en'):
        """Create a comprehensive time series chart showing all metrics over time.
        Adapts between daily and weekly views based on data range."""
        if not time_series_data:
            return go.Figure()
        
        # Determine granularity (daily vs weekly)
        is_daily, time_label, period_count = self.get_time_granularity(time_series_data)
        
        # Extract time labels and metrics
        time_periods = [item.get('time', f'{time_label} {i+1}') for i, item in enumerate(time_series_data)]
        
        fig = go.Figure()
        
        # Extended color palette for all metrics
        metric_colors = [
            '#48BB78',  # Green - success
            '#F56565',  # Red - error  
            '#4FD1C7',  # Teal - primary
            '#B19CD9',  # Purple - secondary
            '#ED8936',  # Orange - warning
            '#87A96B',  # Olive - accent
            '#38B2AC',  # Teal variant
            '#9F7AEA',  # Purple variant
            '#F6AD55',  # Orange variant
            '#68D391',  # Green variant
            '#FC8181',  # Red variant
            '#4299E1',  # Blue
            '#A0AEC0',  # Gray
            '#2D3748'   # Dark gray
        ]
        
        # Add traces for all available metrics
        metrics = {
            'New Users': ([item.get('first_open', 0) for item in time_series_data], metric_colors[0]),
            'App Removals': ([item.get('app_remove', 0) for item in time_series_data], metric_colors[1]),
            'Session Starts': ([item.get('session_start', 0) for item in time_series_data], metric_colors[2]),
            'App Opens': ([item.get('app_open', 0) for item in time_series_data], metric_colors[3]),
            'Logins': ([item.get('login', 0) for item in time_series_data], metric_colors[4]),
            'Exercise Views': ([item.get('view_exercise', 0) for item in time_series_data], metric_colors[5]),
            'Health Surveys': ([item.get('health_survey', 0) for item in time_series_data], metric_colors[6]),
            'Roadmap Views': ([item.get('view_roadmap', 0) for item in time_series_data], metric_colors[7]),
            'Video Practice': ([item.get('practice_with_video', 0) for item in time_series_data], metric_colors[8]),
            'AI Practice': ([item.get('practice_with_ai', 0) for item in time_series_data], metric_colors[9]),
            'AI Chat': ([item.get('chat_ai', 0) for item in time_series_data], metric_colors[10]),
            'Popups Shown': ([item.get('show_popup', 0) for item in time_series_data], metric_colors[11]),
            'Popup Details': ([item.get('view_detail_popup', 0) for item in time_series_data], metric_colors[12]),
            'Popups Closed': ([item.get('close_popup', 0) for item in time_series_data], metric_colors[13])
        }
        
        y_axis_label = self.get_y_axis_label('count', language)
        
        for metric_name, (values, color) in metrics.items():
            fig.add_trace(go.Scatter(
                x=time_periods,
                y=values,
                mode='lines+markers',
                name=metric_name,
                line=dict(color=color, width=3, shape='spline'),
                marker=dict(size=8, color=color),
                hovertemplate=f'<b>{metric_name}</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
            ))
        
        # Calculate tick interval to avoid label overlap
        # Show fewer labels for larger datasets
        if period_count > 30:
            dtick = 7  # Show every 7th label for very large datasets
        elif period_count > 14:
            dtick = 3  # Show every 3rd label
        else:
            dtick = 1  # Show all labels for small datasets
        
        fig.update_layout(
            title=get_text('metrics_trends_title', language),
            xaxis_title=get_text(time_label.lower(), language),
            yaxis_title=y_axis_label,
            height=600,  # Increased height for better visibility with more metrics
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="v",  # Vertical legend for better space utilization
                yanchor="top", 
                y=1, 
                xanchor="left", 
                x=1.02,
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
            ),
            xaxis=dict(
                tickangle=-45,  # Rotate labels 45 degrees
                dtick=dtick,  # Show every nth tick
                tickfont=dict(size=10)
            )
        )
        
        return fig
    
    def create_user_flow_trends_chart(self, time_series_data, language='en'):
        """Create a chart showing user acquisition vs churn trends."""
        if not time_series_data:
            return go.Figure()
        
        # Determine granularity (daily vs weekly)
        is_daily, time_label, period_count = self.get_time_granularity(time_series_data)
        
        time_periods = [item.get('time', f'{time_label} {i+1}') for i, item in enumerate(time_series_data)]
        new_users = [item.get('first_open', 0) for item in time_series_data]
        churn = [item.get('app_remove', 0) for item in time_series_data]
        
        y_axis_label = self.get_y_axis_label('count', language)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=new_users,
            mode='lines+markers',
            name=get_text('new_users', language),
            line=dict(color=self.color_scheme['success'], width=3, shape='spline'),
            marker=dict(size=8),
            fill='tonexty',
            hovertemplate=f'<b>New Users</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=churn,
            mode='lines+markers',
            name=get_text('churn', language),
            line=dict(color=self.color_scheme['error'], width=3, shape='spline'),
            marker=dict(size=8),
            hovertemplate=f'<b>Churn</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        # Calculate tick interval to avoid label overlap
        if period_count > 30:
            dtick = 7
        elif period_count > 14:
            dtick = 3
        else:
            dtick = 1
        
        fig.update_layout(
            title=get_text('user_flow_trends_title', language),
            xaxis_title=get_text(time_label.lower(), language),
            yaxis_title=y_axis_label,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(
                tickangle=-45,
                dtick=dtick,
                tickfont=dict(size=10)
            )
        )
        
        return fig
    
    def create_practice_trends_chart(self, time_series_data, language='en'):
        """Create a chart showing practice session trends (video vs AI)."""
        if not time_series_data:
            return go.Figure()
        
        # Determine granularity (daily vs weekly)
        is_daily, time_label, period_count = self.get_time_granularity(time_series_data)
        
        time_periods = [item.get('time', f'{time_label} {i+1}') for i, item in enumerate(time_series_data)]
        video_practice = [item.get('practice_with_video', 0) for item in time_series_data]
        ai_practice = [item.get('practice_with_ai', 0) for item in time_series_data]
        
        y_axis_label = self.get_y_axis_label('count', language)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=video_practice,
            mode='lines+markers',
            name=get_text('video_practice', language),
            line=dict(color=self.color_scheme['primary'], width=3, shape='spline'),
            marker=dict(size=8),
            stackgroup='one',
            hovertemplate=f'<b>Video Practice</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=ai_practice,
            mode='lines+markers',
            name=get_text('ai_practice', language),
            line=dict(color=self.color_scheme['secondary'], width=3, shape='spline'),
            marker=dict(size=8),
            stackgroup='one',
            hovertemplate=f'<b>AI Practice</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        # Calculate tick interval to avoid label overlap
        if period_count > 30:
            dtick = 7
        elif period_count > 14:
            dtick = 3
        else:
            dtick = 1
        
        fig.update_layout(
            title=get_text('practice_trends_title', language),
            xaxis_title=get_text(time_label.lower(), language),
            yaxis_title=y_axis_label,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(
                tickangle=-45,
                dtick=dtick,
                tickfont=dict(size=10)
            )
        )
        
        return fig
    
    def create_user_activity_comparison(self, time_series_data, language='en'):
        """Create a line chart comparing user activity metrics over time."""
        if not time_series_data:
            # Handle single data point case (aggregated data)
            return self._create_user_activity_comparison_single(time_series_data, language)
        
        # Determine granularity (daily vs weekly)
        is_daily, time_label, period_count = self.get_time_granularity(time_series_data)
        
        time_periods = [item.get('time', f'{time_label} {i+1}') for i, item in enumerate(time_series_data)]
        new_users = [item.get('first_open', 0) for item in time_series_data]
        active_sessions = [item.get('session_start', 0) for item in time_series_data]
        total_practice = [(item.get('practice_with_video', 0) + item.get('practice_with_ai', 0)) 
                         for item in time_series_data]
        
        y_axis_label = self.get_y_axis_label('count', language)
        
        fig = go.Figure()
        
        # New Users line
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=new_users,
            mode='lines+markers',
            name=get_text('new_users', language),
            line=dict(color=self.color_scheme['primary'], width=3, shape='spline'),
            marker=dict(size=10, color=self.color_scheme['primary']),
            hovertemplate='<b>' + get_text('new_users', language) + f'</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        # Active Sessions line
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=active_sessions,
            mode='lines+markers',
            name=get_text('active_sessions', language),
            line=dict(color=self.color_scheme['secondary'], width=3, shape='spline'),
            marker=dict(size=10, color=self.color_scheme['secondary']),
            hovertemplate='<b>' + get_text('active_sessions', language) + f'</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        # Total Practice line
        fig.add_trace(go.Scatter(
            x=time_periods,
            y=total_practice,
            mode='lines+markers',
            name=get_text('total_practice', language),
            line=dict(color=self.color_scheme['accent'], width=3, shape='spline'),
            marker=dict(size=10, color=self.color_scheme['accent']),
            hovertemplate='<b>' + get_text('total_practice', language) + f'</b><br>{time_label}: %{{x}}<br>{y_axis_label}: %{{y}}<extra></extra>'
        ))
        
        # Calculate tick interval to avoid label overlap
        if period_count > 30:
            dtick = 7
        elif period_count > 14:
            dtick = 3
        else:
            dtick = 1
        
        fig.update_layout(
            title=get_text('user_activity_comparison_title', language),
            xaxis_title=get_text(time_label.lower(), language),
            yaxis_title=y_axis_label,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                tickangle=-45,
                dtick=dtick,
                tickfont=dict(size=10)
            )
        )
        
        return fig
    
    def _create_user_activity_comparison_single(self, data, language='en'):
        """Create user activity comparison for single data point (aggregated data)."""
        metrics = [
            get_text('new_users', language),
            get_text('active_sessions', language),
            get_text('total_practice', language)
        ]
        
        values = [
            data.get('first_open', 0) if data else 0,
            data.get('session_start', 0) if data else 0,
            (data.get('practice_with_video', 0) + data.get('practice_with_ai', 0)) if data else 0
        ]
        
        fig = go.Figure(data=[
            go.Bar(
                x=metrics,
                y=values,
                marker_color=[self.color_scheme['primary'], 
                             self.color_scheme['secondary'],
                             self.color_scheme['accent']],
                text=values,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=get_text('user_activity_comparison_title', language),
            xaxis_title='Metrics',
            yaxis_title=get_text('count', language),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_user_funnel_analysis(self, data, language='en'):
        """Create a funnel chart showing user conversion through different stages."""
        # Calculate funnel stages
        stages = [
            (get_text('view_exercise_stage', language), data.get('view_exercise', 0)),
            (get_text('practice_video_stage', language), data.get('practice_with_video', 0)),
            (get_text('practice_ai_stage', language), data.get('practice_with_ai', 0)),
            (get_text('chat_ai_stage', language), data.get('chat_ai', 0))
        ]
        
        # Calculate conversion rates
        conversion_rates = []
        for i, (stage_name, stage_value) in enumerate(stages):
            if i == 0:
                conversion_rates.append("100%")
            else:
                prev_value = stages[i-1][1]
                if prev_value > 0:
                    rate = (stage_value / prev_value) * 100
                    conversion_rates.append(f"{rate:.1f}%")
                else:
                    conversion_rates.append("0%")
        
        # Create funnel visualization
        fig = go.Figure(go.Funnel(
            y=[stage[0] for stage in stages],
            x=[stage[1] for stage in stages],
            textposition="inside",
            textinfo="value+percent initial",
            opacity=0.85,
            marker={
                "color": [self.color_scheme['primary'], 
                         self.color_scheme['secondary'],
                         self.color_scheme['accent'],
                         self.color_scheme['success']],
                "line": {"width": 2, "color": "white"}
            },
            connector={"line": {"color": "rgb(63, 63, 63)", "width": 1}},
            hovertemplate='<b>%{y}</b><br>' +
                         get_text('users_count', language) + ': %{x}<br>' +
                         get_text('conversion_rate', language) + ': %{percentPrevious}<br>' +
                         get_text('conversion_from_start', language) + ': %{percentInitial}<br>' +
                         '<extra></extra>'
        ))
        
        # Add conversion rate annotations
        for i, rate in enumerate(conversion_rates[1:], 1):
            fig.add_annotation(
                x=0.95,
                y=i - 0.5,
                text=f"↓ {rate}",
                showarrow=False,
                font=dict(size=12, color=self.color_scheme['text']),
                xref="paper",
                yref="y"
            )
        
        fig.update_layout(
            title=get_text('user_funnel_analysis_title', language),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            margin=dict(l=20, r=80, t=60, b=20)  # Extra right margin for conversion rate annotations
        )
        
        return fig
    
    def create_churn_risk_indicator(self, data, language='en'):
        """Create a gauge chart showing churn risk based on retention and churn metrics."""
        # Calculate metrics
        first_open = max(data.get('first_open', 1), 1)  # Avoid division by zero
        app_remove = data.get('app_remove', 0)
        app_open = data.get('app_open', 0)
        
        # Calculate churn rate (app removals / first opens)
        churn_rate = (app_remove / first_open) * 100 if first_open > 0 else 0
        
        # Calculate retention rate (app opens - app removals) / first opens
        retention_rate = ((app_open - app_remove) / first_open) * 100 if first_open > 0 else 0
        retention_rate = max(0, min(100, retention_rate))  # Clamp to 0-100
        
        # Calculate risk score using the formula: (churn_rate * 2 + (100 - retention_rate)) / 3
        risk_score = (churn_rate * 2 + (100 - retention_rate)) / 3
        risk_score = max(0, min(100, risk_score))  # Clamp to 0-100
        
        # Determine risk level
        if risk_score <= 33:
            risk_level = get_text('risk_level_low', language)
            risk_color = self.color_scheme['success']
        elif risk_score <= 66:
            risk_level = get_text('risk_level_medium', language)
            risk_color = self.color_scheme['warning']
        else:
            risk_level = get_text('risk_level_high', language)
            risk_color = self.color_scheme['error']
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': get_text('churn_risk_indicator_title', language)},
            delta = {'reference': 50, 'decreasing': {'color': 'green'}, 'increasing': {'color': 'red'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': risk_color, 'thickness': 0.75},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 33], 'color': 'rgba(72, 187, 120, 0.2)'},  # Light green
                    {'range': [33, 66], 'color': 'rgba(237, 137, 54, 0.2)'},  # Light yellow/orange
                    {'range': [66, 100], 'color': 'rgba(245, 101, 101, 0.2)'}  # Light red
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_score
                }
            }
        ))
        
        # Add annotations for additional context
        fig.add_annotation(
            text=f"<b>{risk_level}</b><br>Churn: {churn_rate:.1f}% | Retention: {retention_rate:.1f}%",
            xref="paper",
            yref="paper",
            x=0.5,
            y=-0.15,
            showarrow=False,
            font=dict(size=12),
            align="center"
        )
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14)
        )
        
        return fig
    
    def create_period_comparison_chart(self, current_data, compare_data, granularity, language='en'):
        """Create a comprehensive period comparison bar chart.
        
        Args:
            current_data: Current period data (list of records)
            compare_data: Comparison period data (list of records)
            granularity: 'day', 'week', or 'month'
            language: Language code
            
        Returns:
            Plotly figure with grouped bar comparison
        """
        if not current_data or not compare_data:
            return go.Figure()
        
        metrics = {
            'New Users': 'first_open',
            'Sessions': 'session_start',
            'App Opens': 'app_open',
            'Video Practice': 'practice_with_video',
            'AI Practice': 'practice_with_ai',
            'AI Chat': 'chat_ai',
            'Exercise Views': 'view_exercise',
            'Health Surveys': 'health_survey'
        }
        
        current_values = []
        compare_values = []
        changes = []
        
        for metric_name, metric_key in metrics.items():
            current_val = sum(item.get(metric_key, 0) for item in current_data)
            compare_val = sum(item.get(metric_key, 0) for item in compare_data)
            
            current_values.append(current_val)
            compare_values.append(compare_val)
            
            if compare_val > 0:
                change = ((current_val - compare_val) / compare_val) * 100
            else:
                change = 0 if current_val == 0 else 100
            changes.append(change)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name=get_text('current_period', language) if language == 'en' else 'Thời Kỳ Hiện Tại',
            x=list(metrics.keys()),
            y=current_values,
            marker_color=self.color_scheme['primary'],
            hovertemplate='<b>%{x}</b><br>Current: %{y:,}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name=get_text('compare_to', language) if language == 'en' else 'So Sánh Với',
            x=list(metrics.keys()),
            y=compare_values,
            marker_color=self.color_scheme['secondary'],
            hovertemplate='<b>%{x}</b><br>Compare: %{y:,}<extra></extra>'
        ))
        
        for i, (metric, change) in enumerate(zip(metrics.keys(), changes)):
            max_val = max(current_values[i], compare_values[i])
            fig.add_annotation(
                x=metric,
                y=max_val + (max_val * 0.05),
                text=f"{change:+.1f}%",
                showarrow=False,
                font=dict(
                    color=self.color_scheme['error'] if change < 0 else self.color_scheme['success'],
                    size=11,
                    family="Arial Black"
                ),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
            )
        
        y_axis_label = self.get_y_axis_label('count', language)
        
        fig.update_layout(
            title=f"{granularity.title()} {get_text('period_comparison', language) if language == 'en' else 'So Sánh Thời Kỳ'}",
            xaxis_title=get_text('metrics', language) if language == 'en' else 'Chỉ Số',
            yaxis_title=y_axis_label,
            barmode='group',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=10)
            )
        )
        
        return fig
    
    def create_engagement_comparison_chart(self, current_data, compare_data, granularity, language='en'):
        """Create an engagement time comparison chart between two periods.
        
        Args:
            current_data: Current period data (list of records)
            compare_data: Comparison period data (list of records)
            granularity: 'day', 'week', or 'month'
            language: Language code
            
        Returns:
            Plotly figure with engagement comparison
        """
        if not current_data or not compare_data:
            return go.Figure()
        
        # Extract engagement times
        current_times = [item.get('time', '') for item in current_data]
        compare_times = [item.get('time', '') for item in compare_data]
        
        current_engagement = [item.get('avg_engage_time', 0) / 60 for item in current_data]  # Convert to minutes
        compare_engagement = [item.get('avg_engage_time', 0) / 60 for item in compare_data]
        
        fig = go.Figure()
        
        # Current period bars
        fig.add_trace(go.Bar(
            x=list(range(len(current_times))),
            y=current_engagement,
            name='Current Period',
            marker_color=self.color_scheme['primary'],
            customdata=current_times,
            hovertemplate='<b>Current Period</b><br>Time: %{customdata}<br>Avg Engagement: %{y:.1f} min<extra></extra>',
            opacity=0.8
        ))
        
        # Compare period bars
        fig.add_trace(go.Bar(
            x=list(range(len(compare_times))),
            y=compare_engagement,
            name='Compare Period',
            marker_color=self.color_scheme['secondary'],
            customdata=compare_times,
            hovertemplate='<b>Compare Period</b><br>Time: %{customdata}<br>Avg Engagement: %{y:.1f} min<extra></extra>',
            opacity=0.6
        ))
        
        # X-axis settings with smart label spacing
        period_count = max(len(current_data), len(compare_data))
        if period_count > 30:
            dtick = 7
        elif period_count > 14:
            dtick = 3
        else:
            dtick = 1
        
        fig.update_layout(
            title='⏱️ Average Engagement Time Comparison' if language == 'en' else '⏱️ So Sánh Thời Gian Tương Tác Trung Bình',
            xaxis_title='Period Index' if language == 'en' else 'Chỉ Số Thời Kỳ',
            yaxis_title='Minutes' if language == 'en' else 'Phút',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            barmode='group',
            hovermode='x unified',
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=dtick,
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                gridcolor='rgba(128,128,128,0.2)',
                zeroline=True,
                zerolinecolor='rgba(128,128,128,0.3)'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_comparison_trend_chart(self, current_data, compare_data, granularity, language='en'):
        """Create a trend comparison line chart showing both periods over time.
        
        Args:
            current_data: Current period data (list of records)
            compare_data: Comparison period data (list of records)
            granularity: 'day', 'week', or 'month'
            language: Language code
            
        Returns:
            Plotly figure with trend comparison
        """
        if not current_data or not compare_data:
            return go.Figure()
        
        current_times = [item.get('time', '') for item in current_data]
        compare_times = [item.get('time', '') for item in compare_data]
        
        metrics = {
            'New Users': 'first_open',
            'Sessions': 'session_start',
            'Practice Sessions': 'practice_with_video'
        }
        
        fig = go.Figure()
        
        colors = [self.color_scheme['primary'], self.color_scheme['accent'], self.color_scheme['success']]
        
        for idx, (metric_name, metric_key) in enumerate(metrics.items()):
            current_values = [item.get(metric_key, 0) for item in current_data]
            
            fig.add_trace(go.Scatter(
                x=list(range(len(current_times))),
                y=current_values,
                mode='lines+markers',
                name=f'Current - {metric_name}',
                line=dict(color=colors[idx], width=3),
                marker=dict(size=8),
                customdata=current_times,
                hovertemplate=f'<b>Current {metric_name}</b><br>Time: %{{customdata}}<br>Value: %{{y:,}}<extra></extra>'
            ))
        
        for idx, (metric_name, metric_key) in enumerate(metrics.items()):
            compare_values = [item.get(metric_key, 0) for item in compare_data]
            
            fig.add_trace(go.Scatter(
                x=list(range(len(compare_times))),
                y=compare_values,
                mode='lines+markers',
                name=f'Compare - {metric_name}',
                line=dict(color=colors[idx], width=3, dash='dash'),
                marker=dict(size=8, symbol='diamond'),
                customdata=compare_times,
                hovertemplate=f'<b>Compare {metric_name}</b><br>Time: %{{customdata}}<br>Value: %{{y:,}}<extra></extra>'
            ))
        
        period_count = max(len(current_data), len(compare_data))
        if period_count > 30:
            dtick = 7
        elif period_count > 14:
            dtick = 3
        else:
            dtick = 1
        
        y_axis_label = self.get_y_axis_label('count', language)
        
        fig.update_layout(
            title=f"{granularity.title()} {get_text('trend_comparison', language) if language == 'en' else 'So Sánh Xu Hướng'}",
            xaxis_title=get_text('period_index', language) if language == 'en' else 'Chỉ Số Thời Kỳ',
            yaxis_title=y_axis_label,
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            xaxis=dict(
                tickangle=-45,
                dtick=dtick,
                tickfont=dict(size=10)
            )
        )
        
        return fig
