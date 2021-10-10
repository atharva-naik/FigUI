#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, glob, pathlib
from PIL import Image, ImageQt
from typing import Union, List, Tuple
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QPoint, QPropertyAnimation, QSequentialAnimationGroup, QEasingCurve, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap, QColor, QBrush
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QFileDialog, QScrollArea, QMainWindow, QGraphicsBlurEffect, QGraphicsDropShadowEffect, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsWidget
try:
    from utils import *
    from FlowLayout import FlowLayout
    from assets.Image import ImageAsset
except ImportError:
    from FigUI.utils import *
    from FigUI.assets.Image import ImageAsset
    from FigUI.widgets.FlowLayout import FlowLayout


__current_dir__ = os.path.dirname(os.path.realpath(__file__))
__icons__ = os.path.join(__current_dir__, "../assets/icons")
__fonts__ = os.path.join(__current_dir__, "../assets/fonts")

def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)


class FigWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self, obj, func, **kwargs):
        getattr(obj, func)(**kwargs)
        self.finished.emit()


class FigToolButton(QToolButton):
    def __init__(self, 
                 parent=None, 
                 size=(100,100), 
                 icon_size=(60,60)):
        super(FigToolButton, self).__init__(parent)
        self.keep_running = True
        self.setFixedSize(QSize(*size))
        self.setIconSize(QSize(*icon_size))

    def enterEvent(self, event):
        shadowEffect = QGraphicsDropShadowEffect(self)
        shadowEffect.setOffset(0, 0)
        shadowEffect.setColor(QColor(255, 213, 0))
        shadowEffect.setBlurRadius(50)
        self.setGraphicsEffect(shadowEffect)

    def leaveEvent(self, event):
        self.setGraphicsEffect(None)

    def _animateMovie(self):
        import time
        while self.keep_running:
            self._gifMovie.seek(self._gifIndex)
            pixmap = QPixmap.fromImage(ImageQt.ImageQt(self._gifMovie))
            self.setIcon(QIcon(pixmap))
            self.setIconSize(QSize(*self.size))
            time.sleep(self.rate/1000)
            self._gifIndex += 1
            self._gifIndex %= self._gifLength
            # print("keep_runing=", self.keep_running)
    def _endAnimation(self):
        self.keep_running = False
        # print("keep_runing=", self.keep_running)
        self.thread.join()
    def setMovie(self, path, rate=100, size=(60,60)):
        import threading
        # self.setStyleSheet("background: color(0, 0, 0, 100)")
        self.size = size
        self.rate = rate
        self.thread = threading.Thread(target=self._animateMovie)
        self._gifIndex = 0
        self._gifMovie = Image.open(path)
        self._gifLength = self._gifMovie.n_frames
        self.thread.start()
# class FigScrollArea(QWidget):
#     def __init__(self, parent=None):
#         super(FigScrollArea, self).__init__(parent)
#         self.setAttribute(Qt.WA_StyledBackground)
#         widget = QWidget()
#         widget.setStyleSheet("""QWidget{ background:#fff; color:#000;}""")
#         blur_effect = QGraphicsBlurEffect(blurRadius=5)
#         widget.setGraphicsEffect(blur_effect)

#         self._scrollarea = QScrollArea(parent=self)
#         self.scrollarea.setStyleSheet(""" background-color : transparent; color : black""")
#         self.scrollarea.setContentsMargins(10, 0, 10, 0)

#         lay = QVBoxLayout(self)
#         lay.addWidget(widget)

#     @property
#     def scrollarea(self):
#         return self._scrollarea

#     def sizeHint(self):
#         return self._scrollarea.sizeHint()

#     def resizeEvent(self, event):
#         self._scrollarea.resize(self.size())
#         self._scrollarea.raise_()
#         return super().resizeEvent(event)
class SunAnimation:
    def __init__(self, parent=None, size: Tuple[int, int]=(200, 200)):
        self.sunSprite = QWidget(parent)
        self.sunSprite.setObjectName("Sun")
        # self.sunSprite.setAttribute(Qt.WA_TranslucentBackground)
        self._size = size
        self._center = (size[0]/2, size[1]/2)
        self.sunSprite.setStyleSheet('''
            QWidget#Sun {
                border-radius: 100;
                background: qradialgradient(cx: 1, cy: 1, radius: 1, stop : 0 #fff, stop: 0.5 #000);            
                /* background-image: url('/home/atharva/GUI/FigUI/FigUI/assets/icons/animations/sun.png');
                background-repeat: no-repeat;
                background-position: center; */
            }
        ''')
        self.sunSprite.resize(*size)
        self._animation_group = QSequentialAnimationGroup()
        self.sunSprite.hide()

    @property
    def size(self):
        return self._size

    @property
    def center(self):
        return self._center

    def addAnimation(self, 
                     initial_state: Union[QPoint, Tuple[int, int]],
                     goal_state: Union[QPoint, Tuple[int, int]]=QPoint(800, 0), 
                     duration: int=1000,
                     curve: QEasingCurve=QEasingCurve.OutBounce):
        anim = QPropertyAnimation(self.sunSprite, b"pos")
        anim.setStartValue(initial_state)
        anim.setEndValue(goal_state)
        anim.setEasingCurve(curve)
        anim.setDuration(duration)
        self._animation_group.addAnimation(anim)
        self._animation_group.finished.connect(self.destroyAnimation)

    def _start(self, count):
        print("starting animation")
        self.sunSprite.show()
        self._animation_group.setLoopCount(count)
        self._animation_group.start()

    def destroyAnimation(self):
        '''clear up the animation artefacts after waiting for some time.'''
        # wait for 5 seconds and the hide the sun.
        print("destroying animation")
        pyqtSleep(5000)
        self.sunSprite.hide()

    def start(self, count: int=1):
        '''
        self.thread = QThread()
        self.worker = FigWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(lambda: self.worker.run(self, 
                                        "_start", 
                                        count=count))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # TODO: check dis.
        # self.init_worker.progress.connect(self.reportProgress)
        self.thread.start()
        '''
        self._start(count)


class FigLauncher(QWidget):
    def __init__(self, parent=None, width=8, button_size=(100,100), icon_size=(70,70)):
        super(FigLauncher, self).__init__()
        launcher_layout = FlowLayout()
        # layout.setContentsMargins(2, 2, 2, 2)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.launcherWidget = QGraphicsView(self)
        # 5A8034
        # self.launcherWidget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.gifBtn = None
        self._parent = parent
        # creating a blur effect
        self.blur_effect = QGraphicsBlurEffect()
        # setting blur radius
        self.blur_effect.setBlurRadius(5)
        
        # this snippet of code is to setup a blurred background image.
        if parent:
            img_path = parent.background
            stem = pathlib.Path(img_path).stem
            self.bg_url = f"/tmp/FigUI.Launcher?={stem}.png"
            if not os.path.exists(self.bg_url):
                self.bg_img = ImageAsset(img_path)
                self.bg_img.thumbnail(1920, 1080)
                self.bg_img.gaussBlur(5).save(self.bg_url)
        
        # self.scroll.setStyleSheet("background: rgba(73, 44, 94, 0.5);")
        # self.scroll.setAttribute(Qt.WA_TranslucentBackground, True)
        self.launcherWidget.setStyleSheet('''
            QGraphicsView {
                background-image: url('''+ f"'{self.bg_url}'" +''');
                background-position: center;
                border: 0px;
            }
        ''')
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet('''
            QScrollArea {
                /* background-color: rgba(90, 12, 63, 0.5); */
                background: url('''+ f"'{self.bg_url}'" +'''); /* no-repeat; */
                background-position: center;
                border: 0px;
            }
            QScrollBar:vertical {
                border: 0px solid #999999;
                width: 8px;    
                margin: 0px 0px 0px 0px;
                background-color: rgba(227, 140, 89, 0.5);
            }
            QScrollBar::handle:vertical {         
                min-height: 0px;
                border: 0px solid red;
                border-radius: 4px;
                background-color: #e38c59; /* #c70039; */
            }
            QScrollBar::add-line:vertical {       
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }''')
        # self.scroll.setStyleSheet('''background: rgba(73, 44, 94, 0.5);''')
        self.glowEffect = QGraphicsDropShadowEffect(self)
        self.glowEffect.setOffset(2, 2)
        self.glowEffect.setColor(QColor(255, 132, 0))
        self.glowEffect.setBlurRadius(50)
        # add glow to vertical scroll bar.
        self.vscrollBar = self.scroll.verticalScrollBar()
        self.vscrollBar.setGraphicsEffect(self.glowEffect)

        exclude = ["eclipse", "android", "mozilla", "kivy", "netbeans", "nano", "gnome", "tor", "openoffice", "thunderbird", "dbus", "compiz"]

        launcher_icons = glob.glob(os.path.join(__icons__, "launcher/*"))
        filt_launcher_icons = []
        for icon in launcher_icons: 
            stem = pathlib.Path(icon).stem 
            if stem not in exclude:
                filt_launcher_icons.append(icon)
            else:
                pass
                # print(f"excluded icon for {stem}")

        for i,path in enumerate( sorted(filt_launcher_icons, key=lambda x: x.lower()) ):
            name = pathlib.Path(path).stem
            ext = os.path.splitext(path)[1]

            launcherButton = FigToolButton(self.launcherWidget) # QToolButton(self)
            launcherButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            launcherButton.setText(name)
            launcherButton.setMaximumSize(QSize(*button_size))

            if ext == ".gif":
                launcherButton.setMovie(path, size=icon_size)       
                self.gifBtn = launcherButton
            else:
                launcherButton.setIcon(QIcon(path))
                launcherButton.setIconSize(QSize(*icon_size))
            launcherButton.setAttribute(Qt.WA_TranslucentBackground)
            launcherButton.setStyleSheet('''
            QToolButton {
                color: #fff;
                border: 0px;
                background: transparent;
                border-radius: 50px;
            }
            /* #c70039; */
            QToolButton:hover { 
                background: qradialgradient(cx: 0.6, cy: 0.6, radius: 0.5, stop : 0.3 #ffd500, stop: 0.6 #ffdf61, stop: 0.9 #fcf2ca); 
                font-weight: bold;
                color: #292929;
            }''')
            # background: #42f2f5;
            if name == "browser":
                if parent: 
                    parent.logger.debug("connected browser launcher")
                launcherButton.clicked.connect(parent.addNewTab)
            elif name == "bash":
                if parent:
                    parent.logger.debug("connected terminal launcher")
                launcherButton.clicked.connect(parent.addNewTerm)
            elif name == "Desktop":
                home = str(pathlib.Path.home())
                desktop = os.path.join(home, "Desktop")
                launcherButton.clicked.connect(lambda: parent.addNewFileViewer(path=desktop))
            elif name == "history":
                launcherButton.clicked.connect(lambda: parent.addNewHistoryViewer())
            elif name == "fileviewer":
                if parent:
                    parent.logger.debug("connected terminal launcher")
                launcherButton.clicked.connect(parent.addNewFileViewer)
            elif name == "bashrc":
                if parent:
                    parent.logger.debug("connected bashrc customizer")
                launcherButton.clicked.connect(parent.addNewBashrcViewer)
            elif name == "license":
                if parent:
                    parent.logger.debug("connected license generator")
                launcherButton.clicked.connect(lambda: parent.addNewLicenseGenerator())                
            elif name == "txt":
                if parent:
                    parent.logger.debug("connected text editor")
                launcherButton.clicked.connect(lambda: parent.addNewTextEditor())
            else:
                if parent:
                    parent.logger.debug(f"connected FigHandler instance to '{name}' button")
                    launcherButton.clicked.connect(parent.addNewHandlerTab)
            launcher_layout.addWidget(launcherButton)
            # layout.addWidget(launcherButton, i // width, i % width)
            launcherButton.clicked.connect(self._clickHandler)
        
        self.launcherWidget.setLayout(launcher_layout)
        self.scroll.setWidget(self.launcherWidget) # comment
        
        self.welcomeLabel = QPushButton("Welcome to FIG, launch an app!")
        figLogo = FigIcon("logo.png")
        self.welcomeLabel.setIcon(figLogo)
        self.welcomeLabel.setStyleSheet("color: #734494; border: 0px")
        self.welcomeLabel.setAttribute(Qt.WA_TranslucentBackground)
        self.welcomeLabel.setIconSize(QSize(100,100))
        #self.welcomeLabel.setMaximumWidth(900)
        self.welcomeLabel.setFont(QFont('OMORI_GAME2', 40))

        # self.layout.addWidget(self.welcomeLabel, alignment=Qt.AlignCenter)
        # self.layout.addWidget(self.launcherWidget) 
        self.layout.addWidget(self.scroll) # comment
        self.setLayout(self.layout)
        self.setAcceptDrops(True)

        if self._parent and isinstance(self._parent, QMainWindow):
            print("\x1b[31mconnected FigLauncher.showWeather\x1b[0m")
            self._parent.weatherBtn.clicked.connect(self.showWeather)

    def showWeather(self):
        weather = "sunny"
        if weather == "sunny":
            self.sun_animation = SunAnimation(self)
            w = self.width() # x coordinate of initial point.
            h = self.height() # y coordinate of initial point.s
            c_x, c_y = self.sun_animation.size
            initial_state = QPoint(w-c_x, 0)
            goal_state = QPoint((w-c_x)/2, h-c_y)
            self.sun_animation.addAnimation(initial_state=initial_state, 
                                       goal_state=goal_state,
                                       curve=QEasingCurve.OutBounce,
                                       duration=2000)
            self.sun_animation.start(count=3)

    def _clickHandler(self, event):
        pass

    def dragEnterEvent(self, e):
        import pathlib
        from pathlib import Path
        from urllib.parse import urlparse, unquote_plus
        
        e.accept()
        e.acceptProposedAction()
        filename = e.mimeData().text().strip("\n").strip()
        filename = unquote_plus(filename).replace("file://","")
        print(filename)

        if self._parent:
            handlerWidget = self._parent.handler.getUI(filename)
            name = pathlib.Path(filename).name
            thumbnail = getThumbnail(filename)
            parent = ".../" + pathlib.Path(filename).parent.name
            i = self._parent.tabs.addTab(handlerWidget, FigIcon(thumbnail), f"\t{truncateString(name)} {parent}")
            self._parent.tabs.setCurrentIndex(i)

        super(FigLauncher, self).dragEnterEvent(e)