# ui/views/expense_view.py

import datetime
import os
import shutil
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QPushButton, QDialog, QFormLayout, QLineEdit, QMessageBox,
                               QHeaderView, QDialogButtonBox, QLabel, QComboBox,
                               QDoubleSpinBox, QDateEdit, QFileDialog)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from database.database_manager import add_expense, get_all_expenses

class ExpenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log New Expense")
        self.setMinimumWidth(450)
        self.receipt_path = ""

        layout = QFormLayout(self)
        self.desc_input = QLineEdit()
        self.cat_input = QComboBox(); self.cat_input.addItems(["Software", "Hardware", "Marketing", "Travel", "Office Supplies", "Other"])
        self.amount_input = QDoubleSpinBox(); self.amount_input.setRange(0, 100000); self.amount_input.setPrefix("$ ")
        self.date_input = QDateEdit(QDate.currentDate())
        self.receipt_button = QPushButton("Attach Receipt..."); self.receipt_button.clicked.connect(self.attach_receipt)
        
        layout.addRow("Description:", self.desc_input)
        layout.addRow("Category:", self.cat_input)
        layout.addRow("Amount:", self.amount_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow(self.receipt_button)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def attach_receipt(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Receipt File", "", "Images (*.png *.jpg *.jpeg);;Documents (*.pdf)")
        if path:
            self.receipt_path = path
            self.receipt_button.setText(os.path.basename(path))

    def get_data(self):
        saved_path = None
        if self.receipt_path:
            dest_dir = os.path.join(os.getcwd(), 'data', 'receipts')
            os.makedirs(dest_dir, exist_ok=True)
            # Create a unique filename to avoid overwrites
            filename, file_extension = os.path.splitext(os.path.basename(self.receipt_path))
            unique_filename = f"{filename}_{int(datetime.now().timestamp())}{file_extension}"
            saved_path = os.path.join(dest_dir, unique_filename)
            shutil.copy(self.receipt_path, saved_path)

        return {
            "description": self.desc_input.text(),
            "category": self.cat_input.currentText(),
            "amount": self.amount_input.value(),
            "expense_date": self.date_input.date().toString(Qt.ISODate),
            "receipt_path": saved_path
        }

class ExpenseView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20); self.layout.setSpacing(15)

        header = QLabel("Expense Tracker"); header.setObjectName("HeaderLabel")
        self.layout.addWidget(header)
        
        self.expense_table = QTableWidget(); self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(["Date", "Description", "Category", "Amount"])
        self.expense_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.expense_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.layout.addWidget(self.expense_table)
        
        self.add_button = QPushButton("Log New Expense"); self.add_button.setIcon(QIcon("assets/icons/plus-circle.svg"))
        self.add_button.setFixedWidth(200)
        self.add_button.clicked.connect(self.show_add_expense_dialog)
        self.layout.addWidget(self.add_button, alignment=Qt.AlignRight)

    def refresh_data(self):
        expenses = get_all_expenses()
        self.expense_table.setRowCount(len(expenses))
        for row, expense in enumerate(expenses):
            self.expense_table.setItem(row, 0, QTableWidgetItem(expense['expense_date']))
            self.expense_table.setItem(row, 1, QTableWidgetItem(expense['description']))
            self.expense_table.setItem(row, 2, QTableWidgetItem(expense['category']))
            self.expense_table.setItem(row, 3, QTableWidgetItem(f"${expense['amount']:.2f}"))

    def show_add_expense_dialog(self):
        dialog = ExpenseDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if not data['description'] or data['amount'] == 0:
                QMessageBox.warning(self, "Input Error", "Description and amount are required.")
                return
            add_expense(**data)
            self.refresh_data()