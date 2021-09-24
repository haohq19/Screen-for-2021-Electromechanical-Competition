"""
V1.0 developed by hhq
2021/9/24
"""

from PyQt5.QtWidgets import (QDesktopWidget, QComboBox, QLabel, QApplication, QSlider,
                             QHBoxLayout, QVBoxLayout, QWidget, QLineEdit, QPushButton)
from PyQt5.QtGui import QIntValidator, QPainter, QBrush, QColor, QPalette, QPixmap, QPen
from PyQt5.QtCore import Qt
import sys
import random


class Screen(QWidget):
    max_radius = 300
    min_radius = 1

    def __init__(self):
        super().__init__()

        self.mode = 0  # 模式缺省为0
        self.radius = Screen.min_radius  # 半径缺省为1

        self.mode_combo = QComboBox(self)  # 模式复选框
        self.mode_label = QLabel('mode option', self)  # 模式选择标签
        self.mode_hbox = QHBoxLayout()  # 模式选择部分布局

        self.radius_sld = QSlider(Qt.Horizontal, self)  # 半径调节条
        self.radius_le = QLineEdit(self)  # 半径输入框
        self.radius_label = QLabel('modify radius (px)', self)  # 调节标签
        self.radius_hbox = QHBoxLayout()  # 半径调节部分布局

        self.start_button = QPushButton('start', self)  # 绘图按钮

        self.vbox = QVBoxLayout()  # 左侧总布局

        self.initUI()

    def initUI(self):

        self.mode_combo.addItem("Item 0")
        self.mode_combo.addItem("Item 1")
        self.mode_combo.addItem("Item 2")
        self.mode_combo.currentIndexChanged.connect(self.indexEdited)

        self.mode_hbox.addWidget(self.mode_label)
        self.mode_hbox.addWidget(self.mode_combo)

        self.radius_sld.setFocusPolicy(Qt.NoFocus)
        self.radius_sld.setMinimum(Screen.min_radius)
        self.radius_sld.setMaximum(Screen.max_radius)
        self.radius_sld.setValue(Screen.min_radius)
        self.radius_sld.valueChanged[int].connect(self.valueEdited)

        self.radius_le.setValidator(QIntValidator())
        self.radius_le.setText(str(Screen.min_radius))
        self.radius_le.editingFinished.connect(self.lineEdited)

        self.radius_hbox.addWidget(self.radius_label)
        self.radius_hbox.addWidget(self.radius_sld)
        self.radius_hbox.addWidget(self.radius_le)

        self.start_button.clicked.connect(self.showPaint)

        self.vbox.addLayout(self.mode_hbox)
        self.vbox.addLayout(self.radius_hbox)
        self.vbox.addWidget(self.start_button)

        self.setLayout(self.vbox)

        self.resize(400, 200)
        self.center()
        self.setWindowTitle('screen')
        self.show()

    def center(self):

        frame = self.frameGeometry()
        center_position = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center_position)
        self.move(frame.topLeft())

    def indexEdited(self):

        self.mode = self.mode_combo.currentIndex()

    def lineEdited(self):

        test = self.radius_le.text()
        value = int(test)
        if Screen.max_radius < value:
            # self.blockSignals(True)
            self.radius_le.setText(str(Screen.max_radius))
            self.radius_sld.setValue(Screen.max_radius)
            # self.blockSignals(False)
        elif Screen.min_radius > value:
            # self.blockSignals(True)
            self.radius_le.setText(str(Screen.min_radius))
            self.radius_sld.setValue(Screen.min_radius)
            # self.blockSignals(False)
        else:
            self.radius_sld.setValue(value)

    def valueEdited(self, value):

        self.radius_le.setText(str(value))
        self.radius = value

    def showPaint(self):

        self.area = PaintArea(self.mode, self.radius)


class PaintArea(QWidget):

    def __init__(self, mode, radius):

        super().__init__()

        self.mode = mode
        self.radius = radius

        self.initUI()

    def initUI(self):

        #self.setGeometry(300, 300, 300, 190)
        #self.setWindowTitle('Paint')
        self.setWindowState(Qt.WindowFullScreen)
        self.setFixedSize(self.size().width(), self.size().height())

        if min(self.size().width(), self.size().height()) < 2 * self.radius:
            self.radius = min(self.size().width(), self.size().height()) // 2

        self.show()

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):

        if self.mode == 0:
            self.drawMode0(qp)
        elif self.mode == 1:
            self.drawMode1(qp)
        elif self.mode == 2:
            self.drawMode2(qp)
        else:
            pass

    def drawMode0(self, qp):
        """
        此函数用于绘制模式0
        在屏幕范围内绘制五个圆形靶子
        """
        col = QColor(0, 0, 0)
        col.setNamedColor('#000000')
        brush = QBrush(Qt.SolidPattern)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setBrush(brush)
        qp.setPen(pen)
        qp.drawRect(0, 0, self.size().width(), self.size().height())

        chuckWidth = (self.size().width() - 2 * self.radius)//16
        chuckHeight = (self.size().height() - 2 * self.radius)//9
        chuckRange = list()
        for i in range(16):
            for j in range(9):
                c = Chuck(i*chuckWidth, j*chuckHeight)
                chuckRange.append(c)
        for i in range(5):
            k = random.randint(0, len(chuckRange) - 1)
            wc = chuckRange[k].wc
            hc = chuckRange[k].hc

            col.setNamedColor('#17499d')
            brush.setColor(col)
            pen.setColor(col)
            qp.setBrush(brush)
            qp.setPen(pen)
            qp.drawEllipse(wc, hc, 2 * self.radius, 2 * self.radius)

            col.setNamedColor('#110b64')
            brush.setColor(col)
            pen.setColor(col)
            qp.setBrush(brush)
            qp.setPen(pen)
            qp.drawEllipse(wc + self.radius // 3, hc + self.radius // 3, 4 * self.radius // 3, 4 * self.radius // 3)

            col.setNamedColor('#17499d')
            brush.setColor(col)
            pen.setColor(col)
            qp.setBrush(brush)
            qp.setPen(pen)
            qp.drawEllipse(wc + 2 * self.radius // 3, hc + 2 * self.radius // 3, 2 * self.radius // 3, 2 * self.radius // 3)


            i = len(chuckRange) - 1
            while i >= 0:
                if chuckRange[i].dist(wc, hc) < 4 * self.radius * self.radius:
                    chuckRange.pop(i)
                i = i - 1

            if len(chuckRange) == 0:
                return

    def drawMode1(self, qp):
        """
        此函数用于绘制模式1
        在屏幕范围内绘制直线运动的单个靶子
        """

        pass

    def drawMode2(self, qp):
        """
        此函数用于绘制模式2
        在屏幕范围内绘制随机运动的靶子
        """

        pass

    def keyPressEvent(self, event):

        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        else:
            QWidget.keyPressEvent(self, event)


class Chuck:

    def __init__(self, w, h):
        self.wc = w
        self.hc = h

    def dist(self, x, y):
        return (self.wc - x) * (self.wc - x) + (self.hc - y) * (self.hc - y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Screen()
    sys.exit(app.exec_())
