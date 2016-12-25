import sys
import matplotlib.pyplot as plt

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
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.2, bottom=0.2)
        self.axes.set_xlabel("theta")
        self.axes.set_ylabel("u(t,theta)")

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, self.fig)
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

    def redraw(self, function, t):
        ran = arange(0.0, 3.14, 0.01)

        s = [function.function_u(x, t) for x in ran]
        self.axes.plot(ran, s)
        self.draw()

    def clear(self):
        self.axes.clear()
        self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QWidget(self)

        self.main_linear = QVBoxLayout(self.main_widget)

        self.cEditText = QLineEdit(self.main_widget)
        self.add_edit_text("c", self.cEditText, "1.5")

        self.kEditText = QLineEdit(self.main_widget)
        self.add_edit_text("K", self.kEditText, "0.015")

        self.rEditText = QLineEdit(self.main_widget)
        self.add_edit_text("R", self.rEditText, "2")

        self.betaEditText = QLineEdit(self.main_widget)
        self.add_edit_text("Beta", self.betaEditText, "0.1")

        self.epsEditText = QLineEdit(self.main_widget)
        self.add_edit_text("Eps", self.epsEditText, "0.001")

        self.tEditText = QLineEdit(self.main_widget)
        self.add_edit_text("t", self.tEditText, "1")

        self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)

        self.main_linear.addWidget(self.sc)

        hBox = QHBoxLayout(self.main_widget)
        self.t_label = QLabel(self.main_widget)
        self.e_label = QLabel(self.main_widget)
        self.t_label.setText("Теоритическая оценка ряда: ")
        self.e_label.setText("Экспериментальная оценка ряда: ")
        hBox.addWidget(self.t_label)
        hBox.addWidget(self.e_label)
        self.main_linear.addLayout(hBox)

        self.clearAxes = QPushButton('Clear axes', self)
        self.clearAxes.clicked.connect(self.clearFigure)

        self.button = QPushButton('Rebuild', self)
        self.button.clicked.connect(self.repaint)

        self.main_linear.addWidget(self.clearAxes)
        self.main_linear.addWidget(self.button)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def clearFigure(self):
        self.sc.clear()


    def repaint(self):
        c = float(self.cEditText.text())
        k = float(self.kEditText.text())
        R = float(self.rEditText.text())
        beta = float(self.betaEditText.text())
        t = float(self.tEditText.text())
        eps = float(self.epsEditText.text())
        function = ComputeFunction(c, k, R, beta, t, eps)
        self.sc.redraw(function, t)

        self.t_label.setText("Теоритическая оценка ряда: %d" % function.get_theory_limit())
        self.e_label.setText("Экспериментальная оценка ряда: %d" % function.get_experimental_limit(1, 2))

        pass

    def add_edit_text(self, caption, edit_text, value=""):
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
