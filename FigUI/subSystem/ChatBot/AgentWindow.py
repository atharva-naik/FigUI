'''Chat'''
import PyQt5
import typing
import os, re, sys
import glob, pathlib
# import textwrap, subprocess
# from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QPixmap
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QWidget, QToolBar, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QTextEdit, QSizePolicy
try:
    from .assets.Linker import FigLinker
except ImportError:
    from FigUI.assets.Linker import FigLinker

# class FigLinker:
    # A class to bundle path completion resources for fig
    def __init__(self, current_dir, rel_path="../assets", static_path="static"):
        self.rel_path = rel_path
        self.static_path = static_path
        self.current_dir = os.path.realpath(current_dir)
        self.rel_font_path = os.path.join(rel_path, "fonts")
        self.rel_icon_path = os.path.join(rel_path, "icons")
        # self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.abs_path = os.path.join(self.current_dir, self.rel_path)
        self.abs_font_path = os.path.join(self.current_dir, self.rel_font_path)
        self.abs_icon_path = os.path.join(self.current_dir, self.rel_icon_path)
        self.abs_static_path = os.path.join(self.current_dir, self.static_path)

    def icon(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_icon_path, path)

    def font(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_font_path, path)

    def asset(self, path: str) -> str:
        '''return absolute path of an asset'''
        return os.path.join(self.abs_path, path)

    def static(self, path: str) -> str:
        '''give relative path and get absolute static path.'''
        return os.path.join(self.abs_static_path, path)

    def staticUrl(self, path: str) -> QUrl:
        '''local url given static path'''
        filePath = self.static(path)

        return QUrl.fromLocalFile(filePath)

    def FigIcon(self, name:str) -> QIcon :
        '''return QIcon'''
        icon_path = self.icon(name)
        icon = QIcon(icon_path)

        return icon

    def FigFont(self, name: str) -> QFont :
        '''return QFont'''
        font_path = self.icon(name)
        font = QFont(font_path)

        return font

class FigAgentWindow(QWidget):
    def __init__(self, path=None, parent=None):
        super(FigAgentWindow, self).__init__(parent)
        # create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addStretch(True)
        # create linker
        self.linker = FigLinker(__file__, rel_path="../../../assets")
        if path:
            self.path = path
        else:
            self.path = self.linker.icon("chatbot/assistant1.png")
        # profile picture
        self.profilePic = self.initProfilePic()
        # self.profilePic.setAlignment(Qt.AlignCenter)
        # description panel
        self.description = self.initDescPanel()
        # toolbar
        self.toolbar = self.initToolBar() 
        layout.insertWidget(0, self.toolbar)
        layout.insertWidget(0, self.description)
        layout.insertWidget(0, self.profilePic)
        # set style sheet
        self.setStyleSheet('''
            QWidget {
                background: #292929
            }
            QToolBar { 
                background: #292929; 
                color: #292929; 
                border: 0px;
            } 
            QToolTip { border: 0px }
            QToolButton:hover { 
                background: red;
        }''')
        # set layout
        self.setLayout(layout)

    def initProfilePic(self):
        profilePic = QWidget() 
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # left spacer
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(left_spacer)
        # profile pic
        picture = QToolButton(self)
        picture.setIcon(self.linker.FigIcon("chatbot/assistant2.png")) 
        picture.setIconSize(QSize(300,300))
        layout.addWidget(picture)
        # right spacer
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(left_spacer)

        profilePic.setLayout(layout)

        return profilePic

    def initDescPanel(self):
        panel = QTextEdit()
        panel.setText("I am a sentient chatbot bot")
        panel.setReadOnly(True)
        panel.setAlignment(Qt.AlignCenter)

        return panel

    def initToolBar(self, icon_size=(20,20)):
        toolbar = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # left spacer
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(left_spacer)
        # recognize speech
        asrBtn = QToolButton(self)
        asrBtn.setIcon(self.linker.FigIcon("chatbot/asr.svg"))
        asrBtn.setIconSize(QSize(*icon_size))
        layout.addWidget(asrBtn) 
        # speech output
        speakBtn = QToolButton(self)
        speakBtn.setIcon(self.linker.FigIcon("chatbot/speak.svg"))
        speakBtn.setIconSize(QSize(*icon_size))
        layout.addWidget(speakBtn) 
        # translate
        transBtn = QToolButton(self)
        transBtn.setIcon(self.linker.FigIcon("chatbot/trans.svg"))
        transBtn.setIconSize(QSize(*icon_size))
        layout.addWidget(transBtn) 
        # right spacer
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(right_spacer) 
        toolbar.setLayout(layout)

        return toolbar


if __name__ == '__main__':
    pass