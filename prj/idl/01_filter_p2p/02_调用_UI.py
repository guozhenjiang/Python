from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np

class DataFilter:
    def __init__(self):
        # ----------------------------------------------------------------------------------------------------
        # 加载数据记录文件
        # ----------------------------------------------------------------------------------------------------
        file = open('.\data\record_01_无遮挡2m.txt')
        content = file.read()
        file.close()

        # print('\r\n 文件内容：')
        # print(content)
        # print('\r\n')

        content = content.strip()
        # print('\r\n strip() 后文件内容：')
        # print(content)
        # print('\r\n')

        content = content.split(' ')
        # print('\r\n split(' ') 后文件内容：')
        # print(content)
        # print('\r\n')

        self.data = []
        # print('\r\n 填充内容之前的 data：')
        # print(data)
        # print('\r\n')

        for v in content:
            val = int(v, 16)
            # print(val)
            self.data.append(val)

        # print('\r\n 填充内容之后的 data：')
        # print(self.data)
        # print('\r\n')
        
        # ----------------------------------------------------------------------------------------------------
        # 加载 ui 文件
        # ----------------------------------------------------------------------------------------------------
        # 从文件中加载UI定义
        file = QFile('record_01_无遮挡2m.txt')
        file.open(QFile.ReadOnly)
        file.close()

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('ui_01.ui')
        
        # ----------------------------------------------------------------------------------------------------
        # 添加曲线
        # ----------------------------------------------------------------------------------------------------
        

        # self.ui.button.clicked.connect(self.handleCalc)

    # def handleCalc(self):
    #     info = self.ui.textEdit.toPlainText()

    #     salary_above_20k = ''
    #     salary_below_20k = ''
    #     for line in info.splitlines():
    #         if not line.strip():
    #             continue
    #         parts = line.split(' ')

    #         parts = [p for p in parts if p]
    #         name,salary,age = parts
    #         if int(salary) >= 20000:
    #             salary_above_20k += name + '\n'
    #         else:
    #             salary_below_20k += name + '\n'

    #     QMessageBox.about(self.ui,
    #                 '统计结果',
    #                 f'''薪资20000 以上的有：\n{salary_above_20k}
    #                 \n薪资20000 以下的有：\n{salary_below_20k}'''
    #                 )

app = QApplication([])
data_filter = DataFilter()
data_filter.ui.show()
app.exec_()