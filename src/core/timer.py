"""
Timer logic for Study Timer Pro
"""

import time
import threading
from datetime import datetime

class TimerManager:
    """
    Manages the timer functionality for the Pomodoro technique
    """
    
    def __init__(self, update_callback=None, complete_callback=None):
        """
        Initialize the timer manager
        
        Args:
            update_callback: Function to call on each timer update
            complete_callback: Function to call when timer completes
        """
        self.update_callback = update_callback
        self.complete_callback = complete_callback
        self.is_running = False
        self.is_paused = False
        self.current_timer = None
        self.remaining_seconds = 0
        self.start_time = None
        self.pause_time = None
    
    def start_timer(self, seconds, timer_type="focus"):
        """
        Start a new timer
        
        Args:
            seconds: Duration in seconds
            timer_type: Type of timer (focus, short_break, long_break)
        """
        self.stop_timer()  # Stop any existing timer
        
        self.is_running = True
        self.is_paused = False
        self.remaining_seconds = seconds
        self.start_time = time.time()
        self.timer_type = timer_type
        
        # Start timer in a separate thread
        self.current_timer = threading.Thread(
            target=self._run_timer,
            args=(seconds,),
            daemon=True
        )
        self.current_timer.start()
        
        return True
    
    def pause_timer(self):
        """Pause the current timer"""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_time = time.time()
            return True
        return False
    
    def resume_timer(self):
        """Resume a paused timer"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            # Adjust start time to account for pause duration
            if self.pause_time:
                pause_duration = time.time() - self.pause_time
                self.start_time += pause_duration
            return True
        return False
    
    def stop_timer(self):
        """Stop the current timer"""
        self.is_running = False
        self.is_paused = False
        return True
    
    def get_remaining_time(self):
        """Get the remaining time in seconds"""
        if not self.is_running:
            return 0
        
        if self.is_paused:
            return self.remaining_seconds
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.remaining_seconds - int(elapsed))
        return remaining
    
    def get_formatted_time(self):
        """Get the remaining time formatted as MM:SS"""
        remaining = self.get_remaining_time()
        minutes, seconds = divmod(remaining, 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_progress_percentage(self, total_seconds):
        """Get the progress as a percentage"""
        if not self.is_running or total_seconds == 0:
            return 0
        
        remaining = self.get_remaining_time()
        progress = 100 - (remaining / total_seconds * 100)
        return min(100, max(0, progress))
    
    def _run_timer(self, total_seconds):
        """Internal method to run the timer"""
        self.remaining_seconds = total_seconds
        
        while self.is_running and self.remaining_seconds > 0:
            if not self.is_paused:
                # Calculate remaining time
                elapsed = time.time() - self.start_time
                self.remaining_seconds = max(0, total_seconds - int(elapsed))
                
                # Call update callback if provided
                if self.update_callback:
                    self.update_callback(self.remaining_seconds, self.timer_type)
                
                # Check if timer completed
                if self.remaining_seconds <= 0:
                    self.is_running = False
                    if self.complete_callback:
                        self.complete_callback(self.timer_type)
                    break
            
            # Sleep briefly to avoid high CPU usage
            time.sleep(0.1)