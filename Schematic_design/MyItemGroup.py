import sys
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
#from schematic_main import Test_Demo

class MyItemGroup(QGraphicsItemGroup):
    def __init__(self, designator, comment, pin_list):
        super(MyItemGroup, self).__init__()

        self.designator = designator
        self.comment = comment
        self.pin_list = pin_list
        self.footprint = None

        self.selected = False

        self.setFlags(QGraphicsItemGroup.ItemIsMovable | QGraphicsItemGroup.ItemIsSelectable | QGraphicsItemGroup.ItemSendsGeometryChanges)

        self.designator_signal = pyqtSignal(str)
        self.comment_signal = pyqtSignal(str)

    def itemChange(self, change, value):
        if change == QGraphicsItemGroup.ItemPositionChange:
            newPos = value
            if QApplication.mouseButtons() == Qt.LeftButton:
                xV = round(newPos.x() / 20) * 20
                yV = round(newPos.y() / 20) * 20
                return QPointF(xV, yV)
        return value

    def set_designator(self, new_designator):
        self.designator = new_designator

    def set_footprint(self, new_footprint):
        self.footprint = new_footprint

    def set_comment(self, new_comment):
        self.comment = new_comment

    #def mousePressEvent(self, event):
    #    print("designator:", self.designator)
    #    print("comment:", self.comment)
        #self.designator_signal.emit(str(self.designator))
        #self.designator_signal.emit("123")




        #set_selected_name(self.designator, self.comment, self.pin_list)



        #print("item")




