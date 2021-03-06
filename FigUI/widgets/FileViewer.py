#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
import tempfile, random
from typing import Union, List
# from PIL import Image, ImageQt
import os, re, sys, glob, pathlib, datetime
import argparse, mimetypes, platform, textwrap, subprocess
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QDir, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QObject, QRect, QPoint
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QPainter
from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QSplitter, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton, QGraphicsView, QGraphicsEffect, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect, QTextEdit

try:
    from utils import *
    from api.File import FigFile, listdir
    from api.Image import FigImage
    from widgets.FlowLayout import FlowLayout
except ImportError:
    from FigUI.utils import *
    from FigUI.api.File import FigFile, listdir
    from FigUI.api.Image import FigImage
    from FigUI.widgets.FlowLayout import FlowLayout


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("color: #6E6E6E")

#### TODO: replace with static background given as command line arg." ####
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
# STDLinuxFolders = ["/bin", "/home", "/boot", "/etc", "/opt", "/cdrom", "/proc", "/root", "/sbin", "/usr", "/dev", "/lost+found", "/var", "/tmp", "/snap", "/media", "/lib", "/lib32", "/lib64", "/mnt"]
# ThumbPhrases = ["android", "gnome", "nano", "eclipse", "cache", "java", "cargo", "compiz", "aiml", "kivy", "mozilla"]
# # map for getting filenames for thumbnails given the folder name.
# ThumbMap = {
#             "cuda": "cu.png",
#             ".sbt": "scala.png",
#             ".cmake": "cmake.svg",
#         }

# for folder in ["openoffice", "ssh", "npm", "wine", "dbus", "thunderbird", "gradle"]:
#     ThumbMap["."+folder] = folder + '.png'
# for folder in ["Videos", "Desktop", "Documents", "Downloads", "Pictures"]:
#     ThumbMap[folder] = folder + ".png"
# ThumbMap["Music"] = "Music.svg"
# ThumbMap[".rstudio-desktop"] = "R.png"
# ThumbMap[".python-eggs"] = "python-eggs.png"
# StemMap = {
#     "requirements": "requirements.png",
#     ".cling_history": "cling.png",
#     ".scala_history": "scala.png",
#     ".gitignore": "gitignore.png", 
#     ".gitconfig": "gitignore.png",
#     ".python_history": "py.png",
#     ".julia_history": "jl.png",
#     "README": "README.png",
#     ".gdbinit": "gnu.png",
#     ".Rhistory": "R.png",
#     ".pypirc": "py.png", 
# }
# PrefixMap = {
#     ".python_history": "py.png",
#     ".conda": "anaconda3.png",
#     ".bash": "bashrc.png",
#     "rstudio-": "R.png",
#     ".nvidia": "cu.png",
#     "nvidia-": "cu.png",
#     "zsh": "bashrc.png",
# }
PLATFORM = platform.system()

# def sizeof_fmt(num, suffix="B"):
#     '''convert bytes to human readable format'''
#     for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
#         if abs(num) < 1024.0:
#             return f"{num:3.1f}{unit}{suffix}"
#         num /= 1024.0
    
#     return f"{num:.1f}Y{suffix}"


class QFolderNavBtn(QPushButton):
    def __init__(self, text, till_now, parent=None):
        super(QFolderNavBtn, self).__init__(parent)
        self.setText(text)
        self._till_now = till_now
        self._display_text = text

    def callback(self):
        print(f"QFolderNavBtn(text={self._display_text}, till_now={self._till_now}) clicked")
        self.fileViewer.openPath(self._till_now)

    def connectLauncher(self, fileViewer):
        self.fileViewer = fileViewer
        self.clicked.connect(self.callback)


class FileViewerInitWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def run(self, file_viewer, all_files: List[str]):
        '''for the fileviewer ui loading task.'''
        #  print("called FileViewerInitWorker")
        for i, path in enumerate(all_files):
            figFile = FigFile(path) 
            fileIcon = FigFileIcon(figFile, parent=file_viewer)
            fileIcon.clicked.connect(file_viewer.open)
            ### replace with FlowLayout ###
            file_viewer.gridLayout.addWidget(fileIcon)
            # self.gridLayout.addWidget(fileIcon, i // width, i % width) 
            ###############################       

        # file_viewer.layout.addWidget(file_viewer.scrollArea)
        # file_viewer.setLayout(file_viewer.layout)
        selBtn = file_viewer.gridLayout.itemAt(0).widget()
        selBtn.setStyleSheet("background: color(0, 0, 255, 50)")
        file_viewer.highlight(0)

        file_viewer.viewer.setLayout(file_viewer.gridLayout)
        self.finished.emit()


# class FileViewerRefreshWorker(QObject):
#     finished = pyqtSignal()
#     progress = pyqtSignal(int)
    
#     def run(self, file_viewer, path: str, reverse: bool):
#         '''for the fileviewer ui refresh task.'''
#         file_viewer._refresh(path, reverse)
#         self.finished.emit()
GLOBAL_FILE_LIST = []
class FileViewerRefreshWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def __init__(self, iterator, is_iter=True):
        super(FileViewerRefreshWorker, self).__init__()
        self.file_iter = iterator
        # print(self.file_iter)
        self.file_info = None
        self.is_iter = is_iter
        self.i = 0

    def run(self):
        '''for the fileviewer ui refresh task.'''
        import time
        global GLOBAL_FILE_LIST
        while True:
            try:
                if self.is_iter:
                    path = next(self.file_iter).path
                else:
                    path = self.file_iter[self.i]
                file = FigFile(path)
                GLOBAL_FILE_LIST.append(file)
                # print(f"FileViewerRefreshWorker:", path)
                self.progress.emit(self.i)
                self.i += 1
                # time.sleep(1)
            except (StopIteration, IndexError) as e:
                self.finished.emit()
                return


class GraphicsView(QGraphicsView):
    rectChanged = pyqtSignal(QRect)

    def __init__(self, *args, **kwargs):
        QGraphicsView.__init__(self, *args, **kwargs)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.setMouseTracking(True)
        self.origin = QPoint()
        self.changeRubberBand = False

    def mousePressEvent(self, event):
        print("mouse press")
        self.origin = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rectChanged.emit(self.rubberBand.geometry())
        self.rubberBand.show()
        self.changeRubberBand = True
        QGraphicsView.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.changeRubberBand:
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())
            self.rectChanged.emit(self.rubberBand.geometry())
        QGraphicsView.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.changeRubberBand = False
        QGraphicsView.mouseReleaseEvent(self, event)


class FigFileHoverAnimation(QGraphicsEffect):
    def __init__(self, ):
        super(FigFileHoverAnimation, self).__init__()


# class FigFileIcon(QWidget):
#     def __init__(self, file: FigFile, parent=None, size=(150,150), textwidth=10):
#         super(FigFileIcon, self).__init__(parent)
#         self.file = file
#         self.path = self.file.path
#         self.iconSize = size
#         self._parent = parent
#         # file name label.
#         self.label = self.initLabel(self.file.name)
#         self.label.setReadOnly(True)
#         # tool button.
#         self.icon = QToolButton(self)

#         self.defaultStyle = '''
#         QToolTip {
#             border: 0px;
#             color: #fff;
#             background: #000;
#         }
#         QTextEdit {
#             color: #fff;
#             border: 0px;
#             background: #000;
#         }
#         QTextEdit:hover {
#             color: #292929;
#             font-weight: bold;
#             background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+''');
#         }
#         QToolButton { 
#             border: 0px; 
#             background: transparent;
#             background-image: none;
#             color: #fff;
#             margin: 10px;
#         }
#         /* #e38c59; */ /* #009b9e; */
#         ''' 
#         self.selectedStyle = '''
#         QToolTip {
#             border: 0px;
#             color: #fff;
#         }
#         QToolButton { 
#             border: 0px; 
#             /* background: '''+Fig.FileViewer.SCHEX+'''; */
#             background: transparent;
#             background-image: none;
#             color: #fff;
#             margin: 10px;
#         }
#         /* QToolButton { 
#             '''+f"background: {Fig.FileViewer.SCHEX};"+'''
#             background-image: none;
#             color: #292929;
#             font-weight: bold;
#             margin: 10px;
#         } */   
#         QTextEdit {
#             border: 0px;
#             color: #292929;
#             font-weight: bold;
#             background-image: none;
#             background-color: green;
#         }'''
#         '''
#         QTextEdit {
#             border: 0px;
#             color: #292929;
#             font-weight: bold;
#             background-color: '''+Fig.FileViewer.CLHEX+''';
#             /* qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); */
#         }
#         ''' 
#         self.figImage = FigImage(__icon__(self.file.thumbnail))
#         self.setStyleSheet(self.defaultStyle)
#         self.icon.setAttribute(Qt.WA_TranslucentBackground)
#         # text = "\n".join(textwrap.wrap(self.file.name[:textwidth*3], width=textwidth))
#         # self.label.setWordWrap(True)
#         # truncate at 3 times the max textwidth
#         # self.label.setFixedWidth(70)
#         # self.icon.setFixedSize(QSize(70,70))
#         self.icon.setIconSize(QSize(50,50))
#         self.icon.setFixedWidth(size[0])
#         # create layout.
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.icon, Qt.AlignCenter)
#         self.layout.addWidget(self.label, Qt.AlignCenter)
#         self.setLayout(self.layout)
#         self._setThumbnail()
#         self._setPropertiesTip()
#         self.setFixedSize(QSize(*size))
#         # self.label.setTextColor(QColor(255,255,255))
#     # def format(self, text, k=7):
#     #     List = []
#     #     for i in range(1+len(text)//k):
#     #         List.append(text[k*i:k*(i+1)])
        
#     #     return "\n".join(List)
#     def initEffect(self):
#         shadowEffect = QGraphicsDropShadowEffect(self)
#         shadowEffect.setOffset(0, 0)
#         shadowEffect.setColor(QColor(*Fig.FileViewer.SCRGB))
#         shadowEffect.setBlurRadius(100)
        
#         return shadowEffect

#     def initLabel(self, text: str, trans: bool=True):
#         label = QTextEdit()
#         label.setAttribute(Qt.WA_TranslucentBackground)
#         if not trans:
#             label.setHtml(f"<span style='background: {Fig.FileViewer.SCHEX};'>{text}</span>")
#         else:
#             label.setText(text)
#         label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         label.setFixedWidth(self.iconSize[0])
#         label.setAlignment(Qt.AlignCenter)

#         return label

#     def unselect(self):
#         self.setStyleSheet(self.defaultStyle)
#         self.label.setParent(None)
#         self.label = self.initLabel(self.file.name)
#         self.layout.addWidget(self.label)
#         self.setGraphicsEffect(None)
#         self._setThumbnail()

#     def highlightIcon(self):
#         tinted = self.figImage.tint(color=Fig.FileViewer.SCHEX)
#         self.icon.setIcon(tinted.QIcon())

#     def select(self):
#         self.setStyleSheet(self.selectedStyle)
#         self.label.setParent(None)
#         self.label = self.initLabel(self.file.name, trans=False)
#         self.layout.addWidget(self.label)
#         shadowEffect = self.initEffect()
#         self.setGraphicsEffect(shadowEffect)
#         # to make sure the object isn't garbage collected!
#         self.shadowEffect = shadowEffect
#         self.highlightIcon()

#     def _setPropertiesTip(self):
#         self.setToolTip(str(self.file))

#     def _setThumbnail(self):
#         self.icon.setIcon(FigIcon(self.file.thumbnail))

#     def enterEvent(self, event):
#         shadowEffect = self.initEffect()
#         self.setGraphicsEffect(shadowEffect)
#         self.shadowEffect = shadowEffect

#     def leaveEvent(self, event):
#         self.setGraphicsEffect(None)

class FigFileIcon(QToolButton):
    def __init__(self, file: FigFile, parent=None, size=(150,150), textwidth=10):
        super(FigFileIcon, self).__init__(parent)
        self.file = file
        self._parent = parent
        thumbnail_path = __icon__(self.file.thumbnail)
        if os.path.exists(thumbnail_path):
            self.figImage = FigImage(thumbnail_path)
        else:
            # cases when the file is an image file.
            self.figImage = FigImage(self.file.thumbnail)
        self.defaultStyle = '''
        QToolTip {
            border: 0px;
            color: #fff;
        }
        QToolButton { 
            border: 0px; 
            background: transparent;
            background-image: none;
            color: #fff;
            margin: 10px;
        }
        '''
        '''
        QToolButton:hover {
            background: qradialgradient(
                cx: 0.7, cy: 0.7, radius: 0.5, 
                stop: 0 '''+Fig.FileViewer.CDHEX+''', 
                stop : 0.2 '''+Fig.FileViewer.CLHEX+''', 
                stop : 0.4 '''+Fig.FileViewer.CDHEX+''', 
                stop : 0.6 '''+Fig.FileViewer.CLHEX+''', 
                stop : 0.8 '''+Fig.FileViewer.CDHEX+''', 
                stop: 1 '''+Fig.FileViewer.CLHEX+'''); 
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); */
            color: #292929;
            font-weight: bold;
        }
        /* #e38c59; */ /* #009b9e; */
        ''' 
        self.selectedStyle = '''
        QToolTip {
            border: 0px;
            color: #fff;
        }
        QToolButton { 
            border: 0px;
            color: #292929;
            font-weight: bold;
            margin: 10px;
            background: transparent;
        } 
        '''
        '''
        QToolButton { 
            '''+f"background: {Fig.FileViewer.SCHEX};"+'''
            background-image: none;
            color: #292929;
            font-weight: bold;
            margin: 10px;
        }    
        ''' 
        self.setStyleSheet(self.defaultStyle)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        text = "\n".join(textwrap.wrap(self.file.name[:textwidth*3], width=textwidth))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setText(text) # truncate at 3 times the max textwidth
        self.setFixedSize(QSize(*size))
        self.setIconSize(QSize(50,50))
        self._setThumbnail()
        self._setPropertiesTip()

    def highlightIcon(self):
        tinted = self.figImage.tint(color=Fig.FileViewer.SCHEX)
        self.setIcon(tinted.QIcon())

    def initEffect(self):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setOffset(0, 0)
        shadowEffect.setColor(QColor(*Fig.FileViewer.SCRGB))
        shadowEffect.setBlurRadius(100)
        
        return shadowEffect

    def unselect(self):
        self.setStyleSheet(self.defaultStyle)
        self.setGraphicsEffect(None)
        self._setThumbnail()

    def select(self):
        self.setStyleSheet(self.selectedStyle)
        shadowEffect = self.initEffect()
        self.setGraphicsEffect(shadowEffect)
        # # to make sure the object isn't garbage collected!
        self.shadowEffect = shadowEffect
        self.highlightIcon()

    def _setPropertiesTip(self):
        self.setToolTip(str(self.file))

    def _setThumbnail(self):
        self.setIcon(FigIcon(self.file.thumbnail))

    def enterEvent(self, event):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setOffset(0, 0)
        shadowEffect.setColor(QColor(*Fig.FileViewer.SCRGB))
        shadowEffect.setBlurRadius(100)
        self.setGraphicsEffect(shadowEffect)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)

        
class FigFileViewer(QWidget):
    def __init__(self, path=str(pathlib.Path.home()), parent=None, width=4, button_size=(100,100), icon_size=(60,60)):
        super(FigFileViewer, self).__init__(parent)   
        self.folderBar = self.initFolderNavBar() 
        self.folderBar.path = str(pathlib.Path.home())
        self.selectedItems = []
        self.ribbon_visible = True
        self.curr_path = path # initialize current path with the passed path or home.
        self._parent = parent
        self.window = parent
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.fileFilter = None
        scrollAreaStyle = '''
        QScrollArea {
            background-position: center;
            border: 0px;
        }
        QScrollBar:vertical {
            border: 0px solid #999999;
            width: 10px;    
            margin: 0px 0px 0px 0px;
            background-color: rgba(255, 255, 255, 0);
        }
        QScrollBar:vertical:hover {
            background-color: rgba(255, 253, 184, 0.3);
        }
        QScrollBar::handle:vertical {         
            min-height: 0px;
            border: 0px solid red;
            border-radius: 0px;
            background-color: #484848;
        }
        QScrollBar::handle:vertical:hover {         
            background-color: orange;
        }
        QScrollBar::add-line:vertical {       
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }'''
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet(scrollAreaStyle)
        ### replace with FlowLayout ###
        self.gridLayout = FlowLayout() # QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(5)
        ###############################
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        try: 
            Fig.FileViewer._FVBG = f"url('{parent.bg_blur_url}');"
            print("found background file")
        except AttributeError:
            print("defaulting to backup texture")
        
        self.bgStyle = "url('/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png');"
        self.viewer = QWidget()
        self.viewer.setStyleSheet('''
        background: ''' + Fig.FileViewer._FVBG + '''
        ''')
        self.history = [path]
        self.historyIter = 0
        self.j = 0

        self.viewer.setLayout(self.gridLayout)
        self.refresh(path)
        
        self.scrollArea.setWidget(self.viewer)
        self.sideBar = self.initSideBar()

        self.overallViewer = QSplitter(Qt.Horizontal)
        self.overallViewer.addWidget(self.sideBar)
        self.overallViewer.addWidget(self.scrollArea)
        
        overallScrollArea = QScrollArea()
        overallScrollArea.setWidgetResizable(True)
        overallScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        overallScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        overallScrollArea.setStyleSheet(scrollAreaStyle)
        overallScrollArea.setWidget(self.overallViewer)

        self.navbar = self.initNavBar()
        self.propbar = self.initPropBar()
        # self.editbar = self.initEditBar()
        # self.viewbar = self.initViewBar()
        self.mainMenu = self.initMainMenu()
        # self.utilbar = self.initUtilBar()

        # self.layout.addWidget(self.editbar)
        # self.layout.addWidget(self.propbar)
        self.layout.addWidget(self.folderBar)
        self.layout.addWidget(self.mainMenu)
        self.layout.addWidget(self.navbar)
        # print("created toolbars:", time.time()-start)
        # self.layout.addWidget(self.viewbar)
        # self.layout.addWidget(self.utilbar)
        # self.layout.addWidget(self.scrollArea)
        self.layout.addWidget(overallScrollArea)
        self.setLayout(self.layout)
        self.width = width
        # selBtn = self.gridLayout.itemAt(0).widget()
        # selBtn.setStyleSheet("background: color(0, 0, 255, 50)")
        # self.highlight(0)
        # link folder nav bar buttons.
        self.toggleRibbon()
        self.backNavBtn.clicked.connect(self.prevPath)
        self.nextNavBtn.clicked.connect(self.nextPath)
        self.overallViewer.setSizes([70,700])
        # self.folderBar.hide()
        # self.sideBar.hide()
    def initSideBarBtn(self, name: str):
        home = str(pathlib.Path.home())
        tb = "    "
        btn = QToolButton(self)
        btn.setToolTip(f"open {name}.")
        btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        btn.setText(tb+name.title()+tb)
        btn.setIcon(FigIcon(f"sysbar/{name}.svg"))
        btn.setStyleSheet('''
        QToolButton {
            color: #fff;
            border: 0px;
            background: transparent;
        }
        QToolButton::hover{
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); 
        }
        QToolTip { 
            color: #fff;
            border: 0px;
        }''')
        if name == "trash":
            path = os.path.join(home, ".local/share/Trash/files")
        elif name == "home": path = home
        else: path = os.path.join(home, name.title())
        btn.clicked.connect(lambda: self.refresh(path=path))

        return btn
    
    def initSideBar(self):
        sideBar = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        # # recents.
        # recentBtn = QToolButton("Recent", self)
        # recentBtn.setToolTip("recently modified/opened files.")
        # recentBtn.setIcon(FigIcon("sysbar/recent.svg"))
        # home.
        homeBtn = self.initSideBarBtn(name="home")
        layout.addWidget(homeBtn)
        # desktop.
        desktopBtn = self.initSideBarBtn(name="desktop")
        layout.addWidget(desktopBtn)
        # documents.
        documentBtn = self.initSideBarBtn(name="documents")
        layout.addWidget(documentBtn)
        # downloads.
        downloadsBtn = self.initSideBarBtn(name="downloads")
        layout.addWidget(downloadsBtn)
        # music.
        musicBtn = self.initSideBarBtn(name="music")
        layout.addWidget(musicBtn)
        # videos.
        videosBtn = self.initSideBarBtn(name="videos")
        layout.addWidget(videosBtn)
        # pictures.
        picturesBtn = self.initSideBarBtn(name="pictures")
        layout.addWidget(picturesBtn)
        # trash.
        trashBtn = self.initSideBarBtn(name="trash")
        layout.addWidget(trashBtn)
        layout.addStretch(1)

        sideBar.setLayout(layout)

        return sideBar

    def toggleRibbon(self):
        if self.ribbon_visible:
            self.mainMenu.setFixedHeight(25)
            self.hideBtn.setIcon(FigIcon("fileviewer/show_ribbon.svg"))
        else:
            self.mainMenu.setMaximumHeight(120)
            self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.ribbon_visible = not(
            self.ribbon_visible
        )

    def showRibbon(self):
        self.mainMenu.setMaximumHeight(120)
        self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.ribbon_visible = True

    def mousePressEvent(self, event):
        self.selection=event.pos()
        self.rubberBand.setGeometry(QRect(self.selection,QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        self.rubberBand.setGeometry(
            QRect(
                self.selection, event.pos()
            ).normalized()
        )

    def mouseReleaseEvent(self, event):   
        '''use this function to show the selection'''
        rect = self.rubberBand.geometry()
        # print("\x1b[31;1mrect:\x1b[0m", rect, dir(rect))
        for child in self.listContents():
            # print(child.geometry(), child.text())
            if rect.contains(child.geometry()) and child.inherits('FigFileIcon'):
                print(child.icon.text())
                child.select()
            self.rubberBand.hide()

    def initConvertMenu(self):
        convertMenu = QWidget()
        return convertMenu

    def initMoreMenu(self):
        moreMenu = QWidget()
        return moreMenu

    def initMainMenu(self):
        '''create main menu for file browser.'''
        tb = "\t"*4
        mainMenu = QTabWidget()
        self.fileMenu = self.initFileMenu()
        mainMenu.addTab(self.fileMenu, tb+"File"+tb)
        self.editMenu = self.initEditMenu()
        mainMenu.addTab(self.editMenu, tb+"Edit"+tb)
        self.homeMenu = self.initHomeMenu()
        mainMenu.addTab(self.homeMenu, tb+"Home"+tb)
        self.viewMenu = self.initViewMenu()
        mainMenu.addTab(self.viewMenu, tb+"View"+tb)
        self.propMenu = self.initPropMenu()
        mainMenu.addTab(self.propMenu, tb+"Properties"+tb)
        self.searchMenu = self.initSearchMenu()
        mainMenu.addTab(self.searchMenu, tb+"Search"+tb)
        self.convertMenu = self.initConvertMenu()
        mainMenu.addTab(self.convertMenu, tb+"Convert"+tb)
        self.shareMenu = self.initShareMenu()
        mainMenu.addTab(self.shareMenu, tb+"Share"+tb)
        self.moreMenu = self.initMoreMenu()
        mainMenu.addTab(self.moreMenu, tb+"More"+tb)
        mainMenu.currentChanged.connect(self.showRibbon)
        # hide the ribbon.
        self.hideBtn = QToolButton(mainMenu)
        self.hideBtn.clicked.connect(self.toggleRibbon)
        self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.hideBtn.setIconSize(QSize(23,23))
        self.hideBtn.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')
        # info button.
        self.infoBtn = QToolButton(mainMenu)
        self.infoBtn.pressed.connect(lambda: print("info"))
        self.infoBtn.setIcon(FigIcon("fileviewer/help.svg"))
        self.infoBtn.setStyleSheet('''
        QToolButton {
            border: 0px;
            background: transparent;
        }''')
        self.infoBtn.setIconSize(QSize(23,23))

        mainMenu.addTab(QWidget(), "")
        mainMenu.addTab(QWidget(), "")
        mainMenu.tabBar().setTabButton(9, QTabBar.RightSide, self.hideBtn)
        mainMenu.tabBar().setTabButton(10, QTabBar.RightSide, self.infoBtn)

        mainMenu.setCurrentIndex(0)
        mainMenu.setStyleSheet('''
        QTabWidget {
            background:'''+self.bgStyle+'''
            color: #000;
            border: 0px;
        }
        QTabWidget::pane {
            background:'''+self.bgStyle+'''
            border: 0px;
        }
        QTabBar {
            background:'''+self.bgStyle+'''
            border: 0px;
        }
        QWidget {
            background:'''+self.bgStyle+'''
        }
        QTabBar::tab {
            color: #fff;
            border: 0px;
            margin: 0px;
            padding: 0px;
            font-size: 16px;
            background: #292929;
        }
        QTabBar::tab:hover {
            /* background: qlineargradient(x1 : 0, y1 : 1, x2 : 0, y2 : 0, stop : 0.0 #70121c, stop : 0.6 #b31f2f, stop : 0.8 #de2336); */
            /* background: #ffbb63; */
            background: '''+ Fig.FileViewer.CLHEX +''';
            color: #292929;
        }
        QTabBar::tab:selected {
            /* background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 #de891b, stop : 0.99 #ffbb63); */
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); 
            color: #fff;
        }
        QToolTip { 
            color: #fff;
            border: 0px;
        }
        QToolButton {
            border: 0px;
            font-size: 13px;
            padding-left: 5px;
            padding-right: 5px;
            background: transparent;
            color: #fff;
        }
        QToolButton:hover {
            border: 0px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); 
        }
        QLabel { 
            color: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+''');
            font-size: 14px;
        }''')
        glowEffect = QGraphicsDropShadowEffect()
        glowEffect.setBlurRadius(50)
        glowEffect.setOffset(30,0)
        glowEffect.setColor(QColor(*Fig.FileViewer.CDRGB))
        mainMenu.setGraphicsEffect(glowEffect)
        mainMenu.setMaximumHeight(130)

        return mainMenu

    def listContents(self):
        for i in range(self.gridLayout.count()):
            yield self.gridLayout.itemAt(i).widget()

    def initFileMenu(self):
        fileMenu = QWidget()
        fileLayout = QHBoxLayout()
        fileLayout.setSpacing(0)
        fileLayout.setContentsMargins(0, 0, 0, 0)
        # control groups
        newGroup = QWidget() 
        newLayout = QVBoxLayout()
        newLayout.setSpacing(0)
        newLayout.setContentsMargins(0, 0, 0, 0)
        remGroup = QWidget() 
        remLayout = QVBoxLayout()
        remLayout.setSpacing(0)
        remLayout.setContentsMargins(0, 0, 0, 0)
        openGroup = QWidget()
        openLayout = QVBoxLayout()
        openLayout.setSpacing(0)
        openLayout.setContentsMargins(0, 0, 0, 0)
        renameGroup = QWidget()
        renameLayout = QVBoxLayout()
        renameLayout.setSpacing(0)
        renameLayout.setContentsMargins(0, 0, 0, 0)

        newToolBar = QWidget()
        newToolBarLayout = QHBoxLayout()
        newToolBarLayout.setSpacing(0)
        newToolBarLayout.setContentsMargins(0, 0, 0, 0)   
        
        remToolBar = QWidget()
        remToolBarLayout = QHBoxLayout()
        remToolBarLayout.setSpacing(0)
        remToolBarLayout.setContentsMargins(0, 0, 0, 0)

        renameToolBar = QWidget()
        renameToolBarLayout = QHBoxLayout()
        renameToolBarLayout.setSpacing(0)
        renameToolBarLayout.setContentsMargins(0, 0, 0, 0)

        openToolBar = QWidget()
        openToolBarLayout = QHBoxLayout()
        openToolBarLayout.setSpacing(0)
        openToolBarLayout.setContentsMargins(0, 0, 0, 0)

        verticalRibbon = QWidget()
        verticalRibbonLayout = QVBoxLayout()
        verticalRibbonLayout.setSpacing(0)
        verticalRibbonLayout.setContentsMargins(0, 0, 0, 0)

        removeRibbon = QWidget()
        removeRibbonLayout = QVBoxLayout()
        removeRibbonLayout.setSpacing(0)
        removeRibbonLayout.setContentsMargins(0, 0, 0, 0)

        # create new link
        newLinkBtn = QToolButton()
        newLinkBtn.setIcon(FigIcon("fileviewer/softlink.svg"))
        newLinkBtn.setIconSize(QSize(22,22))
        newLinkBtn.setText("New Link")
        newLinkBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        verticalRibbonLayout.addWidget(newLinkBtn)
        # create new note
        newNoteBtn = QToolButton()
        newNoteBtn.setIcon(FigIcon("fileviewer/add_note.svg"))
        newNoteBtn.setIconSize(QSize(22,22))
        newNoteBtn.setText("New Note")
        newNoteBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        verticalRibbonLayout.addWidget(newNoteBtn)
        # create new tag
        newTagBtn = QToolButton()
        newTagBtn.setIcon(FigIcon("fileviewer/add_tags.svg"))
        newTagBtn.setIconSize(QSize(22,22))
        newTagBtn.setText("New Tag")
        newTagBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        verticalRibbonLayout.addWidget(newTagBtn)
        verticalRibbon.setLayout(verticalRibbonLayout)
        # create new file
        newFileBtn = QToolButton()
        newFileBtn.setIcon(FigIcon("fileviewer/new_file.svg"))
        newFileBtn.setIconSize(QSize(30,30))
        newFileBtn.setText("New File")
        newFileBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newToolBarLayout.addWidget(newFileBtn)
        # create new folder
        newFolderBtn = QToolButton()
        newFolderBtn.setIcon(FigIcon("fileviewer/new_folder.svg"))
        newFolderBtn.setIconSize(QSize(30,30))
        newFolderBtn.setText("New Folder")
        newFolderBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        newToolBarLayout.addWidget(newFolderBtn)
        newToolBarLayout.addWidget(verticalRibbon)

        # remove link
        remLinkBtn = QToolButton()
        remLinkBtn.setIcon(FigIcon("fileviewer/unlink.svg"))
        remLinkBtn.setIconSize(QSize(22,22))
        remLinkBtn.setText("Remove Link")
        remLinkBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        removeRibbonLayout.addWidget(remLinkBtn)
        # remove note
        remNoteBtn = QToolButton()
        remNoteBtn.setIcon(FigIcon("fileviewer/rem_note.svg"))
        remNoteBtn.setIconSize(QSize(22,22))
        remNoteBtn.setText("Remove Note")
        remNoteBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        removeRibbonLayout.addWidget(remNoteBtn)
        # remove tag
        remTagBtn = QToolButton()
        remTagBtn.setIcon(FigIcon("fileviewer/remove_tags.svg"))
        remTagBtn.setIconSize(QSize(22,22))
        remTagBtn.setText("Remove Tag")
        remTagBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        removeRibbonLayout.addWidget(remTagBtn)
        removeRibbon.setLayout(removeRibbonLayout)
        # delete folder/file
        delBtn = QToolButton()
        delBtn.setIcon(FigIcon("fileviewer/delete.svg"))
        delBtn.setIconSize(QSize(30,30))
        delBtn.setText("Delete")
        delBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        remToolBarLayout.addWidget(delBtn)
        remToolBarLayout.addWidget(removeRibbon)
        # rename file/folder
        renameBtn = QToolButton()
        renameBtn.setIcon(FigIcon("fileviewer/rename.svg"))
        renameBtn.setIconSize(QSize(30,30))
        renameBtn.setText("Rename")
        delBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        renameToolBarLayout.addWidget(renameBtn)

        # open with.
        openBtn = QToolButton()
        openBtn.setIcon(FigIcon("fileviewer/open.svg"))
        openBtn.setIconSize(QSize(30,30))
        openBtn.setText("Open")
        openBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        openToolBarLayout.addWidget(openBtn)
        # open in terminal
        openInTermBtn = QToolButton()
        openInTermBtn.setIcon(FigIcon("fileviewer/open_in_terminal.svg"))
        openInTermBtn.setIconSize(QSize(30,30))
        openInTermBtn.setText("Open in Terminal")
        openInTermBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        openInTermBtn.clicked.connect(self.openInTermTab)
        openToolBarLayout.addWidget(openInTermBtn)
        # open in browser
        openInBrowserBtn = QToolButton()
        openInBrowserBtn.setIcon(FigIcon("fileviewer/open_in_browser.svg"))
        openInBrowserBtn.setIconSize(QSize(30,30))
        openInBrowserBtn.setText("Open in Browser")
        openInBrowserBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        openToolBarLayout.addWidget(openInBrowserBtn)

        # construct groups
        ## new group
        newToolBar.setLayout(newToolBarLayout)
        newLayout.addWidget(newToolBar)
        newLabel = QLabel("New")
        newLabel.setAlignment(Qt.AlignCenter)
        newLayout.addWidget(newLabel)
        newGroup.setLayout(newLayout)
        ## remove group
        remToolBar.setLayout(remToolBarLayout)
        remLayout.addWidget(remToolBar)
        remLabel = QLabel("Remove")
        remLabel.setAlignment(Qt.AlignCenter)
        remLayout.addWidget(remLabel)
        remGroup.setLayout(remLayout)
        ## open group
        openToolBar.setLayout(openToolBarLayout)
        openLayout.addWidget(openToolBar)
        openLabel = QLabel("Open")
        openLabel.setAlignment(Qt.AlignCenter)
        openLabel.setMaximumHeight(30)
        openLayout.addWidget(openLabel)
        openGroup.setLayout(openLayout)
        ## rename group
        renameToolBar.setLayout(renameToolBarLayout)
        renameLayout.addWidget(renameToolBar)
        renameLabel = QLabel("Rename")
        renameLabel.setMaximumHeight(30)
        renameLabel.setAlignment(Qt.AlignCenter)
        renameLayout.addWidget(renameLabel)
        renameGroup.setLayout(renameLayout)

        # add groups.
        fileLayout.addWidget(newGroup)
        fileLayout.addWidget(self.addSpacer())
        fileLayout.addWidget(remGroup)
        fileLayout.addWidget(self.addSpacer())
        fileLayout.addWidget(openGroup)
        fileLayout.addWidget(self.addSpacer())
        fileLayout.addWidget(renameGroup)
        fileLayout.addWidget(self.addSpacer())
        fileLayout.addWidget(self.addStretch())

        # set layout
        fileMenu.setLayout(fileLayout)

        return fileMenu

    def initHomeMenu(self):
        '''
        bookmark, history (version control), favourite (star), set as wallpaper, desktop shortcut, zip, select, encrypt etc.'''
        homeMenu = QWidget()
        homeLayout = QHBoxLayout()
        homeLayout.setSpacing(0)
        homeLayout.setContentsMargins(0, 0, 0, 0)
        # # control groups
        # moveGroup = QWidget() 
        # moveLayout = QVBoxLayout()
        # moveLayout.setSpacing(0)
        # moveLayout.setContentsMargins(0, 0, 0, 0)
           
        # pin to quick access.
        pinBtn = QToolButton()
        pinBtn.setIcon(FigIcon("fileviewer/pin.svg"))
        pinBtn.setIconSize(QSize(35,35))
        pinBtn.setText("\nPin to Quick\naccess")
        pinBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # add all groups
        homeLayout.addWidget(pinBtn)
        homeLayout.addWidget(self.addSpacer())
        homeLayout.addWidget(self.addStretch())
        homeMenu.setLayout(homeLayout)

        return homeMenu

    def initSearchMenu(self):
        searchMenu = QWidget()
        searchLayout = QHBoxLayout()
        searchLayout.setSpacing(0)
        searchLayout.setContentsMargins(0, 0, 0, 0)
        # control groups
        filterGroup = QWidget()
        filterLayout = QVBoxLayout()
        filterLayout.setSpacing(0)
        filterLayout.setContentsMargins(0, 0, 0, 0)
        
        filterLowerRibbon = QWidget()
        filterUpperRibbon = QWidget()
        filterUpperRibbonLayout = QHBoxLayout()
        filterLowerRibbonLayout = QHBoxLayout()
        filterUpperRibbonLayout.setSpacing(0)
        filterLowerRibbonLayout.setSpacing(0)
        filterUpperRibbonLayout.setContentsMargins(0, 0, 0, 0)
        filterLowerRibbonLayout.setContentsMargins(0, 0, 0, 0)     
        # filter
        filtBtn = QToolButton()
        filtBtn.setIcon(FigIcon("fileviewer/filter.svg"))
        filtBtn.setIconSize(QSize(18,18))
        filtBtn.setText(" Filter ")
        filtBtn.setMinimumWidth(65)
        filtBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filterUpperRibbonLayout.addWidget(filtBtn)
        # filter add
        filtAddBtn = QToolButton()
        filtAddBtn.setIcon(FigIcon("fileviewer/filter_add.svg"))
        filtAddBtn.setIconSize(QSize(18,18))
        filtAddBtn.setText("   Add  ")
        filtAddBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filterUpperRibbonLayout.addWidget(filtAddBtn)
        # filter delete
        filtDelBtn = QToolButton()
        filtDelBtn.setIcon(FigIcon("fileviewer/filter_delete.svg"))
        filtDelBtn.setIconSize(QSize(18,18))
        filtDelBtn.setText(" Delete ")
        filtDelBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filterUpperRibbonLayout.addWidget(filtDelBtn)
        # filter negate
        filtNegBtn = QToolButton()
        filtNegBtn.setIcon(FigIcon("fileviewer/filter_negate.svg"))
        filtNegBtn.setIconSize(QSize(18,18))
        filtNegBtn.setText(" Negate ")
        filtNegBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filterUpperRibbonLayout.addWidget(filtNegBtn)
        # filter favourites
        filtFavBtn = QToolButton()
        filtFavBtn.setIcon(FigIcon("fileviewer/filter_favourites.svg"))
        filtFavBtn.setIconSize(QSize(18,18))
        filtFavBtn.setText("Favorite")
        filtFavBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filterLowerRibbonLayout.addWidget(filtFavBtn)
        # filter edit
        filtEditBtn = QToolButton()
        filtEditBtn.setIcon(FigIcon("fileviewer/filter_edit.svg"))
        filtEditBtn.setIconSize(QSize(18,18))
        filtEditBtn.setText("  Edit  ")
        filtEditBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        filterLowerRibbonLayout.addWidget(filtEditBtn)
        # right expander
        right = QWidget()
        right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        filterLowerRibbonLayout.addWidget(right)

        filterLowerRibbon.setLayout(filterLowerRibbonLayout)
        filterUpperRibbon.setLayout(filterUpperRibbonLayout)   
        filterLayout.addWidget(filterUpperRibbon)
        filterLayout.addWidget(filterLowerRibbon)
        filterLabel = QLabel("Filter") 
        filterLabel.setAlignment(Qt.AlignCenter)
        filterLayout.addWidget(filterLabel)

        filterGroup.setLayout(filterLayout)
        filterGroup.setMaximumWidth(240)
        # add all groups
        searchLayout.addWidget(filterGroup)
        searchLayout.addWidget(self.addSpacer())
        searchLayout.addWidget(self.addStretch())
        searchMenu.setLayout(searchLayout)

        return searchMenu

    def initViewMenu(self):
        viewMenu = QWidget()
        viewLayout = QHBoxLayout()
        viewLayout.setSpacing(0)
        viewLayout.setContentsMargins(0, 0, 0, 0)
        # control groups
        layoutGroup = QWidget() 
        layoutLayout = QVBoxLayout()
        layoutLayout.setSpacing(0)
        layoutLayout.setContentsMargins(0, 0, 0, 0)

        layoutToolBar = QWidget()
        layoutToolBarLayout = QHBoxLayout()
        layoutToolBarLayout.setSpacing(0)
        layoutToolBarLayout.setContentsMargins(0, 0, 0, 0)
        layoutToolBar.setLayout(layoutToolBarLayout)

        sortRibbon = QWidget()
        sortLayout = QVBoxLayout()
        sortLayout.setSpacing(0)
        sortLayout.setContentsMargins(0, 0, 0, 0)
        sortRibbon.setLayout(sortLayout)

        sideBarRibbon = QWidget()
        sideBarLayout = QVBoxLayout()
        sideBarLayout.setSpacing(0)
        sideBarLayout.setContentsMargins(0, 0, 0, 0)
        sideBarRibbon.setLayout(sideBarLayout)
        
        sideBarVisiblityRibbon = QWidget()
        sideBarVisiblityLayout = QVBoxLayout()
        sideBarVisiblityLayout.setSpacing(0)
        sideBarVisiblityLayout.setContentsMargins(0, 0, 0, 0)
        sideBarVisiblityRibbon.setLayout(sideBarVisiblityLayout)

        folderBarVisiblityRibbon = QWidget()
        folderBarVisiblityLayout = QVBoxLayout()
        folderBarVisiblityLayout.setSpacing(0)
        folderBarVisiblityLayout.setContentsMargins(0, 0, 0, 0)
        folderBarVisiblityRibbon.setLayout(folderBarVisiblityLayout)

        # sort ascending.
        sortUpBtn = QToolButton()
        sortUpBtn.setIcon(FigIcon("fileviewer/sort_ascending.svg"))
        sortUpBtn.setIconSize(QSize(25,25))
        sortUpBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=False))
        sortUpBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sortUpBtn.setText("A to Z")
        sortLayout.addWidget(sortUpBtn)
        # sort descending.
        sortDownBtn = QToolButton()
        sortDownBtn.setIcon(FigIcon("fileviewer/sort_descending.svg"))
        sortDownBtn.setIconSize(QSize(25,25))
        sortDownBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=True))
        sortDownBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sortLayout.addWidget(sortDownBtn)
        sortDownBtn.setText("Z to A")
        layoutToolBarLayout.addWidget(sortRibbon)
        # sidebar to left.
        sideLeftBtn = QToolButton()
        sideLeftBtn.setIcon(FigIcon("fileviewer/sidebar_to_left.svg"))
        sideLeftBtn.setIconSize(QSize(25,25))
        sideLeftBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sideBarLayout.addWidget(sideLeftBtn)
        sideLeftBtn.setText("to left")
        sideLeftBtn.clicked.connect(self.sideBarToLeft)
        # sidebar to right.
        sideRightBtn = QToolButton()
        sideRightBtn.setIcon(FigIcon("fileviewer/sidebar_to_right.svg"))
        sideRightBtn.setIconSize(QSize(25,25))
        sideRightBtn.clicked.connect(self.sideBarToRight)
        sideRightBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sideBarLayout.addWidget(sideRightBtn)
        sideRightBtn.setText("to right")
        layoutToolBarLayout.addWidget(sideBarRibbon)
        
        # show sidebar.
        sideBarShowBtn = QToolButton()
        sideBarShowBtn.setIcon(FigIcon("fileviewer/sidebar_to_left.svg"))
        sideBarShowBtn.setIconSize(QSize(25,25))
        sideBarShowBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sideBarVisiblityLayout.addWidget(sideBarShowBtn)
        sideBarShowBtn.setText("show")
        sideBarShowBtn.clicked.connect(self.sideBar.show)
        # hide sidebar.
        sideBarHideBtn = QToolButton()
        sideBarHideBtn.setIcon(FigIcon("fileviewer/hide_sidebar.svg"))
        sideBarHideBtn.setIconSize(QSize(25,25))
        sideBarHideBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sideBarVisiblityLayout.addWidget(sideBarHideBtn)
        sideBarHideBtn.setText("hide")
        sideBarHideBtn.clicked.connect(self.sideBar.hide)
        layoutToolBarLayout.addWidget(sideBarVisiblityRibbon)

        # show folderbar.
        folderBarShowBtn = QToolButton()
        folderBarShowBtn.setIcon(FigIcon("fileviewer/show_folderbar.svg"))
        folderBarShowBtn.setIconSize(QSize(25,25))
        folderBarShowBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        folderBarVisiblityLayout.addWidget(folderBarShowBtn)
        folderBarShowBtn.setText("show")
        folderBarShowBtn.clicked.connect(self.folderBar.show)
        # hide folderbar.
        folderBarHideBtn = QToolButton()
        folderBarHideBtn.setIcon(FigIcon("fileviewer/hide_folderbar.svg"))
        folderBarHideBtn.setIconSize(QSize(25,25))
        folderBarHideBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        folderBarVisiblityLayout.addWidget(folderBarHideBtn)
        folderBarHideBtn.setText("hide")
        folderBarHideBtn.clicked.connect(self.folderBar.hide)
        layoutToolBarLayout.addWidget(folderBarVisiblityRibbon)

        # list view.
        listViewBtn = QToolButton()
        listViewBtn.setIcon(FigIcon("fileviewer/list_view.svg"))
        listViewBtn.setIconSize(QSize(30,30))
        # listViewBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=False))
        listViewBtn.setText("list")
        listViewBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layoutToolBarLayout.addWidget(listViewBtn)
        # grid view.
        gridViewBtn = QToolButton()
        gridViewBtn.setIcon(FigIcon("fileviewer/grid_view.svg"))
        gridViewBtn.setIconSize(QSize(30,30))
        # gridViewBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=False))
        gridViewBtn.setText("grid")
        gridViewBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layoutToolBarLayout.addWidget(gridViewBtn)
        # tree view.
        treeViewBtn = QToolButton()
        treeViewBtn.setIcon(FigIcon("fileviewer/tree_view.svg"))
        treeViewBtn.setIconSize(QSize(30,30))
        # treeViewBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=False))
        treeViewBtn.setText("tree")
        treeViewBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layoutToolBarLayout.addWidget(treeViewBtn)
        # google drive view.
        driveViewBtn = QToolButton()
        driveViewBtn.setIcon(FigIcon("fileviewer/drive.svg"))
        driveViewBtn.setIconSize(QSize(30,30))
        # treeViewBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=False))
        driveViewBtn.setText("drive")
        driveViewBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        layoutToolBarLayout.addWidget(driveViewBtn)

        # # recently accessed files.
        # recentBtn = QToolButton()
        # recentBtn.setIcon(FigIcon("fileviewer/recent.svg"))
        # propLayout.addWidget(recentBtn)
        # # view hidden files.
        # unhideBtn = QToolButton()
        # unhideBtn.setIcon(FigIcon("fileviewer/unhide.svg"))
        # unhideBtn.clicked.connect(lambda: self.unhide(self.path))
        # propLayout.addWidget(unhideBtn)

        # hideBtn = QToolButton()
        # hideBtn.setIcon(FigIcon("fileviewer/hide.svg"))
        # hideBtn.clicked.connect(lambda: self.refresh(self.path))
        # propLayout.addWidget(hideBtn)
        # # viewLayout.addWidget(QVLine())
        # listViewBtn = QToolButton() # toggle list view.
        # listViewBtn.setIcon(FigIcon("fileviewer/listview.svg"))
        # propLayout.addWidget(listViewBtn)

        # blockViewBtn = QToolButton() # toggle block view.
        # blockViewBtn.setIcon(FigIcon("fileviewer/blockview.svg"))
        # propLayout.addWidget(blockViewBtn) 

        # # right spacer.
        # right_spacer = QWidget()
        # right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # propLayout.addWidget(right_spacer)

        # construct groups
        layoutLayout.addWidget(layoutToolBar)
        layoutLabel = QLabel("Layout")
        layoutLabel.setAlignment(Qt.AlignCenter)
        layoutLabel.setMaximumHeight(30)
        layoutLayout.addWidget(layoutLabel)
        layoutGroup.setLayout(layoutLayout)

        # add all groups
        viewLayout.addWidget(layoutGroup)
        viewLayout.addWidget(self.addSpacer())
        viewLayout.addWidget(self.addStretch())
        viewMenu.setLayout(viewLayout)

        return viewMenu

    def initPropMenu(self):
        propMenu = QWidget()

        return propMenu

    def initShareMenu(self):
        shareMenu = QWidget()

        return shareMenu

    def initEditMenu(self):
        editMenu = QWidget()
        editLayout = QHBoxLayout()
        editLayout.setSpacing(0)
        editLayout.setContentsMargins(0, 0, 0, 0)
        # control groups
        moveGroup = QWidget() 
        moveLayout = QVBoxLayout()
        moveLayout.setSpacing(0)
        moveLayout.setContentsMargins(0, 0, 0, 0)
        
        moveLowerRibbon = QWidget()
        moveUpperRibbon = QWidget()
        moveLowerRibbonLayout = QHBoxLayout()
        moveUpperRibbonLayout = QHBoxLayout()
        moveUpperRibbonLayout.setSpacing(0)
        moveLowerRibbonLayout.setSpacing(0)
        moveUpperRibbonLayout.setContentsMargins(0, 0, 0, 0)
        moveLowerRibbonLayout.setContentsMargins(0, 0, 0, 0)     
        
        # cut file/folder
        cutBtn = QToolButton()
        cutBtn.setIcon(FigIcon("fileviewer/cut.png"))
        cutBtn.setIconSize(QSize(22,22))
        cutBtn.setText("Cut")
        cutBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        moveUpperRibbonLayout.addWidget(cutBtn)
        # copy file/folder
        copyBtn = QToolButton()
        copyBtn.setIcon(FigIcon("fileviewer/copy.png"))
        copyBtn.setIconSize(QSize(22,22))
        copyBtn.setText("Copy")
        copyBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        moveUpperRibbonLayout.addWidget(copyBtn)
        # paste file/folder
        pasteBtn = QToolButton()
        pasteBtn.setIcon(FigIcon("fileviewer/paste.png"))
        pasteBtn.setIconSize(QSize(22,22))
        pasteBtn.setText("Paste")
        pasteBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        moveUpperRibbonLayout.addWidget(pasteBtn)
        # editLayout.addWidget(QVLine())
        # undo
        undoBtn = QToolButton()
        undoBtn.setIcon(FigIcon("fileviewer/undo.svg"))
        undoBtn.setIconSize(QSize(22,22))
        # undoBtn.setText("Undo")
        # undoBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        moveLowerRibbonLayout.addWidget(undoBtn)
        # redo
        redoBtn = QToolButton()
        redoBtn.setIcon(FigIcon("fileviewer/redo.svg"))
        redoBtn.setIconSize(QSize(22,22))
        # redoBtn.setText("Redo")
        # redoBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        moveLowerRibbonLayout.addWidget(redoBtn)
        # copy absolute path.
        copyPathBtn = QToolButton()
        copyPathBtn.setIcon(FigIcon("fileviewer/copy_path.png"))
        copyPathBtn.setIconSize(QSize(22,22))
        # copyPathBtn.setText("Copy Path")
        copyPathBtn.clicked.connect(self.copyPathToClipboard)
        # copyPathBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        moveLowerRibbonLayout.addWidget(copyPathBtn)

        moveLowerRibbon.setLayout(moveLowerRibbonLayout)
        moveUpperRibbon.setLayout(moveUpperRibbonLayout)   
        moveLayout.addWidget(moveUpperRibbon)
        moveLayout.addWidget(moveLowerRibbon)
        moveGroupLabel = QLabel("Move") 
        moveGroupLabel.setAlignment(Qt.AlignCenter)
        moveLayout.addWidget(moveGroupLabel)

        moveGroup.setLayout(moveLayout)

        # add all groups
        editLayout.addWidget(moveGroup)
        editLayout.addWidget(self.addSpacer())
        editLayout.addWidget(self.addStretch())
        editMenu.setLayout(editLayout)

        return editMenu

    def initNavBar(self):
        navbar = QWidget()
        navLayout = QHBoxLayout() 
        # step back one folder.
        backBtn = QToolButton()
        backBtn.setIcon(FigIcon("fileviewer/stepback.svg"))
        backBtn.clicked.connect(self.back)
        navLayout.addWidget(backBtn)
        # prev item
        prevBtn = QToolButton()
        prevBtn.setIcon(FigIcon("fileviewer/back.svg"))
        prevBtn.clicked.connect(self.prevPath)
        navLayout.addWidget(prevBtn)
        # next item
        nextBtn = QToolButton()
        nextBtn.setIcon(FigIcon("fileviewer/forward.svg"))
        nextBtn.clicked.connect(self.nextPath)
        navLayout.addWidget(nextBtn)
        # search bar
        searchBar = QLineEdit()
        searchBar.setStyleSheet("background: #fff; color: #000")
        searchBar.setMinimumWidth(550)
        navLayout.addWidget(searchBar)
        # search button
        searchBtn = QToolButton()
        searchBtn.setIcon(FigIcon("fileviewer/search.svg"))
        searchBtn.setStyleSheet("border: 0px")
        navLayout.addWidget(searchBtn)
        # match case.
        caseBtn = QToolButton()
        caseBtn.setIcon(FigIcon("fileviewer/case-sensitive.svg"))
        # caseBtn.clicked.connect(self.back)
        navLayout.addWidget(caseBtn)
        # match whole word.
        entireBtn = QToolButton()
        entireBtn.setIcon(FigIcon("fileviewer/whole-word.svg"))
        # backBtn.clicked.connect(self.back)
        navLayout.addWidget(entireBtn)
        # use regex search
        regexBtn = QToolButton()
        regexBtn.setIcon(FigIcon("fileviewer/regex_search.svg"))
        # regexBtn.clicked.connect(self.back)
        navLayout.addWidget(regexBtn)
        navLayout.addStretch(1)

        navLayout.setContentsMargins(5, 0, 5, 0)
        navbar.setLayout(navLayout) 

        return navbar

    def addStretch(self):
        stretchGroup = QWidget()
        stretchGroup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return stretchGroup

    def addSpacer(self, width=10, background=None):
        if background is None: 
            background = self.bgStyle
        spacer = QFrame(self)
        spacer.setStyleSheet('''
            QFrame {
                border: 0px;
                background: '''+background+''';
            }
            QFrame::VLine{
                border: 1px;
            }''')
        spacer.setFrameShape(QFrame.VLine)
        spacer.setFrameShadow(QFrame.Sunken)
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        spacer.setFixedWidth(width)

        return spacer

    def initPropBar(self):
        '''
        Initialize properties bar.
        Properties bar contains:
        1. Bookmarking
        2. View bookmarked files
        3. Restricting file visibility (TODO)
        4. Changing user's file access permissions
        5. Changing read/write/execute permissions
        6. Open properties
        7. Open in terminal
        8. Open with xdg-open (for linux)
        9. Encrypt
        10. Decrypt
        11. Zip folder/file
        12. Unzip zip file
        13. Add/Edit/View note
        14. Add/Edit/View tags
        '''
        propbar = QWidget()
        propbar.setStyleSheet('''
        QToolButton:hover {
            background: red;
        }
        ''')
        propLayout = QHBoxLayout()
        # left spacer.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        propLayout.addWidget(left_spacer)
        # bookmark files.
        bookmarkBtn = QToolButton()
        bookmarkBtn.setIcon(FigIcon("fileviewer/bookmark.svg"))
        propLayout.addWidget(bookmarkBtn) 
        # view bookmarked files.
        bookmarkedBtn = QToolButton()
        bookmarkedBtn.setIcon(FigIcon("fileviewer/bookmarked.svg"))
        propLayout.addWidget(bookmarkedBtn)        
        # restrict files from other users.
        # restrictBtn = QToolButton()
        # restrictBtn.setIcon(FigIcon("bookmark.svg"))
        # propLayout.addWidget(restrictBtn)
        # change permissions (user access group.)
        userpermBtn = QToolButton()
        userpermBtn.setIcon(FigIcon("fileviewer/user_permissions.svg")) 
        propLayout.addWidget(userpermBtn) 
        # change r/w/x permissions.
        rwxpermBtn = QToolButton()
        rwxpermBtn.setIcon(FigIcon("fileviewer/permissions.svg"))
        propLayout.addWidget(rwxpermBtn)
        propLayout.addWidget(QVLine())
        # properties of selected file/folder.
        propBtn = QToolButton()
        propBtn.setIcon(FigIcon("fileviewer/properties.svg"))
        propLayout.addWidget(propBtn)
        # encrypt
        encryptBtn = QToolButton()
        encryptBtn.setIcon(FigIcon("fileviewer/encrypt.svg"))
        propLayout.addWidget(encryptBtn)
        # decrypt 
        decryptBtn = QToolButton()
        decryptBtn.setIcon(FigIcon("fileviewer/decrypt.svg"))
        propLayout.addWidget(decryptBtn)
        propLayout.addWidget(QVLine())
        # zip
        zipBtn = QToolButton()
        zipBtn.setIcon(FigIcon("fileviewer/zip.svg"))
        propLayout.addWidget(zipBtn)
        # unzip
        unzipBtn = QToolButton()
        unzipBtn.setIcon(FigIcon("fileviewer/zip.svg"))
        propLayout.addWidget(unzipBtn)
        # view and edit tags
        vETagsBtn = QToolButton()
        vETagsBtn.setIcon(FigIcon("fileviewer/tags.svg"))
        propLayout.addWidget(vETagsBtn)
        # file share.
        fileShareBtn = QToolButton()
        fileShareBtn.setIcon(FigIcon("fileviewer/file_share.svg"))
        propLayout.addWidget(fileShareBtn)
        # email file/folder.
        emailBtn = QToolButton()
        emailBtn.setIcon(FigIcon("fileviewer/email.svg"))
        propLayout.addWidget(emailBtn)

        #####
        propLayout.setContentsMargins(5, 0, 5, 0)
        propbar.setLayout(propLayout)        

        return propbar

    def initEditBar(self):
        '''
        Initialize edit bar.
        Edit bar contains:
        1. Go back a folder
        2. Prev item in history (nav)
        3. Next item in history (nav)
        4. Cut 
        5. Copy
        6. Paste
        7. Undo
        8. Redo
        9. Create new file
        10. Create new folder
        11. Rename
        12. Delete
        13. Share file
        14. Email file
        15. Match case
        16. Match whole phrase
        17. Regex pattern matching for search
        18. Filter
        19. Filter add
        20. Filter edit
        21. Filter delete
        22. Filter heart (favourite)
        23. Filter check
        '''    
        editbar = QWidget()
        editbar.setStyleSheet('''
        QToolButton:hover {
            background: red;
        }
        ''')
        editLayout = QHBoxLayout()
        # left spacer.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        editLayout.addWidget(left_spacer)
        # new file
        newFileBtn = QToolButton()
        newFileBtn.setIcon(FigIcon("fileviewer/new_file.svg"))
        editLayout.addWidget(newFileBtn)
        # new folder
        newFolderBtn = QToolButton()
        newFolderBtn.setIcon(FigIcon("fileviewer/new_folder.svg"))
        editLayout.addWidget(newFolderBtn)
        # editLayout.addWidget(QVLine())
        # new softlink
        newLinkBtn = QToolButton()
        newLinkBtn.setIcon(FigIcon("fileviewer/softlink.svg"))
        editLayout.addWidget(newLinkBtn)
        # unlink
        unLinkBtn = QToolButton()
        unLinkBtn.setIcon(FigIcon("fileviewer/unlink.svg"))
        editLayout.addWidget(unLinkBtn)
        # rename
        renameBtn = QToolButton()
        renameBtn.setIcon(FigIcon("fileviewer/rename.svg"))
        editLayout.addWidget(renameBtn)
        # delete
        delBtn = QToolButton()
        delBtn.setIcon(FigIcon("fileviewer/delete.svg"))
        editLayout.addWidget(delBtn)  
        editLayout.addWidget(QVLine())
        # filter buttons
        filterBtn = QToolButton()
        filterBtn.setIcon(FigIcon("fileviewer/filter.svg"))
        editLayout.addWidget(filterBtn)
        filtAddBtn = QToolButton()
        filtAddBtn.setIcon(FigIcon("fileviewer/filter_add.svg"))
        editLayout.addWidget(filtAddBtn)
        filtDelBtn = QToolButton()
        filtDelBtn.setIcon(FigIcon("fileviewer/filter_delete.svg"))
        editLayout.addWidget(filtDelBtn)
        filtEditBtn = QToolButton()
        filtEditBtn.setIcon(FigIcon("fileviewer/filter_edit.svg"))
        editLayout.addWidget(filtEditBtn)
        filtFavBtn = QToolButton()
        filtFavBtn.setIcon(FigIcon("fileviewer/filter_heart.svg"))
        editLayout.addWidget(filtFavBtn)
        filtStarBtn = QToolButton()
        filtStarBtn.setIcon(FigIcon("fileviewer/filter_star.svg"))
        editLayout.addWidget(filtStarBtn)
        filtCheckBtn = QToolButton()
        filtCheckBtn.setIcon(FigIcon("fileviewer/filter_check.svg"))
        editLayout.addWidget(filtCheckBtn)
        filtStarBtn = QToolButton()
        filtStarBtn.setIcon(FigIcon("fileviewer/filter_remove.svg"))
        editLayout.addWidget(filtStarBtn)
        # editLayout.addWidget(QVLine())
        # right spacer.
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        editLayout.addWidget(left_spacer)

        editLayout.setContentsMargins(5, 0, 5, 0)
        editbar.setLayout(editLayout)

        return editbar

    def openInTermTab(self):
        '''
        Check which file/folder is currently selected and open it in a new term tab.
        '''        
        selBtn = self.gridLayout.itemAt(self.j).widget()
        # accessing the FigWindow
        if self._parent:
            self._parent.addNewTerm(path=selBtn.path)

    def copyPathToClipboard(self):
        '''
        Check which file/folder is currently selected and copy it's path to the clipboard.
        '''
        selBtn = self.gridLayout.itemAt(self.j).widget()
        # accessing the FigWindow
        if self._parent:
            self._parent.clipboard.setText(selBtn.path)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information) # set icon
        msg.setText("Path copied to clipboard") # set text
        msg.setInformativeText(f"{selBtn.path} copied to clipboard !")
        msg.setWindowTitle("Fig::FileViewer")
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        msg.setGeometry(200, 200, 500, 50)
        _ = msg.exec_()

    def initUtilBar(self):
        utilbar = QWidget()
        utilLayout = QHBoxLayout() # bookmarks, restricted view, change permissions, encrypt, zip/unzip, new folder, new file, undo/redo, cut/copy/paste, rename, open in terminal, properties.

        utilLayout.setContentsMargins(5, 0, 5, 0)
        utilbar.setLayout(utilLayout)

        return utilbar

    # def eventFilter(self, obj, event):
    #     if (event.type() == QEvent.Resize):
    #         print( 'Inside event Filter')
    #     return super().eventFilter(obj, event)

    def highlightOnClick(self):
        # sendingBtn = self.sender().parent()
        sendingBtn = self.sender()
        j = self.gridLayout.indexOf(sendingBtn)
        self.highlight(j)
    def clear(self):
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)
        self.j = 0

    def highlight(self, j):
        try:
            selBtn = self.gridLayout.itemAt(self.j).widget()
            selBtn.unselect()
            selBtn.setAttribute(Qt.WA_TranslucentBackground)
            self.j = j
            selBtn = self.gridLayout.itemAt(self.j).widget()
            # selBtn.setStyleSheet("background: #ff5e00; color: #292929; font-weight: bold")
            selBtn.select()
        except AttributeError:
            # to handle empty folders.
            self.back()
    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.KeyPress:
    #         print(event.key())
    #     return super(FigFileViewer, self).eventFilter(source, event)
    def prevPath(self):
        self.historyIter -= 1
        self.historyIter = max(0, self.historyIter)
        path = self.history[self.historyIter]
        self.refresh(path)

    def nextPath(self):
        self.historyIter += 1
        self.historyIter = min(len(self.history)-1, self.historyIter)
        path = self.history[self.historyIter]
        self.refresh(path)

    def back(self):
        path = self.curr_path
        path = pathlib.Path(path).parent
        self.curr_path = path
        self.history.append(path)
        self.historyIter += 1
        self.refresh(path)

    def openPath(self, path):
        self.curr_path = path
        # print(f"opened {path}") # DEBUG
        if not os.path.isfile(path):
            self.history.append(path)
            self.historyIter += 1
            self.refresh(path)
        else:
            # call file handler for the extension here
            pass

    def listFiles(self, path, hide=True, reverse=False):
        home = str(pathlib.Path.home())
        # setting desktop background.
        desktop = os.path.join(home, "Desktop")
        try:
            if path == desktop:
                wallpaper_path = getWallpaper()
                self.viewer.setStyleSheet(f"background-image: url({wallpaper_path});")
            else:
                self.viewer.setStyleSheet("background-image: none")
        except AttributeError:
            pass
        
        files = []
        try:
            # print("reverse:", reverse)
            for file in os.listdir(path):
                if not(file.startswith(".") and hide):
                    files.append(os.path.join(path, file))
            return sorted(files, key= lambda x: x.lower(), reverse=reverse)
        except PermissionError:
            return files

    def updateFolderBar(self, path, viewer=None):
        folderBtnStyle = '''
        QPushButton:hover{
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6e);
        }

        QPushButton {
                border: 1px solid;
                border-radius: 2px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
                margin-left: 2px;
                margin-right: 4px;
                padding-top: 4px;
                padding-bottom: 4px;
                padding-left: 5px;
                padding-right: 5px;
                font-size: 16px;
        }
        '''
        selFolderBtnStyle = '''
        QPushButton:hover{
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6e);
        }

        QPushButton {
                border: 1px solid;
                border-radius: 2px;
                background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
                margin-left: 2px;
                margin-right: 2px;
                padding-top: 4px;
                padding-bottom: 4px;
                padding-left: 5px;
                padding-right: 5px;
                font-weight: bold; 
                color: #ff9100;
                font-size: 16px;
        }
        '''
        if self.folderBar.path.startswith(str(path)): 
            # selectedBtn = self.sender()
            # print(selectedBtn)
            # selectedBtn.setStyleSheet(selFolderBtnStyle)
            return

        for action in self.folderBarActions:
            self.folderBar.removeAction(action)
        self.folderBarActions = []
        path = str(path)
        
        folders = path.split('/')
        till_now = "/" # running variable for subpath till now.
        for i,folder in enumerate(folders):
            if folder != "":
                till_now = os.path.join(till_now, folder)
                btn = QFolderNavBtn(folder, till_now)
                # event handler for click will be attached to open the subpath till now.
                if viewer:
                    btn.connectLauncher(viewer)
                # color the active button differently
                if i == len(folders)-1:
                    btn.setStyleSheet(selFolderBtnStyle)
                else:
                    btn.setStyleSheet(folderBtnStyle)
                action = self.folderBar.addWidget(btn)
                self.folderBarActions.append(action)
        self.folderBar.path = str(path)

    def refresh(self, path, reverse=False):
        '''launch worker to refresh file layout..'''
        import time
        start = time.time()
        self.clear()
        global GLOBAL_FILE_LIST
        GLOBAL_FILE_LIST = []
        if self.window:
            i = self._parent.tabs.currentIndex()
            name = pathlib.Path(path).name
            parent = pathlib.Path(path).parent.name
            self.updateFolderBar(path, viewer=self)
            self._parent.tabs.setTabText(i, f"{name} .../{parent}")
            self._parent.log("launcher/fileviewer.png", str(path))
            # print("refreshing view ...")
            # self._parent.setWindowTitle("Loading")
        print(f"refreshing {path}")
        self.refresh_thread = QThread()
        self.refresh_worker = FileViewerRefreshWorker(listdir(path, reverse=reverse), is_iter=False)
        self.refresh_worker.moveToThread(self.refresh_thread)
        self.refresh_thread.started.connect(self.refresh_worker.run)
        # self.refresh_worker.finished.connect(lambda: self.highlight(0))
        self.refresh_worker.finished.connect(self.refresh_thread.quit)
        self.refresh_worker.finished.connect(self.refresh_worker.deleteLater)
        self.refresh_thread.finished.connect(self.refresh_thread.deleteLater)
        self.refresh_worker.progress.connect(self.reportProgress)
        self.refresh_thread.start()
        self.viewer.setStyleSheet(f"background: {Fig.FileViewer._FVBG}")
        # self.highlight(0)     
        # print("refreshed in:", time.time()-start)
    
    def reportProgress(self, i):
        global GLOBAL_FILE_LIST
        fileIcon = FigFileIcon(GLOBAL_FILE_LIST[i], parent=self)
        fileIcon.clicked.connect(self.open)
        self.gridLayout.addWidget(fileIcon)

    def _refresh(self, path, reverse=False):
        '''function to be executed inside the worker.'''
        self.clear()
        if self._parent:
            i = self._parent.tabs.currentIndex()
            name = pathlib.Path(path).name
            parent = pathlib.Path(path).parent.name
            self.updateFolderBar(path, viewer=self)
            self._parent.tabs.setTabText(i, f"{name} .../{parent}")
            self._parent.log("launcher/fileviewer.png", str(path))
        all_files = self.listFiles(path, reverse=reverse) # get list of all files and folders.
        
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            ### replace with FlowLayout ###
            self.gridLayout.addWidget(fileIcon)  
            # self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
            ###############################
        self.viewer.setStyleSheet(f"background: {Fig.FileViewer._FVBG}")
        self.highlight(0)        

    def initFolderNavBar(self):
        backBtnStyle = '''
        QPushButton:hover{
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6d);
        }

        QPushButton {
            border: 1px solid;
            border-radius: 2px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #6e6e6d, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
            margin-left: 1px;
            margin-right: 1px;
            padding-top: 2px;
            padding-bottom: 2px;
        }
        '''
        nextBtnStyle = '''
        QPushButton:hover{
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #6e6e6d, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
        }

        QPushButton {
            border: 1px solid;
            border-radius: 2px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 1, y2 : 0, stop : 0.0 #292929, stop : 0.2 #4a4a4a, stop : 1.0 #6e6e6d);
            margin-left: 1px;
            margin-right: 1px;
            padding-top: 2px;
            padding-bottom: 2px;
        }
        '''
        toolbar = QToolBar("Folder Navigation Bar Visibility")
        toolbar.setStyleSheet("border: 0px")
        toolbar.setStyleSheet("color: #fff; background: #292929; border: 0px; padding: 2px;")
        toolbar.setIconSize(QSize(22,22))
        toolbar.setMovable(False)

        backBtn = QPushButton()
        backBtn.setToolTip("go back in folders")
        backBtn.setStyleSheet(backBtnStyle)
        backBtn.setIcon(FigIcon("back.svg"))
        self.backNavBtn = backBtn

        nextBtn = QPushButton()
        nextBtn.setToolTip("go forward in folders")
        nextBtn.setStyleSheet(nextBtnStyle)
        nextBtn.setIcon(FigIcon("forward.svg"))
        self.nextNavBtn = nextBtn

        toolbar.addWidget(backBtn)
        toolbar.addWidget(nextBtn)
        toolbar.addSeparator()
        # add actions.
        self.folderBarActions = []

        return toolbar

    def unhide(self, path):        
        self.clear()
        all_files = self.listFiles(path, hide=False) # get list of all files and folders.
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            ### replace with FlowLayout ###
            # self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
            self.gridLayout.addWidget(fileIcon)
            ###############################
        self.highlight(0)   

    def open(self):
        sendingBtn = self.sender()
        j = self.gridLayout.indexOf(sendingBtn)
        if j != self.j:
            self.highlight(j)
            return
        if not sendingBtn.file.isfile:
            # print("opening folder:", sendingBtn.file.path)
            path = sendingBtn.file.path
            self.curr_path = path
            self.history.append(path)
            self.historyIter += 1
            self.refresh(path)
        else:
            if self.window: # call file handler for the extension here
                path = sendingBtn.file.path
                print(f"getting handler for {path}")
                
                handlerWidget = self.window.handler.getUI(path)
                thumbnail = sendingBtn.file.thumbnail
                
                i = self.window.tabs.addTab(handlerWidget, FigIcon(thumbnail), f"\t{sendingBtn.file.name} .../{sendingBtn.file.parent}")
                self.window.tabs.setCurrentIndex(i)

    def sideBarToLeft(self):
        self.scrollArea.hide()
        self.sideBar.hide()
        self.overallViewer.addWidget(self.sideBar)
        self.overallViewer.addWidget(self.scrollArea)
        self.scrollArea.show()
        self.sideBar.show()

    def sideBarToRight(self):
        self.scrollArea.hide()
        self.sideBar.hide()
        self.overallViewer.addWidget(self.scrollArea)
        self.overallViewer.addWidget(self.sideBar)
        self.scrollArea.show()
        self.sideBar.show()

class FigTreeFileExplorer(QWidget):
    def __init__(self, root_path="/home/atharva", parent=None):
        super(FigTreeFileExplorer, self).__init__(parent)
        # veritcal layout.
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(root_path))
        # root path.
        self.fileRoot = root_path
        # file system model.
        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(QDir.currentPath())
        # file tree view.
        self.fileTree = QTreeView()
        self.fileTree.setModel(self.fileModel)
        self.fileTree.setRootIndex(
            self.fileModel.index(
                QDir.currentPath()
            )
        )
        # hide Size, Type and Date Modified.
        self.fileTree.hideColumn(1)
        self.fileTree.hideColumn(2)
        self.fileTree.hideColumn(3)
        # hide scroll bar.
        self.fileTree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # add file tree to layout.
        layout.addWidget(self.fileTree)

        self.setLayout(layout)
        self.visible = False
        self.setStyleSheet('''
            background: #292929;
            color: #fff;
        ''')
        self.hide()

    def toggle(self):
        if self.visible: self.hide()
        else: self.show()
        self.visible = not self.visible            


if __name__ == "__main__":
    FigFileViewer("/home/atharva/GUI/FigUI")
    # def _setThumbnailMime(self):
    #     _,ext = os.path.splitext(self.name)
    #     # print(self.name, self.stem, ext, os.path.isfile(self.path))
    #     ext = ext[1:]
    #     if self.name == ".git":
    #         self.setIcon(FigIcon("launcher/git.png"))
    #         return
    #     elif self.name == "pom.xml":
    #         self.setIcon(FigIcon("launcher/pom.png"))
    #         return
    #     elif self.name.lower() == "todo":
    #         self.setIcon(FigIcon("launcher/todo.png"))
    #         return
    #     elif not self.isfile:
    #         for phrase in ["nano", "eclipse", "cache", "java", "cargo", "compiz", "aiml", "kivy", "netbeans", "mozilla"]:
    #             if phrase in self.name.lower():
    #                 self.setIcon(FigIcon(f"launcher/{phrase}.png"))
    #                 return
    #         if self.name == "Music":
    #             self.setIcon(FigIcon("launcher/Music.svg"))
    #         elif self.name in ["Videos", "Desktop", "Documents", "Downloads", "Pictures"]:
    #             self.setIcon(FigIcon(f"launcher/{self.name}.png"))
    #         elif self.name.startswith(".git"):
    #             self.setIcon(FigIcon("launcher/git.png"))
    #         elif self.name in [".rstudio-desktop"]:
    #             self.setIcon(FigIcon("launcher/R.png"))
    #         elif self.name in [".python-eggs"]:
    #             self.setIcon(FigIcon("launcher/python-eggs.png"))
    #         elif "android" in self.name.lower():
    #             self.setIcon(FigIcon("launcher/android.png"))
    #         elif "gnome" in self.name.lower():
    #             self.setIcon(FigIcon("launcher/gnome.png"))
    #         elif "anaconda" in self.name.lower() or self.name.startswith(".conda"):
    #             self.setIcon(FigIcon("launcher/anaconda3.png"))
    #         elif "jupyter" in self.name.lower() or "ipython" in self.name.lower() or "ipynb" in self.name.lower():
    #             self.setIcon(FigIcon("launcher/ipynb.png"))
    #         elif "julia" in self.name.lower():
    #             self.setIcon(FigIcon("launcher/jl.png"))
    #         elif "vscode" in self.name.lower():
    #             self.setIcon(FigIcon("launcher/notvscode.png"))
    #         elif "tor" in re.split("_| |-", self.name.lower()) or self.name == ".tor":
    #             self.setIcon(FigIcon("launcher/tor.png"))
    #         elif self.name in [".thunderbird", ".wine", ".dbus", ".ssh", ".npm", ".gradle", ".openoffice"]:
    #             self.setIcon(FigIcon(f"launcher/{self.name[1:]}.png"))
    #         elif self.name == ".linuxbrew" or self.name == "Homebrew":
    #             self.setIcon(FigIcon("launcher/brew.png"))
    #         elif self.name == ".cmake":
    #             self.setIcon(FigIcon("launcher/cmake.svg"))
    #         else:    
    #             self.setIcon(FigIcon("launcher/fileviewer.png"))
    #         return      

# def getThumbnail(path):
#     name = pathlib.Path(path).name 
#     _,ext = os.path.splitext(name)
#     stem = pathlib.Path(path).stem
#     # print(self.name, self.stem, ext, os.path.isfile(self.path))
#     ext = ext[1:]
#     if name.lower() == "todo": return "launcher/todo.png"
#     # elif ext in ["png","jpg"]: # display standard thumbnail for png/jpg.
#     #     return path
#     elif stem == "README": return "launcher/README.png"
#     elif stem == "requirements": return "launcher/requirements.png"
#     elif stem.lower() == "license": return "launcher/license.png"
#     elif stem == ".gitignore": return "launcher/gitignore.png"
#     elif ext == "":
#         if subprocess.getoutput(f"file --mime-encoding {path}").endswith("binary"):
#             return "launcher/bin.png"
#         else:
#             return "launcher/txt.png"
#     if os.path.exists(__icon__(f"launcher/{ext}.png")): # check if png file for the ext
#         return f"launcher/{ext}.png"
#     else:
#         if os.path.exists(__icon__(f"launcher/{ext}.svg")): 
#             return f"launcher/{ext}.svg"
#         else: 
#             return f"launcher/txt.png" # if ext is not recognized set it to txt

        # backBtn = QToolButton()
        # backBtn.setIcon(FigIcon("stepback.svg"))
        # backBtn.clicked.connect(self.back)
        # navLayout.addWidget(backBtn)
        
        # prevBtn = QToolButton()
        # prevBtn.setIcon(FigIcon("back.svg"))
        # prevBtn.clicked.connect(self.prevPath)
        # navLayout.addWidget(prevBtn)

        # nextBtn = QToolButton()
        # nextBtn.setIcon(FigIcon("forward.svg"))
        # nextBtn.clicked.connect(self.nextPath)
        # navLayout.addWidget(nextBtn)

        # self.scrollArea.setStyleSheet('''
        #     QScrollArea {
        #         background-color: rgba(73, 44, 94, 0.5);
        #     }
        #     QScrollBar:vertical {
        #         border: 0px solid #999999;
        #         width: 8px;    
        #         margin: 0px 0px 0px 0px;
        #         background-color: rgba(227, 140, 89, 0.5);
        #     }
        #     QScrollBar::handle:vertical {         
        #         min-height: 0px;
        #         border: 0px solid red;
        #         border-radius: 4px;
        #         background-color: #e38c59; /* #c70039; */
        #     }
        #     QScrollBar::add-line:vertical {       
        #         height: 0px;
        #         subcontrol-position: bottom;
        #         subcontrol-origin: margin;
        #     }
        #     QScrollBar::sub-line:vertical {
        #         height: 0 px;
        #         subcontrol-position: top;
        #         subcontrol-origin: margin;
        #     }
        #     /* QScrollBar:vertical {
        #         border: 0px solid #999999;
        #         width:14px;    
        #         margin: 0px 0px 0px 3px;
        #         background-color: rgba(73, 44, 94, 0.5);
        #     }
        #     QScrollBar::handle:vertical {         
        #         min-height: 0px;
        #         border: 0px solid red;
        #         border-radius: 5px;
        #         background-color: rgb(92, 95, 141);
        #     }
        #     QScrollBar::add-line:vertical {       
        #         height: 0px;
        #         subcontrol-position: bottom;
        #         subcontrol-origin: margin;
        #     }
        #     QScrollBar::sub-line:vertical {
        #         height: 0 px;
        #         subcontrol-position: top;
        #         subcontrol-origin: margin;
        #     } */
        #     QToolTip { border: 0px }
        # ''')
        # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_A:
    #         j = max(self.j-1,0)
    #     elif e.key() == Qt.Key_D:
    #         j = min(self.gridLayout.count()-1,self.j+1)
    #     elif e.key() == Qt.Key_W:
    #         j = max(self.j-self.width,0)
    #     elif e.key() == Qt.Key_S:
    #         j = min(self.gridLayout.count()-1,self.j+self.width)
    #     elif e.key() == Qt.Key_Return:
    #         selBtn = self.gridLayout.itemAt(self.j).widget()
    #         path = selBtn.path
    #         self.openPath(path)
    #         return
    #     else:
    #         return
    #     self.highlight(j)
    # def initViewBar(self):
    #     '''
    #     Initialize view bar.
    #     View bar contains:
    #     1. Sort ascending
    #     2. Sort descending
    #     3. Recently accessed
    #     4. Show hidden files (linux: . prefix)
    #     5. Hide hidden files
    #     6. Toggle list view
    #     7. Toggle block view
    #     '''
    #     viewbar = QWidget()
    #     viewLayout = QHBoxLayout()
    #     # left spacer.
    #     left_spacer = QWidget()
    #     left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    #     viewLayout.addWidget(left_spacer)
    #     # sort ascending.
    #     sortUpBtn = QToolButton()
    #     sortUpBtn.setIcon(FigIcon("fileviewer/sort_ascending.svg"))
    #     sortUpBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=False))
    #     viewLayout.addWidget(sortUpBtn)
    #     # sort descending.
    #     sortDownBtn = QToolButton()
    #     sortDownBtn.setIcon(FigIcon("fileviewer/sort_descending.svg"))
    #     sortDownBtn.clicked.connect(lambda: self.refresh(self.curr_path, reverse=True))
    #     viewLayout.addWidget(sortDownBtn)
    #     # viewLayout.addWidget(QVLine())
    #     # recently accessed files.
    #     recentBtn = QToolButton()
    #     recentBtn.setIcon(FigIcon("fileviewer/recent.svg"))
    #     # sortUpBtn.clicked.connect(self.nextPath)
    #     viewLayout.addWidget(recentBtn)
    #     # view hidden files.
    #     unhideBtn = QToolButton()
    #     unhideBtn.setIcon(FigIcon("fileviewer/unhide.svg"))
    #     unhideBtn.clicked.connect(lambda: self.unhide(self.curr_path))
    #     viewLayout.addWidget(unhideBtn)

    #     hideBtn = QToolButton()
    #     hideBtn.setIcon(FigIcon("fileviewer/hide.svg"))
    #     hideBtn.clicked.connect(lambda: self.refresh(self.curr_path))
    #     viewLayout.addWidget(hideBtn)
    #     # viewLayout.addWidget(QVLine())
    #     listViewBtn = QToolButton() # toggle list view.
    #     listViewBtn.setIcon(FigIcon("fileviewer/listview.svg"))
    #     viewLayout.addWidget(listViewBtn)

    #     blockViewBtn = QToolButton() # toggle block view.
    #     blockViewBtn.setIcon(FigIcon("fileviewer/blockview.svg"))
    #     viewLayout.addWidget(blockViewBtn)        
    #     # right spacer.
    #     right_spacer = QWidget()
    #     right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    #     viewLayout.addWidget(right_spacer)

    #     viewLayout.setContentsMargins(5, 0, 5, 0)
    #     viewbar.setLayout(viewLayout)

    #     return viewbar

# class FigFileIcon(QToolButton):
#     def __init__(self, path, parent=None, size=(150,150), textwidth=10):
#         super(FigFileIcon, self).__init__(parent)
#         self._parent = parent
#         self.name = pathlib.Path(path).name
#         self.path = path
#         self.isfile = os.path.isfile(path)
#         self.stem = pathlib.Path(path).stem
#         self.defaultStyle = '''
#         QToolTip {
#             border: 0px;
#             color: #fff;
#         }
#         QToolButton { 
#             border: 0px; 
#             background: transparent;
#             background-image: none;
#             color: #fff;
#             margin: 10px;
#         }
#         QToolButton:hover {
#             background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); 
#             /* #e38c59; */ /* #009b9e; */
#             color: #292929;
#             font-weight: bold;
#         }        
#         ''' 
#         self.selectedStyle = '''
#         QToolTip {
#             border: 0px;
#             color: #fff;
#         }
#         QToolButton { 
#             '''+f"background: {Fig.FileViewer.SCHEX};"+'''
#             background-image: none;
#             color: #292929;
#             font-weight: bold;
#             margin: 10px;
#         }    
#         ''' 
#         self.setStyleSheet(self.defaultStyle)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
#         text = "\n".join(textwrap.wrap(self.name[:textwidth*3], width=textwidth))
#         self.setAttribute(Qt.WA_TranslucentBackground, True)
#         self.setText(text) # truncate at 3 times the max textwidth
#         self.setFixedSize(QSize(*size))
#         self.setIconSize(QSize(50,50))
#         self._getFileProperties()
#         self._setThumbnail()
#         self._setPropertiesTip()

#     def unselect(self):
#         self.setStyleSheet(self.defaultStyle)

#     def select(self):
#         self.setStyleSheet(self.selectedStyle)

#     def _getMimeType(self):
#         mimeType,_ = mimetypes.guess_type(self.path) 
#         if not self.isfile:
#             return "Folder"
#         elif mimeType:
#             return mimeType
#         else:
#             if PLATFORM == "Linux":
#                 cmd = f"file --mime-type {self.path}"
#                 op = subprocess.getoutput(cmd)
#                 return op.split()[-1]
#             else:
#                 return "Unknown"

#     def _getFileProperties(self):
#         try:
#             stat = os.stat(self.path)
#         except (PermissionError, FileNotFoundError) as e: 
#             self.props = argparse.Namespace()
#             self.props.access_time = datetime.datetime.now().strftime("%b,%b %d %Y %H:%M:%S")
#             self.props.modified_time = datetime.datetime.now().strftime("%b,%b %d %Y %H:%M:%S")
#             self.props.size = "0B"
#             return 
#         self.props = argparse.Namespace()
#         if PLATFORM == "Linux":
#             self.props.access_time = datetime.datetime.fromtimestamp(stat.st_atime).strftime("%b,%b %d %Y %H:%M:%S")
#             self.props.modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%b,%b %d %Y %H:%M:%S")
#             self.props.size = sizeof_fmt(stat.st_size)
#         elif PLATFORM == "Windows":
#             pass
#         elif PLATFORM == "Darwin":
#             pass
#         else:
#             pass

#     def _setPropertiesTip(self):
#         properties = f'''
# Name: {self.name}
# Type: {self._getMimeType()}
# Size: {self.props.size}

# Location: {self.path}

# Accessed: {self.props.access_time} 
# Modified: {self.props.modified_time}
# '''
#         self.setToolTip(properties)

#     def _setThumbnail(self):
#         _,ext = os.path.splitext(self.name)
#         # print(self.name, self.stem, ext, os.path.isfile(self.path))
#         ext = ext[1:]
#         if self.name == ".git":
#             self.setIcon(FigIcon("launcher/git.png"))
#             return
#         elif self.name == "pom.xml":
#             self.setIcon(FigIcon("launcher/pom.png"))
#             return
#         elif self.name.lower() == "todo":
#             self.setIcon(FigIcon("launcher/todo.png"))
#             return
#         elif not self.isfile:            
#             # phrase contained case.
#             for phrase in ThumbPhrases:
#                 if phrase in self.name.lower():
#                     self.setIcon(FigIcon(f"launcher/{phrase}.png")); return 
            
#             if self.name in ThumbMap:
#                 filename = ThumbMap[self.name]
#                 self.setIcon(FigIcon(f"launcher/{filename}"))
#             # elif self.name == ".sbt":
#             #     self.setIcon(FigIcon("launcher/scala.png"))
#             elif self.name.startswith(".git"):
#                 self.setIcon(FigIcon("launcher/git.png"))

#             elif "julia" in self.name.lower():
#                 self.setIcon(FigIcon("launcher/jl.png"))
#             elif "netbeans" in self.name.lower():
#                 self.setIcon(FigIcon("launcher/netbeans.svg"))
#             elif "vscode" in self.name.lower():
#                 self.setIcon(FigIcon("launcher/notvscode.png"))

#             elif self.stem == ".gconf":
#                 self.setIcon(FigIcon("launcher/gnome.png"))
#             elif self.stem == ".fontconfig":
#                 self.setIcon(FigIcon("launcher/ttf.svg"))
#             elif "anaconda" in self.name.lower() or self.name.startswith(".conda"):
#                 self.setIcon(FigIcon("launcher/anaconda3.png"))

#             elif "jupyter" in self.name.lower() or "ipython" in self.name.lower() or "ipynb" in self.name.lower():
#                 self.setIcon(FigIcon("launcher/ipynb.png"))

#             elif "tor" in re.split("_| |-", self.name.lower()) or self.name == ".tor":
#                 self.setIcon(FigIcon("launcher/tor.png"))
#             elif self.name == ".linuxbrew" or self.name == "Homebrew":
#                 self.setIcon(FigIcon("launcher/brew.png"))
#             # elif self.name == "cuda":
#             #     self.setIcon(FigIcon("launcher/cu.png"))
#             elif self.name in [".gnupg"]:
#                 self.setIcon(FigIcon("launcher/gnu.png"))
#             elif self.path in STDLinuxFolders:
#                 self.setIcon(FigIcon(f"dir/{self.name}.png"))
#             else:    
#                 self.setIcon(FigIcon("launcher/fileviewer.png"))
#             return
#         elif ext in ["STL", "OBJ"]:
#             self.setIcon(FigIcon(f"launcher/{ext.lower()}.png"))
#             return
#         elif ext in ["png","jpg","svg"]:
#             self.setIcon(QIcon(self.path))
#             return
#         # elif ext in ["webm", "mp4", "flv", "ogv", "wmv", "mov"]:
#         #     import moviepy.editor
#         #     with tempfile.NamedTemporaryFile() as temp:
#         #         os.rename(temp.name, temp.name+'.jpg')
#         #         clip = moviepy.editor.VideoFileClip(self.path)
#         #         clip.save_frame(temp.name+'.jpg',t=1.0)
#         #         self.setIcon(QIcon(temp.name+'.jpg'))
#         #         os.rename(temp.name+'.jpg', temp.name)
#         #     return
#         # elif self.stem in ["README", "requirements"]:
#         #     self.setIcon(FigIcon(f"launcher/{self.stem}.png"))
#         #     return
#         elif self.name == ".profile":
#             self.setIcon(FigIcon("launcher/bashrc.png"))
#             return  
#         elif self.stem.lower() == "license":
#             self.setIcon(FigIcon("launcher/license.png"))
#             return              
#         # REMOVE #
#         elif self.stem.startswith(".bash"):
#             self.setIcon(FigIcon("launcher/bashrc.png"))
#             return  
#         elif self.stem.startswith("zsh"):
#             self.setIcon(FigIcon("launcher/bashrc.png"))
#             return  
#         elif self.stem.startswith(".conda"):
#             self.setIcon(FigIcon("launcher/anaconda3.png"))
#             return
#         elif self.stem.startswith("nvidia-"):
#             self.setIcon(FigIcon("launcher/cu.png"))
#             return
#         elif self.name.startswith(".nvidia"):
#             self.setIcon(FigIcon("launcher/cu.png"))
#             return
#         # REMOVE #
#         elif self.name.startswith(".") and "cookie" in self.name:
#             self.setIcon(FigIcon("launcher/cookie.png"))
#             return

#         elif self.stem in StemMap:
#             filename = StemMap[self.stem]
#             self.setIcon(FigIcon(f"launcher/{filename}"))
#             return    

#         elif self.stem.endswith("_history"):
#             self.setIcon(FigIcon("launcher/history.png"))
#             return
   
#         # txt/bin classification.
#         elif ext == "":
#             if subprocess.getoutput(f"file --mime-encoding {self.path}").endswith("binary"):
#                 self.setIcon(FigIcon("launcher/bin.png"))    
#             else:
#                 self.setIcon(FigIcon("launcher/txt.png"))
#             return

#         for prefix in PrefixMap:
#             if self.stem.startswith(prefix):
#                 filename = PrefixMap[prefix]
#                 self.setIcon(FigIcon(f"launcher/{filename}")) 
#                 return
#         # check for .ext kind of files.
#         if os.path.exists(__icon__(f"launcher/{ext}.png")): # check if png file for the ext
#             self.setIcon(FigIcon(f"launcher/{ext}.png"))
#         else:
#             if os.path.exists(__icon__(f"launcher/{ext}.svg")): 
#                 self.setIcon(FigIcon(f"launcher/{ext}.svg")) # check if svg file exists for the ext
#             else: 
#                 # print(self.name)
#                 self.setIcon(FigIcon(f"launcher/txt.png")) # if ext is not recognized set it to txt