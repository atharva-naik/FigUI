import psutil
from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QVariant, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QListWidget, QListWidgetItem


class ProcListWorker(QObject):
    pass


class SysMonitorBackend:
    def __init__(self):
        self.process_view = Template("{{ pid }} {{ name }} {{ username }}")

    def ls_proc(self):
        for process in  psutil.process_iter(['pid', 'name', 'username']):
            yield self.process_view.render(**process.info)

class FigSysDashboard(QWidget):
    def __init__(self, parent=None):
        super(FigSysDashboard, self).__init__()
        # system monitor backend.
        self.backend = SysMonitorBackend()
        layout = QVBoxLayout()
        procList = self.initProcList()
        layout.addWidget(procList)
        self.setLayout(layout)

    def initProcTools(self):
        '''tools for filtering, search, deleting elements from proclist.
        1. search process name.
        2. username dropdown.
        '''
        widget = QWidget()
        layout = QHBoxLayout()
        searchBar = QLineEdit()
        layout.addWidget(searchBar)
        widget.setLayout(layout)

        return widget

    def initProcList(self):
        '''create widget to display list of active processes.'''
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Process List"))
        procTools = self.initProcTools()
        layout.addWidget(procTools)
        procList = QListWidget()
        procListItems = []
        for ps_str in self.backend.ls_proc():
            procListItems.append(QListWidgetItem(ps_str))
            procList.addItem(procListItems[-1])
        widget.setLayout(layout)

        return procList


def test_dashboard(argv):
    app = QApplication(argv)
    dashboard = FigSysDashboard()
    dashboard.show()
    app.exec_()


if __name__ == '__main__':
    test_dashboard(sys.argv)