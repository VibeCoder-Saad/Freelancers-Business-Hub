# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

# Import all final views
from .views.dashboard_view import DashboardView
from .views.project_hub_view import ProjectHubView
from .views.time_tracking_view import TimeTrackingView
from .views.invoice_view import InvoiceView
from .views.expense_view import ExpenseView
from .views.client_view import ClientView
from .views.settings_view import SettingsView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Freelancer's Business Hub - Professional Edition")
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowIcon(QIcon("assets/icons/briefcase.svg"))

        # --- THE FIX IS HERE ---
        # We give the main window a name so the stylesheet can target it specifically.
        self.setObjectName("MainWindow")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setIconSize(QSize(20, 20))
        self.main_layout.addWidget(self.tab_widget)

        # --- Instantiate and Add All Final Views as Tabs ---
        self.dashboard_tab = DashboardView()
        self.tab_widget.addTab(self.dashboard_tab, QIcon("assets/icons/activity.svg"), "Dashboard")
        
        self.project_hub_tab = ProjectHubView()
        self.tab_widget.addTab(self.project_hub_tab, QIcon("assets/icons/briefcase.svg"), "Projects Hub")
        
        self.time_tracking_tab = TimeTrackingView()
        self.tab_widget.addTab(self.time_tracking_tab, QIcon("assets/icons/clock.svg"), "Time Tracking")
        
        self.invoice_tab = InvoiceView()
        self.tab_widget.addTab(self.invoice_tab, QIcon("assets/icons/dollar-sign.svg"), "Invoices")
        
        self.expense_tab = ExpenseView()
        self.tab_widget.addTab(self.expense_tab, QIcon("assets/icons/shopping-cart.svg"), "Expenses")
        
        self.client_tab = ClientView()
        self.tab_widget.addTab(self.client_tab, QIcon("assets/icons/users.svg"), "Clients")
        
        self.settings_tab = SettingsView()
        self.tab_widget.addTab(self.settings_tab, QIcon("assets/icons/settings.svg"), "Settings & Data")

        # --- Connect the signal to refresh data when a tab is clicked ---
        self.tab_widget.currentChanged.connect(self.refresh_current_tab)
        
        # Initial refresh of the first tab
        self.refresh_current_tab(0)

    def refresh_current_tab(self, index):
        current_widget = self.tab_widget.widget(index)
        if hasattr(current_widget, 'refresh_data'):
            try:
                current_widget.refresh_data()
            except Exception as e:
                print(f"Error refreshing tab {index}: {e}")