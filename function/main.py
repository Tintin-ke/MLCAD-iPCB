from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog, QMessageBox, QListWidget, QInputDialog, QLineEdit, QListWidgetItem
from PyQt5.QtWidgets import QTableView, QTableWidget,QTableWidgetItem, QLabel, QSlider, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QStringListModel, Qt, QAbstractTableModel, QRect, QRectF
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPen
from new_ui.main_ui import *
import sys
from qt_material import apply_stylesheet
import find_square as fs
import openpyxl
from angle_identify import angle_identify
from PIL import Image
from Schematic_design.import_ui import import_ui

from QCandyUi.CandyWindow import *
from QCandyUi import CandyWindow
import identify
import trans
import save
from Schematic_design.Scene import Scene_1
from Schematic_design.View import View_1
from Schematic_design.component import *
from Schematic_design.MyListWidgetItem import MyListWidgetItem as myitem
from Schematic_design.pin import Pin,Pin_left

#@colorful('blueDeep')


class main_window(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(main_window, self).__init__(parent)
		self.setupUi(self)

		self.list = []  # 识别图像后，存储信息的列表
		self.new_list = []  # 经过修改后的信息列表
		self.double_list = []  # 二维列表，num，name
		# self.name = []
		self.new_path = ''  # 手动截图或不截图的图片
		self.screenshots_path = ''  # 自动截图后的多张结果
		self.type = 'two_side_leftright'  # 默认识别的类型为two side
		self.name = []

		self.stackedWidget.setCurrentIndex(0)

		self.component_list = []  # 用于存放元件的列表
		self.name_list = []
		self.draw = ''

		self.group_num = 1

		#库页面
		self.scene_1 = Scene_1(self)
		self.view_1 = View_1(self.scene_1, self.library_widget)

		print("widet height:", self.library_widget.height())
		print("widget width:", self.library_widget.width())
		self.view_1.setGeometry(QtCore.QRect(15, 1, 1591, 1161))


		#界面切换
		self.menu_change.clicked.connect(self.change_form)

		#按钮
		self.open_image_btn.clicked.connect(self.openImage)
		self.seg_btn.clicked.connect(self.slot_auto_printscreen)
		self.up_image_btn.clicked.connect(self.slot_pic_up)
		self.next_image_btn.clicked.connect(self.slot_pic_down)
		self.sin90_btn.clicked.connect(self.Sinistral_rotation_slot)
		self.dex90_btn.clicked.connect(self.Dextral_rotation_slot)
		self.auto_rot_btn.clicked.connect(self.Automatic_rotation_slot)
		self.identify_btn.clicked.connect(self.slot_start)
		self.edit_btn.clicked.connect(self.slot_modify)
		self.add_btn.clicked.connect(self.slot_add)
		self.delete_btn_2.clicked.connect(self.slot_delete)
		self.save_btn.clicked.connect(self.slot_save)
		self.export_btn.clicked.connect(self.export_slot)
		#self.drag_btn.clicked.connect(self.slot_drag_mode)
		#self.select_btn.clicked.connect(self.slot_select_mode)

		self.import_btn.clicked.connect(self.slot_library_add)
		self.delete_btn.clicked.connect(self.delete)
		self.input_btn.clicked.connect(self.input_btn_slot)
		self.output_btn.clicked.connect(self.output_btn_slot)
		self.addgroup_btn.clicked.connect(self.group_btn_slot)



		#rationbutton
		self.dual_left_btn.setChecked(True)
		self.dual_left_btn.toggled.connect(self.dual_leftright_clicked)
		self.dual_up_btn.toggled.connect(self.dual_updown_clicked)
		self.quad_btn.toggled.connect(self.quad_clicked)

		self.component_listWidget.itemClicked.connect(self.item_click)
		self.component_listWidget.itemDoubleClicked.connect(self.item_double_click)

		# 点击事件获取所选内容、行列
		#self.tableWidget.cellPressed.connect(self.getPosContent)

	#切换页面
	def change_form(self):
		item = self.menu_change.currentItem()
		if item.text(0)=='识别':
			self.stackedWidget.setCurrentIndex(0)
		elif item.text(0) == '编辑':
			self.stackedWidget.setCurrentIndex(1)
		elif item.text(0) == '符号库':
			self.stackedWidget.setCurrentIndex(2)

	#打开文件
	def openImage(self):
		global imgNamepath
		imgNamepath, imgType = QFileDialog.getOpenFileName(self.open_image_btn, "打开文件夹",
														   "D:\\PycharmProject\\chip_album\\re_chip",
														   "*.jpg;;*.png;;All Files(*)")
		if imgNamepath == '':
			pass  # 防止关闭或取消导入关闭所有页面
		else:
			# 以下写你想进行的正常操作
			img = QtGui.QPixmap(imgNamepath).scaled(self.image_label.width(), self.image_label.height())
			self.image_label.setPixmap(img)
			self.file_path_line.setText(imgNamepath)
			self.clearlist()

	def dual_updown_clicked(self):
		self.type = 'two_side_updown'


	def dual_leftright_clicked(self):
		self.type = 'two_side_leftright'

	def quad_clicked(self):
		self.type = 'four_side'

	def clearlist(self):
		self.list = []
		self.new_list = []
		self.double_list = []
		self.name_label = []
		self.listWidget.clear()
		self.tableWidget.clear()

	def slot_auto_printscreen(self):                               #分割图片
		self.screenshots_path = fs.auto_(imgNamepath, self.type, self.name)
		#if self.name != []:
		#	self.file_path_line.setText(self.name[0])
		print("这里是screenshots_path:",self.screenshots_path)
		new_img = QtGui.QPixmap(self.screenshots_path[0]).scaled(self.image_label.width(), self.image_label.height())
		self.image_label.setPixmap(new_img)
		self.file_path_line.setText(self.screenshots_path[0])
		print(self.file_path_line.text())

	def slot_pic_up(self):
		current_imgpath = self.file_path_line.text()
		current_index = self.screenshots_path.index(current_imgpath)
		up_index = (current_index - 1 + len(self.screenshots_path)) % len(self.screenshots_path)
		self.file_path_line.setText(self.screenshots_path[up_index])
		up_img = QtGui.QPixmap(self.screenshots_path[up_index]).scaled(self.image_label.width(), self.image_label.height())
		self.image_label.setPixmap(up_img)

	def slot_pic_down(self):
		current_imgpath = self.file_path_line.text()
		current_index = self.screenshots_path.index(current_imgpath)
		down_index = (current_index + 1) % len(self.screenshots_path)
		self.file_path_line.setText(self.screenshots_path[down_index])
		down_img = QtGui.QPixmap(self.screenshots_path[down_index]).scaled(self.image_label.width(), self.image_label.height())
		self.image_label.setPixmap(down_img)

	def Automatic_rotation_slot(self):
		#print("auto")
		if len(self.screenshots_path) == 0:
			print("没有图片")
			return
		#print(self.screenshots_path)

		current_imgpath = self.file_path_line.text()  # 获取当前图片的名字
		current_index = self.screenshots_path.index(current_imgpath)

		for i in range(0, len(self.screenshots_path)):
			img = self.screenshots_path[i]
			angle_identify(img)

		print("自动旋转结束")

#逆时针旋转90
	def Sinistral_rotation_slot(self):
		print("left")
		if len(self.screenshots_path) == 0:
			print("没有图片")
			return

		current_imgpath = self.file_path_line.text()  # 获取当前图片的名字
		current_index = self.screenshots_path.index(current_imgpath)

		img = Image.open(current_imgpath)
		img = img.transpose(Image.ROTATE_90)  # 旋转90度
		img.save(current_imgpath)

		new_img = QtGui.QPixmap(current_imgpath).scaled(self.image_label.width(), self.image_label.height())
		self.image_label.setPixmap(new_img)  # 展示

	#顺时针旋转90
	def Dextral_rotation_slot(self):
		print("right")
		if len(self.screenshots_path) == 0:
			print("没有图片")
			return

		current_imgpath = self.file_path_line.text()  # 获取当前图片的名字
		current_index = self.screenshots_path.index(current_imgpath)

		img = Image.open(current_imgpath)
		img = img.transpose(Image.ROTATE_270)  # 旋转90度
		img.save(current_imgpath)

		new_img = QtGui.QPixmap(current_imgpath).scaled(self.image_label.width(), self.image_label.height())
		self.image_label.setPixmap(new_img)  # 展示

	def slot_start(self):
		#global  list
		lan_choice = 'en'    #获取语言模型
		#self.slot_auto_printscreen()

		if self.type == 'BGA':
			print("BGA")
			current_imgpath = self.file_path_line.text()  # 获取当前图片的名字
			identify.identi_BGA(current_imgpath)

			return


		if len(self.screenshots_path) == 0:
			print("只有一张图片")
			current_imgpath = self.file_path_line.text()  # 获取当前图片的名字
			self.list = identify.identi(current_imgpath, lan_choice)

			new_img = QtGui.QPixmap('results.jpg').scaled(self.image_label.width(), self.image_label.height())  # 展示图片

			# new_img = QtGui.QPixmap(result_path).scaled(self.G_label.width(), self.G_label.height())
			self.image_label.setPixmap(new_img)  # 展示
			self.file_path_line.setText('results.jpg')

			for i in self.list:
				self.listWidget.addItem(i)

			listModel = QStringListModel()
			listModel.setStringList(self.list)


		else:
			print("多张结果")
			self.list = identify.identi_more_pic(self.screenshots_path, lan_choice)  # 识别图片
			current_imgpath = self.file_path_line.text()  # 获取当前图片的名字
			current_index = self.screenshots_path.index(current_imgpath)

			result_path = []
			for i in range(0, len(self.screenshots_path)):
				result_path.append(f'results_{i + 1}.jpg')  # 将截取后标注的图片存储到列表中

			self.screenshots_path = result_path[:]  # 用result_path替换new_path
			new_img = QtGui.QPixmap(self.screenshots_path[0]).scaled(self.image_label.width(), self.image_label.height())  # 展示图片
			print('0')

			# new_img = QtGui.QPixmap(result_path).scaled(self.G_label.width(), self.G_label.height())

			##################
			self.image_label.setPixmap(new_img)  # 展示
			self.file_path_line.setText(self.screenshots_path[0])
			#print('1')
			##########

			print('\n')
			print("\n/ntest list.....:\n", self.list)
			print('\n')

			for i in self.list:
				self.listWidget.addItem(i)

			listModel = QStringListModel()
			listModel.setStringList(self.list)

	def slot_modify(self):
		item = self.listWidget.currentItem()
		num = self.listWidget.row(item)
		item.setFlags(item.flags()|Qt.ItemIsEditable)
		self.listWidget.editItem(item)

	def slot_add(self):
		reply = QMessageBox.question(self, '确认', '确认添加数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			item = self.listWidget.currentItem()
			num = self.listWidget.row(item)
			print(num)
			#self.listWidget.takeItem(self.listWidget.row(item))
			value, ok = QInputDialog.getText(self, "增加", "请输入增加的信息:", QLineEdit.Normal, "default")
			print(value)
			self.listWidget.insertItem(num, value)


	def slot_delete(self):
		reply = QMessageBox.question(self, '确认', '确认删除数据？', QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			item = self.listWidget.currentItem()
			num = self.listWidget.row(item)         #获取当前选中的行号
			print(num)
			self.listWidget.takeItem(self.listWidget.row(item))

	def slot_save(self):
		length = self.listWidget.count()
		print(length)
		self.new_list = []
		for i in range(length):
			item = self.listWidget.item(i)
			text = item.text()
			self.new_list.append(text)
		print(self.new_list)

		self.double_list = trans.transfer(self.new_list)     #将一维列表转换成二维列表
		print("转换完成")

		count = len(self.double_list)
		print(count)

		#self.tableWidget = QTableWidget(count, 2, self)
		self.tableWidget.setRowCount(count)
		self.tableWidget.setColumnCount(2)
		self.tableWidget.setHorizontalHeaderLabels(['num', 'name'])

		self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
		self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)


		for i in range(len(self.double_list)):
			for j in range(len(self.double_list[i])):
				#new_item = QStandardItem(self.double_list[i][j])
				new_item = QTableWidgetItem(self.double_list[i][j])
				self.tableWidget.setItem(i, j, new_item)    #这一句有问题！！

	def export_slot(self):
		filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "D:\\PycharmProject\\image\\result",
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



	# txt(*.txt*.xls);;image(*.png)不同类别

	def save_txt(self):
		filepath, type = QFileDialog.getSaveFileName(self, "文件保存", "D:\\PycharmProject\\image\\result",
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
		filepath, type = QFileDialog.getSaveFileName(self, "文件保存",
													 "D:\\PycharmProject\\image\\result",
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
				#save.save_to_excel_ad(self.double_list, ws)
				save.sava_data_to_xlsx(self.double_list, ws)
				wb.save(filepath)

			else:
				# 以下写你想进行的正常操作
				file = open(filepath, 'a+', encoding='gbk')
				print(filepath)
				save.save_data_to_excel(self.double_list, file)

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
		#偏移量
		self.offset_y = -200
		p.setPos(0, 0)

		print("添加成功")

		for i in range(item.get_count()):
			pin = Pin(item.pin_list[i][0], item.pin_list[i][1])
			#self.scene_1.addItem(pin)
			#print("count:", item.get_count())
			self.set_position(pin, item.get_count(), i)
	'''
	def slot_drag_mode(self):
		self.view_1.setDragMode(QGraphicsView.ScrollHandDrag)

		if self.view_1.DragMode == QGraphicsView.ScrollHandDrag:
			print("main+")
		if self.view_1.DragMode == QGraphicsView.RubberBandDrag:
			print("none")

	def slot_select_mode(self):
		self.view_1.setDragMode(QGraphicsView.RubberBandDrag)
	'''

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
			#self.scene_1.addItem(item)
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
				#item.setTransformOriginPoint(0, 0)
				#item.setRotation(180)
			# up
			elif 2 * num <= i < 3 * num:
				self.scene_1.addItem(item)
				item.setPos((i - 2 * num + 1) * self.interval, 0)
				item.setTransformOriginPoint(0, 0)
				item.setRotation(270)
			#down
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
				#item.setTransformOriginPoint(0, 0)
				#item.setRotation(180)
			# up
			elif 2 * num <= i < 3 * num:
				self.scene_1.addItem(item)
				item.setPos((i - 2 * num + 1) * self.interval, 0)
				item.setTransformOriginPoint(0, 0)
				item.setRotation(270)
			#down
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
				#item.setTransformOriginPoint(0, 0)
				#item.setRotation(180)
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

	def get_table_data(self):
		print("get_table_data")
		items = []
		for row in range(self.tableWidget_2.rowCount()):
			items.append([])
			for column in range(self.tableWidget_2.columnCount()):
				#line = []
				#line.append(self.tableWidget_2.item(row, column).text())
				items[row].append(self.tableWidget_2.item(row, column).text())

		return items
		#print('new_items:', items)


	def input_btn_slot(self):
		print("input")
		#获取当前选中行的行数
		row = self.tableWidget.currentRow()
		#如果没有选中任何行，则返回
		if row == -1:
			print("no value")
			return
		#获取整行的数据
		items = []
		for column in range(self.tableWidget.columnCount()):
			items.append(self.tableWidget.item(row, column).text())

		self._deleteRows(self.tableWidget)
		self.addRow(self.tableWidget_2, items)

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


	def addRow(self,tablewidget, items):
		print("add")
		num = tablewidget.rowCount()
		tablewidget.setRowCount(num + 1)
		tablewidget.setColumnCount(2)
		tablewidget.setHorizontalHeaderLabels(['num', 'name'])
		for i in range(len(items)):
				#new_item = QStandardItem(self.double_list[i][j])
				new_item = QTableWidgetItem(items[i])
				tablewidget.setItem(num, i, new_item)

	def output_btn_slot(self):
		print("output")
		# 获取当前选中行的行数
		row = self.tableWidget_2.currentRow()
		# 如果没有选中任何行，则返回
		if row == -1:
			print("no value")
			return
		# 获取整行的数据
		items = []
		for column in range(self.tableWidget_2.columnCount()):
			#line = []
			items.append(self.tableWidget_2.item(row, column).text())
		#items.append(line)

		self._deleteRows(self.tableWidget_2)
		self.addRow(self.tableWidget, items)

		print("items:", items)

	def group_btn_slot(self):
		print(self.group_num)
		#groupHeaderItem = QTableWidgetItem("Cubes")
		#groupHeaderItem.setTextAlignment(Qt.AlignVCenter)
		#self.tableWidget_2.setHorizontalHeaderItem(groupHeaderItem)
		#self.tableWidget_2.setColumnCount(2)
		#self.tableWidget_2.setRowCount(4)
		#self.tableWidget_2.setSpan(0,0,0,2)
		#self.tableWidget_2.setHorizontalHeaderItem(0, QTableWidgetItem(str(self.group_num))
		self.group_num += 1

	"""
	# 获取选中行列、内容
	def getPosContent(self, row, col):
		try:
			content = self.tableWidget.item(row, col).text()
			print("选中行：" + str(row))
			print("选中列：" + str(col))
			print('选中内容:' + content)
		except:
			print('选中内容为空')
	"""


if __name__ == "__main__":
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

	app = QApplication(sys.argv)
	test_demo = main_window()
	#test_demo = CandyWindow.createWindow(test_demo, 'blueDeep')
	apply_stylesheet(app, theme='light_blue.xml')
	test_demo.setWindowTitle('iPCB Lib')
	test_demo.show()





	sys.exit(app.exec_())


'''
from PyQt5.QtWidgets import QDesktopWidget#桌面类
screen = QDesktopWidget().screenGeometry()  # 自动适应屏幕宽高
width = screen.width()
height = screen.height()
MainWindow.resize(width - 25, height - 125)  # 这里比电脑桌面宽高各缩小了一点，以免电脑的状态栏遮掉了自己的窗口状态栏
'''