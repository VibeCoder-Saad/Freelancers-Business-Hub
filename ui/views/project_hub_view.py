# ui/views/project_hub_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
                               QTableWidgetItem, QHeaderView, QSplitter, QPushButton,
                               QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox,
                               QDoubleSpinBox, QDialogButtonBox, QFrame, QTabWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from database.database_manager import (get_all_projects_with_client_name, get_project_details,
                                       get_time_entries_for_project, get_invoices_for_project,
                                       get_project_financial_summary, add_project, get_all_clients,
                                       delete_project)
from datetime import datetime, timedelta

# Import Kanban Board
from ..widgets.kanban_board import KanbanBoard

class ProjectDialog(QDialog):
    """A dialog for adding new projects."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setMinimumWidth(450)
        
        layout = QFormLayout(self)
        self.name_input = QLineEdit()
        self.client_combo = QComboBox()
        self.rate_spinbox = QDoubleSpinBox()
        self.rate_spinbox.setRange(0, 10000); self.rate_spinbox.setPrefix("$ "); self.rate_spinbox.setSuffix("/hr")

        self.populate_clients()
        layout.addRow(QLabel("Project Name:"), self.name_input)
        layout.addRow(QLabel("Client:"), self.client_combo)
        layout.addRow(QLabel("Default Hourly Rate:"), self.rate_spinbox)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def populate_clients(self):
        clients = get_all_clients()
        for client in clients: self.client_combo.addItem(client['name'], userData=client['id'])

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "client_id": self.client_combo.currentData(),
            "rate": self.rate_spinbox.value()
        }

class ProjectHubView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # --- View Switcher (List vs Board) ---
        self.view_tabs = QTabWidget()
        self.layout.addWidget(self.view_tabs)

        # --- Tab 1: List View (Original Splitter) ---
        self.list_view_widget = QWidget()
        list_layout = QVBoxLayout(self.list_view_widget)
        list_layout.setContentsMargins(0, 0, 0, 0)
        
        self.splitter = QSplitter(Qt.Horizontal)
        list_layout.addWidget(self.splitter)

        # Left Panel: Project List
        left_panel = QFrame(); left_panel.setContentsMargins(0,0,10,0)
        left_layout = QVBoxLayout(left_panel)
        header = QLabel("Active Projects"); header.setObjectName("HeaderLabel")
        
        self.projects_table = QTableWidget(); self.projects_table.setColumnCount(2)
        self.projects_table.setHorizontalHeaderLabels(["Project", "Client"])
        self.projects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.projects_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.projects_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        button_layout = QHBoxLayout()
        self.delete_project_button = QPushButton("Delete"); self.delete_project_button.setIcon(QIcon("assets/icons/trash-2.svg"))
        self.add_project_button = QPushButton("New Project"); self.add_project_button.setIcon(QIcon("assets/icons/plus-circle.svg"))
        button_layout.addWidget(self.delete_project_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.add_project_button)
        
        left_layout.addWidget(header)
        left_layout.addWidget(self.projects_table)
        left_layout.addLayout(button_layout)
        
        # Right Panel: Project Dashboard
        self.right_panel = QFrame(); self.right_panel.setContentsMargins(10,0,0,0)
        self.right_layout = QVBoxLayout(self.right_panel)
        self.placeholder_label = QLabel("Select a project to view details"); self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.dashboard_widget = QWidget(); self.dashboard_widget.setVisible(False)
        self.right_layout.addWidget(self.placeholder_label)
        self.right_layout.addWidget(self.dashboard_widget)

        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setSizes([400, 800])
        
        self.projects_table.itemSelectionChanged.connect(self.display_project_dashboard)
        self.add_project_button.clicked.connect(self.show_add_project_dialog)
        self.delete_project_button.clicked.connect(self.delete_selected_project)

        # --- Tab 2: Kanban Board ---
        self.kanban_widget = KanbanBoard()

        # Add tabs
        self.view_tabs.addTab(self.list_view_widget, QIcon("assets/icons/list.svg"), "List View")
        self.view_tabs.addTab(self.kanban_widget, QIcon("assets/icons/trello.svg"), "Task Board")
        
        self.view_tabs.currentChanged.connect(self.on_tab_changed)

    def refresh_data(self):
        """Called when tab is selected. Refreshes data for both views."""
        self.refresh_project_list()
        self.refresh_kanban()
        self.placeholder_label.setVisible(True)
        self.dashboard_widget.setVisible(False)

    def on_tab_changed(self, index):
        if index == 1: # Kanban
            self.refresh_kanban()
        else:
            self.refresh_project_list()

    def refresh_kanban(self):
        """Loads projects into the Kanban Board."""
        projects = get_all_projects_with_client_name() # Returns dicts 
        # Convert to list of dicts if needed, logic is handled inside board
        self.kanban_widget.load_projects(projects)

    def refresh_project_list(self):
        """Refreshes the project list table and stores the project ID in each row."""
        projects = get_all_projects_with_client_name()
        self.projects_table.setRowCount(len(projects))
        for row, project in enumerate(projects):
            name_item = QTableWidgetItem(project["name"])
            name_item.setData(Qt.UserRole, project["id"]) # Store the ID
            self.projects_table.setItem(row, 0, name_item)
            self.projects_table.setItem(row, 1, QTableWidgetItem(project["client_name"]))

    def display_project_dashboard(self):
        """Displays the detailed dashboard for the selected project."""
        selected_items = self.projects_table.selectedItems()
        if not selected_items:
            self.placeholder_label.setVisible(True)
            self.dashboard_widget.setVisible(False)
            return
        
        self.placeholder_label.setVisible(False)
        self.dashboard_widget.setVisible(True)
        project_id = selected_items[0].data(Qt.UserRole)
        
        details = get_project_details(project_id)
        if not details: 
            self.refresh_data()
            return

        financials = get_project_financial_summary(project_id)
        time_entries = get_time_entries_for_project(project_id)
        invoices = get_invoices_for_project(project_id)

        if self.dashboard_widget.layout(): QWidget().setLayout(self.dashboard_widget.layout())
        layout = QVBoxLayout(self.dashboard_widget)

        title = QLabel(details['name']); title.setObjectName("HeaderLabel")
        client = QLabel(f"Client: {details['client_name']}")
        layout.addWidget(title); layout.addWidget(client)
        
        kpi_layout = QHBoxLayout()
        kpi_layout.addWidget(self.create_kpi_widget("Total Hours Logged", f"{financials['total_hours']:.2f} hrs"))
        kpi_layout.addWidget(self.create_kpi_widget("Amount Billed", f"${financials['billed_amount']:.2f}"))
        layout.addLayout(kpi_layout)
        
        time_header = QLabel("Recent Time Entries"); time_header.setObjectName("HeaderLabel")
        layout.addWidget(time_header)
        time_table = self.create_time_table(time_entries); layout.addWidget(time_table)

        invoice_header = QLabel("Associated Invoices"); invoice_header.setObjectName("HeaderLabel")
        layout.addWidget(invoice_header)
        invoice_table = self.create_invoice_table(invoices); layout.addWidget(invoice_table)
        
    def create_kpi_widget(self, label_text, value_text):
        widget = QFrame(); widget.setObjectName("KPICard"); layout = QVBoxLayout(widget)
        value_label = QLabel(value_text); value_label.setObjectName("KPIValue")
        text_label = QLabel(label_text); text_label.setObjectName("KPILabel")
        layout.addWidget(value_label); layout.addWidget(text_label); return widget

    def create_time_table(self, entries):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Date", "Duration", "Description"])
        table.setRowCount(len(entries))
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        for r, entry in enumerate(entries):
            duration_minutes = entry.get('duration_minutes')
            if duration_minutes is None:
                duration_text = "Running..."
            else:
                duration_text = str(timedelta(minutes=duration_minutes))
            date_str = datetime.fromisoformat(entry['start_time']).strftime('%Y-%m-%d %H:%M')
            
            table.setItem(r, 0, QTableWidgetItem(date_str))
            table.setItem(r, 1, QTableWidgetItem(duration_text))
            table.setItem(r, 2, QTableWidgetItem(entry.get('description')))
        return table

    def create_invoice_table(self, invoices):
        table = QTableWidget(); table.setColumnCount(4); table.setHorizontalHeaderLabels(["Invoice #", "Issue Date", "Status", "Amount"])
        table.setRowCount(len(invoices)); table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); table.setEditTriggers(QTableWidget.NoEditTriggers)
        for r, invoice in enumerate(invoices):
            table.setItem(r, 0, QTableWidgetItem(invoice['invoice_number']))
            table.setItem(r, 1, QTableWidgetItem(invoice['issue_date']))
            table.setItem(r, 2, QTableWidgetItem(invoice['status']))
            table.setItem(r, 3, QTableWidgetItem(f"${invoice['total_amount']:.2f}"))
        return table

    def show_add_project_dialog(self):
        dialog = ProjectDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['name'] or not data['client_id']:
                QMessageBox.warning(self, "Input Error", "Project Name and a Client are required."); return
            add_project(data['name'], data['client_id'], data['rate'])
            self.refresh_project_list()

    def delete_selected_project(self):
        selected_items = self.projects_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a project from the list to delete."); return

        project_item = selected_items[0]
        project_name = project_item.text()
        project_id = project_item.data(Qt.UserRole)

        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete the project '{project_name}'?\n"
                                     "WARNING: This will also delete all its time entries. This cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_project(project_id)
            self.refresh_data()
            QMessageBox.information(self, "Success", f"Project '{project_name}' has been deleted.")