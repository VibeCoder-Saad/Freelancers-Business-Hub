# ui/widgets/mpl_chart_widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MplChartWidget(QWidget):
    """A custom widget to embed a Matplotlib chart into a PySide6 application."""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- Matplotlib Figure Setup ---
        # Use a style that complements dark themes
        plt.style.use('dark_background')
        
        # Create a figure with a transparent background to blend with our app's theme
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor('none')
        
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color:transparent;")

        # --- Layout ---
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_bar_chart(self, x_data, y_data, title):
        """Clears the previous plot and draws a new styled bar chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        bars = ax.bar(x_data, y_data, color='#89b4fa') # Blue bars from our theme
        
        # Style the chart elements to match our UI colors
        ax.set_title(title, color='#f5c2e7', weight='bold', fontsize=14) # Pink
        ax.tick_params(axis='x', colors='#b4befe', labelrotation=45) # Lavender
        ax.tick_params(axis='y', colors='#b4befe') # Lavender
        
        # Make the plot area background match our app's surface color
        ax.set_facecolor('#24273a') 
        
        # Remove unnecessary chart lines (spines) for a cleaner look
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Style the remaining axes lines to be subtle
        ax.spines['bottom'].set_color('#494d64')
        ax.spines['left'].set_color('#494d64')
        
        self.figure.tight_layout() # Adjust plot to prevent labels overlapping
        self.canvas.draw()