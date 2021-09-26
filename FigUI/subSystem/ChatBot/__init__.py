#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Chat'''
import PyQt5
import typing
import os, re, sys
import glob, pathlib
# import tempfile, random
from jinja2 import Template
# import textwrap, subprocess
# from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings#, QWebChannel
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit, QFrame, QSizePolicy
try:
    from .assets.Linker import FigLinker
    from AgentWindow import FigAgentWindow
except ImportError:
    from FigUI.assets.Linker import FigLinker
    from FigUI.subSystem.ChatBot.AgentWindow import FigAgentWindow

class BotWebView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(BotWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # self.channel = QWebChannel()
        # self.page().setWebChannel(self.channel)
        self.linker = FigLinker(__file__)
        self.setMinimumHeight(700)
        ### views
        ## 1. Analog Clock
        ## 2. Stop Watch
        # self.sources = {
        #     "AnalogClock": {
        #         "index": self.linker.static("clock.html"),
        #         "params": {},
        #         "rendered": self.linker.static("clock_rendered.html"),
        #         "url": self.linker.staticUrl("clock_rendered.html"),
        #     },
        #     "Timer": {
        #         "index": self.linker.static("timer.html"),
        #         "params": {
        #             "TIMER_JS": self.linker.staticUrl("timer.js").toString(),
        #             "TIMER_CSS": self.linker.staticUrl("timer.css").toString(),
        #             "JQUERY_JS": self.linker.staticUrl("jquery.js").toString(),
        #             "JQUERY_MOUSEWHEEL_JS": self.linker.staticUrl("jquery.mousewheel.min.js").toString(),
        #         },
        #         "rendered": self.linker.static("timer_rendered.html"),
        #         "url": self.linker.staticUrl("timer_rendered.html"),
        #     } 
        # }
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
        super(BotWebView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Change Sprite')
        self.menu.popup(event.globalPos())

    def execJS(self, script, callback=None):
        if callback:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script, callback))
        else:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script))

    def update(self, widget):
        pass

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class FigChatBot(QWidget):
    def __init__(self, parent=None):
        super(FigChatBot, self).__init__(parent)
        # create layout.
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        # layout.addStretch(True)
        # # bot web view.
        # self.botView = BotWebView(self)
        # agent window
        self.agentWindow = FigAgentWindow(parent=self)
        # # chat layout
        # self.chatLayout = FigChatLayout(parent=self)
        # add widget to layout.
        layout.addWidget(self.agentWindow)
        # set layout.
        self.setLayout(layout)