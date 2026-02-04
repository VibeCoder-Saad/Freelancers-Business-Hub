from fastapi.testclient import TestClient
from server.main import app
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "running", "message": "Freelancer Hub Sync Server is Active"}

def test_activity_sync():
    payload = [{
        "project_id": 1,
        "window_title": "Test Window",
        "start_time": "2026-01-04T12:00:00",
        "end_time": "2026-01-04T12:00:30"
    }]
    response = client.post("/sync/activity", json=payload)
    assert response.status_code == 200
    assert response.json()['status'] == "synced"
    assert response.json()['count'] == 1

def test_screenshot_upload():
    # Create a dummy file
    dummy_file = "test_scr.png"
    with open(dummy_file, "wb") as f:
        f.write(b"fake image data")
        
    try:
        with open(dummy_file, "rb") as f:
            response = client.post(
                "/upload/screenshot",
                params={"project_id": 1},
                files={"file": ("test_scr.png", f, "image/png")}
            )
            
        assert response.status_code == 200
        assert response.json()['status'] == "success"
        
        # Verify file exists in upload dir
        # The server stores in server_uploads/1/test_scr.png
        expected_path = os.path.join("server_uploads", "1", "test_scr.png")
        assert os.path.exists(expected_path)
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)
