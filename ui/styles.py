# ui/styles.py

# --- MATRIX CONSOLE THEME ---
# High contrast, monospaced, black & green.

MODERN_STYLESHEET = """
/* --- GLOBAL --- */
QWidget {
    background-color: #000000;
    color: #00ff00;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 14px;
}

/* --- SIDEBAR --- */
#Sidebar {
    background-color: #0d0d0d;
    border-right: 2px solid #003300;
    min-width: 200px;
}

#SidebarTitle {
    color: #00ff00;
    font-size: 18px;
    font-weight: bold;
    padding: 15px;
    border-bottom: 2px solid #003300;
    text-transform: uppercase;
    letter-spacing: 2px;
}

#SidebarButton {
    background-color: transparent;
    color: #008f00;
    border: none;
    text-align: left;
    padding: 12px 20px;
    font-family: 'Consolas', monospace;
    font-weight: bold;
}

#SidebarButton:hover {
    background-color: #001a00;
    color: #00ff00;
    border-left: 4px solid #00ff00;
}

#SidebarButton:checked {
    background-color: #003300;
    color: #ffffff;
    border-left: 4px solid #00ff00;
}

/* --- CARDS & CONTAINERS --- */
#ContentContainer, #ChartFrame, #KPICard, #GlassFrame {
    background-color: #050505;
    border: 1px solid #003300;
    border-radius: 0px; /* Sharp corners for Matrix look */
}

/* --- KPI CARDS --- */
#KPICard {
    background-color: #000000;
    border: 1px solid #00ff00;
    min-width: 200px;
    padding: 15px;
}

#KPIValue {
    color: #00ff00;
    font-size: 28px;
    font-weight: bold;
    font-family: 'Consolas', monospace;
    background: transparent;
}

#KPILabel {
    color: #008f00;
    font-size: 12px;
    text-transform: uppercase;
    background: transparent;
}

#KPITitle {
    color: #ffffff;
    font-size: 14px;
    font-weight: bold;
    border-bottom: 1px dashed #003300;
    padding-bottom: 5px;
    margin-bottom: 10px;
    background: transparent;
}

/* --- HEADERS --- */
#HeaderLabel {
    color: #00ff00;
    font-size: 24px;
    font-weight: bold;
    border-bottom: 2px solid #00ff00;
    background: transparent;
    padding-bottom: 10px;
    margin-bottom: 20px;
    text-transform: uppercase;
}

/* --- TABLES --- */
QTableWidget {
    background-color: #000000;
    border: 1px solid #003300;
    gridline-color: #003300;
    color: #00ff00;
    selection-background-color: #003300;
    selection-color: #ffffff;
    font-family: 'Consolas', monospace;
}

QHeaderView::section {
    background-color: #001a00;
    color: #00ff00;
    border: 1px solid #003300;
    padding: 5px;
    font-weight: bold;
    text-transform: uppercase;
}

QTableCornerButton::section {
    background-color: #000000;
    border: 1px solid #003300;
}

/* --- INPUTS --- */
QLineEdit, QTextEdit, QComboBox, QDateEdit, QDoubleSpinBox {
    background-color: #000000;
    border: 1px solid #008f00;
    color: #00ff00;
    padding: 8px;
    border-radius: 0px;
    font-family: 'Consolas', monospace;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #00ff00;
    background-color: #050505;
}

/* --- BUTTONS --- */
QPushButton {
    background-color: #000000;
    border: 1px solid #00ff00;
    color: #00ff00;
    padding: 10px 20px;
    border-radius: 0px;
    font-weight: bold;
    text-transform: uppercase;
}

QPushButton:hover {
    background-color: #00ff00;
    color: #000000;
}

QPushButton:pressed {
    background-color: #ffffff;
    color: #000000;
}

/* --- SCROLLBARS --- */
QScrollBar:vertical {
    background: #000000;
    width: 12px;
    border-left: 1px solid #003300;
}
QScrollBar::handle:vertical {
    background: #003300;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #008f00;
}
"""