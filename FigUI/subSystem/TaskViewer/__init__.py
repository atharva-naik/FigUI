#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
import os, sys, pathlib
from jinja2 import Template
from typing import Union, List
# from PIL import Image, ImageQt
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QVariant, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy


def static(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)

    return path


class TabIndexChannel(QObject):
    def __init__(self, parent=None):
        # make sure that the parent is the FigWindow.
        super(TabIndexChannel, self).__init__()
        self.i = 0 # index of chosen tab.
        self.parent = parent

    @pyqtSlot(int)
    def sendCursorPos(self, i: int):
        if self.parent and isinstance(self.parent, QMainWindow):
            self.parent.tabs.setCurrentIndex(i)
            self.i = i 


class FigTaskWebView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(FigTaskWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
        self.cursorHandler = TabIndexChannel(parent=parent) 
        self.channel.registerObject("backend", self.cursorHandler)
        # load template.
        template = Template(open(
            static("view.html")
        ).read())
        params = {
            "CAROUSEL_JS": static("carousel.js"),
            "QWEBCHANNEL_JS": static("qwebchannel.js"),
            "NUM_TABS": parent.tabs.count() if parent else 0,
        }
        # render template and write to disk.
        open(
            static("view_rendered.html"), 
        "w").write(
            template.render(**params)
        )
        self.load(QUrl.fromLocalFile(static("view_rendered.html")))

    def dragEnterEvent(self, e):
        e.ignore()

    def dropEvent(self, e):
        e.ignore()

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.popup(event.globalPos())
        # self.menu.addAction('Refactor')
    def execJS(self, script, callback=None):
        if callback:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script, callback))
        else:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script))

    def alert(self, message):
        self.execJS(f"alert('{message}')")


if __name__ == '__main__':
    pass