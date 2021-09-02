#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
import textwrap, subprocess
import os, sys, glob, pathlib
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QToolButton


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

def __icon__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return path

def __font__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/fonts")
    path = os.path.join(__icons__, name)

    return path


class FigFileIcon(QToolButton):
    def __init__(self, path, parent=None, size=(100,120), textwidth=10):
        super(FigFileIcon, self).__init__(parent)
        self.name = pathlib.Path(path).name
        self.path = path
        self.isfile = os.path.isfile(path)
        self.stem = pathlib.Path(path).stem
        self.setStyleSheet("background-color: #292929; border: 0px")
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        text = "\n".join(textwrap.wrap(self.name[:textwidth*3], width=textwidth))
        self.setText(text) # truncate at 3 times the max textwidth
        self.setMaximumSize(QSize(*size))
        self.setIconSize(QSize(size[0]-40, size[1]-40))
        self._setThumbnail()

    def _setThumbnail(self):
        _,ext = os.path.splitext(self.name)
        # print(self.name, self.stem, ext, os.path.isfile(self.path))
        ext = ext[1:]
        if self.name == ".git":
            self.setIcon(FigIcon("launcher/git.png"))
            return
        elif not self.isfile:
            self.setIcon(FigIcon("launcher/fileviewer.png"))
            return
        elif ext in ["png","jpg"]:
            self.setIcon(QIcon(self.path))
            return
        elif self.stem == "README":
            self.setIcon(FigIcon("launcher/README.png"))
            return
        elif self.stem == "requirements":
            self.setIcon(FigIcon("launcher/requirements.png"))
            return
        elif self.stem.lower() == "license":
            self.setIcon(FigIcon("launcher/license.png"))
            return      
        elif self.stem == ".gitignore":
            self.setIcon(FigIcon("launcher/gitignore.png"))
            return
        elif ext == "":
            if subprocess.getoutput(f"file --mime-encoding {self.path}").endswith("binary"):
                self.setIcon(FigIcon("launcher/bin.png"))    
            else:
                self.setIcon(FigIcon("launcher/txt.png"))
            return

        if os.path.exists(__icon__(f"launcher/{ext}.png")): # check if png file for the ext
            self.setIcon(FigIcon(f"launcher/{ext}.png"))
        else:
            if os.path.exists(__icon__(f"launcher/{ext}.svg")): 
                self.setIcon(FigIcon(f"launcher/{ext}.svg")) # check if svg file exists for the ext
            else: 
                print(self.name)
                self.setIcon(FigIcon(f"launcher/txt.png")) # if ext is not recognized set it to txt
    # def _animateMovie(self):
    #     import time
    #     while True:
    #         self._gifMovie.seek(self._gifIndex)
    #         pixmap = QPixmap.fromImage(ImageQt.ImageQt(self._gifMovie))
    #         self.setIcon(QIcon(pixmap))
    #         self.setIconSize(QSize(*self.size))
    #         time.sleep(self.rate/1000)
    #         self._gifIndex += 1
    #         self._gifIndex %= self._gifLength

    # def setMovie(self, path, rate=100, size=(60,60)):
    #     import threading
    #     self.size = size
    #     self.rate = rate
    #     self.thread = threading.Thread(target=self._animateMovie)
    #     self._gifIndex = 0
    #     self._gifMovie = Image.open(path)
    #     self._gifLength = self._gifMovie.n_frames
    #     self.thread.start()
class FigFileViewer(QWidget):
    def __init__(self, path="/home/atharva/GUI/FigUI", parent=None, width=6, button_size=(100,100), icon_size=(60,60)):
        super(FigFileViewer, self).__init__(parent)   
        all_files = [os.path.join(path, file) for file in os.listdir(path)] # get list of all files and folders.

        self.gridLayout = QGridLayout()
        self.layout = QVBoxLayout(self)
        self.viewer = QWidget()

        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // width, i % width)        
        self.viewer.setLayout(self.gridLayout)
        # self.layout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.viewer)
        self.setLayout(self.layout)
        self.width = width

    def clear(self):
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)

    def open(self):
        sendingBtn = self.sender()
        if not sendingBtn.isfile:
            path = sendingBtn.path
            self.clear()
            all_files = [os.path.join(path, file) for file in os.listdir(path)] # get list of all files and folders.
            for i,path in enumerate(all_files):
                fileIcon = FigFileIcon(path, parent=self)
                fileIcon.clicked.connect(self.open)
                self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
        else:
            # call file handler for the extension here
            pass

if __name__ == "__main__":
    FigFileViewer("/home/atharva/GUI/FigUI")