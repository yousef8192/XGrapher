

from _XGRAPHER_LOGIC_ import *

from PySide2.QtWidgets import (
    QApplication    ,   # for the Application itself 
    QMainWindow     ,   # for the Main Window
    QWidget         ,   # for widgets 
    QGridLayout     ,   # for Grid Layout
    QMenu           ,   # for the Menu Bar
    QMenuBar        ,   # for the Menu Bar
    QToolBar        ,   # for the tool bar
    QStatusBar      ,   # for the status bar
    QAction         ,   # for the actions
    QPushButton     ,   # for the Push Button
    QLineEdit       ,   # for Display Fields
    QLabel          ,   # for Labels
    QSlider         ,   # for slider
    QSizePolicy         # for sizing policy
)

from PySide2.QtCore import (
    QTimer          ,   # for animation tricks that require timing
    Qt              ,   # for Qt.Vertical in slider 
    QSize               # for sizing icons
) 

from PySide2.QtGui import (
    QIcon           ,   # for the icons
    QPalette            # for checking status bar text color
)

import os   # for os specific operations
import numpy
import matplotlib
import matplotlib.pyplot
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg, FigureCanvas, NavigationToolbar2QT)
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')
numpy.seterr(all='raise')   # Configure NumPy to treat warnings as exceptions



