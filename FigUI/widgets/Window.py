#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, math
import mimetypes, platform
import json, datetime, pathlib
import psutil, webbrowser, threading
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QThread, QUrl, pyqtSignal, QObject, QTimer, QPoint, QRect, QSize, Qt, QT_VERSION_STR, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QPainter, QTransform, QCursor, QPixmap, QWindow, QTextCharFormat, QSyntaxHighlighter, QFontDatabase, QTextFormat, QColor, QPainter, QDesktopServices
from PyQt5.QtWidgets import QMenu, QShortcut, QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QTabBar, QDesktopWidget, QLabel, QToolButton, QTextEdit, QComboBox, QListWidget, QListWidgetItem, QScrollArea, QDockWidget, QGraphicsBlurEffect, QSplitter, QShortcut, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QSplashScreen
# utility functions
def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)

def FigFont(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/fonts")
    path = os.path.join(__icons__, name)

    return QFont(path)

def __font__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/fonts")
    path = os.path.join(__icons__, name)

    return path

def __icon__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return path

def __asset__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __assets__ = os.path.join(__current_dir__, "../assets")
    path = os.path.join(__assets__, name)

    return path

try:
    from FigUI.utils import *
    # from Theme import FigTheme
    # from Tab import FigTabWidget
    from FigUI.widgets.SearchBar import FigSearchBar
    from FigUI.subSystem.History import HistoryLogger
    from FigUI.widgets.Taskbar import SmartPhoneTaskBar
    from FigUI.subSystem.TaskViewer import FigTaskWebView
    from FigUI.widgets.QRCodeCreator import FigQRCodeWindow
    from FigUI.widgets.ActivityPanel import FigActivityPanel
    from FigUI.handler.Code.QtColorPicker import ColorPicker
    from FileViewer import FigFileViewer, FigTreeFileExplorer
    from FigUI.subSystem.System.Network import NetworkHandler
    from FigUI.subSystem.Math.Calculator import FigCalculator
    from FigUI.subSystem.System.Power import FigPowerController
    from FigUI.subSystem.System.Display import BrightnessController
#     from utils import *
except ImportError:
    from ..utils import *
    # from .Theme import FigTheme
    # from .Tab import FigTabWidget
    from .SearchBar import FigSearchBar
    from .Taskbar import SmartPhoneTaskBar
    from .QRCodeCreator import FigQRCodeWindow
    from .ActivityPanel import FigActivityPanel
    from ..subSystem.History import HistoryLogger
    from ..subSystem.TaskViewer import FigTaskWebView
    from ..handler.Code.QtColorPicker import ColorPicker
    from ..subSystem.System.Network import NetworkHandler
    from ..subSystem.Math.Calculator import FigCalculator
    from ..subSystem.System.Power import FigPowerController
    from .FileViewer import FigFileViewer, FigTreeFileExplorer
    from ..subSystem.System.Display import BrightnessController

try: 
    from FigUI.handler.Code import CodeEditor
except ImportError: 
    from ..handler.Code import CodeEditor
#     from .utils import *
def openQRCodeWindow(url=None, clipboard=None):
    qrCodeWindow = FigQRCodeWindow(url, clipboard)
    qrCodeWindow.show()

def openCalculator():
    calculator = FigCalculator()
    calculator.show()

# platform name
PLATFORM = platform.system()
# system controllers.
brightnessCtrl = BrightnessController()


class FigWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self, obj, func, *args, **kwargs):
        getattr(obj, func)(*args, **kwargs)
        self.finished.emit()

    def sleep_n_run(self, obj, func, *args, 
                    sleep_interval=2, **kwargs):
        pyqtSleep(sleep_interval)
        getattr(obj, func)(*args, **kwargs)
        self.finished.emit()


class FigAppBtn(QPushButton):
    def __init__(self, 
                 orig_size=30, 
                 hover_size=40, 
                 **kwargs):
        super(FigAppBtn, self).__init__(**kwargs)
        self.orig_size = orig_size
        self.hover_size = hover_size
        self.setIconSize(QSize(orig_size,
                               orig_size))
        self.taskBarAppStyle = '''
            QPushButton {
                color: #fff; 
                background: transparent; 
                border: 0px; 
                border-radius: 20px;
                /* padding-top: 5px;
                padding-bottom: 5px;
                padding-left: 4px;
                padding-right: 4px; */
            }
            /* QPushButton:hover {
                background: rgba(235, 235, 235, 0.5);
            } */
            QToolTip  {
                background: #292929;
                color: #fff;
                border: 0px;
            }
        '''
        self.setStyleSheet(self.taskBarAppStyle)

    def leaveEvent(self, event):
        self.setIconSize(QSize(self.orig_size, 
                               self.orig_size))

    def enterEvent(self, event):
        self.setIconSize(QSize(self.hover_size, 
                               self.hover_size))


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setStyleSheet("background: gray; border: 0px")
        self.setFrameShadow(QFrame.Raised)


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet("color: white")


class TimeDisplay(QLabel):
    def __init__(self, parent=None):
        super(TimeDisplay, self).__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateTime)
        self.timer.start(1000)
        # self.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
    def _updateTime(self):
        currTime = datetime.datetime.strftime(
            datetime.datetime.now(), 
            "  %-I:%M:%S %p\n%a %-m/%-d/%Y"
        )
        self.setText(currTime)


class BatteryDisplay(QPushButton):
    def __init__(self, parent=None):
        super(BatteryDisplay, self).__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateTime)
        self.timer.start(1000)
        # self.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
    def _updateTime(self):
        batLvl = psutil.sensors_battery()
        percent = int(batLvl.percent)
        pluggedIn = batLvl.power_plugged
        self.setText(f"({percent}%)")
        
        if pluggedIn:
            self.setIcon(FigIcon("bottombar/plugged.svg"))
        else:
            self.setIcon(QIcon())
        self.setIconSize(QSize(16,16))


class NetDisplay(QPushButton):
    def __init__(self, parent=None):
        super(NetDisplay, self).__init__(parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateWifiInfo)
        self.timer.start(1000)
        self.net_handler = NetworkHandler()
        # self.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.setIcon(FigIcon("bottombar/wifi.svg"))
        self.setIconSize(QSize(16,16))

    def _updateWifiInfo(self):
        info = self.net_handler.manager.net_info
        net_name = info.name
        # print(info.name)
        self.setText(net_name)


class QFolderNavBtn(QPushButton):
    def __init__(self, text, till_now, parent=None):
        super(QFolderNavBtn, self).__init__(parent)
        self.setText(text)
        self._till_now = till_now
        self._display_text = text

    def callback(self):
        print(f"QFolderNavBtn(text={self._display_text}, till_now={self._till_now}) clicked")
        self.fileViewer.openPath(self._till_now)

    def connectLauncher(self, fileViewer):
        self.fileViewer = fileViewer
        self.clicked.connect(self.callback)
# class FigLogHiglighter(QSyntaxHighlighter):
#     def __init__(self, parent):
#         self._highlight_lines = dict()

#     def highlight_line(self, line, fmt):
#         if isinstance(line, int) and line >= 0 and isinstance(fmt, QTextCharFormat):
#             self._highlight_lines[line] = fmt
#             tb = self.document().findBlockByLineNumber(line)
#             self.rehighlightBlock(tb)

#     def clear_highlight(self):
#         self._highlight_lines = dict()
#         self.rehighlight()

#     def highlightBlock(self, text):
#         line = self.currentBlock().blockNumber()
#         fmt = self._highlight_lines.get(line)
#         if fmt is not None:
#             self.setFormat(0, len(text), fmt)
# class FigTabWidget(QTabWidget):
#     '''
#     https://forum.qt.io/topic/67542/drag-tabs-between-qtabwidgets/6
#     '''
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.parent = parent
#         self.setAcceptDrops(True)
#         self.tabBar = self.tabBar()
#         self.tabBar.setMouseTracking(True)
#         self.indexTab = None
#         self.setMovable(True)
#         # self.addTab(QWidget(self), 'Tab One')
#         # self.addTab(QWidget(self), 'Tab Two')
#     def mouseMoveEvent(self, e):
#         if e.buttons() != Qt.RightButton:
#             return

#         globalPos = self.mapToGlobal(e.pos())
#         tabBar = self.tabBar
#         posInTab = tabBar.mapFromGlobal(globalPos)
#         self.indexTab = tabBar.tabAt(e.pos())
#         tabRect = tabBar.tabRect(self.indexTab)

#         pixmap = QPixmap(tabRect.size())
#         tabBar.render(pixmap,QPoint(),QRegion(tabRect))
#         mimeData = QMimeData()
#         drag = QDrag(tabBar)
#         drag.setMimeData(mimeData)
#         drag.setPixmap(pixmap)
#         cursor = QCursor(Qt.OpenHandCursor)
#         drag.setHotSpot(e.pos() - posInTab)
#         drag.setDragCursor(cursor.pixmap(),Qt.MoveAction)
#         dropAction = drag.exec_(Qt.MoveAction)

#     def dragEnterEvent(self, e):
#         e.accept()
#         if e.source().parentWidget() != self:
#             return

#         print(self.indexOf(self.widget(self.indexTab)))
#         self.parent.TABINDEX = self.indexOf(self.widget(self.indexTab))


#     def dragLeaveEvent(self,e):
#         e.accept()


#     def dropEvent(self, e):
#         print(self.parent.TABINDEX)
#         if e.source().parentWidget() == self:
#             return

#         e.setDropAction(Qt.MoveAction)
#         e.accept()
#         counter = self.count()

#         if counter == 0:
#             self.addTab(e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabText(self.parent.TABINDEX))
#         else:
#             self.insertTab(counter + 1 ,e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabText(self.parent.TABINDEX))
class FigLogger:
    def __init__(self, path="system.log"):
        self.path = path
        self.widgets = [] # list of widgets that are displaying the log contents.
        self.records = [] # list of log records.
        self.formatted = []
        self.html = []
        open(self.path, "w")
        self.style = {"DEBUG" : "color: #c79f00; font-weight: bold;",
                      "INFO" : "color: #00c76a; font-weight: bold;",
                      "date" : "color: #ff7e1c; font-style: oblique;"}

    def addWidget(self, widget):
        self.widgets.append(widget)

    def _update_widgets(self):
        for widget in self.widgets:
            try:
                widget.setText("<br>".join(self.html))
            except AttributeError:
                pass # if setText is not possible.
            except RuntimeError:
                self.error("deleted window")

    def _write(self):
        with open(self.path, "a") as f:
            f.write(self.formatted[-1]+"\n")

    def _update_records(self, msg, **kwargs):
        now = datetime.datetime.now().strftime("%a %-d-%b-%Y %-I:%M:%S %p")
        record = {"type" : kwargs.get("type", "INFO"),
                  "timestamp" : now,
                  "message" : msg}
        self.records.append(record)
        self.formatted.append(f"{record['type']}::{now} {msg}")
        level = record["type"]
        style = self.style[level]
        spacer = "&nbsp;"*6
        date_style = self.style["date"]
        html_line = f"<span style='{style}'>{level}</span> <b>::</b> <span style='{date_style}'>{now}</span>{spacer}{msg}"
        self.html.append(html_line)
        self._write()
        self._update_widgets()

    def debug(self, msg):
        self._update_records(msg, type="DEBUG")

    def info(self, msg):
        self._update_records(msg, type="INFO")

    def warning(self, msg):
        self._update_records(msg, type="WARNING")

    def error(self, msg):
        self._update_records(msg, type="ERROR")


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.textEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.textEditor.lineNumberAreaPaintEvent(event)


class FigHistoryViewer(QWidget):
    def __init__(self, logger, parent=None):
        import getpass

        super(FigHistoryViewer, self).__init__(parent)
        # main layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # layout.addStretch(True)

        VLayout = QVBoxLayout()
        VLayout.setAlignment(Qt.AlignTop)
        VLayout.setContentsMargins(0, 0, 0, 0)
        VLayout.setSpacing(0)
        VLayout.addStretch(True) # THIS IS VERY IMPORTANT.
        # load records from history log file.
        for record in logger:
            HLayout = QHBoxLayout()
            HLayout.setContentsMargins(5, 10, 10, 10)
            HLayout.setSpacing(0)
            # icon image.
            icon = QPushButton(self)
            icon.setStyleSheet("border: 0px")
            icon_path = record["handler"]
            icon.setIcon(QIcon(icon_path))
            icon.setIconSize(QSize(30,30))
            HLayout.addWidget(icon)            
            # path button.
            path = record["path"]
            path = path.replace(f"/home/{getpass.getuser()}", "~")
            pathBtn = QPushButton(path)
            pathBtn.setStyleSheet('''
                QPushButton {
                    border: 0px; 
                    color: #32a8a6; 
                    font-weight: bold; 
                }
                QPushButton:hover {
                    background: #32a8a6; 
                    font-weight: bold;
                    color: #292929;
                }
            ''')
            HLayout.addWidget(pathBtn)
            # left spacer.
            left_spacer = QWidget()
            left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            HLayout.addWidget(left_spacer)
            # timestamp label.
            timestamp = record["time"]
            timeLbl = QLabel()
            timeLbl.setText(timestamp)
            timeLbl.setStyleSheet('''
                QLabel {
                    color: #fff;
                }
                QLabel:hover {
                    background: #32a8a6; 
                    color: #292929;
                    font-weight: bold;
                }
            ''')
            HLayout.addWidget(timeLbl)
            # create widget for this row.
            rowWidget = QWidget()
            rowWidget.setLayout(HLayout)
            rowWidget.setStyleSheet('''
                QWidget:hover {
                    background: #32a8a6; 
                    color: #292929;
                }
            ''')
            # add row widget to vertical layout.
            VLayout.insertWidget(0, rowWidget) #, Qt.AlignBottom)
        # create history widget.
        historyWidget = QWidget()
        historyWidget.setLayout(VLayout)
        # create scroll area.
        scroll = QScrollArea()
        scroll.setWidget(historyWidget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        title = QLabel("History")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold")
        layout.addWidget(title)
        layout.addWidget(scroll)
        # set layout.
        self.setLayout(layout)


class QTextEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class FigLicenseGenerator(QWidget):
    ''''''
    def __init__(self, parent=None):
        super(FigLicenseGenerator, self).__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(0, 0, 0, 0)
        self.license_templates = json.load(open(__asset__("license_templates.json")))
        # select license type.
        self.dropdown = QComboBox()
        self.dropdown.addItem("Apache License 2.0")
        self.dropdown.addItem("GNU General Public License v3.0")
        self.dropdown.addItem("MIT License")
        self.dropdown.addItem('BSD 2-Clause "Simplified" License')
        self.dropdown.addItem('BSD 3-Clause "New" or "Revised" License')
        self.dropdown.addItem("Boost Software License 1.0")
        self.dropdown.addItem("Creative Commons Zero v1.0 Universal")
        self.dropdown.addItem("Eclipse Public License 2.0")
        self.dropdown.addItem("GNU Affero General Public License v3.0")
        self.dropdown.addItem("GNU General Public License v2.0")
        self.dropdown.addItem("GNU Lesser General Public License v2.1")
        self.dropdown.addItem("Mozilla Public License 2.0")
        self.dropdown.addItem("The Unlicense")
        self.dropdown.currentIndexChanged.connect(self.onSelChange)
        # save the file.
        self.saveBtn = QToolButton(self)
        self.saveBtn.setIcon(FigIcon("save.svg"))
        # open file.
        self.openBtn = QToolButton(self)
        self.openBtn.setIcon(FigIcon("open.svg"))
        # generate license from template.
        self.genBtn = QToolButton(self)
        self.genBtn.setIcon(FigIcon("gen.svg"))
        # version placard.
        self.version = QLabel()
        # datetime placard.
        self.timestamp = QLabel()
        # link for more details.
        self.learnMore = QLabel()
        html = '''<a style="text-decoration: none; color: #42f5e3" href="https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#disclaimer">Learn more about licenses</a>'''
        self.learnMore.setText(html)
        self.learnMore.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.learnMore.linkActivated.connect(lambda: QDesktopServices.openUrl(QUrl("https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository#disclaimer")))
        # add widgets to layout.
        topLayout.addWidget(self.openBtn)
        topLayout.addWidget(self.dropdown)
        topLayout.addWidget(self.version)
        topLayout.addWidget(self.timestamp)
        # topLayout.addWidget(self.genBtn)
        topLayout.addWidget(self.saveBtn)

        # top bar.
        self.topBar = QWidget()
        self.topBar.setLayout(topLayout)
        # edit area
        self.textedit = QTextEditor(self)
        self.textedit.setStyleSheet(f"background: url({__icon__('scratchpad/bg.jpg')}); color: #000")
        self.textedit.setMinimumHeight(500)
        # list of permissions, limitations and conditions
        self.permList = QListWidget()
        self.permList.setFixedHeight(100)
        self.limList = QListWidget()
        self.limList.setFixedHeight(100)
        self.condList = QListWidget()
        self.condList.setFixedHeight(100)

        listLayout = QHBoxLayout()    
        listLayout.addWidget(self.permList) # permissions list
        listLayout.addWidget(self.limList) # limitations list
        listLayout.addWidget(self.condList) # conditions list
        
        # stats widget.
        self.stats = QWidget()
        self.stats.setLayout(listLayout)
        # preare the final layout.
        layout.addWidget(self.topBar)
        layout.addWidget(self.textedit)
        layout.addWidget(self.stats)
        layout.addWidget(self.learnMore)
        self.setLayout(layout)
        self.updateLicense(license_name="Apache License 2.0")
        self.setStyleSheet('''
            color: #fff;
        ''')

    def onSelChange(self, id):
        license_name = self.dropdown.itemText(id)
        self.updateLicense(license_name)

    def updateLicense(self, license_name):
        license_template = self.license_templates[license_name]
        self.textedit.setPlainText(license_template["text"])
        # clear all lists.
        self.permList.clear()
        self.limList.clear()
        self.condList.clear()
        # populate lists.
        # permissions.
        for pt in license_template["permissions"]:
            self.permList.addItem(QListWidgetItem(f"?????? {pt}",  self.permList))
        # limitations.
        for pt in license_template["limitations"]:
            self.limList.addItem(QListWidgetItem(f"??? {pt}",  self.limList))
        # conditions.
        for pt in license_template["conditions"]:
            self.condList.addItem(QListWidgetItem(f"??? {pt}",  self.condList))
        
        version = license_template["version"]
        timestamp = license_template["date"]
        self.version.setText(version)
        self.timestamp.setText(f"???? {timestamp}")


class WebRenderEngine(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(WebRenderEngine, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self._parent = parent
        # self.browserZoomInAction = QAction("Zoom in", self)
        # self.browserZoomInAction.setShortcut(QKeySequence.ZoomIn)
        # self.browserZoomInAction.triggered.connect(self.zoomInEvent)
        # self.browserZoomFactor = 1 
    def dragEnterEvent(self, e):
        from pathlib import Path
        from pprint import pprint
        filename = e.mimeData().text().strip("\n").strip()
        file_format = Path(filename).suffix
        # if file_format == ".pdf":
        #     self.setHtml(pdfRenderContext, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))
        #     print(filename)
        #     if self.enable_zoom: self.attachJSZoomHandler
        #     # self.load_pdf(filename) 
        super(WebRenderEngine, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('QR Code')
        self.menu.popup(event.globalPos())

    def execJS(self, script):
        self.loadFinished.connect(lambda: self.page().runJavaScript(script, self.consoleLog))

    def consoleLog(self, message):
        self.consoleHistory.append(message)
        return message

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class FigBrowser(QWidget):
    def __init__(self, parent=None):
        super(FigBrowser, self).__init__()
        self._parent = parent
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        # navbar = QToolBar("Navigation")
        self.browser = WebRenderEngine(parent)
        layout.addWidget(self.browser)
        # set toolbar sizes.
        if parent:
            parent.browserNavBar.show()
        self.setLayout(layout)
        self._parent = parent

    def url(self):
        return self.browser.url()


class FigWindow(QMainWindow):
    keyPressed = pyqtSignal(int)
    
    def __init__(self, screen=None, background="logo.png", *args, **kwargs):
        self.threads = [] # collect threads.
        os.makedirs("logs", exist_ok=True)
        super(FigWindow, self).__init__(*args, **kwargs)  
        self.setMouseTracking(True) # allow mouse tracking   
        # attach primary screen (from QApplication)
        self.screen = screen
        # set background image path.
        self.background = background
        # initialize file tree.
        self.fileTree = FigTreeFileExplorer()
        # initialize activity panel.
        self.activity = FigActivityPanel(parent=self)

        self.opacLevel = 0.99
        self.ontopFlag = True

        self.ctrlBar = self.initCtrlBar()
        self.bottomBar = self.initBottomBar()
        self.subSysBar = self.subSystemsBar()
        self.debugBar = self.initDebugBar()
        # self.mediaBar = self.initMediaBar()
        # self.systemBar = self.systemBar()
        self.titleBar = self.initTitleBar()
        self.folderBar = self.folderNavBar()
        # currently displayed path (on the folder bar)
        self.folderBar.path = str(pathlib.Path.home())
        self.shortcutBar = self.initShortcutBar()
        # browser navigation bar.
        self.browserNavBar = self.initBrowserNavBar() 
        # package manager launcher
        self.packmanBar = self.initPackmanBar()
        self.packmanBar.setMinimumSize(QSize(300,400))

        self.addToolBar(Qt.TopToolBarArea, self.titleBar)
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(Qt.TopToolBarArea, self.folderBar)
        self.addToolBar(Qt.TopToolBarArea, self.shortcutBar)
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(Qt.TopToolBarArea, self.browserNavBar)
        self.addToolBar(Qt.LeftToolBarArea, self.debugBar)
        # self.addToolBar(Qt.LeftToolBarArea, self.mediaBar)
        # self.addToolBar(Qt.LeftToolBarArea, self.systemBar)
        self.addToolBarBreak(Qt.LeftToolBarArea)
        # self.addToolBar(Qt.LeftToolBarArea, self.packmanBar)
        self.addToolBar(Qt.RightToolBarArea, self.subSysBar)
        # self.addToolBar(Qt.RightToolBarArea, self.subSysBar2)
        self.addToolBar(Qt.BottomToolBarArea, self.ctrlBar)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.bottomBar)
        self.addToolBarBreak(Qt.TopToolBarArea)

        self.tabs = QTabWidget() # tab widget
        # self.tabs.setDocumentMode(True) # making document mode true
        # self.tabs.tabBar().setExpanding(True)
        self.tabs.tabBarDoubleClicked.connect(self.addNewTab)
        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.onCurrentTabChange)
        # making tabs closeable	
        self.tabs.setTabsClosable(True)
        self.tabs.setElideMode(True)
        self.tabs.setMovable(True) 	
        self.tabs.tabCloseRequested.connect(self.onCurrentTabClose) # adding action when tab close is requested
        # self.tabs.setGraphicsEffect(self.blur_effect)
        self.tabs.setStyleSheet('''
        QTabWidget {
            background: rgba(29, 29, 29, 0.95);
            color: #fff;
        }
        QTabWidget::pane {
            border: 0px;
        }
        QTabBar {
            border: 0px;
        }
        QTabBar::close-button {
            color: #fff;
            background: url("/home/atharva/GUI/FigUI/FigUI/assets/icons/close-tab.svg");
            background-repeat: no-repeat;
            background-position: center;
            subcontrol-position: right;
            border-radius: 12px;
        }
        QTabBar::close-button:hover {
            color: #fff;
            background: url("/home/atharva/GUI/FigUI/FigUI/assets/icons/close-tab-hover.svg");
            background-repeat: no-repeat;
            background-position: center;
            background-color: rgba(235, 235, 235, 0.50);
        }
        QTabBar::tab {
            border: 0px;
            background: #292929;
            color: #eee;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 9px;
            padding-right: 5px;
            margin-right: 1px;
            margin-left: 1px;
            border: 0px;
            font-size: 18px;
        }
        QTabBar::tab:hover {
            /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #70121c, stop : 0.6 #b31f2f, stop : 0.8 #de2336); */
            /* background: #ffbb63; */
            background: '''+ Fig.Window.CLHEX +''';
            color: #292929;
        }
        QTabBar::tab:selected {
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #de891b, stop : 0.99 #ffbb63); */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.Window.CDHEX+''', stop : 0.99 '''+Fig.Window.CLHEX+'''); 
            color: #fff;
            padding-top: 2px;
            padding-bottom: 2px;
            padding-left: 9px;
            padding-right: 5px;
        }
        /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929); */
        /* QTabBar::tab {
            background: #292929;
            color: #eee;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 9px;
            padding-right: 5px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            margin-right: 1px;
            margin-left: 1px;
            border: 0px;
            font-size: 18px;
        } */
        /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018); */
        /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #e38c59, stop : 0.99 #ff5e00); */
        ''') # TODO: theme
        self.logger = FigLogger(path=f"logs/{datetime.datetime.now().strftime('%d_%b_%Y_%H_%M_%S')}.log")
        # wrapper widget has the top ribbon and the central widget-terminal splitter.
        self.wrapperWidget = QWidget()
        self.wrapperWidgetLayout = QVBoxLayout()
        self.wrapperWidgetLayout.setContentsMargins(0,0,0,0)
        
        self.wrapperWidgetLayout.setSpacing(0)
        # vertical splitter between the central tab widget and the FigTerminal.
        self.centralTermSplitter = QSplitter(Qt.Vertical)
        self.centralTermSplitter.setStyleSheet('''QSplitter { background: #000 }''')

        # the main menu top ribbon.
        self.mainMenu = self.initMainMenu() 
        self.wrapperWidgetLayout.addWidget(self.mainMenu)
        # the central widget: a horizontal splitter with file tree, tabwidget and activity sidepanel.
        self.centralWidget = QSplitter(Qt.Horizontal)
        self.centralWidget.addWidget(self.fileTree)
        self.centralWidget.addWidget(self.tabs)
        self.centralWidget.addWidget(self.activity)
        self.centralWidget.setStyleSheet("background: #292929")
        self.centralTermSplitter.addWidget(self.centralWidget)
        # the fig terminal (add to the centralTermSplitter)
        self.fig_terminal = self.initFigTerminal()
        self.fig_terminal.hide()
        self.centralTermSplitter.addWidget(self.fig_terminal)
        # add centralTermSplitter to wrapper widget.
        self.wrapperWidgetLayout.addWidget(self.centralTermSplitter)
        # self.wrapperWidgetLayout.addWidget(self.smartPhoneTaskBar)
        self.wrapperWidget.setLayout(self.wrapperWidgetLayout)
        self.ribbon_visible = True
        self.toggleRibbon()
        # self.centralWidget.layout.addWidget(QPushButton("Wow"))
        # self.centralWidget.setLayout(self.centralWidget.layout)
        self.setCentralWidget(self.wrapperWidget) # making tabs as central widget
        self.statusBar = QStatusBar() # creating a status bar
        
        try: from FigUI.handler import FigHandler
        except ImportError: from ..handler import FigHandler
        self.handler = FigHandler(self)
        
        self.fig_history = HistoryLogger()
        try: from Launcher import FigLauncher
        except: from .Launcher import FigLauncher
        self.fig_launcher = FigLauncher(self)
        # self.newTabBtn.clicked.connect(self.addNewTab)
        self.tabs.addTab(self.fig_launcher, FigIcon("launcher.png"), "Launcher")
        transBtn = QToolButton(self.tabs)
        transBtn.setAttribute(Qt.WA_TranslucentBackground)
        transBtn.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, transBtn) 
        # make launcher tab unclosable.
        # self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground, True) # NOTE: need for rounded corners
        # fullscreen on F11.
        self.isfullscreen = False
        self.ctrlBar.hide()
        self.debugBar.hide()
        self.bottomBar.hide()
        self.folderBar.hide()
        self.subSysBar.hide()
        self.shortcutBar.hide()
        self.browserNavBar.hide()
        # self.showFullScreen()
        if PLATFORM == "Linux":
            self.fnF11 = QShortcut(QKeySequence('Fn+F11'), self)
            self.fnF11.activated.connect(self.toggleFullScreen)

        self.smartPhoneTaskBar = self.initSmartPhoneTaskBar(current_widget=self)

    def showFullScreen(self):
        super(FigWindow, self).showFullScreen()
        self.titleBar.hide()
        # self.closeBtn.hide()
        # self.maximizeBtn.hide()
        # self.minimizeBtn.hide()
        self.ctrlBar.show()

    def showNormal(self):
        super(FigWindow, self).showNormal()
        self.titleBar.show()
        # self.closeBtn.show()
        # self.maximizeBtn.show()
        # self.minimizeBtn.show()
        self.ctrlBar.hide()

    def toggleTabBar(self):
        '''toggle visibility of the tab bar.'''
        if self.istabbar_visible:
            self.tabs.tabBar().hide()
        else:
            self.tabs.tabBar().show()
        self.istabbar_visible = not self.istabbar_visible

    def toggleFullScreen(self):
        # print("toggling full screen")
        if self.isfullscreen: 
            self.showNormal()
        else: 
            self.showFullScreen()
        self.isfullscreen = not self.isfullscreen

    def toggleTerminal(self):
        if self.isterm_visible:
            self.fig_terminal.hide()
            self.termBtn.setText("show\nterminal")
        else:
            self.fig_terminal.show()
            self.termBtn.setText("hide\nterminal")
        self.isterm_visible = not(self.isterm_visible)

    def resizeEvent(self, event):
        self.smartPhoneTaskBar.rePos()
        return super(FigWindow, self).resizeEvent(event)

    def toggleTitleBar(self):
        if self.istitle_visible:
            self.titleBar.hide()
        else:
            self.titleBar.show()
        self.istitle_visible = not(self.istitle_visible)

    def toggleRibbon(self):
        if self.ribbon_visible:
            self.mainMenu.setFixedHeight(Fig.Window.MINH)
            self.hideBtn.setIcon(FigIcon("fileviewer/show_ribbon.svg"))
        else:
            self.mainMenu.setFixedHeight(Fig.Window.MAXH)
            self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.ribbon_visible = not(self.ribbon_visible)

    def onKey(self, key):
        if key == Qt.Key_F11:
            if platform.system() == "Windows":
                self.toggleFullScreen()
        # elif key == KeySequence:
    def keyPressEvent(self, event):
        super(FigWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

    def stayOnTop(self):
        '''change flags to make the window stay on top.'''
        if self.ontopFlag:
            self.setWindowFlags(self.windowFlags() | ~Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint )
            # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.ontopFlag = not self.ontopFlag

    def initFigTerminal(self):
        from FigUI.FigTerminal import FigTerminal
        self.figTermRef = FigTerminal()
        self.figTermRef.titleBar.hide()
        # term = QLabel("TERMINAL")
        return self.figTermRef

    def initBrowserNavBar(self):
        '''create the navbar for borwser instances.'''
        navbar = QToolBar("Navigation")
        # move back.
        backBtn = QAction("Back", self)
        backBtn.setToolTip("Go back to the previous page ...")
        backBtn.setIcon(FigIcon("browser/back.svg"))
        # move forward.
        forwardBtn = QAction("Forward", self)
        forwardBtn.setToolTip("Go forward while navigating ...")
        forwardBtn.setIcon(FigIcon("browser/forward.svg"))
        # refresh.
        refreshBtn = QAction("Refresh", self)
        refreshBtn.setToolTip("Refresh webpage")
        refreshBtn.setIcon(FigIcon("browser/refresh.svg"))
        # stop loading.
        stopBtn = QAction("Stop", self)
        stopBtn.setToolTip("Stop loading of the webpage")
        stopBtn.setIcon(FigIcon("browser/stop.svg"))
        # home page.
        homeBtn = QAction("Home", self)
        homeBtn.setToolTip("Got back to home page")
        homeBtn.setIcon(FigIcon("browser/home.svg"))
        # search function.
        searchBtn = QAction("Search", self)
        searchBtn.setToolTip("Search the url entered in the search bar.")
        searchBtn.setIcon(FigIcon("browser/search.svg"))
        # url search bar.
        searchBar = QLineEdit()
        searchBar.setToolTip("Type a url or search query.")
        searchBar.setStyleSheet("background: #fff")
        # extensions.
        extensionsBtn = QAction("Extensions", self)
        extensionsBtn.setToolTip("Extensions.")
        extensionsBtn.setIcon(FigIcon("browser/extensions.svg"))
        # user profile.
        profileBtn = QAction("User", self)
        profileBtn.setToolTip("Change user profile.")
        profileBtn.setIcon(FigIcon("browser/user.svg"))
        # settings.
        settingsBtn = QAction("Settings", self)
        settingsBtn.setToolTip("Modify settings.")
        settingsBtn.setIcon(FigIcon("browser/settings.svg"))
        # navigation bar.
        navbar.addAction(backBtn)
        navbar.addAction(forwardBtn)
        navbar.addAction(refreshBtn)
        navbar.addAction(homeBtn)
        navbar.addSeparator()
        navbar.addWidget(searchBar)
        navbar.addSeparator()
        navbar.addAction(searchBtn)
        navbar.addAction(extensionsBtn)
        navbar.addAction(stopBtn)
        navbar.addAction(profileBtn)
        navbar.addAction(settingsBtn)
        navbar.setStyleSheet("background: #292929")
        navbar.setIconSize(QSize(17,17))

        return navbar

    def initShortcutBar(self):
        home = str(pathlib.Path.home())
        music = os.path.join(home, "Music")
        videos = os.path.join(home, "Videos")
        desktop = os.path.join(home, "Desktop")
        pictures = os.path.join(home, "Pictures")
        documents = os.path.join(home, "Documents")
        downloads = os.path.join(home, "Downloads")
        trash = os.path.join(home, ".local/share/Trash/files")

        sysbar = QToolBar("Shortcuts Bar Visibility")
        sysbar.setIconSize(QSize(22,22))
        sysbar.setStyleSheet("background: #292929; color: #fff; border: 0px")   
        sysbar.setMovable(False)
        # left spacer.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # recents.
        recentBtn = QAction("Recent", self)
        recentBtn.setToolTip("recently modified/opened files.")
        recentBtn.setIcon(FigIcon("sysbar/recent.svg"))
        # home.
        homeBtn = QAction("Home", self)
        homeBtn.setToolTip("open home folder.")
        homeBtn.setIcon(FigIcon("sysbar/home.svg"))
        homeBtn.triggered.connect(lambda : self.addNewFileViewer(path=home))
        # desktop.
        desktopBtn = QAction("Desktop", self)
        desktopBtn.setToolTip("open desktop.")
        desktopBtn.setIcon(FigIcon("sysbar/desktop.svg"))
        desktopBtn.triggered.connect(lambda: self.addNewFileViewer(path=desktop))
        # documents.
        documentBtn = QAction("Documents", self)
        documentBtn.setToolTip("open documents.")
        documentBtn.setIcon(FigIcon("sysbar/documents.svg"))
        documentBtn.triggered.connect(lambda: self.addNewFileViewer(path=documents))
        # downloads.
        downloadsBtn = QAction("Downloads", self)
        downloadsBtn.setToolTip("open downloads.")
        downloadsBtn.setIcon(FigIcon("sysbar/downloads.svg"))
        downloadsBtn.triggered.connect(lambda: self.addNewFileViewer(path=downloads))
        # music.
        musicBtn = QAction("Music", self)
        musicBtn.setToolTip("open music.")
        musicBtn.setIcon(FigIcon("sysbar/music.svg"))
        musicBtn.triggered.connect(lambda: self.addNewFileViewer(path=music))
        # pictures.
        picturesBtn = QAction("Pictures", self)
        picturesBtn.setToolTip("open videos.")
        picturesBtn.setIcon(FigIcon("sysbar/pictures.svg"))
        picturesBtn.triggered.connect(lambda: self.addNewFileViewer(path=pictures))
        # videos.
        videosBtn = QAction("Videos", self)
        videosBtn.setIcon(FigIcon("sysbar/videos.svg"))
        videosBtn.triggered.connect(lambda: self.addNewFileViewer(path=videos))
        # trash.
        trashBtn = QAction("Trash", self)
        trashBtn.setIcon(FigIcon("sidebar/trash.svg"))
        trashBtn.triggered.connect(lambda: self.addNewFileViewer(path=trash))
        # blank.
        blank = QWidget()
        blank.setFixedWidth(20)
        # add actions.
        sysbar.addWidget(left_spacer)
        sysbar.addAction(recentBtn)
        sysbar.addAction(homeBtn)
        sysbar.addAction(desktopBtn)
        sysbar.addAction(documentBtn)
        sysbar.addAction(downloadsBtn)
        sysbar.addAction(musicBtn)
        sysbar.addAction(picturesBtn)
        sysbar.addAction(videosBtn)
        sysbar.addAction(trashBtn)
        sysbar.addWidget(blank)

        return sysbar

    def initDebugBar(self):
        sysbar = QToolBar("Coding ToolBar Visibility")
        sysbar.setIconSize(QSize(30,30))
        sysbar.setStyleSheet('''
            padding: 3px; 
            margin: 0px; 
            background: url('/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png');
            color: #fff; 
            border: 0px
        ''')
        sysbar.setMovable(False)       
        # file explorer.
        fileTreeBtn = QAction("Explorer", self)
        fileTreeBtn.setToolTip("file explorer.")
        fileTreeBtn.setIcon(FigIcon("sysbar/explorer.svg"))
        fileTreeBtn.triggered.connect(self.toggleCtrlB)
        self.ctrlB = QShortcut(QKeySequence("Ctrl+B"), self)
        self.ctrlB.activated.connect(self.toggleCtrlB)
        # activity panel.
        activityBtn = QAction("Activity", self)
        activityBtn.setToolTip("Check activity panel.")
        activityBtn.setIcon(FigIcon("sysbar/activity.svg"))
        activityBtn.triggered.connect(self.activity.toggle)
        # titleToggleBtn = QAction("Show titlebar", self)
        # titleToggleBtn.setToolTip("Toggle titlebar visibility.")
        # titleToggleBtn.setIcon(FigIcon("titlebar.svg"))
        # titleToggleBtn.triggered.connect(self.toggleTitleBar)
        # debugging.
        bugBtn = QAction("Debug", self)
        bugBtn.setToolTip("start debugging.")
        bugBtn.setIcon(FigIcon("sysbar/bug.svg"))
        # lab.
        labBtn = QAction("Lab", self)
        labBtn.setToolTip("Open development lab")
        labBtn.setIcon(FigIcon("sysbar/lab.svg"))
        # github GUI.
        gitHubBtn = QAction("GitHub", self)
        gitHubBtn.setToolTip("Integrate with github")
        gitHubBtn.setIcon(FigIcon("sysbar/github.svg"))
        # run code to test.
        runBtn = QAction("Run Code", self)
        runBtn.setToolTip("Run code for testing.") 
        runBtn.setIcon(FigIcon("sysbar/run.svg"))
        # expander.
        expander = QWidget()
        expander.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # user settings.
        userBtn = QAction("User Settings", self)
        userBtn.setToolTip("Open user/admin system settings.")
        userBtn.setIcon(FigIcon("sysbar/user_settings.svg"))
        # settings.
        settingsBtn = QAction("Settings", self)
        settingsBtn.setToolTip("Open system settings.")
        settingsBtn.setIcon(FigIcon("sysbar/settings.svg"))

        sysbar.addAction(fileTreeBtn)
        sysbar.addAction(activityBtn)
        sysbar.addAction(bugBtn)
        sysbar.addAction(labBtn)
        sysbar.addAction(gitHubBtn)
        sysbar.addAction(runBtn)
        sysbar.addWidget(expander)
        sysbar.addAction(userBtn)
        sysbar.addAction(settingsBtn)

        return sysbar

    def toggleCtrlB(self):
        currentTab = self.tabs.currentWidget()
        try:
            currentTab.togglePreview()
        except AttributeError:
            self.fileTree.toggle()
    # def initMediaBar(self):
    #     sysbar = QToolBar("Media Controls Bar Visibility")
    #     sysbar.setIconSize(QSize(25,25))
    #     sysbar.setStyleSheet('''
    #         padding: 3px; 
    #         margin: 0px; 
    #         background: #292929; 
    #         color: #fff; 
    #         border: 0px
    #     ''')
    #     # decrease volume .
    #     volMinusBtn = QAction("Volume Minus", self)
    #     volMinusBtn.setToolTip("Decrease volume.")
    #     volMinusBtn.setIcon(FigIcon("sysbar/volminus.svg"))
    #     volMinusBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioLowerVolume")) 
    #     # increase volume .
    #     volPlusBtn = QAction("Volume Plus", self)
    #     volPlusBtn.setToolTip("Increase volume.")
    #     volPlusBtn.setIcon(FigIcon("sysbar/volplus.svg")) 
    #     volPlusBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioRaiseVolume"))
    #     # mute.
    #     muteBtn = QAction("Mute", self)
    #     muteBtn.setToolTip("Mute.")
    #     muteBtn.setIcon(FigIcon("sysbar/mute.svg"))
    #     muteBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioMute"))
    #     # play or pause media.
    #     playBtn = QAction("Play/Pause", self)
    #     playBtn.setToolTip("Play or pause media.")
    #     playBtn.setIcon(FigIcon("sysbar/play.svg"))
    #     playBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioPlay"))
    #     # previous media.
    #     prevBtn = QAction("Prev", self)
    #     prevBtn.setToolTip("Previous media.")
    #     prevBtn.setIcon(FigIcon("sysbar/prev.svg"))
    #     prevBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioPrev"))
    #     # next media.
    #     nextBtn = QAction("Next", self)
    #     nextBtn.setToolTip("Next media.")
    #     nextBtn.setIcon(FigIcon("sysbar/next.svg"))
    #     nextBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioNext"))
    #     blank1 = QAction("", self)
    #     blank2 = QAction("", self)
    #     # add actions.
    #     sysbar.addAction(blank1)
    #     sysbar.addAction(volPlusBtn)
    #     sysbar.addAction(volMinusBtn)
    #     sysbar.addAction(muteBtn)
    #     sysbar.addAction(playBtn)
    #     sysbar.addAction(prevBtn)
    #     sysbar.addAction(nextBtn)
    #     sysbar.addAction(blank2)

    #     return sysbar
    # def systemBar(self):
    #     sysbar = QToolBar("System Controls Bar Visibility")
    #     sysbar.setIconSize(QSize(25,25))
    #     sysbar.setStyleSheet('''
    #         padding: 3px; 
    #         margin: 0px; 
    #         background: #292929; 
    #         color: #fff; 
    #         border: 0px
    #     ''')
    #     sysbar.setMovable(False)

    #     return sysbar

    def subSystemsBar(self):
        subbar = QToolBar("App Launcher Bar Visibility")
        '''
        QPushButton {
            border: 0px;
            background: transparent;
            padding-top: 2px;
            padding-bottom: 2px;
        }
        '''
        subbar.setStyleSheet('''
        QToolBar { 
            border: 0px; 
            color: #fff;
            background: rgba(0, 77, 57, 0.90);
            /* background: rgba(37, 21, 47, 0.80); */
            /* background: rgba(33, 10, 18, 0.80); */
        } 
        QPushButton {
            /* background: qradialgradient(cx: 1, cy: 1, radius: 1, stop : 0 #7a4416, stop: 0.8 #fa8e34); */ /* #fa8e34 */
            /* background: qradialgradient(cx: 1, cy: 1, radius: 1, stop : 0 #404040, stop: 0.8 #b8b8b8); */
            font-family: Helvetica;
            padding-left: 3px;
            padding-right: 3px;
            padding-top: 5px;
            padding-bottom: 5px;
            margin-top: 1px;
            margin-bottom: 1px;
            margin-left: 2px;
            margin-right: 2px;
            border-radius: 14px; 
        }
        QPushButton:hover {
            /* background: #b31f2f; */
            background: rgba(185, 255, 236, 0.5);
        }
        QToolBar::separator {
            background: #734494;
        }
        ''')
        # subbar.setAttribute(Qt.WA_TranslucentBackground)
        sysbar = QToolBar("System Management Bar Visibility")
        # sysbar.setIconSize(QSize(25,25))
        sysbar.setStyleSheet('''
        QToolBar { 
            border: 0px; 
            color: #fff; 
            background: rgba(0, 77, 57, 0.90);
            /* background: url('/home/atharva/GUI/FigUI/FigUI/assets/icons/glass_texture.jpg') 0 0 0 0;
            background-repeat: y;
            background-position: center; */
        }
        QPushButton {
            /* background: qradialgradient(cx: 1, cy: 1, radius: 1, stop : 0 #7a4416, stop: 0.8 #fa8e34); */ /* #fa8e34 */
            /* background: qradialgradient(cx: 1, cy: 1, radius: 1, stop : 0 #404040, stop: 0.8 #b8b8b8); */
            font-family: Helvetica;
            padding-left: 3px;
            padding-right: 3px;
            padding-top: 5px;
            padding-bottom: 5px;
            margin-top: 1px;
            margin-bottom: 1px;
            margin-left: 2px;
            margin-right: 2px;
            border-radius: 14px; 
        }
        QPushButton:hover {
            background: rgba(185, 255, 236, 0.5);
        }
        /* background: #b31f2f; */
        /* QPushButton {
            background: transparent;
            border: 0px;
            padding-top: 2px;
            padding-bottom: 2px;
        }
        QPushButton::hover { 
            background: #734494;
        } */
        ''')
        sysbar.setMovable(False)
        # sysbar.setAttribute(Qt.WA_TranslucentBackground)
        # open email client.
        size = QSize(20,20) 
        btnSize = QSize(20,20)
        # open p2p chat server.
        chatBtn = QPushButton()#("Chat", self)
        chatBtn.setToolTip("Open chat server")
        chatBtn.setIcon(FigIcon("sidebar/chat.svg"))
        chatBtn.setIconSize(btnSize)
        # open assitant.
        asstBtn = QPushButton()#("Assistant", self)
        asstBtn.setToolTip("Open assitant")
        asstBtn.setIcon(FigIcon("sidebar/assistant.svg"))
        asstBtn.setIconSize(btnSize)
        asstBtn.clicked.connect(self.addNewBotTab)
        # open math package.
        mathBtn = QPushButton()#("Math", self)
        mathBtn.setToolTip("Open scientific calculator.")
        mathBtn.setIcon(FigIcon("sidebar/calculator.svg"))
        mathBtn.clicked.connect(openCalculator)
        mathBtn.setIconSize(btnSize)
        # open newsfeed.
        newsBtn = QPushButton()#("Newsfeed", self)
        newsBtn.setToolTip("Open news feed")
        newsBtn.setIcon(FigIcon("sidebar/news.svg"))
        newsBtn.setIconSize(btnSize)
        # whiteboard.
        wbBtn = QPushButton()#("Whiteboard", self)
        wbBtn.setToolTip("Open whiteboard")
        wbBtn.setIcon(FigIcon("sidebar/whiteboard.svg"))
        wbBtn.setIconSize(btnSize)
        # illustrator
        illuBtn = QPushButton()#("Illustrator", self)
        illuBtn.setToolTip("Open illustrator")
        illuBtn.setIcon(FigIcon("sidebar/illustrator.svg"))
        illuBtn.setIconSize(btnSize)
        # kanban board.
        kanbanBtn = QPushButton()#("Kanban Board", self)
        kanbanBtn.setToolTip("Open kanban board")
        kanbanBtn.setIcon(FigIcon("sidebar/kanban.svg"))
        kanbanBtn.setIconSize(btnSize)
        # open date and time.
        calBtn = QPushButton()#("Calendar", self)
        calBtn.setToolTip("Open date/time widget")
        calBtn.setIcon(FigIcon("sidebar/calendar.svg"))
        calBtn.setIconSize(btnSize)
        # open clock
        clockBtn = QPushButton()#("Clock", self)
        clockBtn.setToolTip("Open clock")
        clockBtn.setIcon(FigIcon("sidebar/clock.svg"))
        clockBtn.setIconSize(btnSize)
        clockBtn.clicked.connect(self.addNewClock)
        # open weather
        weatherBtn = QPushButton()#("Weather", self)
        weatherBtn.setToolTip("Open weather forecast")
        weatherBtn.setIcon(FigIcon("sidebar/weather.svg"))
        weatherBtn.setIconSize(btnSize)
        self.weatherBtn = weatherBtn
        
        b1 = QPushButton()#("Weather", self)
        b1.setToolTip("Open weather forecast")
        b1.setIcon(FigIcon("sidebar/lolxd.png"))
        b1.setStyleSheet('''background: transparent''')
        b1.setIconSize(btnSize)
        
        b2 = QPushButton()#("Weather", self)
        b2.setToolTip("Open weather forecast")
        b2.setIcon(FigIcon("sidebar/lolxd.png"))
        b2.setStyleSheet('''background: transparent''')
        b2.setIconSize(btnSize)
        
        b3 = QPushButton()#("Weather", self)
        b3.setToolTip("Open weather forecast")
        b3.setIcon(FigIcon("sidebar/lolxd.png"))
        b3.setStyleSheet('''background: transparent''')
        b3.setIconSize(btnSize)
        
        b4 = QPushButton()#("Weather", self)
        b4.setToolTip("Open weather forecast")
        b4.setIcon(FigIcon("sidebar/lolxd.png"))
        b4.setStyleSheet('''background: transparent''')
        b4.setIconSize(btnSize)

        # add actions.
        subbar.addWidget(chatBtn)
        subbar.addWidget(asstBtn)
        # subbar.addWidget(b2)
        subbar.addWidget(mathBtn)
        subbar.addWidget(calBtn)
        subbar.addWidget(clockBtn)
        subbar.addWidget(weatherBtn)
        subbar.addWidget(newsBtn)
        # subbar.addWidget(b3)
        subbar.addWidget(wbBtn)
        subbar.addWidget(illuBtn)
        subbar.addWidget(kanbanBtn)
        subbar.addWidget(b4)
        # subbar.addSeparator()
        # subbar.addWidget(QHLine())
        # subbar.addSeparator()
        top_spacer = QWidget()
        top_spacer.setAttribute(Qt.WA_TranslucentBackground)
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # sysbar.addWidget(top_spacer)

        return subbar

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
    def colorPickerDialog(self):
        colorPicker = ColorPicker(useAlpha=True)
        picked_color = colorPicker.getColor((0,0,0,50))
        print(picked_color)

    def log(self, icon, path):
        handler = __icon__(icon)
        self.fig_history.log(handler, path)
    # def save_screenshot(self, widget: QWidget):
    #     pixmap = self.screen.grabWindow(widget.winId())
    #     path = f"/tmp/FigUI.widgets.FigWindow.tabs.{widget.winId()}.png"
    #     worker = FigWorker()
    #     thread = QThread()
    #     worker.moveToThread(thread)
    #     thread.started.connect(lambda: worker.sleep_n_run(pixmap, "save", path, "png"))
    #     worker.finished.connect(thread.quit)
    #     worker.finished.connect(worker.deleteLater)
    #     thread.finished.connect(thread.deleteLater)
    #     thread.start()
    #     self.threads.append(thread)
    def addNewTerm(self, path=None):
        '''Add new terminal widget'''
        try: from FigUI.subSystem.Shell import FigShell
        except ImportError: from ..subSystem.Shell import FigShell
        if path: terminal = FigShell(parent=self, cmd=f"cd '{path}'; bash")
        else: terminal = FigShell(parent=self)
        # self.terminals = []
        # main_window = QMainWindow()
        # main_window.setCentralWidget(terminal)
        # main_window.show()
        # self.terminals.append(main_window)
        # window = QWindow.fromWinId(main_window.winId())
        # shell = QWidget.createWindowContainer(window)
        i = self.tabs.addTab(terminal, FigIcon("launcher/bash.png"), "Terminal")
        self.tabs.setCurrentIndex(i)
        self.tabs.tabBar().setExpanding(True)
        # self.tabs.setTabWhatsThis(i, "xterm (embedded)")
        self.tabs.setTabToolTip(i, "xterm (embedded)")
        self.log("launcher/bash.png", "Terminal")
        # self.save_screenshot(terminal)
    def addNewClock(self):
        '''Add new clock window'''
        try: from FigUI.subSystem.Clock import FigClock
        except ImportError: from ..subSystem.Clock import FigClock
        clockApp = FigClock()
        i = self.tabs.addTab(clockApp, FigIcon("sidebar/clock.png"), "Clock")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabToolTip(i, "clock app")

        self.log("sidebar/clock.png", "Clock")
        # self.save_screenshot(clockApp)
    def addNewTaskView(self):
        '''Add new task view window'''
        taskView = FigTaskWebView(parent=self, screen=self.screen)
        i = self.tabs.addTab(taskView, FigIcon("ctrlbar/task-view.svg"), "Tasks")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabToolTip(i, "manage tasks/tabs")
        self.log("ctrlbar/task-view.svg", "Task Viewer")
        # self.save_screenshot(taskView)
    def addNewBotTab(self):
        '''Add new chat bot tab'''
        try: from FigUI.subSystem.ChatBot import FigChatBot
        except ImportError: from ..subSystem.ChatBot import FigChatBot
        chatBotApp = FigChatBot()
        i = self.tabs.addTab(chatBotApp, FigIcon("sidebar/assistant.png"), "Clock")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabToolTip(i, "assistant app")
        self.log("sidebar/assistant.png", "Assistant")
        # self.save_screenshot(chatBotApp)
    def addNewKanBanBoard(self):
        '''Add a new kanban board'''
        pass

    def addNewBashrcViewer(self):
        '''Add new bashrc customizer.'''
        home = pathlib.Path.home()
        bashrc = os.path.join(home, ".bashrc")
        handlerWidget = self.handler.getUI(path=bashrc)
        i = self.tabs.addTab(handlerWidget, FigIcon("launcher/bashrc.png"), ".bashrc")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/bashrc.png", bashrc)
        # self.save_screenshot(handlerWidget)
    def addNewLicenseGenerator(self):
        '''Add new license template generator.'''
        licenseViewer = FigLicenseGenerator()
        i = self.tabs.addTab(licenseViewer, FigIcon("launcher/license.png"), "LICENSE")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/license.png", "LICENSE Generator")
        # self.save_screenshot(licenseViewer)
    def addNewHistoryViewer(self):
        '''Add new tab for viewing history.'''
        historyViewer = FigHistoryViewer(self.fig_history)
        i = self.tabs.addTab(historyViewer, FigIcon("launcher/history.png"), f"{self.fig_history.title}'s history")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/history.png", self.fig_history.path)
        # self.save_screenshot(historyViewer)
    def addNewTextEditor(self):
        '''Add new bashrc customizer.'''
        handlerWidget = self.handler.getUI("Untitled.txt")
        i = self.tabs.addTab(handlerWidget, FigIcon("launcher/txt.png"), "Untitled")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/txt.png", "Untitled")
        # self.save_screenshot(handlerWidget)
    def addNewHandlerTab(self):
        handlerWidget = self.handler.handle()
        i = self.tabs.addTab(handlerWidget, "New Tab")
        self.tabs.setCurrentIndex(i)

    def addNewFileViewer(self, path):
        if path:
            fileViewer = FigFileViewer(path=path, parent=self)
        else:
            fileViewer = FigFileViewer(parent=self)
            path = str(pathlib.Path.home())
        parent = ".../" + pathlib.Path(path).parent.name
        name = pathlib.Path(path).name
        i = self.tabs.addTab(fileViewer, FigIcon("launcher/fileviewer.png"), f"{name} {parent}")# f"\t{str(pathlib.Path.home())}")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/fileviewer.png", path)
        # self.save_screenshot(fileViewer)

    def addNewMailClient(self):
        try: from FigUI.subSystem.Email import FigEmailClient
        except ImportError: from ..subSystem.Email import FigEmailClient
        mailClient = FigEmailClient(self)
        i = self.tabs.addTab(mailClient, FigIcon("sidebar/email.png"), f"{mailClient.imap_url}")
        self.tabs.setCurrentIndex(i)

    def addNewTab(self, qurl=None, label="Blank"):
        '''method for adding new tab'''
        qurl = QUrl('http://www.google.com') # show bossweb homepage
        browser = FigBrowser(self) # creating a WebRenderEngine object
        dev_view = QWebEngineView()
        browser.browser.page().setDevToolsPage(dev_view.page())		
        browser.browser.setUrl(qurl) 
        # browser.execJS("document.location.href='https://developer.mozilla.org/en-US/docs/Web/API/document.location';") # setting url to browser
		# setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        self.logger.info(f"browser opened into a window with id: {int(self.winId())}")
		# adding action to the browser when url is changed, update the url
        # browser.urlChanged.connect(lambda qurl, browser = browser: self.update_urlbar(qurl, browser))
        # adding action to the browser when loading is finished and set the tab title
        browser.browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.setupTab(i, browser.browser))

    def setupTab(self, i, browser):
        self.tabs.setTabText(i, ""+browser.page().title())
        self.tabs.setTabIcon(i, FigIcon("launcher/browser.png"))
        self.log("launcher/browser.png", QUrl('http://www.google.com'))

    def tab_open_doubleclick(self, i):
        # checking index i.e and No tab under the click
        if i == -1: self.addNewTab() # creating a new tab
    
    def onCurrentTabChange(self, i):
        '''when tab is changed.'''
        currentWidget = self.tabs.currentWidget()
        # print(type(currentWidget))
        # REMOVE
        # if isinstance(currentWidget, FigFileViewer):
        #     self.folderBar.show()
        #     self.shortcutBar.show()
        # else:
        #     self.folderBar.hide()
        #     self.shortcutBar.hide()
        
        if isinstance(currentWidget, (CodeEditor)):
            self.bottomBar.show()
            self.debugBar.show()
        else:
            self.bottomBar.hide()
            self.debugBar.hide()
        
        try:
            qurl = self.tabs.currentWidget().url() # get the curl
		    # self.update_urlbar(qurl, self.tabs.currentWidget()) # update the url 
            self.browserNavBar.show()
            self.tabs.setTabText(i, qurl.toString())
        except AttributeError:
            self.browserNavBar.hide()
        
        self.langBtn.setIcon(self.tabs.tabIcon(i))
        filename = pathlib.Path(self.tabs.tabText(i).split("...")[0].strip()
        ).__str__().strip()
        try: self.smartPhoneTaskBar.history.append(i)
        except AttributeError: pass
        self.langBtn.setIconSize(QSize(16,16))
        #  print("\x1b[34;1m"+filename+"\x1b[0m")
        
        MimeType, _ = mimetypes.guess_type(filename)
        if MimeType:
            self.indentBtn.setText("Spaces: 4")
            self.langBtn.setText("\t"+MimeType)
            self.encBtn.setText("UTF-8")
            self.eosBtn.setText("LF")
            self.rwBtn.setText("[RW]")
        else:
            self.cursorBtn.setText("")
            self.indentBtn.setText("")
            self.langBtn.setText("")
            self.encBtn.setText("")
            self.eosBtn.setText("")
            self.rwBtn.setText("")

    def onCurrentTabClose(self, i):
        '''when tab is closed'''
		# if there is only one tab
        if self.tabs.count() < 2:
            return # do nothing
        self.tabs.removeTab(i) # else remove the tab
    # def update_title(self, browser):
    #     '''method for update_title'''
    #     # if signal is not from the current tab
    #     if browser != self.tabs.currentWidget(): return # do nothing
    #     title = self.tabs.currentWidget().page().title() # get the page title
    #     self.setWindowTitle(title) # set the window title
    def navigate_to_url(self):
        '''method for navigating to the url.'''
        # get the line edit text and convert it to QUrl object
        q = QUrl(self.urlbar.text())
        if q.scheme() == "": # if scheme is blank
            q.setScheme("http") # set the scheme to
        self.tabs.currentWidget().setUrl(q) # set the url

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def initTitleBar(self):
        toolbar = QToolBar("Title Bar Visibility")
        toolbar.setStyleSheet('''
        QToolBar {
            margin: 0px; 
            border: 0px; 
            color: #fff;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            background: url('/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png');
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929); */
        }''')
        toolbar.setIconSize(QSize(20,20))
        toolbar.setMovable(False)
        ctrlBtnStyle = '''
            QToolButton {
                font-family: Helvetica;
                padding-left: 0px;
                padding-right: 0px;
                padding-top: 0px;
                padding-bottom: 0px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-left: 1px;
                margin-right: 1px;
                border-radius: 11px; 
            }
            QToolButton:hover {
                background: rgba(235, 235, 235, 0.5);
            }         
        '''

        closeBtn = QToolButton(self)
        closeBtn.setToolTip("close window")
        closeBtn.setIcon(FigIcon("close.svg")) 
        closeBtn.setStyleSheet(ctrlBtnStyle)
        closeBtn.clicked.connect(lambda: self.close()) # closing logic.
        self.closeBtn = closeBtn

        minimizeBtn = QToolButton(self)
        minimizeBtn.setToolTip("minimize window")
        minimizeBtn.setIcon(FigIcon("minimize.svg"))
        minimizeBtn.clicked.connect(lambda: self.showMinimized())
        minimizeBtn.setStyleSheet(ctrlBtnStyle)
        self.minimizeBtn = minimizeBtn

        maximizeBtn = QToolButton(self)
        maximizeBtn.setToolTip("maximize window")
        maximizeBtn.setIcon(FigIcon("maximize.svg"))
        maximizeBtn.clicked.connect(lambda: self.maximize())
        maximizeBtn.setStyleSheet(ctrlBtnStyle)
        self.maximizeBtn = maximizeBtn

        titleBtnStyle = '''
            QToolButton {
                font-family: Helvetica;
                padding-left: 4px;
                padding-right: 4px;
                padding-top: 4px;
                padding-bottom: 4px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-left: 2px;
                margin-right: 2px;
                border-radius: 16px; 
            }
            QToolButton:hover {
                background: rgba(255, 223, 97, 0.5);
            }        
        '''

        windowTitle = QLabel()
        windowTitle.setText("") # ("???????????? ???????? ???? ????????????") #("????ig ????s a ????UI")
        windowTitle.setStyleSheet("color: #fff; font-size: 16px")
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # blank spacer.
        blankL = QWidget()
        blankL.setFixedWidth(5)
        blankR = QWidget()
        blankR.setFixedWidth(5)

        toolbar.addWidget(blankL)
        toolbar.addWidget(closeBtn)
        toolbar.addWidget(minimizeBtn)
        toolbar.addWidget(maximizeBtn)
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(windowTitle)
        toolbar.addWidget(right_spacer)
        toolbar.addWidget(blankR)
        toolbar.setMaximumHeight(28)

        return toolbar

    def incOpac(self):
        self.opacLevel += 0.01 
        self.opacLevel = min(self.opacLevel, 1)
        self.tabs.setWindowOpacity(self.opacLevel)

    def decOpac(self):
        self.opacLevel -= 0.01 
        self.opacLevel = max(self.opacLevel, 0.9)
        self.tabs.setWindowOpacity(self.opacLevel)

    def updateFolderBar(self, path, viewer=None):
        folderBtnStyle = '''
        QPushButton:hover{
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6e);
        }

        QPushButton {
                border: 1px solid;
                border-radius: 2px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
                margin-left: 2px;
                margin-right: 4px;
                padding-top: 4px;
                padding-bottom: 4px;
                padding-left: 5px;
                padding-right: 5px;
                font-size: 16px;
        }
        '''
        selFolderBtnStyle = '''
        QPushButton:hover{
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6e);
        }

        QPushButton {
                border: 1px solid;
                border-radius: 2px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
                margin-left: 2px;
                margin-right: 2px;
                padding-top: 4px;
                padding-bottom: 4px;
                padding-left: 5px;
                padding-right: 5px;
                font-weight: bold; 
                color: #ff9100;
                font-size: 16px;
        }
        '''
        if self.folderBar.path.startswith(str(path)): 
            # selectedBtn = self.sender()
            # print(selectedBtn)
            # selectedBtn.setStyleSheet(selFolderBtnStyle)
            return

        for action in self.folderBarActions:
            self.folderBar.removeAction(action)
        self.folderBarActions = []
        path = str(path)
        
        folders = path.split('/')
        till_now = "/" # running variable for subpath till now.
        for i,folder in enumerate(folders):
            if folder != "":
                till_now = os.path.join(till_now, folder)
                btn = QFolderNavBtn(folder, till_now)
                # event handler for click will be attached to open the subpath till now.
                if viewer:
                    btn.connectLauncher(viewer)
                # color the active button differently
                if i == len(folders)-1:
                    btn.setStyleSheet(selFolderBtnStyle)
                else:
                    btn.setStyleSheet(folderBtnStyle)
                action = self.folderBar.addWidget(btn)
                self.folderBarActions.append(action)
        self.folderBar.path = str(path)

    def folderNavBar(self):
        backBtnStyle = '''
        QPushButton:hover{
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6d);
        }

        QPushButton {
            border: 1px solid;
            border-radius: 2px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #6e6e6d, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
            margin-left: 1px;
            margin-right: 1px;
            padding-top: 2px;
            padding-bottom: 2px;
        }
        '''
        nextBtnStyle = '''
        QPushButton:hover{
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #6e6e6d, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
        }

        QPushButton {
            border: 1px solid;
            border-radius: 2px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6d);
            margin-left: 1px;
            margin-right: 1px;
            padding-top: 2px;
            padding-bottom: 2px;
        }
        '''
        # folderBtnStyle = '''
        # QPushButton:hover{
        #         background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
        # }

        # QPushButton {
        #         border: 1px solid;
        #         border-radius: 2px;
        #         background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6e);
        #         margin-left: 2px;
        #         margin-right: 2px;
        #         padding: 5px;
        # }
        # '''
        # selFolderBtnStyle = '''
        # QPushButton:hover{
        #         background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
        # }

        # QPushButton {
        #         border: 1px solid;
        #         border-radius: 2px;
        #         background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6e);
        #         margin-left: 2px;
        #         margin-right: 2px;
        #         padding: 5px;
        #         font-weight: bold; 
        #         color: #ff9100;
        # }
        # '''
        toolbar = QToolBar("Folder Navigation Bar Visibility")
        toolbar.setStyleSheet("border: 0px")
        toolbar.setStyleSheet("color: #fff; background: #292929; border: 0px; padding: 2px;")
        toolbar.setIconSize(QSize(22,22))
        toolbar.setMovable(False)

        backBtn = QPushButton()
        backBtn.setToolTip("go back in folders")
        backBtn.setStyleSheet(backBtnStyle)
        backBtn.setIcon(FigIcon("back.svg"))
        self.backNavBtn = backBtn

        nextBtn = QPushButton()
        nextBtn.setToolTip("go forward in folders")
        nextBtn.setStyleSheet(nextBtnStyle)
        nextBtn.setIcon(FigIcon("forward.svg"))
        self.nextNavBtn = nextBtn

        toolbar.addWidget(backBtn)
        toolbar.addWidget(nextBtn)
        toolbar.addSeparator()

        self.folderBarActions = []
        # folders = os.getcwd().split("/")
        # for i,folder in enumerate(folders):
        #     if folder != "":
        #         btn = QPushButton(folder)        
        #         if i == len(folders)-1:
        #             btn.setStyleSheet(selFolderBtnStyle)
        #         else:
        #             btn.setStyleSheet(folderBtnStyle)
                
        #         action = toolbar.addWidget(btn)
        #         self.folderBarActions.append(action)
        return toolbar

    def showRibbon(self):
        self.mainMenu.setFixedHeight(Fig.Window.MAXH)
        self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.ribbon_visible = True

    def showDashboard(self):
        pass

    def initRemoteMenu(self):
        return QWidget()

    def initMainMenu(self):
        '''create main menu for file browser.'''
        tb = "\t"*4
        mainMenu = QTabWidget()
        self.appMenu = self.initAppMenu()
        mainMenu.addTab(self.appMenu, FigIcon("topbar/apps.svg"), "")
        self.mediaMenu = self.initMediaMenu()
        mainMenu.addTab(self.mediaMenu, FigIcon("topbar/media.svg"), "")
        self.viewMenu = self.initViewMenu()
        mainMenu.addTab(self.viewMenu, FigIcon("topbar/view.svg"), "")
        self.sysMenu = self.initSysMenu()
        mainMenu.addTab(self.sysMenu, FigIcon("topbar/system.svg"), "")
        self.actMenu = self.initActMenu()
        mainMenu.addTab(self.actMenu, tb+"Activity"+tb) # site blockers, history, remind to take a break, productivity etc.
        self.remoteMenu = self.initRemoteMenu()
        mainMenu.addTab(self.actMenu, FigIcon("topbar/remote.svg"), "")
        # hide the ribbon.
        toolBtnStyle = '''
        QToolButton {
            border: 0px;
            background: transparent;
        }
        QToolTip {
            color: #fff;
            background: #292929;
        }'''
        self.hideBtn = QToolButton(mainMenu)
        self.hideBtn.clicked.connect(self.toggleRibbon)
        self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.hideBtn.setIconSize(QSize(23,23))
        self.hideBtn.setStyleSheet(toolBtnStyle)
        # toggle file browser.
        self.fileBtn = QToolButton(mainMenu)
        self.fileBtn.setToolTip("Open file browser.")
        self.fileBtn.setIcon(FigIcon("topbar/file_browser.svg"))
        self.fileBtn.setIconSize(QSize(23,23))
        self.fileBtn.clicked.connect(self.fileTree.toggle)
        self.fileBtn.setStyleSheet(toolBtnStyle)
        # toggle activity panel.
        self.actBtn = QToolButton(mainMenu)
        self.actBtn.setToolTip("Check activity panel.")
        self.actBtn.setIcon(FigIcon("sysbar/activity.svg"))
        self.actBtn.setIconSize(QSize(23,23))
        self.actBtn.clicked.connect(self.activity.toggle)
        self.actBtn.setStyleSheet(toolBtnStyle)
        # toggle title bar visibility.
        self.titleToggleBtn = QToolButton(mainMenu)
        self.titleToggleBtn.setToolTip("Check activity panel.")
        self.titleToggleBtn.setIcon(FigIcon("topbar/titlebar.svg"))
        self.titleToggleBtn.setIconSize(QSize(23,23))
        self.titleToggleBtn.clicked.connect(self.toggleTitleBar)
        self.titleToggleBtn.setStyleSheet(toolBtnStyle)
        # toggle tab bar visibility.
        self.tabToggleBtn = QToolButton(mainMenu)
        self.tabToggleBtn.setToolTip("Toggle tabbar visibility.")
        self.tabToggleBtn.setIcon(FigIcon("topbar/tabbar.svg"))
        self.tabToggleBtn.setIconSize(QSize(23,23))
        self.tabToggleBtn.clicked.connect(self.toggleTabBar)
        self.tabToggleBtn.setStyleSheet(toolBtnStyle)
        # show dashboard`.
        self.dashBtn = QToolButton(mainMenu)
        self.dashBtn.setToolTip("Toggle tabbar visibility.")
        self.dashBtn.setIcon(FigIcon("topbar/dashboard.svg"))
        self.dashBtn.setIconSize(QSize(23,23))
        self.dashBtn.clicked.connect(self.showDashboard)
        self.dashBtn.setStyleSheet(toolBtnStyle)
        # enable fullscreen.
        self.fullScreenBtn = QToolButton(mainMenu)
        self.fullScreenBtn.setIcon(FigIcon("topbar/fullscreen.svg"))
        self.fullScreenBtn.setIconSize(QSize(23,23))
        self.fullScreenBtn.setToolTip("Enable full screen mode")
        self.fullScreenBtn.clicked.connect(self.showFullScreen)
        self.fullScreenBtn.setStyleSheet(toolBtnStyle)
        # exit fullscreen.
        self.exitFullScreenBtn = QToolButton(mainMenu)
        self.exitFullScreenBtn.setIcon(FigIcon("topbar/exit_fullscreen.svg"))
        self.exitFullScreenBtn.setIconSize(QSize(23,23))
        self.exitFullScreenBtn.setToolTip("Disable full screen mode")
        self.exitFullScreenBtn.clicked.connect(self.showNormal)
        self.exitFullScreenBtn.setStyleSheet(toolBtnStyle)
        # always stay on top.
        self.onTopBtn = QToolButton(mainMenu)
        self.onTopBtn.setIcon(FigIcon("topbar/ontop.svg"))
        self.onTopBtn.setIconSize(QSize(23,23))
        self.onTopBtn.setToolTip("Disable full screen mode")
        self.onTopBtn.clicked.connect(self.stayOnTop)
        self.onTopBtn.setStyleSheet(toolBtnStyle)

        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.tabBar().setTabButton(5, QTabBar.RightSide, self.hideBtn)
        mainMenu.tabBar().setTabButton(6, QTabBar.RightSide, self.fileBtn)
        mainMenu.tabBar().setTabButton(7, QTabBar.RightSide, self.actBtn)
        mainMenu.tabBar().setTabButton(8, QTabBar.RightSide, self.titleToggleBtn)
        mainMenu.tabBar().setTabButton(9, QTabBar.RightSide, self.tabToggleBtn)
        mainMenu.tabBar().setTabButton(10, QTabBar.RightSide, self.dashBtn)
        mainMenu.tabBar().setTabButton(11, QTabBar.RightSide, self.fullScreenBtn)
        mainMenu.tabBar().setTabButton(12, QTabBar.RightSide, self.exitFullScreenBtn)
        mainMenu.tabBar().setTabButton(13, QTabBar.RightSide, self.onTopBtn)

        mainMenu.setCurrentIndex(0)
        mainMenu.setStyleSheet('''
        QTabWidget {
            background:'''+Fig.Window.BG+'''
            color: #000;
            border: 0px;
        }
        QTabWidget::pane {
            background:'''+Fig.Window.BG+'''
            border: 0px;
        }
        QTabBar {
            background:'''+Fig.Window.BG+'''
            border: 0px;
        }
        QWidget {
            background:'''+Fig.Window.BG+'''
        }
        QTabBar::tab {
            color: #fff;
            border: 0px;
            margin: 0px;
            padding: 0px;
            font-size: 16px;
            background: #292929;
        }
        QTabBar::tab:hover {
            /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #70121c, stop : 0.6 #b31f2f, stop : 0.8 #de2336); */
            /* background: #ffbb63; */
            background: '''+ Fig.Window.CLHEX +''';
            color: #292929;
        }
        /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #de891b, stop : 0.99 #ffbb63); */
        /* QTabBar::tab:selected {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.Window.CDHEX+''', stop : 0.99 '''+Fig.Window.CLHEX+'''); 
            color: #fff;
        } */
        QToolTip { 
            color: #fff;
            border: 0px;
        }
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding-left: 5px;
            padding-right: 5px;
            background: transparent;
            color: #fff;
        }
        QToolButton:hover {
            border: 0px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.Window.CDHEX+''', stop : 0.99 '''+Fig.Window.CLHEX+'''); 
        }
        QLabel { 
            color: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 '''+Fig.Window.CDHEX+''', stop : 0.99 '''+Fig.Window.CLHEX+''');
            font-size: 14px;
        }''')
        mainMenu.currentChanged.connect(self.showRibbon)
        glowEffect = QGraphicsDropShadowEffect()
        glowEffect.setBlurRadius(50)
        glowEffect.setOffset(30,0)
        glowEffect.setColor(QColor(*Fig.Window.CDRGB))
        mainMenu.setGraphicsEffect(glowEffect)
        mainMenu.setMaximumHeight(Fig.Window.MAXH)

        wrapperWidget = QWidget()
        wrapperLayout = QVBoxLayout()
        wrapperWidget.setStyleSheet('''
        QWidget {
            background: #292929;
        }
        ''')
        wrapperLayout.setSpacing(0)
        wrapperLayout.setContentsMargins(0, 0, 0, 0)
        wrapperLayout.addWidget(mainMenu)
        wrapperWidget.setLayout(wrapperLayout)

        return wrapperWidget

    def initActMenu(self):
        actMenu = QWidget()
        actLayout = QHBoxLayout()
        actLayout.setSpacing(0)
        actLayout.setContentsMargins(0, 0, 0, 0)
        actMenu.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding: 5px;
            border-radius: 15px;
            background: transparent;
            color: #fff;
        }
        QToolTip {
            background: #292929;
            color: #fff;
        }
        QToolButton:hover {
            background: rgba(255, 223, 97, 0.5);
        } 
        ''')
        # open assistant.
        botBtn = QToolButton(actMenu)
        botBtn.setToolTip("Open assistant.")
        botBtn.setIcon(FigIcon("sidebar/assistant.svg"))
        botBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        botBtn.setText("assistant\n")
        # botBtn.clicked.connect(self.decOpac) 
        actLayout.addWidget(botBtn)
        actLayout.addStretch(1)
        # set layout.
        actMenu.setLayout(actLayout)

        return actMenu

    def initAppMenu(self):
        appMenu = QWidget()
        appLayout = QHBoxLayout()
        appLayout.setSpacing(0)
        appLayout.setContentsMargins(0, 0, 0, 0)
        appMenu.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding: 5px;
            border-radius: 15px;
            background: transparent;
            color: #fff;
        }
        QToolTip {
            background: #292929;
            color: #fff;
        }
        QToolButton:hover {
            background: rgba(255, 223, 97, 0.5);
        } 
        ''')
        # open Fig Chat.
        chatBtn = QToolButton(appMenu)
        chatBtn.setToolTip("Open chat.")
        chatBtn.setIcon(FigIcon("sidebar/chat.svg"))
        chatBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        chatBtn.setText("chat\n")
        # chatBtn.clicked.connect(self.openChat) 
        appLayout.addWidget(chatBtn)
        # open assistant.
        botBtn = QToolButton(appMenu)
        botBtn.setToolTip("Open assistant.")
        botBtn.setIcon(FigIcon("sidebar/assistant.svg"))
        botBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        botBtn.setText("assistant\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(botBtn)
        # open calculator.
        calcBtn = QToolButton(appMenu)
        calcBtn.setToolTip("Open calculator.")
        calcBtn.setIcon(FigIcon("sidebar/calculator.svg"))
        calcBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        calcBtn.setText("calculator\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(calcBtn)
        # open calendar.
        calBtn = QToolButton(appMenu)
        calBtn.setToolTip("Open calendar.")
        calBtn.setIcon(FigIcon("sidebar/calendar.svg"))
        calBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        calBtn.setText("calendar\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(calBtn)
        # open clock.
        clockBtn = QToolButton(appMenu)
        clockBtn.setToolTip("Open clock.")
        clockBtn.setIcon(FigIcon("sidebar/clock.svg"))
        clockBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        clockBtn.setText("clock\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(clockBtn)
        # open weather.
        tempBtn = QToolButton(appMenu)
        tempBtn.setToolTip("Open weather.")
        tempBtn.setIcon(FigIcon("sidebar/weather.svg"))
        tempBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        tempBtn.setText("weather\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(tempBtn)
        # open news.
        newsBtn = QToolButton(appMenu)
        newsBtn.setToolTip("Open news.")
        newsBtn.setIcon(FigIcon("sidebar/news.svg"))
        newsBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newsBtn.setText("news\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(newsBtn)
        # open whiteboard.
        wbBtn = QToolButton(appMenu)
        wbBtn.setToolTip("Open whiteboard.")
        wbBtn.setIcon(FigIcon("sidebar/whiteboard.svg"))
        wbBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        wbBtn.setText("whiteboard\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(wbBtn)
        # open illustrator.
        illuBtn = QToolButton(appMenu)
        illuBtn.setToolTip("Open whiteboard.")
        illuBtn.setIcon(FigIcon("sidebar/illustrator.svg"))
        illuBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        illuBtn.setText("illustrator\n")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(illuBtn)
        # open kanban board.
        kanBanBtn = QToolButton(appMenu)
        kanBanBtn.setToolTip("Open weather.")
        kanBanBtn.setIcon(FigIcon("sidebar/kanban.svg"))
        kanBanBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        kanBanBtn.setText("kanban\nboard")
        # botBtn.clicked.connect(self.decOpac) 
        appLayout.addWidget(kanBanBtn)
        # expander.
        expander = QWidget()
        expander.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        appLayout.addWidget(expander)
        # set layout.
        appMenu.setLayout(appLayout)

        return appMenu

    def initSmartPhoneTaskBar(self, current_widget=None):
        # spDock = QDockWidget()
        # spTaskLayout = QHBoxLayout()
        # spTaskLayout.setSpacing(0)
        # spTaskLayout.setContentsMargins(0, 0, 0, 0)
        # spTaskBar = QWidget(parent=parent)
        # spTaskBar.setStyleSheet('''
        # QWidget {
        #     background: rgba(235, 235, 235, 0.9);
        # }
        # QToolButton {
        #     color: #000;
        #     background: transparent;
        # }''')
        # # spTaskBar.setWindowOpacity(0.9)
        # # task view button.
        # btn1 = QToolButton(spTaskBar)
        # btn1.setIcon(FigIcon("ctrlbar/task-view.svg"))
        # btn1.clicked.connect(self.addNewTaskView)
        # btn1.setAttribute(Qt.WA_TranslucentBackground)
        # # home button 
        # btn2 = QToolButton(spTaskBar)
        # btn2.setText("home")
        # btn2.clicked.connect(lambda: self.tabs.setCurrentIndex(0))
        # btn2.setAttribute(Qt.WA_TranslucentBackground)
        # # back button
        # btn3 = QToolButton(spTaskBar)
        # btn3.setText("back")
        # btn3.setAttribute(Qt.WA_TranslucentBackground)
        # # btn3.clicked.connect(self.histBack())
        
        # # add buttons to layout.
        # spTaskLayout.addStretch(1)
        # spTaskLayout.addWidget(btn3)
        # spTaskLayout.addWidget(btn2)
        # spTaskLayout.addWidget(btn1)
        # spTaskLayout.addStretch(1)
        
        # spTaskBar.setLayout(spTaskLayout)
        # spTaskBar.setMaximumWidth(200)
        # spTaskBar.setMaximumHeight(30)
        # # spDock.setWidget(spTaskBar)
        # # spDock.setAttribute(Qt.WA_TranslucentBackground)
        # spTaskBar.setMaximumHeight(50)
        spTaskBar = SmartPhoneTaskBar(
            parent=self, 
            current_widget=current_widget
        )

        return spTaskBar

    def initSysMenu(self):
        sysMenu = QWidget()
        sysLayout = QHBoxLayout()
        sysLayout.setSpacing(0)
        sysLayout.setContentsMargins(0, 0, 0, 0)
        sysMenu.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding: 5px;
            border-radius: 15px;
            background: transparent;
            color: #fff;
        }
        QToolTip {
            background: #292929;
            color: #fff;
        }
        QToolButton:hover {
            background: rgba(255, 223, 97, 0.5);
        } 
        ''')
        # increase opacity.
        opacUpBtn = QToolButton(sysMenu)
        opacUpBtn.setToolTip("increase opacity")
        opacUpBtn.setIcon(FigIcon("sysbar/opacity_up.svg"))
        opacUpBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        opacUpBtn.setText("opac\nup")
        opacUpBtn.clicked.connect(self.incOpac) 
        sysLayout.addWidget(opacUpBtn)
        # decrease opacity.
        opacDownBtn = QToolButton(sysMenu)
        opacDownBtn.setToolTip("increase opacity")
        opacDownBtn.setIcon(FigIcon("sysbar/opacity_down.svg"))
        opacDownBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        opacDownBtn.setText("opac\ndown")
        opacDownBtn.clicked.connect(self.decOpac) 
        sysLayout.addWidget(opacDownBtn)
        # lower brightness.
        dimBtn = QToolButton(sysMenu)
        dimBtn.setToolTip("Lower screen brightness.")
        dimBtn.setIcon(FigIcon("sysbar/dim.svg"))
        dimBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        dimBtn.setText("lower\n")
        dimBtn.clicked.connect(brightnessCtrl.dec_brightness)
        sysLayout.addWidget(dimBtn)
        # increase brightness.
        brightBtn = QToolButton(sysMenu)
        brightBtn.setToolTip("Increase screen brightness.")
        brightBtn.setIcon(FigIcon("sysbar/bright.svg"))
        brightBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        brightBtn.setText("raise\n")
        brightBtn.clicked.connect(brightnessCtrl.inc_brightness)
        sysLayout.addWidget(brightBtn)
        # open history.
        histBtn = QToolButton(sysMenu)#("History", self)
        histBtn.setToolTip("Open History.")
        histBtn.setIcon(FigIcon("sidebar/history.svg"))
        histBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        histBtn.setText("history\n")
        histBtn.clicked.connect(self.addNewHistoryViewer)
        # histBtn.setIconSize()
        sysLayout.addWidget(histBtn)
        # open hardware monitoring dashboard.
        hardwareBtn = QToolButton(sysMenu)
        hardwareBtn.setToolTip("Open hardware dashboard.")
        hardwareBtn.setIcon(FigIcon("sidebar/hard-ware.svg"))
        hardwareBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        hardwareBtn.setText("hardware\nmanager")
        # hardwareBtn.clicked.connect()
        # hardwareBtn.setIconSize(size)
        sysLayout.addWidget(hardwareBtn)
        # open password manager.
        passBtn = QToolButton(sysMenu)
        passBtn.setToolTip("Open password manager.")
        passBtn.setIcon(FigIcon("sidebar/password.svg"))
        passBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        passBtn.setText("password\nmanager")
        # passBtn.setIconSize(size)
        sysLayout.addWidget(passBtn)
        # trash.
        # trash = QToolButton(sysMenu)
        # trash.setToolTip("Open trash folder.")
        # trash.setIcon(FigIcon("sidebar/trash.svg"))
        # trash.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # trash.setText("trash\n")
        # # trash.setIconSize(size)
        # sysLayout.addWidget(trash)
        # email.
        emailBtn = QToolButton(sysMenu)
        emailBtn.setToolTip("Open email client")
        emailBtn.setIcon(FigIcon("sidebar/email.svg"))
        # emailBtn.setIconSize(btnSize)
        emailBtn.clicked.connect(self.addNewMailClient)
        emailBtn.setText("email\n")
        emailBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        sysLayout.addWidget(emailBtn)
        # open notes.
        notesBtn = QToolButton(sysMenu)
        notesBtn.setToolTip("Open note taking app")
        notesBtn.setIcon(FigIcon("sidebar/contacts.svg"))
        # notesBtn.setIconSize(btnSize)
        notesBtn.setText("notes\n")
        notesBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        sysLayout.addWidget(notesBtn)
        # open translator.
        transBtn = QToolButton(sysMenu)
        transBtn.setToolTip("Open translator")
        transBtn.setIcon(FigIcon("sidebar/translate.svg"))
        transBtn.setText("translate\n")
        transBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # transBtn.setIconSize(btnSize)
        sysLayout.addWidget(transBtn)
        # open text to speech.
        ttsBtn = QToolButton(sysMenu)#("Text2Speech", self)
        ttsBtn.setToolTip("Open text to speech")
        ttsBtn.setIcon(FigIcon("sidebar/tts.svg"))
        ttsBtn.setText("text to\nspeech")
        ttsBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # ttsBtn.setIconSize(btnSize)
        sysLayout.addWidget(ttsBtn)
        # open optical character recognition.
        ocrBtn = QToolButton(sysMenu)
        ocrBtn.setToolTip("Open optical character recognition")
        ocrBtn.setIcon(FigIcon("sidebar/ocr.svg"))
        ocrBtn.setText("OCR\n")
        ocrBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # ocrBtn.setIconSize(btnSize)
        sysLayout.addWidget(ocrBtn)
        # qr code generator.
        qrBtn = QToolButton(sysMenu)
        qrBtn.setToolTip("Open qr code generator")
        qrBtn.setIcon(FigIcon("sidebar/qrcode.svg"))
        qrBtn.setText("QR\n")
        qrBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # qrBtn.setIconSize(btnSize)
        qrBtn.clicked.connect(lambda: openQRCodeWindow(
            clipboard=self.clipboard)
        )
        sysLayout.addWidget(qrBtn)
        # blank
        expander = QWidget()
        expander.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sysLayout.addWidget(expander)
        # set layout.
        sysMenu.setLayout(sysLayout)

        return sysMenu

    def initViewMenu(self):
        viewMenu = QWidget()
        viewLayout = QHBoxLayout()
        viewLayout.setSpacing(0)
        viewLayout.setContentsMargins(0, 0, 0, 0)
        # show terminal button.
        termBtn = QToolButton(viewMenu)
        termBtn.setToolTip("Toggle terminal visibility.")
        termBtn.setIcon(FigIcon("fileviewer/open_in_terminal.svg"))
        termBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        termBtn.setText("show\nterminal")
        termBtn.clicked.connect(self.toggleTerminal) 
        # demo gif background.
        gifBackBtn = QToolButton(viewMenu)
        gifBackBtn.setToolTip("Try a gif background.")
        gifBackBtn.setIcon(FigIcon("gif_background.svg"))
        gifBackBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        gifBackBtn.setText("try gif\nbackground")
        # activate wallpaper carousel.
        carouselBtn = QToolButton(viewMenu)
        carouselBtn.setToolTip("Activate wallpaper carousel.")
        carouselBtn.setIcon(FigIcon("carousel.svg"))
        carouselBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        carouselBtn.setText("activate\ncarousel")
        # termBtn.clicked.connect(self.toggleTerminal) 
        self.termBtn = termBtn
        self.isterm_visible = False
        self.istitle_visible = True
        self.istabbar_visible = True
        viewLayout.addWidget(self.termBtn)
        viewLayout.addWidget(gifBackBtn)
        viewLayout.addWidget(carouselBtn)
        # expander
        expander = QWidget()
        expander.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        viewLayout.addWidget(expander)
        
        viewMenu.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding: 5px;
            border-radius: 15px;
            background: transparent;
            color: #fff;
        }   
        QToolTip {
            background: #292929;
            color: #fff;
        }
        QToolButton:hover {
            background: rgba(255, 223, 97, 0.5);
        }      
        ''')
        viewMenu.setLayout(viewLayout)

        return viewMenu

    def initMediaMenu(self):
        mediaMenu = QWidget()
        mediaLayout = QHBoxLayout()
        mediaLayout.setSpacing(0)
        mediaLayout.setContentsMargins(0, 0, 0, 0)
        mediaMenu.setStyleSheet('''
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding: 5px;
            border-radius: 15px;
            background: transparent;
            color: #fff;
        }
        QToolTip {
            background: #292929;
            color: #fff;
        }
        QToolButton:hover {
            background: rgba(255, 223, 97, 0.5);
        } 
        ''')
        # decrease volume.
        volMinusBtn = QToolButton(mediaMenu)
        volMinusBtn.setToolTip("Decrease volume.")
        volMinusBtn.setIcon(FigIcon("sysbar/volminus.svg"))
        volMinusBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        volMinusBtn.setText("lower vol")
        volMinusBtn.clicked.connect(lambda: os.system("xdotool key XF86AudioLowerVolume")) 
        # increase volume .
        volPlusBtn = QToolButton(mediaMenu)
        volPlusBtn.setToolTip("Increase volume.")
        volPlusBtn.setIcon(FigIcon("sysbar/volplus.svg"))
        volPlusBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) 
        volPlusBtn.setText("raise vol")
        volPlusBtn.clicked.connect(lambda: os.system("xdotool key XF86AudioRaiseVolume"))
        # mute.
        muteBtn = QToolButton(mediaMenu)
        muteBtn.setToolTip("Mute.")
        muteBtn.setIcon(FigIcon("sysbar/mute.svg"))
        muteBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        muteBtn.setText("mute")
        muteBtn.clicked.connect(lambda: os.system("xdotool key XF86AudioMute"))
        # play or pause media.
        playBtn = QToolButton(mediaMenu)
        playBtn.setToolTip("Play or pause media.")
        playBtn.setIcon(FigIcon("sysbar/play.svg"))
        playBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        playBtn.setText("play")
        playBtn.clicked.connect(lambda: os.system("xdotool key XF86AudioPlay"))
        # previous media.
        prevBtn = QToolButton(mediaMenu)
        prevBtn.setToolTip("Previous media.")
        prevBtn.setIcon(FigIcon("sysbar/prev.svg"))
        prevBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        prevBtn.setText("prev")
        prevBtn.clicked.connect(lambda: os.system("xdotool key XF86AudioPrev"))
        # next media.
        nextBtn = QToolButton(mediaMenu)
        nextBtn.setToolTip("Next media.")
        nextBtn.setIcon(FigIcon("sysbar/next.svg"))
        nextBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        nextBtn.setText("next")
        nextBtn.clicked.connect(lambda: os.system("xdotool key XF86AudioNext"))
        # add actions.
        expander = QWidget()
        expander.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        mediaLayout.addWidget(volPlusBtn)
        mediaLayout.addWidget(volMinusBtn)
        mediaLayout.addWidget(muteBtn)
        mediaLayout.addWidget(playBtn)
        mediaLayout.addWidget(prevBtn)
        mediaLayout.addWidget(nextBtn)
        mediaLayout.addWidget(expander)
        # set layout.
        mediaMenu.setLayout(mediaLayout)

        return mediaMenu

    def packageManagerBar(self):
        toolbar = QToolBar("Package Manager Bar Visibility")
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setIconSize(QSize(25,25))
        toolbar.setStyleSheet('''
        QToolBar { 
            background: #292929; 
            color: #292929; 
            border: 0px;
        } 
        QToolTip { border: 0px }
        QPushButton { 
            margin: 2px; 
            background: #292929; 
            padding: 2px;
        }
        QPushButton:hover { 
            background: red;
        }
        ''')
        toolbar.setMovable(False)
        # apt package manager.s
        aptBtn = QPushButton()#(" apt ")
        aptBtn.setToolTip("Open a UI for apt/pacman.")
        aptBtn.setIcon(FigIcon("bottombar/apt.png"))
        # aptBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # snapcraft package manager.
        snapBtn = QPushButton()#(" snap ")
        snapBtn.setToolTip("Open a UI for snapcraft.")
        snapBtn.setIcon(FigIcon("bottombar/snap.png"))
        # snapBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # homebrew.
        brewBtn = QPushButton()#(" brew ")
        brewBtn.setToolTip("Get started with brew package manager (recommended for mac)")
        brewBtn.setIcon(FigIcon("bottombar/beer.png"))
        # brewBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # wine.
        wineBtn = QPushButton()#(" wine ")
        wineBtn.setToolTip("Get started with wine for running windows software.")
        wineBtn.setIcon(FigIcon("bottombar/wine.png"))
        # wineBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # pip.
        pipBtn = QPushButton()#(" pip ")
        pipBtn.setToolTip("Open UI for pip.")
        pipBtn.setIcon(FigIcon("bottombar/pip.png"))
        # pipBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # annaconda.
        condaBtn = QPushButton()#(" conda (base) ")
        condaBtn.setToolTip("Open annaconda UI.")
        condaBtn.setIcon(FigIcon("bottombar/conda.png"))
        # condaBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # npm package manager.
        npmBtn = QPushButton()#(" npm ")
        npmBtn.setToolTip("Open a UI for npm.")
        npmBtn.setIcon(FigIcon("bottombar/npm.png"))
        # npmBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # gem package manager.
        gemBtn = QPushButton()#(" gem ")
        gemBtn.setToolTip("Open a UI for gem package manager.")
        gemBtn.setIcon(FigIcon("bottombar/gem.png"))
        # gemBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # maven package manager.
        mvnBtn = QPushButton()#(" mvn ")
        mvnBtn.setToolTip("Open a UI for maven.")
        mvnBtn.setIcon(FigIcon("bottombar/mvn.png"))
        # mvnBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # crates package manager for RUST.
        cargoBtn = QPushButton()#(" cargo ")
        cargoBtn.setToolTip("Open a UI for cargo package manager.")
        cargoBtn.setIcon(FigIcon("bottombar/cargo.png"))
        # cargoBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px; margin: 0px")
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # add actions.
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(aptBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(snapBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(brewBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(wineBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(pipBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(condaBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(npmBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(gemBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(mvnBtn)
        # toolbar.addSeparator()
        toolbar.addWidget(cargoBtn)   
        toolbar.addWidget(right_spacer)  

        return dockToolBar

    def initActBar(self):
        return QWidget()

    def initPackmanBar(self):
        label = QLabel()
        label.setText("THIS IS A LABEL")
        dockPMLauncher = QDockWidget("Package Manager Launcher", self)
        dockPMLauncher.setWidget(label)
        dockPMLauncher.setGeometry(100, 0, 200, 30)

        return dockPMLauncher

    def initBottomBar(self):
        toolbar = QToolBar("Status Bar Visibility")
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setIconSize(QSize(22,22))
        toolbar.setStyleSheet("background: url('/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png');; color: #fff; margin: 0px; border: 0px")
        toolbar.setMovable(False)
        # get git info.
        gitBtn = QPushButton(" main*")
        gitBtn.setToolTip("Inspect current git branch")
        gitBtn.setIcon(FigIcon("bottombar/git-merge.svg"))
        gitBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # warnings.
        warningBtn = QPushButton(" 0")
        warningBtn.setToolTip("See warnings")
        warningBtn.setIcon(FigIcon("bottombar/warning.png"))
        warningBtn.setIconSize(QSize(16,16))
        warningBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # errors.
        errorBtn = QPushButton(" 0")
        errorBtn.setToolTip("See errors")
        errorBtn.setIcon(FigIcon("bottombar/error.png"))
        errorBtn.setIconSize(QSize(16,16))
        errorBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # rw permissions.
        rwBtn = QPushButton("[RW]")
        rwBtn.setToolTip("See read write permissions")
        rwBtn.setIcon(FigIcon("bottombar/pen.svg"))
        rwBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.rwBtn = rwBtn
        # show cursor location.
        cursorBtn = QPushButton("Ln 0, Col 0")
        cursorBtn.setToolTip("Get cursor location.")
        cursorBtn.setIcon(FigIcon("bottombar/mouse.png"))
        cursorBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.cursorBtn = cursorBtn
        # select indentation.
        indentBtn = QPushButton("Spaces: 4")
        indentBtn.setToolTip("Select Indentation.")
        indentBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.indentBtn = indentBtn
        # select encoding.
        encBtn = QPushButton("UTF-8")
        encBtn.setToolTip("Select Encoding.")
        encBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.encBtn = encBtn
        # select end of sequence.
        eosBtn = QPushButton("LF")
        eosBtn.setToolTip("Select End of Sequence.")
        eosBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.eosBtn = eosBtn
        # language mode of code.
        langBtn = QPushButton()
        # langBtn.setIcon(FigIcon("launcher/txt.png"))
        langBtn.setToolTip("Select Language mode.")
        langBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.langBtn = langBtn
        # tweet.
        tweetBtn = QPushButton()
        tweetBtn.setToolTip("Tweet out any issues at me (@Atharva93149016).")
        tweetBtn.setIcon(FigIcon("bottombar/tweet.png"))
        tweetBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        tweetBtn.clicked.connect(lambda x: webbrowser.open("https://twitter.com/compose/tweet?text=@Atharva93149016"))
        # notifications.
        notifBtn = QPushButton()
        notifBtn.setToolTip("Open notifications.")
        notifBtn.setIcon(FigIcon("bottombar/bell.svg"))
        notifBtn.setIconSize(QSize(16,16))
        notifBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # apt package manager.
        aptBtn = QPushButton("apt")
        aptBtn.setToolTip("Open a UI for apt/pacman.")
        aptBtn.setIcon(FigIcon("bottombar/apt.png"))
        aptBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # homebrew.
        brewBtn = QPushButton("brew")
        brewBtn.setToolTip("Get started with brew package manager (recommended for mac)")
        brewBtn.setIcon(FigIcon("bottombar/beer.png"))
        brewBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # wine.
        wineBtn = QPushButton("wine")
        wineBtn.setToolTip("Get started with wine for running windows software.")
        wineBtn.setIcon(FigIcon("bottombar/wine.png"))
        wineBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # pip.
        pipBtn = QPushButton("pip")
        pipBtn.setToolTip("Open UI for pip.")
        pipBtn.setIcon(FigIcon("bottombar/pip.png"))
        pipBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # annaconda.
        condaBtn = QPushButton("conda (base)")
        condaBtn.setToolTip("Open annaconda UI.")
        condaBtn.setIcon(FigIcon("bottombar/conda.png"))
        condaBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # npm package manager.
        npmBtn = QPushButton("npm")
        npmBtn.setToolTip("Open a UI for npm.")
        npmBtn.setIcon(FigIcon("bottombar/npm.png"))
        npmBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # npm package manager.
        mvnBtn = QPushButton("mvn")
        mvnBtn.setToolTip("Open a UI for maven.")
        mvnBtn.setIcon(FigIcon("bottombar/mvn.png"))
        mvnBtn.setStyleSheet("color: #fff; background: #292929; font-family: Monospace; font-size: 14px")
        # buy me a coffee.
        coffeeBtn = QPushButton()
        coffeeBtn.setToolTip("Buy me a coffee :)")
        coffeeBtn.setIcon(FigIcon("bottombar/coffee.png"))
        coffeeBtn.setIconSize(QSize(16,16))
        coffeeBtn.setStyleSheet("color: #fff; background: #292929; font-family: Helvetica; font-size: 14px")
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        spacer.setFixedWidth(30)
        # add actions and widgets.
        toolbar.addWidget(gitBtn)
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(warningBtn)
        toolbar.addSeparator()
        toolbar.addWidget(errorBtn)
        toolbar.addSeparator()
        toolbar.addWidget(rwBtn)
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addSeparator()
        toolbar.addWidget(cursorBtn)
        toolbar.addSeparator()
        toolbar.addWidget(indentBtn)
        toolbar.addSeparator()
        toolbar.addWidget(encBtn)
        toolbar.addSeparator()
        toolbar.addWidget(eosBtn)
        toolbar.addSeparator()
        toolbar.addWidget(langBtn)
        toolbar.addSeparator()
        # toolbar.addWidget(aptBtn)
        # toolbar.addWidget(brewBtn)
        # toolbar.addWidget(wineBtn)
        # toolbar.addWidget(pipBtn)
        # toolbar.addWidget(condaBtn)
        # toolbar.addWidget(npmBtn)
        # toolbar.addWidget(mvnBtn)
        # toolbar.addSeparator() 
        toolbar.addWidget(right_spacer)
        toolbar.addSeparator()
        toolbar.addWidget(tweetBtn)
        toolbar.addWidget(coffeeBtn)
        toolbar.addSeparator()
        toolbar.addWidget(notifBtn)
        toolbar.addWidget(spacer)

        return toolbar

    def initCtrlBar(self):
        toolbar = QToolBar("Control Bar Visibility")
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setIconSize(QSize(16,16))
        toolbar.setFixedHeight(45)
        toolbar.setStyleSheet('''
            QToolBar {
                margin: 0px; 
                border: 0px; 
                color: #fff;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #341d45, stop : 0.8 #8148a8, stop : 1.0 #997eab); */
                /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018); */
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #001433, stop : 0.8 #152d54);
            }
            QLabel {
                color: #fff; 
                /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018); */
                background: transparent;
                border: 0px; 
                font-family: Helvetica; 
                font-size: 14px;            
            }
            QPushButton {
                color: #fff; 
                background: transparent;
                /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018); */
                font-family: Helvetica; 
                font-size: 14px;
                border: 0px;
            }''')
        toolbar.setMovable(False)
        # blank.
        blank1 = QWidget()
        blank2 = QWidget()
        blank5 = QWidget()
        blank6 = QWidget()
        blank1.setFixedWidth(10)
        blank2.setFixedWidth(10)
        blank5.setFixedWidth(10)
        blank6.setFixedWidth(10)
        # about qt button.
        qtBtn = FigAppBtn()
        qtBtn.setIcon(FigIcon("ctrlbar/qt.png"))
        qtBtn.setToolTip("Learn more about Qt and PyQt5.")
        self.qtBtn = qtBtn
        # launch windows menu.
        winBtn = FigAppBtn(orig_size=25, hover_size=30)
        winBtn.setIcon(FigIcon("ctrlbar/windows.svg"))
        winBtn.setToolTip("Open launch menu.")
        # task view button.
        taskViewBtn = FigAppBtn(orig_size=22, hover_size=25)
        taskViewBtn.setIcon(FigIcon("ctrlbar/task-view.svg"))
        taskViewBtn.setToolTip("Open task view.")
        taskViewBtn.clicked.connect(self.addNewTaskView)
        # open color picker dialogue.
        colorpickerBtn = FigAppBtn()
        colorpickerBtn.setToolTip("Open color picker")
        colorpickerBtn.setIcon(FigIcon("ctrlbar/color-picker.png"))
        colorpickerBtn.clicked.connect(lambda: self.colorPickerDialog())
        self.winBtn = winBtn
        # taskbar style.
        taskbarStyle = '''
            QPushButton {
                font-family: Helvetica;
                padding-left: 7px;
                padding-right: 7px;
                padding-top: 8px;
                padding-bottom: 8px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-left: 2px;
                margin-right: 2px;
                border-radius: 20px; 
            }
            QPushButton:hover {
                background: rgba(235, 235, 235, 0.5);
            }'''
        # on screen keyboard.
        oskBtn = QPushButton()
        oskBtn.setToolTip("Open onscreen keyboard.")
        oskBtn.setIcon(FigIcon("ctrlbar/keyboard.svg"))
        oskBtn.setIconSize(QSize(25,25))
        oskBtn.setStyleSheet(taskbarStyle)
        # time label.
        timeLbl = TimeDisplay(self)
        batLbl = BatteryDisplay(self)
        netLbl = NetDisplay(self)
        # system language label.
        langLbl = QLabel()
        langLbl.setText("ENG\n US")
        langLbl.setStyleSheet('''
            QLabel {
                color: #fff;
                background: transparent;
            }
        ''')
        # power button.
        powerBtn = FigPowerController(self)
        powerBtn.setIcon(FigIcon("bottombar/power.svg"))
        powerBtn.setIconSize(QSize(20,20))
        # powerBtn.pressed
        powerBtn.setStyleSheet('''
            QPushButton {
                font-family: Helvetica;
                padding-left: 8px;
                padding-right: 8px;
                padding-top: 10px;
                padding-bottom: 10px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-left: 2px;
                margin-right: 2px;
                border-radius: 18px; 
            }
            QPushButton:hover {
                background: rgba(255, 94, 0, 0.5);
            } ''')
        blank3 = QWidget()
        blank3.setFixedWidth(10)
        blank4 = QWidget()
        blank4.setFixedWidth(30)
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # fig search bar utility.
        searchBar = FigSearchBar()
        
        spacer1 = QWidget()
        spacer1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        spacer1.setFixedWidth(30)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        spacer2.setFixedWidth(30)
        toolbar.addWidget(blank1)
        # add actions and widgets.
        toolbar.addWidget(winBtn)
        toolbar.addWidget(blank2)
        toolbar.addWidget(searchBar)
        toolbar.addWidget(blank3)
        toolbar.addWidget(taskViewBtn)
        # add a blank.
        toolbar.addWidget(blank4)
        toolbar.addWidget(qtBtn)
        toolbar.addWidget(colorpickerBtn)
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(netLbl)
        # toolbar.addSeparator()
        toolbar.addWidget(batLbl)
        # toolbar.addSeparator()
        toolbar.addWidget(oskBtn)
        toolbar.addWidget(langLbl)
        toolbar.addWidget(timeLbl)
        toolbar.addWidget(blank6)
        toolbar.addWidget(powerBtn)
        toolbar.addWidget(blank5)
        # change opacity
        opacEffect = QGraphicsOpacityEffect(self)
        opacEffect.setOpacity(0.97)
        toolbar.setGraphicsEffect(opacEffect)
        toolbar.setAutoFillBackground(True)

        return toolbar


class FigApp(QApplication):
    def __init__(self, argv,
                 background="logo.png",
                 x=100, y=100, w=1000, h=850, 
                 theme=None, icon="logo.png", 
                 *args, **kwargs):
        # Handle high resolution displays:
        if len(sys.argv)>1 and sys.argv[1] == "high_dpi":
            if hasattr(Qt, 'AA_EnableHighDpiScaling'):
                print("high resolution")
                QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
            if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
                QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        super(FigApp, self).__init__(argv)
        self.splash_pixmap = QPixmap(__icon__("email/bg_texture2.png"))
        self.splash_screen = QSplashScreen(self.splash_pixmap)
        self.splash_screen.setStyleSheet('''
        QSplashScreen {
            color: #fff;
        }''')
        self.splash_screen.show()
        self.splash_screen.showMessage("Loading fonts")
        self.processEvents()
        # self.setApplicationName("Fig: any Format Is Good enough")
        # add fonts to database.
        fontIds = []
        fontFiles = ["OMORI_GAME.ttf", "OMORI_GAME2.ttf", "HomemadeApple.ttf"]
        for fontFile in fontFiles:
            fontIds.append(QFontDatabase.addApplicationFont(__font__(fontFile)))
        self.splash_screen.showMessage("Loading window")
        self.processEvents()
        self.screen = self.primaryScreen()
        self.window = FigWindow(*args, 
                                screen=self.screen, background=background, 
                                **kwargs)
        
        geometry = self.screen.availableGeometry()
        screen_w, screen_h = geometry.width(), geometry.height()
        self.window.setGeometry(screen_w/2-w/2, screen_h/2-h/2, w, h)
        # TODO: always stay on top (from commandline).
        FigStayOnTop = True
        if FigStayOnTop:
            self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            self.window.setWindowFlags(Qt.FramelessWindowHint)
        self.desktop = self.desktop()
        self.window.setWindowOpacity(self.window.opacLevel)
        self.window.clipboard = self.clipboard() 
        self.setWindowIcon(QIcon(icon))
        self.window.qtBtn.clicked.connect(self.aboutQt)
        self.setup_cursor()

    def notify(self, obj, event):
        if event.type() == QEvent.WindowDeactivate:
            # if isinstance(obj, FigWindow):
            self.window.fig_launcher.blur_bg()
        if event.type() == QEvent.WindowActivate:
            # if isinstance(obj, FigWindow):
            self.window.fig_launcher.unblur_bg()
        return super().notify(obj, event)

    def announce(self):
        print("\x1b[33;1m")
        print(sys.version)
        print("Qt", QT_VERSION_STR)
        print("PyQt5", PYQT_VERSION_STR)
        print("???????????????????????????? ????????????????, ???????????????? \x1b[0m\x1b[31;1m???\x1b[0m")

    def setup_cursor(self):
        '''setup cursor image.'''
        self.setCursorFlashTime(1000)
        pixmap = QPixmap(__icon__("cursor.svg")).scaledToWidth(32).scaledToWidth(32)
        cursor = QCursor(pixmap, 32, 32)
        # self.window.tabs.setCursor(cursor)

    def run(self):
        # self.aboutQt()
        import time
        start = time.time()
        self.window.show()
        self.splash_screen.finish(self.window)
        # print("window.show took:", time.time()-start)
        start = time.time()
        # self.server_thread.start()
        # print("server.thread.start() took:", time.time()-start)
        start = time.time()
        self.beep()
        # print("self.beep() took:", time.time()-start)
        self.announce()
        sys.exit(self.__exec__())

    def __exec__(self):
        self.exec_()
        self.window.fig_launcher.gifBtn._endAnimation()
        # self.server_thread.join()
        
if __name__ == "__main__":
    pass