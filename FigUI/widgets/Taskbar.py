from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolButton, QHBoxLayout, QWidget
try:
    from FigUI.assets.Linker import FigLinker
except ImportError:
    from ..assets.Linker import FigLinker


class SmartPhoneTaskBar(QWidget):
    def __init__(self, parent=None, current_widget=None):
        # spDock = QDockWidget()
        super(SmartPhoneTaskBar, self).__init__(current_widget)
        self.linker = FigLinker(__file__, "../../assets")
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('''
        QWidget {
            background: rgba(235, 235, 235, 0.9);
        }''')
        # spTaskBar.setWindowOpacity(0.9)
        # task view button.
        if parent:
            cb1 = parent.addNewTaskView
            cb2 = lambda: parent.tabs.setCurrentIndex(0)
            cb3 = None # cb3 = parent.histBack
        else:
            cb1, cb2, cb3 = None, None, None
        btn1 = self.initBtn("ctrlbar/task-view.svg", cb1) # task view button.
        btn2 = self.initBtn("ctrlbar/home.svg", cb2) # home button.
        btn3 = self.initBtn("ctrlbar/back.svg", cb3) # back button.
        # add buttons to layout.
        layout.addStretch(1)
        layout.addWidget(btn3)
        layout.addStretch(1)
        layout.addWidget(btn2)
        layout.addStretch(1)
        layout.addWidget(btn1)
        layout.addStretch(1)
        
        # taskBar.setLayout(layout)
        # spDock.setWidget(spTaskBar)
        # spDock.setAttribute(Qt.WA_TranslucentBackground)
        # self.setMaximumHeight(50)
        self.setLayout(layout)
        if current_widget:
            print(
                "w=", current_widget.width(), 
                "h=",  current_widget.height()
            )
            print("setting geometry")
            x = current_widget.width()
            y = current_widget.height()
            self.setGeometry(x, y, 100, 30)
            self.show()

    def initBtn(self, icon_path: str, callback=None):
        btn = QToolButton(self)
        btn.setIcon(self.linker.FigIcon(icon_path))
        if callback:
            btn.clicked.connect(callback)
        # btn.setAttribute(Qt.WA_TranslucentBackground)
        btn.setStyleSheet('''
        QToolButton {
            background: #000;
        }
        QToolButton:hover {
            background: red;
        }''')

        return btn