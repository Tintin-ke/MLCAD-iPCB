import sys
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MyLineItem(QGraphicsLineItem):
    def __init__(self):
        super(MyLineItem, self).__init__()

        self.start = None
        self.end = None

        self.lines = []

        self.drawing = False

    def unable_drawing(self):
        self.drawing = not self.drawing # 切换绘制状态
        if not self.drawing:
            self.lines = []
            self.update()  # 更新绘图

    def set_start_point(self, point):
        self.start = point
        self.lines.append(point)

    def set_end_point(self, point):
        self.end = point
        self.lines.append(point)

    def add_turning_point(self, start, end):
        self.lines.append((start, end))

    def paint(self, painter, option, widget=None):
        painter.setPen(QPen(Qt.black, 3))
        painter.setFont(QFont('SimSun', 13))
        painter.setBrush(Qt.darkBlue)
        print("start to draw")

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            newPos = value
            if QApplication.mouseButtons() == Qt.LeftButton:
                xV = round(newPos.x() / 20) * 20
                yV = round(newPos.y() / 20) * 20
                return QPointF(xV, yV)
        return value



class MyLineItem_2(QGraphicsLineItem):
    # 重写QGraphicsLineItem类型，可以添加一些自定义属性或方法
    def __init__(self, *args, **kwargs):

        # 初始化导线的起点和终点为None
        self.start = None
        self.end = None

        super().__init__(*args, **kwargs)
        self.setFlags(
            QGraphicsLineItem.ItemIsMovable | QGraphicsLineItem.ItemIsSelectable | QGraphicsLineItem.ItemSendsGeometryChanges)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            newPos = value
            if QApplication.mouseButtons() == Qt.LeftButton:
                xV = round(newPos.x() / 20) * 20
                yV = round(newPos.y() / 20) * 20
                return QPointF(xV, yV)
        return value

    def set_start_point(self, point):
        self.start = point

    def set_end_point(self, point):
        self.end = point

    def get_start_point(self):
        return self.start

    def get_end_point(self):
        return self.end

    def whether_connect(self, line):
        #print("检测中")
        #print("self.start:", self.start.x(), self.start.y())
        #print("self.end:", self.end.x(), self.end.y())
        #print("line.start:", line.start.x(), line.start.y())
        #print("line.end:", line.end.x(), line.end.y())
        if self.start == line.end:
            print("connect_0")
            return True
        elif self.end == line.start:
            print("connect_1")
            return True


    """
    def collidesWithPath(self, path, mode):
        # 获取直线的两个端点
        line = self.line()
        p1 = line.p1()
        print(p1.x(), p1.y())
        p2 = line.p2()
        print(p2.x(), p2.y())

        # 创建一个包含端点的路径
        linePath = QPainterPath()
        linePath.addEllipse(p1, 30, 30)  # 以端点为圆心，半径为5的圆
        linePath.addEllipse(p2, 30, 30)

        pen = QPen()
        painter = QPainter()
        painter.setBrush(Qt.red)
        painter.setPen(pen)
        painter.drawPath(linePath)


        # 调用基类的方法判断路径是否碰撞
        return super().collidesWithPath(linePath, mode)
    """

    """
    def collidesWithItem(self, other, mode):

        # 获取直线的两个端点
        line = self.line()
        p1 = line.p1()
        p2 = line.p2()

        # 创建一个包含端点的路径

        linePath = QPainterPath()
        linePath.addEllipse(p1, 5, 5)  # 以端点为圆心，半径为5的圆
        linePath.addEllipse(p2, 5, 5)

        # 调用基类的方法判断路径是否和其他图元碰撞
        return super().collidesWithPath(linePath, mode)
    """






