# shared/export_manager.py

import csv
import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog, QMessageBox

def export_to_csv(parent_widget, headers, data, default_filename="export.csv"):
    """
    Exports a list of lists (data) to a CSV file.
    
    Args:
        parent_widget (QWidget): Parent for the file dialog.
        headers (list): List of column names.
        data (list): List of rows, where each row is a list/tuple of values.
        default_filename (str): Default name for the file.
    """
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getSaveFileName(
        parent_widget,
        "Export to CSV",
        default_filename,
        "CSV Files (*.csv);;All Files (*)",
        options=options
    )

    if not file_path:
        return False # User canceled

    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)
        
        QMessageBox.information(parent_widget, "Export Successful", f"Data exported to:\n{file_path}")
        return True
    
    except Exception as e:
        QMessageBox.critical(parent_widget, "Export Error", f"Failed to export data:\n{e}")
        return False
