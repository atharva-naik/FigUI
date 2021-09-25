try:
    import Xlib
except ImportError:
    pass
import logging
from PyQt5.QtCore import pyqtSlot, QProcess, Qt, QSize, QTimer
import os, sys, glob, pathlib, copy, time, datetime
from PyQt5.QtGui import QIcon, QWindow, QColor, QTextFormat
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QTextEdit


class FigShellCore(QWidget):
    '''You can display images with lsix.'''
    def __init__(self, parent=None, height=25, cmd=None):
        super(FigShellCore, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.process = QProcess(self)
        flags = ['-into', str(int(self.winId())), 
                # '-ls',
                '-xrm', "'XTerm*selectToClipboard: true'",
                '-ti', 'vt340', 
                '-fa', 'Monospace', 
                '-fs', '11', 
                '-geometry', f'300x{height}', 
                '-background', '#300a24']
        if cmd: 
            flags += ["-e", f'"{cmd}"']
            print(cmd)
        self.process.start('xterm', flags)
        # print(int(window.winId()))
        # self.terminal = QWidget.createWindowContainer(window, parent=self)
        blankWindow = QTextEdit()
        blankWindow.setReadOnly(True)
        # blankWindow.setsetFixedWidth(800)
        blankWindow.setFixedHeight(20*height+20)
        self.loggerWindow = QTextEdit()
        self.loggerWindow.setReadOnly(True)
        self.loggerWindow.setStyleSheet('''
        QTextEdit {
            background:#ffdb78; 
            color: black;
        }''')
        self.loggerWindow.cursorPositionChanged.connect(self.highlightLoggerLine)
        # loggerWindow.setLineWrapColumnOrWidth(200)
        # loggerWindow.setLineWrapMode(QTextEdit.FixedPixelWidth)
        # loggerWindow.verticalScrollBar().minimum()
        if parent:
            parent.logger.addWidget(self.loggerWindow)
            parent.logger.info(f"xterm opened into a window with id: {int(self.winId())}")
            # print("inside grand parent")
        layout.addWidget(blankWindow)
        layout.addWidget(self.loggerWindow)
        self.setLayout(layout)
        # print(str(int(self.winId())))
    def highlightLoggerLine(self):
        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor(Qt.yellow).lighter(160)
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)
        selection.cursor = self.loggerWindow.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.loggerWindow.setExtraSelections(extraSelections)

    
class FigShell(QWidget):
    def __init__(self, parent=None, height=25, cmd=None):
        super(FigShell, self).__init__(parent)
        layout = QVBoxLayout()
        self.shell = FigShellCore(parent, height, cmd)
        self._parent = parent
        self.window = QWindow.fromWinId(self.shell.winId())
        self.viewer = QWidget.createWindowContainer(self.window)
        layout.addWidget(self.shell)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setMinimumHeight(700)
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.periodicResizer)
        # self.timer.start(1000)
        # self._Parent = parent
    # def periodicResizer(self):
    #     print("resizing")
    #     if self._Parent:
    #         self._Parent.resize(QSize(700,650))
    #         time.sleep(2)
    #         self._Parent.resize(QSize(700,700))


# class FigShell(QWidget):
#     def __init__(self, parent=None, height=25, cmd=None):
#         super(FigShell, self).__init__(parent)
#         self.shellCore = FigShellCore(parent, height, cmd)
#         # QMainWindow creation.
#         self.mainWindow = QMainWindow()
#         self.mainWindow.setCentralWidget(self.shellCore)
#         self.mainWindow.show()
#         # QWindow creation.
#         self.window = QWindow.fromWinId(self.mainWindow.winId())
#         self.window.show()
#         # # create central widget.
#         self.centralWidget = QWidget.createWindowContainer(self.window)
#         # create layout and add widget.
#         layout = QVBoxLayout()
#         # layout.setContentsMargins(0, 0, 0, 0)
#         layout.addWidget(self.centralWidget)
#         # set layout
#         self.setLayout(layout)
#         self.setStyleSheet("background: red")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    shell = FigShell()
    window = QMainWindow()
    window.setCentralWidget(shell)
    window.show()
    sys.exit(app.exec_())