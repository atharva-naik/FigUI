import pathlib, os
import FigUI.handler.Image.svg
import FigUI.handler.Archives.pt
import FigUI.handler.Archives.pkl
import FigUI.handler.Archives.zip
from PyQt5.QtWidgets import QFileDialog, QLabel


class FigHandler:
    def __init__(self, parent=None):
        self.path = None
        self.parent = parent

    def handle(self):
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
        if self.ext == ".pkl":
            self.handler = FigUI.handler.Archives.pkl.PickleHandler(self.path)
            return self.handler.getUI(path)       
        else:
            return QLabel("no handler found")
        # elif self.ext == ".svg":
        #     self.handler = FigUI.handler.Image.svg.SvgHandler(self.path)


if __name__ == '__main__':
    pass