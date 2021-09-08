# handler codes for various image file formats.
from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy


def localStaticUrl(filename):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    STATIC = os.path.join("static", filename)
    
    return QUrl.fromLocalFile(os.path.join(CURRENT_DIR, STATIC)).toString()

def getLocalUrl(filename):
    return QUrl.fromLocalFile(filename).toString()


class ImageWebView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(ImageWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

    def dragEnterEvent(self, e):
        from pathlib import Path
        from pprint import pprint
        filename = e.mimeData().text().strip("\n").strip()
        file_format = Path(filename).suffix
        # if file_format == ".pdf":
        #     self.setHtml(pdfRenderContext, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))
        #     print(filename)
        #     if self.enable_zoom: self.attachJSZoomHandler
        #     # self.load_pdf(filename) 
        super(ImageWebView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Refactor')
        self.menu.popup(event.globalPos())

    def execJS(self, script):
        self.loadFinished.connect(lambda: self.page().runJavaScript(script))

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class FigImageViewer(QWidget):
    '''
    You need to provide a file always. 
    If you want to code a new script, create a file first at a given path and then open it.
    --'''
    def __init__(self, path, parent=None):
        super(FigImageViewer, self).__init__(parent=parent)
        self.path = path
        self.code = open(self.path).read()
        self.params = {
            "CODE_FILE_CONTENT" : self.code,
            "EDITOR_BACKGROUND_COLOR" : "#292929",
            "JQUERY_MIN_JS" : serve("jquery.min.js"),
            "MODERNIZR_MIN_JS" : serve("modernizr.min.js"),
            "SUBLIME_SCROLL_JS" : serve("sublimeScroll.js"),
            "SUBLIME_SCROLL_CSS" : serve("sublimeScroll.css"),
            "SUBLIME_SCROLL_LITE_JS" : serve("sublimeScrollLite.js"),
            "SUBLIME_SCROLL_LITE_CSS" : serve("sublimeScrollLite.css"),
        }
        self.template = Template(open(static("code.html")).read())
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.editor = CodeWebView(self)
        self.editor.setZoomFactor(1.25)
        self.editor.setHtml(self.template.render(**self.params))
        layout.addWidget(self.editor)
        self.setLayout(layout)
    # def save(self):
    #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
    