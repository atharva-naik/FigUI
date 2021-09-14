# an advanced editor program with AI based writing tools to write better prose. 
# AI based tools: 
# 1. Summarization
# 2. TTS
# 3. NER
# 4. Citation
# 5. PlagCheck
# 6. FactChecking
# 7. Text Completer (Langauge Model)
# 8. Thesaurus, WordNet (not just synonyms and antononyms, but hyper and hyponyms as well)
# 9. Grammar and spell check.
# 10. Speech to text.
# 11. OCR.
# 12. Create word cloud.
# 13. Compute other statistics
# 14. Translate using google translate API
# 15. Detect language
# 16. Get sentiment
# 17. Do a DEP parse. (Spacy)
# It also has an inbuilt note taking module. 
import PyQt5, re
import os, sys, pathlib
import tempfile, random
import textwrap, subprocess
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QFontDatabase, QMovie, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QTextEdit


class FigTextEditor(QWidget):
    def __init__(self, parent=None):
        super(FigTextEditor, self).__init__(parent)
        layout = QVBoxLayout()
        self.toolbar = QHBoxLayout()
        self.toolbar.addWidget()
        self.textEdit = QTextEdit()
        toolbar = QWidget()
        toolbar.setLayout(self.toolbar)
        layout.addWidget(toolbar)
        layout.addWidget(self.textEdit)