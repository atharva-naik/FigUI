#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5, re
import tempfile, random
import textwrap, subprocess
import os, sys, glob, pathlib
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit, QFrame
try:
    from utils import *
except ImportError:
    from FigUI.utils import *


class QVLine(QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("color: #6E6E6E")


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

    def _setThumbnailMime(self):
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
            for phrase in ["nano", "eclipse", "cache", "java", "cargo", "compiz", "aiml", "kivy", "netbeans", "mozilla"]:
                if phrase in self.name.lower():
                    self.setIcon(FigIcon(f"launcher/{phrase}.png"))
                    return

            if self.name == "Music":
                self.setIcon(FigIcon("launcher/Music.svg"))
            elif self.name in ["Videos", "Desktop", "Documents", "Downloads", "Pictures"]:
                self.setIcon(FigIcon(f"launcher/{self.name}.png"))
            elif self.name.startswith(".git"):
                self.setIcon(FigIcon("launcher/git.png"))
            elif self.name in [".rstudio-desktop"]:
                self.setIcon(FigIcon("launcher/R.png"))
            elif self.name in [".python-eggs"]:
                self.setIcon(FigIcon("launcher/python-eggs.png"))
            elif "android" in self.name.lower():
                self.setIcon(FigIcon("launcher/android.png"))
            elif "gnome" in self.name.lower():
                self.setIcon(FigIcon("launcher/gnome.png"))
            elif "anaconda" in self.name.lower() or self.name.startswith(".conda"):
                self.setIcon(FigIcon("launcher/anaconda3.png"))
            elif "jupyter" in self.name.lower() or "ipython" in self.name.lower() or "ipynb" in self.name.lower():
                self.setIcon(FigIcon("launcher/ipynb.png"))
            # elif "nano" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/nano.png"))
            # elif "eclipse" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/eclipse.png"))
            # elif "cache" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/cache.png"))
            # elif "java" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/java.png"))
            # elif "cargo" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/cargo.png"))
            # elif "compiz" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/compiz.png"))
            # elif "aiml" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/aiml.png"))
            # elif "kivy" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/kivy.png"))
            # elif "netbeans" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/netbeans.svg"))
            # elif "mozilla" in self.name.lower():
            #     self.setIcon(FigIcon("launcher/mozilla.png"))
            elif "julia" in self.name.lower():
                self.setIcon(FigIcon("launcher/jl.png"))
            elif "vscode" in self.name.lower():
                self.setIcon(FigIcon("launcher/notvscode.png"))
            
            elif "tor" in re.split("_| |-", self.name.lower()) or self.name == ".tor":
                self.setIcon(FigIcon("launcher/tor.png"))
            elif self.name in [".thunderbird", ".wine", ".dbus", ".ssh", ".npm", ".gradle", ".openoffice"]:
                self.setIcon(FigIcon(f"launcher/{self.name[1:]}.png"))
            # elif self.name == ".wine":
            #     self.setIcon(FigIcon("launcher/wine.png"))
            # elif self.name == ".dbus":
            #     self.setIcon(FigIcon("launcher/dbus.png"))
            # elif self.name == ".ssh":
            #     self.setIcon(FigIcon("launcher/ssh.png"))
            # elif self.name == ".npm":
            #     self.setIcon(FigIcon("launcher/npm.png"))
            # elif self.name == ".gradle":
            #     self.setIcon(FigIcon("launcher/gradle.png"))
            elif self.name == ".linuxbrew" or self.name == "Homebrew":
                self.setIcon(FigIcon("launcher/brew.png"))
            # elif self.name == ".openoffice":
            #     self.setIcon(FigIcon("launcher/openoffice.png"))
            elif self.name == ".cmake":
                self.setIcon(FigIcon("launcher/cmake.svg"))
            else:    
                self.setIcon(FigIcon("launcher/fileviewer.png"))
            return        

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
            if self.name == "Music":
                self.setIcon(FigIcon("launcher/Music.svg"))
            elif self.name in ["Videos", "Desktop", "Documents", "Downloads", "Pictures"]:
                self.setIcon(FigIcon(f"launcher/{self.name}.png"))
            elif self.name.startswith(".git"):
                self.setIcon(FigIcon("launcher/git.png"))
            elif self.name in [".rstudio-desktop"]:
                self.setIcon(FigIcon("launcher/R.png"))
            elif self.name in [".python-eggs"]:
                self.setIcon(FigIcon("launcher/python-eggs.png"))
            elif "android" in self.name.lower():
                self.setIcon(FigIcon("launcher/android.png"))
            elif "gnome" in self.name.lower():
                self.setIcon(FigIcon("launcher/gnome.png"))
            elif "anaconda" in self.name.lower() or self.name.startswith(".conda"):
                self.setIcon(FigIcon("launcher/anaconda3.png"))
            elif "nano" in self.name.lower():
                self.setIcon(FigIcon("launcher/nano.png"))
            elif "eclipse" in self.name.lower():
                self.setIcon(FigIcon("launcher/eclipse.png"))
            elif "jupyter" in self.name.lower() or "ipython" in self.name.lower() or "ipynb" in self.name.lower():
                self.setIcon(FigIcon("launcher/ipynb.png"))
            elif "cache" in self.name.lower():
                self.setIcon(FigIcon("launcher/cache.png"))
            elif "java" in self.name.lower():
                self.setIcon(FigIcon("launcher/java.png"))
            elif "julia" in self.name.lower():
                self.setIcon(FigIcon("launcher/jl.png"))
            elif "cargo" in self.name.lower():
                self.setIcon(FigIcon("launcher/cargo.png"))
            elif "compiz" in self.name.lower():
                self.setIcon(FigIcon("launcher/compiz.png"))
            elif "aiml" in self.name.lower():
                self.setIcon(FigIcon("launcher/aiml.png"))
            elif "kivy" in self.name.lower():
                self.setIcon(FigIcon("launcher/kivy.png"))
            elif "netbeans" in self.name.lower():
                self.setIcon(FigIcon("launcher/netbeans.svg"))
            elif "mozilla" in self.name.lower():
                self.setIcon(FigIcon("launcher/mozilla.png"))
            elif "vscode" in self.name.lower():
                self.setIcon(FigIcon("launcher/notvscode.png"))
            elif "tor" in re.split("_| |-", self.name.lower()) or self.name == ".tor":
                self.setIcon(FigIcon("launcher/tor.png"))
            elif self.name == ".thunderbird":
                self.setIcon(FigIcon("launcher/thunderbird.png"))
            elif self.name == ".wine":
                self.setIcon(FigIcon("launcher/wine.png"))
            elif self.name == ".dbus":
                self.setIcon(FigIcon("launcher/dbus.png"))
            elif self.name == ".ssh":
                self.setIcon(FigIcon("launcher/ssh.png"))
            elif self.name == ".npm":
                self.setIcon(FigIcon("launcher/npm.png"))
            elif self.name == ".gradle":
                self.setIcon(FigIcon("launcher/gradle.png"))
            elif self.name == ".linuxbrew" or self.name == "Homebrew":
                self.setIcon(FigIcon("launcher/brew.png"))
            elif self.name == ".openoffice":
                self.setIcon(FigIcon("launcher/openoffice.png"))
            elif self.name == ".cmake":
                self.setIcon(FigIcon("launcher/cmake.svg"))
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
        elif self.stem == "README":
            self.setIcon(FigIcon("launcher/README.png"))
            return
        elif self.stem == "requirements":
            self.setIcon(FigIcon("launcher/requirements.png"))
            return
        elif self.stem.lower() == "license":
            self.setIcon(FigIcon("launcher/license.png"))
            return      
        elif self.stem.startswith(".bash") or self.stem.startswith("zsh"):
            self.setIcon(FigIcon("launcher/bashrc.png"))
            return  
        elif self.stem.startswith(".conda"):
            self.setIcon(FigIcon("launcher/anaconda3.png"))
            return
        elif self.stem.startswith("rstudio-"):
            self.setIcon(FigIcon("launcher/R.png"))
            return
        elif self.stem.startswith("nvidia-"):
            self.setIcon(FigIcon("launcher/cu.png"))
            return
        elif self.stem in [".julia_history"]:
            self.setIcon(FigIcon("launcher/jl.png"))
            return   
        elif self.stem in [".Rhistory"]:
            self.setIcon(FigIcon("launcher/R.png"))
            return 
        elif self.stem in [".pypirc", ".python_history"]:
            self.setIcon(FigIcon("launcher/py.png"))
            return 
        elif self.stem.startswith(".python_history"):
            self.setIcon(FigIcon("launcher/py.png"))
            return 
        elif self.name.startswith(".") and "cookie" in self.name:
            self.setIcon(FigIcon("launcher/cookie.png"))
            return
        elif self.name.startswith(".nvidia"):
            self.setIcon(FigIcon("launcher/cu.png"))
            return
        elif self.stem in [".scala_history"]:
            self.setIcon(FigIcon("launcher/scala.png"))
            return
        elif self.stem in [".gitignore", ".gitconfig"]:
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
        self._parent = parent
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
        self.navbar = QWidget()
        self.utilbar = QWidget()
        navLayout = QHBoxLayout() 
        utilLayout = QHBoxLayout() # bookmarks, restricted view, change permissions, encrypt, zip/unzip, new folder, new file, undo/redo, cut/copy/paste, rename, open in terminal, properties.
        # bookmark files.
        bookmarkBtn = QToolButton()
        bookmarkBtn.setIcon(FigIcon("bookmark.svg"))
        utilLayout.addWidget(bookmarkBtn)
        # restrict files from other users.
        # restrictBtn = QToolButton()
        # restrictBtn.setIcon(FigIcon("bookmark.svg"))
        # utilLayout.addWidget(restrictBtn)
        # change permissions (user access group.)
        userpermBtn = QToolButton()
        userpermBtn.setIcon(FigIcon("user_permissions.svg")) 
        utilLayout.addWidget(userpermBtn) 
        # change r/w/x permissions.
        rwxpermBtn = QToolButton()
        rwxpermBtn.setIcon(FigIcon("permissions.svg"))
        utilLayout.addWidget(rwxpermBtn)
        utilLayout.addWidget(QVLine())
        # encrypt
        encryptBtn = QToolButton()
        encryptBtn.setIcon(FigIcon("encrypt.svg"))
        utilLayout.addWidget(encryptBtn)
        # decrypt 
        decryptBtn = QToolButton()
        decryptBtn.setIcon(FigIcon("decrypt.svg"))
        utilLayout.addWidget(decryptBtn)
        utilLayout.addWidget(QVLine())
        # zip
        zipBtn = QToolButton()
        zipBtn.setIcon(FigIcon("zip.svg"))
        utilLayout.addWidget(zipBtn)
        # unzip
        unzipBtn = QToolButton()
        unzipBtn.setIcon(FigIcon("zip.svg"))
        utilLayout.addWidget(unzipBtn)
        utilLayout.addWidget(QVLine())
        # new file
        newFileBtn = QToolButton()
        newFileBtn.setIcon(FigIcon("new_file.svg"))
        utilLayout.addWidget(newFileBtn)
        # file share
        fileShareBtn = QToolButton()
        fileShareBtn.setIcon(FigIcon("file_share.svg"))
        utilLayout.addWidget(fileShareBtn)
        # new folder
        newFolderBtn = QToolButton()
        newFolderBtn.setIcon(FigIcon("new_folder.svg"))
        utilLayout.addWidget(newFolderBtn)
        # email file/folder.
        emailBtn = QToolButton()
        emailBtn.setIcon(FigIcon("email.svg"))
        utilLayout.addWidget(emailBtn)
        # rename
        renameBtn = QToolButton()
        renameBtn.setIcon(FigIcon("rename.svg"))
        utilLayout.addWidget(renameBtn)
        # delete
        delBtn = QToolButton()
        delBtn.setIcon(FigIcon("delete.svg"))
        utilLayout.addWidget(delBtn)
        # properties of selected file/folder.
        utilLayout.addWidget(QVLine())
        propBtn = QToolButton()
        propBtn.setIcon(FigIcon("properties.svg"))
        utilLayout.addWidget(propBtn)
        # open in terminal
        openInTermBtn = QToolButton()
        openInTermBtn.setIcon(FigIcon("open_in_terminal.svg"))
        utilLayout.addWidget(openInTermBtn)
        # open with.
        openBtn = QToolButton()
        openBtn.setIcon(FigIcon("open.svg"))
        utilLayout.addWidget(openBtn)
        utilLayout.addWidget(QVLine())
        # cut/copy/paste
        cutBtn = QToolButton()
        cutBtn.setIcon(FigIcon("cut.svg"))
        utilLayout.addWidget(cutBtn)
        copyBtn = QToolButton()
        copyBtn.setIcon(FigIcon("copy.svg"))
        utilLayout.addWidget(copyBtn)
        pasteBtn = QToolButton()
        pasteBtn.setIcon(FigIcon("paste.svg"))
        utilLayout.addWidget(pasteBtn)
        utilLayout.addWidget(QVLine())
        # undo/redo
        undoBtn = QToolButton()
        undoBtn.setIcon(FigIcon("undo.svg"))
        utilLayout.addWidget(undoBtn)
        redoBtn = QToolButton()
        redoBtn.setIcon(FigIcon("redo.svg"))
        utilLayout.addWidget(redoBtn)
        utilLayout.addWidget(QVLine())

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
        utilLayout.addWidget(sortUpBtn)

        sortDownBtn = QToolButton()
        sortDownBtn.setIcon(FigIcon("sort_descending.svg"))
        # sortUpBtn.clicked.connect(self.nextPath)
        utilLayout.addWidget(sortDownBtn)
        utilLayout.addWidget(QVLine())

        unhideBtn = QToolButton()
        unhideBtn.setIcon(FigIcon("unhide.svg"))
        unhideBtn.clicked.connect(lambda: self.unhide(self.path))
        utilLayout.addWidget(unhideBtn)

        hideBtn = QToolButton()
        hideBtn.setIcon(FigIcon("hide.svg"))
        hideBtn.clicked.connect(lambda: self.refresh(self.path))
        utilLayout.addWidget(hideBtn)
        utilLayout.addWidget(QVLine())

        searchBar = QLineEdit()
        searchBar.setStyleSheet("background: #fff; color: #000")
        navLayout.addWidget(searchBar)

        # match case.
        caseBtn = QToolButton()
        caseBtn.setIcon(FigIcon("case-sensitive.svg"))
        # caseBtn.clicked.connect(self.back)
        navLayout.addWidget(caseBtn)
        # match whole word.
        entireBtn = QToolButton()
        entireBtn.setIcon(FigIcon("whole-word.svg"))
        # backBtn.clicked.connect(self.back)
        navLayout.addWidget(entireBtn)
        # use regex search
        regexBtn = QToolButton()
        regexBtn.setIcon(FigIcon("regex_search.svg"))
        # regexBtn.clicked.connect(self.back)
        navLayout.addWidget(regexBtn)
        
        searchBtn = QToolButton()
        searchBtn.setIcon(FigIcon("search.svg"))
        navLayout.addWidget(searchBtn)

        listViewBtn = QToolButton() # toggle list view.
        listViewBtn.setIcon(FigIcon("listview.svg"))
        utilLayout.addWidget(listViewBtn)

        blockViewBtn = QToolButton() # toggle block view.
        blockViewBtn.setIcon(FigIcon("blockview.svg"))
        utilLayout.addWidget(blockViewBtn)

        navLayout.setContentsMargins(0, 0, 0, 0)
        utilLayout.setContentsMargins(0, 0, 0, 0)
        self.navbar.setLayout(navLayout)  
        self.utilbar.setLayout(utilLayout)
        self.layout.addWidget(self.navbar)
        self.layout.addWidget(self.utilbar)
        self.layout.addWidget(self.scroll)
        self.setLayout(self.layout)
        self.width = width
        selBtn = self.gridLayout.itemAt(0).widget()
        selBtn.setStyleSheet("background: color(0, 0, 255, 50)")
        self.highlight(0)

        if self._parent:
            self._parent.backNavBtn.clicked.connect(self.prevPath)
            self._parent.nextNavBtn.clicked.connect(self.nextPath)

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
            selBtn.setStyleSheet("background-color: #292929; border: 0px")
            self.j = j
            selBtn = self.gridLayout.itemAt(self.j).widget()
            selBtn.setStyleSheet("background: #42f2f5; color: #292929; font-weight: bold")
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

    def refresh(self, path):
        self.clear()
        if self._parent:
            i = self._parent.tabs.currentIndex()
            name = pathlib.Path(path).name
            parent = pathlib.Path(path).parent.name
            self._parent.tabs.setTabText(i, f"{name} .../{parent}")
            self._parent.updateFolderBar(path, viewer=self)
        all_files = self.listFiles(path) # get list of all files and folders.
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
        self.highlight(0)        

    def unhide(self, path):        
        self.clear()
        all_files = self.listFiles(path, hide=False) # get list of all files and folders.
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            self.gridLayout.addWidget(fileIcon, i // self.width, i % self.width)  
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


if __name__ == "__main__":
    FigFileViewer("/home/atharva/GUI/FigUI")