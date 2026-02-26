from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(facecolor="#1e1e1e")
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

    def plot_bar(self, x, y):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#1e1e1e")
        ax.bar(x, y, color="#2ecc71")
        ax.tick_params(colors="white")
        ax.spines[:].set_color("#444")
        self.canvas.draw()

    def plot_line(self, x, y):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#1e1e1e")
        ax.plot(x, y, color="#2ecc71", linewidth=2)
        ax.tick_params(colors="white")
        ax.spines[:].set_color("#444")
        self.canvas.draw()
        
