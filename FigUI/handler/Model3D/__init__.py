#!/usr/bin/env python
# source code for handling 3D model files.
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QTabWidget
try:
    from FigUI.handler.Model3D.stl import FigSTLViewer
except ImportError:
    from stl import FigSTLViewer


class FigModelViewer(QWidget):
    def __init__(self, parent=None, path=""):
        super(FigModelViewer, self).__init__(parent)
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        if path.endswith(".stl") or path.endswith(".STL"):
            self.viewer = FigSTLViewer(self, filename=path)
            self.viewer.build()
        elif path.endswith(".obj"):
            pass
        else:
            print("Unknown file format.")
        layout.addWidget(self.viewer)
        
    def initMainMenu(self):
        return QWidget()
        
