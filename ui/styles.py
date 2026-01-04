# ui/styles.py

# This stylesheet is for the main application window (dark theme with background).
MODERN_STYLESHEET = """
QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
}

#MainWindow {
    /* --- THE BACKGROUND IMAGE IS SET HERE --- */
    background-image: url(assets/main_background.png);
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed; /* Ensures the background doesn't scroll */
}
#MainWindow, #MainWindow QWidget {
    /* Fallback color if image fails to load */
    background-color: #1e1e2f; 
    color: #cad3f5;
    font-size: 14px;
}

/* --- Make UI elements semi-transparent for the "glass" effect --- */
#ChartFrame, #KPICard, QTableWidget, QHeaderView::section, QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit, QDateEdit {
    background-color: rgba(36, 39, 58, 0.85); /* Semi-transparent version of #24273a */
    border: 1px solid rgba(73, 77, 100, 0.7); /* Semi-transparent version of #494d64 */
    border-radius: 8px;
}

QTabBar::tab {
    background: rgba(30, 30, 47, 0.8);
    color: #b4befe;
    font-weight: bold;
    padding: 12px 22px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: rgba(54, 58, 79, 0.9); /* More opaque when selected */
    color: #ffffff;
}
QTabWidget::pane {
    border: none;
}

/* --- Text and other styles remain the same for readability --- */
#HeaderLabel { 
    background-color: transparent; /* Headers should not have a background */
    font-size: 18px; 
    font-weight: bold; 
    color: #89b4fa; 
    padding-top: 10px; 
    border-bottom: 1px solid rgba(73, 77, 100, 0.7);
    margin-bottom: 5px; 
}
#KPIValue { background-color: transparent; font-size: 28px; font-weight: bold; color: #a6e3a1; }
#KPILabel, #KPITitle { background-color: transparent; font-size: 12px; color: #b4befe; }

QPushButton { 
    background-color: #89b4fa; 
    color: #1e1e2f; 
    font-weight: bold; 
    border: none; 
    border-radius: 5px; 
    padding: 10px 15px; 
    icon-size: 18px; 
}
QPushButton:hover { background-color: #a6e3a1; }

QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit, QDateEdit { 
    padding: 8px; 
    color: #cad3f5; 
}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QTextEdit:focus, QDateEdit:focus { 
    border: 1px solid #cba6f7; 
}

QTableWidget { gridline-color: rgba(73, 77, 100, 0.7); }
QHeaderView::section {
    color: #f5c2e7; 
    font-weight: bold; 
    padding: 10px; 
    border: none; 
    border-bottom: 2px solid #cba6f7;
}
"""