# a tool for viewing and editing bashrc related formatting.
# TODO: 
# 1. render bash prompt.
# 2. convert rgb color (hex-picker) to ANSI.
# 3. editor specifically for creating config files.
import colors
from jinja2 import Template
from colormap import rgb2hex, hex2rgb
import os, sys, logging, datetime, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QProcess
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QTextEdit, QToolButton, QLabel
try:
    from . import CodeEditor
    from QtColorPicker import ColorPicker
except ImportError:
    from FigUI.handler.Code import CodeEditor
    from FigUI.handler.Code.QtColorPicker import ColorPicker


class VisualizerShell(QWidget):
    '''You can display images with lsix.'''
    def __init__(self, parent=None, height=2):
        super(VisualizerShell, self).__init__()
        self.process = QProcess(self)
        self.process.start('xterm',['-into', str(int(self.winId())), 
                                    # '-ls',
                                    '-xrm', "'XTerm*selectToClipboard: true'",
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
        # loggerWindow.setLineWrapColumnOrWidth(200)
        # loggerWindow.setLineWrapMode(QTextEdit.FixedPixelWidth)
        # loggerWindow.verticalScrollBar().minimum()
class PromptEditor(QWidget):
    def __init__(self, parent=None):
        super(PromptEditor, self).__init__(parent)
        layout = QVBoxLayout()
        self.editor = QLineEdit()
        self.viewer = VisualizerShell(parent)
        layout.addWidget(self.editor)
        layout.addWidget(self.viewer)
        self.setLayout(layout)


class ANSIColorPicker(QWidget):
    def __init__(self, parent=None):
        super(ANSIColorPicker, self).__init__(parent)
        layout = QHBoxLayout()
        self.picked_color = (0,0,0,50)
        # create widgets.
        self.rgb_color = QLineEdit() # enter input color in rgb
        self.rgb_color.setText("0, 0, 0")
        self.rgb_color.returnPressed.connect(self.fromRGB)

        self.hex_color = QLineEdit() # enter input color in hex
        self.hex_color.setText("#000") 
        self.hex_color.returnPressed.connect(self.fromHex)

        self.ansi_color = QLineEdit()
        self.ansi_color.setReadOnly(True)

        self.color_tab = QPushButton()
        self.color_tab.setStyleSheet(f"background: #000")

        pickBtn = QToolButton(self)
        pickBtn.setText("pick")
        pickBtn.setToolTip("pick a color from the color-picker.")
        pickBtn.clicked.connect(lambda: self.launchDialog())
        # convBtn = QToolButton(self)
        # convBtn.setText("convert")
        # convBtn.setToolTip("convert from rgb or hex to ansi code.")
        # convBtn.clicked.connect(lambda: self.launchDialog())
        # convert color.
        hex_color = rgb2hex(self.picked_color[0], self.picked_color[1], self.picked_color[2])
        self.convt_color = colors.color("text", fg=hex_color) 
        self.ansi_color.setText(self.convt_color) 
        # setup layout.
        layout.addWidget(self.rgb_color)
        layout.addWidget(self.hex_color)
        layout.addWidget(self.ansi_color)
        layout.addWidget(self.color_tab)
        layout.addWidget(pickBtn)
        # layout.addWidget(convBtn)
        self.setLayout(layout)

    def fromRGB(self):
        self.picked_color = tuple(self.rgb_color.text().split(","))
        hex_color = rgb2hex(int(self.picked_color[0]), int(self.picked_color[1]), int(self.picked_color[2]))
        self.convt_color = colors.color("text", fg=hex_color) 
        self.ansi_color.setText(self.convt_color)
        self.rgb_color.setText(f"{int(self.picked_color[0])}, {int(self.picked_color[1])}, {int(self.picked_color[2])}")
        self.hex_color.setText(hex_color)
        self.color_tab.setStyleSheet(f"background: {hex_color}")

    def fromHex(self):
        hex_color = self.hex_color.text()
        self.picked_color = hex2rgb(hex_color)
        self.convt_color = colors.color("text", fg=hex_color) 
        self.ansi_color.setText(self.convt_color)
        self.rgb_color.setText(f"{int(self.picked_color[0])}, {int(self.picked_color[1])}, {int(self.picked_color[2])}")
        self.hex_color.setText(hex_color)
        self.color_tab.setStyleSheet(f"background: {hex_color}")

    def launchDialog(self):
        colorPicker = ColorPicker(useAlpha=True)
        self.picked_color = colorPicker.getColor((0,0,0,50))
        # print(self.picked_color)
        hex_color = rgb2hex(int(self.picked_color[0]), int(self.picked_color[1]), int(self.picked_color[2]))
        # print(hex_color)
        self.convt_color = colors.color("text", fg=hex_color) 
        # print(self.convt_color)
        self.ansi_color.setText(self.convt_color)
        self.rgb_color.setText(f"{int(self.picked_color[0])}, {int(self.picked_color[1])}, {int(self.picked_color[2])}")
        self.hex_color.setText(hex_color)
        self.color_tab.setStyleSheet(f"background: {hex_color}")


class BashrcCustomizer(QWidget):
    def __init__(self, parent=None, path="~/.bashrc"):
        super(BashrcCustomizer, self).__init__(parent)
        
        prompt_editor = PromptEditor(parent=parent)
        ansi_color_picker = ANSIColorPicker(parent=parent)
        code_editor = CodeEditor(path=path, parent=parent)
        
        prompt_editor.setMaximumHeight(100)
        ansi_color_picker.setMaximumHeight(100)

        layout = QVBoxLayout()
        layout.addWidget(code_editor)
        layout.addWidget(prompt_editor)
        layout.addWidget(ansi_color_picker)

        self.setLayout(layout)