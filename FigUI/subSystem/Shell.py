try:
    import Xlib
except ImportError:
    pass
import logging
from PyQt5.QtGui import QIcon, QWindow
from PyQt5.QtCore import pyqtSlot, QProcess
import os, sys, glob, pathlib, copy, time, datetime
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QTextEdit


class FigShell(QWidget):
    '''You can display images with lsix.'''
    def __init__(self, parent=None, height=25):
        super(FigShell, self).__init__()
        layout = QVBoxLayout(self)
        self.process = QProcess(self)
        self.process.start('xterm',['-into', str(int(self.winId())), 
                                    '-ti', 'vt340', 
                                    '-fa', 'Monospace', 
                                    '-fs', '11', 
                                    '-geometry', f'300x{height}', 
                                    '-background', '#300a24'])
        # print(int(window.winId()))
        # self.terminal = QWidget.createWindowContainer(window, parent=self)
        blankWindow = QTextEdit()
        blankWindow.setReadOnly(True)
        blankWindow.setFixedHeight(20*height+20)
        loggerWindow = QTextEdit()
        loggerWindow.setReadOnly(True)
        loggerWindow.setStyleSheet("background:black")
        # loggerWindow.setLineWrapColumnOrWidth(200)
        # loggerWindow.setLineWrapMode(QTextEdit.FixedPixelWidth)
        # loggerWindow.verticalScrollBar().minimum()
        if parent:
            parent.logger.addWidget(loggerWindow)
            parent.logger.info(f"xterm opened into a window with id: {int(self.winId())}")
        # layout.addWidget(self.terminal)
        layout.addWidget(blankWindow)
        layout.addWidget(loggerWindow)
        self.setLayout(layout)
        # print(str(int(self.winId())))

    
