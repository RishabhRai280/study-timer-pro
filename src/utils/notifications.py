"""
Notification system for Study Timer Pro
"""

import platform
import os

def show_notification(title, message, timeout=10):
    """
    Show a desktop notification
    
    Args:
        title: Notification title
        message: Notification message
        timeout: Notification timeout in seconds
    
    Returns:
        bool: True if notification was shown, False otherwise
    """
    try:
        # Try using plyer if available
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_name='Study Timer Pro',
                timeout=timeout,
            )
            return True
        except ImportError:
            pass
        
        # Platform-specific fallbacks
        if platform.system() == "Windows":
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=timeout, threaded=True)
                return True
            except ImportError:
                pass
            
            # Try using Windows PowerShell
            try:
                import subprocess
                powershell_cmd = f'powershell -command "& {{Add-Type -AssemblyName System.Windows.Forms; ' \
                               f'$notify = New-Object System.Windows.Forms.NotifyIcon; ' \
                               f'$notify.Icon = [System.Drawing.SystemIcons]::Information; ' \
                               f'$notify.Visible = $true; ' \
                               f'$notify.ShowBalloonTip({timeout * 1000}, \'{title}\', \'{message}\', ' \
                               f'[System.Windows.Forms.ToolTipIcon]::None)}}"'
                subprocess.Popen(powershell_cmd, shell=True)
                return True
            except:
                pass
        
        elif platform.system() == "Darwin":  # macOS
            try:
                os.system(f"""
                osascript -e 'display notification "{message}" with title "{title}"'
                """)
                return True
            except:
                pass
        
        elif platform.system() == "Linux":
            try:
                os.system(f'notify-send "{title}" "{message}"')
                return True
            except:
                pass
        
        return False
    except Exception as e:
        print(f"Failed to show notification: {e}")
        return False

class NotificationManager:
    """
    Manages notifications for the application
    """
    
    def __init__(self):
        """Initialize the notification manager"""
        self.enabled = True
    
    def send_notification(self, title, message, timeout=10):
        """
        Send a notification if enabled
        
        Args:
            title: Notification title
            message: Notification message
            timeout: Notification timeout in seconds
        
        Returns:
            bool: True if notification was shown, False otherwise
        """
        if not self.enabled:
            return False
        
        return show_notification(title, message, timeout)
    
    def enable(self):
        """Enable notifications"""
        self.enabled = True
    
    def disable(self):
        """Disable notifications"""
        self.enabled = False