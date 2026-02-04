from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QStyle, QApplication, 
                               QSpacerItem, QSizePolicy)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon

class Sidebar(QWidget):
    """
    A modern, vertical sidebar navigation widget.
    Emits `page_changed(int)` when a button is clicked.
    """
    page_changed = Signal(int)

    def __init__(self, parent=None, user_role="Freelancer"):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)  # Fixed width for the sidebar

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 20, 10, 20)
        self.layout.setSpacing(8)

        # --- 1. App Logo / Title Area ---
        title_text = "Freelancer Hub" if user_role == "Freelancer" else "Client Portal"
        self.logo_label = QLabel(title_text)
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
        
        # Helper to get standard icons
        style = QApplication.style()
        
        # Define the buttons: (Label, Icon)
        all_items = [
            ("Dashboard", style.standardIcon(QStyle.SP_ComputerIcon)),
            ("Projects", style.standardIcon(QStyle.SP_DirIcon)), 
            ("Time Tracking", style.standardIcon(QStyle.SP_FileDialogDetailedView)),
            ("Invoices", style.standardIcon(QStyle.SP_FileIcon)),
            ("Expenses", style.standardIcon(QStyle.SP_DialogDiscardButton)),
            ("Clients", style.standardIcon(QStyle.SP_DirHomeIcon)),
            ("Settings", style.standardIcon(QStyle.SP_BrowserReload)),
        ]

        if user_role == "Client":
            # Filter for Client: Dashboard, Projects, Invoices, Settings
            # Indices: 0, 1, 3, 6 (Note: We just list the items we want)
            nav_items = [
                all_items[0], # Dashboard
                all_items[1], # Projects
                all_items[3], # Invoices
                all_items[6]  # Settings
            ]
        else:
            nav_items = all_items

        for i, (label, icon) in enumerate(nav_items):
            btn = QPushButton(label)
            btn.setIcon(icon)
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
