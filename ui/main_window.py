# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QStyle
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

# Import Sidebar
from .widgets.sidebar import Sidebar

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
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        # Object name for styling
        self.setObjectName("MainWindow")

        # --- Main Layout Container ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Horizontal Layout: Sidebar (Left) | Content (Right)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0) # No margins for full immersion
        self.main_layout.setSpacing(0)

        # --- 1. Sidebar ---
        self.sidebar = Sidebar()
        self.main_layout.addWidget(self.sidebar)

        # --- 2. Main Content Area (Stacked) ---
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentContainer") # For optional styling
        self.main_layout.addWidget(self.content_stack)

        # --- Instantiate Views ---
        self.dashboard_tab = DashboardView()
        self.project_hub_tab = ProjectHubView()
        self.time_tracking_tab = TimeTrackingView()
        self.invoice_tab = InvoiceView()
        self.expense_tab = ExpenseView()
        self.client_tab = ClientView()
        self.settings_tab = SettingsView()

        # Add views to stack (Order matches sidebar index)
        self.content_stack.addWidget(self.dashboard_tab)      # Index 0
        self.content_stack.addWidget(self.project_hub_tab)    # Index 1
        self.content_stack.addWidget(self.time_tracking_tab)  # Index 2
        self.content_stack.addWidget(self.invoice_tab)        # Index 3
        self.content_stack.addWidget(self.expense_tab)        # Index 4
        self.content_stack.addWidget(self.client_tab)         # Index 5
        self.content_stack.addWidget(self.settings_tab)       # Index 6

        # --- Connect Signals ---
        self.sidebar.page_changed.connect(self.switch_page)

        # Initial Load
        self.switch_page(0)

    def switch_page(self, index):
        """Switches the stacked widget page and refreshes data."""
        self.content_stack.setCurrentIndex(index)
        
        current_widget = self.content_stack.widget(index)
        if hasattr(current_widget, 'refresh_data'):
            try:
                current_widget.refresh_data()
            except Exception as e:
                print(f"Error refreshing page {index}: {e}")