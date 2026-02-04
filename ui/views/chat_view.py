from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, 
                               QLineEdit, QPushButton, QListWidgetItem, QLabel, QFrame)
from PySide6.QtCore import Qt, QTimer, QSize
from database.database_manager import send_message, get_messages
from datetime import datetime

class ChatView(QWidget):
    def __init__(self, project_id, user_id, user_role):
        super().__init__()
        self.project_id = project_id
        self.user_id = user_id
        self.user_role = user_role
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("Project Chat")
        header.setObjectName("HeaderLabel")
        self.layout.addWidget(header)
        
        # Message List
        self.msg_list = QListWidget()
        self.msg_list.setStyleSheet("""
            QListWidget { background-color: #1e1e2f; border: 1px solid #45475a; border-radius: 8px; padding: 10px; }
            QListWidget::item { padding: 5px; }
        """)
        self.layout.addWidget(self.msg_list)
        
        # Input Area
        input_layout = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type a message...")
        self.msg_input.setStyleSheet("padding: 8px; border-radius: 4px; background-color: #313244; color: white;")
        self.msg_input.returnPressed.connect(self.handle_send)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("""
            QPushButton { background-color: #89b4fa; color: #1e1e2f; font-weight: bold; padding: 8px 15px; border-radius: 4px; }
            QPushButton:hover { background-color: #74c7ec; }
        """)
        self.send_btn.clicked.connect(self.handle_send)
        
        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(self.send_btn)
        self.layout.addLayout(input_layout)
        
        # Polling for new messages (Simple real-time simulation)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_messages)
        self.timer.start(3000) # Every 3 seconds
        
        self.refresh_messages()

    def handle_send(self):
        text = self.msg_input.text().strip()
        if not text: return
        
        if send_message(self.project_id, self.user_id, text):
            self.msg_input.clear()
            self.refresh_messages()
            # Scroll to bottom
            self.msg_list.scrollToBottom()

    def refresh_messages(self):
        messages = get_messages(self.project_id)
        
        # Smart refresh: only add new ones? 
        # For simple list widget, clearing and re-adding causes flicker but ensures consistency.
        # To avoid flicker, we can check count.
        if self.msg_list.count() == len(messages):
            return # No new messages (naive check)
            
        self.msg_list.clear() # Simplest for MVP
        
        for msg in messages:
            # Format: [Name] Content (Time)
            sender = msg['sender_name']
            content = msg['content']
            ts = msg['timestamp'].split('T')[1][:5]
            
            item_text = f"[{ts}] {sender}: {content}"
            item = QListWidgetItem(item_text)
            
            # Align logic (Self vs Others)
            # Note: msg['sender_id'] check
            if msg['sender_id'] == self.user_id:
                item.setTextAlignment(Qt.AlignRight)
                item.setBackground(Qt.transparent) # Custom widget better for styling bubble, but text align works for now
                # We can't easily style text color per line in standard QListWidget without HTML delegate.
                # Just prefix "Me:"
                item.setText(f"Me: {content}   [{ts}]")
            else:
                 item.setText(f"[{ts}] {sender}: {content}")
            
            self.msg_list.addItem(item)
            
        self.msg_list.scrollToBottom()
