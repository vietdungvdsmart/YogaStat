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
    
    def render_comparison_controls(self, granularity: str = 'day'):
        """Render date range controls specifically for comparison tab.
        
        Args:
            granularity: 'day', 'week', or 'month' - determines UI type
        
        Returns:
            Tuple of ((current_start, current_end), (compare_start, compare_end))
        """
        col1, col2 = st.columns(2)
        
        if granularity == 'day':
            # Use date pickers for daily granularity
            with col1:
                st.subheader("📅 Current Period")
                current_filter = DateRangeFilter(key_prefix=f"{self.key_prefix}current_", data=self.data)
                current_range = current_filter.render()
            
            with col2:
                st.subheader("📅 Compare To")
                compare_filter = DateRangeFilter(key_prefix=f"{self.key_prefix}compare_", data=self.data)
                compare_range = compare_filter.render()
            
            return current_range, compare_range
        
        elif granularity == 'week':
            # Use dropdown for week selection
            weeks = self.get_available_weeks()
            
            if not weeks:
                st.error("No weekly data available")
                today = date.today()
                return (today, today), (today, today)
            
            week_labels = [w[0] for w in weeks]
            
            with col1:
                st.subheader("📅 Current Period")
                
                # Initialize session state
                current_key = f"{self.key_prefix}current_week"
                if current_key not in st.session_state:
                    st.session_state[current_key] = len(weeks) - 1  # Default to latest week
                
                current_idx = st.selectbox(
                    "Select week:",
                    options=range(len(weeks)),
                    format_func=lambda i: week_labels[i],
                    index=st.session_state[current_key],
                    key=f"{current_key}_selector"
                )
                st.session_state[current_key] = current_idx
                current_range = (weeks[current_idx][1], weeks[current_idx][2])
            
            with col2:
                st.subheader("📅 Compare To")
                
                # Initialize session state
                compare_key = f"{self.key_prefix}compare_week"
                if compare_key not in st.session_state:
                    st.session_state[compare_key] = max(0, len(weeks) - 2)  # Default to previous week
                
                compare_idx = st.selectbox(
                    "Select week:",
                    options=range(len(weeks)),
                    format_func=lambda i: week_labels[i],
                    index=st.session_state[compare_key],
                    key=f"{compare_key}_selector"
                )
                st.session_state[compare_key] = compare_idx
                compare_range = (weeks[compare_idx][1], weeks[compare_idx][2])
            
            return current_range, compare_range
        
        else:  # month
            # Use dropdown for month selection
            months = self.get_available_months()
            
            if not months:
                st.error("No monthly data available")
                today = date.today()
                return (today, today), (today, today)
            
            month_labels = [m[0] for m in months]
            
            with col1:
                st.subheader("📅 Current Period")
                
                # Initialize session state
                current_key = f"{self.key_prefix}current_month"
                if current_key not in st.session_state:
                    st.session_state[current_key] = len(months) - 1  # Default to latest month
                
                current_idx = st.selectbox(
                    "Select month:",
                    options=range(len(months)),
                    format_func=lambda i: month_labels[i],
                    index=st.session_state[current_key],
                    key=f"{current_key}_selector"
                )
                st.session_state[current_key] = current_idx
                current_range = (months[current_idx][1], months[current_idx][2])
            
            with col2:
                st.subheader("📅 Compare To")
                
                # Initialize session state
                compare_key = f"{self.key_prefix}compare_month"
                if compare_key not in st.session_state:
                    st.session_state[compare_key] = max(0, len(months) - 2)  # Default to previous month
                
                compare_idx = st.selectbox(
                    "Select month:",
                    options=range(len(months)),
                    format_func=lambda i: month_labels[i],
                    index=st.session_state[compare_key],
                    key=f"{compare_key}_selector"
                )
                st.session_state[compare_key] = compare_idx
                compare_range = (months[compare_idx][1], months[compare_idx][2])
            
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
    
    def get_available_weeks(self) -> List[Tuple[str, date, date]]:
        """Extract available weeks from data (Monday-Sunday boundaries).
        
        Returns:
            List of tuples: (week_label, start_date, end_date)
        """
        if not self.data:
            return []
        
        dates = []
        for item in self.data:
            try:
                item_date = datetime.strptime(item['time'], '%d/%m/%Y').date()
                dates.append(item_date)
            except (ValueError, KeyError):
                continue
        
        if not dates:
            return []
        
        min_date = min(dates)
        max_date = max(dates)
        
        # Find the Monday of the week containing min_date
        days_since_monday = min_date.weekday()
        current_monday = min_date - timedelta(days=days_since_monday)
        
        weeks = []
        week_num = 1
        
        while current_monday <= max_date:
            week_end = current_monday + timedelta(days=6)
            
            # Format: "Week 1: Jan 1 - Jan 7, 2025"
            if current_monday.year == week_end.year:
                week_label = f"Week {week_num}: {current_monday.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
            else:
                week_label = f"Week {week_num}: {current_monday.strftime('%b %d, %Y')} - {week_end.strftime('%b %d, %Y')}"
            
            weeks.append((week_label, current_monday, week_end))
            current_monday += timedelta(days=7)
            week_num += 1
        
        return weeks
    
    def get_available_months(self) -> List[Tuple[str, date, date]]:
        """Extract available months from data.
        
        Returns:
            List of tuples: (month_label, start_date, end_date)
        """
        if not self.data:
            return []
        
        dates = []
        for item in self.data:
            try:
                item_date = datetime.strptime(item['time'], '%d/%m/%Y').date()
                dates.append(item_date)
            except (ValueError, KeyError):
                continue
        
        if not dates:
            return []
        
        min_date = min(dates)
        max_date = max(dates)
        
        # Get all unique months
        months = set()
        current_date = date(min_date.year, min_date.month, 1)
        
        while current_date <= max_date:
            months.add((current_date.year, current_date.month))
            # Move to next month
            if current_date.month == 12:
                current_date = date(current_date.year + 1, 1, 1)
            else:
                current_date = date(current_date.year, current_date.month + 1, 1)
        
        # Convert to list of tuples with labels and date ranges
        month_list = []
        for year, month in sorted(months):
            month_start = date(year, month, 1)
            # Get last day of month
            if month == 12:
                month_end = date(year, 12, 31)
            else:
                next_month = date(year, month + 1, 1)
                month_end = next_month - timedelta(days=1)
            
            month_label = month_start.strftime('%B %Y')
            month_list.append((month_label, month_start, month_end))
        
        return month_list