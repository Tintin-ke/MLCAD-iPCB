import sys
from PyQt5.QtCore import Qt, QMimeData, QByteArray
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QWidget, QLineEdit, QApplication, QSplitter, QHBoxLayout, QListWidget
from PyQt5 import QtWidgets
from Schematic_design.component import Component
import os

class MyListWidget(QListWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

    def mouseMoveEvent(self, event):
        if not(Qt.LeftButton):
            print(event.button())
            print(Qt.LeftButton)
            #print("first if")
            return
        if self.currentItem() == None:
            #$print("second if")
            return
        drag = QDrag(self)
        mime = QMimeData()
        #strtext = self.currentItem().text()
        designator = self.currentItem().designator
        comment = self.currentItem().comment
        pin_list = self.currentItem().pin_list


        ba = QByteArray()
        ba.append(designator)
        ba.append(" ")
        ba.append(comment)
        #ba.append(" ")
        for i in range(0, len(pin_list)):
            ba.append(" ")
            ba.append(pin_list[i][0])
            ba.append(" ")
            ba.append(pin_list[i][1])

        print(ba)


        mime.setData('text/csv', ba)
        drag.setMimeData(mime)
        drag.exec(Qt.CopyAction | Qt.MoveAction)


class MyListWidget_2(QListWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setDragDropOverwriteMode(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

    def mouseMoveEvent(self, event):
        if not(Qt.LeftButton):
            print(event.button())
            print(Qt.LeftButton)
            #print("first if")
            return
        if self.currentItem() == None:
            #$print("second if")
            return
        drag = QDrag(self)
        mime = QMimeData()
        #strtext = self.currentItem().text()
        designator = self.currentItem().designator
        comment = self.currentItem().comment
        pin_list = self.currentItem().pin_list


        ba = QByteArray()
        ba.append(designator)
        ba.append(" ")
        ba.append(comment)

        for i in range(0, len(pin_list)):
            ba.append(" ")
            ba.append(pin_list[i][0])
            ba.append(" ")
            ba.append(pin_list[i][1])

        print(ba)

        mime.setData('text/csv', ba)
        drag.setMimeData(mime)
        drag.exec(Qt.CopyAction | Qt.MoveAction)
