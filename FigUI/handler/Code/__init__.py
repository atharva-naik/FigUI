import threading
import http.server
import socketserver
from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl, QVariant, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy


# class StaticServer(http.server.SimpleHTTPRequestHandler):
#     def __init__(self, directory, *args, **kwargs):
#         super().__init__(*args, directory=directory, **kwargs)
#         self.thread = threading.Thread(target=self._serve)

#     def _serve(self):
#         with socketserver.TCPServer(("", self.port), StaticServer) as httpd:
#             print("serving at port", self.port)
#             httpd.serve_forever()

#     def serve(self, port="3000"):
#         self.port = port
#         self.start()

#     def close(self):
#         self.thread.join()
__lang_map__ = {
    ".py" : "x-python",
    ".html" : "x-html",
    ".js" : "x-javascript",
    ".css" : "css",
    ".scss" : "x-scss",
    ".less" : "x-less",
    ".md" : "x-markdown",
    ".bashrc" : "x-sh",
}

__highlight_map__ = {
    ".py" : "python",
    ".html" : "htmlmixed",
    ".js" : "javascript",
    ".css" : "css",
    ".scss" : "scss",
    ".less" : "less",
    ".md" : "markdown",
    ".bashrc" : "shell",
}

# def serve(path):
#     '''give relative path and get absolute static path.'''
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     rel_path = os.path.join("static", path)
#     path = os.path.join(__current_dir__, rel_path)
#     path = f"http://localhost:3000{path}"

#     return path

def static(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)

    return path


class CursorPosHandler(QObject):
    def __init__(self, parent=None):
        super(CursorPosHandler, self).__init__()
        self.cursorPos = [0,0] # x,y cordinates of cursor.
        self.parent = parent

    @pyqtSlot(int, int)
    def sendCursorPos(self, line, col):
        # print("Ln", line, "Col", col)
        self.cursorPos[1] = col
        self.cursorPos[0] = line
        if self.parent:
            # get parent (CodeWebView) of parent (CodeEditor)
            if self.parent._parent:
                self.parent._parent.cursorBtn.setText(f"Ln {line+1}, Col {col+1}")


class CodeWebView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(CodeWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
        # NOTE: get parent (CodeEditor) 
        self.cursorHandler = CursorPosHandler(parent=parent) 
        self.channel.registerObject("backend", self.cursorHandler)

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
        super(CodeWebView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Refactor')
        self.menu.popup(event.globalPos())

    def execJS(self, script, callback=None):
        if callback:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script, callback))
        else:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script))

    def update(self, widget):
        pass

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class CodeEditor(QWidget):
    '''
    You need to provide a file always. 
    If you want to code a new script, create a file first at a given path and then open it.
    --'''
    def __init__(self, path, parent=None):
        super(CodeEditor, self).__init__(parent=parent)
        self.path = path
        self._parent = parent
        # self.server = StaticServer("/")
        # self.server.serve()
        lang = pathlib.Path(path).suffix
        print(f"file type by .ext is: {lang}")
        if path == os.path.join(pathlib.Path.home(), ".bashrc"):
            lang = "x-sh"
        else:
            lang = __lang_map__.get(lang, "text")
        print(f"syntax highlight mode is:", lang)
        self.code = open(self.path).read()
        self.params = {
            "LANGUAGE" : lang,
            "JAR_IMAGE" : static("hints/jar.png"),
            "HINT_IMAGE" : static("hints/fix.png"),
            "CODE_FILE_CONTENT" : self.code,
            "EDITOR_BACKGROUND_COLOR" : "#292929",
            "JQUERY_MIN_JS" : static("jquery.min.js"),
            "MODERNIZR_MIN_JS" : static("modernizr.min.js"),
            "SUBLIME_SCROLL_JS" : static("sublimeScroll.js"),
            "SUBLIME_SCROLL_CSS" : static("sublimeScroll.css"),
            "SUBLIME_SCROLL_LITE_JS" : static("sublimeScrollLite.js"),
            "SUBLIME_SCROLL_LITE_CSS" : static("sublimeScrollLite.css"),
        }
        # read template.
        self.template = Template(
            open(
                static("code.html")
            ).read()
        )
        # write code_rendered.html to static.
        open(
            static("code_rendered.html"), "w"
        ).write(
            self.template.render(**self.params)
        )
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.editor = CodeWebView(self)
        self.editor.setZoomFactor(1.25)
        self.editor.load(
            QUrl.fromLocalFile(
                static("code_rendered.html")
            )
        )
        
        layout.addWidget(self.editor)
        self.setLayout(layout)

    def callback(self, data):
        print(data)
        self.innerText = str(data)

    def getText(self):
        import time
        self.innerText = None
        self.editor.execJS("document.getElementById('codemirror').innerText", self.callback)
        while self.innerText is None:
            time.sleep(1000)
            print(self.innerText)
        
        return self.innerText
    # def save(self):
    #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
    