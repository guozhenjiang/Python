# https://www.cnblogs.com/liming19680104/p/13211626.html?utm_source=tuicool


from PyQt5.QtWidgets import QApplication, QWidget
import sys
import pyqtgraph as pg
import numpy as np

class win(QWidget):
    def __init__(self):
        super().__init__()
        
        self.resize(600, 300)
        self.pw = pg.PlotWidget(self)   # 创建一个绘图控件
        
        # 要将 pyqtgraph 的图形添加到 pyqt5 的部件中，
        # 我们首先要做的就是将 pyqtgraph 的绘图方式由 window 改为 widget。
        # PlotWidget方法就是通过widget方法进行绘图的
        
        self.pw.resize(400, 200)
        self.pw.move(10, 10)
        data = np.random.random(size=50)
        
        self.pw.plot(data)  # 在绘图控件中绘制图形

if __name__=='__main__':
    app = QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(app.exec_())