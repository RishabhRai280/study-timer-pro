#!/usr/bin/env python3
"""
Study Timer Pro - A comprehensive Pomodoro timer application with productivity features
"""

import os
import sys
import tkinter as tk
from ui.main_window import StudyTimerApp

def main():
    """Main entry point for the application"""
    # Ensure resources directory is accessible
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    # Create and run the application
    root = tk.Tk()
    app = StudyTimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()