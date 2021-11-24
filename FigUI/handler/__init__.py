import os
import pathlib
import subprocess
import FigUI.handler.Code
import FigUI.handler.Image
import FigUI.handler.Video
import FigUI.handler.Model3D
import FigUI.handler.Text.md
import FigUI.handler.Text.txt
import FigUI.handler.Code.html
import FigUI.handler.Image.svg
import FigUI.handler.Code.bashrc
import FigUI.handler.Archives.pt
import FigUI.handler.Archives.pkl
import FigUI.handler.Archives.zip
import FigUI.handler.Document.pdf
from PyQt5.QtWidgets import QFileDialog, QWidget, QTextEdit
try:
    from utils import *
except ImportError:
    from FigUI.utils import *

def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)


class FigHandler:
    def __init__(self, parent=None):
        self.path = None
        self.parent = parent

    def handle(self):
        # if btn.text() == "bashrc":
        #     home = pathlib.Path.home()
        #     bashrc = os.path.join(home, ".bashrc")
            
        #     return self.getUI(bashrc) 
        path = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption="Select a file",
            )
        path, filetype = path
        if path != "" and os.path.exists(path):
            widget = self.getUI(path)
        else:
            widget = QTextEdit()
            widget.setText("File Not Found")
            
        return widget

    def _set_path(self, path):
        # print("Path:", path)
        self.path = path
        self.name = pathlib.Path(path).name
        self.stem = pathlib.Path(path).stem 
        _,ext = os.path.splitext(path)
        self.ext = ext

    def getUI(self, path):
        # generate and return UI handler.
        self._set_path(path)
        # if self.parent:
        #     iconPath = getThumbnail(path)
        #     self.parent.langReadOut.setIcon(FigIcon(iconPath))
            # self.parent.langReadOut.setText(self.ext[1:])
        if self.ext == ".pkl":
            self.handler = FigUI.handler.Archives.pkl.PickleHandler(self.path)
            return self.handler.getUI(path)   
        elif self.ext == ".md":
            return FigUI.handler.Text.md.MarkdownEditor(path=path, parent=self.parent)       
        elif self.ext == ".txt":
            return FigUI.handler.Text.txt.FigTextEditor(path=path, parent=self.parent)  
        elif self.ext in [".feature", ".py", ".css", ".scss", ".less", ".js", ".cpp", ".c", ".scala", ".md"]:
            return FigUI.handler.Code.CodeEditor(path=path, parent=self.parent)
        elif self.name == ".bashrc":
            return FigUI.handler.Code.bashrc.BashrcCustomizer(parent=self.parent, path=path)
        elif self.ext in [".html"]:
            return FigUI.handler.Code.html.FigHTMLEditor(path=path, parent=self.parent)
        elif self.ext in [".pdf"]:
            return FigUI.handler.Document.pdf.FigPdfViewer(path)
        elif self.ext in [".png", ".jpg", ".gif", ".bmp"]:
            return FigUI.handler.Image.FigImageViewer(path=path, parent=self.parent)
        elif self.ext in [".webm", ".mp4", ".flv", ".ogv", ".wmv", ".mov"]:
            return FigUI.handler.Video.FigVideoPlayer(parent=self.parent, path=path)
        elif self.ext in [".stl", ".STL"]:
            return FigUI.handler.Model3D.FigModelViewer(parent=self.parent, path=path)
        elif self.ext in [".tgz", ".zip"]:
            return QWidget()
        else:
            try: 
                import magic
                magic = magic.Magic()
                mimetype = magic.from_file(path)
                print("mimetype:", mimetype)
                if mimetype == "text/plain":
                    return FigUI.handler.Text.txt.FigTextEditor(path=path, parent=self.parent) 
            # catch any possible exception.
            except: 
                pass
            subprocess.call(["xdg-open", path])
            # return QLabel("no handler found")
        # elif self.ext == ".svg":
        #     self.handler = FigUI.handler.Image.svg.SvgHandler(self.path)


if __name__ == '__main__':
    pass