# create UI for loading html files.
import os, sys, pathlib
from jinja2 import Template
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy


def static(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)

    return path

def expandStatic(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)

    return path

def iconUrl(path):
    '''give url and get icon uri'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("../../assests/icons/", path)
    path = os.path.join(__current_dir__, rel_path)

    return QUrl.fromLocalFile(path).toString()


class HTMLPreView(QWebEngineView):
    def __init__(self, parent=None):
        super(HTMLPreView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # def dragEnterEvent(self, e):
    #     from pathlib import Path
    #     from pprint import pprint
    #     filename = e.mimeData().text().strip("\n").strip() 
    #     super(HTMLPreView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Reload')
        self.menu.popup(event.globalPos())

    def execJS(self, script):
        self.loadFinished.connect(lambda: self.page().runJavaScript(script))


class CodeEditor(QWebEngineView):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
    # def dragEnterEvent(self, e):
    #     from pathlib import Path
    #     from pprint import pprint
    #     filename = e.mimeData().text().strip("\n").strip() 
    #     super(HTMLPreView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Reload')
        self.menu.popup(event.globalPos())

    def execJS(self, script):
        self.loadFinished.connect(lambda: self.page().runJavaScript(script))


class FigHTMLEditor(QWidget):
    '''
    A code editor specialized for html files, with file support for
    rendering file previews.
    '''
    def __init__(self, path, parent=None):
        super(FigHTMLEditor, self).__init__(parent=parent)
        self.path = path
        self.code = open(self.path).read()
        self.viewer_template = Template(open(expandStatic("viewer.html")).read())
        self.html_template = Template(open(expandStatic("editor.html")).read())
        self.css_template = Template(open(expandStatic("editor.html")).read())
        self.js_template = Template(open(expandStatic("editor.html")).read())
        
        layout = QHBoxLayout()
        LLayout = QVBoxLayout()
        RLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.js_editor = CodeEditor(self)
        self.css_editor = CodeEditor(self)
        self.html_editor = CodeEditor(self)
        self.html_viewer = HTMLPreView(self)
        LLayout.addWidget(self.html_editor)
        LLayout.addWidget(self.js_editor)
        RLayout.addWidget(self.html_viewer)
        RLayout.addWidget(self.css_editor)

        # set codes.
        self.js_editor.setHtml(self.html_template.render(**{
                                    "CODE_FILE_CONTENT" : self.code, 
                                    "EDITOR_BACKGROUND_COLOR" : "#292929"    
                                }))
        self.css_editor.setHtml(self.css_template.render(**{
                                    "CODE_FILE_CONTENT" : self.code,
                                    "EDITOR_BACKGROUND_COLOR" : "#292929",
                                }))
        self.html_editor.setHtml(self.js_template.render(**{
                                    "CODE_FILE_CONTENT" : self.code,
                                    "EDITOR_BACKGROUND_COLOR" : "#292929",
                                 }))
        self.html_viewer.setHtml(self.viewer_template.render(**{
                                    "ICON_URL" : iconUrl("launcher/html.png"), 
                                    "HTML_CODE" : "<h1>This is a website.</h1>"
                                 }))
        self.js_editor.setZoomFactor(1.25)
        self.css_editor.setZoomFactor(1.25)
        self.html_editor.setZoomFactor(1.25)
        self.html_viewer.setZoomFactor(1.25)
        # set layouts.
        LWidget = QWidget(self)
        RWidget = QWidget(self)
        LWidget.setLayout(LLayout)
        RWidget.setLayout(RLayout)
        layout.addWidget(LWidget)
        layout.addWidget(RWidget)
        self.setLayout(layout)
    # def save(self):
    #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
    