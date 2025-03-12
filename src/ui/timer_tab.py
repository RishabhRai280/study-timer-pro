"""
Timer tab implementation for Study Timer Pro
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import calendar
from datetime import datetime, timedelta
import platform
import subprocess
import psutil
import os
from PIL import Image, ImageTk
from io import BytesIO
import requests

from utils.notifications import show_notification
from core.timer import TimerManager
from core.app_blocker import block_application, unblock_application
from core.website_blocker import block_website, unblock_website, get_hosts_path

class TimerTab:
    def __init__(self, parent, app):
        self.app = app
        self.settings = app.settings
        self.notification_manager = app.notification_manager
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=self.settings.colors['bg'])
        
        # Timer state
        self.is_timer_running = False
        self.paused = False
        self.remaining_seconds = 0
        self.start_time = None
        self.current_timer_thread = None
        
        # Create UI components
        self.setup_frames()
        self.create_left_panel()
        self.create_center_panel()
        self.create_right_panel()
        
        # Start monitoring thread
        self.start_monitoring()
        
        # Create minimized window
        self.create_minimized_window()
        
        # Update session indicators
        self.update_session_indicators()
        
        # Update calendar
        self.update_calendar()
    
    def setup_frames(self):
        """Set up the main frames for the timer tab"""
        # Main container with padding
        self.main_container = tk.Frame(self.frame, bg=self.settings.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Three columns
        self.left_frame = tk.Frame(self.main_container, bg=self.settings.colors['bg'])
        self.center_frame = tk.Frame(self.main_container, bg=self.settings.colors['bg'])
        self.right_frame = tk.Frame(self.main_container, bg=self.settings.colors['bg'])
        
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, expand=True)
        self.center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, expand=True)
    
    def create_left_panel(self):
        """Create the left panel with timer controls and settings"""
        # Timer controls
        controls_frame = tk.Frame(self.left_frame, bg=self.settings.colors['bg'])
        controls_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = tk.Button(controls_frame,
                                    text="Start Session",
                                    command=self.start_session,
                                    bg=self.settings.colors['button'],
                                    fg=self.settings.colors['text'],
                                    font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT,
                                    width=10,
                                    pady=10)
        self.start_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.pause_button = tk.Button(controls_frame,
                                    text="Pause",
                                    command=self.pause_resume_session,
                                    bg=self.settings.colors['button'],
                                    fg=self.settings.colors['text'],
                                    font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT,
                                    width=10,
                                    pady=10,
                                    state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.stop_button = tk.Button(controls_frame,
                                   text="Stop Session",
                                   command=self.stop_session,
                                   bg=self.settings.colors['button'],
                                   fg=self.settings.colors['text'],
                                   font=('Arial', 10, 'bold'),
                                   relief=tk.FLAT,
                                   width=10,
                                   pady=10)
        self.stop_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.reset_button = tk.Button(self.left_frame,
                                    text="Reset Session",
                                    command=self.reset_session,
                                    bg=self.settings.colors['button'],
                                    fg=self.settings.colors['text'],
                                    font=('Arial', 10, 'bold'),
                                    relief=tk.FLAT,
                                    width=31,
                                    pady=10)
        self.reset_button.pack(pady=5, fill=tk.X)
        
        # Time settings
        settings_frame = tk.LabelFrame(self.left_frame,
                                     text="Pomodoro Settings",
                                     bg=self.settings.colors['bg'],
                                     fg=self.settings.colors['fg'],
                                     font=('Arial', 10, 'bold'))
        settings_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Grid layout for time settings
        tk.Label(settings_frame, text="Focus time (min):", bg=self.settings.colors['bg'], fg=self.settings.colors['fg']).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Entry(settings_frame, textvariable=self.settings.focus_time, width=5, bg=self.settings.colors['bg'], fg=self.settings.colors['text']).grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(settings_frame, text="Short break (min):", bg=self.settings.colors['bg'], fg=self.settings.colors['fg']).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Entry(settings_frame, textvariable=self.settings.short_break, width=5, bg=self.settings.colors['bg'], fg=self.settings.colors['text']).grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(settings_frame, text="Long break (min):", bg=self.settings.colors['bg'], fg=self.settings.colors['fg']).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Entry(settings_frame, textvariable=self.settings.long_break, width=5, bg=self.settings.colors['bg'], fg=self.settings.colors['text']).grid(row=2, column=1, padx=5, pady=2)
        
        tk.Label(settings_frame, text="Sessions before long break:", bg=self.settings.colors['bg'], fg=self.settings.colors['fg']).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        tk.Entry(settings_frame, textvariable=self.settings.sessions_before_long_break, width=5, bg=self.settings.colors['bg'], fg=self.settings.colors['text']).grid(row=3, column=1, padx=5, pady=2)
        
        # Calendar
        self.create_calendar()
        
        # Streak tracking
        streak_frame = tk.LabelFrame(self.left_frame,
                                   text="Study Streak",
                                   bg=self.settings.colors['bg'],
                                   fg=self.settings.colors['fg'],
                                   font=('Arial', 10, 'bold'))
        streak_frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.streak_label = tk.Label(streak_frame,
                                   text="Current Streak: 0 days",
                                   bg=self.settings.colors['bg'],
                                   fg=self.settings.colors['fg'],
                                   font=('Arial', 10, 'bold'))
        self.streak_label.pack(pady=5)
        
        self.streak_goal = tk.Label(streak_frame,
                                  text=f"Goal: {self.settings.streak_goal_var.get()} days",
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'])
        self.streak_goal.pack(pady=5)
        
        # Progress bar for streak
        self.streak_progress = ttk.Progressbar(streak_frame, orient=tk.HORIZONTAL, length=200, mode='determinate', style="TProgressbar")
        self.streak_progress.pack(pady=5, fill=tk.X, padx=5)
        
        # Calculate streak
        self.calculate_streak()
    
    def create_calendar(self):
        """Create the calendar widget"""
        cal_frame = tk.LabelFrame(self.left_frame,
                                text="Study Calendar",
                                bg=self.settings.colors['bg'],
                                fg=self.settings.colors['fg'],
                                font=('Arial', 10, 'bold'))
        cal_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Month navigation
        nav_frame = tk.Frame(cal_frame, bg=self.settings.colors['bg'])
        nav_frame.pack(fill=tk.X)
        
        self.prev_month_btn = tk.Button(nav_frame, 
                                      text="◀", 
                                      command=self.prev_month,
                                      bg=self.settings.colors['bg'],
                                      fg=self.settings.colors['fg'],
                                      relief=tk.FLAT,
                                      font=('Arial', 10))
        self.prev_month_btn.pack(side=tk.LEFT, padx=5)
        
        # Month/Year display
        now = datetime.now()
        self.calendar_date = now
        self.month_year = tk.Label(nav_frame,
                                 text=f"{now.strftime('%B %Y')}",
                                 bg=self.settings.colors['bg'],
                                 fg=self.settings.colors['fg'],
                                 font=('Arial', 10, 'bold'))
        self.month_year.pack(side=tk.LEFT, expand=True)
        
        self.next_month_btn = tk.Button(nav_frame, 
                                      text="▶", 
                                      command=self.next_month,
                                      bg=self.settings.colors['bg'],
                                      fg=self.settings.colors['fg'],
                                      relief=tk.FLAT,
                                      font=('Arial', 10))
        self.next_month_btn.pack(side=tk.RIGHT, padx=5)
        
        # Days header
        days_frame = tk.Frame(cal_frame, bg=self.settings.colors['bg'])
        days_frame.pack(fill=tk.X)
        
        days = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        for i, day in enumerate(days):
            tk.Label(days_frame,
                   text=day,
                   bg=self.settings.colors['bg'],
                   fg=self.settings.colors['text'],
                   width=3).grid(row=0, column=i, padx=1, pady=1)
        
        # Calendar days
        self.cal_days_frame = tk.Frame(cal_frame, bg=self.settings.colors['bg'])
        self.cal_days_frame.pack(fill=tk.X)
    
    def create_center_panel(self):
        """Create the center panel with timer display and motivational elements"""
        # Timer display
        timer_frame = tk.Frame(self.center_frame, bg=self.settings.colors['bg'])
        timer_frame.pack(pady=10)
        
        self.time_display = tk.Label(timer_frame,
                                   text="00:00",
                                   font=('Arial', 48, 'bold'),
                                   bg=self.settings.colors['bg'],
                                   fg=self.settings.colors['fg'])
        self.time_display.pack()
        
        # Timer progress bar
        self.timer_progress = ttk.Progressbar(timer_frame, 
                                            orient=tk.HORIZONTAL, 
                                            length=300, 
                                            mode='determinate',
                                            style="TProgressbar")
        self.timer_progress.pack(fill=tk.X, pady=5)
        
        # Date and time
        self.date_time = tk.Label(self.center_frame,
                                text=self.get_datetime_str(),
                                font=('Arial', 12),
                                bg=self.settings.colors['bg'],
                                fg=self.settings.colors['fg'])
        self.date_time.pack()
        
        # Motivational quote
        self.quote_frame = tk.LabelFrame(self.center_frame,
                                       text="Today's Motivation",
                                       bg=self.settings.colors['bg'],
                                       fg=self.settings.colors['fg'],
                                       font=('Arial', 10, 'bold'))
        self.quote_frame.pack(fill=tk.X, pady=10)
        
        self.current_quote = random.choice(self.settings.motivational_quotes)
        self.quote_label = tk.Label(self.quote_frame,
                                  text=self.current_quote,
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'],
                                  wraplength=350,
                                  justify=tk.CENTER)
        self.quote_label.pack(pady=10, padx=10)
        
        tk.Button(self.quote_frame,
                text="New Quote",
                command=self.new_quote,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(pady=5)
        
        # Study image
        self.image_frame = tk.Frame(self.center_frame, bg=self.settings.colors['bg'])
        self.image_frame.pack(pady=10)
        
        # Load and display study image
        self.load_study_image()
        
        # Session counter
        self.session_frame = tk.Frame(self.center_frame, bg=self.settings.colors['bg'])
        self.session_frame.pack(pady=10)
        
        self.session_label = tk.Label(self.session_frame,
                                    text=f"SESSION NO:- {self.settings.session_count}",
                                    font=('Arial', 14, 'bold'),
                                    bg=self.settings.colors['bg'],
                                    fg=self.settings.colors['fg'])
        self.session_label.pack(side=tk.LEFT, padx=5)
        
        # Session indicators (circles showing completed/pending sessions)
        self.session_indicators_frame = tk.Frame(self.center_frame, bg=self.settings.colors['bg'])
        self.session_indicators_frame.pack(pady=5)
        
        self.session_indicators = []
    
    def load_study_image(self):
        """Load and display the study image"""
        # Clear any existing widgets in the image frame
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        try:
            # Check if custom study image is set
            custom_image_path = self.settings.custom_study_image.get()
            
            if custom_image_path and os.path.exists(custom_image_path):
                # Load custom image from file
                img_data = Image.open(custom_image_path)
                img_data = img_data.resize((250, 250), Image.LANCZOS)
                img = ImageTk.PhotoImage(img_data)
                
                img_label = tk.Label(self.image_frame,
                                   image=img,
                                   bg=self.settings.colors['bg'])
                img_label.image = img  # Keep a reference to prevent garbage collection
                img_label.pack(pady=10)
            else:
                # Try to load default image from URL
                try:
                    response = requests.get("https://hebbkx1anhila5yf.public.blob.vercel-storage.com/Post2-tZfCun4BBdFUBdGHLDq3XeBP2UHwFc.png")
                    img_data = Image.open(BytesIO(response.content))
                    img_data = img_data.resize((250, 250), Image.LANCZOS)
                    img = ImageTk.PhotoImage(img_data)
                    
                    img_label = tk.Label(self.image_frame,
                                       image=img,
                                       bg=self.settings.colors['bg'])
                    img_label.image = img
                    img_label.pack(pady=10)
                except Exception as e:
                    print(f"Error loading image from URL: {e}")
                    # Try to load local default image
                    default_img_path = os.path.join("resources", "images", "study_image.png")
                    if os.path.exists(default_img_path):
                        img_data = Image.open(default_img_path)
                        img_data = img_data.resize((250, 250), Image.LANCZOS)
                        img = ImageTk.PhotoImage(img_data)
                        
                        img_label = tk.Label(self.image_frame,
                                           image=img,
                                           bg=self.settings.colors['bg'])
                        img_label.image = img
                        img_label.pack(pady=10)
                    else:
                        # Fallback to text
                        tk.Label(self.image_frame,
                               text="Study Time!",
                               font=('Arial', 24, 'bold'),
                               bg=self.settings.colors['bg'],
                               fg=self.settings.colors['fg']).pack(pady=10)
        except Exception as e:
            print(f"Error loading study image: {e}")
            # Fallback to text
            tk.Label(self.image_frame,
                   text="Study Time!",
                   font=('Arial', 24, 'bold'),
                   bg=self.settings.colors['bg'],
                   fg=self.settings.colors['fg']).pack(pady=10)
    
    def create_right_panel(self):
        """Create the right panel with app locker, website blocker, and to-do list"""
        # App locker
        locker_frame = tk.LabelFrame(self.right_frame,
                                   text="App Locker",
                                   bg=self.settings.colors['bg'],
                                   fg=self.settings.colors['fg'],
                                   font=('Arial', 10, 'bold'))
        locker_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(locker_frame,
               text="Select app:",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack(anchor=tk.W, padx=5)
        
        self.app_var = tk.StringVar()
        app_combo = ttk.Combobox(locker_frame,
                               textvariable=self.app_var,
                               values=self.settings.app_list)
        app_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Add custom app entry
        app_frame = tk.Frame(locker_frame, bg=self.settings.colors['bg'])
        app_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.custom_app = tk.Entry(app_frame, bg=self.settings.colors['bg'], fg=self.settings.colors['text'])
        self.custom_app.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(app_frame,
                text="Add App",
                command=self.add_custom_app,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Lock/Unlock buttons
        btn_frame = tk.Frame(locker_frame, bg=self.settings.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.lock_button = tk.Button(btn_frame,
                                   text="Lock App",
                                   command=self.lock_app,
                                   bg=self.settings.colors['button'],
                                   fg=self.settings.colors['text'])
        self.lock_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.unlock_button = tk.Button(btn_frame,
                                     text="Unlock App",
                                     command=self.unlock_app,
                                     bg=self.settings.colors['button'],
                                     fg=self.settings.colors['text'])
        self.unlock_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Locked apps list
        self.locked_apps_list = tk.Listbox(locker_frame,
                                         bg=self.settings.colors['bg'],
                                         fg=self.settings.colors['text'],
                                         selectbackground=self.settings.colors['accent'],
                                         height=5)
        self.locked_apps_list.pack(fill=tk.X, padx=5, pady=5)
        
        # Blocked websites
        sites_frame = tk.LabelFrame(self.right_frame,
                                  text="Blocked Websites",
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'],
                                  font=('Arial', 10, 'bold'))
        sites_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(sites_frame,
               text="Select website:",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack(anchor=tk.W, padx=5)
        
        self.website_var = tk.StringVar()
        web_combo = ttk.Combobox(sites_frame,
                                textvariable=self.website_var,
                                values=self.settings.website_list)
        web_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Add custom website entry
        site_frame = tk.Frame(sites_frame, bg=self.settings.colors['bg'])
        site_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.custom_website = tk.Entry(site_frame, bg=self.settings.colors['bg'], fg=self.settings.colors['text'])
        self.custom_website.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(site_frame,
                text="Add Website",
                command=self.block_website,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Block/Unblock buttons
        site_btn_frame = tk.Frame(sites_frame, bg=self.settings.colors['bg'])
        site_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.block_button = tk.Button(site_btn_frame,
                                    text="Block Website",
                                    command=self.block_website,
                                    bg=self.settings.colors['button'],
                                    fg=self.settings.colors['text'])
        self.block_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        self.unblock_button = tk.Button(site_btn_frame,
                                      text="Unblock Website",
                                      command=self.unblock_website,
                                      bg=self.settings.colors['button'],
                                      fg=self.settings.colors['text'])
        self.unblock_button.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Blocked websites list
        self.blocked_sites_list = tk.Listbox(sites_frame,
                                           bg=self.settings.colors['bg'],
                                           fg=self.settings.colors['text'],
                                           selectbackground=self.settings.colors['accent'],
                                           height=5)
        self.blocked_sites_list.pack(fill=tk.X, padx=5, pady=5)

        # To-Do List
        todo_frame = tk.LabelFrame(self.right_frame,
                                 text="To-Do List",
                                 bg=self.settings.colors['bg'],
                                 fg=self.settings.colors['fg'],
                                 font=('Arial', 10, 'bold'))
        todo_frame.pack(fill=tk.X, pady=5)
        
        # Task entry
        self.task_entry = tk.Entry(todo_frame,
                                bg=self.settings.colors['bg'],
                                fg=self.settings.colors['text'],
                                insertbackground=self.settings.colors['text'])
        self.task_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Add task button and priority selection
        task_control_frame = tk.Frame(todo_frame, bg=self.settings.colors['bg'])
        task_control_frame.pack(fill=tk.X, padx=5, pady=2)
        
        self.priority_var = tk.StringVar(value="Normal")
        priority_combo = ttk.Combobox(task_control_frame, 
                                     textvariable=self.priority_var, 
                                     values=["High", "Normal", "Low"],
                                     width=8)
        priority_combo.pack(side=tk.LEFT, padx=2)
        
        tk.Button(task_control_frame,
                text="Add Task",
                command=self.add_task,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Task list with scrollbar
        todo_list_frame = tk.Frame(todo_frame, bg=self.settings.colors['bg'])
        todo_list_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.todo_listbox = tk.Listbox(todo_list_frame,
                                    bg=self.settings.colors['bg'],
                                    fg=self.settings.colors['text'],
                                    selectbackground=self.settings.colors['accent'],
                                    height=8)
        self.todo_listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        todo_scrollbar = tk.Scrollbar(todo_list_frame, orient=tk.VERTICAL)
        todo_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.todo_listbox.config(yscrollcommand=todo_scrollbar.set)
        todo_scrollbar.config(command=self.todo_listbox.yview)
        
        # Task buttons
        task_btn_frame = tk.Frame(todo_frame, bg=self.settings.colors['bg'])
        task_btn_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Button(task_btn_frame,
                text="Complete Task",
                command=self.complete_task,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        tk.Button(task_btn_frame,
                text="Delete Task",
                command=self.delete_task,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    def create_minimized_window(self):
        """Create a minimized window for when the main window is minimized"""
        self.minimized_window = tk.Toplevel(self.app.root)
        self.minimized_window.geometry("200x130")
        self.minimized_window.withdraw()
        self.minimized_window.overrideredirect(True)
        self.minimized_window.attributes('-topmost', True)
        self.minimized_window.configure(bg=self.settings.colors['bg'])
        
        # Add a border to make it more visible
        self.minimized_window.configure(highlightbackground=self.settings.colors['accent'], 
                                      highlightcolor=self.settings.colors['accent'], 
                                      highlightthickness=2)
        
        # Minimized window contents
        self.minimized_time_display = tk.Label(self.minimized_window,
                                             text="00:00",
                                             font=('Arial', 20, 'bold'),
                                             bg=self.settings.colors['bg'],
                                             fg=self.settings.colors['fg'])
        self.minimized_time_display.pack(pady=5)
        
        self.minimized_session_label = tk.Label(self.minimized_window,
                                              text=f"SESSION NO:- {self.settings.session_count}",
                                              font=('Arial', 10, 'bold'),
                                              bg=self.settings.colors['bg'],
                                              fg=self.settings.colors['fg'])
        self.minimized_session_label.pack(pady=5)
        
        self.minimized_phase_label = tk.Label(self.minimized_window,
                                            text="Ready",
                                            bg=self.settings.colors['bg'],
                                            fg=self.settings.colors['fg'])
        self.minimized_phase_label.pack(pady=5)
        
        self.minimized_window.bind("<Double-Button-1>", self.expand_window)
        self.minimized_window.bind("<Button-1>", self.start_move)
        self.minimized_window.bind("<ButtonRelease-1>", self.stop_move)
        self.minimized_window.bind("<B1-Motion>", self.do_move)
    
    def start_move(self, event):
        """Start moving the minimized window"""
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        """Stop moving the minimized window"""
        self.x = None
        self.y = None

    def do_move(self, event):
        """Move the minimized window"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.minimized_window.winfo_x() + deltax
        y = self.minimized_window.winfo_y() + deltay
        self.minimized_window.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        """Minimize the main window and show the minimized window"""
        self.app.root.withdraw()
        self.minimized_window.deiconify()

    def expand_window(self, event=None):
        """Expand the minimized window back to the main window"""
        self.minimized_window.withdraw()
        self.app.root.deiconify()
    
    # Timer methods
    def start_session(self):
        """Start a new focus session"""
        try:
            focus = int(self.settings.focus_time.get())
            short = int(self.settings.short_break.get())
            long = int(self.settings.long_break.get())
            sessions = int(self.settings.sessions_before_long_break.get())
            
            if not (0 < focus <= 120 and 0 < short <= 30 and 0 < long <= 60 and 0 < sessions <= 10):
                raise ValueError("Invalid time values")
            
            self.is_timer_running = True
            self.paused = False
            self.start_time = time.time()
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.DISABLED)
            
            # Auto-block if enabled
            if self.settings.auto_block.get():
                for app in self.settings.locked_apps:
                    block_application(app)
            
            # Change button states based on strict mode
            if self.settings.strict_mode.get():
                self.lock_button.config(state=tk.DISABLED)
                self.unlock_button.config(state=tk.DISABLED)
                self.block_button.config(state=tk.DISABLED)
                self.unblock_button.config(state=tk.DISABLED)
            
            # Update session indicators
            self.update_session_indicators()
            
            # Update current quote
            self.current_quote = random.choice(self.settings.motivational_quotes)
            self.quote_label.config(text=self.current_quote)
            
            # Calculate total seconds for the timer
            total_seconds = focus * 60
            self.remaining_seconds = total_seconds
            
            # Set up progress bar
            self.timer_progress['maximum'] = total_seconds
            self.timer_progress['value'] = 0
            
            # Start the timer thread
            self.current_timer_thread = threading.Thread(
                target=self.run_timer,
                args=(focus, short, long, sessions),
                daemon=True
            )
            self.current_timer_thread.start()
            
            # Show desktop notification if enabled
            if self.settings.desktop_notifications.get():
                show_notification("Study Session Started", "Your focus time has begun. Stay focused!")
            
            # Play start sound if enabled
            if self.settings.sound_notifications.get() and self.settings.start_sound_path.get():
                try:
                    import pygame
                    sound = pygame.mixer.Sound(self.settings.start_sound_path.get())
                    sound.set_volume(0 if self.settings.is_muted.get() else self.settings.volume_level.get() / 100.0)
                    sound.play()
                except Exception as e:
                    print(f"Error playing start sound: {e}")
            
            # Play background music if available
            if self.settings.sound_notifications.get() and self.settings.background_music_path.get():
                try:
                    import pygame
                    pygame.mixer.music.load(self.settings.background_music_path.get())
                    pygame.mixer.music.set_volume(0 if self.settings.is_muted.get() else self.settings.volume_level.get() / 100.0)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                except Exception as e:
                    print(f"Error playing background music: {e}")
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid times (1-120 min for focus, 1-30 min for breaks, 1-10 sessions)")
    
    def pause_resume_session(self):
        """Pause or resume the current timer session"""
        if self.is_timer_running:
            if self.paused:
                # Resume the timer
                self.paused = False
                self.pause_button.config(text="Pause")
                
                # Resume background music if it was playing
                if self.settings.sound_notifications.get() and self.settings.background_music_path.get():
                    import pygame
                    pygame.mixer.music.unpause()
                
                # Show notification
                if self.settings.desktop_notifications.get():
                    show_notification("Session Resumed", "Your focus time continues. Stay focused!")
            else:
                # Pause the timer
                self.paused = True
                self.pause_button.config(text="Resume")
                
                # Pause background music
                import pygame
                pygame.mixer.music.pause()
                
                # Show notification
                if self.settings.desktop_notifications.get():
                    show_notification("Session Paused", "Your focus time is paused. Resume when ready.")
    
    def stop_session(self):
        """Stop the current session"""
        if self.is_timer_running:
            # Calculate total focus time for this session
            end_time = time.time()
            session_time = int(end_time - self.start_time)
            
            # Update statistics
            self.update_daily_stats(session_time)
            
            # Stop the timer
            self.is_timer_running = False
            self.paused = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, text="Pause")
            self.reset_button.config(state=tk.NORMAL)
            self.lock_button.config(state=tk.NORMAL)
            self.unlock_button.config(state=tk.NORMAL)
            self.block_button.config(state=tk.NORMAL)
            self.unblock_button.config(state=tk.NORMAL)
            
            # Stop background music
            import pygame
            pygame.mixer.music.stop()
            
            # Unblock all apps and websites if not in strict mode
            if not self.settings.strict_mode.get():
                self.unlock_all_apps()
                self.unblock_all_websites()
            
            # Save data
            self.settings.save_settings()
    
    def reset_session(self):
        """Reset the session counter and timer"""
        self.stop_session()
        self.settings.session_count = 1
        self.session_label.config(text=f"SESSION NO:- {self.settings.session_count}")
        self.time_display.config(text="00:00")
        self.timer_progress['value'] = 0
        self.update_session_indicators()
    
    def run_timer(self, focus, short, long, sessions_before_long):
        """Run the timer with focus and break periods"""
        total_seconds = focus * 60
        self.remaining_seconds = total_seconds
        
        while self.is_timer_running:
            # Focus period
            self.run_countdown(total_seconds, "Focus")
            if not self.is_timer_running:
                break
            
            # Break period
            break_time = long if self.settings.session_count % sessions_before_long == 0 else short
            break_type = "Long Break" if self.settings.session_count % sessions_before_long == 0 else "Short Break"
            break_seconds = break_time * 60
            
            # Show notification
            if self.settings.desktop_notifications.get():
                show_notification("Break Time", f"Time for a {break_type.lower()}! ({break_time} minutes)")
            
            # Play end sound
            if self.settings.sound_notifications.get() and self.settings.end_sound_path.get():
                try:
                    import pygame
                    sound = pygame.mixer.Sound(self.settings.end_sound_path.get())
                    sound.set_volume(0 if self.settings.is_muted.get() else self.settings.volume_level.get() / 100.0)
                    sound.play()
                except Exception as e:
                    print(f"Error playing end sound: {e}")
            
            # Stop background music during break
            import pygame
            pygame.mixer.music.stop()
            
            # Enable controls during break
            self.lock_button.config(state=tk.NORMAL)
            self.unlock_button.config(state=tk.NORMAL)
            self.block_button.config(state=tk.NORMAL)
            self.unblock_button.config(state=tk.NORMAL)
            
            # Reset progress bar for break
            self.timer_progress['maximum'] = break_seconds
            self.timer_progress['value'] = 0
            
            self.run_countdown(break_seconds, break_type)
            
            if self.is_timer_running:
                self.settings.session_count += 1
                self.session_label.config(text=f"SESSION NO:- {self.settings.session_count}")
                self.update_session_indicators()
                
                # Reset progress bar for next focus session
                self.timer_progress['maximum'] = total_seconds
                self.timer_progress['value'] = 0
                
                # Show notification
                if self.settings.desktop_notifications.get():
                    show_notification("Focus Time", "Break is over. Time to focus!")
                
                # Play start sound
                if self.settings.sound_notifications.get() and self.settings.start_sound_path.get():
                    try:
                        import pygame
                        sound = pygame.mixer.Sound(self.settings.start_sound_path.get())
                        sound.set_volume(0 if self.settings.is_muted.get() else self.settings.volume_level.get() / 100.0)
                        sound.play()
                    except Exception as e:
                        print(f"Error playing start sound: {e}")
                
                # Resume background music for focus session
                if self.settings.sound_notifications.get() and self.settings.background_music_path.get():
                    try:
                        import pygame
                        pygame.mixer.music.load(self.settings.background_music_path.get())
                        pygame.mixer.music.set_volume(0 if self.settings.is_muted.get() else self.settings.volume_level.get() / 100.0)
                        pygame.mixer.music.play(-1)  # Loop indefinitely
                    except Exception as e:
                        print(f"Error playing background music: {e}")
                
                # Disable controls during focus based on strict mode
                if self.settings.strict_mode.get():
                    self.lock_button.config(state=tk.DISABLED)
                    self.unlock_button.config(state=tk.DISABLED)
                    self.block_button.config(state=tk.DISABLED)
                    self.unblock_button.config(state=tk.DISABLED)
    
    def run_countdown(self, seconds, phase_type="Focus"):
        """Run the countdown timer"""
        self.remaining_seconds = seconds
        
        while self.remaining_seconds > 0 and self.is_timer_running:
            if not self.paused:
                minutes, secs = divmod(int(self.remaining_seconds), 60)
                time_text = f"{minutes:02d}:{secs:02d}"
                self.time_display.config(text=time_text)
                self.minimized_time_display.config(text=time_text)
                self.minimized_session_label.config(text=f"SESSION NO:- {self.settings.session_count}")
                self.minimized_phase_label.config(text=phase_type)
                
                # Update progress bar
                self.timer_progress['value'] = self.timer_progress['maximum'] - self.remaining_seconds
                
                self.app.root.update()
                time.sleep(1)  # Sleep for 1 second
                self.remaining_seconds -= 1
            else:
                # When paused, just update UI and wait
                self.app.root.update()
                time.sleep(0.1)
        
        # Ensure we display exactly 00:00 at the end
        if self.is_timer_running and not self.paused:
            self.time_display.config(text="00:00")
            self.timer_progress['value'] = self.timer_progress['maximum']
            
            # Play end sound
            if self.settings.sound_notifications.get() and self.settings.end_sound_path.get():
                try:
                    import pygame
                    sound = pygame.mixer.Sound(self.settings.end_sound_path.get())
                    sound.set_volume(0 if self.settings.is_muted.get() else self.settings.volume_level.get() / 100.0)
                    sound.play()
                except Exception as e:
                    print(f"Error playing end sound: {e}")
            
            self.app.root.attributes('-topmost', True)
            messagebox.showinfo("Time's up!", f"The {phase_type.lower()} timer has finished.")
            self.app.root.attributes('-topmost', False)
    
    # App and website blocking methods
    def lock_app(self):
        """Lock an application to prevent it from running"""
        app = self.app_var.get()
        if app and app not in self.settings.locked_apps:
            self.settings.locked_apps.append(app)
            self.locked_apps_list.insert(tk.END, app)
            block_application(app)
            self.settings.save_settings()

    def add_custom_app(self):
        """Add a custom application to the app list"""
        app = self.custom_app.get().strip()
        if app and app not in self.settings.app_list:
            self.settings.app_list.append(app)
            self.app_var.set(app)
            self.custom_app.delete(0, tk.END)
            self.settings.save_settings()

    def unlock_app(self):
        """Unlock a previously locked application"""
        selection = self.locked_apps_list.curselection()
        if selection:
            app = self.locked_apps_list.get(selection)
            self.settings.locked_apps.remove(app)
            self.locked_apps_list.delete(selection)
            unblock_application(app)
            self.settings.save_settings()
    
    def unlock_all_apps(self):
        """Unlock all locked applications"""
        self.settings.locked_apps.clear()
        self.locked_apps_list.delete(0, tk.END)
        self.settings.save_settings()
    
    def block_website(self):
        """Block a website to prevent access"""
        site = self.website_var.get() or self.custom_website.get().strip()
        if site and site not in self.settings.blocked_websites:
            try:
                block_website(site)
                self.settings.blocked_websites.append(site)
                self.blocked_sites_list.insert(tk.END, site)
                self.settings.save_settings()
                self.custom_website.delete(0, tk.END)
            except PermissionError:
                messagebox.showwarning("Permission Error", 
                                     "Need admin privileges to block websites.\n\nTry running the application as administrator.")

    def unblock_website(self):
        """Unblock a previously blocked website"""
        selection = self.blocked_sites_list.curselection()
        if selection:
            site = self.blocked_sites_list.get(selection)
            try:
                unblock_website(site)
                self.settings.blocked_websites.remove(site)
                self.blocked_sites_list.delete(selection)
                self.settings.save_settings()
            except PermissionError:
                messagebox.showwarning("Permission Error", 
                                     "Need admin privileges to unblock websites.\n\nTry running the application as administrator.")
    
    def unblock_all_websites(self):
        """Unblock all blocked websites"""
        hosts_path = get_hosts_path()
        try:
            with open(hosts_path, 'r') as hosts_file:
                lines = hosts_file.readlines()
            
            with open(hosts_path, 'w') as hosts_file:
                for line in lines:
                    if not any(site in line for site in self.settings.blocked_websites):
                        hosts_file.write(line)
            
            self.settings.blocked_websites.clear()
            self.blocked_sites_list.delete(0, tk.END)
            self.settings.save_settings()
        except PermissionError:
            messagebox.showwarning("Permission Error", 
                                 "Need admin privileges to unblock websites.\n\nTry running the application as administrator.")
    
    # Task management methods
    def add_task(self):
        """Add a task to the to-do list"""
        task = self.task_entry.get().strip()
        priority = self.priority_var.get()
        
        if task:
            # Format with priority
            task_with_priority = f"[{priority}] {task}"
            self.settings.todo_list.append(task_with_priority)
            
            # Color code based on priority
            if priority == "High":
                self.todo_listbox.insert(tk.END, task_with_priority)
                self.todo_listbox.itemconfig(tk.END, {'fg': '#EF4444'})  # Red for high priority
            elif priority == "Low":
                self.todo_listbox.insert(tk.END, task_with_priority)
                self.todo_listbox.itemconfig(tk.END, {'fg': '#10B981'})  # Green for low priority
            else:
                self.todo_listbox.insert(tk.END, task_with_priority)
            
            self.task_entry.delete(0, tk.END)
            self.settings.save_settings()

    def complete_task(self):
        """Mark a task as complete"""
        selection = self.todo_listbox.curselection()
        if selection:
            task = self.todo_listbox.get(selection)
            self.settings.todo_list.remove(task)
            self.todo_listbox.delete(selection)
            self.settings.completed_tasks.append(task)
            self.settings.save_settings()
            
            # Show notification
            if self.settings.desktop_notifications.get():
                show_notification("Task Completed", "Great job! Keep up the good work!")

    def delete_task(self):
        """Delete a task from the to-do list"""
        selection = self.todo_listbox.curselection()
        if selection:
            task = self.todo_listbox.get(selection)
            self.settings.todo_list.remove(task)
            self.todo_listbox.delete(selection)
            self.settings.save_settings()
    
    def new_quote(self):
        """Display a new motivational quote"""
        self.current_quote = random.choice(self.settings.motivational_quotes)
        self.quote_label.config(text=self.current_quote)
    
    # Calendar methods
    def prev_month(self):
        """Navigate to previous month in calendar"""
        year = self.calendar_date.year
        month = self.calendar_date.month - 1
        
        if month < 1:
            month = 12
            year -= 1
            
        self.calendar_date = self.calendar_date.replace(year=year, month=month)
        self.update_calendar()
        
    def next_month(self):
        """Navigate to next month in calendar"""
        year = self.calendar_date.year
        month = self.calendar_date.month + 1
        
        if month > 12:
            month = 1
            year += 1
            
        self.calendar_date = self.calendar_date.replace(year=year, month=month)
        self.update_calendar()
    
    def update_calendar(self):
        """Update the calendar display"""
        # Clear existing calendar
        for widget in self.cal_days_frame.winfo_children():
            widget.destroy()
        
        # Update month/year display
        self.month_year.config(text=f"{self.calendar_date.strftime('%B %Y')}")
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.calendar_date.year, self.calendar_date.month)
        
        # Highlight days with completed study sessions
        study_days = self.get_study_days()
        today = datetime.now().date()
        
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    # Check if this day had study session
                    day_str = f"{self.calendar_date.year}-{self.calendar_date.month:02d}-{day:02d}"
                    
                    # Check if this is today
                    is_today = (day == today.day and 
                               self.calendar_date.month == today.month and 
                               self.calendar_date.year == today.year)
                    
                    if is_today:
                        bg_color = self.settings.colors['accent']
                        fg_color = self.settings.colors['text']
                    elif day_str in study_days:
                        bg_color = self.settings.colors['button']
                        fg_color = self.settings.colors['text']
                    else:
                        bg_color = self.settings.colors['bg']
                        fg_color = self.settings.colors['fg']
                    
                    day_label = tk.Label(self.cal_days_frame,
                                       text=str(day),
                                       bg=bg_color,
                                       fg=fg_color,
                                       width=3)
                    day_label.grid(row=week_num, column=day_num, padx=1, pady=1)
                    
                    # Add tooltip for study time on this day
                    if day_str in study_days:
                        study_time = self.settings.daily_stats.get(day_str, 0)
                        hours, remainder = divmod(study_time, 3600)
                        minutes = remainder // 60
                        self.create_tooltip(day_label, f"Study time: {hours}h {minutes}m")
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def enter(event):
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            
            # Create a toplevel window
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            label = tk.Label(self.tooltip, text=text, bg=self.settings.colors['accent'], fg=self.settings.colors['text'],
                           relief=tk.SOLID, borderwidth=1, padx=5, pady=2)
            label.pack()
            
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def get_study_days(self):
        """Return list of days with completed study sessions"""
        return list(self.settings.daily_stats.keys())
    
    # Statistics methods
    def update_daily_stats(self, session_time):
        """Update daily statistics with completed session time"""
        today = datetime.now().date().strftime("%Y-%m-%d")
        
        if today in self.settings.daily_stats:
            self.settings.daily_stats[today] += session_time
        else:
            self.settings.daily_stats[today] = session_time
        
        # Update streak info
        self.calculate_streak()
        
        # Update calendar display
        self.update_calendar()
    
    def calculate_streak(self):
        """Calculate the current study streak"""
        today = datetime.now().date()
        streak = 0
        current_date = today
        
        # Count backwards from today
        while True:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in self.settings.daily_stats and self.settings.daily_stats[date_str] >= 10 * 60:  # At least 10 minutes
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        # Update streak display
        self.streak_label.config(text=f"Current Streak: {streak} days")
        
        # Update streak progress bar
        streak_goal = int(self.settings.streak_goal_var.get())
        progress = min(100, int((streak / streak_goal) * 100))
        self.streak_progress['value'] = progress
    
    def update_session_indicators(self):
        """Update session indicator circles"""
        # Update session indicator circles
        sessions_per_day = int(self.settings.sessions_before_long_break.get())
        
        # Clear existing indicators
        for indicator in self.session_indicators:
            indicator.destroy()
        
        self.session_indicators = []
        
        # Create new indicators
        for i in range(sessions_per_day):
            indicator = tk.Canvas(self.session_indicators_frame, width=20, height=20, bg=self.settings.colors['bg'], highlightthickness=0)
            if i+1 < self.settings.session_count:
                indicator.create_oval(2, 2, 18, 18, fill=self.settings.colors['fg'], outline="")
            else:
                indicator.create_oval(2, 2, 18, 18, fill=self.settings.colors['bg'], outline=self.settings.colors['fg'])
            indicator.pack(side=tk.LEFT, padx=5)
            self.session_indicators.append(indicator)
    
    def get_datetime_str(self):
        """Get formatted date and time string"""
        now = datetime.now()
        return f"{now.strftime('%d %b %Y')}\n{now.strftime('%I:%M %p')}"
    
    def start_monitoring(self):
        """Start the app monitoring thread"""
        self.monitor_thread = threading.Thread(target=self.monitor_apps, daemon=True)
        self.monitor_thread.start()
    
    def monitor_apps(self):
        """Monitor and block apps that should be locked"""
        while True:
            if self.is_timer_running and not self.paused and self.settings.locked_apps:
                for proc in psutil.process_iter(['name']):
                    try:
                        for app in self.settings.locked_apps:
                            if app.lower() in proc.info['name'].lower():
                                proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
            time.sleep(1)
    
    def adjust_layout_for_size(self, width, height):
        """Adjust layout based on window dimensions"""
        # For smaller windows, adjust the layout
        if width < 900:
            # Compact mode adjustments
            self.center_frame.pack_configure(padx=5)
            self.left_frame.pack_configure(padx=5)
            self.right_frame.pack_configure(padx=5)
        else:
            # Regular mode adjustments
            self.center_frame.pack_configure(padx=10)
            self.left_frame.pack_configure(padx=10)
            self.right_frame.pack_configure(padx=10)
    
    def apply_theme(self):
        """Apply the current theme to all UI elements"""
        # Update frames
        for frame in [self.frame, self.main_container, self.left_frame, 
                     self.center_frame, self.right_frame]:
            frame.configure(bg=self.settings.colors['bg'])
        
        # Update all widgets
        self.update_widget_colors(self.frame)
        
        # Update minimized window
        if hasattr(self, 'minimized_window'):
            self.minimized_window.configure(bg=self.settings.colors['bg'])
            self.minimized_window.configure(highlightbackground=self.settings.colors['accent'], 
                                          highlightcolor=self.settings.colors['accent'])
            
            for widget in self.minimized_window.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=self.settings.colors['bg'], fg=self.settings.colors['fg'])
    
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
