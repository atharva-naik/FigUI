#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PyQt5
import tempfile, random
# from PIL import Image, ImageQt
import os, re, sys, glob, pathlib, datetime
import argparse, mimetypes, platform, textwrap, subprocess
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWidgets import QAction, QDialog, QWidget, QToolBar, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox

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


class FigFileIcon(QToolButton):
    def __init__(self, path, parent=None, size=(120,120), textwidth=10):
        super(FigFileIcon, self).__init__(parent)
        self._parent = parent
        self.name = pathlib.Path(path).name
        self.path = path
        self.isfile = os.path.isfile(path)
        self.stem = pathlib.Path(path).stem
        self.setStyleSheet('''
            QToolTip {
                border: 0px;
                color: #fff;
            }
            QToolButton { 
                border: 0px; 
                background-image: none;
                color: #fff;
            }
            QToolButton:hover {
                background: #009b9e;
                color: #292929;
                font-weight: bold;
        }''')
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
        stat = os.stat(self.path)
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

class FigFileViewer(QWidget):
    def __init__(self, path=str(pathlib.Path.home()), parent=None, width=4, button_size=(100,100), icon_size=(60,60)):
        super(FigFileViewer, self).__init__(parent)   
        all_files = self.listFiles(path) # get list of all files and folders.
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
            }
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
        self.history = [path]
        self.i = 0
        self.j = 0
        for i,path in enumerate(all_files):
            fileIcon = FigFileIcon(path, parent=self)
            fileIcon.clicked.connect(self.open)
            ### replace with FlowLayout ###
            self.gridLayout.addWidget(fileIcon)
            # self.gridLayout.addWidget(fileIcon, i // width, i % width) 
            ###############################       
        self.viewer.setLayout(self.gridLayout)
        # self.layout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        self.scrollArea.setWidget(self.viewer)

        self.navbar = self.initNavBar()
        self.propbar = self.initPropBar()
        self.editbar = self.initEditBar()
        self.viewbar = self.initViewBar()
        # self.utilbar = self.initUtilBar()
        self.layout.addWidget(self.navbar)
        self.layout.addWidget(self.editbar)
        self.layout.addWidget(self.propbar)
        # self.layout.addWidget(self.viewbar)
        # self.layout.addWidget(self.utilbar)
        self.layout.addWidget(self.scrollArea)
        self.setLayout(self.layout)
        self.width = width
        selBtn = self.gridLayout.itemAt(0).widget()
        selBtn.setStyleSheet("background: color(0, 0, 255, 50)")
        self.highlight(0)

        if self._parent:
            self._parent.backNavBtn.clicked.connect(self.prevPath)
            self._parent.nextNavBtn.clicked.connect(self.nextPath)

    def initNavBar(self):
        navbar = QWidget()
        navLayout = QHBoxLayout() 
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
        searchBar = QLineEdit()
        searchBar.setStyleSheet("background: #fff; color: #000")
        navLayout.addWidget(searchBar)
        
        searchBtn = QToolButton()
        searchBtn.setIcon(FigIcon("fileviewer/search.svg"))
        searchBtn.setStyleSheet("border: 0px")
        navLayout.addWidget(searchBtn)

        navLayout.setContentsMargins(5, 0, 5, 0)
        navbar.setLayout(navLayout) 

        return navbar

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
        # open in terminal
        openInTermBtn = QToolButton()
        openInTermBtn.setIcon(FigIcon("fileviewer/open_in_terminal.svg"))
        openInTermBtn.clicked.connect(self.openInTermTab)
        propLayout.addWidget(openInTermBtn)
        # open with.
        openBtn = QToolButton()
        openBtn.setIcon(FigIcon("fileviewer/open.svg"))
        propLayout.addWidget(openBtn)
        propLayout.addWidget(QVLine())
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
        # notes
        noteBtn = QToolButton()
        noteBtn.setIcon(FigIcon("fileviewer/add_note.svg"))
        propLayout.addWidget(noteBtn)
        # view and edit tags
        vETagsBtn = QToolButton()
        vETagsBtn.setIcon(FigIcon("fileviewer/tags.svg"))
        propLayout.addWidget(vETagsBtn)
        # add tags
        addTagBtn = QToolButton()
        addTagBtn.setIcon(FigIcon("fileviewer/add_tags.svg"))
        propLayout.addWidget(addTagBtn)
        # clear all tags
        clearTagsBtn = QToolButton()
        clearTagsBtn.setIcon(FigIcon("fileviewer/remove_tags.svg"))
        propLayout.addWidget(clearTagsBtn)
        propLayout.addWidget(QVLine())
        # file share.
        fileShareBtn = QToolButton()
        fileShareBtn.setIcon(FigIcon("fileviewer/file_share.svg"))
        propLayout.addWidget(fileShareBtn)
        # email file/folder.
        emailBtn = QToolButton()
        emailBtn.setIcon(FigIcon("fileviewer/email.svg"))
        propLayout.addWidget(emailBtn)
        # copy absolute path.
        copyPathBtn = QToolButton()
        copyPathBtn.setIcon(FigIcon("fileviewer/copy_path.svg"))
        copyPathBtn.clicked.connect(self.copyPathToClipboard)
        propLayout.addWidget(copyPathBtn)
        propLayout.addWidget(QVLine())

        #####
        # sort ascending.
        sortUpBtn = QToolButton()
        sortUpBtn.setIcon(FigIcon("fileviewer/sort_ascending.svg"))
        sortUpBtn.clicked.connect(lambda: self.refresh(self.path, reverse=False))
        propLayout.addWidget(sortUpBtn)
        # sort descending.
        sortDownBtn = QToolButton()
        sortDownBtn.setIcon(FigIcon("fileviewer/sort_descending.svg"))
        sortDownBtn.clicked.connect(lambda: self.refresh(self.path, reverse=True))
        propLayout.addWidget(sortDownBtn)
        # viewLayout.addWidget(QVLine())
        # recently accessed files.
        recentBtn = QToolButton()
        recentBtn.setIcon(FigIcon("fileviewer/recent.svg"))
        # sortUpBtn.clicked.connect(self.nextPath)
        propLayout.addWidget(recentBtn)
        # view hidden files.
        unhideBtn = QToolButton()
        unhideBtn.setIcon(FigIcon("fileviewer/unhide.svg"))
        unhideBtn.clicked.connect(lambda: self.unhide(self.path))
        propLayout.addWidget(unhideBtn)

        hideBtn = QToolButton()
        hideBtn.setIcon(FigIcon("fileviewer/hide.svg"))
        hideBtn.clicked.connect(lambda: self.refresh(self.path))
        propLayout.addWidget(hideBtn)
        # viewLayout.addWidget(QVLine())
        listViewBtn = QToolButton() # toggle list view.
        listViewBtn.setIcon(FigIcon("fileviewer/listview.svg"))
        propLayout.addWidget(listViewBtn)

        blockViewBtn = QToolButton() # toggle block view.
        blockViewBtn.setIcon(FigIcon("fileviewer/blockview.svg"))
        propLayout.addWidget(blockViewBtn) 
        #####

        # right spacer.
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        propLayout.addWidget(right_spacer)

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
        # step back one folder.
        backBtn = QToolButton()
        backBtn.setIcon(FigIcon("fileviewer/stepback.svg"))
        backBtn.clicked.connect(self.back)
        editLayout.addWidget(backBtn)
        # prev item
        prevBtn = QToolButton()
        prevBtn.setIcon(FigIcon("fileviewer/back.svg"))
        prevBtn.clicked.connect(self.prevPath)
        editLayout.addWidget(prevBtn)
        # next item
        nextBtn = QToolButton()
        nextBtn.setIcon(FigIcon("fileviewer/forward.svg"))
        nextBtn.clicked.connect(self.nextPath)
        editLayout.addWidget(nextBtn)
        editLayout.addWidget(QVLine())
        # cut/copy/paste
        cutBtn = QToolButton()
        cutBtn.setIcon(FigIcon("fileviewer/cut.svg"))
        editLayout.addWidget(cutBtn)
        copyBtn = QToolButton()
        copyBtn.setIcon(FigIcon("fileviewer/copy.svg"))
        editLayout.addWidget(copyBtn)
        pasteBtn = QToolButton()
        pasteBtn.setIcon(FigIcon("fileviewer/paste.svg"))
        editLayout.addWidget(pasteBtn)
        # editLayout.addWidget(QVLine())
        # undo/redo
        undoBtn = QToolButton()
        undoBtn.setIcon(FigIcon("fileviewer/undo.svg"))
        editLayout.addWidget(undoBtn)
        redoBtn = QToolButton()
        redoBtn.setIcon(FigIcon("fileviewer/redo.svg"))
        editLayout.addWidget(redoBtn)
        editLayout.addWidget(QVLine()) 
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
        # match case.
        caseBtn = QToolButton()
        caseBtn.setIcon(FigIcon("fileviewer/case-sensitive.svg"))
        # caseBtn.clicked.connect(self.back)
        editLayout.addWidget(caseBtn)
        # match whole word.
        entireBtn = QToolButton()
        entireBtn.setIcon(FigIcon("fileviewer/whole-word.svg"))
        # backBtn.clicked.connect(self.back)
        editLayout.addWidget(entireBtn)
        # use regex search
        regexBtn = QToolButton()
        regexBtn.setIcon(FigIcon("fileviewer/regex_search.svg"))
        # regexBtn.clicked.connect(self.back)
        editLayout.addWidget(regexBtn)
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

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.Resize):
            print( 'Inside event Filter')
        return super().eventFilter(obj, event)

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
            selBtn.setStyleSheet("background-color: #292929; color: #fff; border: 0px")
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
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel(root_path))
        self.fileRoot = root_path
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