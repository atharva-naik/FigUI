#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# GUI frontend that uses python-apt bindings to communicate with apt.
try:
    import apt
except ImportError:
    print("python-apt not installed, you are likely on a non Debian OS")

import os, sys 
import pathlib
import datetime 
# from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QTabBar


class AptBackend:
    def __init__(self):
        self.cache = apt.cache.Cache()
        self.cache.update()
        self.cache.open()

    def is_installed(self, pkg_name):
        '''check if a package is installed.'''
        pkg = self.cache[pkg_name]
        return pkg.is_installed

    def install(self, pkg_name):
        '''Boolean return value. True returned in package is succesfully installed else False (when installation fails).'''
        pkg = self.cache[pkg_name]
        if pkg.is_installed: return True
        else:
            pkg.mark_install()
            try:
                self.cache.commit()
                return True
            except Exception as e: return False


class AptFrontend:
    def __init__(self):
        pass
    

if __name__ == '__main__':
    pass