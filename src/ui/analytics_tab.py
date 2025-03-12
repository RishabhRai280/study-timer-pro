"""
Analytics tab implementation for Study Timer Pro
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsTab:
    def __init__(self, parent, app):
        self.app = app
        self.settings = app.settings
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=self.settings.colors['bg'])
        
        # Create UI components
        self.create_analytics_panel()
        
        # Update statistics display
        self.update_statistics_display()
    
    def create_analytics_panel(self):
        """Create the analytics panel with statistics and charts"""
        # Statistics display
        stats_frame = tk.LabelFrame(self.frame,
                                  text="Study Statistics",
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'],
                                  font=('Arial', 12, 'bold'))
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Summary statistics
        self.today_time_label = tk.Label(stats_frame,
                                       text="Today's Study Time: 0h 0m",
                                       bg=self.settings.colors['bg'],
                                       fg=self.settings.colors['fg'],
                                       font=('Arial', 10, 'bold'))
        self.today_time_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.week_time_label = tk.Label(stats_frame,
                                      text="This Week's Study Time: 0h 0m",
                                      bg=self.settings.colors['bg'],
                                      fg=self.settings.colors['fg'],
                                      font=('Arial', 10, 'bold'))
        self.week_time_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.total_time_label = tk.Label(stats_frame,
                                       text="Total Study Time: 0h 0m",
                                       bg=self.settings.colors['bg'],
                                       fg=self.settings.colors['fg'],
                                       font=('Arial', 10, 'bold'))
        self.total_time_label.pack(anchor=tk.W, padx=10, pady=5)
        
        self.completed_tasks_label = tk.Label(stats_frame,
                                            text="Completed Tasks: 0",
                                            bg=self.settings.colors['bg'],
                                            fg=self.settings.colors['fg'],
                                            font=('Arial', 10, 'bold'))
        self.completed_tasks_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # Daily goal progress
        goal_frame = tk.Frame(stats_frame, bg=self.settings.colors['bg'])
        goal_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(goal_frame, 
               text="Daily Goal Progress:", 
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg'],
               font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.goal_progress = ttk.Progressbar(goal_frame, 
                                           orient=tk.HORIZONTAL, 
                                           length=200, 
                                           mode='determinate',
                                           style="TProgressbar")
        self.goal_progress.pack(fill=tk.X, pady=5)
        
        self.goal_percent = tk.Label(goal_frame,
                                   text="0%",
                                   bg=self.settings.colors['bg'],
                                   fg=self.settings.colors['fg'])
        self.goal_percent.pack(anchor=tk.E)
        
        # Create chart area
        self.chart_frame = tk.Frame(self.frame, bg=self.settings.colors['bg'])
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chart controls
        chart_control_frame = tk.Frame(self.frame, bg=self.settings.colors['bg'])
        chart_control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(chart_control_frame,
                text="Daily View",
                command=lambda: self.update_chart_view("daily"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(chart_control_frame,
                text="Weekly View",
                command=lambda: self.update_chart_view("weekly"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(chart_control_frame,
                text="Monthly View",
                command=lambda: self.update_chart_view("monthly"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Export button
        tk.Button(chart_control_frame,
                text="Export Data",
                command=self.app.export_statistics,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.RIGHT, padx=5)
        
        # Create initial chart
        self.create_study_time_chart()
    
    def create_study_time_chart(self, view_type="weekly"):
        """Create a chart showing study time data"""
        # Clear existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Get data based on view type
        if view_type == "daily":
            self.create_daily_chart(ax)
        elif view_type == "monthly":
            self.create_monthly_chart(ax)
        else:  # weekly (default)
            self.create_weekly_chart(ax)
        
        # Customize chart style
        ax.set_facecolor(self.settings.colors['bg'])
        fig.patch.set_facecolor(self.settings.colors['bg'])
        
        # Adjust text colors
        ax.title.set_color(self.settings.colors['fg'])
        ax.xaxis.label.set_color(self.settings.colors['fg'])
        ax.yaxis.label.set_color(self.settings.colors['fg'])
        ax.tick_params(colors=self.settings.colors['fg'])
        
        # Add chart to frame
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_weekly_chart(self, ax):
        """Create a weekly view chart"""
        # Get data for weekly view
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        times = [0, 0, 0, 0, 0, 0, 0]  # in minutes
        
        # Get actual data if available
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_str = day_date.strftime("%Y-%m-%d")
            if day_str in self.settings.daily_stats:
                times[i] = self.settings.daily_stats[day_str] // 60  # Convert seconds to minutes
        
        # Create bar chart
        bars = ax.bar(days, times, color=self.settings.colors['accent'])
        
        # Add labels and title
        ax.set_ylabel('Study Time (minutes)')
        ax.set_title('Weekly Study Time')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', color=self.settings.colors['fg'])
    
    def create_daily_chart(self, ax):
        """Create a daily view chart"""
        # Get data for daily view (hours of the day)
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        # For now, we'll just show a placeholder
        # In a real implementation, you would track study time by hour
        hours = list(range(24))
        times = [0] * 24  # Placeholder data
        
        # Create bar chart
        bars = ax.bar(hours, times, color=self.settings.colors['accent'])
        
        # Add labels and title
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel('Study Time (minutes)')
        ax.set_title('Today\'s Study Time by Hour')
        ax.set_xticks(range(0, 24, 2))  # Show every 2 hours
    
    def create_monthly_chart(self, ax):
        """Create a monthly view chart"""
        # Get data for monthly view
        today = datetime.now().date()
        first_day = today.replace(day=1)
        
        # Get number of days in month
        if today.month == 12:
            last_day = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        days_in_month = last_day.day
        
        # Prepare data
        days = list(range(1, days_in_month + 1))
        times = [0] * days_in_month
        
        # Fill in actual data
        for day in range(1, days_in_month + 1):
            day_str = f"{today.year}-{today.month:02d}-{day:02d}"
            if day_str in self.settings.daily_stats:
                times[day-1] = self.settings.daily_stats[day_str] // 60  # Convert seconds to minutes
        
        # Create bar chart
        bars = ax.bar(days, times, color=self.settings.colors['accent'])
        
        # Add labels and title
        ax.set_xlabel('Day of Month')
        ax.set_ylabel('Study Time (minutes)')
        ax.set_title(f'Study Time for {today.strftime("%B %Y")}')
        
        # Set x-ticks to show every 5 days
        ax.set_xticks(range(1, days_in_month + 1, 5))
    
    def update_chart_view(self, view_type):
        """Update the chart to show a different view"""
        self.create_study_time_chart(view_type)
    
    def update_statistics_display(self):
        """Update all statistics displays"""
        # Update time statistics
        today = datetime.now().date().strftime("%Y-%m-%d")
        today_seconds = self.settings.daily_stats.get(today, 0)
        today_hours, remainder = divmod(today_seconds, 3600)
        today_minutes = remainder // 60
        
        self.today_time_label.config(text=f"Today's Study Time: {today_hours}h {today_minutes}m")
        
        # Calculate week time
        current_date = datetime.now().date()
        start_of_week = current_date - timedelta(days=current_date.weekday())
        week_seconds = 0
        
        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_str = day_date.strftime("%Y-%m-%d")
            if day_str in self.settings.daily_stats:
                week_seconds += self.settings.daily_stats[day_str]
        
        week_hours, remainder = divmod(week_seconds, 3600)
        week_minutes = remainder // 60
        self.week_time_label.config(text=f"This Week's Study Time: {week_hours}h {week_minutes}m")
        
        # Total time
        total_seconds = sum(self.settings.daily_stats.values())
        total_hours, remainder = divmod(total_seconds, 3600)
        total_minutes = remainder // 60
        self.total_time_label.config(text=f"Total Study Time: {total_hours}h {total_minutes}m")
        
        # Tasks completed
        self.completed_tasks_label.config(text=f"Completed Tasks: {len(self.settings.completed_tasks)}")
        
        # Update goal progress
        self.update_goal_progress()
        
        # Update chart
        self.create_study_time_chart()
    
    def update_goal_progress(self):
        """Update the daily goal progress bar"""
        today = datetime.now().date().strftime("%Y-%m-%d")
        today_seconds = self.settings.daily_stats.get(today, 0)
        goal_minutes = int(self.settings.daily_goal.get())
        goal_seconds = goal_minutes * 60
        
        progress = min(100, int((today_seconds / goal_seconds) * 100))
        self.goal_progress['value'] = progress
        self.goal_percent.config(text=f"{progress}%")
    
    def adjust_layout_for_size(self, width, height):
        """Adjust layout based on window dimensions"""
        # Adjust chart size based on window dimensions
        if hasattr(self, 'chart_frame'):
            if width < 900:
                # Smaller chart for small windows
                for widget in self.chart_frame.winfo_children():
                    if isinstance(widget, tk.Canvas):
                        widget.config(width=width-100)
            else:
                # Regular chart size
                pass
    
    def apply_theme(self):
        """Apply the current theme to all UI elements"""
        # Update frame
        self.frame.configure(bg=self.settings.colors['bg'])
        
        # Update all widgets
        self.update_widget_colors(self.frame)
        
        # Update chart
        self.create_study_time_chart()
    
    def update_widget_colors(self, widget):
        """Recursively update colors of all widgets"""
        try:
            if isinstance(widget, tk.Label) or isinstance(widget, tk.LabelFrame):
                widget.configure(bg=self.settings.colors['bg'], fg=self.settings.colors['fg'])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.settings.colors['button'], fg=self.settings.colors['text'])
            elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Listbox):
                widget.configure(bg=self.settings.colors['bg'], fg=self.settings.colors['text'])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=self.settings.colors['bg'])
                
            # Recursively update children widgets
            for child in widget.winfo_children():
                self.update_widget_colors(child)
        except:
            pass