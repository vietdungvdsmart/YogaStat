import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from .translations import get_text

class ChartGenerator:
    """Generates interactive charts for the yoga app analytics dashboard."""
    # Ghi chú (VI): Danh sách hàm sinh biểu đồ và ý nghĩa
    # - create_feature_adoption_funnel: Biểu đồ phễu thể hiện mức độ sử dụng tính năng (xem bài tập → luyện video → luyện AI → chat AI)
    # - create_user_funnel_analysis: Biểu đồ phễu phân tích chuyển đổi người dùng theo các bước sử dụng tính năng
    # - create_time_series_chart: Biểu đồ chuỗi thời gian cho tất cả metric theo từng tuần
    # - create_user_flow_trends_chart: Biểu đồ xu hướng người dùng mới vs rời bỏ theo thời gian
    # - create_practice_trends_chart: Biểu đồ xu hướng luyện tập (video vs AI) theo thời gian
    # - create_user_activity_comparison: So sánh hoạt động người dùng theo thời gian (người dùng mới, phiên hoạt động, tổng buổi luyện tập)
    # - _create_user_activity_comparison_single: Phiên bản cột cho dữ liệu gộp 1 kỳ (không phải chuỗi thời gian)
    # - create_feature_usage_chart: Biểu đồ thanh ngang về mức độ sử dụng các tính năng chính
    # - create_ai_engagement_chart: Đồng hồ đo (gauge) thể hiện mức độ tương tác với AI
    # - create_popup_performance_chart: Biểu đồ phễu hiệu suất popup (hiển thị → xem chi tiết → đóng)
    # - create_engagement_score_radar: Radar điểm tương tác đa chiều (login, survey, nội dung, AI, popup, giữ chân)
    # - create_user_journey_sankey: Sơ đồ Sankey mô tả hành trình người dùng qua các bước
    # - create_churn_risk_indicator: Đồng hồ đo rủi ro rời bỏ dựa trên churn/retention

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
        """Create a comprehensive time series chart showing all metrics over time."""
        if not time_series_data:
            return go.Figure()
        
        # Extract time labels and metrics
        weeks = [item.get('time', f'Week {i+1}') for i, item in enumerate(time_series_data)]
        
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
        
        for metric_name, (values, color) in metrics.items():
            fig.add_trace(go.Scatter(
                x=weeks,
                y=values,
                mode='lines+markers',
                name=metric_name,
                line=dict(color=color, width=3, shape='spline'),
                marker=dict(size=8, color=color),
                hovertemplate=f'<b>{metric_name}</b><br>Week: %{{x}}<br>Count: %{{y}}<extra></extra>'
            ))
        
        fig.update_layout(
            title=get_text('metrics_trends_title', language),
            xaxis_title=get_text('week', language),
            yaxis_title="Count",
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
            )
        )
        
        return fig
    
    def create_user_flow_trends_chart(self, time_series_data, language='en'):
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
            name=get_text('new_users', language),
            line=dict(color=self.color_scheme['success'], width=3, shape='spline'),
            marker=dict(size=8),
            fill='tonexty',
            hovertemplate='<b>New Users</b><br>Week: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=weeks,
            y=churn,
            mode='lines+markers',
            name=get_text('churn', language),
            line=dict(color=self.color_scheme['error'], width=3, shape='spline'),
            marker=dict(size=8),
            hovertemplate='<b>Churn</b><br>Week: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=get_text('user_flow_trends_title', language),
            xaxis_title="Time Period",
            yaxis_title="Count",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_practice_trends_chart(self, time_series_data, language='en'):
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
            name=get_text('video_practice', language),
            line=dict(color=self.color_scheme['primary'], width=3, shape='spline'),
            marker=dict(size=8),
            stackgroup='one',
            hovertemplate='<b>Video Practice</b><br>Week: %{x}<br>Sessions: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=weeks,
            y=ai_practice,
            mode='lines+markers',
            name=get_text('ai_practice', language),
            line=dict(color=self.color_scheme['secondary'], width=3, shape='spline'),
            marker=dict(size=8),
            stackgroup='one',
            hovertemplate='<b>AI Practice</b><br>Week: %{x}<br>Sessions: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=get_text('practice_trends_title', language),
            xaxis_title="Time Period",
            yaxis_title="Practice Sessions",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    def create_user_activity_comparison(self, time_series_data, language='en'):
        """Create a line chart comparing user activity metrics over time."""
        if not time_series_data:
            # Handle single data point case (aggregated data)
            return self._create_user_activity_comparison_single(time_series_data, language)
        
        weeks = [item.get('time', f'Week {i+1}') for i, item in enumerate(time_series_data)]
        new_users = [item.get('first_open', 0) for item in time_series_data]
        active_sessions = [item.get('session_start', 0) for item in time_series_data]
        total_practice = [(item.get('practice_with_video', 0) + item.get('practice_with_ai', 0)) 
                         for item in time_series_data]
        
        fig = go.Figure()
        
        # New Users line
        fig.add_trace(go.Scatter(
            x=weeks,
            y=new_users,
            mode='lines+markers',
            name=get_text('new_users', language),
            line=dict(color=self.color_scheme['primary'], width=3, shape='spline'),
            marker=dict(size=10, color=self.color_scheme['primary']),
            hovertemplate='<b>' + get_text('new_users', language) + '</b><br>Week: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        # Active Sessions line
        fig.add_trace(go.Scatter(
            x=weeks,
            y=active_sessions,
            mode='lines+markers',
            name=get_text('active_sessions', language),
            line=dict(color=self.color_scheme['secondary'], width=3, shape='spline'),
            marker=dict(size=10, color=self.color_scheme['secondary']),
            hovertemplate='<b>' + get_text('active_sessions', language) + '</b><br>Week: %{x}<br>Count: %{y}<extra></extra>'
        ))
        
        # Total Practice line
        fig.add_trace(go.Scatter(
            x=weeks,
            y=total_practice,
            mode='lines+markers',
            name=get_text('total_practice', language),
            line=dict(color=self.color_scheme['accent'], width=3, shape='spline'),
            marker=dict(size=10, color=self.color_scheme['accent']),
            hovertemplate='<b>' + get_text('total_practice', language) + '</b><br>Week: %{x}<br>Sessions: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=get_text('user_activity_comparison_title', language),
            xaxis_title=get_text('week', language),
            yaxis_title=get_text('count', language),
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
