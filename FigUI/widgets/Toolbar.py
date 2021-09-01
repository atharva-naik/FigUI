#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, glob
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QTransform
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout


class FigRBar(QToolBar):
    '''the right side toolbar of FigUI layout.'''
    