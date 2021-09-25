#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
for managing activites such as open tabs, notifications etc.
'''
import typing
import PyQt5, re
import tempfile, random
import textwrap, subprocess
import os, sys, glob, pathlib
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit, QFrame, QSizePolicy


class FigLinker:
    '''A class to bundle path completion resources for fig'''
    def __init__(self, rel_path="../assets"):
        self.rel_path = rel_path
        self.rel_font_path = os.path.join(rel_path, "fonts")
        self.rel_icon_path = os.path.join(rel_path, "icons")
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.abs_path = os.path.join(self.current_dir, self.rel_path)
        self.abs_font_path = os.path.join(self.current_dir, self.rel_font_path)
        self.abs_icon_path = os.path.join(self.current_dir, self.rel_icon_path)

    def icon(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_icon_path, path)

    def font(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_font_path, path)

    def asset(self, path: str) -> str:
        '''return absolute path of an asset'''
        return os.path.join(self.abs_path, path)

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
# def FigIcon(name, w=None, h=None):
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     __icons__ = os.path.join(__current_dir__, "../assets/icons")
#     path = os.path.join(__icons__, name)

#     return QIcon(path)

# def FigFont(name):
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     __icons__ = os.path.join(__current_dir__, "../assets/fonts")
#     path = os.path.join(__icons__, name)

#     return QFont(path)

# def __font__(name):
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     __icons__ = os.path.join(__current_dir__, "../assets/fonts")
#     path = os.path.join(__icons__, name)

#     return path

# def __icon__(name):
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     __icons__ = os.path.join(__current_dir__, "../assets/icons")
#     path = os.path.join(__icons__, name)

#     return path

# def __asset__(name):
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     __assets__ = os.path.join(__current_dir__, "../assets")
#     path = os.path.join(__assets__, name)

#     return path
class FigActivityPanel(QWidget):
    def __init__(self, parent=None):
        super(FigActivityPanel, self).__init__(parent)
        # asset linker.
        self.linker = FigLinker()
        # create navbar.
        self.navbar = self.initNavBar()
        # create vertical layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch(True)

        '''since insertWidget is used, add widgets in reverse order of what you usually do.'''
        # add navbar to layout.
        layout.insertWidget(0, self.navbar)

        # set style
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

        # set the layout.
        self.setLayout(layout)
        self.is_visible = False
        self.hide()
        self._parent = parent

    def toggle(self):
        # print(self._parent)
        if not self.is_visible:
            self.show()
            self.resize(QSize(300,700))
            # self.setSize()
        else:
            self.hide()
        self.is_visible = not self.is_visible

    def initNavBar(self, icon_size=(20,20)):
        navbar = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # left spacer
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(left_spacer)
        # notifications tab
        notifsBtn = QToolButton(self)
        # print(self.linker.icon("activity/notifs.svg"))
        notifsBtn.setIcon(self.linker.FigIcon("activity/notifs.svg"))
        notifsBtn.setIconSize(QSize(*icon_size))
        layout.addWidget(notifsBtn) 
        # open tabs
        tabsBtn = QToolButton(self)
        tabsBtn.setIcon(self.linker.FigIcon("activity/tabs.svg"))
        tabsBtn.setIconSize(QSize(*icon_size))
        layout.addWidget(tabsBtn) 
        # history (do I need ?)
        histBtn = QToolButton(self)
        histBtn.setIcon(self.linker.FigIcon("activity/history.svg"))
        histBtn.setIconSize(QSize(*icon_size))
        layout.addWidget(histBtn) 
        # # notifications tab
        # notifsBtn = QToolButton(self)
        # notifsBtn.setIcon(self.linker.FigIcon("activity/notifs.svg"))
        # notifsBtn.setIconSize(QSize(25,25))
        # layout.addWidget(notifsBtn)
        # right spacer
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(right_spacer) 
        navbar.setLayout(layout)

        return navbar