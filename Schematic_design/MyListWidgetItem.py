import sys
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MyListWidgetItem(QListWidgetItem):
    def __init__(self, designator, comment, pin_list):
        super().__init__()
        self.widget = QWidget()

        self.designator_label = QLabel()
        self.designator_label.setText(designator)

        self.designator = designator
        self.comment = comment
        self.pin_list = pin_list

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.designator_label)
        self.hbox.addStretch(1)

        self.widget.setLayout(self.hbox)

        self.setSizeHint(self.widget.sizeHint())


    def get_count(self):
        return len(self.pin_list)