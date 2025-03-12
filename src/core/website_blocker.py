"""
Website blocking functionality for Study Timer Pro
"""

import os
import platform

def get_hosts_path():
    """
    Get the hosts file path based on the operating system
    
    Returns:
        str: Path to the hosts file
    """
    if platform.system() == "Windows":
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

def block_website(site):
    """
    Block a website by adding it to the hosts file
    
    Args:
        site: Website to block
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        PermissionError: If the hosts file cannot be modified
    """
    hosts_path = get_hosts_path()
    
    # Ensure the site has a domain format
    if not site.startswith("www.") and not site.startswith("http"):
        if "." not in site:
            site = f"www.{site}.com"
        elif not site.startswith("www."):
            site = f"www.{site}"
    
    # Remove http/https prefix if present
    if site.startswith("http://"):
        site = site[7:]
    elif site.startswith("https://"):
        site = site[8:]
    
    try:
        with open(hosts_path, 'r') as hosts_file:
            content = hosts_file.read()
            
            # Check if site is already blocked
            if site in content:
                return True
        
        with open(hosts_path, 'a') as hosts_file:
            hosts_file.write(f"\n127.0.0.1 {site}")
            # Also block non-www version if www version is provided
            if site.startswith("www."):
                hosts_file.write(f"\n127.0.0.1 {site[4:]}")
            # Also block www version if non-www version is provided
            else:
                hosts_file.write(f"\n127.0.0.1 www.{site}")
        
        return True
    except PermissionError:
        raise PermissionError("Need administrator privileges to block websites")
    except Exception as e:
        print(f"Error blocking website {site}: {e}")
        return False

def unblock_website(site):
    """
    Unblock a website by removing it from the hosts file
    
    Args:
        site: Website to unblock
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        PermissionError: If the hosts file cannot be modified
    """
    hosts_path = get_hosts_path()
    
    try:
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        
        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if site not in line:
                    hosts_file.write(line)
        
        return True
    except PermissionError:
        raise PermissionError("Need administrator privileges to unblock websites")
    except Exception as e:
        print(f"Error unblocking website {site}: {e}")
        return False

def is_website_blocked(site):
    """
    Check if a website is blocked
    
    Args:
        site: Website to check
    
    Returns:
        bool: True if blocked, False otherwise
    """
    hosts_path = get_hosts_path()
    
    try:
        with open(hosts_path, 'r') as hosts_file:
            content = hosts_file.read()
            return site in content
    except Exception as e:
        print(f"Error checking if website {site} is blocked: {e}")
        return False

def unblock_all_websites(website_list):
    """
    Unblock all websites in the list
    
    Args:
        website_list: List of websites to unblock
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        PermissionError: If the hosts file cannot be modified
    """
    hosts_path = get_hosts_path()
    
    try:
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()
        
        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if not any(site in line for site in website_list):
                    hosts_file.write(line)
        
        return True
    except PermissionError:
        raise PermissionError("Need administrator privileges to unblock websites")
    except Exception as e:
        print(f"Error unblocking all websites: {e}")
        return False