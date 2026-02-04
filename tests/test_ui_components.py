import pytest
from PySide6.QtWidgets import QApplication
import sys

# Ensure one QApplication exists
@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.views.client_dashboard_view import ClientDashboardView

def test_login_window_loads(qapp, mock_db):
    """Verify Login Window loads without error"""
    window = LoginWindow()
    assert window is not None
    window.close()

def test_freelancer_dashboard_loads(qapp, mock_db):
    """Verify MainWindow loads in Freelancer mode"""
    # Initialize with Freelancer role
    window = MainWindow(user_role="Freelancer")
    
    # Verify Sync Tabs exist (Index 2 is Time Tracking)
    assert window.content_stack.count() >= 5
    # Force load of the view to check for crashes
    window.switch_page(2) 
    assert window.time_tracking_tab is not None
    window.close()

def test_client_dashboard_loads(qapp, mock_db):
    """Verify MainWindow loads in Client mode"""
    # Initialize with Client role
    window = MainWindow(user_role="Client")
    
    # Verify Client Dashboard is at Index 0
    assert isinstance(window.content_stack.widget(0), ClientDashboardView)
    window.close()
