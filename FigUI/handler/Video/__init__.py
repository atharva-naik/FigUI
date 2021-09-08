import vlc
import os, sys, logging, datetime, pathlib
from PyQt5.QtCore import QThread, QUrl, QRegExp, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QToolBar, QFrame, QSizePolicy, QToolButton


class VLCManager:
    def __init__(self):
        self.instance = vlc.Instance()
        self.mediaplayers = []

    def new(self):
        self.mediaplayers.append(self.instance.media_player_new())


SCREENSHOT_FUNC = '''
function getScreenshot(videoEl, scale) {
    scale = scale || 1;

    const canvas = document.createElement("canvas");
    canvas.width = videoEl.clientWidth * scale;
    canvas.height = videoEl.clientHeight * scale;
    canvas.getContext('2d').drawImage(videoEl, 0, 0, canvas.width, canvas.height);

    const image = new Image()
    image.src = canvas.toDataURL();
'''
SCREENSHOT_JS = '''
var vid = document.getElementsByTagName("video")[0];
function getScreenshot(videoEl, scale) {
    scale = scale || 1;

    const canvas = document.createElement("canvas");
    canvas.width = videoEl.clientWidth * scale;
    canvas.height = videoEl.clientHeight * scale;
    canvas.getContext('2d').drawImage(videoEl, 0, 0, canvas.width, canvas.height);

    const image = new Image()
    image.src = canvas.toDataURL();
    return image;
}
return getScreenshot(vid).getAttribute("src");
'''