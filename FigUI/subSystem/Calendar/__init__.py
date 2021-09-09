# handler codes for various image file formats.
from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy


def localStaticUrl(filename):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    STATIC = os.path.join("static", filename)
    
    return QUrl.fromLocalFile(os.path.join(CURRENT_DIR, STATIC))

def __static__(filename):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", filename)

    return os.path.join(CURRENT_DIR, rel_path)

def getLocalUrl(filename):
    return QUrl.fromLocalFile(filename)


class CalendarWebView(QWebEngineView):
    # TODO: 
    def __init__(self, path, parent=None):
        super(CalendarWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        # self.load(path)
    # def load(self, path):
    #     self.uris = []
    #     self.files = []
    #     self.path = path
    #     self.dir = str(pathlib.Path().parent)
        
    #     for file in os.listdir(self.dir):
    #         self.files.append(os.path.join(self.dir, file))
    #         self.uris.append(getLocalUrl(self.files[-1]).toString())
    #     self.uri = getLocalUrl(self.path).toString()
    def dragEnterEvent(self, e):
        '''use drag event on ics files to add events to the callendar.'''
        from pathlib import Path
        filename = e.mimeData().text().strip()
        file_format = Path(filename).suffix
        # if file_format == ".pdf":
        #     self.setHtml(pdfRenderContext, baseUrl=QUrl.fromLocalFile(str(Path(__file__).resolve().parent)))
        #     print(filename)
        #     if self.enable_zoom: self.attachJSZoomHandler
        #     # self.load_pdf(filename) 
        super(CalendarWebView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.popup(event.globalPos())

    def execJS(self, script, callback=None):
        if callback is None:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script))
        else:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script, callback))

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class FigCalendar(QWidget):
    '''
    You need to provide a file always. 
    If you want to code a new script, create a file first at a given path and then open it.
    --'''
    def __init__(self, path, parent=None):
        super(FigCalendar, self).__init__(parent=parent)
        self.path = path
        self.params = {
            "FABRIC_JS" : localStaticUrl("fabric.js").toString(),
            "FILE_SAVER_MIN_JS" : localStaticUrl("FileSaver.min.js").toString(),
            "IMAGE_FILE_PATH" : getLocalUrl(path).toString(),
            "IMAGE_FILE_NAME" : pathlib.Path(path).stem,
            "COLOR_PICKER_JS" : localStaticUrl("tui-color-picker.js").toString(),
            "COLOR_PICKER_CSS" : localStaticUrl("tui-color-picker.css").toString(),
            "TUI_IMAGE_EDITOR_CSS" : localStaticUrl("tui-image-editor.css").toString(),
            "TUI_IMAGE_EDITOR_JS" : localStaticUrl("tui-image-editor.js").toString(),
            "TUI_CODE_SNIPPET_MIN_JS" : localStaticUrl("tui-code-snippet.min.js").toString(),
        }
        self.template = Template(open(__static__("viewer.html")).read())
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.viewer = CalendarWebView(path, self)
        self.viewer.setZoomFactor(1.25)
        open(__static__("rendered.html"),"w").write(self.template.render(**self.params))
        self.viewer.load(localStaticUrl("rendered.html"))
        layout.addWidget(self.viewer)
        self.setLayout(layout)
    # def save(self):
    #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
    