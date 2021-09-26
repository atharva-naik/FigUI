#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Chat Layout: messages in a scroll area'''
import PyQt5
import typing
import os, re, sys
import glob, pathlib
# import textwrap, subprocess
# from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QPixmap
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QWidget, QToolBar, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QScrollArea, QLineEdit, QSizePolicy
try:
    from .assets.Linker import FigLinker
except ImportError:
    from FigUI.assets.Linker import FigLinker


class FigChatLayout(QWidget):
    def __init__(self, parent=None):
        super(FigChatLayout, self).__init__(parent)
        pass
        self.setLayout()


if __name__ == '__main__':
    pass