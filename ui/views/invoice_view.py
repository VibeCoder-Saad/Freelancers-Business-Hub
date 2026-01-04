# ui/views/invoice_view.py

import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QDialog, QFormLayout, QMessageBox,
                               QHeaderView, QDialogButtonBox, QLabel, QComboBox,
                               QDateEdit)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from database.database_manager import (get_all_clients, get_client_by_id, get_all_projects_with_client_name,
                                       get_unbilled_time_for_project, create_invoice_from_time_entries,
                                       get_next_invoice_number, update_invoice_pdf_path,
                                       get_all_invoices_with_details, get_all_settings,
                                       delete_invoice)
from shared.pdf_generator import create_invoice_pdf

class InvoiceView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        header = QLabel("Invoices"); header.setObjectName("HeaderLabel")
        self.layout.addWidget(header)
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(5)
        self.invoices_table.setHorizontalHeaderLabels(["Invoice #", "Client", "Issue Date", "Status", "Amount"])
        self.invoices_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.invoices_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.invoices_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.invoices_table)

        # --- NEW: Button Layout ---
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.delete_invoice_button = QPushButton("Delete Selected"); self.delete_invoice_button.setIcon(QIcon("assets/icons/trash-2.svg"))
        self.add_invoice_button = QPushButton("Create New Invoice"); self.add_invoice_button.setIcon(QIcon("assets/icons/plus-circle.svg"))
        button_layout.addWidget(self.delete_invoice_button)
        button_layout.addWidget(self.add_invoice_button)
        self.layout.addLayout(button_layout)
        
        self.add_invoice_button.clicked.connect(self.show_create_invoice_dialog)
        self.delete_invoice_button.clicked.connect(self.delete_selected_invoice)

    def refresh_data(self):
        """Refreshes the invoice list and stores the ID in each row."""
        invoices = get_all_invoices_with_details()
        self.invoices_table.setRowCount(len(invoices))
        for row, invoice in enumerate(invoices):
            inv_num_item = QTableWidgetItem(invoice['invoice_number'])
            inv_num_item.setData(Qt.UserRole, invoice['id']) # Store the ID
            
            self.invoices_table.setItem(row, 0, inv_num_item)
            self.invoices_table.setItem(row, 1, QTableWidgetItem(invoice['client_name']))
            self.invoices_table.setItem(row, 2, QTableWidgetItem(invoice['issue_date']))
            self.invoices_table.setItem(row, 3, QTableWidgetItem(invoice['status']))
            self.invoices_table.setItem(row, 4, QTableWidgetItem(f"${invoice.get('total_amount', 0):.2f}"))

    def show_create_invoice_dialog(self):
        dialog = self.CreateInvoiceDialog(self)
        if dialog.exec() == QDialog.Accepted:
            invoice_data, line_items, time_entry_ids, client_id = dialog.get_data()
            if not line_items: QMessageBox.warning(self, "Empty Invoice", "Cannot create an invoice with no line items."); return
            client_data = get_client_by_id(client_id)
            company_details = get_all_settings()
            invoice_id = create_invoice_from_time_entries(invoice_data, line_items, time_entry_ids)
            pdf_path = create_invoice_pdf(invoice_data, line_items, client_data, company_details)
            if pdf_path: update_invoice_pdf_path(invoice_id, pdf_path)
            self.refresh_data()
            
    def delete_selected_invoice(self):
        selected_items = self.invoices_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an invoice from the table to delete."); return

        inv_item = self.invoices_table.item(selected_items[0].row(), 0)
        inv_num = inv_item.text()
        inv_id = inv_item.data(Qt.UserRole)

        reply = QMessageBox.question(self, "Confirm Deletion",
                                     f"Are you sure you want to delete invoice '{inv_num}'?\n"
                                     "Associated time entries will be marked as 'un-billed' again.",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_invoice(inv_id)
            self.refresh_data()
            QMessageBox.information(self, "Success", f"Invoice '{inv_num}' has been deleted.")

    class CreateInvoiceDialog(QDialog):
        # This nested class code is unchanged and correct.
        def __init__(self, parent=None):
            super().__init__(parent); self.setWindowTitle("Create Invoice from Project Time"); self.setMinimumWidth(600)
            self.layout = QVBoxLayout(self); self.line_items = []; self.time_entry_ids = []
            form = QFormLayout(); self.project_combo = QComboBox(); self.project_combo.setPlaceholderText("Select a project with unbilled hours")
            self.invoice_number_label = QLabel(get_next_invoice_number()); self.issue_date = QDateEdit(QDate.currentDate()); self.due_date = QDateEdit(QDate.currentDate().addDays(30))
            form.addRow("Invoice Number:", self.invoice_number_label); form.addRow("Generate from Project:", self.project_combo)
            form.addRow("Issue Date:", self.issue_date); form.addRow("Due Date:", self.due_date); self.layout.addLayout(form)
            self.generate_button = QPushButton("Generate Line Items"); self.generate_button.setIcon(QIcon("assets/icons/plus-circle.svg")); self.layout.addWidget(self.generate_button)
            self.items_table = QTableWidget(); self.items_table.setColumnCount(4); self.items_table.setHorizontalHeaderLabels(["Description", "Hours", "Rate", "Amount"])
            self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.layout.addWidget(self.items_table)
            self.total_label = QLabel("Total: $0.00"); self.total_label.setStyleSheet("font-weight: bold; font-size: 16px;"); self.layout.addWidget(self.total_label, alignment=Qt.AlignRight)
            self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel); self.button_box.button(QDialogButtonBox.Save).setText("Save Invoice"); self.layout.addWidget(self.button_box)
            self.button_box.accepted.connect(self.accept); self.button_box.rejected.connect(self.reject); self.generate_button.clicked.connect(self.generate_line_items)
            self.populate_projects()
        def populate_projects(self):
            self.projects = get_all_projects_with_client_name()
            for p in self.projects: self.project_combo.addItem(f"{p['name']} ({p['client_name']})", userData=p)
        def generate_line_items(self):
            project = self.project_combo.currentData()
            if not project: QMessageBox.warning(self, "No Project Selected", "Please select a project."); return
            unbilled_entries = get_unbilled_time_for_project(project['id'])
            if not unbilled_entries:
                QMessageBox.information(self, "No Unbilled Time", "No unbilled time entries found for this project.")
                self.line_items.clear(); self.time_entry_ids.clear(); self.items_table.setRowCount(0); self.total_label.setText("Total: $0.00")
                return
            self.line_items.clear(); self.time_entry_ids.clear(); self.items_table.setRowCount(len(unbilled_entries)); total = 0.0; rate = project.get('rate', 0.0)
            for row, entry in enumerate(unbilled_entries):
                hours = entry['duration_minutes'] / 60.0; amount = hours * rate; desc = f"Work from {datetime.fromisoformat(entry['start_time']).strftime('%Y-%m-%d')}: {entry.get('description', 'General Work')}"
                self.items_table.setItem(row, 0, QTableWidgetItem(desc)); self.items_table.setItem(row, 1, QTableWidgetItem(f"{hours:.2f}")); self.items_table.setItem(row, 2, QTableWidgetItem(f"${rate:.2f}")); self.items_table.setItem(row, 3, QTableWidgetItem(f"${amount:.2f}"))
                self.line_items.append({"description": desc, "quantity": hours, "rate": rate, "amount": amount}); self.time_entry_ids.append(entry['id']); total += amount
            self.total_label.setText(f"Total: ${total:.2f}")
        def get_data(self):
            project = self.project_combo.currentData(); total = sum(item['amount'] for item in self.line_items)
            invoice_data = {"invoice_number": self.invoice_number_label.text(), "client_id": project['client_id'], "issue_date": self.issue_date.date().toString(Qt.ISODate), "due_date": self.due_date.date().toString(Qt.ISODate), "total_amount": total}
            return invoice_data, self.line_items, self.time_entry_ids, project['client_id']