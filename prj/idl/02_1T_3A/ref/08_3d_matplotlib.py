#!/usr/bin/env python
import sys
import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rcParams['backend.qt5']='PySide2'
import pylab

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2 import QtWidgets

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # generate the plot
    fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
    ax = fig.add_subplot(111)
    ax.plot([0,1])
    
    canvas = FigureCanvas(fig)
    print('\r\n canvas type:', type(canvas))

    win = QMainWindow()
    win.setCentralWidget(canvas)

    win.show()

    sys.exit(app.exec_())

# https://scipy-cookbook.readthedocs.io/items/Matplotlib_PySide.html