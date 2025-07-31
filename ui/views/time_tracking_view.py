# ui/views/time_tracking_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QLabel, QTableWidget,
                               QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from database.database_manager import (get_all_projects_with_client_name, start_time_entry,
                                       stop_time_entry, get_time_entries_for_project)
from datetime import datetime, timedelta

class TimeTrackingView(QWidget):
    def __init__(self):
        super().__init__()
        self.current_timer_id = None
        self.timer_start_time = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = QLabel("Time Tracker"); header.setObjectName("HeaderLabel")
        self.layout.addWidget(header)

        # --- Timer Control UI ---
        timer_frame = QFrame(); timer_frame.setObjectName("KPICard")
        timer_layout = QHBoxLayout(timer_frame)
        self.project_combo = QComboBox(); self.project_combo.setPlaceholderText("Select a Project to Track")
        self.description_input = QLineEdit(); self.description_input.setPlaceholderText("What are you working on?")
        self.timer_label = QLabel("00:00:00"); self.timer_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #a6e3a1;")
        self.start_stop_button = QPushButton("Start"); self.start_stop_button.setIcon(QIcon("assets/icons/clock.svg")); self.start_stop_button.setFixedWidth(120)
        
        timer_layout.addWidget(QLabel("Track Time for Project:"))
        timer_layout.addWidget(self.project_combo, 2) # Give more space
        timer_layout.addWidget(self.description_input, 3) # Give more space
        timer_layout.addWidget(self.timer_label)
        timer_layout.addWidget(self.start_stop_button)
        self.layout.addWidget(timer_frame)

        # --- Time Entries Table ---
        self.entries_table = QTableWidget(); self.entries_table.setColumnCount(4)
        self.entries_table.setHorizontalHeaderLabels(["Date", "Duration", "Description", "Billed?"])
        self.entries_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.entries_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.entries_table)
        
        # --- Connections ---
        self.start_stop_button.clicked.connect(self.toggle_timer)
        self.project_combo.currentIndexChanged.connect(self.project_changed)
        
        # --- Live Timer ---
        self.live_timer = QTimer(self); self.live_timer.timeout.connect(self.update_display_time)

    def refresh_data(self): # Method called when tab is selected
        self.load_projects()
        self.project_changed()

    def load_projects(self):
        current_selection_id = None
        if self.project_combo.count() > 0:
            current_selection_id = self.project_combo.currentData()['id']

        self.project_combo.clear()
        projects = get_all_projects_with_client_name()
        for p in projects: self.project_combo.addItem(f"{p['name']} ({p['client_name']})", userData=p)
        
        if current_selection_id:
            index = self.project_combo.findData(next((p for p in projects if p['id'] == current_selection_id), None))
            if index != -1: self.project_combo.setCurrentIndex(index)

    def project_changed(self):
        project = self.project_combo.currentData()
        if project: self.refresh_entries_table(project['id'])
        else: self.entries_table.setRowCount(0)

    def refresh_entries_table(self, project_id):
        self.entries_table.setRowCount(0)
        entries = get_time_entries_for_project(project_id)
        for row, entry in enumerate(entries):
            self.entries_table.insertRow(row)
            date = datetime.fromisoformat(entry['start_time']).strftime('%Y-%m-%d')
            duration_minutes = entry.get('duration_minutes', 0)
            duration = str(timedelta(minutes=duration_minutes if duration_minutes else 0))
            billed_status = "Yes" if entry['is_billed'] else "No"
            self.entries_table.setItem(row, 0, QTableWidgetItem(date))
            self.entries_table.setItem(row, 1, QTableWidgetItem(duration))
            self.entries_table.setItem(row, 2, QTableWidgetItem(entry.get('description')))
            self.entries_table.setItem(row, 3, QTableWidgetItem(billed_status))

    def toggle_timer(self):
        if self.live_timer.isActive():
            self.live_timer.stop()
            self.start_stop_button.setText("Start")
            end_time = datetime.now()
            duration = end_time - self.timer_start_time
            duration_minutes = int(duration.total_seconds() / 60)
            description = self.description_input.text() or "General Work"
            
            stop_time_entry(self.current_timer_id, end_time, duration_minutes, description)
            self.refresh_entries_table(self.project_combo.currentData()['id'])
            self.description_input.clear()
            QMessageBox.information(self, "Timer Stopped", f"Logged {duration_minutes} minutes.")
        else:
            project = self.project_combo.currentData()
            if not project:
                QMessageBox.warning(self, "No Project Selected", "Please select a project before starting the timer.")
                return
            self.timer_start_time = datetime.now()
            self.current_timer_id = start_time_entry(project['id'], self.timer_start_time)
            self.live_timer.start(1000) # Update every second
            self.start_stop_button.setText("Stop")

    def update_display_time(self):
        if self.timer_start_time:
            elapsed = datetime.now() - self.timer_start_time
            # Format as H:M:S
            self.timer_label.setText(str(timedelta(seconds=int(elapsed.total_seconds()))))