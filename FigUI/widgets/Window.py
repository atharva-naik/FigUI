#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import webbrowser, psutil, threading
import os, sys, logging, datetime, pathlib
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QThread, QUrl, QTimer, QPoint, QRegExp, QSize, Qt, QT_VERSION_STR
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QTabBar, QDesktopWidget, QLabel, QToolButton

try:
    from Theme import FigTheme
    from Tab import FigTabWidget
    from Launcher import FigLauncher
    from FileViewer import FigFileViewer
    from FigUI.handler import FigHandler
    # from FigUI.handler.Code import CodeEditor
    from FigUI.subSystem.Shell import FigShell
    from FigUI.handler.Code.QtColorPicker import ColorPicker
    from FigUI.subSystem.system.brightness import BrightnessController
#     from utils import *
except ImportError:
    from .Theme import FigTheme
    from .Tab import FigTabWidget
    from ..handler import FigHandler
    from .Launcher import FigLauncher
    from .FileViewer import FigFileViewer
    # from ..handler.Code import CodeEditor
    from ..subSystem.Shell import FigShell
    from ..handler.Code.QtColorPicker import ColorPicker
    from ..subSystem.system.brightness import BrightnessController
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

# system controllers.
brightnessCtrl = BrightnessController()

def serve_all_files(directory="/", port=3000):
    import http.server
    import socketserver
    PORT = port
    DIRECTORY = directory

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=DIRECTORY, **kwargs)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


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
        self.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")

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
        self.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")

    def _updateTime(self):
        batLvl = psutil.sensors_battery()
        percent = int(batLvl.percent)
        pluggedIn = batLvl.power_plugged
        self.setText(f"({percent}%)")
        
        if pluggedIn:
            self.setIcon(FigIcon("bottombar/plugged.svg"))
        else:
            self.setIcon(QIcon())


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
        self.centralWidget.layout.setContentsMargins(0, 0, 0, 0)
        self.centralWidget.layout.addWidget(self.tabs)
        # self.centralWidget.layout.addWidget(QPushButton("Wow"))
        self.centralWidget.setLayout(self.centralWidget.layout)
        self.setCentralWidget(self.centralWidget) # making tabs as central widget
        self.statusBar = QStatusBar() # creating a status bar
        self.handler = FigHandler(self)
        self.fig_launcher = FigLauncher(self)
        # self.newTabBtn.clicked.connect(self.addNewTab)
        self.tabs.addTab(self.fig_launcher, FigIcon("launcher.png"), "\tLauncher")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide,None) # make launcher tab unclosable.
        self.navBarAdded = False
        # self.setLayout(self.layout)
        self.bottomBar = self.initBottomBar()
        self.subSysBar1, self.subSysBar2 = self.subSystemsBar()
        self.debugBar = self.initDebugBar()
        self.mediaBar = self.initMediaBar()
        self.systemBar = self.systemBar()
        self.titleBar = self.initTitleBar()
        self.folderBar = self.folderNavBar()
        self.shortcutBar = self.initShortcutBar()
        self.packmanBar = self.packageManagerBar()
        self.addToolBar(Qt.TopToolBarArea, self.titleBar)
        self.addToolBarBreak(Qt.TopToolBarArea)
        self.addToolBar(Qt.TopToolBarArea, self.folderBar)
        self.addToolBar(Qt.TopToolBarArea, self.shortcutBar)
        self.addToolBar(Qt.LeftToolBarArea, self.debugBar)
        self.addToolBar(Qt.LeftToolBarArea, self.mediaBar)
        self.addToolBar(Qt.LeftToolBarArea, self.systemBar)
        self.addToolBar(Qt.RightToolBarArea, self.subSysBar1)
        self.addToolBar(Qt.RightToolBarArea, self.subSysBar2)
        self.addToolBar(Qt.BottomToolBarArea, self.bottomBar)
        self.addToolBarBreak(Qt.BottomToolBarArea)
        self.addToolBar(Qt.BottomToolBarArea, self.packmanBar)
        self.addToolBarBreak(Qt.TopToolBarArea)

    def initShortcutBar(self):
        home = str(pathlib.Path.home())
        music = os.path.join(home, "Music")
        videos = os.path.join(home, "Videos")
        desktop = os.path.join(home, "Desktop")
        pictures = os.path.join(home, "Pictures")
        documents = os.path.join(home, "Documents")
        downloads = os.path.join(home, "Downloads")

        sysbar = QToolBar()
        sysbar.setIconSize(QSize(22,22))
        sysbar.setStyleSheet("background: #292929; color: #fff")   
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
        sysbar = QToolBar()
        sysbar.setIconSize(QSize(22,22))
        sysbar.setStyleSheet("background: #292929; color: #fff") 
        sysbar.setMovable(False)       
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
        sysbar.addAction(bugBtn)
        sysbar.addAction(labBtn)
        sysbar.addAction(gitHubBtn)
        sysbar.addAction(runBtn)

        return sysbar

    def initMediaBar(self):
        sysbar = QToolBar()
        sysbar.setIconSize(QSize(22,22))
        sysbar.setStyleSheet("background: #292929; color: #fff")        
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
        # add actions.
        sysbar.addAction(prevBtn)
        sysbar.addAction(nextBtn)
        sysbar.addAction(volPlusBtn)
        sysbar.addAction(volMinusBtn)
        sysbar.addAction(muteBtn)
        sysbar.addAction(playBtn)

        return sysbar

    def systemBar(self):
        sysbar = QToolBar()
        sysbar.setIconSize(QSize(22,22))
        sysbar.setStyleSheet("background: #292929; color: #fff")
        sysbar.setMovable(False)
        # top spacer
        top_spacer = QWidget()
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        # add actions and buttons.
        sysbar.addWidget(top_spacer)
        sysbar.addAction(dimBtn)
        sysbar.addAction(brightBtn)
        sysbar.addAction(userBtn)
        sysbar.addAction(settingsBtn)

        return sysbar

    def subSystemsBar(self):
        subbar = QToolBar()
        subbar.setIconSize(QSize(25,25))
        subbar.setStyleSheet('''
        QToolBar { 
            border: 0px; 
            background: #292929; 
            color: #fff 
        } ''')
        
        sysbar = QToolBar()
        sysbar.setIconSize(QSize(25,25))
        sysbar.setStyleSheet("QToolBar { border: 0px; background: #292929; color: #fff }")
        sysbar.setMovable(False)
        # open email client.
        emailBtn = QAction("Email", self)
        emailBtn.setToolTip("Open email client")
        emailBtn.setIcon(FigIcon("sidebar/email.png"))
        # open p2p chat server.
        chatBtn = QAction("Chat", self)
        chatBtn.setToolTip("Open chat server")
        chatBtn.setIcon(FigIcon("sidebar/chat.png"))
        # open math package.
        mathBtn = QAction("Math", self)
        mathBtn.setToolTip("Open mathematical and scientific computing software suite.")
        mathBtn.setIcon(FigIcon("sidebar/calculator.png"))
        # open newsfeed.
        newsBtn = QAction("Newsfeed", self)
        newsBtn.setToolTip("Open news feed")
        newsBtn.setIcon(FigIcon("sidebar/news.png"))
        # open password manager.
        passBtn = QAction("PassMan", self)
        passBtn.setToolTip("Open password manager")
        passBtn.setIcon(FigIcon("sidebar/password.png"))
        # open hardware monitoring software package.
        hardwareBtn = QAction("Hardware Manager", self)
        hardwareBtn.setToolTip("Open hardware manager")
        hardwareBtn.setIcon(FigIcon("sidebar/hardware.svg"))
        # open date and time.
        calBtn = QAction("Calendar", self)
        calBtn.setToolTip("Open date/time widget")
        calBtn.setIcon(FigIcon("sidebar/calendar.png"))
        # trash.
        trash = QAction("Trash", self)
        trash.setToolTip("Open trash folder.")
        trash.setIcon(FigIcon("sidebar/trash.png"))
        # add actions.
        subbar.addAction(emailBtn)
        subbar.addAction(chatBtn)
        subbar.addAction(calBtn)
        # subbar.addSeparator()
        subbar.addAction(newsBtn)
        subbar.addAction(mathBtn)
        # subbar.addSeparator()
        # subbar.addWidget(QHLine())
        # subbar.addSeparator()
        top_spacer = QWidget()
        top_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sysbar.addWidget(top_spacer)
        sysbar.addAction(hardwareBtn)
        sysbar.addAction(passBtn)
        sysbar.addAction(trash)

        return subbar, sysbar

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

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
        ontopBtn.setToolTip("always stay on top")
        ontopBtn.setIcon(FigIcon("ontop.svg"))
        ontopBtn.triggered.connect(lambda: self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint))

        self.opacLevel = 0.99
        opacUpBtn = QAction(self)
        opacUpBtn.setToolTip("increase opacity")
        opacUpBtn.setIcon(FigIcon("blue.svg"))
        opacUpBtn.triggered.connect(self.incOpac)

        opacDownBtn = QAction(self)
        opacDownBtn.setToolTip("decrease opacity")
        opacDownBtn.setIcon(FigIcon("orange.svg"))
        opacDownBtn.triggered.connect(self.decOpac)

        windowTitle = QLabel()
        windowTitle.setText("𝔽𝕚𝕘 𝕀𝕤 𝕒 𝔾𝕦𝕚") #("𝗙ig 𝗜s a 𝗚UI")

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
        toolbar = QToolBar()
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
        toolbar = QToolBar()
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
        QPushButton:hover { background: red }
        ''')
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

        return toolbar

    def initBottomBar(self):
        toolbar = QToolBar()
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
        # open color picker dialogue.
        colorpickerBtn = QAction("Colorpicker", self)
        colorpickerBtn.setToolTip("Open color picker")
        colorpickerBtn.setIcon(FigIcon("bottombar/colorwheel.svg"))
        colorpickerBtn.triggered.connect(lambda: self.colorPickerDialog())
        # get git info.
        gitBtn = QPushButton(" main*")
        gitBtn.setToolTip("Inspect current git branch")
        gitBtn.setIcon(FigIcon("bottombar/git-merge.svg"))
        gitBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # warnings.
        warningBtn = QPushButton(" 10")
        warningBtn.setToolTip("See warnings")
        warningBtn.setIcon(FigIcon("bottombar/warning.png"))
        warningBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # errors.
        errorBtn = QPushButton(" 24")
        errorBtn.setToolTip("See errors")
        errorBtn.setIcon(FigIcon("bottombar/error.png"))
        errorBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # rw permissions.
        rwBtn = QPushButton("[RW]")
        rwBtn.setToolTip("See read write permissions")
        rwBtn.setIcon(FigIcon("bottombar/pen.svg"))
        rwBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # show cursor location.
        cursorBtn = QPushButton("Ln 0, Col 0")
        cursorBtn.setToolTip("Get cursor location.")
        cursorBtn.setIcon(FigIcon("bottombar/mouse.png"))
        cursorBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # select indentation.
        indentBtn = QPushButton("Spaces: 4")
        indentBtn.setToolTip("Select Indentation.")
        indentBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # select encoding.
        encBtn = QPushButton("UTF")
        encBtn.setToolTip("Select Encoding.")
        encBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # select end of sequence.
        eosBtn = QPushButton("LF")
        eosBtn.setToolTip("Select End of Sequence.")
        eosBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        # language mode of code.
        langBtn = QPushButton()
        # langBtn.setIcon(FigIcon("launcher/txt.png"))
        langBtn.setToolTip("Select Language mode.")
        langBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        self.langReadOut = langBtn
        # tweet.
        tweetBtn = QPushButton()
        tweetBtn.setToolTip("Tweet out any issues at me (@Atharva93149016).")
        tweetBtn.setIcon(FigIcon("bottombar/tweet.png"))
        tweetBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Helvetica; font-size: 14px")
        tweetBtn.clicked.connect(lambda x: webbrowser.open("https://twitter.com/compose/tweet?text=@Atharva93149016"))
        # notifications.
        notifBtn = QPushButton()
        notifBtn.setToolTip("Open notifications.")
        notifBtn.setIcon(FigIcon("bottombar/bell.png"))
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
        coffeeBtn = QPushButton(" Donate")
        coffeeBtn.setToolTip("Buy me a coffe :)")
        coffeeBtn.setIcon(FigIcon("bottombar/coffee.png"))
        coffeeBtn.setStyleSheet("color: #fff; background: #292929; font-family: Helvetica; font-size: 14px")
        # time label.
        timeLbl = TimeDisplay(self)
        batLbl = BatteryDisplay(self)
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # add actions.
        toolbar.addWidget(qtBtn)
        toolbar.addAction(colorpickerBtn)
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
        toolbar.addWidget(coffeeBtn)
        toolbar.addSeparator()
        toolbar.addWidget(right_spacer)
        toolbar.addSeparator()
        toolbar.addWidget(tweetBtn)
        toolbar.addSeparator()
        toolbar.addWidget(notifBtn)       
        toolbar.addSeparator()
        toolbar.addWidget(batLbl)
        toolbar.addSeparator()
        toolbar.addWidget(timeLbl)

        return toolbar

    def colorPickerDialog(self):
        colorPicker = ColorPicker(useAlpha=True)
        picked_color = colorPicker.getColor((0,0,0,50))
        print(picked_color)

    def addNewTerm(self):
        '''Add new terminal widget'''
        terminal = FigShell(parent=self)
        i = self.tabs.addTab(terminal, FigIcon("launcher/bash.png"), "\tTerminal")
        self.tabs.setCurrentIndex(i)

    def addNewBashrcViewer(self):
        '''Add new bashrc customizer.'''
        home = pathlib.Path.home()
        bashrc = os.path.join(home, ".bashrc")
        handlerWidget = self.handler.getUI(path=bashrc)
        i = self.tabs.addTab(handlerWidget, FigIcon("launcher/bashrc.png"), "\t.bashrc")
        self.tabs.setCurrentIndex(i)

    def addNewTextEditor(self):
        '''Add new bashrc customizer.'''
        handlerWidget = self.handler.getUI("Untitled.txt")
        i = self.tabs.addTab(handlerWidget, FigIcon("launcher/txt.png"), "\tUntitled")
        self.tabs.setCurrentIndex(i)

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


class FigApp(QApplication):
    def __init__(self, argv, 
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
        self.setApplicationName("Fig: any Format Is Good enough")
        # add fonts to database.
        fontIds = []
        fontFiles = ["OMORI_GAME.ttf", "OMORI_GAME2.ttf", "HomemadeApple.ttf"]
        for fontFile in fontFiles:
            fontIds.append(QFontDatabase.addApplicationFont(__font__(fontFile)))

        self.window = FigWindow(*args, **kwargs)
        self.window.setGeometry(x, y, w, h)
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.window.setWindowOpacity(self.window.opacLevel)
        self.server_thread = threading.Thread(target=serve_all_files)
        self.setWindowIcon(QIcon(icon))
        # if fontId1 < 0:
        #     self.window.logger.error("unable to load OMORI_GAME.ttf")
        # else:
        #     self.window.logger.debug("loaded OMORI_GAME.ttf successfully")
        self.setCursorFlashTime(1000)
        self.window.qtBtn.clicked.connect(self.aboutQt)

    def announce(self):
        print(sys.version)
        print("Qt version:", QT_VERSION_STR)
        print("PyQt5 version:", PYQT_VERSION_STR)
        print("made by: 𝓐𝓽𝓱𝓪𝓻𝓿𝓪 𝓝𝓪𝓲𝓴, with ❤️ ")

    def run(self):
        # self.aboutQt()
        import time
        start = time.time()
        self.window.show()
        print("window.show took:", time.time()-start)
        
        start = time.time()
        self.server_thread.start()
        print("server.thread.start() took:", time.time()-start)
        
        start = time.time()
        self.beep()
        print("self.beep() took:", time.time()-start)

        self.announce()
        sys.exit(self.__exec__())

    def __exec__(self):
        self.exec_()
        self.window.fig_launcher.gifBtn._endAnimation()
        self.server_thread.join()
        

if __name__ == "__main__":
    pass