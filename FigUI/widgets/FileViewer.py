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
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor
from PyQt5.QtWidgets import QAction, QWidget, QTabWidget, QToolBar, QTabBar, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QGraphicsView, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox, QTreeView, QRubberBand,  QFileSystemModel, QGraphicsDropShadowEffect

try:
    from utils import *
    from widgets.FlowLayout import FlowLayout
except ImportError:
    from FigUI.utils import *
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

STDLinuxFolders = ["/bin", "/home", "/boot", "/etc", "/opt", "/cdrom", "/proc", "/root", "/sbin", "/usr", "/dev", "/lost+found", "/var", "/tmp", "/snap", "/media", "/lib", "/lib32", "/lib64", "/mnt"]
ThumbPhrases = ["android", "gnome", "nano", "eclipse", "cache", "java", "cargo", "compiz", "aiml", "kivy", "mozilla"]
# map for getting filenames for thumbnails given the folder name.
ThumbMap = {
            "cuda": "cu.png",
            ".sbt": "scala.png",
            ".cmake": "cmake.svg",
        }

for folder in ["openoffice", "ssh", "npm", "wine", "dbus", "thunderbird", "gradle"]:
    ThumbMap["."+folder] = folder + '.png'
for folder in ["Videos", "Desktop", "Documents", "Downloads", "Pictures"]:
    ThumbMap[folder] = folder + ".png"
ThumbMap["Music"] = "Music.svg"
ThumbMap[".rstudio-desktop"] = "R.png"
ThumbMap[".python-eggs"] = "python-eggs.png"
StemMap = {
    "requirements": "requirements.png",
    ".cling_history": "cling.png",
    ".scala_history": "scala.png",
    ".gitignore": "gitignore.png", 
    ".gitconfig": "gitignore.png",
    ".python_history": "py.png",
    ".julia_history": "jl.png",
    "README": "README.png",
    ".gdbinit": "gnu.png",
    ".Rhistory": "R.png",
    ".pypirc": "py.png", 
}
PrefixMap = {
    ".python_history": "py.png",
    ".conda": "anaconda3.png",
    ".bash": "bashrc.png",
    "rstudio-": "R.png",
    ".nvidia": "cu.png",
    "nvidia-": "cu.png",
    "zsh": "bashrc.png",
}
PLATFORM = platform.system()

def sizeof_fmt(num, suffix="B"):
    '''convert bytes to human readable format'''
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    
    return f"{num:.1f}Y{suffix}"


class FileViewerInitWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def run(self, file_viewer, all_files: List[str]):
        '''for the fileviewer ui loading task.'''
        for i, path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=file_viewer)
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


class FileViewerRefreshWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def run(self, file_viewer, path: str, reverse: bool):
        '''for the fileviewer ui refresh task.'''
        file_viewer._refresh(path, reverse)
        self.finished.emit()


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


class FigFileIcon(QToolButton):
    def __init__(self, path, parent=None, size=(120,120), textwidth=10):
        super(FigFileIcon, self).__init__(parent)
        self._parent = parent
        self.name = pathlib.Path(path).name
        self.path = path
        self.isfile = os.path.isfile(path)
        self.stem = pathlib.Path(path).stem
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
        }
        QToolButton:hover {
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 2, stop : 0.0 '''+Fig.FileViewer.CDHEX+''', stop : 0.99 '''+Fig.FileViewer.CLHEX+'''); 
            /* #e38c59; */ /* #009b9e; */
            color: #292929;
            font-weight: bold;
        }        
        ''' 
        self.selectedStyle = f"background: {Fig.FileViewer.SCHEX}; color: #292929; font-weight: bold"
        self.setStyleSheet(self.defaultStyle)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        text = "\n".join(textwrap.wrap(self.name[:textwidth*3], width=textwidth))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setText(text) # truncate at 3 times the max textwidth
        self.setFixedSize(QSize(*size))
        self.setIconSize(QSize(size[0]-60, size[1]-60))
        self._getFileProperties()
        self._setThumbnail()
        self._setPropertiesTip()

    def unselect(self):
        self.setStyleSheet(self.defaultStyle)

    def select(self):
        self.setStyleSheet(self.selectedStyle)

    def _getMimeType(self):
        mimeType,_ = mimetypes.guess_type(self.path) 
        if not self.isfile:
            return "Folder"
        elif mimeType:
            return mimeType
        else:
            if PLATFORM == "Linux":
                cmd = f"file --mime-type {self.path}"
                op = subprocess.getoutput(cmd)
                return op.split()[-1]
            else:
                return "Unknown"

    def _getFileProperties(self):
        try:
            stat = os.stat(self.path)
        except (PermissionError, FileNotFoundError) as e: 
            self.props = argparse.Namespace()
            self.props.access_time = datetime.datetime.now().strftime("%b,%b %d %Y %H:%M:%S")
            self.props.modified_time = datetime.datetime.now().strftime("%b,%b %d %Y %H:%M:%S")
            self.props.size = "0B"
            return 
        self.props = argparse.Namespace()
        if PLATFORM == "Linux":
            self.props.access_time = datetime.datetime.fromtimestamp(stat.st_atime).strftime("%b,%b %d %Y %H:%M:%S")
            self.props.modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%b,%b %d %Y %H:%M:%S")
            self.props.size = sizeof_fmt(stat.st_size)
        elif PLATFORM == "Windows":
            pass
        elif PLATFORM == "Darwin":
            pass
        else:
            pass

    def _setPropertiesTip(self):
        properties = f'''
Name: {self.name}
Type: {self._getMimeType()}
Size: {self.props.size}

Location: {self.path}

Accessed: {self.props.access_time} 
Modified: {self.props.modified_time}
'''
        self.setToolTip(properties)

    def _setThumbnail(self):
        _,ext = os.path.splitext(self.name)
        # print(self.name, self.stem, ext, os.path.isfile(self.path))
        ext = ext[1:]
        if self.name == ".git":
            self.setIcon(FigIcon("launcher/git.png"))
            return
        elif self.name == "pom.xml":
            self.setIcon(FigIcon("launcher/pom.png"))
            return
        elif self.name.lower() == "todo":
            self.setIcon(FigIcon("launcher/todo.png"))
            return
        elif not self.isfile:            
            # phrase contained case.
            for phrase in ThumbPhrases:
                if phrase in self.name.lower():
                    self.setIcon(FigIcon(f"launcher/{phrase}.png")); return 
            
            if self.name in ThumbMap:
                filename = ThumbMap[self.name]
                self.setIcon(FigIcon(f"launcher/{filename}"))
            # elif self.name == ".sbt":
            #     self.setIcon(FigIcon("launcher/scala.png"))
            elif self.name.startswith(".git"):
                self.setIcon(FigIcon("launcher/git.png"))

            elif "julia" in self.name.lower():
                self.setIcon(FigIcon("launcher/jl.png"))
            elif "netbeans" in self.name.lower():
                self.setIcon(FigIcon("launcher/netbeans.svg"))
            elif "vscode" in self.name.lower():
                self.setIcon(FigIcon("launcher/notvscode.png"))

            elif self.stem == ".gconf":
                self.setIcon(FigIcon("launcher/gnome.png"))
            elif self.stem == ".fontconfig":
                self.setIcon(FigIcon("launcher/ttf.svg"))
            elif "anaconda" in self.name.lower() or self.name.startswith(".conda"):
                self.setIcon(FigIcon("launcher/anaconda3.png"))

            elif "jupyter" in self.name.lower() or "ipython" in self.name.lower() or "ipynb" in self.name.lower():
                self.setIcon(FigIcon("launcher/ipynb.png"))

            elif "tor" in re.split("_| |-", self.name.lower()) or self.name == ".tor":
                self.setIcon(FigIcon("launcher/tor.png"))
            elif self.name == ".linuxbrew" or self.name == "Homebrew":
                self.setIcon(FigIcon("launcher/brew.png"))
            # elif self.name == "cuda":
            #     self.setIcon(FigIcon("launcher/cu.png"))
            elif self.name in [".gnupg"]:
                self.setIcon(FigIcon("launcher/gnu.png"))
            elif self.path in STDLinuxFolders:
                self.setIcon(FigIcon(f"dir/{self.name}.png"))
            else:    
                self.setIcon(FigIcon("launcher/fileviewer.png"))
            return
        elif ext in ["png","jpg","svg"]:
            self.setIcon(QIcon(self.path))
            return
        # elif ext in ["webm", "mp4", "flv", "ogv", "wmv", "mov"]:
        #     import moviepy.editor
        #     with tempfile.NamedTemporaryFile() as temp:
        #         os.rename(temp.name, temp.name+'.jpg')
        #         clip = moviepy.editor.VideoFileClip(self.path)
        #         clip.save_frame(temp.name+'.jpg',t=1.0)
        #         self.setIcon(QIcon(temp.name+'.jpg'))
        #         os.rename(temp.name+'.jpg', temp.name)
        #     return
        # elif self.stem in ["README", "requirements"]:
        #     self.setIcon(FigIcon(f"launcher/{self.stem}.png"))
        #     return
        elif self.name == ".profile":
            self.setIcon(FigIcon("launcher/bashrc.png"))
            return  
        elif self.stem.lower() == "license":
            self.setIcon(FigIcon("launcher/license.png"))
            return              
        # REMOVE #
        elif self.stem.startswith(".bash"):
            self.setIcon(FigIcon("launcher/bashrc.png"))
            return  
        elif self.stem.startswith("zsh"):
            self.setIcon(FigIcon("launcher/bashrc.png"))
            return  
        elif self.stem.startswith(".conda"):
            self.setIcon(FigIcon("launcher/anaconda3.png"))
            return
        elif self.stem.startswith("nvidia-"):
            self.setIcon(FigIcon("launcher/cu.png"))
            return
        elif self.name.startswith(".nvidia"):
            self.setIcon(FigIcon("launcher/cu.png"))
            return
        # REMOVE #
        elif self.name.startswith(".") and "cookie" in self.name:
            self.setIcon(FigIcon("launcher/cookie.png"))
            return

        elif self.stem in StemMap:
            filename = StemMap[self.stem]
            self.setIcon(FigIcon(f"launcher/{filename}"))
            return    

        elif self.stem.endswith("_history"):
            self.setIcon(FigIcon("launcher/history.png"))
            return
   
        # txt/bin classification.
        elif ext == "":
            if subprocess.getoutput(f"file --mime-encoding {self.path}").endswith("binary"):
                self.setIcon(FigIcon("launcher/bin.png"))    
            else:
                self.setIcon(FigIcon("launcher/txt.png"))
            return

        for prefix in PrefixMap:
            if self.stem.startswith(prefix):
                filename = PrefixMap[prefix]
                self.setIcon(FigIcon(f"launcher/{filename}")) 
                return
        # check for .ext kind of files.
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

class FigFileViewer(GraphicsView):
    def __init__(self, path=str(pathlib.Path.home()), parent=None, width=4, button_size=(100,100), icon_size=(60,60)):
        super(FigFileViewer, self).__init__(parent)   
        all_files = self.listFiles(path) # get list of all files and folders.
        self.ribbon_visible = True
        self.path = path
        self._parent = parent
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet('''
            QScrollArea {
                background-color: rgba(73, 44, 94, 0.5);
            }
            QScrollBar:vertical {
                border: 0px solid #999999;
                width: 8px;    
                margin: 0px 0px 0px 0px;
                background-color: rgba(227, 140, 89, 0.5);
            }
            QScrollBar::handle:vertical {         
                min-height: 0px;
                border: 0px solid red;
                border-radius: 4px;
                background-color: #e38c59; /* #c70039; */
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
            }
            /* QScrollBar:vertical {
                border: 0px solid #999999;
                width:14px;    
                margin: 0px 0px 0px 3px;
                background-color: rgba(73, 44, 94, 0.5);
            }
            QScrollBar::handle:vertical {         
                min-height: 0px;
                border: 0px solid red;
                border-radius: 5px;
                background-color: rgb(92, 95, 141);
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
            } */
            QToolTip { border: 0px }
        ''')
        ### replace with FlowLayout ###
        self.gridLayout = FlowLayout() # QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(5)
        ###############################
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.viewer = QWidget()
        self.viewer.setStyleSheet('''
        background: ''' + Fig.FileViewer.FVBG + '''
        ''')
        self.history = [path]
        self.i = 0
        self.j = 0
        import time
        start = time.time()

        self.bgStyle = "url('/home/atharva/GUI/FigUI/FigUI/assets/icons/email/bg_texture2.png');"

        self.init_thread = QThread()
        self.init_worker = FileViewerInitWorker()
        self.init_worker.moveToThread(self.init_thread)
        self.init_thread.started.connect(lambda: self.init_worker.run(self, all_files))
        self.init_worker.finished.connect(self.init_thread.quit)
        self.init_worker.finished.connect(self.init_worker.deleteLater)
        self.init_thread.finished.connect(self.init_thread.deleteLater)
        # TODO: check dis.
        # self.init_worker.progress.connect(self.reportProgress)
        self.init_thread.start()
        # for i, path in enumerate(all_files):
        #     fileIcon = FigFileIcon(path, parent=self)
        #     fileIcon.clicked.connect(self.open)
        #     ### replace with FlowLayout ###
        #     self.gridLayout.addWidget(fileIcon)
        #     # self.gridLayout.addWidget(fileIcon, i // width, i % width) 
        #     ###############################       
        # self.viewer.setLayout(self.gridLayout)
        
        print("created grid layout:", time.time()-start)
        # self.layout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        self.scrollArea.setWidget(self.viewer)

        start = time.time()
        self.navbar = self.initNavBar()
        self.propbar = self.initPropBar()
        # self.editbar = self.initEditBar()
        self.viewbar = self.initViewBar()
        self.mainMenu = self.initMainMenu()
        # self.utilbar = self.initUtilBar()

        self.layout.addWidget(self.navbar)
        # self.layout.addWidget(self.editbar)
        self.layout.addWidget(self.propbar)
        
        self.layout.addWidget(self.mainMenu)
        # print("created toolbars:", time.time()-start)
        # self.layout.addWidget(self.viewbar)
        # self.layout.addWidget(self.utilbar)

        start = time.time()
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)
        self.width = width
        # selBtn = self.gridLayout.itemAt(0).widget()
        # selBtn.setStyleSheet("background: color(0, 0, 255, 50)")
        # self.highlight(0)
        # link folder nav bar buttons.
        self.hideRibbon()
        if self._parent:
            self._parent.backNavBtn.clicked.connect(self.prevPath)
            self._parent.nextNavBtn.clicked.connect(self.nextPath)
        # print("created toolbars:", time.time()-start)
        # self.setLayout(self.gridLayout)
    def hideRibbon(self):
        if self.ribbon_visible:
            self.mainMenu.setFixedHeight(25)
            self.hideBtn.setIcon(FigIcon("fileviewer/show_ribbon.svg"))
        else:
            self.mainMenu.setMaximumHeight(120)
            self.hideBtn.setIcon(FigIcon("fileviewer/hide_ribbon.svg"))
        self.ribbon_visible = not(
            self.ribbon_visible
        )

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
        # hide the ribbon.
        self.hideBtn = QToolButton(mainMenu)
        self.hideBtn.clicked.connect(self.hideRibbon)
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

        # sort ascending.
        sortUpBtn = QToolButton()
        sortUpBtn.setIcon(FigIcon("fileviewer/sort_ascending.svg"))
        sortUpBtn.setIconSize(QSize(25,25))
        sortUpBtn.clicked.connect(lambda: self.refresh(self.path, reverse=False))
        sortUpBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sortUpBtn.setText("A to Z")
        sortLayout.addWidget(sortUpBtn)
        # sort descending.
        sortDownBtn = QToolButton()
        sortDownBtn.setIcon(FigIcon("fileviewer/sort_descending.svg"))
        sortDownBtn.setIconSize(QSize(25,25))
        sortDownBtn.clicked.connect(lambda: self.refresh(self.path, reverse=True))
        sortDownBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        sortLayout.addWidget(sortDownBtn)
        sortDownBtn.setText("Z to A")
        layoutToolBarLayout.addWidget(sortRibbon)

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

    def initViewBar(self):
        '''
        Initialize view bar.
        View bar contains:
        1. Sort ascending
        2. Sort descending
        3. Recently accessed
        4. Show hidden files (linux: . prefix)
        5. Hide hidden files
        6. Toggle list view
        7. Toggle block view
        '''
        viewbar = QWidget()
        viewLayout = QHBoxLayout()
        # left spacer.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        viewLayout.addWidget(left_spacer)
        # sort ascending.
        sortUpBtn = QToolButton()
        sortUpBtn.setIcon(FigIcon("fileviewer/sort_ascending.svg"))
        sortUpBtn.clicked.connect(lambda: self.refresh(self.path, reverse=False))
        viewLayout.addWidget(sortUpBtn)
        # sort descending.
        sortDownBtn = QToolButton()
        sortDownBtn.setIcon(FigIcon("fileviewer/sort_descending.svg"))
        sortDownBtn.clicked.connect(lambda: self.refresh(self.path, reverse=True))
        viewLayout.addWidget(sortDownBtn)
        # viewLayout.addWidget(QVLine())
        # recently accessed files.
        recentBtn = QToolButton()
        recentBtn.setIcon(FigIcon("fileviewer/recent.svg"))
        # sortUpBtn.clicked.connect(self.nextPath)
        viewLayout.addWidget(recentBtn)
        # view hidden files.
        unhideBtn = QToolButton()
        unhideBtn.setIcon(FigIcon("fileviewer/unhide.svg"))
        unhideBtn.clicked.connect(lambda: self.unhide(self.path))
        viewLayout.addWidget(unhideBtn)

        hideBtn = QToolButton()
        hideBtn.setIcon(FigIcon("fileviewer/hide.svg"))
        hideBtn.clicked.connect(lambda: self.refresh(self.path))
        viewLayout.addWidget(hideBtn)
        # viewLayout.addWidget(QVLine())
        listViewBtn = QToolButton() # toggle list view.
        listViewBtn.setIcon(FigIcon("fileviewer/listview.svg"))
        viewLayout.addWidget(listViewBtn)

        blockViewBtn = QToolButton() # toggle block view.
        blockViewBtn.setIcon(FigIcon("fileviewer/blockview.svg"))
        viewLayout.addWidget(blockViewBtn)        
        # right spacer.
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        viewLayout.addWidget(right_spacer)

        viewLayout.setContentsMargins(5, 0, 5, 0)
        viewbar.setLayout(viewLayout)

        return viewbar

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
        try:
            selBtn = self.gridLayout.itemAt(self.j).widget()
            selBtn.unselect()
            selBtn.setAttribute(Qt.WA_TranslucentBackground)
            self.j = j
            selBtn = self.gridLayout.itemAt(self.j).widget()
            # selBtn.setStyleSheet("background: #ff5e00; color: #292929; font-weight: bold")
            selBtn.select()
        except AttributeError:
            self.back()
    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.KeyPress:
    #         print(event.key())
    #     return super(FigFileViewer, self).eventFilter(source, event)
    def prevPath(self):
        self.i -= 1
        self.i = max(0, self.i)
        path = self.history[self.i]
        self.refresh(path)

    def nextPath(self):
        self.i += 1
        self.i = min(len(self.history)-1, self.i)
        path = self.history[self.i]
        self.refresh(path)

    def back(self):
        path = self.path
        path = pathlib.Path(path).parent
        self.path = path
        self.history.append(path)
        self.i += 1
        self.refresh(path)

    def openPath(self, path):
        self.path = path
        # print(f"opened {path}") # DEBUG
        if not os.path.isfile(path):
            self.history.append(path)
            self.i += 1
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
            print("reverse:", reverse)
            for file in os.listdir(path):
                if not(file.startswith(".") and hide):
                    files.append(os.path.join(path, file))
            return sorted(files, key= lambda x: x.lower(), reverse=reverse)
        except PermissionError:
            return files

    def refresh(self, path, reverse=False):
        '''launch worker to refresh file layout..'''
        import time
        start = time.time()
        if self._parent:
            print("refreshing view ...")
            self._parent.setWindowTitle("Loading")
        self.refresh_thread = QThread()
        self.refresh_worker = FileViewerRefreshWorker()
        self.refresh_worker.moveToThread(self.refresh_thread)
        self.refresh_thread.started.connect(lambda: self.refresh_worker.run(self, path, reverse))
        self.refresh_worker.finished.connect(self.refresh_thread.quit)
        self.refresh_worker.finished.connect(self.refresh_worker.deleteLater)
        self.refresh_thread.finished.connect(self.refresh_thread.deleteLater)
        # TODO: check dis.
        # self.init_worker.progress.connect(self.reportProgress)
        self.refresh_thread.start()
        print("refreshed in:", time.time()-start)

    def _refresh(self, path, reverse=False):
        '''function to be executed inside the worker.'''
        self.clear()
        if self._parent:
            i = self._parent.tabs.currentIndex()
            name = pathlib.Path(path).name
            parent = pathlib.Path(path).parent.name
            self._parent.tabs.setTabText(i, f"{name} .../{parent}")
            self._parent.updateFolderBar(path, viewer=self)
            self._parent.log("launcher/fileviewer.png", str(path))
        all_files = self.listFiles(path, reverse=reverse) # get list of all files and folders.
        
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            ### replace with FlowLayout ###
            self.gridLayout.addWidget(fileIcon)  
            # self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
            ###############################
        self.highlight(0)        

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
        if not sendingBtn.isfile:
            path = sendingBtn.path
            self.path = path
            self.history.append(path)
            self.i += 1
            self.refresh(path)
        else:
            if self._parent: # call file handler for the extension here
                path = sendingBtn.path
                handlerWidget = self._parent.handler.getUI(path)
                name = pathlib.Path(path).name
                parent = ".../" + pathlib.Path(path).parent.name
                thumbnail = getThumbnail(path)
                i = self._parent.tabs.addTab(handlerWidget, FigIcon(thumbnail), f"\t{name} {parent}")
                self._parent.tabs.setCurrentIndex(i)


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