# ui/views/client_view.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QDialog, QFormLayout, QLineEdit,
                               QMessageBox, QHeaderView, QDialogButtonBox, QLabel, QStyle)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
# Import the new delete function
from database.database_manager import add_client, get_all_clients, delete_client

class ClientDialog(QDialog):
    # This class is unchanged from your provided code.
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Add New Client"); self.setMinimumWidth(450)
        layout = QFormLayout(self); self.name_input = QLineEdit(); self.email_input = QLineEdit(); self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("e.g., 123 Main St, Anytown, USA")
        layout.addRow(QLabel("Full Name / Company Name:"), self.name_input); layout.addRow(QLabel("Contact Email:"), self.email_input); layout.addRow(QLabel("Mailing Address:"), self.address_input)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel); buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); layout.addRow(buttons)
    def get_data(self):
        return {"name": self.name_input.text(), "email": self.email_input.text(), "address": self.address_input.text()}

class ClientView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self); self.layout.setContentsMargins(20, 20, 20, 20); self.layout.setSpacing(15)
        header = QLabel("Client Management"); header.setObjectName("HeaderLabel"); self.layout.addWidget(header)
        
        self.clients_table = QTableWidget(); self.clients_table.setColumnCount(3)
        self.clients_table.setHorizontalHeaderLabels(["Client Name", "Email Address", "Mailing Address"]); self.clients_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.clients_table.setSelectionBehavior(QTableWidget.SelectRows); self.clients_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.clients_table)

        # --- NEW: Button Layout ---
        button_layout = QHBoxLayout()
        button_layout.addStretch(1) # Pushes buttons to the right

        self.delete_client_button = QPushButton("Delete Client")
        self.delete_client_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        self.delete_client_button.setFixedWidth(180)
        self.delete_client_button.clicked.connect(self.delete_selected_client)
        button_layout.addWidget(self.delete_client_button)

        self.add_client_button = QPushButton("Add New Client")
        self.add_client_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.add_client_button.setFixedWidth(180)
        self.add_client_button.clicked.connect(self.show_add_client_dialog)
        button_layout.addWidget(self.add_client_button)
        self.layout.addLayout(button_layout)

    def refresh_data(self):
        """Refreshes the client list and crucially stores the ID in each row."""
        clients = get_all_clients()
        self.clients_table.setRowCount(len(clients))
        for row, client in enumerate(clients):
            # --- CRITICAL CHANGE ---
            # Store the database ID in the item's data role. This is invisible to the user
            # but allows us to retrieve the ID when a row is selected.
            name_item = QTableWidgetItem(client.get("name"))
            name_item.setData(Qt.UserRole, client.get("id"))
            
            self.clients_table.setItem(row, 0, name_item)
            self.clients_table.setItem(row, 1, QTableWidgetItem(client.get("email")))
            self.clients_table.setItem(row, 2, QTableWidgetItem(client.get("address")))

    def show_add_client_dialog(self):
        dialog = ClientDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['name']:
                QMessageBox.warning(self, "Input Error", "Client Name is a required field.")
                return
            add_client(data['name'], data['email'], data['address'])
            self.refresh_data()

    def delete_selected_client(self):
        """Handles the logic for deleting a client."""
        selected_items = self.clients_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a client from the table to delete.")
            return

        # Get the item from the first column of the selected row
        selected_row = selected_items[0].row()
        client_item = self.clients_table.item(selected_row, 0)
        client_name = client_item.text()
        # Retrieve the stored database ID
        client_id = client_item.data(Qt.UserRole)

        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete the client '{client_name}'?\n"
                                     "WARNING: This will also delete all associated projects, time entries, and invoices. This action cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            delete_client(client_id)
            self.refresh_data() # Refresh the table to show the client has been removed
            QMessageBox.information(self, "Success", f"Client '{client_name}' has been deleted.")