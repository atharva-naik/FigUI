# UI for markdown.
import markdown
from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QProcess
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QToolBar, QFrame, QSizePolicy, QTextEdit, QToolButton, QLabel
try:
    from . import CodeEditor
except ImportError:
    from FigUI.handler.Code import CodeEditor


def __static__(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)

    return path

def __serve__(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)
    uri = QUrl.fromLocalFile(path)

    return uri


class MarkdownView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(MarkdownView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

    def dragEnterEvent(self, e):
        e.ignore()
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Refactor')
        self.menu.popup(event.globalPos())

    def update(self, md):
        md = md.replace("`", '''${"`"}''')
        self.execJS(f"md = `{md}`")
        self.execJS(f"updateMd(md)")

    def execJS(self, script):
        self.loadFinished.connect(lambda: self.page().runJavaScript(script))

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class MarkdownEditor(QWidget):
    def __init__(self, path, parent=None):
        super(MarkdownEditor, self).__init__(parent)
        layout = QVBoxLayout()
        splitLayout = QHBoxLayout()
        toolBarLayout = QHBoxLayout()
        # editor for markdown files.
        self.editor = CodeEditor(path, self)
        # markdown renderer.
        self.viewer = MarkdownView(self)
        markdown_source = open(path).read()
        html_source = markdown.markdown(markdown_source)
        
        self.params = {
            "SHOWDOWN_JS" : __serve__("dist/showdowns.min.js").toString(),
            "SHOWDOWN_CSS" : __serve__("dist/showdowns.min.css").toString(),
        }
        self.template = Template(open(__static__("viewer.html")).read())
        self.editor.setMinimumSize(QSize(500,700))
        self.viewer.setMinimumSize(QSize(500,700))
        # self.viewer.execJS(__static__("dist/showdown.js"))
        # print(self.template.render(**self.params))
        open(__static__("rendered.html"), "w").write(self.template.render(**self.params))
        self.viewer.load(__serve__("rendered.html"))
        self.viewer.update(open(path).read())

        refreshBtn = QToolButton(self)
        refreshBtn.setText("refresh")
        refreshBtn.clicked.connect(self.update)
        # refreshBtn.setIcon()
        splitLayout.addWidget(self.editor)
        splitLayout.addWidget(self.viewer)
        toolBarLayout.addWidget(refreshBtn)

        splitWidget = QWidget()
        splitWidget.setLayout(splitLayout)
        toolBar = QWidget()
        toolBar.setLayout(toolBarLayout)

        layout.addWidget(splitWidget)
        layout.addWidget(toolBar)
        self.setLayout(layout)

    def update(self):
        text = self.editor.getText()
        self.viewer.update(text)