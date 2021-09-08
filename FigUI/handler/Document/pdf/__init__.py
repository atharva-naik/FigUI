from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QImage, QFont, QKeySequence, QTransform, QTextCharFormat, QPixmap
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QLabel
# highlightFunction = '''
# function load(){
#       window.document.designMode = "On";
#       //run this in a button, will highlight selected text
#       window.document.execCommand("hiliteColor", false, "#768");
#     }
# '''
getHighlightCoords = '''
function getHighlightCoords() {
var pageIndex = PDFViewerApplication.pdfViewer.currentPageNumber - 1; 
var page = PDFViewerApplication.pdfViewer.getPageView(pageIndex);
var pageRect = page.canvas.getClientRects()[0];
var selectionRects = window.getSelection().getRangeAt(0).getClientRects();
var viewport = page.viewport;
var selected = selectionRects.map(function (r) {
  return viewport.convertToPdfPoint(r.left - pageRect.x, r.top - pageRect.y).concat(
     viewport.convertToPdfPoint(r.right - pageRect.x, r.bottom - pageRect.y)); 
});
return {page: pageIndex, coords: selected};
}
'''

def localStaticUrl(filename):
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    STATIC = os.path.join("static", filename)
    
    return QUrl.fromLocalFile(os.path.join(CURRENT_DIR, STATIC)).toString()

def getLocalUrl(filename):
    return QUrl.fromLocalFile(filename).toString()


class PDFWebView(QWebEngineView):
    # TODO: 
    def __init__(self, parent=None):
        super(PDFWebView, self).__init__(parent)
        self.consoleHistory = []
        self.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(QWebEngineSettings.ErrorPageEnabled, True)
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.execJS(getHighlightCoords)
        # self.execJS(highlightFunction)
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
        super(PDFWebView, self).dragEnterEvent(e)
    # def dropEvent(self, e):
    #     e.ignore()
    def contextMenuEvent(self, event):
        self.menu = self.page().createStandardContextMenu()
        self.highlightAction = self.menu.addAction('Higlight')
        self.highlightAction.triggered.connect(self.highlightText)
        self.menu.popup(event.globalPos())

    def highlightText(self):
        print("higlighted")
        self.execJS("alert('lol')")
        self.execJS("getHighlightCoords()", self.getData)

    def getData(self, data):
        print("data:", data, "type:", type(data))

    def execJS(self, script, callback=None):
        if callback is None:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script))            
        else:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script, callback))

    def alert(self, message):
        self.execJS(f"alert('{message}')")


class FigPdfViewer(QWidget):
    '''
    You need to provide a file always. 
    If you want to code a new script, create a file first at a given path and then open it.
    --'''
    def __init__(self, path, parent=None):
        import fitz
        self.doc = fitz.open(path)
        super(FigPdfViewer, self).__init__(parent=parent)
        self.path = path
        # self.params = {
        #     "CODE_FILE_CONTENT" : self.code,
        #     "EDITOR_BACKGROUND_COLOR" : "#292929",
        #     "JQUERY_MIN_JS" : serve("jquery.min.js"),
        #     "MODERNIZR_MIN_JS" : serve("modernizr.min.js"),
        #     "SUBLIME_SCROLL_JS" : serve("sublimeScroll.js"),
        #     "SUBLIME_SCROLL_CSS" : serve("sublimeScroll.css"),
        #     "SUBLIME_SCROLL_LITE_JS" : serve("sublimeScrollLite.js"),
        #     "SUBLIME_SCROLL_LITE_CSS" : serve("sublimeScrollLite.css"),
        # }
        self.setupUIJS()

    def setupUIJS(self):
        PDFJS = localStaticUrl("pdfjs/web/viewer.html")
        PDF = getLocalUrl(self.path)
        layout = QVBoxLayout()
        self.viewer = PDFWebView(self)
        self.viewer.load(QUrl.fromUserInput(f'{PDFJS}?file={PDF}'))
        layout.addWidget(self.viewer)
        self.setLayout(layout)

    def setupUImg(self):
        page = self.doc.load_page(1)
        pix = page.get_pixmap()
        fmt = QImage.Format_RGBA8888 if pix.alpha else QImage.Format_RGB888
        qtimg = QImage(pix.samples_ptr, pix.width, pix.height, fmt)
        label = QLabel(self)
        label.setPixmap(QPixmap.fromImage(qtimg))

    def setupUIHtml(self):
        pdf_html = ""
        print(len(self.doc))
        for i in range(10):
            # pages.append(self.doc.load_page(i+1))
            try:
                pdf_html += self.doc.load_page(i+1).get_text("html")
                pdf_html += f"<br><h3>Page {i+1}<h3><br>"
            except ValueError:
                print(i)
                pass
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.viewer = PDFWebView(self)
        self.viewer.setZoomFactor(1.25)
        self.viewer.setHtml(pdf_html)
        layout.addWidget(self.viewer)
        self.setLayout(layout)
    # def save(self):
    #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
    