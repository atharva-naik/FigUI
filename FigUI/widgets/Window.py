#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mimetypes
import os, sys, math
import json, datetime, pathlib
import psutil, webbrowser, threading
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QThread, QUrl, QTimer, QPoint, QRect, QSize, Qt, QT_VERSION_STR
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QCursor, QPixmap, QTextCharFormat, QSyntaxHighlighter, QFontDatabase, QTextFormat, QColor, QPainter, QDesktopServices, QWindow
from PyQt5.QtWidgets import QMenu, QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QTabBar, QDesktopWidget, QLabel, QToolButton, QTextEdit, QComboBox, QListWidget, QListWidgetItem, QScrollArea, QDockWidget, QGraphicsBlurEffect, QSplitter

try:
    from Theme import FigTheme
    from Tab import FigTabWidget
    from Launcher import FigLauncher
    from FigUI.handler import FigHandler
    # from FigUI.handler.Code import CodeEditor
    from FigUI.subSystem.Clock import FigClock
    from FigUI.subSystem.Shell import FigShell
    from FigUI.subSystem.ChatBot import FigChatBot
    from FigUI.subSystem.History import HistoryLogger
    from FigUI.widgets.ActivityPanel import FigActivityPanel
    from FigUI.handler.Code.QtColorPicker import ColorPicker
    from FileViewer import FigFileViewer, FigTreeFileExplorer
    from FigUI.subSystem.System.Network import NetworkHandler
    from FigUI.subSystem.Math.Calculator import FigCalculator
    from FigUI.subSystem.System.Power import FigPowerController
    from FigUI.subSystem.System.Display import BrightnessController
#     from utils import *
except ImportError:
    from .Theme import FigTheme
    from .Tab import FigTabWidget
    from ..handler import FigHandler
    from .Launcher import FigLauncher
    # from ..handler.Code import CodeEditor
    from ..subSystem.Clock import FigClock
    from ..subSystem.Shell import FigShell
    from ..subSystem.ChatBot import FigChatBot
    from .ActivityPanel import FigActivityPanel
    from ..subSystem.History import HistoryLogger
    from ..handler.Code.QtColorPicker import ColorPicker
    from ..subSystem.System.Network import NetworkHandler
    from ..subSystem.Math.Calculator import FigCalculator
    from ..subSystem.System.Power import FigPowerController
    from .FileViewer import FigFileViewer, FigTreeFileExplorer
    from ..subSystem.System.Display import BrightnessController
#     from .utils import *
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

# system controllers.
brightnessCtrl = BrightnessController()
# def serve_all_files(directory="/", port=5000):
#     import http.server
#     import socketserver
#     PORT = port
#     DIRECTORY = directory

#     class Handler(http.server.SimpleHTTPRequestHandler):
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, directory=DIRECTORY, **kwargs)

#     with socketserver.TCPServer(("", PORT), Handler) as httpd:
#         print("serving at port", PORT)
#         httpd.serve_forever()
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
            "%a %b %d %Y %-I:%M:%S %p "
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
class FigTabWidget(QTabWidget):
    '''
    https://forum.qt.io/topic/67542/drag-tabs-between-qtabwidgets/6
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setAcceptDrops(True)
        self.tabBar = self.tabBar()
        self.tabBar.setMouseTracking(True)
        self.indexTab = None
        self.setMovable(True)
        # self.addTab(QWidget(self), 'Tab One')
        # self.addTab(QWidget(self), 'Tab Two')
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar
        posInTab = tabBar.mapFromGlobal(globalPos)
        self.indexTab = tabBar.tabAt(e.pos())
        tabRect = tabBar.tabRect(self.indexTab)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap,QPoint(),QRegion(tabRect))
        mimeData = QMimeData()
        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        cursor = QCursor(Qt.OpenHandCursor)
        drag.setHotSpot(e.pos() - posInTab)
        drag.setDragCursor(cursor.pixmap(),Qt.MoveAction)
        dropAction = drag.exec_(Qt.MoveAction)


    def dragEnterEvent(self, e):
        e.accept()
        if e.source().parentWidget() != self:
            return

        print(self.indexOf(self.widget(self.indexTab)))
        self.parent.TABINDEX = self.indexOf(self.widget(self.indexTab))


    def dragLeaveEvent(self,e):
        e.accept()


    def dropEvent(self, e):
        print(self.parent.TABINDEX)
        if e.source().parentWidget() == self:
            return

        e.setDropAction(Qt.MoveAction)
        e.accept()
        counter = self.count()

        if counter == 0:
            self.addTab(e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabText(self.parent.TABINDEX))
        else:
            self.insertTab(counter + 1 ,e.source().parentWidget().widget(self.parent.TABINDEX),e.source().tabText(self.parent.TABINDEX))

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
                    font-weight: bold 
                }

                QPushButton:hover {
                    color: #292929;
                    background: #32a8a6; 
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
            HLayout.addWidget(timeLbl)
            # create widget for this row.
            rowWidget = QWidget()
            rowWidget.setLayout(HLayout)
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
            self.permList.addItem(QListWidgetItem(f"✔️ {pt}",  self.permList))
        # limitations.
        for pt in license_template["limitations"]:
            self.limList.addItem(QListWidgetItem(f"❌ {pt}",  self.limList))
        # conditions.
        for pt in license_template["conditions"]:
            self.condList.addItem(QListWidgetItem(f"ⓘ {pt}",  self.condList))
        
        version = license_template["version"]
        timestamp = license_template["date"]
        self.version.setText(version)
        self.timestamp.setText(f"🗓 {timestamp}")


class WebRenderEngine(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(WebRenderEngine, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
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
        self.menu.addAction('My action')
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
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
        self.browser = WebRenderEngine(parent)
        layout.addWidget(self.browser)
        # set toolbar sizes.
        navbar.setIconSize(QSize(20,20))
        if parent:
            parent.navbar = navbar
            if not(parent.navBarAdded):
                parent.addToolBar(navbar)
                parent.logger.info(f"browser bar added for {parent.winId()}")
        self.setLayout(layout)


class FigWindow(QMainWindow):
    def __init__(self, background="logo.png", *args, **kwargs):
        os.makedirs("logs", exist_ok=True)
        super(FigWindow, self).__init__(*args, **kwargs)  
        self.setMouseTracking(True) # allow mouse tracking   

        # set background image path.
        self.background = background
        # initialize file tree.
        self.fileTree = FigTreeFileExplorer()
        # initialize activity panel.
        self.activity = FigActivityPanel(parent=self)

        self.ctrlBar = self.initCtrlBar()
        self.bottomBar = self.initBottomBar()
        self.subSysBar1, self.subSysBar2 = self.subSystemsBar()
        # self.subSysBar1.hide()
        # self.subSysBar2.hide()
        self.debugBar = self.initDebugBar()
        self.mediaBar = self.initMediaBar()
        self.systemBar = self.systemBar()
        self.titleBar = self.initTitleBar()
        self.folderBar = self.folderNavBar()
        self.shortcutBar = self.initShortcutBar()

        # package manager launcher
        self.packmanBar = self.initPackmanBar()
        self.packmanBar.setMinimumSize(QSize(300,400))

        self.addToolBar(Qt.TopToolBarArea, self.titleBar)
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(Qt.TopToolBarArea, self.folderBar)
        self.addToolBar(Qt.TopToolBarArea, self.shortcutBar)
        self.addToolBar(Qt.LeftToolBarArea, self.debugBar)
        self.addToolBar(Qt.LeftToolBarArea, self.mediaBar)
        self.addToolBar(Qt.LeftToolBarArea, self.systemBar)
        self.addToolBarBreak(Qt.LeftToolBarArea)
        # self.addToolBar(Qt.LeftToolBarArea, self.packmanBar)
        self.addToolBar(Qt.RightToolBarArea, self.subSysBar1)
        self.addToolBar(Qt.RightToolBarArea, self.subSysBar2)
        self.addToolBar(Qt.BottomToolBarArea, self.ctrlBar)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.bottomBar)
        self.addToolBarBreak(Qt.TopToolBarArea)

        self.tabs = QTabWidget() # tab widget
        self.tabs.setDocumentMode(True) # making document mode true
        self.tabs.tabBarDoubleClicked.connect(self.addNewTab)
        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.onCurrentTabChange)
        # making tabs closeable	 		
        self.tabs.setTabsClosable(True) 	
        self.tabs.tabCloseRequested.connect(self.onCurrentTabClose) # adding action when tab close is requested
        # self.tabs.setGraphicsEffect(self.blur_effect)
        self.tabs.setStyleSheet('''
        QTabWidget {
            background: rgba(29, 29, 29, 0.95);
            color: #fff;
        }
        QTabBar::tab {
            /* background: #292929; */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
            color: #eee;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 9px;
            padding-right: 5px;
            /* border-top-left-radius: 5px;
            border-top-right-radius: 5px; */
            margin-right: 1px;
            margin-left: 1px;
        }
        QTabBar::tab:hover {
            background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #70121c, stop : 0.6 #b31f2f, stop : 0.8 #de2336);
            color: #fff;
        }
        QTabBar::tab:selected {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018);
            color: #fff;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 9px;
            padding-right: 5px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        ''') # TODO: theme
        self.logger = FigLogger(path=f"logs/{datetime.datetime.now().strftime('%d_%b_%Y_%H_%M_%S')}.log")
        self.centralWidget = QSplitter(Qt.Horizontal)
        # self.centralWidget.layout = QHBoxLayout()
        # self.centralWidget.layout.setContentsMargins(0, 0, 0, 0)
        # side bar with hierarchical file explorer.
        # self.centralWidget.layout.addWidget(self.fileTree)
        # self.centralWidget.layout.addWidget(self.tabs)
        self.centralWidget.addWidget(self.fileTree)
        self.centralWidget.addWidget(self.tabs)
        self.centralWidget.addWidget(self.activity)
        self.centralWidget.setStyleSheet("background: #292929")
        # self.centralWidget.layout.addWidget(QPushButton("Wow"))
        # self.centralWidget.setLayout(self.centralWidget.layout)
        self.setCentralWidget(self.centralWidget) # making tabs as central widget
        self.statusBar = QStatusBar() # creating a status bar
        self.handler = FigHandler(self)
        self.fig_history = HistoryLogger()
        self.fig_launcher = FigLauncher(self)
        # self.newTabBtn.clicked.connect(self.addNewTab)
        self.tabs.addTab(self.fig_launcher, FigIcon("launcher.png"), "\tLauncher")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide,None) # make launcher tab unclosable.
        self.navBarAdded = False
        # self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground, True) # NOTE: need for rounded corners

    def initShortcutBar(self):
        home = str(pathlib.Path.home())
        music = os.path.join(home, "Music")
        videos = os.path.join(home, "Videos")
        desktop = os.path.join(home, "Desktop")
        pictures = os.path.join(home, "Pictures")
        documents = os.path.join(home, "Documents")
        downloads = os.path.join(home, "Downloads")

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
        videosBtn.setToolTip("open videos.")
        videosBtn.setIcon(FigIcon("sysbar/videos.svg"))
        videosBtn.triggered.connect(lambda: self.addNewFileViewer(path=videos))
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

        return sysbar

    def initDebugBar(self):
        sysbar = QToolBar("Coding ToolBar Visibility")
        sysbar.setIconSize(QSize(25,25))
        sysbar.setStyleSheet('''
            padding: 3px; 
            margin: 0px; 
            background: #292929; 
            color: #fff; 
            border: 0px
        ''')
        sysbar.setMovable(False)       
        # file explorer.
        fileTreeBtn = QAction("Explorer", self)
        fileTreeBtn.setToolTip("file explorer.")
        fileTreeBtn.setIcon(FigIcon("sysbar/explorer.svg"))
        fileTreeBtn.triggered.connect(self.fileTree.toggle)
        # activity panel.
        activityBtn = QAction("Activity", self)
        activityBtn.setToolTip("Check activity panel.")
        activityBtn.setIcon(FigIcon("sysbar/activity.svg"))
        activityBtn.triggered.connect(self.activity.toggle)
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

        sysbar.addAction(fileTreeBtn)
        sysbar.addAction(activityBtn)
        sysbar.addAction(bugBtn)
        sysbar.addAction(labBtn)
        sysbar.addAction(gitHubBtn)
        sysbar.addAction(runBtn)

        return sysbar

    def initMediaBar(self):
        sysbar = QToolBar("Media Controls Bar Visibility")
        sysbar.setIconSize(QSize(25,25))
        sysbar.setStyleSheet('''
            padding: 3px; 
            margin: 0px; 
            background: #292929; 
            color: #fff; 
            border: 0px
        ''')
        # decrease volume .
        volMinusBtn = QAction("Volume Minus", self)
        volMinusBtn.setToolTip("Decrease volume.")
        volMinusBtn.setIcon(FigIcon("sysbar/volminus.svg"))
        volMinusBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioLowerVolume")) 
        # increase volume .
        volPlusBtn = QAction("Volume Plus", self)
        volPlusBtn.setToolTip("Increase volume.")
        volPlusBtn.setIcon(FigIcon("sysbar/volplus.svg")) 
        volPlusBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioRaiseVolume"))
        # mute.
        muteBtn = QAction("Mute", self)
        muteBtn.setToolTip("Mute.")
        muteBtn.setIcon(FigIcon("sysbar/mute.svg"))
        muteBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioMute"))
        # play or pause media.
        playBtn = QAction("Play/Pause", self)
        playBtn.setToolTip("Play or pause media.")
        playBtn.setIcon(FigIcon("sysbar/play.svg"))
        playBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioPlay"))
        # previous media.
        prevBtn = QAction("Prev", self)
        prevBtn.setToolTip("Previous media.")
        prevBtn.setIcon(FigIcon("sysbar/prev.svg"))
        prevBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioPrev"))
        # next media.
        nextBtn = QAction("Next", self)
        nextBtn.setToolTip("Next media.")
        nextBtn.setIcon(FigIcon("sysbar/next.svg"))
        nextBtn.triggered.connect(lambda: os.system("xdotool key XF86AudioNext"))
        blank1 = QAction("", self)
        blank2 = QAction("", self)
        # add actions.
        sysbar.addAction(blank1)
        sysbar.addAction(volPlusBtn)
        sysbar.addAction(volMinusBtn)
        sysbar.addAction(muteBtn)
        sysbar.addAction(playBtn)
        sysbar.addAction(prevBtn)
        sysbar.addAction(nextBtn)
        sysbar.addAction(blank2)

        return sysbar

    def systemBar(self):
        sysbar = QToolBar("System Controls Bar Visibility")
        sysbar.setIconSize(QSize(25,25))
        sysbar.setStyleSheet('''
            padding: 3px; 
            margin: 0px; 
            background: #292929; 
            color: #fff; 
            border: 0px
        ''')
        sysbar.setMovable(False)
        # top spacer
        top_spacer = QWidget()
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # stay on top
        ontopBtn = QAction(self)
        ontopBtn.setToolTip("always stay on top")
        ontopBtn.setIcon(FigIcon("sysbar/ontop.svg"))
        
        # flag to stay on top
        ontopBtn.triggered.connect(lambda: self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))
        # increase opacity
        self.opacLevel = 0.99
        opacUpBtn = QAction(self)
        opacUpBtn.setToolTip("increase opacity")
        opacUpBtn.setIcon(FigIcon("sysbar/opacity_up.svg"))
        opacUpBtn.triggered.connect(self.incOpac)
        # decrease opacity
        opacDownBtn = QAction(self)
        opacDownBtn.setToolTip("decrease opacity")
        opacDownBtn.setIcon(FigIcon("sysbar/opacity_down.svg"))
        opacDownBtn.triggered.connect(self.decOpac)
        # lower brightness.
        dimBtn = QAction("Lower Brightness", self)
        dimBtn.setToolTip("Lower screen brightness.")
        dimBtn.setIcon(FigIcon("sysbar/dim.svg"))
        dimBtn.triggered.connect(brightnessCtrl.dec_brightness)
        # increase brightness.
        brightBtn = QAction("Increase Brightness", self)
        brightBtn.setToolTip("Increase screen brightness.")
        brightBtn.setIcon(FigIcon("sysbar/bright.svg"))
        brightBtn.triggered.connect(brightnessCtrl.inc_brightness)
        # user settings.
        userBtn = QAction("User Settings", self)
        userBtn.setToolTip("Open user/admin system settings.")
        userBtn.setIcon(FigIcon("sysbar/user_settings.svg"))
        # settings.
        settingsBtn = QAction("Settings", self)
        settingsBtn.setToolTip("Open system settings.")
        settingsBtn.setIcon(FigIcon("sysbar/settings.svg"))
        # on screen keyboard.
        oskBtn = QAction("On Screen Keyboard", self)
        oskBtn.setToolTip("Open onscreen keyboard.")
        oskBtn.setIcon(FigIcon("sysbar/keyboard.svg"))
        # open color picker dialogue.
        colorpickerBtn = QAction("Colorpicker", self)
        colorpickerBtn.setToolTip("Open color picker")
        colorpickerBtn.setIcon(FigIcon("bottombar/colorwheel.svg"))
        colorpickerBtn.triggered.connect(lambda: self.colorPickerDialog())
        # add actions and buttons.
        sysbar.addAction(opacUpBtn)
        sysbar.addAction(opacDownBtn)
        sysbar.addAction(ontopBtn)
        sysbar.addAction(oskBtn)
        sysbar.addAction(dimBtn)
        sysbar.addAction(brightBtn)
        sysbar.addAction(colorpickerBtn)
        sysbar.addWidget(top_spacer)
        sysbar.addAction(userBtn)
        sysbar.addAction(settingsBtn)

        return sysbar

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
            /* background: url('/home/atharva/GUI/FigUI/FigUI/assets/icons/glass_texture.jpg') 0 0 0 0;
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
            /* background: #b31f2f; */
            background: rgba(185, 255, 236, 0.5);
        }
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
        emailBtn = QPushButton()
        emailBtn.setToolTip("Open email client")
        emailBtn.setIcon(FigIcon("sidebar/email.svg"))
        emailBtn.setIconSize(btnSize)
        # open notes.
        notesBtn = QPushButton()
        notesBtn.setToolTip("Open note taking app")
        notesBtn.setIcon(FigIcon("sidebar/contacts.svg"))
        notesBtn.setIconSize(btnSize)
        # open translator.
        transBtn = QPushButton()#("Translator", self)
        transBtn.setToolTip("Open translator")
        transBtn.setIcon(FigIcon("sidebar/translate.svg"))
        transBtn.setIconSize(btnSize)
        # open text to speech.
        ttsBtn = QPushButton()#("Text2Speech", self)
        ttsBtn.setToolTip("Open text to speech")
        ttsBtn.setIcon(FigIcon("sidebar/tts.svg"))
        ttsBtn.setIconSize(btnSize)
        # open optical character recognition.
        ocrBtn = QPushButton()#("OCR", self)
        ocrBtn.setToolTip("Open optical character recognition")
        ocrBtn.setIcon(FigIcon("sidebar/ocr.svg"))
        ocrBtn.setIconSize(btnSize)
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
        mathBtn.clicked.connect(FigCalculator().show)
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
        # open history.
        histBtn = QPushButton()#("History", self)
        histBtn.setToolTip("Open history")
        histBtn.setIcon(FigIcon("sidebar/history.svg"))
        histBtn.clicked.connect(self.addNewHistoryViewer)
        histBtn.setIconSize(btnSize)
        # open password manager.
        passBtn = QPushButton()#("PassMan", self)
        passBtn.setToolTip("Open password manager")
        passBtn.setIcon(FigIcon("sidebar/password.svg"))
        passBtn.setIconSize(size)
        # open hardware monitoring software package.
        hardwareBtn = QPushButton()#("Hardware Manager", self)
        hardwareBtn.setToolTip("Open hardware manager")
        hardwareBtn.setIcon(FigIcon("sidebar/hard-ware.svg"))
        hardwareBtn.setIconSize(size)
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
        # trash.
        trash = QPushButton()#("Trash", self)
        trash.setToolTip("Open trash folder.")
        trash.setIcon(FigIcon("sidebar/trash.svg"))
        trash.setIconSize(size)
        
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
        subbar.addWidget(emailBtn)
        subbar.addWidget(notesBtn)
        subbar.addWidget(transBtn)
        subbar.addWidget(ttsBtn)
        subbar.addWidget(ocrBtn)
        subbar.addWidget(b1)
        subbar.addWidget(chatBtn)
        subbar.addWidget(asstBtn)
        # subbar.addWidget(b2)
        subbar.addWidget(mathBtn)
        subbar.addWidget(calBtn)
        subbar.addWidget(clockBtn)
        subbar.addWidget(weatherBtn)
        subbar.addWidget(newsBtn)
        subbar.addWidget(b3)
        subbar.addWidget(wbBtn)
        subbar.addWidget(illuBtn)
        subbar.addWidget(kanbanBtn)
        subbar.addWidget(b4)
        subbar.addWidget(histBtn)
        # subbar.addSeparator()
        # subbar.addWidget(QHLine())
        # subbar.addSeparator()
        top_spacer = QWidget()
        top_spacer.setAttribute(Qt.WA_TranslucentBackground)
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sysbar.addWidget(top_spacer)
        sysbar.addWidget(hardwareBtn)
        sysbar.addWidget(passBtn)
        sysbar.addWidget(trash)

        return subbar, sysbar

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
            # self.subSysBar1.hide()
            # self.subSysBar2.hide()
        else:
            self.showMaximized()
            # self.subSysBar1.show()
            # self.subSysBar2.show()

    def colorPickerDialog(self):
        colorPicker = ColorPicker(useAlpha=True)
        picked_color = colorPicker.getColor((0,0,0,50))
        print(picked_color)

    def log(self, icon, path):
        handler = __icon__(icon)
        self.fig_history.log(handler, path)

    def addNewTerm(self, path=None):
        '''Add new terminal widget'''
        if path:
            terminal = FigShell(parent=self, cmd=f"cd '{path}'; bash")
        else:
            terminal = FigShell(parent=self)
        # self.terminals = []
        # main_window = QMainWindow()
        # main_window.setCentralWidget(terminal)
        # main_window.show()
        # self.terminals.append(main_window)
        # window = QWindow.fromWinId(main_window.winId())
        # shell = QWidget.createWindowContainer(window)
        i = self.tabs.addTab(terminal, FigIcon("launcher/bash.png"), "\tTerminal")
        self.tabs.setCurrentIndex(i)
        # self.tabs.setTabWhatsThis(i, "xterm (embedded)")
        self.tabs.setTabToolTip(i, "xterm (embedded)")
        self.log("launcher/bash.png", "Terminal")

    def addNewClock(self):
        '''Add new clock window'''
        clockApp = FigClock()
        i = self.tabs.addTab(clockApp, FigIcon("sidebar/clock.png"), "\tClock")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabToolTip(i, "clock app")
        self.log("sidebar/clock.png", "Clock")

    def addNewBotTab(self):
        '''Add new chat bot tab'''
        chatBotApp = FigChatBot()
        i = self.tabs.addTab(chatBotApp, FigIcon("sidebar/assistant.png"), "\tClock")
        self.tabs.setCurrentIndex(i)
        self.tabs.setTabToolTip(i, "assistant app")
        self.log("sidebar/assistant.png", "Assistant")

    def addNewKanBanBoard(self):
        '''Add a new kanban board'''
        pass

    def addNewBashrcViewer(self):
        '''Add new bashrc customizer.'''
        home = pathlib.Path.home()
        bashrc = os.path.join(home, ".bashrc")
        handlerWidget = self.handler.getUI(path=bashrc)
        i = self.tabs.addTab(handlerWidget, FigIcon("launcher/bashrc.png"), "\t.bashrc")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/bashrc.png", bashrc)

    def addNewLicenseGenerator(self):
        '''Add new license template generator.'''
        licenseViewer = FigLicenseGenerator()
        i = self.tabs.addTab(licenseViewer, FigIcon("launcher/license.png"), "\tLICENSE")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/license.png", "LICENSE Generator")

    def addNewHistoryViewer(self):
        '''Add new tab for viewing history.'''
        historyViewer = FigHistoryViewer(self.fig_history)
        i = self.tabs.addTab(historyViewer, FigIcon("launcher/history.png"), f"\t{self.fig_history.title}'s history")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/history.png", self.fig_history.path)

    def addNewTextEditor(self):
        '''Add new bashrc customizer.'''
        handlerWidget = self.handler.getUI("Untitled.txt")
        i = self.tabs.addTab(handlerWidget, FigIcon("launcher/txt.png"), "\tUntitled")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/txt.png", "Untitled")

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
        i = self.tabs.addTab(fileViewer, FigIcon("launcher/fileviewer.png"), f"\t{name} {parent}")# f"\t{str(pathlib.Path.home())}")
        self.tabs.setCurrentIndex(i)
        self.log("launcher/fileviewer.png", path)

    def addNewTab(self, Squrl=None, label="Blank"):
        '''method for adding new tab'''
        qurl = QUrl('http://www.google.com') # show bossweb homepage
        browser = FigBrowser(self) # creating a WebRenderEngine object
        dev_view = QWebEngineView()
        browser.browser.page().setDevToolsPage(dev_view.page())		
        browser.browser.setUrl(qurl) 
        # browser.execJS("document.location.href='https://developer.mozilla.org/en-US/docs/Web/API/document.location';") # setting url to browser
		# setting tab index
        self.navBarAdded = True
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        self.logger.info(f"browser opened into a window with id: {int(self.winId())}")
		# adding action to the browser when url is changed, update the url
        # browser.urlChanged.connect(lambda qurl, browser = browser: self.update_urlbar(qurl, browser))
        # adding action to the browser when loading is finished and set the tab title
        browser.browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.setupTab(i, browser.browser))

    def setupTab(self, i, browser):
        self.tabs.setTabText(i, "\t"+browser.page().title())
        self.tabs.setTabIcon(i, FigIcon("launcher/browser.png"))
        self.log("launcher/browser.png", QUrl('http://www.google.com'))

    def tab_open_doubleclick(self, i):
        # checking index i.e and No tab under the click
        if i == -1: self.addNewTab() # creating a new tab
    
    def onCurrentTabChange(self, i):
        '''when tab is changed.'''
        try:
            qurl = self.tabs.currentWidget().url() # get the curl
		    # self.update_urlbar(qurl, self.tabs.currentWidget()) # update the url 
            self.update_title(self.tabs.currentWidget()) # update the title
        except AttributeError:
            pass
        self.langBtn.setIcon(self.tabs.tabIcon(i))
        filename = pathlib.Path(self.tabs.tabText(i).split("...")[0].strip()
        ).__str__().strip()
        
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

    def update_title(self, browser):
        '''method for update_title'''
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget(): return # do nothing
        title = self.tabs.currentWidget().page().title() # get the page title
        self.setWindowTitle(title) # set the window title

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
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
        }''')
        toolbar.setIconSize(QSize(20,20))
        toolbar.setMovable(False)

        closeBtn = QToolButton(self)
        closeBtn.setToolTip("close window")
        closeBtn.setIcon(FigIcon("close.svg")) 
        closeBtn.setStyleSheet('''
        QToolButton {
            margin: 0px;
        }
        QToolButton:hover {
            border: 0px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        ''')
        closeBtn.clicked.connect(lambda: self.close()) # closing logic.

        minimizeBtn = QToolButton(self)
        minimizeBtn.setToolTip("minimize window")
        minimizeBtn.setIcon(FigIcon("minimize.svg"))
        minimizeBtn.clicked.connect(lambda: self.showMinimized())
        minimizeBtn.setStyleSheet('''
        QToolButton {
            margin: 0px;
        }
        QToolButton:hover {
            border: 0px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        ''')

        maximizeBtn = QToolButton(self)
        maximizeBtn.setToolTip("maximize window")
        maximizeBtn.setIcon(FigIcon("maximize.svg"))
        maximizeBtn.clicked.connect(lambda: self.maximize())
        maximizeBtn.setStyleSheet('''
        QToolButton {
            margin: 0px;
        }
        QToolButton:hover {
            border: 0px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
        ''')

        ontopBtn = QAction(self)
        ontop1Btn = QToolButton(self)
        ontop1Btn.setStyleSheet('''
            QToolButton {
                margin: -8px;
                padding: -1px;
            }
        ''')
        opacUpBtn = QAction(self)
        opacDownBtn = QAction(self)

        windowTitle = QLabel()
        windowTitle.setText("") # ("𝔽𝕚𝕘 𝕀𝕤 𝕒 𝔾𝕦𝕚") #("𝗙ig 𝗜s a 𝗚UI")
        windowTitle.setStyleSheet("color: #fff; font-size: 16px")
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        toolbar.addWidget(ontop1Btn)
        toolbar.addWidget(closeBtn)
        toolbar.addWidget(minimizeBtn)
        toolbar.addWidget(maximizeBtn)
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(windowTitle)
        toolbar.addWidget(right_spacer)
        toolbar.addAction(opacUpBtn)
        toolbar.addAction(opacDownBtn)
        toolbar.addAction(ontopBtn)

        return toolbar

    def incOpac(self):
        self.opacLevel += 0.01 
        self.opacLevel = min(self.opacLevel, 1)
        self.setWindowOpacity(self.opacLevel)

    def decOpac(self):
        self.opacLevel -= 0.01 
        self.opacLevel = max(self.opacLevel, 0.9)
        self.setWindowOpacity(self.opacLevel)

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
        toolbar.setStyleSheet("background: #292929; color: #fff; margin: 0px; border: 0px")
        toolbar.setMovable(False)
        # about qt button.
        qtBtn = QPushButton()
        qtBtn.setIcon(FigIcon("bottombar/qt.png"))
        qtBtn.setToolTip("Learn more about Qt and PyQt5.")
        qtBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.qtBtn = qtBtn
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
        # add actions.
        toolbar.addWidget(qtBtn)
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
        toolbar.setMinimumHeight(16)
        toolbar.setStyleSheet('''
        QToolBar {
            margin: 0px; 
            border: 0px; 
            color: #fff;
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #341d45, stop : 0.8 #8148a8, stop : 1.0 #997eab); */
            background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018);
        }
        QLabel {
            color: #fff; 
            background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018);
            border: 0px; 
            font-family: Helvetica; 
            font-size: 14px;            
        }
        QPushButton {
            color: #fff; 
            background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #61313c, stop : 0.8 #451f2b, stop : 1.0 #331018);
            font-family: Helvetica; 
            font-size: 14px;
            border: 0px;
        }''')
        toolbar.setMovable(False)
        # time label.
        timeLbl = TimeDisplay(self)
        batLbl = BatteryDisplay(self)
        netLbl = NetDisplay(self)
        # power button.
        powerBtn = FigPowerController(self)
        powerBtn.setIcon(FigIcon("bottombar/power.svg"))
        powerBtn.setIconSize(QSize(20,20))
        # powerBtn.pressed
        powerBtn.setStyleSheet('''
        QPushButton {
            background: qradialgradient(cx: 1, cy: 1, radius: 1, stop : 0 #404040, stop: 0.8 #b8b8b8);
            font-family: Helvetica;
            border-radius: 10px;
        }
        QPushButton:hover {
            background: #c0a5d4;
        }''')
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer1 = QWidget()
        spacer1.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        spacer1.setFixedWidth(30)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        spacer2.setFixedWidth(30)
        # add actions.
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(netLbl)
        # toolbar.addSeparator()
        toolbar.addWidget(batLbl)
        # toolbar.addSeparator()
        toolbar.addWidget(timeLbl)
        toolbar.addWidget(spacer1)
        toolbar.addWidget(powerBtn)
        toolbar.addWidget(spacer2)

        return toolbar


class FigApp(QApplication):
    def __init__(self, argv,
                 background="logo.png",
                 x=100, y=100, w=1050, h=850, 
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
        # self.setApplicationName("Fig: any Format Is Good enough")
        # add fonts to database.
        fontIds = []
        fontFiles = ["OMORI_GAME.ttf", "OMORI_GAME2.ttf", "HomemadeApple.ttf"]
        for fontFile in fontFiles:
            fontIds.append(QFontDatabase.addApplicationFont(__font__(fontFile)))

        self.window = FigWindow(*args, background=background, **kwargs)
        self.window.setGeometry(x, y, w, h)
        
        # TODO: always stay on top (from commandline).
        FigStayOnTop = True
        if FigStayOnTop:
            self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        else:
            self.window.setWindowFlags(Qt.FramelessWindowHint)
        
        self.window.setWindowOpacity(self.window.opacLevel)
        self.window.clipboard = self.clipboard() 
        self.setWindowIcon(QIcon(icon))
        self.window.qtBtn.clicked.connect(self.aboutQt)
        self.setup_cursor()

    def announce(self):
        print("\x1b[33;1m")
        print(sys.version)
        print("Qt", QT_VERSION_STR)
        print("PyQt5", PYQT_VERSION_STR)
        print("𝓐𝓽𝓱𝓪𝓻𝓿𝓪 𝓝𝓪𝓲𝓴, 𝔀𝓲𝓽𝓱 \x1b[0m\x1b[31;1m❤\x1b[0m")

    def setup_cursor(self):
        '''setup cursor image.'''
        self.setCursorFlashTime(1000)
        pixmap = QPixmap(__icon__("cursor.svg")).scaledToWidth(32).scaledToWidth(32)
        cursor = QCursor(pixmap, 32, 32)
        self.window.tabs.setCursor(cursor)

    def run(self):
        # self.aboutQt()
        import time
        start = time.time()
        self.window.show()
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