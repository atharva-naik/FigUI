# json file reading widget.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, logging, datetime, pathlib
from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QThread, QUrl, QTimer, QPoint, QRegExp, QSize, Qt, QT_VERSION_STR
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QSizePolicy, QTabBar, QLabel, QToolButton


class FigJsonReader(QWidget):
    def __init__(self, parent=None):
        super(FigJsonReader, self).__init__(parent)
        self._parent = parent


if __name__ == '__main__':
    pass