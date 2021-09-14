# a UI frontend to various popular CLI tools
import os, sys
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QTabBar

class FigInstaller(QWidget):
    '''
    This class is a frontend wrapper class around all available packaged installers. 
    It mainly just invokes the respective frontend and backend classes defined for each package installer, along with any additional tasks that may need to be peformed.
    It is a QWidget.
    '''
    def __init__(self, parent=None):
        super(FigInstaller, self).__init__(parent)