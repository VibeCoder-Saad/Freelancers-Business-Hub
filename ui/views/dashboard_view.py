# ui/views/dashboard_view.py

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
                               QTableWidget, QTableWidgetItem, QHeaderView, QPushButton)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from ui.widgets.mpl_chart_widget import MplChartWidget
from database.database_manager import get_dashboard_kpis, get_monthly_income_summary, get_recent_activity
from datetime import datetime, timedelta

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(25)

        # --- MODIFIED: Header with Exit Button ---
        header_layout = QHBoxLayout()
        header_label = QLabel("Dashboard"); header_label.setObjectName("HeaderLabel")
        header_layout.addWidget(header_label)
        header_layout.addStretch(1) # Pushes the button to the right
        
        # --- NEW: Exit Button ---
        exit_button = QPushButton("Exit Application")
        # ASSUMES you have a 'log-out.svg' or similar icon in assets/icons/
        exit_button.setIcon(QIcon("assets/icons/log-out.svg"))
        exit_button.setFixedWidth(180)
        exit_button.clicked.connect(QApplication.instance().quit) # Safely quits the app
        header_layout.addWidget(exit_button)
        self.layout.addLayout(header_layout)

        # --- The rest of the dashboard UI is unchanged ---
        main_grid = QGridLayout(); main_grid.setSpacing(20); self.layout.addLayout(main_grid)
        kpi_layout = QHBoxLayout(); kpi_layout.setSpacing(20)
        self.kpi_revenue = self.create_kpi_card("Total Revenue (All-Time)", "$0.00")
        self.kpi_unpaid = self.create_kpi_card("Outstanding Amount", "$0.00")
        self.kpi_projects = self.create_kpi_card("Active Projects", "0")
        self.kpi_hours = self.create_kpi_card("Hours Logged (This Month)", "0.0")
        kpi_layout.addWidget(self.kpi_revenue[0]); kpi_layout.addWidget(self.kpi_unpaid[0])
        kpi_layout.addWidget(self.kpi_projects[0]); kpi_layout.addWidget(self.kpi_hours[0])
        self.income_chart_frame = QFrame(); self.income_chart_frame.setObjectName("ChartFrame")
        chart_layout = QVBoxLayout(self.income_chart_frame); self.income_chart = MplChartWidget(); chart_layout.addWidget(self.income_chart)
        self.activity_frame = QFrame(); self.activity_frame.setObjectName("ChartFrame")
        activity_layout = QVBoxLayout(self.activity_frame)
        activity_header = QLabel("Recent Activity"); activity_header.setObjectName("KPITitle")
        self.activity_table = QTableWidget(); self.activity_table.setColumnCount(3); self.activity_table.setHorizontalHeaderLabels(["Date", "Project", "Duration"])
        self.activity_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); self.activity_table.setEditTriggers(QTableWidget.NoEditTriggers)
        activity_layout.addWidget(activity_header); activity_layout.addWidget(self.activity_table)
        main_grid.addLayout(kpi_layout, 0, 0, 1, 2); main_grid.addWidget(self.income_chart_frame, 1, 0); main_grid.addWidget(self.activity_frame, 1, 1)
        main_grid.setColumnStretch(0, 2); main_grid.setColumnStretch(1, 1)

    def create_kpi_card(self, title_text, value_text):
        card = QFrame(); card.setObjectName("KPICard"); layout = QVBoxLayout(card)
        title_label = QLabel(title_text); title_label.setObjectName("KPITitle"); value_label = QLabel(value_text); value_label.setObjectName("KPIValue")
        layout.addWidget(title_label); layout.addWidget(value_label); return card, value_label

    def refresh_data(self):
        kpis = get_dashboard_kpis(); income_data = get_monthly_income_summary(months=6); recent_activity = get_recent_activity(limit=5)
        self.kpi_revenue[1].setText(f"${kpis['total_revenue']:.2f}"); self.kpi_unpaid[1].setText(f"${kpis['total_unpaid']:.2f}")
        self.kpi_projects[1].setText(str(kpis['active_projects'])); self.kpi_hours[1].setText(f"{kpis['logged_hours_this_month']:.1f} hrs")
        months = list(income_data.keys()); income = list(income_data.values()); self.income_chart.plot_bar_chart(months, income, "Monthly Revenue (from Paid Invoices)")
        self.activity_table.setRowCount(len(recent_activity))
        for row, activity in enumerate(recent_activity):
            date = datetime.fromisoformat(activity['start_time']).strftime('%Y-%m-%d'); project = activity['project_name']
            duration = str(timedelta(minutes=activity.get('duration_minutes', 0)))
            self.activity_table.setItem(row, 0, QTableWidgetItem(date)); self.activity_table.setItem(row, 1, QTableWidgetItem(project)); self.activity_table.setItem(row, 2, QTableWidgetItem(duration))