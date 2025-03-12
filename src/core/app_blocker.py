"""
App blocking functionality for Study Timer Pro
"""

import platform
import subprocess
import psutil

def block_application(app_name):
    """
    Block an application by terminating its process
    
    Args:
        app_name: Name of the application to block
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if platform.system() == "Windows":
            # Try multiple variations of the app name
            for exe_name in [f"{app_name}.exe", app_name]:
                try:
                    subprocess.run(["taskkill", "/IM", exe_name, "/F"],
                                 check=False,
                                 capture_output=True)
                except:
                    pass
                
        # On macOS
        elif platform.system() == "Darwin":
            try:
                subprocess.run(["killall", app_name], check=False, capture_output=True)
            except:
                pass
                
        # On Linux
        elif platform.system() == "Linux":
            try:
                subprocess.run(["killall", app_name], check=False, capture_output=True)
            except:
                pass
        
        return True
    except Exception as e:
        print(f"Error blocking {app_name}: {e}")
        return False

def unblock_application(app_name):
    """
    Unblock an application (no action needed, just stops monitoring)
    
    Args:
        app_name: Name of the application to unblock
    
    Returns:
        bool: Always returns True
    """
    # We don't actually start the app, just allow it to be opened
    return True

def monitor_applications(app_list):
    """
    Check if any of the applications in the list are running
    
    Args:
        app_list: List of application names to check
    
    Returns:
        list: List of running applications from the provided list
    """
    running_apps = []
    
    for proc in psutil.process_iter(['name']):
        try:
            for app in app_list:
                if app.lower() in proc.info['name'].lower():
                    running_apps.append(app)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return running_apps

def is_admin():
    """
    Check if the application is running with administrator privileges
    
    Returns:
        bool: True if running as admin, False otherwise
    """
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        elif platform.system() in ["Darwin", "Linux"]:
            return os.geteuid() == 0
    except:
        pass
    
    return False