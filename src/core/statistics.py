"""
Statistics tracking functionality for Study Timer Pro
"""

from datetime import datetime, timedelta

class StatisticsManager:
    """
    Manages statistics for study sessions
    """
    
    def __init__(self):
        """Initialize the statistics manager"""
        self.daily_stats = {}  # Format: {"YYYY-MM-DD": seconds}
        self.completed_tasks = []
    
    def add_session_time(self, seconds):
        """
        Add completed session time to statistics
        
        Args:
            seconds: Duration of the session in seconds
        """
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        if today in self.daily_stats:
            self.daily_stats[today] += seconds
        else:
            self.daily_stats[today] = seconds
    
    def add_completed_task(self, task):
        """
        Add a completed task to statistics
        
        Args:
            task: Task description
        """
        # Add timestamp to task
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task_with_timestamp = f"{timestamp} - {task}"
        self.completed_tasks.append(task_with_timestamp)
    
    def get_today_time(self):
        """
        Get today's total study time in seconds
        
        Returns:
            int: Total study time in seconds
        """
        today = datetime.now().date().strftime("%Y-%m-%d")
        return self.daily_stats.get(today, 0)
    
    def get_week_time(self):
        """
        Get this week's total study time in seconds
        
        Returns:
            int: Total study time in seconds
        """
        current_date = datetime.now().date()
        start_of_week = current_date - timedelta(days=current_date.weekday())
        week_seconds = 0
        
        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_str = day_date.strftime("%Y-%m-%d")
            if day_str in self.daily_stats:
                week_seconds += self.daily_stats[day_str]
        
        return week_seconds
    
    def get_month_time(self):
        """
        Get this month's total study time in seconds
        
        Returns:
            int: Total study time in seconds
        """
        current_date = datetime.now().date()
        month_prefix = current_date.strftime("%Y-%m")
        month_seconds = 0
        
        for day_str, seconds in self.daily_stats.items():
            if day_str.startswith(month_prefix):
                month_seconds += seconds
        
        return month_seconds
    
    def get_total_time(self):
        """
        Get all-time total study time in seconds
        
        Returns:
            int: Total study time in seconds
        """
        return sum(self.daily_stats.values())
    
    def get_streak_days(self):
        """
        Calculate the current streak of consecutive study days
        
        Returns:
            int: Number of consecutive days with study sessions
        """
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        # Count backwards from today
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in self.daily_stats and self.daily_stats[date_str] >= 10 * 60:  # At least 10 minutes
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        return streak
    
    def get_study_days(self):
        """
        Get a list of days with study sessions
        
        Returns:
            list: List of date strings with study sessions
        """
        return list(self.daily_stats.keys())
    
    def format_time(self, seconds):
        """
        Format seconds into hours and minutes
        
        Args:
            seconds: Time in seconds
        
        Returns:
            str: Formatted time string (e.g., "2h 30m")
        """
        hours, remainder = divmod(seconds, 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m"
    
    def get_daily_goal_progress(self, goal_minutes):
        """
        Calculate progress towards daily goal
        
        Args:
            goal_minutes: Daily goal in minutes
        
        Returns:
            float: Percentage of goal completed (0-100)
        """
        today_seconds = self.get_today_time()
        goal_seconds = goal_minutes * 60
        
        if goal_seconds == 0:
            return 100.0
        
        progress = (today_seconds / goal_seconds) * 100
        return min(100.0, progress)
    
    def reset_statistics(self):
        """Reset all statistics"""
        self.daily_stats = {}
        self.completed_tasks = []