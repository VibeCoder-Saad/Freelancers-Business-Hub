# main.py

import sys
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from database.database_manager import user_exists
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from ui.styles import MODERN_STYLESHEET

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # --- NO GLOBAL STYLESHEET IS SET HERE ---

    # --- Secure Login Flow ---
    if not user_exists():
        reply = QMessageBox.information(None, "Welcome!",
                                        "No user account found. Let's create the primary admin account.",
                                        QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            sys.exit(0)

    # 1. Create your custom LoginWindow. It will handle its own styling internally.
    login_dialog = LoginWindow()
    
    if login_dialog.exec() == QDialog.Accepted:
        # 2. Only after a successful login, create the MainWindow.
        main_window = MainWindow()
        
        # 3. Apply the modern dark theme ONLY to the MainWindow.
        main_window.setStyleSheet(MODERN_STYLESHEET)
        
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)