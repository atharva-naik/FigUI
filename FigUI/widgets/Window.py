#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, logging, datetime
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QRegExp
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QPlainTextEdit
try:
    from Theme import FigTheme
    from Tab import FigTabWidget
    from Launcher import FigLauncher
    from FigUI.subSystem.Shell import FigShell
#     from utils import *
except ImportError:
    from .Theme import FigTheme
    from .Tab import FigTabWidget
    from .Launcher import FigLauncher
    from ..subSystem.Shell import FigShell
#     from .utils import *
def FigIcon(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)


class FigLogHiglighter(QSyntaxHighlighter):
    def __init__(self, parent):
        self._highlight_lines = dict()

    def highlight_line(self, line, fmt):
        if isinstance(line, int) and line >= 0 and isinstance(fmt, QTextCharFormat):
            self._highlight_lines[line] = fmt
            tb = self.document().findBlockByLineNumber(line)
            self.rehighlightBlock(tb)

    def clear_highlight(self):
        self._highlight_lines = dict()
        self.rehighlight()

    def highlightBlock(self, text):
        line = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(line)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)


class FigLogger:
    def __init__(self, path="system.log"):
        self.path = path
        self.widgets = [] # list of widgets that are displaying the log contents.
        self.records = [] # list of log records.
        self.formatted = []
        self.html = []
        open(self.path, "w")
        self.style = {"DEBUG" : "color: #ffe838; font-weight: bold;",
                      "INFO" : "color: #03fcfc; font-weight: bold;",
                      "date" : "color: #ff8e38; font-style: oblique;"}

    def addWidget(self, widget):
        self.widgets.append(widget)

    def _update_widgets(self):
        for widget in self.widgets:
            try:
                widget.setText("<br>".join(self.html))
            except AttributeError:
                pass # if setText is not possible.

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
        date_style = self.style["date"]
        html_line = f"<span style='{style}'>{level}</span>::<span style='{date_style}'>{now}</span>&nbsp;&nbsp;&nbsp;&nbsp;{msg}"
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


class WebRenderEngine(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(WebRenderEngine, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
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


class FigWindow(QMainWindow):
    def __init__(self, init_url='https://pypi.org/project/bossweb/0.0.1/', *args, **kwargs):
        os.makedirs("logs", exist_ok=True)
        super(FigWindow, self).__init__(*args, **kwargs)        
        self.tabs = QTabWidget() # tab widget
        self.tabs.setDocumentMode(True) # making document mode true
        self.tabs.tabBarDoubleClicked.connect(self.addNewTab)
        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.onCurrentTabChange)
        # making tabs closeable	 		
        self.tabs.setTabsClosable(True) 	
        self.tabs.tabCloseRequested.connect(self.onCurrentTabClose) # adding action when tab close is requested
        self.tabs.setStyleSheet("background: #292929; color: #d4d4d4;") # TODO: theme
        self.logger = FigLogger(path=f"logs/{datetime.datetime.now().strftime('%d_%b_%Y_%H_%M_%S')}.log")
        self.centralWidget = QWidget()
        self.centralWidget.layout = QHBoxLayout()
        self.centralWidget.layout.addWidget(self.tabs)
        # self.centralWidget.layout.addWidget(QPushButton("Wow"))
        self.centralWidget.setLayout(self.centralWidget.layout)
        self.setCentralWidget(self.centralWidget) # making tabs as central widget

        self.statusBar = QStatusBar() # creating a status bar
        self.fig_launcher = FigLauncher(self)
        # self.newTabBtn.clicked.connect(self.addNewTab)
        self.tabs.addTab(self.fig_launcher, FigIcon("launcher.png"), "\tLauncher")
        # self.setLayout(self.layout)

    def addNewTerm(self):
        '''Add new terminal widget'''
        terminal = FigShell(parent=self)
        i = self.tabs.addTab(terminal, FigIcon("launcher/bash.png"), "\tTerminal")
        self.tabs.setCurrentIndex(i)

    def addNewTab(self, Squrl=None, label="Blank"):
        '''method for adding new tab'''
        qurl = QUrl('http://www.google.com') # show bossweb homepage
        browser = WebRenderEngine() # creating a WebRenderEngine object
        dev_view = QWebEngineView()
        browser.page().setDevToolsPage(dev_view.page())		
        browser.setUrl(qurl) 
        # browser.execJS("document.location.href='https://developer.mozilla.org/en-US/docs/Web/API/document.location';") # setting url to browser
		# setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
		# adding action to the browser when url is changed, update the url
        # browser.urlChanged.connect(lambda qurl, browser = browser: self.update_urlbar(qurl, browser))
        # adding action to the browser when loading is finished and set the tab title
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
									self.setupTab(i, browser))

    def setupTab(self, i, browser):
        self.tabs.setTabText(i, "\t"+browser.page().title())
        self.tabs.setTabIcon(i, FigIcon("launcher/browser.png"))

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


class FigApp(QApplication):
    def __init__(self, argv, x=100, y=100, w=1000, h=6*125, theme=None, *args, **kwargs):
        super(FigApp, self).__init__(argv)
        self.setApplicationName("Fig: any Format Is Good enough")
        self.window = FigWindow(*args, **kwargs)
        self.window.setGeometry(x, y, w, h)

    def run(self):
        self.window.show()
        sys.exit(self.exec_())


if __name__ == "__main__":
    pass