from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem
from PyQt5.Qt import *
import math


class Pin(QGraphicsItem):

    def __init__(self, num, name):
        super(Pin, self).__init__()

        self.pin_num = num
        self.pin_name = name
        self.pin_net = ''

        self.length = 160
        self.start_point = 0

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        #self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)

    def print(self):
        print(self.pin_num)
        print(self.pin_name)
        print(self.pin_net)

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 3))
        painter.setFont(QFont('SimSun', 16))
        painter.setBrush(Qt.black)
        painter.drawLine(0, 0,  self.length, 0)
        painter.drawText(0 - 100, 10, str(self.pin_name))
        painter.drawText(self.length - 30, 0 - 5, str(self.pin_num))

        if self.isSelected():
            pen = QPen(Qt.darkBlue, 3, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect().adjusted(0.5, 0.5, -0.5, -0.5))
        #self.start_point += 50

    def boundingRect(self):
        return QRectF(0 - 100, 0 - 35, 280, 45)         #经验值

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            newPos = value
            if QApplication.mouseButtons() == Qt.LeftButton:
                xV = round(newPos.x() / 20) * 20
                yV = round(newPos.y() / 20) * 20
                return QPointF(xV, yV)
        return value

    def text_rotation(self):
        print("!!!!")

    def set_pin_num(self, num):
        self.pin_num = num

    def set_pin_name(self, name):
        self.pin_name = name

    def set_pin_net(self, net):
        self.pin_net = net

    def get_pin_num(self):
        return self.pin_num

    def get_pin_name(self):
        return self.pin_name

    def get_pin_net(self):
        return self.pin_net

    def mouseDoubleClickEvent(self, event):
        print("double click")



class Pin_left(Pin):
    def __init__(self, num, name):
        super(Pin_left, self).__init__(num, name)
        #self.length = 160

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 3))
        painter.setFont(QFont('SimSun', 16))
        painter.setBrush(Qt.black)
        #painter.drawLine(0, 0,  self.length, 0)
        painter.drawLine(- self.length, 0, 0, 0)

        painter.drawText(5, 10, str(self.pin_name))
        painter.drawText(- self.length + 5, 0 - 5, str(self.pin_num))

        ##
        #num_item = Num_Item(self.pin_num)


        if self.isSelected():
            pen = QPen(Qt.darkBlue, 3, Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect().adjusted(0.5, 0.5, -0.5, -0.5))

    def boundingRect(self):
        return QRectF(0 - 180, 0 - 35, 360, 45)         #经验值
"""
class Name_Item(QGraphicsItem):
    def __init__(self, name):
        super(Name_Item, self).__init__()
        self.name = name

    def paint(self, painter, option, widget=None):
        painter.drawText(5, 10, str(self.name))


class Num_Item(QGraphicsItem):
    def __init__(self, num):
        super(Num_Item, self).__init__()
        self.num = num

    def paint(self, painter, option, widget=None):
        painter.drawText(0, 0, str(self.num))
"""