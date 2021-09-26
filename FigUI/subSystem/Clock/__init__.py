#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Clock display: Analog + Digital'''
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
# try:
#     from .assets.Linker import FigLinker
# except ImportError:
#     from FigUI.assets.Linker import FigLinker
class FigLinker:
    '''A class to bundle path completion resources for fig'''
    def __init__(self, rel_path="../assets", static_path="static"):
        self.rel_path = rel_path
        self.static_path = static_path
        self.rel_font_path = os.path.join(rel_path, "fonts")
        self.rel_icon_path = os.path.join(rel_path, "icons")
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.abs_path = os.path.join(self.current_dir, self.rel_path)
        self.abs_font_path = os.path.join(self.current_dir, self.rel_font_path)
        self.abs_icon_path = os.path.join(self.current_dir, self.rel_icon_path)
        self.abs_static_path = os.path.join(self.current_dir, self.static_path)

    def icon(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_icon_path, path)

    def font(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_font_path, path)

    def asset(self, path: str) -> str:
        '''return absolute path of an asset'''
        return os.path.join(self.abs_path, path)

    def static(self, path: str) -> str:
        '''give relative path and get absolute static path.'''
        return os.path.join(self.abs_static_path, path)

    def staticUrl(self, path: str) -> QUrl:
        '''local url given static path'''
        filePath = self.static(path)

        return QUrl.fromLocalFile(filePath)

    def FigIcon(self, name:str) -> QIcon :
        '''return QIcon'''
        icon_path = self.icon(name)
        icon = QIcon(icon_path)
        # if w is not None:
        #     if h is not None:
        #         size = QSize(w, h) 
        #     else:
        #         size = QSize(w, w)
        #     icon.set
        # else:
        return icon

    def FigFont(self, name: str) -> QFont :
        '''return QFont'''
        font_path = self.icon(name)
        font = QFont(font_path)

        return font


class ClockWebView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(ClockWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # self.channel = QWebChannel()
        # self.page().setWebChannel(self.channel)
        self.linker = FigLinker("../assets", static_path="static")
        self.setMinimumHeight(500)
        ### views
        ## 1. Analog Clock
        ## 2. Stop Watch
        self.sources = {
            "AnalogClock": {
                "index": self.linker.static("clock.html"),
                "params": {},
                "rendered": self.linker.static("clock_rendered.html"),
                "url": self.linker.staticUrl("clock_rendered.html"),
            },
            "Timer": {
                "index": self.linker.static("timer.html"),
                "params": {
                    "TIMER_JS": self.linker.staticUrl("timer.js").toString(),
                    "TIMER_CSS": self.linker.staticUrl("timer.css").toString(),
                    "JQUERY_JS": self.linker.staticUrl("jquery.js").toString(),
                    "JQUERY_MOUSEWHEEL_JS": self.linker.staticUrl("jquery.mousewheel.min.js").toString(),
                },
                "rendered": self.linker.static("timer_rendered.html"),
                "url": self.linker.staticUrl("timer_rendered.html"),
            } 
        }

        # NOTE: get parent (CodeEditor) 
        # self.cursorHandler = CursorPosHandler(parent=parent) 
        # self.channel.registerObject("backend", self.cursorHandler)
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
        super(ClockWebView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        # self.menu.addAction('')
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

    def Load(self, app_name):
        # load analog clock
        app = self.sources.get(app_name)
        if not app: return
        # load index
        index = app.get("index")
        if not index: return
        template = Template(open(index).read())
        # load parameters
        params = app.get("params", {})
        # render template and save to static
        rendered = app.get("rendered")
        if not rendered: return 
        open(rendered, "w").write(template.render(**params))
        # load url of rendered template
        url = app.get("url")
        if not url: return
        self.load(url)

    def showAnalogClock(self):
        self.Load("AnalogClock")

    def showStopWatch(self):
        self.Load("StopWatch")

    def showTimer(self):
        self.Load("Timer")


class FigClock(QWidget):
    def __init__(self, parent=None):
        super(FigClock, self).__init__(parent)
        # create linker for asset loading
        self.linker = FigLinker("../../assets")
        # vertical layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch(True)
        # create widgets
        self.clockView = ClockWebView(self)
        self.clockView.showAnalogClock()
        # set analog clock by default.
        self.clockBar = self.initClockBar()
        # add widgets to layout
        layout.insertWidget(0, self.clockBar)
        layout.insertWidget(0, self.clockView)
        # set style sheet
        self.setStyleSheet('''
            QToolBar { 
                background: #292929; 
                color: #292929; 
                border: 0px;
            } 
            QToolTip { border: 0px }
            QToolButton:hover { 
                background: red;
        }''')
        # set layout
        self.setLayout(layout)

    def initClockBar(self, icon_size=(20,20)):
        clockbar = QWidget()
        clockbar.setStyleSheet('''
            QWidget {
                background: #292929
            }
            QToolBar { 
                background: #292929; 
                color: #292929; 
                border: 0px;
            } 
            QToolTip { border: 0px }
            QToolButton:hover { 
                background: red;
        }''')
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # left spacer
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(left_spacer)
        # alarm utility
        alarmBtn = QToolButton(self)
        alarmBtn.setIcon(self.linker.FigIcon("clock/alarm.svg"))
        alarmBtn.setIconSize(QSize(*icon_size))
        alarmBtn.setToolTip("set alarm")
        layout.addWidget(alarmBtn) 
        # analog clock utility
        clockBtn = QToolButton(self)
        clockBtn.setIcon(self.linker.FigIcon("clock/clock.svg"))
        clockBtn.setIconSize(QSize(*icon_size))
        clockBtn.setToolTip("open analog clock")
        clockBtn.clicked.connect(self.clockView.showAnalogClock)
        layout.addWidget(clockBtn) 
        # stop watch utility
        stopWatchBtn = QToolButton(self)
        stopWatchBtn.setIcon(self.linker.FigIcon("clock/stopwatch.svg"))
        stopWatchBtn.setIconSize(QSize(*icon_size))
        stopWatchBtn.setToolTip("start stop watch")
        layout.addWidget(stopWatchBtn) 
        # timer utility
        timerBtn = QToolButton(self)
        timerBtn.setIcon(self.linker.FigIcon("clock/timer.svg"))
        timerBtn.setIconSize(QSize(*icon_size))
        timerBtn.setToolTip("set timer")
        timerBtn.clicked.connect(self.clockView.showTimer)
        layout.addWidget(timerBtn) 
        # time-zone conversion utility
        globeBtn = QToolButton(self)
        globeBtn.setIcon(self.linker.FigIcon("clock/time-zone-converter.svg"))
        globeBtn.setIconSize(QSize(*icon_size))
        globeBtn.setToolTip("open time-zone converter")
        layout.addWidget(globeBtn) 
        # right spacer
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(right_spacer) 
        # set layout
        clockbar.setLayout(layout)

        return clockbar


if __name__ == "__main__":
    pass