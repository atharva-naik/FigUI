# handler codes for various image file formats.
import os, stat
import mimetypes
from PIL import Image
from jinja2 import Template
from PIL.ExifTags import TAGS
import os, sys, logging, datetime, pathlib
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QToolBar, QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QSizePolicy


def getStatInfo(path, fstring="%a,%b %d %Y %H:%M:%S"):
    import datetime, pathlib
    fname = pathlib.Path(path)
    stat_output = fname.stat()
    a_time = stat_output.st_atime
    m_time = stat_output.st_mtime
    a_time = datetime.datetime.fromtimestamp(a_time)
    m_time = datetime.datetime.fromtimestamp(m_time)
    a_time = a_time.strftime(fstring)
    m_time = m_time.strftime(fstring)

    return {"access" : a_time,
            "modify" : m_time}

def getColors(path, topk=8):
    from PIL import Image
    import extcolors, colormap
    # with tempfile.NamedTemporaryFile(mode="wb") as jpg:
    img = Image.open(path)
    img.thumbnail((500,500))
    img.save("/tmp/tempfile_tempimg_12345.png")
    colors,_ = extcolors.extract_from_path("/tmp/tempfile_tempimg_12345.png")
    hexcolors = []
    tot = sum([clr[1] for clr in colors])
    for clr, count in colors:
        hexcolors.append((
            colormap.rgb2hex(*clr), 
            round(100*count/tot,1) 
        ))
   
    return hexcolors[:topk]

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


class ImageWebView(QWebEngineView):
    # TODO: 
    def __init__(self, path, parent=None):
        super(ImageWebView, self).__init__(parent)
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
        from pathlib import Path
        filename = e.mimeData().text().strip()
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
        self.menu.popup(event.globalPos())

    def execJS(self, script, callback=None):
        if callback is None:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script))
        else:
            self.loadFinished.connect(lambda: self.page().runJavaScript(script, callback))

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
        sinfo = getStatInfo(path)
        img = Image.open(path)
        # extract image metadata.
        exifdata = img.getexif()
        metadata = []
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            metadata.append((tag, data))

        width, height = img.size
        # print("type:", mimetypes.guess_type(self.path))
        import json
        color_hist = json.load(open(__static__("color_histograms.json"), 'r'))
        try:
            colors = color_hist[path]
            print("found in cache!")
        except KeyError:
            colors = getColors(path)
            color_hist[path] = colors
            json.dump(color_hist, open(__static__("color_histograms.json"),  "w"))
        
        self.viewer_params = {
            "NAME" : pathlib.Path(self.path).name,
            "MIMETYPE" : mimetypes.guess_type(self.path)[0],
            "FILE_SIZE" : os.path.getsize(self.path),
            "FILE_PATH" : self.path,
            "ACCESS_TIME" : sinfo["access"],  
            "MODIFY_TIME" : sinfo["modify"], 
            "IMAGE_WIDTH" : width,
            "IMAGE_HEIGHT" : height,
            "IMAGE_URL" : getLocalUrl(path).toString(), 
            "IMAGE_HISTOGRAM" : colors,
            "JQUERY_JS" : localStaticUrl("jquery.js").toString(),
            "EDITOR_PATH" : localStaticUrl("editor_rendered.html").toString(),
            "IMAGE_METADATA": metadata,
        }
        
        self.editor_params = {
            "FABRIC_JS" : localStaticUrl("fabric.js").toString(),
            "VIEWER_PATH" : localStaticUrl("viewer_rendered.html").toString(),
            "FILE_SAVER_MIN_JS" : localStaticUrl("FileSaver.min.js").toString(),
            "IMAGE_FILE_PATH" : getLocalUrl(path).toString(),
            "IMAGE_FILE_NAME" : pathlib.Path(path).stem,
            "COLOR_PICKER_JS" : localStaticUrl("tui-color-picker.js").toString(),
            "COLOR_PICKER_CSS" : localStaticUrl("tui-color-picker.css").toString(),
            "TUI_IMAGE_EDITOR_CSS" : localStaticUrl("tui-image-editor.css").toString(),
            "TUI_IMAGE_EDITOR_JS" : localStaticUrl("tui-image-editor.js").toString(),
            "TUI_CODE_SNIPPET_MIN_JS" : localStaticUrl("tui-code-snippet.min.js").toString(),
        }
        
        self.editor_template = Template(open(__static__("editor.html")).read())
        self.viewer_template = Template(open(__static__("viewer.html")).read())
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.viewer = ImageWebView(path, self)
        self.viewer.setZoomFactor(1.25)
        
        open(__static__("viewer_rendered.html"),"w").write(self.viewer_template.render(**self.viewer_params))
        open(__static__("editor_rendered.html"),"w").write(self.editor_template.render(**self.editor_params))
        
        self.viewer.load(localStaticUrl("viewer_rendered.html"))
        layout.addWidget(self.viewer)
        self.setLayout(layout)
    # def save(self):
    #     open(self.path, "w").write(code)
if __name__ == "__main__":
    test_app = QApplication(sys.argv)
    test_app.setCursorFlashTime(100)
    