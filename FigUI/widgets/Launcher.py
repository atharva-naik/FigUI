#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
from PIL import Image, ImageQt
import os, sys, glob, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QToolButton, QFileDialog, QScrollArea


__current_dir__ = os.path.dirname(os.path.realpath(__file__))
__icons__ = os.path.join(__current_dir__, "../assets/icons")
__fonts__ = os.path.join(__current_dir__, "../assets/fonts")
launcher_icons = glob.glob(os.path.join(__icons__, "launcher/*"))


class FigToolButton(QToolButton):
    def __init__(self, parent=None):
        super(FigToolButton, self).__init__(parent)

    def _animateMovie(self):
        import time
        while True:
            self._gifMovie.seek(self._gifIndex)
            pixmap = QPixmap.fromImage(ImageQt.ImageQt(self._gifMovie))
            self.setIcon(QIcon(pixmap))
            self.setIconSize(QSize(*self.size))
            time.sleep(self.rate/1000)
            self._gifIndex += 1
            self._gifIndex %= self._gifLength

    def setMovie(self, path, rate=100, size=(60,60)):
        import threading
        # self.setStyleSheet("background: color(0, 0, 0, 100)")
        self.size = size
        self.rate = rate
        self.thread = threading.Thread(target=self._animateMovie)
        self._gifIndex = 0
        self._gifMovie = Image.open(path)
        self._gifLength = self._gifMovie.n_frames
        self.thread.start()


class FigLauncher(QWidget):
    def __init__(self, parent=None, width=8, button_size=(100,100), icon_size=(60,60)):
        super(FigLauncher, self).__init__(parent)
        layout = QGridLayout()
        self.layout = QVBoxLayout(self)
        self.launcherWidget = QWidget()
        self.gifBtn = None
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i,path in enumerate(launcher_icons):
            name = pathlib.Path(path).stem
            ext = os.path.splitext(path)[1]
            
            launcherButton = FigToolButton(self) # QToolButton(self)
            launcherButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            launcherButton.setText(name)
            launcherButton.setMaximumSize(QSize(*button_size))
            
            if ext == ".gif":
                launcherButton.setMovie(path, size=icon_size)       
                self.giBtn = launcherButton
            else:
                launcherButton.setIcon(QIcon(path))
                launcherButton.setIconSize(QSize(*icon_size))
            launcherButton.setStyleSheet("background: #3a3d41; color: #ffffff;")
            if name == "browser":
                if parent: 
                    parent.logger.debug("connected browser launcher")
                launcherButton.clicked.connect(parent.addNewTab)
            elif name == "bash":
                if parent:
                    parent.logger.debug("connected terminal launcher")
                launcherButton.clicked.connect(parent.addNewTerm)
            elif name == "fileviewer":
                if parent:
                    parent.logger.debug("connected terminal launcher")
                launcherButton.clicked.connect(parent.addNewFileViewer)
            else:
                if parent:
                    parent.logger.debug(f"connected FigHandler instance to '{name}' button")
                    launcherButton.clicked.connect(parent.addNewHandlerTab)
            layout.addWidget(launcherButton, i // width, i % width)
            launcherButton.clicked.connect(self._clickHandler)
        
        self.launcherWidget.setLayout(layout)
        self.scroll.setWidget(self.launcherWidget) # comment
        
        self.welcomeLabel = QPushButton("Welcome to FIG, launch an app!")
        figLogo = QIcon("logo.png")
        self.welcomeLabel.setIcon(figLogo)
        self.welcomeLabel.setStyleSheet("background: transparent; color: #734494")
        self.welcomeLabel.setIconSize(QSize(100,100))
        self.welcomeLabel.setMaximumWidth(800)
        self.welcomeLabel.setFont(QFont('OMORI_GAME2', 40))

        self.layout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        # self.layout.addWidget(self.launcherWidget) 
        self.layout.addWidget(self.scroll) # comment
        self.setLayout(self.layout)

    def _clickHandler(self, event):
        pass