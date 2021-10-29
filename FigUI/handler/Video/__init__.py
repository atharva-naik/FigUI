#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vlc
import os, sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, QSplitter, QAction, QFileDialog, QApplication, QStyleOptionSlider, QStyle, QLabel, QToolButton, QLineEdit
try:
    from FigUI.assets.Linker import FigLinker
except ImportError:
    from ...assets.Linker import FigLinker

sliderStyleSheet = '''
QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 6px;
    border-radius: 2px;
}

QSlider::handle:horizontal { 
	background-color: #e85035; 
	/* border: 1px solid #e85035; */
    width: 6px; 
	height: 6px; 
	line-height: 6px; 
	border-radius: 1px; 
}

QSlider::handle:horizontal:hover { 
	background-color: gray; 
	/* border: 1px solid gray; */
}

QSlider::add-page:qlineargradient {
    background: #121212;
    border-radius: 5px;
}

QSlider::sub-page:qlineargradient {
    background: #e85035;
    border-radius: 6px;
}
'''

def fmtTime(timestamp):
    import time
    timestamp = int(timestamp)
    ms = timestamp % 1000
    ms = str(ms).rjust(3, "0")
    s = timestamp // 1000
    timestr = time.strftime('%H:%M:%S', time.gmtime(s))

    return str(timestr) # f"{timestr}:{ms}"

def extractTime(timestr): 
    '''extract time from timestring and return millis.'''
    import time
    splits = timestr.split(":")
    N = len(splits)-1
    timeInt = 0
    for i, split_ in enumerate(splits):
        try:
            timeInt += (60**(N-i))*int(split_.strip())
        except: # if any error in format then return 0.
            return 0

    return timeInt*1000

class CustomSlider(QSlider):
    def __init__(self, x, parent=None):
        super(CustomSlider, self).__init__(x, parent)
        self.setStyleSheet(sliderStyleSheet)

    def mousePressEvent(self, event):
        '''Jump to click position'''
        position = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        try:
            self.mediaplayer_ref.set_position(position / 1000.0)
        except:
            print("can't seek, as no media player ref found.")
        # window.seekMusic(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))

    def mouseMoveEvent(self, event):
        '''ump to pointer position while moving'''
        position = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
        self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width()))
        try:
            self.mediaplayer_ref.set_position(position / 1000.0)
        except:
            print("can't seek, as no media player ref found.")
        self.setToolTip(str(position))

class FigVideoPlayer(QMainWindow):
    '''Fig Video player. A frontend for VLC, style inspired by YouTube's layout.'''
    def __init__(self, master=None):
        super(FigVideoPlayer, self).__init__()
        self.setWindowTitle("Fig Video Player")
        self.isSideBarVisible = False
        self.linker = FigLinker(__file__, rel_path="../../../assets")
        # create basic vlc instance.
        self.instance = vlc.Instance('-q --mouse-hide-timeout=14400000')
        # create empty vlc player.
        self.mediaplayer = self.instance.media_player_new()
        # main layout.
        videoLayout = QVBoxLayout() 
        # layout.setContentsMargins(0, 0, 0, 0)
        # create central widget.
        self.videoWidget = QWidget(self)
        # create sub widgets.
        self.videoFrame = self.initVideoFrame()
        self.posSlider = self.initPosSlider(self.mediaplayer)
        self.controls = self.initControls()
        self.carousel = self.initCarousel()
        # build main layout.
        videoLayout.addWidget(self.videoFrame)
        videoLayout.addWidget(self.posSlider)
        videoLayout.addLayout(self.controls)
        # set layout.
        self.videoWidget.setLayout(videoLayout)
        self.isPaused = False
        self.currFile = None
        self.centralWidget = QSplitter(Qt.Horizontal)
        self.collapse = self.initCarouselBtn()
        self.centralWidget.addWidget(self.videoWidget)
        self.centralWidget.addWidget(self.collapse)
        self.centralWidget.addWidget(self.carousel)
        # set central widget.
        self.setCentralWidget(self.centralWidget)
        # set style of central widget.
        self.centralWidget.setStyleSheet('''
        QWidget {
            color: #fff;
            background: #292929;
        }
        QToolButton {
            font-family: Helvetica;
            padding-left: 3px;
            padding-right: 3px;
            padding-top: 3px;
            padding-bottom: 3px;
            margin-top: 1px;
            margin-bottom: 1px;
            margin-left: 1px;
            margin-right: 1px;
            border-radius: 14px; 
        }
        QToolButton:hover {
            background: rgba(232, 177, 167, 0.3);
        }''')

    def toggleSideBar(self):
        if self.isSideBarVisible:
            self.carousel.hide()
            self.collapse.collapseBtn.setIcon(self.linker.FigIcon("video/expand.svg"))
        else:
            self.carousel.show()
            self.collapse.collapseBtn.setIcon(self.linker.FigIcon("video/collapse.svg"))
        self.isSideBarVisible = not(self.isSideBarVisible)

    def initTranscript(self):
        pass

    def initTextArea(self):
        pass

    def initCarouselBtn(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        
        layout.addStretch(1)
        collapseBtn = QToolButton(self)
        collapseBtn.setIcon(self.linker.FigIcon("video/expand.svg"))
        collapseBtn.clicked.connect(self.toggleSideBar)
        layout.addWidget(collapseBtn)
        collapseWidget = QWidget()
        collapseWidget.setLayout(layout)
        layout.addStretch(1)
        collapseWidget.collapseBtn = collapseBtn
        collapseWidget.setMaximumWidth(25)

        return collapseWidget

    def initCarouselControls(self):
        '''create carousel controls.'''
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        ctrls = QWidget()
        # frames view button.
        framesBtn = QToolButton(self)
        framesBtn.setToolTip("View frames.")
        framesBtn.setIcon(self.linker.FigIcon("video/frames.svg"))
        layout.addWidget(framesBtn)
        # chapters view button.
        chapBtn = QToolButton(self)
        chapBtn.setToolTip("View frames.")
        chapBtn.setIcon(self.linker.FigIcon("video/chapters.svg"))
        layout.addWidget(chapBtn)
        # local files.
        localBtn = QToolButton(self)
        localBtn.setToolTip("View frames.")
        localBtn.setIcon(self.linker.FigIcon("video/local.svg"))
        layout.addWidget(localBtn)
        # search results.
        webSearchBtn = QToolButton(self)
        webSearchBtn.setToolTip("View online search results.")
        webSearchBtn.setIcon(self.linker.FigIcon("video/online_results.svg"))
        layout.addWidget(webSearchBtn)
        ctrls.setLayout(layout)

        return ctrls

    def initCarousel(self):
        '''
        Carousel panels:
        1. Frames list.
        2. Chapters list.
        3. Video Carousel (local videos).
        4. Search results (online search).
        '''
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(0)

        carouselCtrls = self.initCarouselControls()
        layout.addWidget(carouselCtrls)
        layout.addStretch(1) 

        carousel = QWidget()
        carousel.setLayout(layout)
        carousel.hide()

        return carousel

    def initMainMenu(self):
        '''
        1. file
        2. edit (video editing tools)
        3. view (zoom in, zoom out, mini player)
        4. search (search web, search frames by image, search local)
        5. convert (thumbnail, video format, cc, transcription, cc translation etc.)
        6. share
        7. properties (duration, encoding, all that jazz)
        '''
        pass

    def initVideoFrame(self):
        '''In this widget, the video will be drawn'''
        if sys.platform == "darwin":
            # to handle MacOS.
            from PyQt5.QtWidgets import QMacCocoaViewContainer	
            videoframe = QMacCocoaViewContainer(0)
        else:
            videoframe = QFrame()
        palette = videoframe.palette()
        palette.setColor(QPalette.Window, QColor(0,0,0))
        videoframe.setPalette(palette)
        videoframe.setAutoFillBackground(True)

        return videoframe

    def initControls(self):
        '''create video navigation and media controls'''
        ctrlLayout = QHBoxLayout()
        # time readout.
        self.timelabel = QLabel(fmtTime(0))
        ctrlLayout.addWidget(self.timelabel)      
        # play/pause video.
        self.playBtn = QToolButton(self)
        self.playBtn.setIcon(self.linker.FigIcon("video/play"))
        self.playBtn.setToolTip("Toggle play/pause.")
        ctrlLayout.addWidget(self.playBtn)
        self.playBtn.clicked.connect(self.togglePlay)
        # replay video.
        self.replayBtn = QToolButton(self)
        self.replayBtn.setIcon(self.linker.FigIcon("video/replay.svg"))
        self.replayBtn.setToolTip("Replay video.")
        ctrlLayout.addWidget(self.replayBtn)
        self.replayBtn.clicked.connect(self.replay)
        # seek backward.
        self.backwardBtn = QToolButton(self)
        self.backwardBtn.setIcon(self.linker.FigIcon("video/seek_left.svg"))
        self.backwardBtn.setToolTip("Seek forward.")
        ctrlLayout.addWidget(self.backwardBtn)
        # seek prompt area.
        self.seekPrompt = QLineEdit(self)
        self.seekPrompt.setPlaceholderText("00:00")
        self.seekPrompt.setAlignment(Qt.AlignCenter)
        self.seekPrompt.setMaximumWidth(70)
        self.seekPrompt.returnPressed.connect(self.seekTimeStamp)
        ctrlLayout.addWidget(self.seekPrompt)
        # seek forward.
        self.forwardBtn = QToolButton(self)
        self.forwardBtn.setIcon(self.linker.FigIcon("video/seek_right.svg"))
        self.forwardBtn.setToolTip("Seek forward.")
        ctrlLayout.addWidget(self.forwardBtn)
        # self.forwardBtn.clicked.connect(self.forward)
        # playback rate dropdown.
        self.rateBtn = QToolButton(self)
        self.rateBtn.setIcon(self.linker.FigIcon("video/speed.svg"))
        self.rateBtn.setToolTip("Set playback rate.")
        ctrlLayout.addWidget(self.rateBtn)
        # playback rate prompt area.
        self.speedPrompt = QLineEdit(self)
        self.speedPrompt.setPlaceholderText("1.00x")
        self.speedPrompt.setAlignment(Qt.AlignCenter)
        self.speedPrompt.setMaximumWidth(60)
        self.speedPrompt.returnPressed.connect(self.setSpeed)
        ctrlLayout.addWidget(self.speedPrompt)
        # loop video.
        self.loopBtn = QToolButton(self)
        self.loopBtn.setIcon(self.linker.FigIcon("video/loop.svg"))
        self.loopBtn.setToolTip("Loop video after it ends.")
        ctrlLayout.addWidget(self.loopBtn)
        self.loopBtn.clicked.connect(self.loopVideo)
        # stop video.
        self.stopBtn = QToolButton(self)
        self.stopBtn.setIcon(self.linker.FigIcon("video/stop.svg"))
        self.stopBtn.setToolTip("Clear playback source.")
        ctrlLayout.addWidget(self.stopBtn)
        self.stopBtn.clicked.connect(self.clearMedia)
        # loop video.
        self.ccBtn = QToolButton(self)
        self.ccBtn.setIcon(self.linker.FigIcon("video/closed_captions.svg"))
        self.ccBtn.setToolTip("Activate closed captions.")
        ctrlLayout.addWidget(self.ccBtn)
        # self.ccBtn.clicked.connect(self.loopVideo)
        # transcribe video.
        self.transcribeBtn = QToolButton(self)
        self.transcribeBtn.setIcon(self.linker.FigIcon("video/transcribe.svg"))
        self.transcribeBtn.setToolTip("Activate closed captions.")
        ctrlLayout.addWidget(self.transcribeBtn)
        # translate closed captions.
        self.transBtn = QToolButton(self)
        self.transBtn.setIcon(self.linker.FigIcon("video/translate.svg"))
        self.transBtn.setToolTip("Translate closed captions.")
        ctrlLayout.addWidget(self.transBtn)
        # open file.
        self.openBtn = QToolButton(self)
        self.openBtn.setIcon(self.linker.FigIcon("video/open.svg"))
        self.openBtn.setToolTip("Open video file.")
        self.openBtn.clicked.connect(self.onClickOpen)
        ctrlLayout.addWidget(self.openBtn)
        # share video.
        self.shareBtn = QToolButton(self)
        self.shareBtn.setIcon(self.linker.FigIcon("video/share.svg"))
        self.shareBtn.setToolTip("Share video online.")
        ctrlLayout.addWidget(self.shareBtn)
        # share on youtube.
        self.ytBtn = QToolButton(self)
        self.ytBtn.setIcon(self.linker.FigIcon("video/youtube.svg"))
        self.ytBtn.setToolTip("Share video on youtube.")
        ctrlLayout.addWidget(self.ytBtn)
        ctrlLayout.addStretch(1)
        # control volume.
        self.volSlider = QSlider(Qt.Horizontal, self)
        self.volSlider.setMaximum(100)
        self.volSlider.setValue(100)
        self.volSlider.setValue(self.mediaplayer.audio_get_volume())
        self.volSlider.setToolTip("Volume")
        # self.volSlider.setStyleSheet('''
        # QSlider::groove:horizontal {
        #     border: 1px solid #999999;
        #     height: 6px;
        # }

        # QSlider::handle:horizontal {  
        #     width: 10px; 
        #     height: 10px; 
        #     line-height: 20px; 
        #     border-radius: 1px; 
        # }

        # QSlider::handle:horizontal:hover { 
        #     background-color: gray; 
        # }

        # QSlider::add-page:qlineargradient {
        #     background: #121212;
        #     border-radius: 5px;
        # }
        # QSlider::sub-page:qlineargradient {
        #     background: #e85035;
        #     border-radius: 6px;
        # }''')
        ctrlLayout.addWidget(self.volSlider)
        self.volSlider.valueChanged.connect(self.setVolume)
        # open and exit actions.
        openAct = QAction("&Open", self)
        openAct.triggered.connect(self.openFile)
        # exit videoplayer action.
        exitAct = QAction("&Exit", self)
        exitAct.triggered.connect(sys.exit)
        # create menu bar.
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        # timer for ?
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)  

        return ctrlLayout

    def replay(self):
        '''replay video by setting position to 0.'''
        if self.isPaused:
            self.togglePlay()
        self.setPosition(0)

    def loopVideo(self):
        pass

    def setSpeed(self):
        speed = self.speedPrompt.text()
        speed.replace("x","")
        try: speed = float(speed)
        except: return # if error in format then return.
        self.setRate(speed)

    def setRate(self, rate=1):
        self.mediaplayer.set_rate(rate)

    def seekTimeStamp(self):
        timeStr = self.seekPrompt.text()
        timeInt = extractTime(timeStr)
        duration = self.media.get_duration()
        # print(timeInt, duration)
        ratio = min(timeInt/duration, 0.99)
        self.mediaplayer.set_position(ratio)

    def initPlaybackControls(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)


    def initPosSlider(self, mediaplayer):
        posSlider = CustomSlider(Qt.Horizontal, self)
        posSlider.mediaplayer_ref = self.mediaplayer
        posSlider.setToolTip("Navigate Video")
        posSlider.setMaximum(1000)
        posSlider.sliderMoved.connect(self.setPosition)
        posSlider.valueChanged.connect(self.updateTimestamp)

        return posSlider

    def updateTimestamp(self, value):
        value = (self.mediaplayer.get_length())*(value/1000)
        self.timelabel.setText(f"{fmtTime(value)}/{fmtTime(self.media.get_duration())}")

    def onClickOpen(self):
        '''when open button is clicked.'''
        # print(self.mediaplayer.play(), self.mediaplayer.is_playing())
        # when no media is chosen
        if self.currFile is None:
            self.openFile()
        # when current video is playing.
        elif self.mediaplayer.is_playing():
            self.togglePlay()
            self.openFile()
        # when current video is paused.
        else:
            self.openFile()

    def togglePlay(self):
        '''Toggle play/pause status'''
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playBtn.setIcon(self.linker.FigIcon("video/play.svg"))
            # self.playBtn.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.openFile()
                return
            self.mediaplayer.play()
            self.playBtn.setIcon(self.linker.FigIcon("video/pause.svg"))
            # self.playBtn.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def clearMedia(self):
        """clear media from player.
        """
        self.mediaplayer.stop()
        self.playBtn.setText("Play")

    def openFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))[0]
        if not filename:
            return
        self.currFile = filename
        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoFrame.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoFrame.winId()))
        self.togglePlay()

    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def setPosition(self, position):
        """
        function for setting the position to where the slider was dragged
        
        -> vlc MediaPlayer needs a float value between 0 & 1, Qt uses integer variables, so you need a factor. 
        -> The higher the factor, the more precise are the results (1000 should be enough)
        """
        self.mediaplayer.set_position(position / 1000.0)


    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.posSlider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.clearMedia()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = FigVideoPlayer()
    player.setWindowFlags(Qt.WindowStaysOnTopHint)
    player.show()
    player.resize(1280, 720)
    if sys.argv[1:]:
        player.openFile(sys.argv[1])
    sys.exit(app.exec_())
# import vlc
# import os, sys, logging, datetime, pathlib
# from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
# from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
# from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QToolButton
# class VLCManager:
#     def __init__(self):
#         self.instance = vlc.Instance()
#         self.mediaplayers = []

#     def new(self):
#         self.mediaplayers.append(self.instance.media_player_new())


# SCREENSHOT_FUNC = '''
# function getScreenshot(videoEl, scale) {
#     scale = scale || 1;

#     const canvas = document.createElement("canvas");
#     canvas.width = videoEl.clientWidth * scale;
#     canvas.height = videoEl.clientHeight * scale;
#     canvas.getContext('2d').drawImage(videoEl, 0, 0, canvas.width, canvas.height);

#     const image = new Image()
#     image.src = canvas.toDataURL();
# '''
# SCREENSHOT_JS = '''
# var vid = document.getElementsByTagName("video")[0];
# function getScreenshot(videoEl, scale) {
#     scale = scale || 1;

#     const canvas = document.createElement("canvas");
#     canvas.width = videoEl.clientWidth * scale;
#     canvas.height = videoEl.clientHeight * scale;
#     canvas.getContext('2d').drawImage(videoEl, 0, 0, canvas.width, canvas.height);

#     const image = new Image()
#     image.src = canvas.toDataURL();
#     return image;
# }
# return getScreenshot(vid).getAttribute("src");
# '''

# class CustomSlider(QSlider):
#     def mousePressEvent(self, event):
#         super(CustomSlider, self).mousePressEvent(event)
#         if event.button() == Qt.LeftButton:
#             val = self.pixelPosToRangeValue(event.pos())
#             self.setValue(val)

#     def pixelPosToRangeValue(self, pos):
#         opt = QStyleOptionSlider()
#         self.initStyleOption(opt)
#         gr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)
#         sr = self.style().subControlRect(QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)

#         if self.orientation() == Qt.Horizontal:
#             sliderLength = sr.width()
#             sliderMin = gr.x()
#             sliderMax = gr.right() - sliderLength + 1
#         else:
#             sliderLength = sr.height()
#             sliderMin = gr.y()
#             sliderMax = gr.bottom() - sliderLength + 1;
#         pr = pos - sr.center() + sr.topLeft()
#         p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
#         return QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
#                                                sliderMax - sliderMin, opt.upsideDown)

# sliderStyleSheet = '''
# QSlider::groove:horizontal { 
# 	background-color: black;
# 	border: 0px solid #424242; 
# 	height: 12px; 
# 	border-radius: 4px;
# }

# QSlider::handle:horizontal { 
# 	background-color: gray; 
# 	border: 1px solid gray; 
# 	width: 10px; 
# 	height: 10px; 
# 	line-height: 20px; 
# 	border-radius: 4px; 
# }

# QSlider::handle:horizontal:hover { 
# 	border-radius: 4px;
#     background-color: red; 
#     border: 1px solid red; 
# }
# ''' 