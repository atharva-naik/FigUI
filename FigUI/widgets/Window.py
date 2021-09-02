#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import webbrowser
import os, sys, logging, datetime
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy
try:
    from Theme import FigTheme
    from Tab import FigTabWidget
    from Launcher import FigLauncher
    from FileViewer import FigFileViewer
    from FigUI.subSystem.Shell import FigShell
    from FigUI.subSystem.system.brightness import BrightnessController
#     from utils import *
except ImportError:
    from .Theme import FigTheme
    from .Tab import FigTabWidget
    from .Launcher import FigLauncher
    from .FileViewer import FigFileViewer
    from ..subSystem.Shell import FigShell
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
        self.fig_launcher = FigLauncher(self)
        # self.newTabBtn.clicked.connect(self.addNewTab)
        self.tabs.addTab(self.fig_launcher, FigIcon("launcher.png"), "\tLauncher")
        self.navBarAdded = False
        # self.setLayout(self.layout)
        self.bottomBar = self.initBottomBar()
        self.subSysBar = self.subSystemsBar()
        self.systemBar = self.systemBar()
        self.folderBar = self.folderNavBar()
        self.addToolBar(Qt.TopToolBarArea, self.folderBar)
        self.addToolBar(Qt.LeftToolBarArea, self.systemBar)
        self.addToolBar(Qt.RightToolBarArea, self.subSysBar)
        self.addToolBar(Qt.BottomToolBarArea, self.bottomBar)
        self.addToolBarBreak(Qt.TopToolBarArea)

    def systemBar(self):
        sysbar = QToolBar()
        sysbar.setIconSize(QSize(25,25))
        sysbar.setStyleSheet("background: #292929; color: #fff")
        # decrease volume .
        volMinusBtn = QAction("Volume Minus", self)
        volMinusBtn.setToolTip("Decrease volume.")
        volMinusBtn.setIcon(FigIcon("sysbar/volminus.svg")) 
        # increase volume .
        volPlusBtn = QAction("Volume Plus", self)
        volPlusBtn.setToolTip("Increase volume.")
        volPlusBtn.setIcon(FigIcon("sysbar/volplus.svg")) 
        # mute.
        muteBtn = QAction("Mute", self)
        muteBtn.setToolTip("Mute.")
        muteBtn.setIcon(FigIcon("sysbar/mute.svg"))
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
        # recents.
        recentBtn = QAction("Recent", self)
        recentBtn.setToolTip("recently modified/opened files.")
        recentBtn.setIcon(FigIcon("sysbar/recent.svg"))
        # home.
        homeBtn = QAction("Home", self)
        homeBtn.setToolTip("open home folder.")
        homeBtn.setIcon(FigIcon("sysbar/home.svg"))
        # desktop.
        desktopBtn = QAction("Desktop", self)
        desktopBtn.setToolTip("open desktop.")
        desktopBtn.setIcon(FigIcon("sysbar/desktop.svg"))
        # documents.
        documentBtn = QAction("Documents", self)
        documentBtn.setToolTip("open documents.")
        documentBtn.setIcon(FigIcon("sysbar/documents.svg"))
        # downloads.
        downloadsBtn = QAction("Downloads", self)
        downloadsBtn.setToolTip("open downloads.")
        downloadsBtn.setIcon(FigIcon("sysbar/downloads.svg"))
        # music.
        musicBtn = QAction("Music", self)
        musicBtn.setToolTip("open music.")
        musicBtn.setIcon(FigIcon("sysbar/music.svg"))
        # pictures.
        picturesBtn = QAction("Pictures", self)
        picturesBtn.setToolTip("open videos.")
        picturesBtn.setIcon(FigIcon("sysbar/pictures.svg"))
        # videos.
        videosBtn = QAction("Videos", self)
        videosBtn.setToolTip("open videos.")
        videosBtn.setIcon(FigIcon("sysbar/videos.svg"))
        # debugging.
        bugBtn = QAction("Debug", self)
        bugBtn.setToolTip("start debugging.")
        bugBtn.setIcon(FigIcon("sysbar/bug.svg"))
        # lab.
        labBtn = QAction("Lab", self)
        labBtn.setToolTip("Open development lab")
        labBtn.setIcon(FigIcon("sysbar/lab.svg"))
        # lab.
        gitHubBtn = QAction("GitHub", self)
        gitHubBtn.setToolTip("Integrate with github")
        gitHubBtn.setIcon(FigIcon("sysbar/github.svg"))
        # add actions and buttons.
        sysbar.addAction(recentBtn)
        sysbar.addAction(homeBtn)
        sysbar.addAction(desktopBtn)
        sysbar.addAction(documentBtn)
        sysbar.addAction(downloadsBtn)
        sysbar.addAction(musicBtn)
        sysbar.addAction(picturesBtn)
        sysbar.addAction(videosBtn)
        sysbar.addSeparator()
        sysbar.addWidget(QHLine())
        sysbar.addSeparator()
        sysbar.addAction(bugBtn)
        sysbar.addAction(labBtn)
        sysbar.addAction(gitHubBtn)
        sysbar.addSeparator()
        sysbar.addWidget(QHLine())
        sysbar.addSeparator()
        sysbar.addAction(volPlusBtn)
        sysbar.addAction(volMinusBtn)
        sysbar.addAction(muteBtn)
        sysbar.addSeparator()
        sysbar.addWidget(QHLine())
        sysbar.addSeparator()
        sysbar.addAction(dimBtn)
        sysbar.addAction(brightBtn)
        sysbar.addSeparator()
        sysbar.addWidget(QHLine())
        sysbar.addSeparator()
        sysbar.addAction(userBtn)
        sysbar.addAction(settingsBtn)

        return sysbar

    def subSystemsBar(self):
        subbar = QToolBar()
        subbar.setIconSize(QSize(30,30))
        subbar.setStyleSheet("background: #292929; color: #fff")
        # open email client.
        emailBtn = QAction("Email", self)
        emailBtn.setToolTip("Open email client")
        emailBtn.setIcon(FigIcon("sidebar/email.png"))
        # open newsfeed.
        newsBtn = QAction("Newsfeed", self)
        newsBtn.setToolTip("Open news feed")
        newsBtn.setIcon(FigIcon("sidebar/news.png"))
        # open password manager.
        passBtn = QAction("PassMan", self)
        passBtn.setToolTip("Open password manager")
        passBtn.setIcon(FigIcon("sidebar/password.png"))
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
        # subbar.addSeparator()
        subbar.addAction(newsBtn)
        subbar.addAction(passBtn)
        subbar.addAction(calBtn)
        subbar.addSeparator()
        subbar.addAction(trash)

        return subbar

    def folderNavBar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("color: #fff; background: #292929")
        toolbar.setIconSize(QSize(22,22))
        
        backBtn = QPushButton()
        backBtn.setToolTip("go back in folders")
        backBtn.setIcon(FigIcon("back.svg"))
        nextBtn = QPushButton()
        nextBtn.setToolTip("go forward in folders")
        nextBtn.setIcon(FigIcon("forward.svg"))
        toolbar.addWidget(backBtn)
        toolbar.addWidget(nextBtn)
        
        folders = os.getcwd().split("/")
        for i,folder in enumerate(folders):
            if folder != "":
                btn = QPushButton(folder)
                if i == len(folders)-1:
                    btn.setStyleSheet("font-weight: bold; color: #ff9100")
                toolbar.addWidget(btn)

        return toolbar

    def initBottomBar(self):
        toolbar = QToolBar()
        toolbar.setStyleSheet("color: #fff")
        toolbar.setContentsMargins(0, 0, 0, 0)
        toolbar.setIconSize(QSize(22,22))
        toolbar.setStyleSheet("background: #292929; color: #fff")
        # open color picker dialogue.
        colorpickerBtn = QAction("Colorpicker", self)
        colorpickerBtn.setToolTip("Open color picker")
        colorpickerBtn.setIcon(FigIcon("bottombar/colorwheel.svg"))
        # get git info.
        gitBtn = QPushButton(" main*")
        gitBtn.setToolTip("Inspect current git branch")
        gitBtn.setIcon(FigIcon("bottombar/git-merge.svg"))
        gitBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # warnings.
        warningBtn = QPushButton(" 0")
        warningBtn.setToolTip("See warnings")
        warningBtn.setIcon(FigIcon("bottombar/warning.png"))
        warningBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # errors.
        errorBtn = QPushButton(" 0")
        errorBtn.setToolTip("See errors")
        errorBtn.setIcon(FigIcon("bottombar/error.png"))
        errorBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # rw permissions.
        rwBtn = QPushButton("[RW]")
        rwBtn.setToolTip("See read write permissions")
        rwBtn.setIcon(FigIcon("bottombar/pen.svg"))
        rwBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # show cursor location.
        cursorBtn = QPushButton("Ln 0, Col 0")
        cursorBtn.setToolTip("Get cursor location.")
        cursorBtn.setIcon(FigIcon("bottombar/mouse.png"))
        cursorBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # select indentation.
        indentBtn = QPushButton("Spaces: 4")
        indentBtn.setToolTip("Select Indentation.")
        indentBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # select encoding.
        encBtn = QPushButton("UTF")
        encBtn.setToolTip("Select Encoding.")
        encBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # select end of sequence.
        eosBtn = QPushButton("LF")
        eosBtn.setToolTip("Select End of Sequence.")
        eosBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # language mode of code.
        langBtn = QPushButton("Text")
        langBtn.setToolTip("Select Language mode.")
        langBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # tweet.
        tweetBtn = QPushButton()
        tweetBtn.setToolTip("Tweet out any issues at me (@Atharva93149016).")
        tweetBtn.setIcon(FigIcon("bottombar/tweet.png"))
        tweetBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        tweetBtn.clicked.connect(lambda x: webbrowser.open("https://twitter.com/compose/tweet?text=@Atharva93149016"))
        # notifications.
        notifBtn = QPushButton()
        notifBtn.setToolTip("Open notifications.")
        notifBtn.setIcon(FigIcon("bottombar/bell.png"))
        notifBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # homebrew.
        brewBtn = QPushButton("brew")
        brewBtn.setToolTip("Get started with brew package manager (recommended for mac)")
        brewBtn.setIcon(FigIcon("bottombar/beer.png"))
        brewBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # annaconda.
        condaBtn = QPushButton(" conda (base)")
        condaBtn.setToolTip("Open annaconda UI.")
        condaBtn.setIcon(FigIcon("bottombar/conda.png"))
        condaBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # buy me a coffee.
        coffeeBtn = QPushButton("Donate")
        coffeeBtn.setToolTip("Buy me a coffe :)")
        coffeeBtn.setIcon(FigIcon("bottombar/coffee.png"))
        coffeeBtn.setStyleSheet("color: #fff; background: #292929; border: 0px; font-family: Monospace; font-size: 14px")
        # add actions.
        toolbar.addAction(colorpickerBtn)
        toolbar.addWidget(gitBtn)
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
        toolbar.addSeparator()
        toolbar.addWidget(tweetBtn)
        toolbar.addSeparator()
        toolbar.addWidget(notifBtn)
        toolbar.addSeparator()
        toolbar.addWidget(brewBtn)
        toolbar.addSeparator()
        toolbar.addWidget(condaBtn)
        toolbar.addSeparator()
        toolbar.addWidget(coffeeBtn)

        return toolbar

    def addNewTerm(self):
        '''Add new terminal widget'''
        terminal = FigShell(parent=self)
        i = self.tabs.addTab(terminal, FigIcon("launcher/bash.png"), "\tTerminal")
        self.tabs.setCurrentIndex(i)

    def addNewFileViewer(self):
        fileViewer = FigFileViewer(parent=self)
        i = self.tabs.addTab(fileViewer, "\tpath")
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


class FigApp(QApplication):
    def __init__(self, argv, 
                 x=100, y=100, w=1050, h=850, 
                 theme=None, icon="logo.png", 
                 *args, **kwargs):
        super(FigApp, self).__init__(argv)
        self.setApplicationName("Fig: any Format Is Good enough")
        fontId1 = QFontDatabase.addApplicationFont(__font__("OMORI_GAME.ttf"))
        fontId2 = QFontDatabase.addApplicationFont(__font__("OMORI_GAME2.ttf"))
        if fontId1 >= 0:
            families = QFontDatabase.applicationFontFamilies(fontId1)
        if fontId2 >= 0:
            families = QFontDatabase.applicationFontFamilies(fontId2)
            # self.window.fig_launcher.setFont(QFont(families[0], 20))
        self.window = FigWindow(*args, **kwargs)
        self.window.setGeometry(x, y, w, h)
        self.setWindowIcon(QIcon(icon))
        if fontId1 < 0:
            self.window.logger.error("unable to load OMORI_GAME.ttf")
        else:
            self.window.logger.debug("loaded OMORI_GAME.ttf successfully")
        if fontId2 < 0:
            self.window.logger.error("unable to load OMORI_GAME2.ttf")
        else:
            self.window.logger.debug("loaded OMORI_GAME2.ttf successfully")

    def run(self):
        self.window.show()
        sys.exit(self.exec_())
        self.window.fig_launcher.gifBtn.thread.join()


if __name__ == "__main__":
    pass