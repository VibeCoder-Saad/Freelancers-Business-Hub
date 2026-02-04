from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                               QTextEdit, QCheckBox, QHBoxLayout)
from PySide6.QtCore import Qt

class PrivacyPolicyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Privacy & Monitoring Consent")
        self.setFixedSize(500, 600)
        self.layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Transparency Agreement")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #89b4fa;")
        self.layout.addWidget(title)
        
        # Policy Text
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setHtml("""
            <h3 style='color: #cba6f7;'>Data Monitoring Disclosure</h3>
            <p>To provide clients with "Proof of Work", this application creates a rigorous audit trail of your activity 
            <b>ONLY while the Timer is running</b>.</p>
            
            <p><b>What We Track:</b></p>
            <ul>
                <li><b>Screenshots:</b> Captured randomly every ~10 minutes.</li>
                <li><b>Window Titles:</b> The name of the active application (e.g., "Photoshop", "VS Code").</li>
                <li><b>Activity Levels:</b> Interaction intensity (clicks/keystrokes).</li>
            </ul>
            
            <p><b>What We DO NOT Track:</b></p>
            <ul>
                <li>❌ Keystroke content (passwords, messages).</li>
                <li>❌ Webcam or Microphone.</li>
                <li>❌ Files on your computer (other than the screenshots we take).</li>
            </ul>
            
            <p><b>Your Rights:</b></p>
            <p>You can pause tracking at any time by stopping the timer. 
            All data is stored locally before being synced. You have the right to review it.</p>
        """)
        self.layout.addWidget(self.text_area)
        
        # Consent Checkbox
        self.consent_checkbox = QCheckBox("I have read and agree to the monitoring terms.")
        self.consent_checkbox.setStyleSheet("color: #bac2de; font-size: 14px;")
        self.layout.addWidget(self.consent_checkbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Accept & Create Account")
        self.accept_button.setObjectName("AcceptButton")
        self.accept_button.setStyleSheet("""
            QPushButton { background-color: #a6e3a1; color: #1e1e2f; font-weight: bold; padding: 10px; border-radius: 5px; }
            QPushButton:disabled { background-color: #45475a; color: #a6adc8; }
        """)
        self.accept_button.setEnabled(False)
        
        self.cancel_button = QPushButton("Decline")
        self.cancel_button.setStyleSheet("background-color: #f38ba8; color: #1e1e2f; font-weight: bold; padding: 10px; border-radius: 5px;")
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.accept_button)
        self.layout.addLayout(button_layout)
        
        # Logic
        self.consent_checkbox.stateChanged.connect(self.toggle_accept)
        self.accept_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
    def toggle_accept(self):
        self.accept_button.setEnabled(self.consent_checkbox.isChecked())
