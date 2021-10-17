# create UI for loading html files.
import mimetypes
import os, sys, pathlib
from typing import Union
from jinja2 import Template
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt, QObject, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QToolBar, QSplitter, QShortcut


def static(path):
    '''give relative path and get absolute static path.'''
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    rel_path = os.path.join("static", path)
    path = os.path.join(__current_dir__, rel_path)

    return path


class OnChangeHandler(QObject):
    def __init__(self, parent=None):
        super(OnChangeHandler, self).__init__()
        self.parent = parent
        self.code = ""

    @pyqtSlot(str)
    def sendCode(self, code: str):
        if self.parent:
            self.parent.refresHTML(code)


class HTMLEditor(QWebEngineView):
    def __init__(self, file: Union[str, pathlib.Path], parent=None):
        super(HTMLEditor, self).__init__(parent)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        mimetype, _ = mimetypes.guess_type(file)

        js = open(file).read() if mimetype == "application/javascript" else ""
        css = open(file).read() if mimetype == "text/css" else ""
        html = open(file).read() if mimetype == "text/html" else ""
        # template rendering params.
        self.params = {
            "JS_FILE_CONTENT": js,
            "CSS_FILE_CONTENT": css,
            "HTML_FILE_CONTENT": html,
            "QWEBCHANNEL_JS": QUrl.fromLocalFile(
                static("qwebchannel.js")
            ).toString()
        }
        # load template.
        editor_html = Template(
            open(
                static("html_editor.html")
            ).read()
        )
        # save rendered html content.
        with open(static("html_editor_rendered.html"), "w") as f:
            f.write(editor_html.render(**self.params))
        # load the rendered html editor page.
        self.load(
            QUrl.fromLocalFile(
                static("html_editor_rendered.html")
            )
        )
        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
        self.html = html
        self.setZoomFactor(1.3)
    
    def dragEnterEvent(self, e):
        super(HTMLEditor, self).dragEnterEvent(e)
    # def dragEnterEvent(self, e):
    #     from pathlib import Path
    #     from pprint import pprint
    #     filename = e.mimeData().text().strip("\n").strip() 
    #     super(HTMLPreView, self).dragEnterEvent(e)
    def dropEvent(self, e):
        e.ignore()

    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.menu.addAction('Reload')
        self.menu.popup(event.globalPos())

    def execJS(self, script):
        self.loadFinished.connect(
            lambda: self.page().runJavaScript(
                script
            )
        )

    def __call__(self) -> str:
        return self.html


class HTMLPreview(QWebEngineView):
    def __init__(self, parent=None):
        super(HTMLPreview, self).__init__(parent)
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.handler = None

    def connect(self, editor: QWebEngineView) -> None: 
        self.handler = OnChangeHandler(parent=self) 
        editor.channel.registerObject("backend", self.handler)

    def refresHTML(self, content: str) -> None:
        '''re render content'''
        filename = static("rendered-content.html")
        with open(filename, "w") as f:
            f.write(content)
        uri = QUrl.fromLocalFile(filename)
        self.load(uri)


class FigHTMLEditor(QSplitter):
    '''
    A code editor specialized for html files, with file support for
    rendering file previews.
    '''
    def __init__(self, path, parent=None):
        super(FigHTMLEditor, self).__init__(Qt.Vertical, parent=parent)
        self.path = path
        # html editor.
        self.html_editor = HTMLEditor(path, self)
        # html preview.
        self.html_preview = HTMLPreview(parent=self)
        self.html_preview.refresHTML(self.html_editor())
        self.html_preview.connect(self.html_editor)
        # setup layout.
        # layout = QVBoxLayout()
        # layout.setContentsMargins(0, 0, 0, 0)
        self.addWidget(self.html_editor)
        self.addWidget(self.html_preview)
        # self.ctrlB = QShortcut(QKeySequence("Ctrl+B"), self)
        # self.ctrlB.activated.connect(self.togglePreview)
        self.preview_visible = True
        # self.setLayout(layout)
    def togglePreview(self):
        if self.preview_visible:
            self.html_preview.hide()
        else:
            self.html_preview.show()
        self.preview_visible = not self.preview_visible

# class FigHTMLEditor(QWidget):
#     '''
#     A code editor specialized for html files, with file support for
#     rendering file previews.
#     '''
#     def __init__(self, path, parent=None):
#         super(FigHTMLEditor, self).__init__(parent=parent)
#         self.path = path
#         self.code = open(self.path).read()
#         self.viewer_template = Template(open(expandStatic("viewer.html")).read())
#         self.html_template = Template(open(expandStatic("editor.html")).read())
#         self.css_template = Template(open(expandStatic("editor.html")).read())
#         self.js_template = Template(open(expandStatic("editor.html")).read())
        
#         layout = QHBoxLayout()
#         LLayout = QVBoxLayout()
#         RLayout = QVBoxLayout()
#         layout.setContentsMargins(0, 0, 0, 0)
        
#         self.js_editor = CodeEditor(self)
#         self.css_editor = CodeEditor(self)
#         self.html_editor = CodeEditor(self)
#         self.html_viewer = HTMLPreView(self)
#         LLayout.addWidget(self.html_editor)
#         LLayout.addWidget(self.js_editor)
#         RLayout.addWidget(self.html_viewer)
#         RLayout.addWidget(self.css_editor)

#         # set codes.
#         self.js_editor.setHtml(self.html_template.render(**{
#                                     "CODE_FILE_CONTENT" : self.code, 
#                                     "EDITOR_BACKGROUND_COLOR" : "#292929"    
#                                 }))
#         self.css_editor.setHtml(self.css_template.render(**{
#                                     "CODE_FILE_CONTENT" : self.code,
#                                     "EDITOR_BACKGROUND_COLOR" : "#292929",
#                                 }))
#         self.html_editor.setHtml(self.js_template.render(**{
#                                     "CODE_FILE_CONTENT" : self.code,
#                                     "EDITOR_BACKGROUND_COLOR" : "#292929",
#                                  }))
#         self.html_viewer.setHtml(self.viewer_template.render(**{
#                                     "ICON_URL" : iconUrl("launcher/html.png"), 
#                                     "HTML_CODE" : "<h1>This is a website.</h1>"
#                                  }))
#         self.js_editor.setZoomFactor(1.25)
#         self.css_editor.setZoomFactor(1.25)
#         self.html_editor.setZoomFactor(1.25)
#         self.html_viewer.setZoomFactor(1.25)
#         # set layouts.
#         LWidget = QWidget(self)
#         RWidget = QWidget(self)
#         LWidget.setLayout(LLayout)
#         RWidget.setLayout(RLayout)
#         layout.addWidget(LWidget)
#         layout.addWidget(RWidget)
#         self.setLayout(layout)
#     # def save(self):
#     #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
# def expandStatic(path):
#     '''give relative path and get absolute static path.'''
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     rel_path = os.path.join("static", path)
#     path = os.path.join(__current_dir__, rel_path)

#     return path
# def iconUrl(path):
#     '''give url and get icon uri'''
#     __current_dir__ = os.path.dirname(os.path.realpath(__file__))
#     rel_path = os.path.join("../../assests/icons/", path)
#     path = os.path.join(__current_dir__, rel_path)

#     return QUrl.fromLocalFile(path).toString()