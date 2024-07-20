import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from import_ui import import_ui
from component import *
import numpy as np
import time
from PyQt5.QtCore import *

class Canvas(QLabel):
    def __init__(self):
        super().__init__()

        canvas = QPixmap(1300, 1000)
        canvas.fill(QColor('white'))
        self.setPixmap(canvas)
        self.pen_color = QColor('#000')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("原理图绘制")