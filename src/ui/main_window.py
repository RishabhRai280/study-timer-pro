"""
Main window implementation for Study Timer Pro
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
import json
import pygame

from ui.timer_tab import TimerTab
from ui.analytics_tab import AnalyticsTab
from ui.settings_tab import SettingsTab
from utils.settings import Settings
from utils.notifications import NotificationManager
from PIL import Image, ImageTk

class StudyTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Timer Pro")
        self.root.geometry("1100x800")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        
        # Initialize pygame mixer for sound playback
        pygame.mixer.init()
        
        # Load settings
        self.settings = Settings()
        self.settings.load_settings()
        
        # Set app icon
        self.set_app_icon()
        
        # Create notification manager
        self.notification_manager = NotificationManager()
        
        # Setup UI
        self.setup_notebook()
        self.create_menu()
        
        # Override the close button behavior
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Bind window resize event
        self.root.bind("<Configure>", self.on_window_resize)
        
        # Apply background image if set
        self.apply_background_image()
    
    def set_app_icon(self):
        """Set the application icon"""
        try:
            # Check for custom app icon
            custom_icon_path = self.settings.custom_app_icon.get()
            if custom_icon_path and os.path.exists(custom_icon_path):
                icon_photo = ImageTk.PhotoImage(Image.open(custom_icon_path))
                self.root.iconphoto(True, icon_photo)
            else:
                # Use default icon
                icon_path = os.path.join("resources", "images", "app_icon.png")
                if os.path.exists(icon_path):
                    icon_photo = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(True, icon_photo)
        except Exception as e:
            print(f"Error loading icon: {e}")
    
    def setup_notebook(self):
        """Set up the main notebook with tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.timer_tab = TimerTab(self.notebook, self)
        self.analytics_tab = AnalyticsTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        
        # Add tabs to notebook
        self.notebook.add(self.timer_tab.frame, text="Timer")
        self.notebook.add(self.analytics_tab.frame, text="Analytics")
        self.notebook.add(self.settings_tab.frame, text="Settings")
    
    def create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export Statistics", command=self.export_statistics)
        file_menu.add_command(label="Import Settings", command=self.import_settings)
        file_menu.add_command(label="Export Settings", command=self.export_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        for theme in self.settings.color_schemes:
            theme_menu.add_command(label=theme, command=lambda t=theme: self.change_theme(t))
        view_menu.add_cascade(label="Themes", menu=theme_menu)
        
        view_menu.add_command(label="Custom Colors", command=self.customize_colors)
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Options menu
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_checkbutton(label="Enable Sounds", variable=self.settings.sound_enabled)
        options_menu.add_command(label="Pomodoro Settings", command=self.show_pomodoro_settings)
        options_menu.add_command(label="Reset Statistics", command=self.reset_statistics)
        menubar.add_cascade(label="Options", menu=options_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=lambda: self.open_documentation())
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def on_window_resize(self, event):
        """Handle window resize events to adjust UI elements"""
        # Only respond to root window resizes, not child widgets
        if event.widget == self.root:
            # Update layout if needed for responsive design
            width, height = event.width, event.height
            self.timer_tab.adjust_layout_for_size(width, height)
            self.analytics_tab.adjust_layout_for_size(width, height)
            
            # Reapply background image to fit new size
            if self.settings.background_image_path.get():
                self.apply_background_image()
    
    def apply_background_image(self):
        """Apply the selected background image"""
        # Remove existing background if any
        if hasattr(self, 'bg_image_label'):
            self.bg_image_label.destroy()
        
        # If a background image is set, apply it
        bg_path = self.settings.background_image_path.get()
        if bg_path and os.path.exists(bg_path):
            try:
                from PIL import Image, ImageTk
                
                # Load and resize image to fit window
                image = Image.open(bg_path)
                width, height = self.root.winfo_width(), self.root.winfo_height()
                
                # If window hasn't been drawn yet, use default size
                if width <= 1:
                    width, height = 1100, 700
                
                image = image.resize((width, height), Image.LANCZOS)
                bg_image = ImageTk.PhotoImage(image)
                
                # Create label with image
                self.bg_image_label = tk.Label(self.root, image=bg_image)
                self.bg_image_label.image = bg_image  # Keep a reference
                self.bg_image_label.place(x=0, y=0, relwidth=1, relheight=1)
                
                # Move notebook to top
                self.notebook.lift()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply background image: {e}")
    
    def change_theme(self, theme_name):
        """Change the application theme"""
        if theme_name in self.settings.color_schemes:
            self.settings.current_theme = theme_name
            self.settings.colors = self.settings.color_schemes[theme_name]
            self.apply_theme()
    
    def apply_theme(self):
        """Apply the current theme to all UI elements"""
        # Update root and notebook
        self.root.configure(bg=self.settings.colors['bg'])
        
        # Update tabs
        self.timer_tab.apply_theme()
        self.analytics_tab.apply_theme()
        self.settings_tab.apply_theme()
        
        # Update notebook style
        style = ttk.Style()
        style.configure('TNotebook', background=self.settings.colors['bg'])
        style.configure('TNotebook.Tab', background=self.settings.colors['button'], 
                       foreground=self.settings.colors['text'],
                       padding=[10, 2])
        style.map('TNotebook.Tab', 
                 background=[('selected', self.settings.colors['accent']), 
                            ('!selected', self.settings.colors['button'])],
                 foreground=[('selected', self.settings.colors['text']), 
                            ('!selected', self.settings.colors['text'])])
        
        # Update progress bar style
        style.configure("TProgressbar", 
                       background=self.settings.colors['accent'],
                       troughcolor=self.settings.colors['bg'],
                       borderwidth=0,
                       thickness=10)
    
    def customize_colors(self):
        """Allow user to customize theme colors"""
        from tkinter import colorchooser
        
        color = colorchooser.askcolor(
            initialcolor=self.settings.colors['accent'], 
            title="Choose Accent Color"
        )[1]
        
        if color:
            # Create a custom theme based on current theme
            custom_colors = self.settings.color_schemes.get(self.settings.current_theme).copy()
            custom_colors['accent'] = color
            custom_colors['button'] = color
            self.settings.color_schemes['Custom'] = custom_colors
            self.change_theme('Custom')
    
    def export_statistics(self):
        """Export statistics to a CSV file"""
        from tkinter import filedialog
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Statistics"
            )
            if filename:
                with open(filename, 'w') as f:
                    f.write("Date,Study Time (minutes),Tasks Completed\n")
                    for date, seconds in self.settings.daily_stats.items():
                        minutes = seconds // 60
                        f.write(f"{date},{minutes},0\n")  # We don't track tasks by date
                messagebox.showinfo("Export", "Statistics exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export statistics: {e}")
    
    def import_settings(self):
        """Import settings from a JSON file"""
        from tkinter import filedialog
        
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Import Settings"
            )
            if filename:
                self.settings.import_settings(filename)
                self.apply_theme()
                messagebox.showinfo("Import", "Settings imported successfully!")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import settings: {e}")
    
    def export_settings(self):
        """Export settings to a JSON file"""
        from tkinter import filedialog
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Export Settings"
            )
            if filename:
                self.settings.export_settings(filename)
                messagebox.showinfo("Export", "Settings exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export settings: {e}")
    
    def show_pomodoro_settings(self):
        """Show the Pomodoro settings tab"""
        self.notebook.select(2)  # Select the Settings tab
    
    def reset_statistics(self):
        """Reset all statistics data"""
        if messagebox.askyesno("Reset Statistics", 
                              "Are you sure you want to reset all statistics? This cannot be undone."):
            self.settings.daily_stats = {}
            self.settings.completed_tasks = []
            self.analytics_tab.update_statistics_display()
            self.timer_tab.calculate_streak()
            self.settings.save_settings()
            messagebox.showinfo("Reset", "Statistics have been reset.")
    
    def open_documentation(self):
        """Open the user documentation"""
        import webbrowser
        doc_path = os.path.join("docs", "user_guide.md")
        
        if os.path.exists(doc_path):
            webbrowser.open(f"file://{os.path.abspath(doc_path)}")
        else:
            webbrowser.open("https://github.com/RishabhRai280/study-timer-pro")
    
    def show_about(self):
        """Show the about dialog"""
        about_window = tk.Toplevel(self.root)
        about_window.title("About Study Timer Pro")
        about_window.geometry("400x300")
        about_window.resizable(False, False)
        about_window.configure(bg=self.settings.colors['bg'])
        
        tk.Label(about_window,
               text="Study Timer Pro",
               font=('Arial', 16, 'bold'),
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack(pady=10)
        
        tk.Label(about_window,
               text="Version 1.0.0",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack()
        
        tk.Label(about_window,
               text="A comprehensive study timer with focus tools,\nanalytics, and productivity features.",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg'],
               justify=tk.CENTER).pack(pady=20)
        
        tk.Label(about_window,
               text="© 2025 Study Timer Pro",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack(pady=10)
        
        tk.Button(about_window,
                text="Close",
                command=about_window.destroy,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(pady=10)
    
    def on_close(self):
        """Handle application close event"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?\nAll apps will be unlocked."):
            self.timer_tab.unlock_all_apps()
            self.timer_tab.unblock_all_websites()
            self.settings.save_settings()
            self.root.destroy()

