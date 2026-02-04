from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QFrame, QScrollArea, QSizePolicy)
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDrag, QPixmap

class KanbanCard(QFrame):
    def __init__(self, project_data, parent=None):
        super().__init__(parent)
        self.project_data = project_data
        self.setObjectName("KanbanCard")
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QVBoxLayout(self)
        
        title = QLabel(project_data.get("name", "Untitled"))
        title.setObjectName("KanbanCardTitle")
        title.setWordWrap(True)
        
        client = QLabel(f"Client: {project_data.get('client_name', 'Unknown')}")
        client.setObjectName("KanbanCardDetail")
        
        budget = QLabel(f"${project_data.get('budget', 0):,.2f}")
        budget.setObjectName("KanbanCardBudget")
        
        layout.addWidget(title)
        layout.addWidget(client)
        layout.addWidget(budget)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(str(self.project_data.get("id"))) # Pass ID as data
            drag.setMimeData(mime)
            drag.setPixmap(self.grab())
            drag.setHotSpot(event.position().toPoint())
            drag.exec(Qt.MoveAction)

class KanbanColumn(QWidget):
    card_dropped = Signal(int, str) # project_id, new_status

    def __init__(self, title, status_key, parent=None):
        super().__init__(parent)
        self.status_key = status_key
        self.setObjectName("KanbanColumn")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel(title)
        header.setObjectName("KanbanColumnHeader")
        header.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(header)
        
        # Scroll Area for Cards
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName("KanbanScroll")
        
        self.content_widget = QWidget()
        self.content_widget.setObjectName("KanbanContent")
        self.card_layout = QVBoxLayout(self.content_widget)
        self.card_layout.setAlignment(Qt.AlignTop)
        self.card_layout.setSpacing(10)
        
        self.scroll.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll)
        
        self.setAcceptDrops(True)

    def add_card(self, project_data):
        card = KanbanCard(project_data)
        self.card_layout.addWidget(card)

    def clear_cards(self):
        while self.card_layout.count():
            item = self.card_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        project_id = int(event.mimeData().text())
        self.card_dropped.emit(project_id, self.status_key)
        event.accept()

class KanbanBoard(QWidget):
    status_changed = Signal(int, str) # Re-emit for controller

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(15)
        
        # Define Columns
        self.columns = {}
        cols_config = [
            ("To Do", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed")
        ]
        
        for title, key in cols_config:
            col = KanbanColumn(title, key)
            col.card_dropped.connect(self.status_changed.emit)
            self.layout.addWidget(col)
            self.columns[key] = col

    def load_projects(self, projects):
        # Clear existing
        for col in self.columns.values():
            col.clear_cards()
            
        # Distribute projects
        for p in projects:
            # Check if p is a tuple (SQlite Row) or dict
            # Assuming main logic converts rows to dicts, but let's be safe if it's raw
            # Standardizing on Dict for UI
            p_data = p if isinstance(p, dict) else {
                "id": p[0], "name": p[1], "client_name": "Client X", "budget": 0.0, "status": p[4] if len(p)>4 else "Pending"
            }
            
            # Fallback status
            status = p_data.get("status", "Pending")
            if status not in self.columns:
                status = "Pending"
                
            self.columns[status].add_card(p_data)
