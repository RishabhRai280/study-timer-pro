"""
Settings management for Study Timer Pro
"""

import os
import json
import tkinter as tk
import random

class Settings:
    """
    Manages application settings and state
    """
    
    def __init__(self):
        """Initialize settings with default values"""
        # Timer settings
        self.focus_time = tk.StringVar(value="25")
        self.short_break = tk.StringVar(value="5")
        self.long_break = tk.StringVar(value="15")
        self.sessions_before_long_break = tk.StringVar(value="4")
        
        # App state
        self.session_count = 1
        self.locked_apps = []
        self.blocked_websites = []
        self.todo_list = []
        self.completed_tasks = []
        self.daily_stats = {}
        
        # App blocking settings
        self.strict_mode = tk.BooleanVar(value=False)
        self.auto_block = tk.BooleanVar(value=False)
        
        # Notification settings
        self.desktop_notifications = tk.BooleanVar(value=True)
        self.sound_notifications = tk.BooleanVar(value=True)
        
        # Sound settings
        self.sound_enabled = tk.BooleanVar(value=True)
        self.start_sound_path = tk.StringVar(value="")
        self.end_sound_path = tk.StringVar(value="")
        self.background_music_path = tk.StringVar(value="")
        self.volume_level = tk.IntVar(value=70)
        self.is_muted = tk.BooleanVar(value=False)
        
        # Image settings
        self.custom_study_image = tk.StringVar(value="")
        self.custom_app_icon = tk.StringVar(value="")
        self.background_image_path = tk.StringVar(value="")
        
        # Statistics settings
        self.daily_goal = tk.StringVar(value="120")
        self.streak_goal_var = tk.StringVar(value="7")
        self.auto_start = tk.BooleanVar(value=False)
        
        # Theme settings
        self.color_schemes = {
            'Deep Blue': {
                'bg': '#1E293B',  # Darker blue for better contrast
                'fg': '#F59E0B',  # Warmer gold for better visibility
                'accent': '#3B82F6',  # Brighter blue accent
                'text': '#F8FAFC',  # Lighter text for better readability
                'button': '#2563EB',  # Vibrant button color
                'button_hover': '#1D4ED8'  # Slightly darker for hover state
            },
            'Dark Mode': {
                'bg': '#111827',  # Darker background for true dark mode
                'fg': '#F9FAFB',
                'accent': '#4B5563',
                'text': '#E5E7EB',
                'button': '#374151',
                'button_hover': '#4B5563'
            },
            'Light Mode': {
                'bg': '#F8FAFC',  # Lighter background for better contrast
                'fg': '#0F172A',  # Darker text for better readability
                'accent': '#CBD5E1',  # Subtle accent
                'text': '#1E293B',
                'button': '#E2E8F0',
                'button_hover': '#CBD5E1'
            },
            'Forest': {
                'bg': '#064E3B',
                'fg': '#ECFDF5',
                'accent': '#10B981',
                'text': '#D1FAE5',
                'button': '#059669',
                'button_hover': '#047857'
            },
            'Purple': {  # New theme
                'bg': '#2E1065',
                'fg': '#E9D5FF',
                'accent': '#7E22CE',
                'text': '#F3E8FF',
                'button': '#9333EA',
                'button_hover': '#7E22CE'
            },
        }
        
        # Default color scheme
        self.current_theme = 'Deep Blue'
        self.colors = self.color_schemes[self.current_theme]
        
        # App lists
        self.app_list = ["Chrome", "Firefox", "Edge", "Safari", "WhatsApp", "Discord", "Spotify", 
                        "Steam", "Epic Games", "Telegram", "Slack", "Twitter", "Instagram", 
                        "Facebook", "TikTok", "YouTube", "Netflix", "Zoom", "Teams", "Outlook"]
        
        # Website list
        self.website_list = ["www.facebook.com", "www.instagram.com", "www.twitter.com",
                           "www.youtube.com", "www.reddit.com", "www.tiktok.com",
                           "www.netflix.com", "www.twitch.tv", "www.pinterest.com",
                           "www.tumblr.com", "www.snapchat.com", "www.vk.com"]
        
        # Motivational quotes
        self.motivational_quotes = [
            "The secret of getting ahead is getting started. – Mark Twain",
            "It always seems impossible until it's done. – Nelson Mandela",
            "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
            "Believe you can and you're halfway there. – Theodore Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. – Winston Churchill",
            "Your focus determines your reality. – Qui-Gon Jinn",
            "The best way to predict the future is to create it. – Abraham Lincoln",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "Progress is not achieved by luck or accident, but by working on yourself daily. – Epictetus",
            "Study hard what interests you the most in the most undisciplined, irreverent and original manner possible. – Richard Feynman",
            "The only place where success comes before work is in the dictionary. – Vidal Sassoon",
            "The difference between ordinary and extraordinary is that little extra. – Jimmy Johnson",
            "The expert in anything was once a beginner. – Helen Hayes",
            "The beautiful thing about learning is that no one can take it away from you. – B.B. King",
            "Education is the passport to the future, for tomorrow belongs to those who prepare for it today. – Malcolm X"
        ]
    
    def save_settings(self):
        """Save settings to a JSON file"""
        data = {
            'todo_list': self.todo_list,
            'locked_apps': self.locked_apps,
            'blocked_websites': self.blocked_websites,
            'completed_tasks': self.completed_tasks,
            'daily_stats': self.daily_stats,
            'focus_time': self.focus_time.get(),
            'short_break': self.short_break.get(),
            'long_break': self.long_break.get(),
            'sessions_before_long_break': self.sessions_before_long_break.get(),
            'daily_goal': self.daily_goal.get(),
            'streak_goal': self.streak_goal_var.get(),
            'strict_mode': self.strict_mode.get(),
            'auto_block': self.auto_block.get(),
            'desktop_notifications': self.desktop_notifications.get(),
            'sound_notifications': self.sound_notifications.get(),
            'theme': self.current_theme,
            'auto_start': self.auto_start.get(),
            'start_sound_path': self.start_sound_path.get(),
            'end_sound_path': self.end_sound_path.get(),
            'background_music_path': self.background_music_path.get(),
            'background_image_path': self.background_image_path.get(),
            'custom_study_image': self.custom_study_image.get(),
            'custom_app_icon': self.custom_app_icon.get(),
            'volume_level': self.volume_level.get(),
            'is_muted': self.is_muted.get(),
            'session_count': self.session_count
        }
        try:
            with open('study_timer_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_settings(self):
        """Load settings from a JSON file"""
        try:
            if not os.path.exists('study_timer_data.json'):
                return
                
            with open('study_timer_data.json', 'r') as f:
                data = json.load(f)
                
            self.todo_list = data.get('todo_list', [])
            self.locked_apps = data.get('locked_apps', [])
            self.blocked_websites = data.get('blocked_websites', [])
            self.completed_tasks = data.get('completed_tasks', [])
            self.daily_stats = data.get('daily_stats', {})
            self.session_count = data.get('session_count', 1)
            
            # Convert string keys back to dictionary keys
            if isinstance(self.daily_stats, dict):
                self.daily_stats = {str(k): v for k, v in self.daily_stats.items()}
            
            # Load settings
            self.focus_time.set(data.get('focus_time', '25'))
            self.short_break.set(data.get('short_break', '5'))
            self.long_break.set(data.get('long_break', '15'))
            self.sessions_before_long_break.set(data.get('sessions_before_long_break', '4'))
            self.daily_goal.set(data.get('daily_goal', '120'))
            self.streak_goal_var.set(data.get('streak_goal', '7'))
            self.strict_mode.set(data.get('strict_mode', False))
            self.auto_block.set(data.get('auto_block', False))
            self.desktop_notifications.set(data.get('desktop_notifications', True))
            self.sound_notifications.set(data.get('sound_notifications', True))
            
            # Load sound settings
            self.start_sound_path.set(data.get('start_sound_path', ''))
            self.end_sound_path.set(data.get('end_sound_path', ''))
            self.background_music_path.set(data.get('background_music_path', ''))
            self.background_image_path.set(data.get('background_image_path', ''))
            self.volume_level.set(data.get('volume_level', 70))
            self.is_muted.set(data.get('is_muted', False))
            
            # Load image settings
            self.custom_study_image.set(data.get('custom_study_image', ''))
            self.custom_app_icon.set(data.get('custom_app_icon', ''))
            
            # Load auto-start setting if available
            if 'auto_start' in data:
                self.auto_start.set(data.get('auto_start', False))
            
            # Load theme
            theme = data.get('theme', 'Deep Blue')
            if theme in self.color_schemes:
                self.current_theme = theme
                self.colors = self.color_schemes[theme]
            
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def export_settings(self, filename):
        """Export settings to a JSON file"""
        settings = {
            'focus_time': self.focus_time.get(),
            'short_break': self.short_break.get(),
            'long_break': self.long_break.get(),
            'sessions_before_long_break': self.sessions_before_long_break.get(),
            'daily_goal': self.daily_goal.get(),
            'streak_goal': self.streak_goal_var.get(),
            'strict_mode': self.strict_mode.get(),
            'auto_block': self.auto_block.get(),
            'desktop_notifications': self.desktop_notifications.get(),
            'sound_notifications': self.sound_notifications.get(),
            'theme': self.current_theme,
            'start_sound_path': self.start_sound_path.get(),
            'end_sound_path': self.end_sound_path.get(),
            'background_music_path': self.background_music_path.get(),
            'background_image_path': self.background_image_path.get(),
            'custom_study_image': self.custom_study_image.get(),
            'custom_app_icon': self.custom_app_icon.get(),
            'volume_level': self.volume_level.get(),
            'is_muted': self.is_muted.get()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            raise Exception(f"Failed to export settings: {e}")
    
    def import_settings(self, filename):
        """Import settings from a JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Only import settings, not statistics or tasks
            settings_keys = ['focus_time', 'short_break', 'long_break', 
                           'sessions_before_long_break', 'daily_goal', 
                           'streak_goal', 'strict_mode', 'auto_block', 
                           'desktop_notifications', 'sound_notifications', 'theme',
                           'start_sound_path', 'end_sound_path', 'background_music_path',
                           'background_image_path', 'custom_study_image', 'custom_app_icon',
                           'volume_level', 'is_muted']
            
            for key in settings_keys:
                if key in data:
                    if key == 'focus_time':
                        self.focus_time.set(data[key])
                    elif key == 'short_break':
                        self.short_break.set(data[key])
                    elif key == 'long_break':
                        self.long_break.set(data[key])
                    elif key == 'sessions_before_long_break':
                        self.sessions_before_long_break.set(data[key])
                    elif key == 'daily_goal':
                        self.daily_goal.set(data[key])
                    elif key == 'streak_goal':
                        self.streak_goal_var.set(data[key])
                    elif key == 'strict_mode':
                        self.strict_mode.set(data[key])
                    elif key == 'auto_block':
                        self.auto_block.set(data[key])
                    elif key == 'desktop_notifications':
                        self.desktop_notifications.set(data[key])
                    elif key == 'sound_notifications':
                        self.sound_notifications.set(data[key])
                    elif key == 'theme' and data[key] in self.color_schemes:
                        self.current_theme = data[key]
                        self.colors = self.color_schemes[data[key]]
                    elif key == 'start_sound_path':
                        self.start_sound_path.set(data[key])
                    elif key == 'end_sound_path':
                        self.end_sound_path.set(data[key])
                    elif key == 'background_music_path':
                        self.background_music_path.set(data[key])
                    elif key == 'background_image_path':
                        self.background_image_path.set(data[key])
                    elif key == 'custom_study_image':
                        self.custom_study_image.set(data[key])
                    elif key == 'custom_app_icon':
                        self.custom_app_icon.set(data[key])
                    elif key == 'volume_level':
                        self.volume_level.set(data[key])
                    elif key == 'is_muted':
                        self.is_muted.set(data[key])
        except Exception as e:
            raise Exception(f"Failed to import settings: {e}")

