from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtGui import QIcon

class Sidebar(QWidget):
    """
    A modern, vertical sidebar navigation widget.
    Emits `page_changed(int)` when a button is clicked.
    """
    page_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)  # Fixed width for the sidebar

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.layout.setSpacing(8)

        # --- 1. App Logo / Title Area ---
        self.logo_label = QLabel("Freelancer Hub")
        self.logo_label.setObjectName("SidebarTitle")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setObjectName("SidebarLine")
        self.layout.addWidget(line)

        self.layout.addSpacing(10)

        # --- 2. Navigation Buttons ---
        self.buttons = []
        
        # Define the buttons: (Label, IconPath)
        # Note: Ensure these paths exist or use standard resource logic
        nav_items = [
            ("Dashboard", "assets/icons/activity.svg"),
            ("Projects", "assets/icons/briefcase.svg"),
            ("Time Tracking", "assets/icons/clock.svg"),
            ("Invoices", "assets/icons/dollar-sign.svg"),
            ("Expenses", "assets/icons/shopping-cart.svg"),
            ("Clients", "assets/icons/users.svg"),
            ("Settings", "assets/icons/settings.svg"),
        ]

        for i, (label, icon_path) in enumerate(nav_items):
            btn = QPushButton(label)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(20, 20))
            btn.setCheckable(True)
            btn.setAutoExclusive(True) # Only one button active at a time
            btn.setObjectName("SidebarButton")
            
            # Connect click to signal
            # We use a closure (lambda) to capture the index `i`
            btn.clicked.connect(lambda checked, idx=i: self.page_changed.emit(idx))
            
            self.layout.addWidget(btn)
            self.buttons.append(btn)

        # Select the first button by default
        if self.buttons:
            self.buttons[0].setChecked(True)

        # --- 3. Spacer to push content up ---
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # --- 4. User Profile / Bottom Area (Optional) ---
        # self.user_label = QLabel("Admin User")
        # self.user_label.setObjectName("SidebarFooter")
        # self.layout.addWidget(self.user_label)

    def set_active_index(self, index):
        """Programmatically set the active button."""
        if 0 <= index < len(self.buttons):
            self.buttons[index].setChecked(True)
