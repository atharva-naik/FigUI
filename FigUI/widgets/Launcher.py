#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
import os, sys, glob, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence, QTransform
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QToolButton


__current_dir__ = os.path.dirname(os.path.realpath(__file__))
__icons__ = os.path.join(__current_dir__, "../assets/icons")
launcher_icons = glob.glob(os.path.join(__icons__, "launcher/*"))


class FigLauncher(QWidget):
    def __init__(self, parent=None, width=8, button_size=(100,100), icon_size=(60,60)):
        super(FigLauncher, self).__init__(parent)
        self.layout = QGridLayout()
        for i,path in enumerate(launcher_icons):
            name = pathlib.Path(path).stem
            launcherButton = QToolButton(self)
            launcherButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            launcherButton.setIcon(QIcon(path))
            launcherButton.setText(name)
            launcherButton.setIconSize(QSize(*icon_size))
            launcherButton.setMaximumSize(QSize(*button_size))
            launcherButton.setStyleSheet("background: #3a3d41; color: #ffffff;")
            if name == "browser":
                if parent: 
                    parent.logger.debug("connected browser launcher")
                launcherButton.clicked.connect(parent.addNewTab)
            elif name == "bash":
                if parent:
                    parent.logger.debug("connected terminal launcher")
                launcherButton.clicked.connect(parent.addNewTerm)
            self.layout.addWidget(launcherButton, i // width, i % width)
            launcherButton.clicked.connect(self._clickHandler)
        self.setLayout(self.layout)

    def _clickHandler(self, event):
        pass