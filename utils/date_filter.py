"""Google Analytics-style date range filter component."""
import streamlit as st
from datetime import datetime, timedelta, date
from typing import Optional, Tuple, List, Dict

class DateRangeFilter:
    """Date range filter with presets and custom range selection."""
    
    # Preset options similar to Google Analytics
    PRESETS = {
        'Today': ('today', 0),
        'Yesterday': ('yesterday', 1),
        'Last 7 days': ('last_days', 7),
        'Last 14 days': ('last_days', 14),
        'Last 28 days': ('last_days', 28),
        'Last 30 days': ('last_days', 30),
        'Last 90 days': ('last_days', 90),
        'Last 12 months': ('last_months', 12),
        'This week (Sun - Today)': ('this_week', 0),
        'Last week (Sun - Sat)': ('last_week', 0),
        'Custom': ('custom', 0)
    }
    
    def __init__(self, key_prefix: str = "", data: Optional[List[Dict]] = None):
        """Initialize the date range filter.
        
        Args:
            key_prefix: Prefix for session state keys to avoid conflicts
            data: Optional data to determine initial date range
        """
        self.key_prefix = key_prefix
        self.data = data
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize session state variables."""
        # If we have data, use its date range for initialization
        if self.data:
            dates = []
            for period in self.data:
                try:
                    # Parse DD/MM/YYYY format
                    period_date = datetime.strptime(period['time'], '%d/%m/%Y').date()
                    dates.append(period_date)
                except (ValueError, KeyError):
                    continue
            
            if dates:
                # Use the full data range by default
                min_date = min(dates)
                max_date = max(dates)
                
                if f"{self.key_prefix}selected_preset" not in st.session_state:
                    st.session_state[f"{self.key_prefix}selected_preset"] = "Custom"
                    
                if f"{self.key_prefix}custom_start" not in st.session_state:
                    # Start from 7 days before the earliest data point
                    st.session_state[f"{self.key_prefix}custom_start"] = min_date - timedelta(days=6)
                    
                if f"{self.key_prefix}custom_end" not in st.session_state:
                    st.session_state[f"{self.key_prefix}custom_end"] = max_date
                    
                if f"{self.key_prefix}applied_range" not in st.session_state:
                    # Show all data by default
                    st.session_state[f"{self.key_prefix}applied_range"] = (min_date - timedelta(days=6), max_date)
                return
        
        # Fallback to default if no data
        if f"{self.key_prefix}selected_preset" not in st.session_state:
            st.session_state[f"{self.key_prefix}selected_preset"] = "Last 7 days"
        
        if f"{self.key_prefix}custom_start" not in st.session_state:
            st.session_state[f"{self.key_prefix}custom_start"] = date.today() - timedelta(days=7)
        
        if f"{self.key_prefix}custom_end" not in st.session_state:
            st.session_state[f"{self.key_prefix}custom_end"] = date.today()
        
        if f"{self.key_prefix}applied_range" not in st.session_state:
            # Default to last 7 days
            start, end = self._calculate_preset_range("Last 7 days")
            st.session_state[f"{self.key_prefix}applied_range"] = (start, end)
    
    def _calculate_preset_range(self, preset: str) -> Tuple[date, date]:
        """Calculate date range for a preset option.
        
        Args:
            preset: The preset option selected
            
        Returns:
            Tuple of (start_date, end_date)
        """
        today = date.today()
        preset_type, value = self.PRESETS[preset]
        
        if preset_type == 'today':
            return (today, today)
        elif preset_type == 'yesterday':
            yesterday = today - timedelta(days=1)
            return (yesterday, yesterday)
        elif preset_type == 'last_days':
            start = today - timedelta(days=value-1)
            return (start, today)
        elif preset_type == 'last_months':
            start = today - timedelta(days=value*30)
            return (start, today)
        elif preset_type == 'this_week':
            # Find the most recent Sunday
            days_since_sunday = today.weekday() + 1 if today.weekday() != 6 else 0
            week_start = today - timedelta(days=days_since_sunday)
            return (week_start, today)
        elif preset_type == 'last_week':
            # Last complete week (Sunday to Saturday)
            days_since_sunday = today.weekday() + 1 if today.weekday() != 6 else 0
            last_sunday = today - timedelta(days=days_since_sunday + 7)
            last_saturday = last_sunday + timedelta(days=6)
            return (last_sunday, last_saturday)
        elif preset_type == 'custom':
            return (
                st.session_state[f"{self.key_prefix}custom_start"],
                st.session_state[f"{self.key_prefix}custom_end"]
            )
        
        # Default fallback
        return (today - timedelta(days=7), today)
    
    def render(self) -> Tuple[date, date]:
        """Render the date range filter component.
        
        Returns:
            Tuple of (start_date, end_date) for the selected range
        """
        # Main container with Google Analytics-like styling
        with st.container():
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                # Preset selector
                selected_preset = st.selectbox(
                    "Date Range",
                    options=list(self.PRESETS.keys()),
                    index=list(self.PRESETS.keys()).index(st.session_state[f"{self.key_prefix}selected_preset"]),
                    key=f"{self.key_prefix}preset_selector"
                )
                
                if selected_preset != st.session_state[f"{self.key_prefix}selected_preset"]:
                    st.session_state[f"{self.key_prefix}selected_preset"] = selected_preset
                    if selected_preset != "Custom":
                        # Auto-apply non-custom presets
                        start, end = self._calculate_preset_range(selected_preset)
                        st.session_state[f"{self.key_prefix}applied_range"] = (start, end)
                        st.rerun()
            
            with col2:
                if selected_preset == "Custom":
                    # Show date pickers for custom range
                    subcol1, subcol2 = st.columns(2)
                    with subcol1:
                        custom_start = st.date_input(
                            "Start date",
                            value=st.session_state[f"{self.key_prefix}custom_start"],
                            key=f"{self.key_prefix}start_picker",
                            max_value=date.today()
                        )
                        st.session_state[f"{self.key_prefix}custom_start"] = custom_start
                    
                    with subcol2:
                        custom_end = st.date_input(
                            "End date",
                            value=st.session_state[f"{self.key_prefix}custom_end"],
                            key=f"{self.key_prefix}end_picker",
                            min_value=custom_start,
                            max_value=date.today()
                        )
                        st.session_state[f"{self.key_prefix}custom_end"] = custom_end
                else:
                    # Show the calculated range for presets
                    start, end = self._calculate_preset_range(selected_preset)
                    if start == end:
                        st.info(f"📅 {start.strftime('%b %d, %Y')}")
                    else:
                        st.info(f"📅 {start.strftime('%b %d, %Y')} - {end.strftime('%b %d, %Y')}")
            
            with col3:
                if selected_preset == "Custom":
                    # Apply button for custom range
                    if st.button("Apply", key=f"{self.key_prefix}apply_btn", type="primary", use_container_width=True):
                        start = st.session_state[f"{self.key_prefix}custom_start"]
                        end = st.session_state[f"{self.key_prefix}custom_end"]
                        st.session_state[f"{self.key_prefix}applied_range"] = (start, end)
                        st.rerun()
        
        # Return the currently applied range
        return st.session_state[f"{self.key_prefix}applied_range"]
    
    def filter_data(self, data: List[Dict], date_field: str = 'time') -> List[Dict]:
        """Filter data based on the selected date range.
        
        Args:
            data: List of data dictionaries with date field
            date_field: Name of the date field in the data
            
        Returns:
            Filtered list of data within the selected range
        """
        start_date, end_date = st.session_state[f"{self.key_prefix}applied_range"]
        filtered_data = []
        
        for item in data:
            if date_field in item:
                # Parse date from DD/MM/YYYY format
                try:
                    date_str = item[date_field]
                    # Handle case where date represents end of 7-day period
                    item_date = datetime.strptime(date_str, '%d/%m/%Y').date()
                    
                    # Since each date represents the END of a 7-day period,
                    # we check if any part of that period falls within our range
                    period_start = item_date - timedelta(days=6)
                    period_end = item_date
                    
                    # Check if periods overlap
                    if period_start <= end_date and period_end >= start_date:
                        filtered_data.append(item)
                except (ValueError, TypeError):
                    # Skip items with invalid dates
                    continue
        
        return filtered_data
    
    def get_range_string(self) -> str:
        """Get a string representation of the current date range.
        
        Returns:
            String describing the current date range
        """
        start, end = st.session_state[f"{self.key_prefix}applied_range"]
        preset = st.session_state[f"{self.key_prefix}selected_preset"]
        
        if preset != "Custom" and preset in self.PRESETS:
            return preset
        else:
            if start == end:
                return start.strftime('%b %d, %Y')
            else:
                return f"{start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}"
    
    def render_comparison_controls(self):
        """Render date range controls specifically for comparison tab.
        
        Returns:
            Tuple of ((current_start, current_end), (compare_start, compare_end))
        """
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📅 Current Period")
            current_filter = DateRangeFilter(key_prefix=f"{self.key_prefix}current_", data=self.data)
            current_range = current_filter.render()
        
        with col2:
            st.subheader("📅 Compare To")
            compare_filter = DateRangeFilter(key_prefix=f"{self.key_prefix}compare_", data=self.data)
            compare_range = compare_filter.render()
        
        return current_range, compare_range
    
    def get_granularity_selector(self):
        """Render granularity selector for comparison.
        
        Returns:
            Selected granularity ('day', 'week', 'month')
        """
        if f"{self.key_prefix}granularity" not in st.session_state:
            st.session_state[f"{self.key_prefix}granularity"] = "week"
        
        st.subheader("📊 Compare By")
        granularity = st.selectbox(
            "Aggregation granularity:",
            options=['Day', 'Week', 'Month'],
            index=['day', 'week', 'month'].index(st.session_state[f"{self.key_prefix}granularity"]),
            key=f"{self.key_prefix}granularity_selector"
        )
        
        st.session_state[f"{self.key_prefix}granularity"] = granularity.lower()
        return granularity.lower()