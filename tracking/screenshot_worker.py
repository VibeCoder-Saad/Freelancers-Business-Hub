from PySide6.QtCore import QThread, Signal
import pyautogui
import os
import time
from datetime import datetime
from database.database_manager import log_screenshot, update_screenshot_upload_status
from networking.api_client import APIClient

SCREENSHOT_DIR = os.path.join("data", "screenshots")

class ScreenshotWorker(QThread):
    screenshot_taken = Signal(str) # Path of the screenshot

    def __init__(self, project_id, interval_seconds=600):
        super().__init__()
        self.project_id = project_id
        self.interval = interval_seconds
        self.running = True

    def run(self):
        # Ensure directory exists
        project_dir = os.path.join(SCREENSHOT_DIR, str(self.project_id))
        os.makedirs(project_dir, exist_ok=True)

        while self.running:
            try:
                # Take Screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"scr_{timestamp}.png"
                filepath = os.path.join(project_dir, filename)
                
                screenshot = pyautogui.screenshot()
                screenshot.save(filepath)
                
                # Log to DB (Local)
                log_screenshot(self.project_id, filepath)
                
                # Upload to Server (Sync)
                if APIClient.upload_screenshot(self.project_id, filepath):
                     update_screenshot_upload_status(filepath, 1)
                
                self.screenshot_taken.emit(filepath)
                
                # Sleep
                for _ in range(self.interval):
                    if not self.running: break
                    time.sleep(1)
            except Exception as e:
                print(f"Screenshot Error: {e}")
                time.sleep(60) # Retry after 1 min on error

    def stop(self):
        self.running = False
        self.wait()
