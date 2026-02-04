from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                               QLabel, QListWidget, QScrollArea, QGridLayout, 
                               QFrame, QStyle, QTabWidget)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                               QLabel, QListWidget, QScrollArea, QGridLayout, 
                               QFrame, QStyle, QTabWidget, QPushButton, QDialog, 
                               QLineEdit, QDialogButtonBox, QMessageBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from database.database_manager import (get_all_projects_with_client_name, 
                                       get_activity_logs, get_screenshots_for_project,
                                       create_invitation)
from networking.websocket_client import WebSocketClient
import os

from PySide6.QtCore import Qt, QSize, QTimer

# New Image Viewer Class
class ImageViewerDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Evidence Viewer")
        self.resize(800, 600)
        self.setStyleSheet("background-color: #1e1e2f;")
        
        layout = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.label.setText("Failed to load image.")
            self.label.setStyleSheet("color: white;")
            
        layout.addWidget(self.label)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("background-color: #f38ba8; color: #1e1e2f; padding: 10px; border-radius: 5px; font-weight: bold;")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

class ClientDashboardView(QWidget):
    def __init__(self, client_id=None):
        super().__init__()
        self.client_id = client_id
        self.ws_client = WebSocketClient(self)
        self.ws_client.message_received.connect(self.handle_live_update)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        self.setup_ui()
        self.refresh_data()
        
        # --- Local Polling for Real-Time Simulation (since Server might not be running) ---
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.load_project_data)
        self.poll_timer.start(5000) # Poll every 5 seconds

    def setup_ui(self):
        # Header
        header = QLabel("Monitoring Dashboard")
        header.setObjectName("HeaderLabel")
        header.setStyleSheet("color: #ffffff; font-size: 24px; font-weight: bold;")
        
        # New Invite Button
        invite_btn = QPushButton("New Project Invite")
        invite_btn.setStyleSheet("""
            QPushButton { background-color: #a6e3a1; color: #1e1e2f; font-weight: bold; padding: 8px 15px; border-radius: 6px; }
            QPushButton:hover { background-color: #94e2d5; }
        """)
        invite_btn.clicked.connect(self.show_invite_dialog)
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(invite_btn)
        
        self.layout.addLayout(header_layout)
        
        # Project Selector
        control_layout = QHBoxLayout()
        self.project_combo = QComboBox()
        self.project_combo.setPlaceholderText("Select Project to Monitor")
        self.project_combo.currentIndexChanged.connect(self.load_project_data)
        control_layout.addWidget(QLabel("Monitoring Project:"))
        control_layout.addWidget(self.project_combo, 1)
        control_layout.addStretch(2)
        self.layout.addLayout(control_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #45475a; background: #1e1e2f; }
            QTabBar::tab { background: #313244; color: #cdd6f4; padding: 10px; }
            QTabBar::tab:selected { background: #89b4fa; color: #1e1e2f; font-weight: bold; }
        """)
        
        self.activity_tab = QWidget()
        self.screenshot_tab = QWidget()
        
        self.setup_activity_tab()
        self.setup_screenshot_tab()
        
        self.tabs.addTab(self.activity_tab, "Activity Timeline")
        self.tabs.addTab(self.screenshot_tab, "Evidence Gallery")
        
        self.layout.addWidget(self.tabs)

    def setup_activity_tab(self):
        layout = QVBoxLayout(self.activity_tab)
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet("background-color: #181825; border: none; color: #cdd6f4;")
        layout.addWidget(self.activity_list)

    def setup_screenshot_tab(self):
        layout = QVBoxLayout(self.screenshot_tab)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #181825; border: none;")
        
        self.gallery_content = QWidget()
        self.gallery_layout = QGridLayout(self.gallery_content)
        self.gallery_layout.setSpacing(10)
        
        scroll.setWidget(self.gallery_content)
        layout.addWidget(scroll)

    def refresh_data(self):
        self.project_combo.clear()
        projects = get_all_projects_with_client_name()
        for p in projects:
            self.project_combo.addItem(f"{p['name']} ({p['client_name']})", userData=p['id'])

    def load_project_data(self):
        project_id = self.project_combo.currentData()
        if not project_id: return
        
        # Connect WS
        self.ws_client.connect_to_project(project_id)
        
        # Load Activity
        self.activity_list.clear()
        logs = get_activity_logs(project_id)
        for log in logs:
            title = log['window_title'] or "Unknown Activity"
            time = log['start_time'].split('T')[1][:5]
            self.activity_list.addItem(f"[{time}] Active Window: {title}")
            
        # Load Screenshots
        # Clear previous items
        for i in reversed(range(self.gallery_layout.count())): 
            self.gallery_layout.itemAt(i).widget().setParent(None)
            
        screenshots = get_screenshots_for_project(project_id)
        row, col = 0, 0
        MAX_COLS = 3
        
        for shot in screenshots:
            self.add_screenshot_to_gallery(shot, row, col)
            col += 1
            if col >= MAX_COLS:
                col = 0
                row += 1
    
    def add_screenshot_to_gallery(self, shot, row=0, col=0):
        # Helper to add widget to gallery (Used by load and live update)
        # Note: Layout management for live updates is tricky with Grid, simplified here
        path = shot['file_path'] or shot.get('url') # Handle API vs DB naming if needed
        if os.path.exists(path):
            card = QFrame()
            card.setStyleSheet("background-color: #313244; border-radius: 8px;")
            card_layout = QVBoxLayout(card)
            
            lbl = QLabel()
            pixmap = QPixmap(path)
            lbl.setPixmap(pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lbl.setAlignment(Qt.AlignCenter)
            
            ts = shot.get('timestamp', 'Now')
            if 'T' in ts: ts = ts.split('T')[1][:8]
            
            t_lbl = QLabel(ts)
            t_lbl.setAlignment(Qt.AlignCenter)
            t_lbl.setStyleSheet("color: #a6adc8; font-size: 10px;")
            
            card_layout.addWidget(lbl)
            card_layout.addWidget(t_lbl)
            
            # Make card clickable
            # Use a transparent button overlay or event filter. Simplest is a button over the image.
            # Or reimplement mousePressEvent. 
            # Let's wrap image in a clickable button style for simplicity or just event filter.
            # QFrame doesn't have clicked signal. 
            # We can replace QFrame with QPushButton acting as a container? No.
            # Let's use mousePressEvent on the label. Requires subclassing or event filter.
            # Quicker way: transparent button on top?
            # Creating a Custom Clickable Label
            
            lbl.mousePressEvent = lambda event, p=path: self.open_image_viewer(p)
            lbl.setCursor(Qt.PointingHandCursor)
            
            # If manually calling, find next spot? 
            # For simplicity, we just add to the end or refresh
            if self.gallery_layout.count() > 0 and row == 0 and col == 0:
                 # Logic to find empty spot is complex, for MVP just append
                 pass

            self.gallery_layout.addWidget(card, row, col)

    def open_image_viewer(self, path):
        viewer = ImageViewerDialog(path, self)
        viewer.exec()

    def handle_live_update(self, data):
        # Handle "new_activity" and "new_screenshot"
        msg_type = data.get("type")
        
        if msg_type == "new_activity":
             for item in data.get("data", []):
                 title = item.get('window_title', "Unknown")
                 time = datetime.now().strftime("%H:%M") 
                 self.activity_list.insertItem(0, f"[{time}] Active Window: {title} (LIVE)")

        elif msg_type == "new_screenshot":
            # Just trigger a reload or prepend if possible
            # Reloading is safer to ensure order
            self.load_project_data()
            print("New Screenshot Received!")

    def show_invite_dialog(self):
        if not self.client_id:
             QMessageBox.warning(self, "Error", "Client ID not found. Please re-login.")
             return
             
        dialog = InviteFreelancerDialog(self)
        if dialog.exec() == QDialog.Accepted:
            project_name = dialog.project_name.text()
            freelancer = dialog.freelancer_username.text()
            try:
                rate = float(dialog.rate.text())
            except ValueError: 
                rate = 0.0
            
            if create_invitation(project_name, self.client_id, freelancer, rate):
                QMessageBox.information(self, "Success", "Invitation sent successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to create invitation.")

class InviteFreelancerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Invite Freelancer to Project")
        self.setStyleSheet("background-color: #1e1e2f; color: #ffffff;")
        self.setFixedWidth(400)
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Project Name:"))
        self.project_name = QLineEdit()
        self.project_name.setStyleSheet("background-color: #313244; color: white; padding: 5px; border-radius: 4px;")
        layout.addWidget(self.project_name)
        
        layout.addWidget(QLabel("Freelancer Username:"))
        self.freelancer_username = QLineEdit()
        self.freelancer_username.setStyleSheet("background-color: #313244; color: white; padding: 5px; border-radius: 4px;")
        layout.addWidget(self.freelancer_username)
        
        layout.addWidget(QLabel("Hourly Rate ($):"))
        self.rate = QLineEdit()
        self.rate.setPlaceholderText("0.00")
        self.rate.setStyleSheet("background-color: #313244; color: white; padding: 5px; border-radius: 4px;")
        layout.addWidget(self.rate)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
