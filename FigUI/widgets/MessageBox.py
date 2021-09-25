#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from inspect import Attribute
import PyQt5, re
import tempfile, random
import textwrap, subprocess
import os, sys, glob, pathlib
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit, QFrame, QSizePolicy, QMessageBox
# custom message box

class FigMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super(FigMessageBox, self).__init__(parent)

