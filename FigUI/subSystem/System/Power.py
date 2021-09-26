#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, math
import json, datetime, pathlib
# import psutil, webbrowser, threading
# from PyQt5.Qt import PYQT_VERSION_STR
from PyQt5.QtCore import QThread, QUrl, QTimer, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QTextFormat, QColor, QPainter, QDesktopServices, QWindow
from PyQt5.QtWidgets import QMenu, QAction, QPushButton, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QToolBar, QSizePolicy, QDesktopWidget, QLabel, QToolButton, QListWidget, QDialog


class FigPowerController(QPushButton):
    def __init__(self, parent=None):
        super(FigPowerController, self).__init__(parent)
        self.menu = QMenu(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.createMenu()
        self.setToolTip("Hold for power off, right click for more options...")
        self.customContextMenuRequested.connect(self.showMenu)
        self.pressed.connect(self.shutDownDialog)
        # self.msg = QMessageBox()
        self.confirmationDialog = QDialog()
        self.createConfirmationDialog()

    def createConfirmationDialog(self):
        # self.confirmationDialog.setIcon(QMessageBox.Information)
        # self.confirm.setText("Do you want to shutdown your PC?") # set text
        # self.msg.setInformativeText("Your PC will be shutdown if you click ok!")
        self.confirmationDialog.setWindowTitle("Shutdown Confirmation")
        # self.confirmationDialog.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.confirmationDialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.msg.setGeometry(200, 200, 500, 50)

    def shutDownDialog(self):
        op = self.confirmationDialog.exec_()
        print(op)

    def createMenu(self):
        '''create power (context) menu'''
        # ["Ubuntu Help...", "Lock/Switch Account...", "Log Out...", "Suspend", "Shut Down..."]
        self.menu.addAction(QAction('Ubuntu Help...', self))
        self.menu.addSeparator()
        self.menu.addAction(QAction('Lock/Switch Account...', self))
        self.menu.addSeparator()
        self.menu.addAction(QAction('Log Out...', self))
        self.menu.addSeparator()
        self.menu.addAction(QAction('Suspend', self))
        self.menu.addAction(QAction('Shut Down...', self)) 

    def showMenu(self, point):
        self.menu.exec_(self.mapToGlobal(point))


if __name__ == '__main__':
    pass