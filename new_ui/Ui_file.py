from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtGui, QtCore

from Ui_openandIdentify import Ui_MainWindow
from Ui_OpenImage import Ui_OpenImage
from Ui_Edit import Ui_Edit
from Ui_Sche import Ui_Sche

from qfluentwidgets import FluentIcon as FIF

from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QWidget
import sys
sys.path.insert(0, sys.path[0]+"/../")
#print(sys.path)

from function import identify
from function import trans
from function import save

from Schematic_design.Scene import Scene_1
from Schematic_design.View import View_1
from Schematic_design.component import *
from Schematic_design.MyListWidgetItem import MyListWidgetItem as myitem
from Schematic_design.pin import Pin,Pin_left
from function import find_square as fs
from function import similar
import openpyxl
from function.angle_identify import angle_identify
from PIL import Image
from Schematic_design.import_ui import import_ui

#全局变量
#_list = []
#new_list = []
#double_list = []

class openandIdentify(QWidget, Ui_OpenImage):
    changeValue = pyqtSignal(list)
    clearValue = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent = None)
        #self.edit = Edit(self)

        self.list = []  # 识别图像后，存储信息的列表
        # self.new_list = []  # 经过修改后的信息列表
        # self.double_list = []  # 二维列表，num，name
        self.new_path = ''  # 手动截图或不截图的图片
        self.screenshots_path = ''  # 自动截图后的多张结果

        #self.edit = Edit
        #self.changeValue.connect(self.edit.getValue)

        self.setupUi(self)



        self.type = 'two_side_leftright'  # 默认识别的类型为two side
        self.name = []


        #设置图标
        self.openfolder_btn.setIcon(FIF.FOLDER)
        self.splitimage_btn.setIcon(FIF.CUT)
        self.identify_btn.setIcon(FIF.PLAY)
        self.picup_btn.setIcon(FIF.LEFT_ARROW)
        self.picdown_btn.setIcon(FIF.RIGHT_ARROW)

        #RATIONBUTTON
        self.leftright_btn.setChecked(True)
        self.leftright_btn.toggled.connect(self.dual_leftright_clicked)
        self.updown_btn.toggled.connect(self.dual_updown_clicked)
        self.quad_btn.toggled.connect(self.quad_clicked)

        #绑定函数
        self.openfolder_btn.clicked.connect(self.openImage)
        self.splitimage_btn.clicked.connect(self.slot_auto_printscreen)
        self.picup_btn.clicked.connect(self.slot_pic_up)
        self.picdown_btn.clicked.connect(self.slot_pic_down)
        self.autorotation_btn.clicked.connect(self.Automatic_rotation_slot)
        self.dex_btn.clicked.connect(self.Dextral_rotation_slot)
        self.levo_btn.clicked.connect(self.Sinistral_rotation_slot)
        self.identify_btn.clicked.connect(self.slot_start)

        #self.LineEdit.textChanged.connect(self.setValue)

        #信号函数
        #self.changeValue.connect()



    def setValue(self):

        #self.changeValue.emit(list(self.list))
        if self.list == None:
            return
        self.changeValue.emit(self.list)
        #self.changeValue.emit(['a','b'])
        #rint('list:', self.list)
        #print('emit!!!')

    def clearEmit(self):
        self.clearValue.emit()



    def openImage(self):
        global imgNamepath
        imgNamepath, imgType = QFileDialog.getOpenFileName(self.openfolder_btn, "打开文件夹",
                                                           "../image",
                                                           "*.jpg;;*.png;;All Files(*)")
        if imgNamepath == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            # 以下写你想进行的正常操作
            img = QtGui.QPixmap(imgNamepath).scaled(self.ImageLabel.width(), self.ImageLabel.height())
            self.ImageLabel.setPixmap(img)
            self.LineEdit.setText(imgNamepath)
            self.clearlist()

    def dual_updown_clicked(self):
        self.type = 'two_side_updown'

    def dual_leftright_clicked(self):
        self.type = 'two_side_leftright'

    def quad_clicked(self):
        self.type = 'four_side'

    def clearlist(self):
        #list = []
        #new_list = []
        #double_list = []
        self.name_label = []
        self.screenshots_path = ''  # 自动截图后的多张结果
        self.clearEmit()

        #edit = Edit()


        #self.listWidget.clear()
        #self.tableWidget.clear()

    def slot_auto_printscreen(self):  # 分割图片
        self.screenshots_path = fs.auto_(imgNamepath, self.type, self.name)
        # if self.name != []:
        #	self.file_path_line.setText(self.name[0])
        print("这里是screenshots_path:", self.screenshots_path)
        new_img = QtGui.QPixmap(self.screenshots_path[0]).scaled(self.ImageLabel.width(), self.ImageLabel.height())
        self.ImageLabel.setPixmap(new_img)
        self.LineEdit.setText(self.screenshots_path[0])
        print(self.LineEdit.text())

    def slot_pic_up(self):
        current_imgpath = self.LineEdit.text()
        current_index = self.screenshots_path.index(current_imgpath)
        up_index = (current_index - 1 + len(self.screenshots_path)) % len(self.screenshots_path)
        self.LineEdit.setText(self.screenshots_path[up_index])
        up_img = QtGui.QPixmap(self.screenshots_path[up_index]).scaled(self.ImageLabel.width(),
                                                                       self.ImageLabel.height())
        self.ImageLabel.setPixmap(up_img)

    def slot_pic_down(self):
        current_imgpath = self.LineEdit.text()
        current_index = self.screenshots_path.index(current_imgpath)
        down_index = (current_index + 1) % len(self.screenshots_path)
        self.LineEdit.setText(self.screenshots_path[down_index])
        down_img = QtGui.QPixmap(self.screenshots_path[down_index]).scaled(self.ImageLabel.width(),
                                                                           self.ImageLabel.height())
        self.ImageLabel.setPixmap(down_img)

    def Automatic_rotation_slot(self):
        # print("auto")
        if len(self.screenshots_path) == 0:
            print("没有图片")
            return
        # print(self.screenshots_path)

        current_imgpath = self.LineEdit.text()  # 获取当前图片的名字
        current_index = self.screenshots_path.index(current_imgpath)

        for i in range(0, len(self.screenshots_path)):
            img = self.screenshots_path[i]
            angle_identify(img)

        print("自动旋转结束")

    def Sinistral_rotation_slot(self):
        print("left")
        if len(self.screenshots_path) == 0:
            print("没有图片")
            return

        current_imgpath = self.LineEdit.text()  # 获取当前图片的名字
        current_index = self.screenshots_path.index(current_imgpath)

        img = Image.open(current_imgpath)
        img = img.transpose(Image.ROTATE_90)  # 旋转90度
        img.save(current_imgpath)

        new_img = QtGui.QPixmap(current_imgpath).scaled(self.ImageLabel.width(), self.ImageLabel.height())
        self.ImageLabel.setPixmap(new_img)  # 展示

    def Dextral_rotation_slot(self):
        print("right")
        if len(self.screenshots_path) == 0:
            print("没有图片")
            return

        current_imgpath = self.LineEdit.text()  # 获取当前图片的名字
        current_index = self.screenshots_path.index(current_imgpath)

        img = Image.open(current_imgpath)
        img = img.transpose(Image.ROTATE_270)  # 旋转90度
        img.save(current_imgpath)

        new_img = QtGui.QPixmap(current_imgpath).scaled(self.ImageLabel.width(), self.ImageLabel.height())
        self.ImageLabel.setPixmap(new_img)  # 展示

    def slot_start(self):
        # global  list
        lan_choice = 'en'  # 获取语言模型
        # self.slot_auto_printscreen()

        if self.type == 'BGA':
            print("BGA")
            current_imgpath = self.LineEdit.text()  # 获取当前图片的名字
            identify.identi_BGA(current_imgpath)

            return

        if len(self.screenshots_path) == 0:
            print("只有一张图片")
            current_imgpath = self.LineEdit.text()  # 获取当前图片的名字
            self.list = identify.identi(current_imgpath, lan_choice)

            new_img = QtGui.QPixmap('results.jpg').scaled(self.ImageLabel.width(), self.ImageLabel.height())  # 展示图片

            # new_img = QtGui.QPixmap(result_path).scaled(self.G_label.width(), self.G_label.height())
            self.ImageLabel.setPixmap(new_img)  # 展示
            self.LineEdit.setText('results.jpg')

            #self.changeValue.emit(self.list)
            self.setValue()


            #for i in self.list:
            #    self.edit.ListWidget.addItem(i)

            #listModel = QStringListModel()
            #listModel.setStringList(self.list)


        else:
            print("多张结果")
            self.list = identify.identi_more_pic(self.screenshots_path, lan_choice)  # 识别图片
            current_imgpath = self.LineEdit.text()  # 获取当前图片的名字
            current_index = self.screenshots_path.index(current_imgpath)

            result_path = []
            for i in range(0, len(self.screenshots_path)):
                result_path.append(f'results_{i + 1}.jpg')  # 将截取后标注的图片存储到列表中

            self.screenshots_path = result_path[:]  # 用result_path替换new_path
            new_img = QtGui.QPixmap(self.screenshots_path[0]).scaled(self.ImageLabel.width(),
                                                                     self.ImageLabel.height())  # 展示图片

            # new_img = QtGui.QPixmap(result_path).scaled(self.G_label.width(), self.G_label.height())

            ##################
            self.ImageLabel.setPixmap(new_img)  # 展示
            self.LineEdit.setText(self.screenshots_path[0])
            ##########

            #self.changeValue.emit(self.list)
            self.setValue()

            #for i in self.list:
            #    self.edit.ListWidget.addItem(i)

            #listModel = QStringListModel()
            #listModel.setStringList(self.list)






class Edit(QWidget, Ui_Edit):
    def __init__(self, parent = None):
        super().__init__(parent = None)
        self.setupUi(self)

        self.double_list = []
        self.new_list = []

        self.add_btn.clicked.connect(self.slot_add)
        self.edit_btn.clicked.connect(self.slot_modify)
        self.delete_btn.clicked.connect(self.slot_delete)
        self.save_btn.clicked.connect(self.slot_save)
        self.export_btn.clicked.connect(self.export_slot)
        self.input_btn.clicked.connect(self.input_btn_slot)
        self.output_btn.clicked.connect(self.output_btn_slot)
        self.auto_input_btn.clicked.connect(self.auto_group_slot)




        #self.ex.changeValue.connect(self.getValue)

        #self.ex.setValue()

    def auto_group_slot(self):
        #print("自动分组")
        if self.TableWidget.item(0, 0) == None:
            print("table为空，无法进行操作")
            return
        else:

            new_double_list = []
            if self.double_list:
                for i in range(1, len(self.double_list)):
                    num = []
                    similarty_list = []

                    current_name = self.double_list[0][1]
                    new_double_list.append(self.double_list[0])

                    for j in range(1, len(self.double_list)):
                        next_name = self.double_list[j][1]
                        num.append(j)

                        similarty_list.append(similar.similarity(current_name, next_name))
                        new_list = list(zip(num, similarty_list))

                    new_list = sorted(new_list, key=(lambda x:x[1]), reverse=True)

                    for k in range(len(new_list)):
                        count = 0
                        if new_list[k][1] >= 0.66:
                            count += 1
                            vector = new_list[k][0]
                            new_double_list.append(self.double_list[int(vector)])

                    self.double_list = [x for x in self.double_list if x not in new_double_list]
                    #print(new_double_list)
                    #print(self.double_list)
                    #print('\n')
                    if len(self.double_list) == 1:
                        new_double_list.append(self.double_list[0])
                        self.double_list.pop(0)

                    if self.double_list == []:
                        break

            #self.double_list == []:
            #print('123')
            self.double_list = new_double_list
            self.TableWidget.clear()
            self.TableWidget_2.setRowCount(len(self.double_list))
            self.TableWidget_2.setColumnCount(2)
            self.TableWidget_2.setHorizontalHeaderLabels(['num', 'name'])
            self.TableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.TableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)

            for i in range(len(self.double_list)):
                for j in range(len(self.double_list[i])):
                    # new_item = QStandardItem(self.double_list[i][j])
                    new_item = QTableWidgetItem(self.double_list[i][j])
                    self.TableWidget_2.setItem(i, j, new_item)  # 这一句有问题！！

    def slot_modify(self):
        item = self.ListWidget.currentItem()
        num = self.ListWidget.row(item)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.ListWidget.editItem(item)

    def slot_add(self):
        reply = QMessageBox.question(self, 'YES', 'Are you sure to add data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.ListWidget.currentItem()
            num = self.ListWidget.row(item)
            print(num)
            # self.listWidget.takeItem(self.listWidget.row(item))
            value, ok = QInputDialog.getText(self, "Add", "Please enter the added information:", QLineEdit.Normal, "default")
            print(value)
            self.ListWidget.insertItem(num, value)

    def slot_delete(self):
        reply = QMessageBox.question(self, 'YES', 'Are you sure to delete data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            item = self.ListWidget.currentItem()
            num = self.ListWidget.row(item)  # 获取当前选中的行号
            print(num)
            self.ListWidget.takeItem(self.ListWidget.row(item))

    def slot_save(self):
        length = self.ListWidget.count()
        print(length)
        self.new_list = []
        for i in range(length):
            item = self.ListWidget.item(i)
            text = item.text()
            self.new_list.append(text)
        print(self.new_list)

        self.double_list = trans.transfer(self.new_list)  # 将一维列表转换成二维列表
        print("转换完成")

        count = len(self.double_list)
        print(count)

        # self.tableWidget = QTableWidget(count, 2, self)
        self.TableWidget.setRowCount(count)
        self.TableWidget.setColumnCount(2)
        self.TableWidget.setHorizontalHeaderLabels(['num', 'name'])

        self.TableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.TableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.TableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.TableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)

        for i in range(len(self.double_list)):
            for j in range(len(self.double_list[i])):
                # new_item = QStandardItem(self.double_list[i][j])
                new_item = QTableWidgetItem(self.double_list[i][j])
                self.TableWidget.setItem(i, j, new_item)  # 这一句有问题！！

    def export_slot(self):
        filepath, type = QFileDialog.getSaveFileName(self, "Save File", "../result",
                                                     'txt(*.txt);;xls(*.xls);;xlsx(*.xlsx)')  # 前面是地址，后面是文件类型,得到输入地址的文件名和地址
        if filepath == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            items = self.get_table_data()
            if type == 'txt(*.txt)':
                file = open(filepath, 'a+', encoding='gbk')
                print(filepath)
                save.save_data_to_txt(items, file)
            elif type == "xlsx(*.xlsx)":
                wb = openpyxl.Workbook()
                # 获取当前活跃的worksheet,默认就是第一个worksheet
                ws = wb.active
                # save.save_to_excel_ad(self.double_list, ws)
                save.sava_data_to_xlsx(items, ws)
                wb.save(filepath)
            else:
                file = open(filepath, 'a+', encoding='gbk')
                print(filepath)
                save.save_data_to_excel(items, file)

    def save_txt(self):
        filepath, type = QFileDialog.getSaveFileName(self, "Save File", "../result",
                                                     'txt(*.txt)')  # 前面是地址，后面是文件类型,得到输入地址的文件名和地址
        # txt(*.txt*.xls);;image(*.png)不同类别
        if filepath == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            # 以下写你想进行的正常操作
            self.get_table_data()
            file = open(filepath, 'a+', encoding='gbk')
            print(filepath)
            save.save_data_to_txt(self.double_list, file)

    def save_excel(self):
        filepath, type = QFileDialog.getSaveFileName(self, "Save File",
                                                     "../result",
                                                     'xls(*.xls);;xlsx(*.xlsx)')
        if filepath == '':
            pass  # 防止关闭或取消导入关闭所有页面
        else:
            print("type:")
            print(type)
            if type == "xlsx(*.xlsx)":
                print("type")
                wb = openpyxl.Workbook()
                # 获取当前活跃的worksheet,默认就是第一个worksheet
                ws = wb.active
                # save.save_to_excel_ad(self.double_list, ws)
                save.sava_data_to_xlsx(self.double_list, ws)
                wb.save(filepath)

            else:
                # 以下写你想进行的正常操作
                file = open(filepath, 'a+', encoding='gbk')
                print(filepath)
                save.save_data_to_excel(self.double_list, file)

    def get_table_data(self):
        print("get_table_data")

        if self.TableWidget_2.item(0, 0) == None:
            items = []
            for row in range(self.TableWidget.rowCount()):
                items.append([])
                for column in range(self.TableWidget.columnCount()):
                    # line = []
                    # line.append(self.tableWidget_2.item(row, column).text())
                    items[row].append(self.TableWidget.item(row, column).text())
            return items
        else:
            items = []
            for row in range(self.TableWidget_2.rowCount()):
                items.append([])
                for column in range(self.TableWidget_2.columnCount()):
                    # line = []
                    # line.append(self.tableWidget_2.item(row, column).text())
                    items[row].append(self.TableWidget_2.item(row, column).text())
            return items


    def getValue(self, val):

        for i in val:
            brush = []
            print("0000000000000000000")
            error= self.judge_problem(i, brush)
            print("end")
            if error:
                print('may error')
                item = QListWidgetItem(i)
                #qss = 'QListWidgetItem{}'

                #setCustomStyleSheet(item, qss, qss)
                #item.setBackground(QBrush(QColor("#ffff99")))
                #print("brush:", brush.color())
                item.setForeground(QBrush(QColor(brush[0], brush[1], brush[2])))

                self.ListWidget.addItem(item)
            else:
                self.ListWidget.addItem(i)

        listModel = QStringListModel()
        listModel.setStringList(val)

    #判断是否出错
    def judge_problem(self, result, brush):
        if result.endswith('O'):   #0   O
            #brush = (255, 0, 0)
            brush.append(255)
            brush.append(0)
            brush.append(0)
            return True
        elif ' ' in result:      #-
            brush.append(0)
            brush.append(0)
            brush.append(255)
            return True
        elif result.istitle() and not(self.Num_In(result)):   #Vss
            #brush = (50, 205, 50)
            brush.append(50)
            brush.append(205)
            brush.append(50)
            return True
        else:
            return False
        #elif self.Num_In(result) and '[' in result:
            #return True
        #elif self.Num_In(result) and ']' in result:
            #return True

    def Num_In(self, s):
        for char in s:
            if char.isdigit():
                return True
        return False





    def input_btn_slot(self):
        print("input")
        # 获取当前选中行的行数
        row = self.TableWidget.currentRow()
        # 如果没有选中任何行，则返回
        if row == -1:
            print("no value")
            return
        # 获取整行的数据
        items = []
        for column in range(self.TableWidget.columnCount()):
            items.append(self.TableWidget.item(row, column).text())

        self._deleteRows(self.TableWidget)
        self.addRow(self.TableWidget_2, items)

        print("items:", items)

    def _deleteRows(self, tablewidget):
        """
        删除所选择行
        :return:
        """
        print('删除所选择行')
        s_items = tablewidget.selectedItems()  # 获取当前所有选择的items
        if s_items:
            selected_rows = []  # 求出所选择的行数
            for i in s_items:
                row = i.row()
                if row not in selected_rows:
                    selected_rows.append(row)
            for r in range(len(sorted(selected_rows))):
                tablewidget.removeRow(selected_rows[r] - r)  # 删除行

    def addRow(self, tablewidget, items):
        print("add")
        num = tablewidget.rowCount()
        tablewidget.setRowCount(num + 1)
        tablewidget.setColumnCount(2)
        tablewidget.setHorizontalHeaderLabels(['num', 'name'])
        for i in range(len(items)):
            # new_item = QStandardItem(self.double_list[i][j])
            new_item = QTableWidgetItem(items[i])
            tablewidget.setItem(num, i, new_item)  # 这一句有问题！！

    def output_btn_slot(self):
        print("output")
        # 获取当前选中行的行数
        row = self.TableWidget_2.currentRow()
        # 如果没有选中任何行，则返回
        if row == -1:
            print("no value")
            return
        # 获取整行的数据
        items = []
        for column in range(self.TableWidget_2.columnCount()):
            #line = []
            items.append(self.TableWidget_2.item(row, column).text())
        #items.append(line)

        self._deleteRows(self.TableWidget_2)
        self.addRow(self.TableWidget, items)

        print("items:", items)

    def getclearValue(self):
        self.double_list = []
        self.new_list = []
        self.ListWidget.clear()
        self.TableWidget.clear()
        self.TableWidget_2.clear()






class Sche(QWidget, Ui_Sche):
    def __init__(self, parent = None):
        super().__init__(parent = None)
        self.setupUi(self)

        self.component_list = []  # 用于存放元件的列表
        self.name_list = []
        self.draw = ''

        # 库页面
        self.scene_1 = Scene_1(self)
        self.view_1 = View_1(self.scene_1, self.library_widget)

        print("widet height:", self.library_widget.height())
        print("widget width:", self.library_widget.width())
        #self.view_1.setGeometry(QtCore.QRect(0, 0, 800, 800))

        self.import_btn.clicked.connect(self.slot_library_add)
        self.delete_btn.clicked.connect(self.delete)

    def slot_library_add(self):  # 传递信号
        # from component_info import Ui_Form
        self.m = import_ui()

        self.m.show()

        self.m.signal_1.connect(self.get_data)  # 将子窗口和当前窗口绑定以获取返回数据

        print(self.name_list)

    def get_data(self, designator, comment, list_info):
        # 用于接受子界面发过来的数据
        p = Component(designator, comment)
        p.set_pin(list_info)

        self.component_list.append(p)
        self.name_list.append(designator)

        # 库页面的
        item = myitem(designator, comment, list_info)
        self.component_listWidget.addItem(item)
        self.component_listWidget.setItemWidget(item, item.widget)
        self.component_listWidget.itemClicked.connect(self.item_click)
        self.component_listWidget.itemDoubleClicked.connect(self.item_double_click)

    def item_click(self, item):
        print("您选择了：", item.designator)
        self.designator_line.setText(item.designator)
        self.comment_line.setText(item.comment)

    def item_double_click(self, item):
        print("您双击了")
        self.scene_1.clear()
        p = Component(item.designator, item.comment)
        p.set_pin(item.pin_list)
        self.scene_1.addItem(p)
        self.offset_x = -300
        # 偏移量
        self.offset_y = -200
        p.setPos(0, 0)

        print("添加成功")

        for i in range(item.get_count()):
            pin = Pin(item.pin_list[i][0], item.pin_list[i][1])
            # self.scene_1.addItem(pin)
            # print("count:", item.get_count())
            self.set_position(pin, item.get_count(), i)

    def set_position(self, item, len, i):

        if len <= 4:
            self.scene_1.addItem(item)
            self.width = 200
            self.height = 300
            self.interval = int(self.height / (len + 1))
            item.setPos(self.width, (i + 1) * self.interval)

        elif 4 < len <= 8:
            self.width = 300
            self.height = 400
            self.interval = int(self.height / (4 + 1))
            if i < 4:
                self.scene_1.addItem(item)
                item.setPos(self.width, (i + 1) * self.interval)
            elif i >= 4:
                left_item = Pin_left(item.pin_num, item.pin_name)
                self.scene_1.addItem(left_item)
                left_item.setPos(0, (i - 3) * self.interval)



        elif 8 < len <= 48:
            # self.scene_1.addItem(item)
            self.width = 500
            self.height = 500

            num = math.ceil(len / 4)
            self.interval = int(self.height / (num + 1))

            # right
            if i < num:
                self.scene_1.addItem(item)
                item.setPos(self.width, (i + 1) * self.interval)
            # left
            elif num <= i < 2 * num:
                left_item = Pin_left(item.pin_num, item.pin_name)
                self.scene_1.addItem(left_item)
                left_item.setPos(0, (i - num + 1) * self.interval)
            # item.setTransformOriginPoint(0, 0)
            # item.setRotation(180)
            # up
            elif 2 * num <= i < 3 * num:
                self.scene_1.addItem(item)
                item.setPos((i - 2 * num + 1) * self.interval, 0)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(270)
            # down
            elif 3 * num <= i < len:
                self.scene_1.addItem(item)
                item.setPos((i - 3 * num + 1) * self.interval, self.height)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(90)


        elif 48 < len <= 96:
            self.width = 600
            self.height = 600

            num = math.ceil(len / 4)
            self.interval = int(self.height / (num + 1))

            # right
            if i < num:
                self.scene_1.addItem(item)
                item.setPos(self.width, (i + 1) * self.interval)
            # left
            elif num <= i < 2 * num:
                left_item = Pin_left(item.pin_num, item.pin_name)
                self.scene_1.addItem(left_item)
                left_item.setPos(0, (i - num + 1) * self.interval)
            # item.setTransformOriginPoint(0, 0)
            # item.setRotation(180)
            # up
            elif 2 * num <= i < 3 * num:
                self.scene_1.addItem(item)
                item.setPos((i - 2 * num + 1) * self.interval, 0)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(270)
            # down
            elif 3 * num <= i < len:
                self.scene_1.addItem(item)
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
                self.scene_1.addItem(item)
                item.setPos(self.width, (i + 1) * self.interval + 70)
            # left
            elif num <= i < 2 * num:

                left_item = Pin_left(item.pin_num, item.pin_name)
                self.scene_1.addItem(left_item)
                left_item.setPos(0, (i - num + 1) * self.interval + 70)
            # item.setTransformOriginPoint(0, 0)
            # item.setRotation(180)
            # up
            elif 2 * num <= i < 3 * num:
                self.scene_1.addItem(item)

                item.setPos((i - 2 * num + 1) * self.interval + 70, 0)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(270)
            # down
            elif 3 * num <= i < len:
                self.scene_1.addItem(item)
                item.setPos((i - 3 * num + 1) * self.interval + 70, self.height)
                item.setTransformOriginPoint(0, 0)
                item.setRotation(90)

    def delete(self):
        itemlist = self.scene_1.selectedItems()
        for i in range(0, len(itemlist)):
            self.scene_1.removeItem(itemlist[i])
        # del itemlist[i]
        del itemlist
