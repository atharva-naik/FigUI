# importing libraries
import os, sys, qrcode
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QToolBar, QLineEdit, QApplication, QFileDialog, QSizePolicy
  

def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)


class QRImage(qrcode.image.base.BaseImage):
    '''QR Image creator.'''
    def __init__(self, border, width, box_size):  
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
  
        self._image = QImage(size, size, QImage.Format_RGB16)
        self._image.fill(Qt.white)
  
    def pixmap(self):
        '''create pixmap and resize while maintaining aspect ratio.'''
        _pixmap = QPixmap.fromImage(self._image)
        _pixmap = _pixmap.scaled(500, 500, Qt.KeepAspectRatio)
        
        return _pixmap
  
    def drawrect(self, row, col):
        '''drawrect method for drawing rectangle'''
        # creating painter object
        painter = QPainter(self._image)
        # drawing rectangle
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size, Qt.black)
  
  
class FigQRCodeWindow(QMainWindow):
    '''QR Code Window'''
    def __init__(self, initial_text=None, clipboard=None):
        QMainWindow.__init__(self)
        self.initial_text = initial_text if initial_text else "your text here"
        self.setGeometry(100, 100, 300, 300)
        # creating a label to show the qr code
        self.label = QLabel(self)
        # create initial qrcode for blank text.
        qr_image = qrcode.make(self.initial_text, image_factory=QRImage).pixmap()
        self.label.setPixmap(qr_image)
        # create text bar.
        self.textBar = self.initTextBar()
        # create title bar.
        self.titleBar = self.initTitleBar()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.clipboard = clipboard

        # create vertical layout.
        widget = QWidget()
        widget.setObjectName("QRWidget")
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.textBar)
        layout.setAlignment(Qt.AlignCenter)
        widget.setLayout(layout)

        self.addToolBar(Qt.TopToolBarArea, self.titleBar)
        self.setCentralWidget(widget)
        self.setStyleSheet('''
            QWidget#QRWidget {
                background: #292929;
            }
        ''')
        self.label.setStyleSheet('''
            background: #292929;
            color: #fff;
        ''')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle(f"QR for: {self.initial_text}")
        # self.setWindowOpacity(0.9)
        # self.label.setWindowOpacity(1)
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def copyQRToClipboard(self):
        if self.clipboard:
            self.clipboard.setPixmap(self.label.pixmap())

    def initTextBar(self):
        toolbar = QWidget()
        toolbar.setObjectName("QRText")
        # build layout.
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # creating a line edit to receive text
        self.edit = QLineEdit(self)
        self.edit.setText(self.initial_text)
        self.edit.setObjectName("QRLineEdit")
        # adding handler for when enter is pressed
        self.edit.returnPressed.connect(self.renderQRCode)
        # adding handler for when text is edited.
        self.edit.textChanged.connect(self.renderQRCode)
        self.edit.setFont(QFont('Monospace', 9)) # font family
        self.edit.setAlignment(Qt.AlignCenter) # alignment
        
        self.copyBtn = QToolButton(self)
        self.copyBtn.setObjectName("QRCopyBtn")
        self.copyBtn.setToolTip("copy QR image to clipboard")
        self.copyBtn.setIcon(FigIcon("qrcreator/copy.svg"))
        self.copyBtn.clicked.connect(self.copyQRToClipboard)

        self.clearBtn = QToolButton(self)
        self.clearBtn.setObjectName("QRClearBtn")
        self.clearBtn.setToolTip("clear text")
        self.clearBtn.setIcon(FigIcon("qrcreator/clear.svg"))
        self.clearBtn.clicked.connect(lambda: self.edit.setText(""))

        self.downloadBtn = QToolButton(self)
        self.downloadBtn.setObjectName("QRDownloadBtn")
        self.downloadBtn.setToolTip("download QR code")
        self.downloadBtn.setIcon(FigIcon("qrcreator/download.svg"))
        self.downloadBtn.clicked.connect(self.downloadQRCode)

        # add all your doo dats to the HBox Layout.
        layout.addWidget(self.edit)
        layout.addWidget(self.copyBtn)
        layout.addWidget(self.clearBtn)
        layout.addWidget(self.downloadBtn)
        # set toolbar style.
        toolbar.setStyleSheet('''
            QWidget#QRText {
                color: #fff;
                background: #292929;
                border: 0px;
            }
            QLineEdit#QRLineEdit {
                color: #fff;
                background: #292929;
                border: 0px;
            }
            QLineEdit#QRLineEdit:hover {
                background: #fff;
                color: #000;
                font-weight: bold;
            }
            QToolButton {
                color: #fff;
                background: #292929;
            }
            QToolButton#QRCopyBtn:hover {
                color: #fff;
                background: green;
            }
            QToolButton#QRClearBtn:hover {
                color: #fff;
                background: red;
            }
            QToolButton#QRDownloadBtn:hover {
                color: #fff;
                background: yellow;
            }
        ''')
        toolbar.setLayout(layout)
        # self.edit.setStyleSheet('''
        #     background: #292929;
        #     color: #fff;
        #     border: 0px;
        # ''')
        return toolbar

    def downloadQRCode(self):
        _pixmap = self.label.pixmap()
        fileName, _  = QFileDialog.getSaveFileName(
            self, 
            'Save File', 
            'fig-qrcode.png', 
            '*.png'
        )
        print(fileName)
        if fileName != "":
            _pixmap.save(fileName, "PNG")

    def setWindowTitle(self, text, k=45):
        if len(text) >= k:
            text = text[:k-3]+"..." 
        self.windowTitleLabel.setText(text)

    def renderQRCode(self):
        '''render QRCode from text.'''
        # fetch text
        text = self.edit.text()
        # update window title
        self.setWindowTitle(f"QR For: {text}")
        # creating a pix map of qrcode
        try:
            qr_image = qrcode.make(text, image_factory=QRImage).pixmap()
        except qrcode.exceptions.DataOverflowError:
            qr_image = qrcode.make("data overflow occured!!", image_factory=QRImage).pixmap()
            self.edit.setText("data overflow occured!!") 
        # set image to label
        self.label.setPixmap(qr_image)

    def initTitleBar(self):
        toolbar = QToolBar("Title Bar Visibility")
        toolbar.setStyleSheet('''
        QToolBar {
            margin: 0px; 
            border: 0px; 
            color: #fff;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            background: qlineargradient(x1 : 0, y1 : 0, x2 : 0, y2 : 1, stop : 0.0 #6e6e6e, stop : 0.8 #4a4a4a, stop : 1.0 #292929);
        }''')
        toolbar.setIconSize(QSize(20,20))
        toolbar.setMovable(False)
        ctrlBtnStyle = '''
            QToolButton {
                font-family: Helvetica;
                padding-left: 0px;
                padding-right: 0px;
                padding-top: 0px;
                padding-bottom: 0px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-left: 1px;
                margin-right: 1px;
                border-radius: 11px; 
            }
            QToolButton:hover {
                background: rgba(235, 235, 235, 0.5);
            }         
        '''

        closeBtn = QToolButton(self)
        closeBtn.setToolTip("close window")
        closeBtn.setIcon(FigIcon("close.svg")) 
        closeBtn.setStyleSheet(ctrlBtnStyle)
        closeBtn.clicked.connect(lambda: self.close()) # closing logic.
        self.closeBtn = closeBtn

        minimizeBtn = QToolButton(self)
        minimizeBtn.setToolTip("minimize window")
        minimizeBtn.setIcon(FigIcon("minimize.svg"))
        minimizeBtn.clicked.connect(lambda: self.showMinimized())
        minimizeBtn.setStyleSheet(ctrlBtnStyle)
        self.minimizeBtn = minimizeBtn

        maximizeBtn = QToolButton(self)
        maximizeBtn.setToolTip("maximize window")
        maximizeBtn.setIcon(FigIcon("maximize.svg"))
        maximizeBtn.clicked.connect(lambda: self.maximize())
        maximizeBtn.setStyleSheet(ctrlBtnStyle)
        self.maximizeBtn = maximizeBtn

        titleBtnStyle = '''
            QToolButton {
                font-family: Helvetica;
                padding-left: 4px;
                padding-right: 4px;
                padding-top: 4px;
                padding-bottom: 4px;
                margin-top: 1px;
                margin-bottom: 1px;
                margin-left: 2px;
                margin-right: 2px;
                border-radius: 14px; 
            }
            QToolButton:hover {
                background: rgba(255, 223, 97, 0.5);
            }        
        '''
        windowTitleLabel = QLabel()
        windowTitleLabel.setStyleSheet("color: #fff; font-size: 16px")
        windowTitleLabel.setWordWrap(True)
        windowTitleLabel.setAlignment(Qt.AlignCenter)
        self.windowTitleLabel = windowTitleLabel
        # for center alignment.
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # blank spacer.
        blankL = QWidget()
        blankL.setFixedWidth(5)
        blankR = QWidget()
        blankR.setFixedWidth(5)

        toolbar.addWidget(blankL)
        toolbar.addWidget(closeBtn)
        toolbar.addWidget(minimizeBtn)
        toolbar.addWidget(maximizeBtn)
        toolbar.addWidget(left_spacer)
        toolbar.addWidget(windowTitleLabel)
        toolbar.addWidget(right_spacer)
        toolbar.addWidget(QToolButton(self))
        toolbar.addWidget(QToolButton(self))
        toolbar.addWidget(QToolButton(self))
        toolbar.addWidget(blankR)

        return toolbar


if __name__ == "__main__":
    testApp = QApplication(sys.argv) 
    window = FigQRCodeWindow()
    window.show()
    sys.exit(testApp.exec_())