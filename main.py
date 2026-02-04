# main.py


import sys
import os

# --- DISABLE GPU ACCELERATION TO FIX FLICKERING ON NON-GPU LAPTOPS ---
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu --disable-software-rasterizer"

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
        # 3. Apply the modern dark theme GLOBALLY to the application
        app.setStyleSheet(MODERN_STYLESHEET)
        
        # 2. Only after a successful login, create the MainWindow.
        #    Get the role from the login dialog (default to Freelancer if missing)
        role = getattr(login_dialog, 'user_role', 'Freelancer')
        user_id = getattr(login_dialog, 'user_id', None)
        username = getattr(login_dialog, 'username', None)
        
        main_window = MainWindow(user_role=role, user_id=user_id, username=username)
        
        # main_window.setStyleSheet(MODERN_STYLESHEET) # Removed: Applied globally above
            
        main_window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)