import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class ChartGenerator:
    """Generates interactive charts for the yoga app analytics dashboard."""
    
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
    
    def create_acquisition_churn_chart(self, data):
        """Create a chart showing user acquisition vs churn."""
        categories = ['New Users', 'App Removals', 'Returning Users']
        values = [
            data.get('first_open', 0),
            data.get('app_remove', 0),
            data.get('app_open', 0)
        ]
        colors = [self.color_scheme['success'], self.color_scheme['error'], self.color_scheme['primary']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=colors,
                text=values,
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="User Acquisition vs Churn Analysis",
            xaxis_title="User Category",
            yaxis_title="Count",
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_practice_preferences_chart(self, data):
        """Create a donut chart showing practice preferences."""
        labels = ['Video Practice', 'AI Practice']
        values = [
            data.get('practice_with_video', 0),
            data.get('practice_with_ai', 0)
        ]
        colors = [self.color_scheme['primary'], self.color_scheme['secondary']]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker_colors=colors,
                hovertemplate='<b>%{label}</b><br>Sessions: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title="Practice Session Preferences",
            showlegend=True,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_feature_usage_chart(self, data):
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
            xaxis_title="Usage Count",
            yaxis_title="Features",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_ai_engagement_chart(self, data):
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
            title = {'text': "AI Engagement Rate (%)"},
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
    
    def create_popup_performance_chart(self, data):
        """Create a funnel chart for popup performance."""
        stages = ['Popups Shown', 'Detail Views', 'Popups Closed']
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
            title="Popup Interaction Funnel",
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
    
    def create_time_series_chart(self, time_series_data):
        """Create a comprehensive time series chart showing key metrics over time."""
        if not time_series_data:
            return go.Figure()
        
        # Extract time labels and metrics
        weeks = [item.get('time', f'Week {i+1}') for i, item in enumerate(time_series_data)]
        
        fig = go.Figure()
        
        # Add traces for key metrics
        metrics = {
            'New Users': ([item.get('first_open', 0) for item in time_series_data], self.color_scheme['success']),
            'App Opens': ([item.get('app_open', 0) for item in time_series_data], self.color_scheme['primary']),
            'Practice Sessions': ([item.get('practice_with_video', 0) + item.get('practice_with_ai', 0) for item in time_series_data], self.color_scheme['secondary']),
            'App Removals': ([item.get('app_remove', 0) for item in time_series_data], self.color_scheme['error'])
        }
        
        for metric_name, (values, color) in metrics.items():
            fig.add_trace(go.Scatter(
                x=weeks,
                y=values,
                mode='lines+markers',
                name=metric_name,
                line=dict(color=color, width=3),
                marker=dict(size=8, color=color),
                hovertemplate=f'<b>{metric_name}</b><br>Week: %{{x}}<br>Count: %{{y}}<extra></extra>'
            ))
        
        fig.update_layout(
            title="Key Metrics Trends Over Time",
            xaxis_title="Time Period",
            yaxis_title="Count",
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_user_flow_trends_chart(self, time_series_data):
        """Create a chart showing user acquisition vs churn trends."""
        if not time_series_data:
            return go.Figure()
        
        weeks = [item.get('time', f'Week {i+1}') for i, item in enumerate(time_series_data)]
        new_users = [item.get('first_open', 0) for item in time_series_data]
        churn = [item.get('app_remove', 0) for item in time_series_data]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weeks,
            y=new_users,
            mode='lines+markers',
            name='New Users',
            line=dict(color=self.color_scheme['success'], width=3),
            marker=dict(size=8),
            fill='tonexty',
            hovertemplate='<b>New Users</b><br>Week: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=weeks,
            y=churn,
            mode='lines+markers',
            name='Churn',
            line=dict(color=self.color_scheme['error'], width=3),
            marker=dict(size=8),
            hovertemplate='<b>Churn</b><br>Week: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="User Acquisition vs Churn Trends",
            xaxis_title="Time Period",
            yaxis_title="Count",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_practice_trends_chart(self, time_series_data):
        """Create a chart showing practice session trends (video vs AI)."""
        if not time_series_data:
            return go.Figure()
        
        weeks = [item.get('time', f'Week {i+1}') for i, item in enumerate(time_series_data)]
        video_practice = [item.get('practice_with_video', 0) for item in time_series_data]
        ai_practice = [item.get('practice_with_ai', 0) for item in time_series_data]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=weeks,
            y=video_practice,
            mode='lines+markers',
            name='Video Practice',
            line=dict(color=self.color_scheme['primary'], width=3),
            marker=dict(size=8),
            stackgroup='one',
            hovertemplate='<b>Video Practice</b><br>Week: %{x}<br>Sessions: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=weeks,
            y=ai_practice,
            mode='lines+markers',
            name='AI Practice',
            line=dict(color=self.color_scheme['secondary'], width=3),
            marker=dict(size=8),
            stackgroup='one',
            hovertemplate='<b>AI Practice</b><br>Week: %{x}<br>Sessions: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Practice Session Trends",
            xaxis_title="Time Period",
            yaxis_title="Practice Sessions",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
