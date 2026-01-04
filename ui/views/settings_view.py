# ui/views/settings_view.py

import os
import shutil
from datetime import datetime
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QMessageBox,
                               QFileDialog, QLabel, QFormLayout, QLineEdit, QGroupBox)
from PySide6.QtGui import QIcon
from database.database_manager import get_all_settings, save_setting

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # --- Company Profile Group ---
        profile_group = QGroupBox("Company Profile for Invoices")
        profile_layout = QFormLayout(profile_group)
        self.company_name_input = QLineEdit()
        self.company_name_input.setPlaceholderText("e.g., Vibe Coder LLC")
        self.company_address_input = QLineEdit()
        self.company_address_input.setPlaceholderText("e.g., 123 Innovation Drive, Tech City")
        
        self.logo_path_input = QLineEdit()
        self.logo_path_input.setPlaceholderText("No logo selected")
        self.logo_path_input.setReadOnly(True)
        
        logo_button = QPushButton("Browse for Logo File...")
        logo_button.clicked.connect(self.browse_logo)
        
        profile_layout.addRow("Company Name:", self.company_name_input)
        profile_layout.addRow("Company Address:", self.company_address_input)
        profile_layout.addRow("Company Logo:", self.logo_path_input)
        profile_layout.addRow(logo_button)
        
        save_profile_button = QPushButton("Save Profile Settings")
        save_profile_button.setIcon(QIcon("assets/icons/plus-circle.svg"))
        save_profile_button.clicked.connect(self.save_profile_settings)
        profile_layout.addRow(save_profile_button)
        self.layout.addWidget(profile_group)

        # --- Data Management Group ---
        data_group = QGroupBox("Data Management")
        data_layout = QVBoxLayout(data_group)
        
        # Database Actions
        db_actions_layout = QHBoxLayout()
        backup_button = QPushButton("Backup Database"); backup_button.setIcon(QIcon("assets/icons/database.svg"))
        restore_button = QPushButton("Restore Backup"); restore_button.setIcon(QIcon("assets/icons/database.svg"))
        db_actions_layout.addWidget(backup_button)
        db_actions_layout.addWidget(restore_button)
        
        # Export Actions
        export_layout = QHBoxLayout()
        self.export_projects_btn = QPushButton("Export Projects (CSV)")
        self.export_projects_btn.setIcon(QIcon("assets/icons/download.svg"))
        self.export_clients_btn = QPushButton("Export Clients (CSV)")
        self.export_clients_btn.setIcon(QIcon("assets/icons/users.svg"))
        export_layout.addWidget(self.export_projects_btn)
        export_layout.addWidget(self.export_clients_btn)
        
        data_layout.addLayout(db_actions_layout)
        data_layout.addWidget(QLabel("Export Data:"))
        data_layout.addLayout(export_layout)

        backup_button.clicked.connect(self.backup_database)
        restore_button.clicked.connect(self.restore_database)
        self.export_projects_btn.clicked.connect(self.export_projects)
        self.export_clients_btn.clicked.connect(self.export_clients)

        self.layout.addWidget(data_group)

        self.layout.addStretch()
        self.load_settings()

    def load_settings(self):
        """Loads all saved settings from the database and populates the fields."""
        settings = get_all_settings()
        self.company_name_input.setText(settings.get('company_name', ''))
        self.company_address_input.setText(settings.get('company_address', ''))
        self.logo_path_input.setText(settings.get('logo_path', ''))

    def browse_logo(self):
        """Opens a file dialog to select a logo image."""
        path, _ = QFileDialog.getOpenFileName(self, "Select Logo Image", "", "Image Files (*.png *.jpg)")
        if path:
            self.logo_path_input.setText(path)

    def save_profile_settings(self):
        """Saves all profile settings to the database."""
        save_setting('company_name', self.company_name_input.text())
        save_setting('company_address', self.company_address_input.text())
        save_setting('logo_path', self.logo_path_input.text())
        QMessageBox.information(self, "Success", "Company profile settings have been saved successfully.")

    def backup_database(self):
        db_path = os.path.join(os.getcwd(), 'database', 'freelancer_hub.db')
        if not os.path.exists(db_path):
            QMessageBox.warning(self, "No Database", "Database file not found."); return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"freelancer_hub_backup_{timestamp}.db"
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Database Backup", backup_name, "Database Files (*.db)")
        if save_path:
            try:
                shutil.copy(db_path, save_path)
                QMessageBox.information(self, "Success", f"Database successfully backed up to:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Backup Failed", f"An error occurred: {e}")

    def restore_database(self):
        reply = QMessageBox.warning(self, "Confirm Restore", 
                                    "Restoring from a backup will OVERWRITE all current data.\nThis action cannot be undone. Are you sure you want to continue?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No: return

        db_path = os.path.join(os.getcwd(), 'database', 'freelancer_hub.db')
        backup_path, _ = QFileDialog.getOpenFileName(self, "Select Backup to Restore", "", "Database Files (*.db)")

        if backup_path:
            try:
                shutil.copy(backup_path, db_path)
                QMessageBox.information(self, "Success", "Database successfully restored.\nPlease restart the application for changes to take effect.")
            except Exception as e:
                QMessageBox.critical(self, "Restore Failed", f"An error occurred: {e}")

    def export_projects(self):
        from database.database_manager import get_all_projects_with_client_name
        from shared.export_manager import export_to_csv
        
        # Fetch Data
        raw_data = get_all_projects_with_client_name() # Returns list of dicts
        
        # Prepare for CSV (order matters)
        headers = ["Project ID", "Name", "Client", "Rate", "Status"]
        rows = []
        for p in raw_data:
            rows.append([
                p.get("id"),
                p.get("name"),
                p.get("client_name"),
                f"${p.get('rate', 0)}/hr",
                p.get("status", "Pending")
            ])
            
        export_to_csv(self, headers, rows, "projects_export.csv")

    def export_clients(self):
        from database.database_manager import get_all_clients
        from shared.export_manager import export_to_csv
        
        raw_data = get_all_clients()
        headers = ["Client ID", "Name", "Email", "Phone"]
        rows = []
        for c in raw_data:
            rows.append([c.get("id"), c.get("name"), c.get("email"), c.get("phone")])
            
        export_to_csv(self, headers, rows, "clients_export.csv")