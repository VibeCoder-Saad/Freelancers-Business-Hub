# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget, QStyle
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

# Import Sidebar
from .widgets.sidebar import Sidebar

# Import all final views
# Import all final views
from .views.dashboard_view import DashboardView
from .views.project_hub_view import ProjectHubView
from .views.time_tracking_view import TimeTrackingView
from .views.invoice_view import InvoiceView
from .views.expense_view import ExpenseView
from .views.client_view import ClientView
from .views.settings_view import SettingsView
from .views.client_dashboard_view import ClientDashboardView

class MainWindow(QMainWindow):
    def __init__(self, user_role="Freelancer", user_id=None, username=None):
        super().__init__()
        self.user_role = user_role
        self.user_id = user_id
        self.username = username
        
        self.setWindowTitle("Freelancer's Business Hub" if user_role == "Freelancer" else "Client Portal")
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
        self.sidebar = Sidebar(user_role=user_role)
        self.main_layout.addWidget(self.sidebar)

        # --- 2. Main Content Area (Stacked) ---
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentContainer") # For optional styling
        self.main_layout.addWidget(self.content_stack)

        # --- Instantiate Component Views ---
        self.project_hub_tab = ProjectHubView()
        self.time_tracking_tab = TimeTrackingView()
        self.invoice_tab = InvoiceView()
        self.expense_tab = ExpenseView()
        self.client_tab = ClientView()
        self.settings_tab = SettingsView()

        # Add views to stack based on Role
        if user_role == "Freelancer":
            self.dashboard_tab = DashboardView(freelancer_username=username, freelancer_id=user_id)
            self.content_stack.addWidget(self.dashboard_tab)      # Index 0
            self.content_stack.addWidget(self.project_hub_tab)    # Index 1
            self.content_stack.addWidget(self.time_tracking_tab)  # Index 2
            self.content_stack.addWidget(self.invoice_tab)        # Index 3
            self.content_stack.addWidget(self.expense_tab)        # Index 4
            self.content_stack.addWidget(self.client_tab)         # Index 5
            self.content_stack.addWidget(self.settings_tab)       # Index 6
        else:
            # Client View
            self.dashboard_tab = ClientDashboardView(client_id=user_id)
            self.content_stack.addWidget(self.dashboard_tab)      # Index 0: Monitor
            self.content_stack.addWidget(self.project_hub_tab)    # Index 1: Projects (View Only ideally)
            self.content_stack.addWidget(self.invoice_tab)        # Index 2: Invoices (Pay)
            self.content_stack.addWidget(self.settings_tab)       # Index 3: Settings

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