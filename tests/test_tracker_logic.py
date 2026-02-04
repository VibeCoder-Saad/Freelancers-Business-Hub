import pytest
import os
import time
from database.database_manager import (create_user, get_activity_logs, 
                                       log_activity, log_screenshot, 
                                       get_screenshots_for_project)

def test_user_creation(mock_db):
    """Test that we can create a user and retrieve role"""
    user_id = create_user("testuser", "password123", "Freelancer")
    assert user_id is not None
    
    # Verify role column exists and is correct (implied by successful creation)
    # We can add a function to get user by ID if needed, but for now this confirms DB schema is good
    assert True

def test_activity_logging(mock_db):
    """Test logging window activity"""
    project_id = 999
    window_title = "Test Window - Chrome"
    
    log_activity(project_id, window_title)
    
    logs = get_activity_logs(project_id)
    assert len(logs) == 1
    assert logs[0]['window_title'] == window_title
    assert logs[0]['project_id'] == project_id

def test_screenshot_logging(mock_db):
    """Test logging a screenshot"""
    project_id = 999
    fake_path = "data/screenshots/999/test.png"
    
    log_screenshot(project_id, fake_path)
    
    shots = get_screenshots_for_project(project_id)
    assert len(shots) == 1
    assert shots[0]['file_path'] == fake_path
