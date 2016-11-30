import sys

import matplotlib
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton

from compute_function import ComputeFunction

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from numpy import arange
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


def compute_initial_figure(self):
    pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        pass

    def redraw(self, function):
        t = arange(0.0, 7.0, 0.1)

        s = [function.function_u(x, 1) for x in t]
        self.axes.plot(t, s)
        self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QWidget(self)

        self.main_linear = QVBoxLayout(self.main_widget)

        self.cEditText = QLineEdit(self.main_widget)
        self.add_edit_text("c", self.cEditText , "2")

        self.kEditText = QLineEdit(self.main_widget)
        self.add_edit_text("K", self.kEditText, "0.01")

        self.rEditText = QLineEdit(self.main_widget)
        self.add_edit_text("R", self.rEditText, "2")

        self.betaEditText = QLineEdit(self.main_widget)
        self.add_edit_text("Beta", self.betaEditText, "0.1")

        self.epsEditText = QLineEdit(self.main_widget)
        self.add_edit_text("eps", self.epsEditText, "1e-7")

        self.tEditText = QLineEdit(self.main_widget)
        self.add_edit_text("t", self.tEditText, "1e-7")

        self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        self.main_linear.addWidget(self.sc)

        self.button = QPushButton('Rebuild', self)
        self.button.clicked.connect(self.repaint)

        self.main_linear.addWidget(self.button)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def repaint(self):
        c = float(self.cEditText.text())
        k = float(self.kEditText.text())
        R = float(self.rEditText.text())
        beta = float(self.betaEditText.text())
        eps = float(self.epsEditText.text())
        t = float(self.tEditText.text())
        function = ComputeFunction(c, k, R, beta, eps, t)
        self.sc.redraw(function)
        pass

    def add_edit_text(self, caption, edit_text, value = ""):
        edit_text.setText(value)
        hBox = QHBoxLayout(self.main_widget)
        label = QLabel(self.main_widget)
        label.setText(caption)
        hBox.addWidget(label)
        hBox.addWidget(edit_text)
        self.main_linear.addLayout(hBox)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.setWindowTitle("Compute")
    aw.show()
    # sys.exit(qApp.exec_())
    app.exec_()
