import math

from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QGraphicsRectItem, QGraphicsItemGroup, QPushButton, QGraphicsProxyWidget
from PyQt5.QtGui import QColor, QPen, QBrush, QCursor, QPainter, QPainterPath
from PyQt5.QtCore import QLine, Qt, QPointF, QLineF, QEvent, pyqtSignal
from Schematic_design.pin import Pin
from Schematic_design.component import Component
from Schematic_design.MyItemGroup import MyItemGroup
from Schematic_design.MyLineItem import MyLineItem, MyLineItem_2


class Scene_1(QGraphicsScene):      #库
    def __init__(self, parent = None):
        super().__init__(parent)

        self.my_rotation = 0

        #settings
        self.grid_size = 20
        self.grid_squares = 5

        self._color_background = QColor('#FFFFBB')
        self._color_light = QColor('#E9E8E8')
        self._color_dark = QColor('#DBDADA')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)

        self.body = []
        self.pins = []


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # draw the lines
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)

            

            


#点阵背景
    """
    def drawBackground(self, painter, rect):
        pen = QPen()
        painter.setPen(pen)
        gridSize = 20
        left = int(rect.left()) - (int(rect.left()) % gridSize)
        top = int(rect.top()) - (int(rect.top()) % gridSize)
        points = []
        #for (x = left; x < rect.right(); x += gridSize):
        #    for (y = top; y < rect.bottom(); y += gridSize):
        #        points.append(QPointF(x, y))
        for x in range(left, int(rect.right()), 20):
            x += gridSize
            for y in range(top, int(rect.bottom()), 20):
                y += gridSize
                painter.drawPoint(QPointF(x, y))
                points.append(QPointF(x, y))
    """



    def add_rect(self):
        rect = QGraphicsRectItem(0, 0, 60, 80)
        rect.setBrush(QBrush(Qt.blue))
        self.addItem(rect)

    def add_node(self, node):
        self.body.append(node)
        self.addItem(node)

    def remove_node(self, node):
        self.body.remove(node)
        for pin in self.pins:
            if pin.edge_wrap.start_item is node or pin.edge_wrap.end_item is node:
                self.remove_pin(pin)
        self.removeItem(node)

    def add_pin(self, edge):
        self.pins.append(edge)
        self.addItem(edge)

    def remove_pin(self, edge):
        self.pins.remove(edge)
        self.removeItem(edge)

    def keyPressEvent(self, event):
        #print('key press response', event.key())
        if event.key() == Qt.Key_Space :
            if self.selectedItems():
                items = self.selectedItems()
                item = items[0]

                if item != None:
                    item.setTransformOriginPoint(0, 0)
                    self.my_rotation += 90
                    item.setRotation(self.my_rotation)


        elif event.key() == Qt.Key_Delete:
            itemlist = self.selectedItems()
            for i in range(0, len(itemlist)):
                self.removeItem(itemlist[i])

                # del itemlist[i]
            del itemlist

                #item.setTransformOriginPoint(0,0)
                #print('space')
                #print(item.pin_name)


class Scene_2(QGraphicsScene):      #原理图
    designator_signal = pyqtSignal(str)
    comment_signal = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

        self.my_rotation = 0

        #settings
        self.grid_size = 20
        self.grid_squares = 5

        self._color_background = QColor('#FFFFAA')
        self._color_light = QColor('#AAAAAA')
        self._color_dark = QColor('#888888')

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)

        self.item_groups = []

        # 初始化导线的起点和终点为None
        self.start = None
        self.end = None
        # 初始化导线的列表为空
        self.lines = []
        # 初始化导线按钮的状态为False
        self.button_pressed = False



        #for i in range(len(self.item_groups)):
        #    print("00000")
        #    self.item_groups[i].designator_signal.connect(self.handle_clicked)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))


        # draw the lines
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)





    def add_node(self, node):
        self.body.append(node)
        self.addItem(node)

    def remove_node(self, node):
        self.body.remove(node)
        for pin in self.pins:
            if pin.edge_wrap.start_item is node or pin.edge_wrap.end_item is node:
                self.remove_pin(pin)
        self.removeItem(node)

    def dragEnterEvent(self, event):
        event.setAccepted(True)
        if event.mimeData().hasFormat("text/csv"):
            event.acceptProposedAction()



    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/csv"):
            ba = event.mimeData().data('text/csv')
            if not(ba.isNull()):

                str1 = str(ba, encoding = 'utf-8')
                print("str:", str1)
                designator, comment, pin_list = self.split_str(str1)

                c = Component(designator, comment)
                c.set_pin(pin_list)

                self.group = MyItemGroup(designator, comment, pin_list)
                self.group.addToGroup(c)

                for i in range(c.get_count()):
                    pin = Pin(pin_list[i][0], pin_list[i][1])
                    self.set_position(pin, len(pin_list), i)
                    self.group.addToGroup(pin)

                self.addItem(self.group)

                self.item_groups.append(self.group)




    def dragMoveEvent(self, event):
        event.accept()


    def split_str(self, str1):
        #print('split')
        result = str1.split(" ")
        print("result:", result)
        print("pre_len:", len(result))
        designator = result[0]
        comment = result[1]
        result.remove(result[0])
        result.remove(result[0])
        #print("after remove result:", result)
        pin_list = []
        print("len:", len(result))
        if(len(result) % 2 == 0):
            for i in range(0, len(result), 2):
                pin_list.append([result[i], result[i + 1]])

        else:
            print("IndexError: list index out of range")
        #print("pin_list:", pin_list)

        return designator, comment, pin_list

    def keyPressEvent(self, event):
        #print('key press response', event.key())
        if event.key() == Qt.Key_Space:
            if self.selectedItems():
                items = self.selectedItems()
                item = items[0]

                if item != None:
                    item.setTransformOriginPoint(0, 0)
                    self.my_rotation += 90
                    item.setRotation(self.my_rotation)

        if event.key() == Qt.Key_Delete:
            itemlist = self.selectedItems()
            for i in range(0, len(itemlist)):
                self.removeItem(itemlist[i])
                print("type:", itemlist[i].type())
                #print("my line type:", MyLineItem_2.type(itemlist[i]))
                #print("my group type:", MyItemGroup.type(itemlist[i]))
                if itemlist[i].type() == 6:
                    print("delete line")
                elif itemlist[i].type() == 10:
                    print("delete group item")
                # del itemlist[i]
            del itemlist


    def set_position(self, item, len, i):
        print("len:",len)

        if len <= 4:
            self.width = 200
            self.height = 300
            self.interval = int(self.height / (len + 1))
            item.setPos(self.width, (i + 1) * self.interval)

        elif 4 < len <= 8:
            print("yeahhhhhhhhh")
            self.width = 300
            self.height = 400
            self.interval = int(self.height / (4 + 1))
            if i < 4:
                item.setPos(self.width, (i + 1) * self.interval)
            elif i >=  4:
                item.setPos(0, (i - 3) * self.interval)
                #item.CustomRotate((0,0), 0, 180)
                #item.setTransformOriginPoint(0, 0)
                #item.setRotation(180)


        elif 8 < len <= 48:
            print("hhhhhhhhh")
            self.width = 500
            self.height = 500


            num = math.ceil(len / 4)
            self.interval = int(self.height / (num + 1))


            #right
            if i < num:
                item.setPos(self.width, (i + 1) * self.interval)
            #left
            elif num <= i < 2 * num:
                item.setPos(0, (i - num + 1) * self.interval)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(180)
            #up
            elif 2 * num <= i < 3 * num:
                item.setPos((i - 2 * num + 1) * self.interval, 0)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(270)
            elif 3 * num <= i < len:
                item.setPos((i - 3 * num + 1) * self.interval, self.height)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(90)

        elif 48 < len <= 96:
            self.width = 800
            self.height = 800

            num = math.ceil(len / 4)
            self.interval = int(self.height / (num + 1))

            # right
            if i < num:
                item.setPos(self.width, (i + 1) * self.interval)
            # left
            elif num <= i < 2 * num:
                item.setPos(0, (i - num + 1) * self.interval)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(180)
            # up
            elif 2 * num <= i < 3 * num:
                item.setPos((i - 2 * num + 1) * self.interval, 0)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(270)
            elif 3 * num <= i < len:
                item.setPos((i - 3 * num + 1) * self.interval, self.height)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(90)


        else:
            self.width = 840
            self.height = 840

            num = math.ceil(len / 4)
            self.interval = int(700 / (num + 1))

            # right
            if i < num:
                item.setPos(self.width, (i + 1) * self.interval + 70)
            # left
            elif num <= i < 2 * num:
                item.setPos(0, (i - num + 1) * self.interval + 70)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(180)
            # up
            elif 2 * num <= i < 3 * num:
                item.setPos((i - 2 * num + 1) * self.interval + 70, 0)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(270)
            #down
            elif 3 * num <= i < len:
                item.setPos((i - 3 * num + 1) * self.interval + 70, self.height)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(90)

    #def mouseMoveEvent(self, event):
    #    print(event.scenePos().x(), event.scenePos().y())

    def mousePressEvent(self, event):
        # 如果点击了鼠标左键，并且导线按钮已经按下
        if event.button() == Qt.LeftButton and self.button_pressed:
            # 如果导线的起点还没有设置，就获取鼠标在场景中的位置作为起点
            if not self.start:

                x = round(event.scenePos().x() / 20) * 20
                y = round(event.scenePos().y() / 20) * 20

                self.start = QPointF(x, y)
            # 否则，获取鼠标在场景中的位置作为终点，并创建一个新的导线对象
            else:
                x = round(event.scenePos().x() / 20) * 20
                y = round(event.scenePos().y() / 20) * 20
                self.end = QPointF(x, y)
                #self.end = event.scenePos()
                # 计算终点和起点的x坐标和y坐标的差值
                dx = abs(self.end.x() - self.start.x())
                dy = abs(self.end.y() - self.start.y())
                # 如果x坐标的差值大于y坐标的差值，表示水平方向的距离更大，就把终点的y坐标设为和起点一样，表示是水平的导线
                if dx > dy:
                    self.end.setY(self.start.y())
                # 否则，表示垂直方向的距离更大，就把终点的x坐标设为和起点一样，表示是垂直的导线
                else:
                    self.end.setX(self.start.x())
                # 创建一个新的导线对象
                line = MyLineItem_2(QLineF(self.start, self.end))

                line.set_start_point(self.start)
                line.set_end_point(self.end)

                # 设置导线的颜色和宽度
                line.setPen(QPen(Qt.darkBlue, 3))
                # 把导线添加到场景中
                self.addItem(line)

                # 把导线添加到列表中，方便后续操作
                self.lines.append(line)
                # 把终点作为下一个导线的起点
                self.start = self.end

                #if self.lines[0].collidesWithItem(line, Qt.IntersectsItemShape):
                #    print("collides")

                # 获取直线的两个端点
                #line = self.lines[0]
                #p1 = line.get_start_point()
                #p2 = line.get_end_point()

                #print("start", p1.x(), p1.y())
                #print("end", p2.x(), p2.y())

                # 创建一个包含端点的路径
                #linePath = QPainterPath()
                #linePath.addEllipse(p1, 5, 5)  # 以端点为圆心，半径为5的圆
                #linePath.addEllipse(p2, 5, 5)

                if line.whether_connect(self.lines[0]):
                    print("collides")


        #原本的想法是点击右键后就结束绘制，但是实际是点击右键后鼠标的格式没有恢复
        #elif event.button() == Qt.RightButton and self.button_pressed and self.start:
        #    print("stop")
            # 重置导线的起点和终点为None，表示结束绘制
        #    self.start = None
        #    self.end = None
        #    self.button_pressed = not self.button_pressed


        #elif not self.button_pressed:
        #    print("not")
        #    self.start = None

        #else:
        #    QGraphicsScene.mousePressEvent(self, event)
            #self.mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            #print("left")
            if self.selectedItems():
                #@print("true")
                item = self.selectedItems()
                current_item = item[0]
                # print("current_item:", current_item.designator)
                designator = str(current_item.designator)
                comment = str(current_item.comment)
                self.designator_signal.emit(designator)
                self.comment_signal.emit(comment)
                QGraphicsScene.mousePressEvent(self, event)
            else:
                #print("false")
                QGraphicsScene.mousePressEvent(self, event)
        else:
            QGraphicsScene.mousePressEvent(self, event)



    def mouseMoveEvent(self, event):

        # 如果鼠标移动，并且导线按钮已经按下，并且导线的起点已经设置
        if event.type() == QEvent.MouseMove and self.button_pressed and self.start:


            # 获取鼠标在场景中的位置作为临时终点，并更新最后一个导线对象的终点坐标

            x = round(event.scenePos().x() / 20) * 20
            y = round(event.scenePos().y() / 20) * 20

            temp_end = QPointF(x, y)
            #temp_end = event.scenePos()
            last_line = self.lines[-1]       #返回最后一个数据
            last_line.setLine(QLineF(self.start, temp_end))

        else:
            QGraphicsScene.mouseMoveEvent(self, event)


    """
    def mouseReleaseEvent(self, event):
        # 如果释放了鼠标右键，并且导线按钮已经按下，并且导线的起点已经设置
        if event.button() == Qt.RightButton and self.button_pressed and self.start:
            # 获取鼠标在场景中的位置作为最终终点，并更新最后一个导线对象的终点坐标
            final_end = event.scenePos()
            last_line = self.lines[-1]
            last_line.setLine(QLineF(self.start, final_end))
            # 重置导线的起点和终点为None，表示结束绘制 
            self.start = None
            self.end = None
    """


    def button_clicked(self):
        self.button_pressed = not self.button_pressed
        if not self.button_pressed:
            # 重置导线的起点和终点为None，表示结束绘制
            self.start = None
            self.end = None
        return self.button_pressed

    def edit_designator_(self, designator):
        #print("scene")
        item = self.selectedItems()
        current_item = item[0]
        current_item.set_designator(designator)

    def edit_footprint_(self, footprint):
        item = self.selectedItems()
        current_item = item[0]
        current_item.set_footprint(footprint)

    def edit_comment_(self, comment):
        item = self.selectedItems()
        current_item = item[0]
        current_item.set_comment(comment)

    def handle_clicked(self, str):
        print("you clicked", str)






