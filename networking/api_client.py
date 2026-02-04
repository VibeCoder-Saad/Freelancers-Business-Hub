import requests
import os

SERVER_URL = "http://localhost:8000"

class APIClient:
    @staticmethod
    def upload_screenshot(project_id, file_path):
        """Uploads a screenshot to the server."""
        url = f"{SERVER_URL}/upload/screenshot"
        try:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return False
                
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f, 'image/png')}
                params = {'project_id': project_id}
                
                response = requests.post(url, params=params, files=files, timeout=10)
                
            if response.status_code == 200:
                print(f"Uploaded: {file_path}")
                return True
            else:
                print(f"Upload Failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            # Silent fail for demo purposes (User is using local DB)
            if "No connection could be made" in str(e) or "Max retries exceeded" in str(e):
                return False 
            print(f"Network Error during upload: {e}")
            return False

    @staticmethod
    def sync_activity(log_data):
        """Syncs a single activity log entry."""
        url = f"{SERVER_URL}/sync/activity"
        try:
            # Wrap properly as list of ActivityLog schemas
            payload = [{
                "project_id": log_data['project_id'],
                "window_title": log_data['window_title'],
                "start_time": log_data['timestamp'],
                "end_time": log_data['timestamp'] # Using same for now as snapshot
            }]
            
            response = requests.post(url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception as e:
            # Silent fail for demo purposes
            if "No connection could be made" in str(e) or "Max retries exceeded" in str(e):
                return False
            print(f"Sync Error: {e}")
            return False
