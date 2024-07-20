import sys
sys.path.append("..")

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import SplitFluentWindow, FluentIcon, setTheme, Theme


from Ui_file import openandIdentify, Edit, Sche

#from Ui_OpenImage import Ui_OpenImage

class Demo(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("iPCB Lib")

        #添加子界面
        self.openImage = openandIdentify(self)
        self.addSubInterface(self.openImage, FluentIcon.SYNC, '识别')

        self.EditForm = Edit(self)
        self.addSubInterface(self.EditForm, FluentIcon.EDIT, '编辑页面')

        self.ScheForm = Sche(self)
        self.addSubInterface(self.ScheForm, FluentIcon.VIEW, '原理图界面')

        #self.menuInterface = MenuInterface()
        #t = Translator()
        #self.addSubInterface(self.menuInterface, FluentIcon.MENU, 't.menus')

        #self.menuForm = Menu()
        #self.addSubInterface(self.menuForm, FluentIcon.HOME, 'nenu')


if __name__ == '__main__':
    #enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    #使用深色模式
    #setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Demo()
    w.resize(1000, 800)
    w.show()


    w.openImage.changeValue.connect(w.EditForm.getValue)
    w.openImage.clearValue.connect(w.EditForm.getclearValue)

    app.exec_()