from PyQt5.QtCore import QThread, QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QFileDialog, QScrollArea, QFrame, QGraphicsBlurEffect, QGraphicsDropShadowEffect, QLineEdit
try:
    from FigUI.assets.Linker import FigLinker
except ImportError:
    from .assets.Linker import FigLinker


linker = FigLinker(__file__, "../../assets")
class FigSearchBarBtn(QToolButton):
    def __init__(self, parent=None, icon_size=(30,30), **kwargs):
        super(FigSearchBarBtn, self).__init__(parent, **kwargs)
        self.setIcon(linker.FigIcon("sysbar/search.png"))
        self.setIconSize(QSize(*icon_size))


class FigSearchBar(QWidget):
    def __init__(self, parent=None):
        super(FigSearchBar, self).__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.searchBar = QLineEdit()
        self.searchBar.setStyleSheet('''
            QLineEdit {
                margin: 0px;
                padding: 0px;
                border-radius: 0px;
                font-size: 18px;
            }
        ''')
        self.searchBar.setPlaceholderText("    Type here to search    ")
        self.setStyleSheet('''
            QWidget {
                margin: 0px;
                padding: 0px;
                color: #404040;
                background: #ebebeb;
            }
        ''')
        self.searchBar.setFixedHeight(45)
        self.searchBar.setMinimumWidth(300)
        # self.searchBtn = FigSearchBarBtn(self)
        self.searchAction = QAction('Search')
        self.searchAction.setIcon(linker.FigIcon("ctrlbar/search.svg"))
        self.voiceAction = QAction('Voice')
        self.voiceAction.setIcon(linker.FigIcon("ctrlbar/tts.svg"))
        self.cortanaAction = QAction("Cortana is a skank")
        self.cortanaAction.setIcon(linker.FigIcon("ctrlbar/cortana.svg"))
        self.searchBar.addAction(self.cortanaAction, self.searchBar.LeadingPosition)
        self.searchBar.addAction(self.searchAction, self.searchBar.LeadingPosition)
        self.searchBar.addAction(self.voiceAction, self.searchBar.TrailingPosition)
        # add widgets.
        layout.addWidget(self.searchBar)
        # layout.addWidget(self.searchBtn)        
        self.setLayout(layout)