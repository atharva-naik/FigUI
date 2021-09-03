#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
import textwrap, subprocess
import os, sys, glob, pathlib
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit


def getWallpaper():
    import os
    import time
    import pathlib 
    import platform 
    import requests
    osname = platform.system()
    home = str(pathlib.Path.home())
    if osname == "Linux":
        wallpath = os.path.join(home, ".cache/wallpaper")
        wallpapers = os.listdir(wallpath)
        if len(wallpapers) > 0:
            return os.path.join(wallpath, wallpapers[0])
        else:
            img = requests.get("https://picsum.photos/1600/900").content
            fname = f"figui_wallpaper_{time.time()}.jpg"
            open(fname, "wb").write(img)

            return fname
    else:
        from wallpaper import get_wallpaper
        return get_wallpaper()

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
            if self.name == "Music":
                self.setIcon(FigIcon("launcher/Music.svg"))
            elif self.name == "Desktop":
                self.setIcon(FigIcon("launcher/Desktop.png"))
            else:    
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
                # print(self.name)
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
    def __init__(self, path=str(pathlib.Path.home()), parent=None, width=6, button_size=(100,100), icon_size=(60,60)):
        super(FigFileViewer, self).__init__(parent)   
        all_files = self.listFiles(path) # get list of all files and folders.
        self.path = path
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gridLayout = QGridLayout()
        self.layout = QVBoxLayout(self)
        self.viewer = QWidget()
        self.history = [path]
        self.i = 0
        self.j = 0
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // width, i % width)        
        self.viewer.setLayout(self.gridLayout)
        # self.layout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        self.scroll.setWidget(self.viewer)
        self.layout.addWidget(self.scroll)
        self.navbar = QWidget()
        navLayout = QHBoxLayout()
        
        backBtn = QToolButton()
        backBtn.setIcon(FigIcon("stepback.svg"))
        backBtn.clicked.connect(self.back)
        navLayout.addWidget(backBtn)
        
        prevBtn = QToolButton()
        prevBtn.setIcon(FigIcon("back.svg"))
        prevBtn.clicked.connect(self.prevPath)
        navLayout.addWidget(prevBtn)

        nextBtn = QToolButton()
        nextBtn.setIcon(FigIcon("forward.svg"))
        nextBtn.clicked.connect(self.nextPath)
        navLayout.addWidget(nextBtn)
        
        sortUpBtn = QToolButton()
        sortUpBtn.setIcon(FigIcon("sort_ascending.svg"))
        # sortUpBtn.clicked.connect(self.nextPath)
        navLayout.addWidget(sortUpBtn)

        sortDownBtn = QToolButton()
        sortDownBtn.setIcon(FigIcon("sort_descending.svg"))
        # sortUpBtn.clicked.connect(self.nextPath)
        navLayout.addWidget(sortDownBtn)

        searchBar = QLineEdit()
        searchBar.setStyleSheet("background: #fff; color: #000")
        navLayout.addWidget(searchBar)

        searchBtn = QToolButton()
        searchBtn.setIcon(FigIcon("search.svg"))
        navLayout.addWidget(searchBtn)

        # hideBtn = QToolButton()
        # hideBtn.setIcon(FigIcon("hide.svg"))
        # navLayout.addWidget(hideBtn)

        delBtn = QToolButton()
        delBtn.setIcon(FigIcon("delete.svg"))
        navLayout.addWidget(delBtn)

        self.navbar.setLayout(navLayout)    
        self.layout.addWidget(self.navbar)
        self.setLayout(self.layout)
        self.width = width
        selBtn = self.gridLayout.itemAt(0).widget()
        selBtn.setStyleSheet("background: color(0, 0, 255, 50)")
        self.highlight(0)

    def highlightOnClick(self):
        sendingBtn = self.sender()
        j = self.gridLayout.indexOf(sendingBtn)
        self.highlight(j)
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_A:
            j = max(self.j-1,0)
        elif e.key() == Qt.Key_D:
            j = min(self.gridLayout.count()-1,self.j+1)
        elif e.key() == Qt.Key_W:
            j = max(self.j-self.width,0)
        elif e.key() == Qt.Key_S:
            j = min(self.gridLayout.count()-1,self.j+self.width)
        elif e.key() == Qt.Key_Return:
            selBtn = self.gridLayout.itemAt(self.j).widget()
            path = selBtn.path
            self.openPath(path)
            return
        else:
            return
        self.highlight(j)

    def clear(self):
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)
        self.j = 0

    def highlight(self, j):
        selBtn = self.gridLayout.itemAt(self.j).widget()
        selBtn.setStyleSheet("background-color: #292929; border: 0px")
        self.j = j
        selBtn = self.gridLayout.itemAt(self.j).widget()
        selBtn.setStyleSheet("background: #42f2f5; color: #292929; font-weight: bold")
    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.KeyPress:
    #         print(event.key())
    #     return super(FigFileViewer, self).eventFilter(source, event)
    def prevPath(self):
        self.i -= 1
        self.i = max(0, self.i)
        self.clear()
        path = self.history[self.i]
        all_files = self.listFiles(path) # get list of all files and folders.
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)
        self.highlight(0)

    def nextPath(self):
        self.i += 1
        self.i = min(len(self.history)-1, self.i)
        self.clear()
        path = self.history[self.i]
        all_files = self.listFiles(path) # get list of all files and folders.
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)
        self.highlight(0)

    def back(self):
        self.clear()
        path = self.path
        path = pathlib.Path(path).parent
        self.path = path
        self.history.append(path)
        self.i += 1
        all_files = self.listFiles(path) # get list of all files and folders.
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)
        self.highlight(0)

    def openPath(self, path):
        self.path = path
        if not os.path.isfile(path):
            self.history.append(path)
            self.i += 1
            self.clear()
            all_files = self.listFiles(path) # get list of all files and folders.
            for i,path in enumerate(all_files):
                fileIcon = FigFileIcon(path, parent=self)
                fileIcon.clicked.connect(self.open)
                self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
            self.highlight(0)
        else:
            # call file handler for the extension here
            pass

    def listFiles(self, path, hide=True, reverse=False):
        home = str(pathlib.Path.home())
        desktop = os.path.join(home, "Desktop")
        if path == desktop:
            wallpaper_path = getWallpaper()
            self.setStyleSheet(f"background-image: url({wallpaper_path});")
        else:
            self.setStyleSheet(f"background-image: none")
        files = []
        try:
            for file in os.listdir(path):
                if not(file.startswith(".") and hide):
                    files.append(os.path.join(path, file))
            return sorted(files, key= lambda x: x.lower(), reverse=reverse)
        except PermissionError:
            return files

    def open(self):
        sendingBtn = self.sender()
        j = self.gridLayout.indexOf(sendingBtn)
        if j != self.j:
            self.highlight(j)
            return 
        if not sendingBtn.isfile:
            path = sendingBtn.path
            self.path = path
            self.history.append(path)
            self.i += 1
            self.clear()
            all_files = self.listFiles(path) # get list of all files and folders.
            for i,path in enumerate(all_files):
                fileIcon = FigFileIcon(path, parent=self)
                fileIcon.clicked.connect(self.open)
                self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
            self.highlight(0)
        else:
            # call file handler for the extension here
            pass


if __name__ == "__main__":
    FigFileViewer("/home/atharva/GUI/FigUI")