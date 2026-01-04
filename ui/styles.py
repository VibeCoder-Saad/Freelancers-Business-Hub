# ui/styles.py

# This stylesheet is for the main application window (dark theme with background).
MODERN_STYLESHEET = """
/* --- GLOBAL RESET & FONTS --- */
QWidget {
    font-family: 'Segoe UI', 'SF Pro Display', 'Helvetica Neue', 'Arial', sans-serif;
    color: #e0e0e0;
}

/* --- MAIN WINDOW BACKGROUND --- */
#MainWindow {
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-color: #1e1e2f; /* Fallback */
}

/* --- SIDEBAR STYLING --- */
#Sidebar {
    background-color: rgba(24, 24, 37, 0.90); /* Dark, semi-transparent sidebar */
    border-right: 1px solid rgba(255, 255, 255, 0.1);
}

#SidebarTitle {
    font-size: 22px;
    font-weight: bold;
    color: #89b4fa; /* Primary Blue Accent */
    padding: 10px;
    background: transparent;
}

#SidebarLine {
    color: rgba(255, 255, 255, 0.1);
}

#SidebarButton {
    background-color: transparent;
    border: none;
    border-radius: 8px;
    color: #a6adc8; /* Muted text */
    text-align: left;
    padding: 12px 20px;
    font-size: 15px;
    font-weight: 500;
}

#SidebarButton:hover {
    background-color: rgba(255, 255, 255, 0.05); /* Subtle highlight */
    color: #ffffff;
}

#SidebarButton:checked {
    background-color: #89b4fa; /* Active Color */
    color: #1e1e2f; /* Text turns dark for contrast */
    font-weight: bold;
}

/* --- GLASSMORPHISM CONTAINERS --- */
/* Used for Dashboards, Cards, Tables */
#ChartFrame, #KPICard, QTableWidget, QHeaderView::section, QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit, QDateEdit, #ContentContainer, #GlassFrame {
    background-color: rgba(30, 30, 46, 0.70); /* Glassy Dark */
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
}

QSplitter::handle {
    background-color: rgba(255, 255, 255, 0.1);
}


/* --- HEADERS --- */
#HeaderLabel { 
    background-color: transparent; 
    font-size: 26px; 
    font-weight: bold; 
    color: #ffffff; 
    padding-bottom: 5px;
    border-bottom: 2px solid #89b4fa;
    margin-bottom: 15px; 
}

/* --- KPIS --- */
#KPIValue { background-color: transparent; font-size: 32px; font-weight: bold; color: #a6e3a1; } /* Green */
#KPILabel { background-color: transparent; font-size: 13px; color: #bac2de; }
#KPITitle { background-color: transparent; font-size: 14px; font-weight: bold; color: #89b4fa; }

/* --- KANBAN BOARD --- */
#KanbanColumn {
    background-color: rgba(30, 30, 46, 0.4);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}
#KanbanColumnHeader {
    font-size: 16px;
    font-weight: bold;
    color: #89b4fa;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0.05);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
}
#KanbanScroll {
    background: transparent;
    border: none;
}
#KanbanContent {
    background: transparent;
}
#KanbanCard {
    background-color: rgba(49, 50, 68, 0.9);
    border-radius: 8px;
    border-left: 4px solid #cba6f7; /* Card Accent */
    margin: 4px;
}
#KanbanCard:hover {
    background-color: rgba(69, 71, 90, 1.0);
    border: 1px solid #89b4fa;
    border-left: 4px solid #cba6f7;
}
#KanbanCardTitle {
    font-size: 14px;
    font-weight: bold;
    color: #ffffff;
}
#KanbanCardDetail {
    font-size: 11px;
    color: #bac2de;
}
#KanbanCardBudget {
    font-size: 12px;
    font-weight: bold;
    color: #a6e3a1; /* Green */
    alignment: right;
}

/* --- BUTTONS (Action Buttons inside pages) --- */
QPushButton { 
    background-color: #89b4fa; 
    color: #1e1e2f; 
    font-weight: bold; 
    border: none; 
    border-radius: 6px; 
    padding: 10px 18px; 
    font-size: 14px;
}
QPushButton:hover { 
    background-color: #b4befe; /* Lighter Blue */
}
QPushButton:pressed {
    background-color: #74c7ec;
}

/* --- FORM INPUTS --- */
QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit, QDateEdit { 
    padding: 10px; 
    color: #ffffff; 
    background-color: rgba(0, 0, 0, 0.2); /* Darker input background */
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QTextEdit:focus, QDateEdit:focus { 
    border: 1px solid #89b4fa; 
    background-color: rgba(0, 0, 0, 0.4);
}

/* --- TABLES --- */
QTableWidget { 
    gridline-color: rgba(255, 255, 255, 0.05); 
    selection-background-color: rgba(137, 180, 250, 0.3); /* Selection Highlight */
}
QHeaderView::section {
    background-color: rgba(30, 30, 46, 0.9);
    color: #89b4fa; 
    font-weight: bold; 
    padding: 12px; 
    border: none; 
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.2);
    min-height: 20px;
    border-radius: 4px;
}
"""