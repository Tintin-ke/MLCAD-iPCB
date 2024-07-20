from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QGraphicsView, QGraphicsRectItem
from PyQt5.Qt import *
from PyQt5 import QtCore
import math
import numpy


from Schematic_design.component import Component

class View_1(QGraphicsView):           #库

    def __init__(self, graphic_scene, parent = None):
        super().__init__(parent)

        self.gr_scene = graphic_scene
        self.parent = parent

        self.press = False

        self.init_ui()

        #self.m_translateSpeed = 1.0


    def init_ui(self):
        self.setScene(self.gr_scene)
        self.setSceneRect(0, 0, 4000, 4000)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform #|
                            #QPainter.LosslessImageRendering
                            )
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.RubberBandDrag)
        #self.setDragMode(self.ScrollHandMode)

        self.begin_drag = False
        self.begin_drag_pos = None
        self.startPos = None
        #self.setDragMode(self.ScrollHandDrag)


        #self.setDragMode(self.NoDrag)
        #self.centerOn(0, 0)


    #放大，缩小功能
    def wheelEvent(self, event):
        wheelValue = event.angleDelta().y()
        ratio = wheelValue / 1200.0 + 1
        self.scale(ratio, ratio)

    def mousePressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier and event.button() == Qt.LeftButton:
            # store the origin point
            self.startPos = event.pos()
        else:
            super(View_1, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.startPos is not None:
            # compute the difference between the current cursor position and the
            # previous saved origin point
            delta = self.startPos - event.pos()
            # get the current transformation (which is a matrix that includes the
            # scaling ratios
            transform = self.transform()
            # m11 refers to the horizontal scale, m22 to the vertical scale;
            # divide the delta by their corresponding ratio
            deltaX = delta.x() / transform.m11()
            deltaY = delta.y() / transform.m22()
            # translate the current sceneRect by the delta
            self.setSceneRect(self.sceneRect().translated(deltaX, deltaY))
            # update the new origin point to the current position
            self.startPos = event.pos()
        else:
            super(View_1, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.startPos = None
        super(View_1, self).mouseReleaseEvent(event)

    '''
    #平移速度
    def setTranslateSpeed(self, speed):
        #建议速度范围
        self.m_translateSpeed = speed

    def translateSpeed(self):
        return self.m_translateSpeed

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.translate_(QPointF(0, -2))

        elif event.key() == Qt.Key_Down:
            self.translate_(QPointF(0, 2))

        elif event.key() == Qt.Key_Left:
            self.translate_(QPointF(-2, 0))

        elif event.key() == Qt.Key_Right:
            self.translate_(QPointF(2, 0))
            self.centerOn(QPointF(200, 200))



    def translate_(self, delta):
        #根据当前zoom缩放平移数
        #delta *= self.m_scale
        print("0")
        #delta *= self.m_translateSpeed
        print('1')

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        print('2')
        VIEW_WIDTH = self.viewport().rect().width()
        VIEW_WIDTH = self.width()
        VIEW_HEIGHT = self.viewport().rect().height()
        VIEW_HEIGHT = self.height()
        print('3')
        newCenter = QPointF(VIEW_WIDTH / 2 - delta.x(), VIEW_HEIGHT / 2 - delta.y())
        print('4')
        self.centerOn(newCenter)
        self.centerOn(QPointF(0,0))
        print('5')

        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        print('6')

    '''




    '''
    def mousePressEvent(self, event):
        #QGraphicsView.mousePressEvent(event)
        print("press")
        self.m_lastPointF = event.pos()
        print("presspoint:",self.m_lastPointF)
        self.press = True

    def mouseReleaseEvent(self, event):
        #QGraphicsView.mouseReleaseEvent(event)
        print("re")
        #self.press = False
        self.viewport().update()
        self.scene().update(0, 0, self.width(), self.height())
        if self.press == True and self.DragMode == QGraphicsView.ScrollHandDrag:
            self.viewport().update()
            self.scene().update(0, 0, self.width(), self.height())

            self.point = event.pos()
            print("point:", self.point)
            print("x:", self.m_lastPointF.x() - self.point.x())
            print('y:', self.m_lastPointF.y() - self.point.y())
            self.scroll((self.point.x() - self.m_lastPointF.x()), (self.point.y() - self.m_lastPointF.y()))


            self.viewport().update()
            self.scene().update(0,0,self.width(),self.height())
            self.press = False
        self.press = False
    '''










    '''
    def wheelEvent(self, event):
        # 滑轮事件
        if event.modifiers() & Qt.ControlModifier:
            self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))
            return event.accept()
        super(View_1, self).wheelEvent(event)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(
            scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
    '''





    #def keyPressEvent(self, event):
    #    if event.key() == Qt.Key_Space:
    #        print("space")

    """
    def mousePressEvent(self, event):
        #QGraphicsView.mousePressEvent(self, event)
        if event.button() == Qt.LeftButton:
            if self.scene().itemAt(self.mapToScene(event.pos()), self.transform() == None):
                print("没有选中任何图元")
                self.mouseLBtnDown = event.pos()
                self.isLBtnDown = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        #QGraphicsView.mouseMoveEvent(self, event)
        if self.isLBtnDown:
            self.ptNow = self.mapToScene(event.pos())
            self.movePt = self.ptNow - self.mapToScene(self.mouseLBtnDown)

            #根据鼠标当前的点作为定位
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.nowCenter = QPointF(-self.movePt.x(), -self.movePt.y())
            self.centerOn((self.nowCenter))
            self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.isLBtnDown = False

        super().mouseReleaseEvent(event)
    """
    '''
    def mousePressEvent(self, event):
        print("0")

        if self.itemAt(event.pos()) is None:
            self.begin_drag = True
            self.begin_drag_pos = event.pos()
        super().mousePressEvent(event)


    def mouseMoveEvent(self, event):
        print("move")
        #super().mouseMoveEvent(event)
        print('1')
        if self.begin_drag and self.begin_drag_pos is not None:
            print("2")
            delta = self.begin_drag_pos - event.pos()
            old_center = QPointF(
                (self.mapToScene(self.pos()).x() + self.width()) / 2,
                (self.mapToScene(self.pos()).y() + self.height()) / 2
            )
            self.centerOn(old_center + delta)
            self.update()
            self.scene().update()

        else:
            super().mouseMoveEvent(event)
        pass

    def mouseReleaseEvent(self, event):

        if self.begin_drag:
            self.begin_drag = False
            self.begin_drag_pos = None

        super().mouseReleaseEvent(event)
    '''





    '''
    def mousePressEvent(self, event):
        #QGraphicsView.mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.rightMousePressed = True
            self.panStartX = event.x()
            self.panStartY = event.y()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
            return

    def mouseMoveEvent(self, event):
        print("move")
        #QGraphicsView.mouseMoveEvent(event)
        if self.rightMousePressed:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self.panStartX))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self.panStartY))
            self.panStartX = event.x()
            self.panStartY = event.y()
            event.accept()
            return
        event.ignore()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightMousePressed = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
            return
        event.ignore()
    '''



class View_2(QGraphicsView):          #原理图

    def __init__(self, graphic_scene, parent = None):
        super().__init__(parent)

        self.gr_scene = graphic_scene
        self.parent = parent

        self.setAcceptDrops(True)

        self.button = QPushButton('导线', self)   #创建一个按钮
        self.button.move(10, 10)
        self.button.clicked.connect(self.button_clicked)

        #self.button = QPushButton()


        self.init_ui()

    def button_clicked(self):
        a = self.gr_scene.button_clicked()
        # 如果导线按钮被按下，就把鼠标的形状改为十字形，表示可以绘制导线
        if a:
            self.setCursor(QCursor(Qt.CrossCursor))

            #self.pixmap = QGraphicsPixmapItem()
            #self.pixmap.setPixmap(QPixmap("aglena.jpg"))
            #self.pixmap.setPos(0,0)

        # 否则，把鼠标的形状恢复为默认，表示不能绘制导线
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))


    def init_ui(self):
        self.setScene(self.gr_scene)
        self.setRenderHints(QPainter.Antialiasing |
                            QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform
                            )
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff )
        self.setTransformationAnchor(self.AnchorUnderMouse)
        self.setDragMode(self.RubberBandDrag)
        self.setResizeAnchor(self.AnchorUnderMouse)
        self.setMouseTracking(True)

        #self.setDragMode(self.ScrollHandDrag)
        self.setAcceptDrops(True)


    #放大，缩小功能

    def dragMoveEvent(self, event):
        event.accept()


    def wheelEvent(self, event):
        wheelValue = event.angleDelta().y()
        ratio = wheelValue / 1200.0 + 1
        self.scale(ratio, ratio)

    #def mouseMoveEvent(self, event):
        #print('move!!!!!')
    #    xV = round(event.pos().x() / 20) * 20
    #    yV = round(event.pos().y() / 20) * 20
    #    #QCursor.setPos(QPointF(xV, yV))

    # 重写mouseMoveEvent方法，让鼠标的位置取整到最近的网格点
    #def mouseMoveEvent(self, event):
        #print("view move")

    #    print(event.x(), event.y())
    #    x = round(event.x() / 20) * 20
    #    y = round(event.y() / 20) * 20
    #    print(x, y)
    #    #self.setCursor(QCursor(Qt.CrossCursor))
    #    self.mapToScene(x, y)


    '''
    def mousePressEvent(self, event):
        if self.scene() == None:
            return
        self.centerAnchor = self.mapToScene(event.pos()) - event.pos() + QPointF(self.width() / 2, self.height() / 2)
        self.posAnchor = event.pos()
        self.isMousePressed = True

    def mouseMoveEvent(self, event):
        offsetPos = event.pos() - self.posAnchor
        if self.isMousePressed:
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.centerOn(self.centerAnchor - offsetPos)

    def mouseReleaseEvent(self, event):
        self.isMousePressed = False
    '''

    '''
    def wheelEvent(self, event):
        # 滑轮事件
        if event.modifiers() & Qt.ControlModifier:
            self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))
            return event.accept()
        super(View_2, self).wheelEvent(event)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(
            scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
    '''

    """
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print("鼠标右键")
            self.setDragMode(self.ScrollHandDrag)
            self.setInteractive(False)

        elif event.button() == Qt.LeftButton:
            self.setDragMode(self.RubberBandDrag)
            self.setInteractive(True)
    """




