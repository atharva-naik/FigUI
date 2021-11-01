#!/usr/bin/env python
import sys, vtk
# noinspection PyUnresolvedReferences
# import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
from PyQt5 import Qt
from typing import Union, List
from PyQt5.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QWidget
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# import vtk
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


class FigSTLViewer(QWidget):
    def __init__(self, parent: Union[None, QWidget]=None, filename: str=""):
        super(FigSTLViewer, self).__init__(parent)
        colors = vtkNamedColors()
        self.frame = QFrame()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)
        # create renderer and interactor.
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        # read file.
        self.reader = vtkSTLReader()
        self.reader.SetFileName(filename)
        # create mapper.
        self.mapper = vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.reader.GetOutputPort())
        # create an actor.
        self.actor = vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetDiffuse(0.8)
        self.actor.GetProperty().SetDiffuseColor(colors.GetColor3d('LightSteelBlue'))
        self.actor.GetProperty().SetSpecular(0.3)
        self.actor.GetProperty().SetSpecularPower(60.0)
        # add actor to renderer.
        self.ren.AddActor(self.actor)
        self.ren.ResetCamera()
        # add layout to frame.
        self.frame.setLayout(self.layout)
        # set central widget.
        # wrapper layout.
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def build(self):
        self.iren.Initialize()
        self.iren.Start()

if __name__ == '__main__':
    # main()
    filename = sys.argv[1] # get stl filename.
    app = Qt.QApplication(sys.argv)
    
    # window = MainWindow(filename=filename)
    # window.show()
    # window.iren.Initialize()
    # window.iren.Start()
    
    widget = FigSTLViewer(filename=filename)
    widget.show()
    widget.build()
    sys.exit(app.exec_())