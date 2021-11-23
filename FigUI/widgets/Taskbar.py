from typing import Union
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QToolButton, QHBoxLayout, QWidget
try:
    from FigUI.assets.Linker import FigLinker
except ImportError:
    from ..assets.Linker import FigLinker


class SmartPhoneTaskBar(QWidget):
    def __init__(self, parent=None, current_widget=None):
        # spDock = QDockWidget()
        super(SmartPhoneTaskBar, self).__init__(current_widget)
        self.icon_size = 25
        self.w = 200
        self.h = 50
        self.history = [0]
        self.linker = FigLinker(__file__, "../../assets")
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet('''
        QWidget {
            background: #eee;
        }''')
        # spTaskBar.setWindowOpacity(0.9)
        # task view button.
        if parent:
            cb1 = parent.addNewTaskView
            cb2 = lambda: parent.tabs.setCurrentIndex(0)
            cb3 = self.backTab # cb3 = parent.histBack
        else:
            cb1, cb2, cb3 = None, None, None
        btn1 = self.initBtn("smt/task-view.svg", cb1) # task view button.
        btn2 = self.initBtn("smt/home.svg", cb2) # home button.
        btn3 = self.initBtn("smt/back.svg", cb3) # back button.
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
            x = parent.width()
            y = parent.height()

            self.setGeometry(x, y, self.w, self.h)
            # self.setGeometry(x, y, 100, 30)
            self.show()
        self.current_widget = current_widget

    def backTab(self):
        try:
            self.history.pop() 
            i = self.history[-1]
            self.parent().tabs.setCurrentIndex(i)
        except IndexError:
            pass
        
    def rePos(self, bottom_pad=20):
        x = (self.current_widget.width()-self.w) / 2
        y = (self.current_widget.height()-self.h-bottom_pad)
        # print(f"repositioned: ({x},{y})")
        self.setGeometry(x, y, self.w, self.h)

    def initBtn(self, icon_path: str, callback=None):
        btn = QToolButton(self)
        btn.setIcon(self.linker.FigIcon(icon_path))
        btn.setIconSize(QSize(
            self.icon_size, 
            self.icon_size
        ))
        btn.setFixedWidth(self.h)
        btn.setFixedHeight(self.h)
        if callback:
            btn.clicked.connect(callback)
        # btn.setAttribute(Qt.WA_TranslucentBackground)
        btn.setStyleSheet('''
        QToolButton {
            background: #000;
            border-radius: '''+f"{self.h/2}"+''';
        }
        QToolButton:hover {
            background: rgba(210, 210, 210, 0.8);
        }''')

        return btn