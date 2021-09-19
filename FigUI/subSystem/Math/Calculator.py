import os, sys
# import tempfile, random
# import textwrap, subprocess
# from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QCursor, QPixmap, QColor, QTextFormat
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QApplication, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QGraphicsColorizeEffect, QAction, QSizePolicy
# class FigCalculator(QWidget):
#     def __init__(self, parent=None):
#         super(FigCalculator, self).__init__(parent)
def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)

class FigCalculator(QMainWindow):
    def __init__(self):
        super(FigCalculator, self).__init__()
        titleBar = self.initTitleBar()
        calcWidget = Calculator(self)
        self.addToolBar(Qt.TopToolBarArea, titleBar)
        self.setCentralWidget(calcWidget)
        self.setGeometry(100, 100, 360, 370) 
        self.setWindowTitle("ℂ𝕒𝕝𝕔𝕦𝕝𝕒𝕥𝕠𝕣") 
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowIcon(FigIcon("sidebar/calculator.png"))
        # self.show()
    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        # Store the positions of mouse and window and
        # change the window position relative to them.
        self.windowPos = self.pos()
        self.mousePos = event.globalPos()
        super(FigCalculator, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.move(self.windowPos + event.globalPos() - self.mousePos)
        super(FigCalculator, self).mouseMoveEvent(event)

    def initTitleBar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("margin: 0px; padding-top: 1px; border: 0px")
        toolbar.setIconSize(QSize(22,22))
        toolbar.setMovable(False)

        closeBtn = QAction(self)
        closeBtn.setToolTip("close window")
        closeBtn.setIcon(FigIcon("close.svg")) 
        closeBtn.triggered.connect(lambda: self.close()) # closing logic.

        minimizeBtn = QAction(self)
        minimizeBtn.setToolTip("minimize window")
        minimizeBtn.setIcon(FigIcon("minimize.svg"))
        minimizeBtn.triggered.connect(lambda: self.showMinimized())

        maximizeBtn = QAction(self)
        maximizeBtn.setToolTip("maximize window")
        maximizeBtn.setIcon(FigIcon("maximize.svg"))
        maximizeBtn.triggered.connect(lambda: self.maximize())

        ontopBtn = QAction(self)
        opacUpBtn = QAction(self)
        opacDownBtn = QAction(self)

        windowTitle = QLabel()
        windowTitle.setText("ℂ𝕒𝕝𝕔𝕦𝕝𝕒𝕥𝕠𝕣") #("𝗙ig 𝗜s a 𝗚UI")

        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toolbar.addAction(closeBtn)
        toolbar.addAction(minimizeBtn)
        toolbar.addAction(maximizeBtn)
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(windowTitle)
        toolbar.addWidget(right_spacer)
        toolbar.addAction(opacUpBtn)
        toolbar.addAction(opacDownBtn)
        toolbar.addAction(ontopBtn)

        return toolbar


class Calculator(QWidget):
    def __init__(self, parent=None):
        super(Calculator, self).__init__(parent)
        # self.setWindowTitle("Fig Calculator")
        # self.setGeometry(100, 100, 360, 350)  
        self.initUI()
        self.setGeometry(0, 0, 360, 350) 
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.show()
    def initUI(self):
        # creating a label
        self.label = QLabel(self)
  
        # setting geometry to the label
        self.label.setGeometry(5, 5, 350, 70)
  
        # creating label multi line
        self.label.setWordWrap(True)
  
        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 4px solid black;"
                                 "background : white;"
                                 "}")
  
        # setting alignment to the label
        self.label.setAlignment(Qt.AlignRight)
  
        # setting font
        self.label.setFont(QFont('Arial', 15))
  
  
        # adding number button to the screen
        # creating a push button
        push1 = QPushButton("1", self)
  
        # setting geometry
        push1.setGeometry(5, 150, 80, 40)
  
        # creating a push button
        push2 = QPushButton("2", self)
  
        # setting geometry
        push2.setGeometry(95, 150, 80, 40)
  
        # creating a push button
        push3 = QPushButton("3", self)
  
        # setting geometry
        push3.setGeometry(185, 150, 80, 40)
  
        # creating a push button
        push4 = QPushButton("4", self)
  
        # setting geometry
        push4.setGeometry(5, 200, 80, 40)
  
        # creating a push button
        push5 = QPushButton("5", self)
  
        # setting geometry
        push5.setGeometry(95, 200, 80, 40)
  
        # creating a push button
        push6 = QPushButton("5", self)
  
        # setting geometry
        push6.setGeometry(185, 200, 80, 40)
  
        # creating a push button
        push7 = QPushButton("7", self)
  
        # setting geometry
        push7.setGeometry(5, 250, 80, 40)
  
        # creating a push button
        push8 = QPushButton("8", self)
  
        # setting geometry
        push8.setGeometry(95, 250, 80, 40)
  
        # creating a push button
        push9 = QPushButton("9", self)
  
        # setting geometry
        push9.setGeometry(185, 250, 80, 40)
  
        # creating a push button
        push0 = QPushButton("0", self)
  
        # setting geometry
        push0.setGeometry(5, 300, 80, 40)
  
        # adding operator push button
        # creating push button
        push_equal = QPushButton("=", self)
  
        # setting geometry
        push_equal.setGeometry(275, 300, 80, 40)
  
        # adding equal button a color effect
        c_effect = QGraphicsColorizeEffect()
        c_effect.setColor(Qt.blue)
        push_equal.setGraphicsEffect(c_effect)
  
        # creating push button
        push_plus = QPushButton("+", self)
  
        # setting geometry
        push_plus.setGeometry(275, 250, 80, 40)
  
        # creating push button
        push_minus = QPushButton("-", self)
  
        # setting geometry
        push_minus.setGeometry(275, 200, 80, 40)
  
        # creating push button
        push_mul = QPushButton("*", self)
  
        # setting geometry
        push_mul.setGeometry(275, 150, 80, 40)
  
        # creating push button
        push_div = QPushButton("/", self)
  
        # setting geometry
        push_div.setGeometry(185, 300, 80, 40)
  
        # creating push button
        push_point = QPushButton(".", self)
  
        # setting geometry
        push_point.setGeometry(95, 300, 80, 40)
  
  
        # clear button
        push_clear = QPushButton("Clear", self)
        push_clear.setGeometry(5, 100, 200, 40)
  
        # del one character button
        push_del = QPushButton("Del", self)
        push_del.setGeometry(210, 100, 145, 40)
  
        # adding action to each of the button
        push_minus.clicked.connect(self.action_minus)
        push_equal.clicked.connect(self.action_equal)
        push0.clicked.connect(self.action0)
        push1.clicked.connect(self.action1)
        push2.clicked.connect(self.action2)
        push3.clicked.connect(self.action3)
        push4.clicked.connect(self.action4)
        push5.clicked.connect(self.action5)
        push6.clicked.connect(self.action6)
        push7.clicked.connect(self.action7)
        push8.clicked.connect(self.action8)
        push9.clicked.connect(self.action9)
        push_div.clicked.connect(self.action_div)
        push_mul.clicked.connect(self.action_mul)
        push_plus.clicked.connect(self.action_plus)
        push_point.clicked.connect(self.action_point)
        push_clear.clicked.connect(self.action_clear)
        push_del.clicked.connect(self.action_del)
  
  
    def action_equal(self):
  
        # get the label text
        equation = self.label.text()
  
        try:
            # getting the ans
            ans = eval(equation)
  
            # setting text to the label
            self.label.setText(str(ans))
  
        except:
            # setting text to the label
            self.label.setText("Wrong Input")
  
    def action_plus(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " + ")
  
    def action_minus(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " - ")
  
    def action_div(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " / ")
  
    def action_mul(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + " * ")
  
    def action_point(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + ".")
  
    def action0(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "0")
  
    def action1(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "1")
  
    def action2(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "2")
  
    def action3(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "3")
  
    def action4(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "4")
  
    def action5(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "5")
  
    def action6(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "6")
  
    def action7(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "7")
  
    def action8(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "8")
  
    def action9(self):
        # appending label text
        text = self.label.text()
        self.label.setText(text + "9")
  
    def action_clear(self):
        # clearing the label text
        self.label.setText("")
  
    def action_del(self):
        ''' clearing a single digit ''' 
        text = self.label.text()
        # print(text[:len(text)-1])
        self.label.setText(text[:len(text)-1])


def calculator():
    calcApp = QApplication(sys.argv)  
    calcWindow = FigCalculator()  
    sys.exit(calcApp.exec())

if __name__ == "__main__":
    calculator()
