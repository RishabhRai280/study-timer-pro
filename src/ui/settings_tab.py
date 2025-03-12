"""
Settings tab implementation for Study Timer Pro
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import os
import platform
import subprocess
import shutil
from PIL import Image, ImageTk

class SettingsTab:
    def __init__(self, parent, app):
        self.app = app
        self.settings = app.settings
        
        # Create main frame
        self.frame = tk.Frame(parent, bg=self.settings.colors['bg'])
        
        # Create UI components
        self.create_settings_panel()
    
    def create_settings_panel(self):
        """Create the settings panel with all configuration options"""
        # Create a canvas with scrollbar for settings
        self.canvas = tk.Canvas(self.frame, bg=self.settings.colors['bg'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.settings.colors['bg'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # App blocking settings
        app_block_frame = tk.LabelFrame(self.scrollable_frame,
                                      text="App Blocking Settings",
                                      bg=self.settings.colors['bg'],
                                      fg=self.settings.colors['fg'],
                                      font=('Arial', 10, 'bold'))
        app_block_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Strict mode setting
        tk.Checkbutton(app_block_frame,
                     text="Strict Mode (Cannot unlock apps during focus time)",
                     variable=self.settings.strict_mode,
                     bg=self.settings.colors['bg'],
                     fg=self.settings.colors['text'],
                     selectcolor=self.settings.colors['bg'],
                     activebackground=self.settings.colors['bg'],
                     activeforeground=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        # Auto-start setting
        tk.Checkbutton(app_block_frame,
                     text="Auto-block apps when session starts",
                     variable=self.settings.auto_block,
                     bg=self.settings.colors['bg'],
                     fg=self.settings.colors['text'],
                     selectcolor=self.settings.colors['bg'],
                     activebackground=self.settings.colors['bg'],
                     activeforeground=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        # Notification settings
        notif_frame = tk.LabelFrame(self.scrollable_frame,
                                  text="Notification Settings",
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'],
                                  font=('Arial', 10, 'bold'))
        notif_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Desktop notifications
        tk.Checkbutton(notif_frame,
                     text="Desktop Notifications",
                     variable=self.settings.desktop_notifications,
                     bg=self.settings.colors['bg'],
                     fg=self.settings.colors['text'],
                     selectcolor=self.settings.colors['bg'],
                     activebackground=self.settings.colors['bg'],
                     activeforeground=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        # Sound notifications
        tk.Checkbutton(notif_frame,
                     text="Sound Notifications",
                     variable=self.settings.sound_notifications,
                     bg=self.settings.colors['bg'],
                     fg=self.settings.colors['text'],
                     selectcolor=self.settings.colors['bg'],
                     activebackground=self.settings.colors['bg'],
                     activeforeground=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        # Sound settings
        sound_settings_frame = tk.LabelFrame(self.scrollable_frame,
                                          text="Sound Settings",
                                          bg=self.settings.colors['bg'],
                                          fg=self.settings.colors['fg'],
                                          font=('Arial', 10, 'bold'))
        sound_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Volume control
        volume_frame = tk.Frame(sound_settings_frame, bg=self.settings.colors['bg'])
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(volume_frame, 
               text="Volume:", 
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        volume_scale = tk.Scale(volume_frame, 
                              from_=0, 
                              to=100, 
                              orient=tk.HORIZONTAL, 
                              variable=self.settings.volume_level,
                              bg=self.settings.colors['bg'], 
                              fg=self.settings.colors['fg'],
                              highlightthickness=0,
                              command=self.update_volume)
        volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Mute checkbox
        tk.Checkbutton(volume_frame,
                     text="Mute",
                     variable=self.settings.is_muted,
                     command=self.toggle_mute,
                     bg=self.settings.colors['bg'],
                     fg=self.settings.colors['text'],
                     selectcolor=self.settings.colors['bg'],
                     activebackground=self.settings.colors['bg'],
                     activeforeground=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        # Start sound selection
        start_sound_frame = tk.Frame(sound_settings_frame, bg=self.settings.colors['bg'])
        start_sound_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(start_sound_frame, 
               text="Start Sound:", 
               width=15, 
               anchor=tk.W,
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        tk.Entry(start_sound_frame, 
               textvariable=self.settings.start_sound_path, 
               state="readonly",
               readonlybackground=self.settings.colors['bg'],
               fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(start_sound_frame,
                text="Browse",
                command=lambda: self.browse_sound_file("start"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(start_sound_frame,
                text="Test",
                command=lambda: self.test_sound("start"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # End sound selection
        end_sound_frame = tk.Frame(sound_settings_frame, bg=self.settings.colors['bg'])
        end_sound_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(end_sound_frame, 
               text="End Sound:", 
               width=15, 
               anchor=tk.W,
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        tk.Entry(end_sound_frame, 
               textvariable=self.settings.end_sound_path, 
               state="readonly",
               readonlybackground=self.settings.colors['bg'],
               fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(end_sound_frame,
                text="Browse",
                command=lambda: self.browse_sound_file("end"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(end_sound_frame,
                text="Test",
                command=lambda: self.test_sound("end"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Background music selection
        bg_music_frame = tk.Frame(sound_settings_frame, bg=self.settings.colors['bg'])
        bg_music_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(bg_music_frame, 
               text="Background Music:", 
               width=15, 
               anchor=tk.W,
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        tk.Entry(bg_music_frame, 
               textvariable=self.settings.background_music_path, 
               state="readonly",
               readonlybackground=self.settings.colors['bg'],
               fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(bg_music_frame,
                text="Browse",
                command=self.browse_background_music,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bg_music_frame,
                text="Test",
                command=lambda: self.test_sound("background"),
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Custom image settings
        image_frame = tk.LabelFrame(self.scrollable_frame,
                                  text="Custom Images",
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'],
                                  font=('Arial', 10, 'bold'))
        image_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Study image selection
        study_image_frame = tk.Frame(image_frame, bg=self.settings.colors['bg'])
        study_image_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(study_image_frame, 
               text="Study Image:", 
               width=15, 
               anchor=tk.W,
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        self.study_image_path_display = tk.Entry(study_image_frame, 
                                              textvariable=self.settings.custom_study_image, 
                                              state="readonly",
                                              readonlybackground=self.settings.colors['bg'],
                                              fg=self.settings.colors['text'])
        self.study_image_path_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(study_image_frame,
                text="Browse",
                command=self.browse_study_image,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(study_image_frame,
                text="Clear",
                command=self.clear_study_image,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Study image preview
        self.study_image_preview_frame = tk.Frame(image_frame, bg=self.settings.colors['bg'])
        self.study_image_preview_frame.pack(fill=tk.X, padx=10, pady=5)
        self.update_study_image_preview()
        
        # App icon selection
        app_icon_frame = tk.Frame(image_frame, bg=self.settings.colors['bg'])
        app_icon_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(app_icon_frame, 
               text="App Icon:", 
               width=15, 
               anchor=tk.W,
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        self.app_icon_path_display = tk.Entry(app_icon_frame, 
                                           textvariable=self.settings.custom_app_icon, 
                                           state="readonly",
                                           readonlybackground=self.settings.colors['bg'],
                                           fg=self.settings.colors['text'])
        self.app_icon_path_display.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(app_icon_frame,
                text="Browse",
                command=self.browse_app_icon,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(app_icon_frame,
                text="Clear",
                command=self.clear_app_icon,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # App icon preview
        self.app_icon_preview_frame = tk.Frame(image_frame, bg=self.settings.colors['bg'])
        self.app_icon_preview_frame.pack(fill=tk.X, padx=10, pady=5)
        self.update_app_icon_preview()
        
        # Background image settings
        bg_image_frame = tk.LabelFrame(self.scrollable_frame,
                                     text="Background Image",
                                     bg=self.settings.colors['bg'],
                                     fg=self.settings.colors['fg'],
                                     font=('Arial', 10, 'bold'))
        bg_image_frame.pack(fill=tk.X, padx=10, pady=10)
        
        bg_image_select_frame = tk.Frame(bg_image_frame, bg=self.settings.colors['bg'])
        bg_image_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(bg_image_select_frame, 
               text="Image:", 
               width=15, 
               anchor=tk.W,
               bg=self.settings.colors['bg'], 
               fg=self.settings.colors['fg']).pack(side=tk.LEFT, padx=5)
        
        tk.Entry(bg_image_select_frame, 
               textvariable=self.settings.background_image_path, 
               state="readonly",
               readonlybackground=self.settings.colors['bg'],
               fg=self.settings.colors['text']).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        tk.Button(bg_image_select_frame,
                text="Browse",
                command=self.browse_background_image,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bg_image_select_frame,
                text="Remove",
                command=self.remove_background_image,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text']).pack(side=tk.LEFT, padx=5)
        
        # Statistics settings
        stats_frame = tk.LabelFrame(self.scrollable_frame,
                                  text="Statistics Settings",
                                  bg=self.settings.colors['bg'],
                                  fg=self.settings.colors['fg'],
                                  font=('Arial', 10, 'bold'))
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Daily goal
        tk.Label(stats_frame,
               text="Daily Study Goal (minutes):",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Entry(stats_frame,
               textvariable=self.settings.daily_goal,
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['text']).pack(fill=tk.X, padx=10, pady=5)
        
        # Streak goal
        tk.Label(stats_frame,
               text="Streak Goal (days):",
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        tk.Entry(stats_frame,
               textvariable=self.settings.streak_goal_var,
               bg=self.settings.colors['bg'],
               fg=self.settings.colors['text']).pack(fill=tk.X, padx=10, pady=5)
        
        # Auto-start at login
        tk.Checkbutton(stats_frame,
                     text="Start application at system login",
                     variable=self.settings.auto_start,
                     bg=self.settings.colors['bg'],
                     fg=self.settings.colors['text'],
                     selectcolor=self.settings.colors['bg'],
                     activebackground=self.settings.colors['bg'],
                     activeforeground=self.settings.colors['fg']).pack(anchor=tk.W, padx=10, pady=5)
        
        # Save settings button
        tk.Button(self.scrollable_frame,
                text="Save Settings",
                command=self.save_settings,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text'],
                font=('Arial', 10, 'bold'),
                width=20,
                pady=10).pack(pady=10)
        
        # Reset all settings button
        tk.Button(self.scrollable_frame,
                text="Reset All Settings",
                command=self.reset_all_settings,
                bg=self.settings.colors['button'],
                fg=self.settings.colors['text'],
                width=20).pack(pady=5)
    
    def update_volume(self, *args):
        """Update volume level for all sounds"""
        import pygame
        volume = self.settings.volume_level.get() / 100.0
        pygame.mixer.music.set_volume(volume)
    
    def toggle_mute(self):
        """Toggle mute state for all sounds"""
        import pygame
        if self.settings.is_muted.get():
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.settings.volume_level.get() / 100.0)
    
    def browse_sound_file(self, sound_type):
        """Browse for a sound file"""
        filetypes = [("Sound files", "*.wav *.mp3 *.ogg"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title=f"Select {sound_type} sound", filetypes=filetypes)
        
        if filename:
            if sound_type == "start":
                self.settings.start_sound_path.set(filename)
            elif sound_type == "end":
                self.settings.end_sound_path.set(filename)
    
    def browse_background_music(self):
        """Browse for background music file"""
        filetypes = [("Audio files", "*.mp3 *.wav *.ogg"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select background music", filetypes=filetypes)
        
        if filename:
            self.settings.background_music_path.set(filename)
    
    def test_sound(self, sound_type):
        """Test the selected sound"""
        if self.settings.is_muted.get():
            messagebox.showinfo("Sound Test", "Sound is currently muted.")
            return
        
        try:
            import pygame
            if sound_type == "start" and self.settings.start_sound_path.get():
                sound = pygame.mixer.Sound(self.settings.start_sound_path.get())
                sound.set_volume(self.settings.volume_level.get() / 100.0)
                sound.play()
            elif sound_type == "end" and self.settings.end_sound_path.get():
                sound = pygame.mixer.Sound(self.settings.end_sound_path.get())
                sound.set_volume(self.settings.volume_level.get() / 100.0)
                sound.play()
            elif sound_type == "background" and self.settings.background_music_path.get():
                # Stop any currently playing music
                pygame.mixer.music.stop()
                
                # Load and play the background music
                pygame.mixer.music.load(self.settings.background_music_path.get())
                pygame.mixer.music.set_volume(self.settings.volume_level.get() / 100.0)
                pygame.mixer.music.play()
                
                # Stop after 5 seconds (for testing)
                self.app.root.after(5000, pygame.mixer.music.stop)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play sound: {e}")
    
    def browse_study_image(self):
        """Browse for study image"""
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select study image", filetypes=filetypes)
        
        if filename:
            # Create resources directory if it doesn't exist
            resources_dir = os.path.join("resources", "images")
            os.makedirs(resources_dir, exist_ok=True)
            
            # Copy the image to resources directory with a unique name
            dest_filename = f"study_image_{os.path.basename(filename)}"
            dest_path = os.path.join(resources_dir, dest_filename)
            
            try:
                shutil.copy2(filename, dest_path)
                self.settings.custom_study_image.set(dest_path)
                self.update_study_image_preview()
                
                # Update the timer tab to show the new image
                if hasattr(self.app, 'timer_tab'):
                    self.app.timer_tab.load_study_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy image: {e}")
    
    def clear_study_image(self):
        """Clear the study image"""
        self.settings.custom_study_image.set("")
        self.update_study_image_preview()
        
        # Update the timer tab to show the default image
        if hasattr(self.app, 'timer_tab'):
            self.app.timer_tab.load_study_image()
    
    def update_study_image_preview(self):
        """Update the study image preview"""
        # Clear existing preview
        for widget in self.study_image_preview_frame.winfo_children():
            widget.destroy()
        
        study_image_path = self.settings.custom_study_image.get()
        if study_image_path and os.path.exists(study_image_path):
            try:
                # Load and resize image for preview
                img = Image.open(study_image_path)
                img = img.resize((150, 150), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Display preview
                preview_label = tk.Label(self.study_image_preview_frame, image=photo, bg=self.settings.colors['bg'])
                preview_label.image = photo  # Keep a reference
                preview_label.pack(pady=5)
                
                tk.Label(self.study_image_preview_frame, 
                       text="Study Image Preview",
                       font=('Arial', 10),
                       bg=self.settings.colors['bg'],
                       fg=self.settings.colors['fg']).pack()
            except Exception as e:
                tk.Label(self.study_image_preview_frame, 
                       text=f"Error loading preview: {e}",
                       font=('Arial', 10),
                       bg=self.settings.colors['bg'],
                       fg="red").pack(pady=5)
        else:
            tk.Label(self.study_image_preview_frame, 
                   text="No study image selected",
                   font=('Arial', 10),
                   bg=self.settings.colors['bg'],
                   fg=self.settings.colors['fg']).pack(pady=5)
    
    def browse_app_icon(self):
        """Browse for app icon"""
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.ico"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select app icon", filetypes=filetypes)
        
        if filename:
            # Create resources directory if it doesn't exist
            resources_dir = os.path.join("resources", "images")
            os.makedirs(resources_dir, exist_ok=True)
            
            # Copy the image to resources directory with a unique name
            dest_filename = f"app_icon_{os.path.basename(filename)}"
            dest_path = os.path.join(resources_dir, dest_filename)
            
            try:
                shutil.copy2(filename, dest_path)
                self.settings.custom_app_icon.set(dest_path)
                self.update_app_icon_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy image: {e}")
    
    def clear_app_icon(self):
        """Clear the app icon"""
        self.settings.custom_app_icon.set("")
        self.update_app_icon_preview()
    
    def update_app_icon_preview(self):
        """Update the app icon preview"""
        # Clear existing preview
        for widget in self.app_icon_preview_frame.winfo_children():
            widget.destroy()
        
        app_icon_path = self.settings.custom_app_icon.get()
        if app_icon_path and os.path.exists(app_icon_path):
            try:
                # Load and resize image for preview
                img = Image.open(app_icon_path)
                img = img.resize((64, 64), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Display preview
                preview_label = tk.Label(self.app_icon_preview_frame, image=photo, bg=self.settings.colors['bg'])
                preview_label.image = photo  # Keep a reference
                preview_label.pack(pady=5)
                
                tk.Label(self.app_icon_preview_frame, 
                       text="App Icon Preview",
                       font=('Arial', 10),
                       bg=self.settings.colors['bg'],
                       fg=self.settings.colors['fg']).pack()
            except Exception as e:
                tk.Label(self.app_icon_preview_frame, 
                       text=f"Error loading preview: {e}",
                       font=('Arial', 10),
                       bg=self.settings.colors['bg'],
                       fg="red").pack(pady=5)
        else:
            tk.Label(self.app_icon_preview_frame, 
                   text="No app icon selected",
                   font=('Arial', 10),
                   bg=self.settings.colors['bg'],
                   fg=self.settings.colors['fg']).pack(pady=5)
    
    def browse_background_image(self):
        """Browse for background image"""
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select background image", filetypes=filetypes)
        
        if filename:
            self.settings.background_image_path.set(filename)
            self.app.apply_background_image()
    
    def remove_background_image(self):
        """Remove the background image"""
        self.settings.background_image_path.set("")
        
        # Remove background label if it exists
        if hasattr(self.app, 'bg_image_label'):
            self.app.bg_image_label.destroy()
            delattr(self.app, 'bg_image_label')
    
    def reset_all_settings(self):
        """Reset all settings to default values"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to default values?"):
            # Reset timer settings
            self.settings.focus_time.set("25")
            self.settings.short_break.set("5")
            self.settings.long_break.set("15")
            self.settings.sessions_before_long_break.set("4")
            
            # Reset app blocking settings
            self.settings.strict_mode.set(False)
            self.settings.auto_block.set(False)
            
            # Reset notification settings
            self.settings.desktop_notifications.set(True)
            self.settings.sound_notifications.set(True)
            
            # Reset sound settings
            self.settings.volume_level.set(70)
            self.settings.is_muted.set(False)
            self.settings.start_sound_path.set("")
            self.settings.end_sound_path.set("")
            self.settings.background_music_path.set("")
            
            # Reset image settings
            self.settings.custom_study_image.set("")
            self.settings.custom_app_icon.set("")
            self.settings.background_image_path.set("")
            
            # Reset background image
            self.remove_background_image()
            
            # Reset statistics settings
            self.settings.daily_goal.set("120")
            self.settings.streak_goal_var.set("7")
            self.settings.auto_start.set(False)
            
            # Update previews
            self.update_study_image_preview()
            self.update_app_icon_preview()
            
            # Update timer tab
            if hasattr(self.app, 'timer_tab'):
                self.app.timer_tab.load_study_image()
            
            # Save settings
            self.save_settings()
            
            messagebox.showinfo("Settings Reset", "All settings have been reset to default values.")
    
    def save_settings(self):
        """Save all settings"""
        try:
            # Update streak goal display in timer tab if it exists
            if hasattr(self.app, 'timer_tab') and hasattr(self.app.timer_tab, 'streak_goal'):
                self.app.timer_tab.streak_goal.config(text=f"Goal: {self.settings.streak_goal_var.get()} days")
            
            # Update session indicators if timer tab exists
            if hasattr(self.app, 'timer_tab'):
                self.app.timer_tab.update_session_indicators()
            
            # Set up auto-start at login if enabled
            if self.settings.auto_start.get():
                self.setup_auto_start()
            else:
                self.remove_auto_start()
            
            # Apply app icon
            self.app.set_app_icon()
            
            # Save all settings to file
            self.settings.save_settings()
            messagebox.showinfo("Settings", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def setup_auto_start(self):
        """Set up application to start at system login"""
        try:
            if platform.system() == "Windows":
                import winreg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                
                # Get the path to the current script
                app_path = os.path.abspath(sys.argv[0])
                
                # Open the registry key
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                
                # Set the value
                winreg.SetValueEx(key, "StudyTimerPro", 0, winreg.REG_SZ, f'"{app_path}"')
                
                # Close the key
                winreg.CloseKey(key)
            
            elif platform.system() == "Darwin":  # macOS
                # Create a plist file in ~/Library/LaunchAgents
                plist_path = os.path.expanduser("~/Library/LaunchAgents/com.studytimerpro.plist")
                app_path = os.path.abspath(sys.argv[0])
                
                plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                <plist version="1.0">
                <dict>
                    <key>Label</key>
                    <string>com.studytimerpro</string>
                    <key>ProgramArguments</key>
                    <array>
                        <string>python3</string>
                        <string>{app_path}</string>
                    </array>
                    <key>RunAtLoad</key>
                    <true/>
                </dict>
                </plist>"""
                
                with open(plist_path, "w") as f:
                    f.write(plist_content)
                
                # Set permissions
                os.chmod(plist_path, 0o644)
                
                # Load the plist
                subprocess.run(["launchctl", "load", plist_path], check=False)
            
            elif platform.system() == "Linux":
                # Create a .desktop file in ~/.config/autostart
                autostart_dir = os.path.expanduser("~/.config/autostart")
                if not os.path.exists(autostart_dir):
                    os.makedirs(autostart_dir)
                
                desktop_path = os.path.join(autostart_dir, "studytimerpro.desktop")
                app_path = os.path.abspath(sys.argv[0])
                
                desktop_content = f"""[Desktop Entry]
                Type=Application
                Exec=python3 {app_path}
                Hidden=false
                NoDisplay=false
                X-GNOME-Autostart-enabled=true
                Name=Study Timer Pro
                Comment=Study Timer Application
                """
                
                with open(desktop_path, "w") as f:
                    f.write(desktop_content)
                
                # Set permissions
                os.chmod(desktop_path, 0o755)
        
        except Exception as e:
            print(f"Error setting up auto-start: {e}")
    
    def remove_auto_start(self):
        """Remove application from system startup"""
        try:
            if platform.system() == "Windows":
                import winreg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                
                # Open the registry key
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
                
                try:
                    # Delete the value
                    winreg.DeleteValue(key, "StudyTimerPro")
                except FileNotFoundError:
                    pass  # Value doesn't exist, which is fine
                
                # Close the key
                winreg.CloseKey(key)
            
            elif platform.system() == "Darwin":  # macOS
                # Remove the plist file
                plist_path = os.path.expanduser("~/Library/LaunchAgents/com.studytimerpro.plist")
                
                if os.path.exists(plist_path):
                    # Unload the plist
                    subprocess.run(["launchctl", "unload", plist_path], check=False)
                    
                    # Remove the file
                    os.remove(plist_path)
            
            elif platform.system() == "Linux":
                # Remove the .desktop file
                desktop_path = os.path.expanduser("~/.config/autostart/studytimerpro.desktop")
                
                if os.path.exists(desktop_path):
                    os.remove(desktop_path)
        
        except Exception as e:
            print(f"Error removing auto-start: {e}")
    
    def apply_theme(self):
        """Apply the current theme to all UI elements"""
        # Update frame
        self.frame.configure(bg=self.settings.colors['bg'])
        self.scrollable_frame.configure(bg=self.settings.colors['bg'])
        self.canvas.configure(bg=self.settings.colors['bg'])
        
        # Update all widgets
        self.update_widget_colors(self.scrollable_frame)
    
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
