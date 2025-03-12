"""
Tests for the timer functionality
"""

import unittest
import time
from src.core.timer import TimerManager

class TestTimerManager(unittest.TestCase):
    """Test cases for the TimerManager class"""
    
    def test_timer_initialization(self):
        """Test timer initialization"""
        timer = TimerManager()
        self.assertFalse(timer.is_running)
        self.assertFalse(timer.is_paused)
        self.assertEqual(timer.remaining_seconds, 0)
    
    def test_start_timer(self):
        """Test starting a timer"""
        timer = TimerManager()
        result = timer.start_timer(60, "focus")
        self.assertTrue(result)
        self.assertTrue(timer.is_running)
        self.assertFalse(timer.is_paused)
        self.assertEqual(timer.timer_type, "focus")
    
    def test_pause_resume_timer(self):
        """Test pausing and resuming a timer"""
        timer = TimerManager()
        timer.start_timer(60, "focus")
        
        # Test pause
        result = timer.pause_timer()
        self.assertTrue(result)
        self.assertTrue(timer.is_paused)
        
        # Test resume
        result = timer.resume_timer()
        self.assertTrue(result)
        self.assertFalse(timer.is_paused)
    
    def test_stop_timer(self):
        """Test stopping a timer"""
        timer = TimerManager()
        timer.start_timer(60, "focus")
        result = timer.stop_timer()
        self.assertTrue(result)
        self.assertFalse(timer.is_running)
    
    def test_get_remaining_time(self):
        """Test getting remaining time"""
        timer = TimerManager()
        timer.start_timer(60, "focus")
        
        # Sleep for 1 second
        time.sleep(1)
        
        # Remaining time should be less than 60 seconds
        remaining = timer.get_remaining_time()
        self.assertLess(remaining, 60)
        self.assertGreater(remaining, 55)  # Allow for some timing variation
    
    def test_get_formatted_time(self):
        """Test getting formatted time"""
        timer = TimerManager()
        timer.start_timer(65, "focus")  # 1 minute and 5 seconds
        
        # Format should be MM:SS
        formatted = timer.get_formatted_time()
        self.assertRegex(formatted, r"^\d{2}:\d{2}$")
    
    def test_get_progress_percentage(self):
        """Test getting progress percentage"""
        timer = TimerManager()
        timer.start_timer(60, "focus")
        
        # Initial progress should be close to 0%
        progress = timer.get_progress_percentage(60)
        self.assertLess(progress, 5)  # Allow for some timing variation
        
        # Sleep for 30 seconds
        timer.stop_timer()
        timer.remaining_seconds = 30
        timer.is_running = True
        
        # Progress should be close to 50%
        progress = timer.get_progress_percentage(60)
        self.assertGreater(progress, 45)
        self.assertLess(progress, 55)

if __name__ == "__main__":
    unittest.main()