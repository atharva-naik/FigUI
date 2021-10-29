from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QVariant, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QListWidget


class FigSysDashboard(QWidget):
    def __init__(self, parent=None):
        super(FigSysDashboard, self).__init__()
        layout = QVBoxLayout()
        procList = self.initProcList()
        layout.addWidget(procList)
        self.setLayout(layout)

    def initProcList(self):
        '''create widget to display list of active processes.'''
        procList = QListWidget()
        return procList

def test_dashboard(argv):
    app = QApplication(argv)
    dashboard = FigSysDashboard()
    dashboard.show()
    app.exec_()


if __name__ == '__main__':
    test_dashboard(sys.argv)