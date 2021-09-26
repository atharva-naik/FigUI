#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Asset management for Fig'''
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QFont


class FigLinker:
    '''A class to bundle path completion resources for fig'''
    def __init__(self, current_dir, rel_path="../assets", static_path="static"):
        self.rel_path = rel_path
        self.static_path = static_path
        self.current_dir = os.path.realpath(current_dir)
        self.rel_font_path = os.path.join(rel_path, "fonts")
        self.rel_icon_path = os.path.join(rel_path, "icons")
        # self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.abs_path = os.path.join(self.current_dir, self.rel_path)
        self.abs_font_path = os.path.join(self.current_dir, self.rel_font_path)
        self.abs_icon_path = os.path.join(self.current_dir, self.rel_icon_path)
        self.abs_static_path = os.path.join(self.current_dir, self.static_path)

    def icon(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_icon_path, path)

    def font(self, path: str) -> str:
        '''return real absolute path'''
        return os.path.join(self.abs_font_path, path)

    def asset(self, path: str) -> str:
        '''return absolute path of an asset'''
        return os.path.join(self.abs_path, path)

    def static(self, path: str) -> str:
        '''give relative path and get absolute static path.'''
        return os.path.join(self.abs_static_path, path)

    def staticUrl(self, path: str) -> QUrl:
        '''local url given static path'''
        filePath = self.static(path)

        return QUrl.fromLocalFile(filePath)

    def FigIcon(self, name:str) -> QIcon :
        '''return QIcon'''
        icon_path = self.icon(name)
        icon = QIcon(icon_path)

        return icon

    def FigFont(self, name: str) -> QFont :
        '''return QFont'''
        font_path = self.icon(name)
        font = QFont(font_path)

        return font