import sys
import time
import psutil
import platform
from datetime import datetime
from networking.api_client import APIClient

# Platform-specific imports
if platform.system() == "Windows":
    import ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

def get_active_window_title():
    if platform.system() == "Windows":
        h_wnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(h_wnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(h_wnd, buf, length + 1)
        return buf.value if buf.value else "Unknown"
    else:
        # Placeholder for Mac/Linux
        return "Not Supported on this OS"

class WindowTracker:
    def __init__(self, project_id):
        self.project_id = project_id
        self.active_log = []

    def log_current_window(self):
        """Captures the current active window."""
        title = get_active_window_title()
        timestamp = datetime.now().isoformat()
        
        data = {
            "project_id": self.project_id,
            "window_title": title,
            "timestamp": timestamp
        }
        
        # Try to sync immediately (Fire and forget style for MVP)
        APIClient.sync_activity(data)
        
        return data
