#元器件类\
from Schematic_design.pin import Pin
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPixmapItem, QApplication
from PyQt5.QtGui import QPen
from PyQt5.Qt import *
import math
class Component(QGraphicsItem):

    def __init__(self, designator, comment):    #初始化类的属性
        #self.pin_numbers = pin_numbers     #管脚数量
        super(Component, self).__init__()
        self.designator = designator
        self.comment = comment
        self.footprint = None
        #self.pin = pin_info        #管脚名 管脚号
        self.pin = []

        #默认的矩形框的长宽
        self.width = 200
        self.height = 300
        self.pin_width = 100     #管脚的长度

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        #self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        #self.setAcceptHoverEvents(True)

    #def hoverEnterEvent(self, event):
    #    qApp.instance().setOverrideCursor(Qt.OpenHandCursor)
    '''
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        print('x:{0}, y:{1}', format(self.pos().x(), self.pos().y()))
    '''

    def paint(self, painter, option, widget = None):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.yellow)

        count = len(self.pin)

        if count <= 4:
            self.width = 200
            self.height = 300
            painter.drawRect(0, 0, self.width, self.height)

        elif 4 < count <= 8:
            self.width = 300
            self.height = 400
            painter.drawRect(0, 0, self.width, self.height)

        elif 8 < count <= 48:
            self.width = 500
            self.height = 500
            painter.drawRect(0, 0, self.width, self.height)

        elif 48 < count <= 96:
            self.width = 600
            self.height = 600
            painter.drawRect(0, 0, self.width, self.height)

        else:
            self.width = 840
            self.height = 840
            painter.drawRect(0, 0, self.width, self.height)

        if self.isSelected():
            pen = QPen(Qt.darkGreen, 3, Qt.DashLine)
            painter.setPen(pen)
            #painter.setBrush(Qt.NoBrush)
            painter.setBrush(QColor(0, 0, 0, 126))
            painter.drawRect(self.boundingRect().adjusted(0.5, 0.5, -0.5, -0.5))


    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    #位置改变时只能根据背景的网格改变
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            newPos = value
            if QApplication.mouseButtons() == Qt.LeftButton:
                xV = round(newPos.x() / 20) * 20
                yV = round(newPos.y() / 20) * 20
                return QPointF(xV, yV)
        return value


    """
    def mousePressEvent(self, event):
        self.offset = event.pos() - self.computeTopLeftGridPoint(event.pos())
        QGraphicsRectItem.mousePressEvent(event)

    def computeTopLeftGridPoint(self, pointP):
        gridSize = 20
        xV = math.floor(pointP.x() / gridSize) * gridSize
        yV = math.floor(pointP.y() / gridSize) * gridSize
        return QPointF(xV, yV)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            newPos = value.toPointF()
            if QApplication.mouseButtons() == Qt.LeftButton:
                closestPoint = self.computeTopLeftGridPoint(newPos)
                point = closestPoint + self.offset
                return point
            else:
                return newPos
        else:
            return QGraphicsItem.itemChange(change, value)
    """





    #设置封装
    def set_package(self, footprint):
        self.footprint = footprint

    def edit_pin_Num(self, i, num):        #管脚号
        self.pin[i].set_pin_num(num)

    def edit_pin_Name(self, i, name):       #管脚名
        self.pin[i].set_pin_name(name)

    def set_pin_Net(self, i, net):           #网络
        self.pin[i].set_pin_net(net)

    def set_pin(self, pin_info):
        for i in range(len(pin_info)):
            #print(pin_info[i][0])
            #print(pin_info[i][1])
            pin = Pin(pin_info[i][0], pin_info[i][1])
            #print("P:", pin)
            self.pin.append(pin)

    def get_pin_num(self, i):
        return self.pin[i].get_pin_num()

    def get_count(self):
        return len(self.pin)

    def get_designator(self):
        return self.designator

    def get_comment(self):
        return self.comment

    def get_pin_list(self):
        return self.pin

    '''
    def paint(self, painter, option, widget = None):
        count = len(self.pin)
        painter.drawRect(10, 10, 100, 100)
        if count <= 4:
            print('one side')
            w = count * 50
            h = count * 100
            pin_length = count * 40
            #painter.drawRect(x, y, w, h)
            painter.drawRect()
            for i in range(count):
                num = self.pin[i].get_pin_num()
                #name = self.pin[i].get_pin_name()
                #self.pin[i].painter(painter, x, y)
                
    

        elif count <= 16:
            print('two side')
        else:
            print('four side')
'''
