#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os, sys, math
from jinja2 import Template
# import mimetypes, platform
from colormap import hex2rgb
import json, datetime, pathlib
# import psutil, webbrowser, threading
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QThread, QUrl, pyqtSignal, pyqtSlot, QObject, QTimer, QPoint, QRect, QSize, Qt, QT_VERSION_STR
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QPainter, QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QTextEdit, QScrollArea, QLabel, QSizePolicy, QGraphicsDropShadowEffect, QTabBar, QTabWidget, QToolButton, QToolBar


class FtNS(argparse.Namespace):
    def __init__(self):
        super(FtNS, self).__init__()
        self._dir = os.path.dirname(
            os.path.realpath(__file__)
        )
        self._static = os.path.join(self._dir, "static")
        # self._BG = f'''url('{os.path.join(self._static, "bg_texture.png")}')'''
        self._BG = "url('/home/atharva/GUI/FigUI/FigUI/FigTerminal/static/bg_texture.png');"
        self._template_path = os.path.join(self._static, "terminal.html")
        self._params = {
            "QWEBCHANNEL_JS" : self.url("qwebchannel.js"),
        }
        with open(self._template_path) as f:    
            self._template = Template(f.read())
        self._rendered_path = os.path.join(self._static, "terminal_rendered.html")
        with open(self._rendered_path, "w") as f:
            f.write(self._template.render(**self._params))
        self._URL = QUrl.fromLocalFile(self._rendered_path)
        self._MINH = 25
        self._MAXH = 100
        self._CLHEX = "#0fe7ff" # "#a4ab1a" # "#fc6b03" # "#89ff69" 
        self._CDHEX = "#f792e8" # "#8c834f" # "#8f3b17" # "#207869"
        self._SCHEX = "#0fe7ff" # "#a4ab1a" # "#fc6b03" # "#89ff69"
        self._HCHEX = "#f792e8" # "#8c834f" # "#8f3b17" # "#207869"
        self._CLRGB = hex2rgb(self._CLHEX)
        self._CDRGB = hex2rgb(self._CDHEX)
        self._SCRGB = hex2rgb(self._SCHEX)
        self._HCRGB = hex2rgb(self._HCHEX)
        self._TAB_PREFIX = "\t"*4

    def url(self, path):
        static_path = os.path.join(self._static, path)
        return QUrl.fromLocalFile(static_path).toString()

    def __call__(self, prop: "str"):
        return getattr(self, prop)

    def Icon(self, path: str):
        path = os.path.join(self._static, path)
        icon = QIcon(path)
 
        return icon

    @property
    def BG(self):
        return self._BG

    @BG.setter
    def BG(self, v):
        '''make background attr. protected.'''
        pass

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, v):
        pass

    @property
    def MAXH(self):
        return self._MAXH

    @MAXH.setter
    def MAXH(self, v):
        pass

    @property
    def MINH(self):
        return self._MINH

    @MINH.setter
    def MINH(self, v):
        pass

    @property
    def CLHEX(self):
        return self._CLHEX

    @CLHEX.setter
    def CLHEX(self, v):
        pass

    @property
    def CLRGB(self):
        return self._CLRGB

    @CLRGB.setter
    def CLRGB(self, v):
        pass

    @property
    def CDHEX(self):
        return self._CDHEX

    @CDHEX.setter
    def CDHEX(self, v):
        pass

    @property
    def CDRGB(self):
        return self._CDRGB

    @CDRGB.setter
    def CDRGB(self, v):
        pass

    @property
    def SCHEX(self):
        return self._SCHEX

    @SCHEX.setter
    def SCHEX(self, v):
        pass

    @property
    def SCRGB(self):
        return self._SCRGB

    @SCRGB.setter
    def SCRGB(self, v):
        pass

    @property
    def HCHEX(self):
        return self._HCHEX

    @HCHEX.setter
    def HCHEX(self, v):
        pass

    @property
    def HCRGB(self):
        return self._HCRGB

    @HCRGB.setter
    def HCRGB(self, v):
        pass

    @property
    def TAB_PREFIX(self):
        return self._TAB_PREFIX

    @TAB_PREFIX.setter
    def TAB_PREFIX(self, v):
        pass
Ft = FtNS()

class TermChannel(QObject):
    def __init__(self, web_view=None):
        super(TermChannel, self).__init__()
        self._web_view = web_view
        self._tab_widget = None

    def setTabs(self, tab_widget: QTabWidget):
        self._tab_widget = tab_widget

    @pyqtSlot(str)
    def sendTitle(self, title: str):
        '''update title of QTabWidget.'''
        if self._tab_widget:
            i = self._tab_widget.currentIndex()
            self._tab_widget.setTabText(i, Ft.TAB_PREFIX+title)


class FigTermView(QWebEngineView):
    def __init__(self, parent=None, tab_widget=None):
        super(FigTermView, self).__init__(parent)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
        self.backend = TermChannel(web_view=self) 
        if tab_widget: self.backend.setTabs(tab_widget)
        self.channel.registerObject("backend", self.backend)
        self.load(Ft.URL)
        self.setZoomFactor(1.35)


class FigTerminal(QMainWindow):
    def __init__(self, icon="terminal.svg"):
        super(FigTerminal, self).__init__()
        self.setWindowIcon(Ft.Icon(icon))
        centralWidget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.ribbon_visible = True
        self.titleBar = self.initTitleBar()
        layout.addWidget(self.titleBar)
        self.mainMenu = self.initMainMenu()
        layout.addWidget(self.mainMenu)
        self.termWidget = self.initTermWidget()
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setWidget(self.termWidget)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # layout.addWidget(self.scrollArea)
        layout.addWidget(self.termWidget)
        centralWidget.setLayout(layout)
        centralWidget.setStyleSheet('''
        QWidget {
            color: #fff;
            background: #000;
        }''')
        self.setGeometry(200, 200, 1000, 600)
        self.setCentralWidget(centralWidget)
        self.hideRibbon()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.addToolBar(Qt.TopToolBarArea, self.titleBar)
    # def addNewTab(self):
    #     '''Add new terminal widget'''
    #     terminal = FigTermView(parent=self)
    #     i = self.tabs.addTab(terminal, "\tNew Tab")
    #     self.tabs.setCurrentIndex(i)
    #     self.tabs.tabBar().setExpanding(True)
    #     self.tabs.setTabToolTip(i, "New Tab")
    def onCurrentTabChange(self, i):
        '''when tab is changed.'''
        if i == self.tabs.count()-1 and self.plusClickedFlag:
            terminal = FigTermView(parent=self, tab_widget=self.tabs)
            self.tabs.insertTab(i, terminal, Ft.TAB_PREFIX+f"Terminal {i}")
            self.tabs.setCurrentIndex(i)

    def onCurrentTabClose(self, i):
        '''when tab is closed'''
        # print("i=", i, "count=", 
        #        self.tabs.count())
		# if there is only one tab, do nothing
        if self.tabs.count() <= 1: return 
        # else remove the tab
        self.tabs.setCurrentIndex(i-1)
        self.tabs.removeTab(i) 
    # @property
    # def plusBtn(self):
    #     '''plus button: for adding new tabs.'''
    #     plusBtn = QToolButton(self)
    #     plusBtn.clicked.connect(self.addNewTab)
    #     plusBtn.setIcon(Ft.Icon("plus.svg"))
    #     plusBtn.setIconSize(QSize(18,18))
    #     plusBtn.setStyleSheet('''
    #     QToolButton {
    #         border: 0px;
    #         background: transparent;
    #     }''')
    #     return plusBtn
    def initTermWidget(self):
        # tab widget for terminal.
        self.i = -1
        self.tabs = QTabWidget() 
        # self.tabs.tabBarDoubleClicked.connect(self.addNewTab)
        self.tabs.setTabsClosable(True) 	
        self.tabs.tabCloseRequested.connect(self.onCurrentTabClose) # adding action when tab close is requested
        self.tabs.setStyleSheet('''
        QTabWidget {
            background: #000; /* rgba(29, 29, 29, 0.95); */
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
            background: url("/home/atharva/GUI/FigUI/FigUI/FigTerminal/static/close-tab.svg");
            background-repeat: no-repeat;
            background-position: center;
            subcontrol-position: right;
            border-radius: 12px;
        }
        QTabBar::close-button:hover {
            color: #fff;
            background: url("/home/atharva/GUI/FigUI/FigUI/FigTerminal/static/close-tab-hover.svg");
            background-repeat: no-repeat;
            background-position: center;
            background-color: rgba(235, 235, 235, 0.50);
        }
        QTabBar::tab {
            color: #fff;
            border: 0px;
            margin: 0px;
            font-size: 16px;
            background: #000;
        }
        QTabBar::tab:hover {
            background: '''+ Ft.CLHEX +''';
            color: #292929;
        }
        QTabBar::tab:selected {
            color: #292929;
            font-weight: bold;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 2, y2 : 2, stop : 0.0 '''+Ft.CLHEX+''', stop : 0.4 '''+Ft.CDHEX+''');
        }''') # TODO: theme
        terminal = FigTermView(parent=self, tab_widget=self.tabs)
        self.tabs.setUpdatesEnabled(True)
        self.tabs.insertTab(0, terminal, "\t\t\t\tHome\t\t\t\t")
        self.tabs.setCurrentIndex(0)
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None) 
        self.tabs.tabBar().setExpanding(True)
        self.tabs.setTabToolTip(0, "Terminal")
        i = self.tabs.insertTab(1, QWidget(), "\t")
        self.plusClickedFlag = False
        self.plusBtn = QToolButton(self)
        self.plusBtn.clicked.connect(self.plusBtnClicked)
        self.plusBtn.setIcon(Ft.Icon("plus.svg"))
        self.plusBtn.setIconSize(QSize(18,18))
        self.plusBtn.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')
        self.tabs.tabBar().setTabButton(1, QTabBar.RightSide, self.plusBtn)
        self.tabs.currentChanged.connect(self.onCurrentTabChange)

        return self.tabs

    def plusBtnClicked(self):
        self.plusClickedFlag = True
        self.tabs.setCurrentIndex(self.tabs.count()-1)
        self.plusClickedFlag = False

    def initFileMenu(self):
        fileMenu = QWidget()
        return fileMenu

    def initEditMenu(self):
        editMenu = QWidget()
        return editMenu

    def initViewMenu(self):
        viewMenu = QWidget()
        return viewMenu

    def initSearchMenu(self):
        searchMenu = QWidget()
        return searchMenu

    def hideRibbon(self):
        if self.ribbon_visible:
            self.mainMenu.setFixedHeight(Ft.MINH)
            self.hideBtn.setIcon(Ft.Icon("show_ribbon.svg"))
        else:
            self.mainMenu.setFixedHeight(Ft.MAXH)
            self.hideBtn.setIcon(Ft.Icon("hide_ribbon.svg"))
        self.ribbon_visible = not(self.ribbon_visible)

    def maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def initMainMenu(self):
        '''create main menu for file browser.'''
        tb = "\t"*4
        mainMenu = QTabWidget()
        self.fileMenu = self.initFileMenu()
        mainMenu.addTab(self.fileMenu, tb+"File"+tb)
        self.editMenu = self.initFileMenu()
        mainMenu.addTab(self.editMenu, tb+"Edit"+tb)
        self.viewMenu = self.initFileMenu()
        mainMenu.addTab(self.viewMenu, tb+"View"+tb)
        self.searchMenu = self.initFileMenu()
        mainMenu.addTab(self.searchMenu, tb+"Search"+tb)
        # hide the ribbon.
        self.hideBtn = QToolButton(mainMenu)
        self.hideBtn.clicked.connect(self.hideRibbon)
        self.hideBtn.setIcon(Ft.Icon("hide_ribbon.svg"))
        self.hideBtn.setIconSize(QSize(18,18))
        self.hideBtn.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')

        mainMenu.addTab(QWidget(), "")
        mainMenu.tabBar().setTabButton(4, QTabBar.RightSide, self.hideBtn)

        mainMenu.setCurrentIndex(0)
        glowEffect = QGraphicsDropShadowEffect()
        glowEffect.setBlurRadius(50)
        glowEffect.setOffset(30,0)
        glowEffect.setColor(QColor(*Ft.CDRGB))
        mainMenu.setGraphicsEffect(glowEffect)
        mainMenu.setMaximumHeight(Ft.MAXH)
        mainMenu.setStyleSheet('''
        QTabWidget {
            background:'''+Ft.BG+'''
            color: #000;
            border: 0px;
        }
        QTabWidget::pane {
            background:'''+Ft.BG+'''
            border: 0px;
        }
        QTabBar {
            background:'''+Ft.BG+'''
            border: 0px;
        }
        QWidget {
            background:'''+Ft.BG+'''
        }
        QTabBar::tab {
            color: #fff;
            border: 0px;
            font-size: 15px;
            font-weight: bold;
            background: #292929;
        }
        QTabBar::tab:hover {
            background: '''+ Ft.CLHEX +''';
            color: #292929;
        }
        QTabBar::tab:selected {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Ft.CDHEX+''', stop : 0.99 '''+Ft.CLHEX+'''); 
            font-weight: bold;
            color: #292929;
        }
        QToolTip { 
            color: #fff;
            border: 0px;
        }
        QToolButton {
            border: 0px;
            font-size: 13px;
            background: transparent;
            color: #fff;
        }
        QToolButton:hover {
            border: 0px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Ft.CDHEX+''', stop : 0.99 '''+Ft.CLHEX+'''); 
        }
        QLabel { 
            color: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 '''+Ft.CDHEX+''', stop : 0.99 '''+Ft.CLHEX+''');
            font-size: 14px;
        }''')

        return mainMenu

    def initTitleBar(self):
        toolbar = QToolBar("Title Bar Visibility")
        toolbar.setStyleSheet('''
        QToolBar {
            margin: 0px; 
            border: 0px; 
            color: #fff;
            /* border-top-left-radius: 12px;
            border-top-right-radius: 12px; */
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
        closeBtn.setIcon(Ft.Icon("close.svg")) 
        closeBtn.setStyleSheet(ctrlBtnStyle)
        closeBtn.clicked.connect(lambda: self.close()) # closing logic.
        self.closeBtn = closeBtn

        minimizeBtn = QToolButton(self)
        minimizeBtn.setToolTip("minimize window")
        minimizeBtn.setIcon(Ft.Icon("minimize.svg"))
        minimizeBtn.clicked.connect(lambda: self.showMinimized())
        minimizeBtn.setStyleSheet(ctrlBtnStyle)
        self.minimizeBtn = minimizeBtn

        maximizeBtn = QToolButton(self)
        maximizeBtn.setToolTip("maximize window")
        maximizeBtn.setIcon(Ft.Icon("maximize.svg"))
        maximizeBtn.clicked.connect(lambda: self.maximize())
        maximizeBtn.setStyleSheet(ctrlBtnStyle)
        self.maximizeBtn = maximizeBtn
        windowTitle = QLabel()
        windowTitle.setText("") # ("𝔽𝕚𝕘 𝕀𝕤 𝕒 𝔾𝕦𝕚") #("𝗙ig 𝗜s a 𝗚UI")
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


def main(argv):
    icon = "/home/atharva/GUI/FigUI/logo.png"
    app = QApplication(argv)
    app.setCursorFlashTime(100)
    app.setObjectName("FigTerminal")
    app.setApplicationDisplayName("Fig — Terminal")
    figTerm = FigTerminal()
    figTerm.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main(sys.argv)