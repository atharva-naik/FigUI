
# NOTE: 
#  For using gmail you need to enable imap [link]()
#  and for enabling login from "less secure apps", enable that using: [link](https://myaccount.google.com/lesssecureapps)

from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QProcess
# from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase, QWindow
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QStatusBar, QToolBar, QWidget, QLineEdit, QMainWindow, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QSizePolicy, QTextEdit, QToolButton, QLabel, QSplitter, QTabWidget
try:
    from FigUI.subSystem.Email.backend import IMapMailHandler
except ImportError:
    from .backend import IMapMailHandler


class FigEmailClient(QWidget):
    '''A simple e-mail client.'''
    def __init__(self, parent=None, imap_url: str="imap.gmail.com"):
        # dummy layout (to sort of set Central Widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        super(FigEmailClient, self).__init__(parent)
        # backend for mailing operations.
        print("creating mailer backend")
        self._mailer_backend = IMapMailHandler(imap_url)
        # the main view/widget of the mail client UI.
        print("created mailer backend")
        self.view = QSplitter(Qt.Horizontal)
        self.folderTree = self.initInboxes(self.view) 
        self.view.addWidget(self.folderTree)
        # self.view.addWidget(self.mailView)
        # add the main view to the dummy layout.
        layout.addWidget(self.view)    
        self.setLayout(layout)

    @property
    def imap_url(self):
        return self._mailer_backend.imap_url

    def initInboxes(self, parent=None):
        '''return folder tree for sections of the inbox.'''
        inboxes = QWidget(parent)
        inboxes
        
        return inboxes

    def initMainMenu(self):
        '''create the top main menu.'''
        mainMenu = QTabWidget()
        # file menu tab.
        fileMenu = self.initFileMenu()
        mainMenu.addTab(fileMenu, "File")
        mainMenu.setCurrentIndex(0)

        return mainMenu

    def initFileMenu(self):
        '''create file menu'''
        fileMenu = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        # 
        QToolButton(fileMenu)

        fileMenu.addLayout(layout)

        return fileMenu

    def initMailView(self):
        mailView = QWidget()

        return mailView

    def postMail(self):
        pass

    def loadMail(self):
        pass


if __name__ == '__main__':
    pass