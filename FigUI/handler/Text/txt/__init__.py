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
import os, sys, pathlib
import tempfile, random
import textwrap, subprocess
from PIL import Image, ImageQt
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import QThread, QUrl, QSize, Qt, QEvent, pyqtSlot, pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QKeySequence, QTransform, QFont, QCursor, QPixmap, QColor, QTextFormat, QPainter
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtWidgets import QAction, QDialog, QPushButton, QWidget, QToolBar, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QToolButton, QTextEdit, QPlainTextEdit


def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../../../assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)

def FigFont(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../../../assets/fonts")
    path = os.path.join(__icons__, name)

    return QFont(path)

def __icon__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../../../assets/icons")
    path = os.path.join(__icons__, name)

    return path


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.textEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.textEditor.lineNumberAreaPaintEvent(event)


class QTextEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class FigTextEditor(QWidget):
    def __init__(self, path, parent=None):
        super(FigTextEditor, self).__init__(parent)
        layout = QVBoxLayout()
        
        self.toolbar = QHBoxLayout()
        self.toolbar.setContentsMargins(0, 0, 0, 0)
        # open text file.
        folderBtn = QToolButton(self)
        folderBtn.setIcon(FigIcon("scratchpad/folder.gif"))
        folderBtn.setStyleSheet("border: 0px")
        folderBtn.setToolTip("open file")
        self.toolbar.addWidget(folderBtn)
        # file menu: rename, save etc.
        fileBtn = QToolButton(self)
        fileBtn.setIcon(FigIcon("scratchpad/file.gif"))
        fileBtn.setStyleSheet("border: 0px")
        fileBtn.setToolTip("file menu")
        self.toolbar.addWidget(fileBtn)
        # undo button.
        undoBtn = QToolButton(self)
        undoBtn.setIcon(FigIcon("scratchpad/undo.gif"))
        undoBtn.setStyleSheet("border: 0px")
        undoBtn.setToolTip("undo")
        self.toolbar.addWidget(undoBtn)
        # cut button.
        cutBtn = QToolButton(self)
        cutBtn.setIcon(FigIcon("scratchpad/cut.gif"))
        cutBtn.setStyleSheet("border: 0px")
        cutBtn.setToolTip("cut")
        self.toolbar.addWidget(cutBtn)
        # paste button.
        pasteBtn = QToolButton(self)
        pasteBtn.setIcon(FigIcon("scratchpad/paste.gif"))
        pasteBtn.setStyleSheet("border: 0px")
        pasteBtn.setToolTip("paste")
        self.toolbar.addWidget(pasteBtn)
        # copy button.
        copyBtn = QToolButton(self)
        copyBtn.setIcon(FigIcon("scratchpad/copy.gif"))
        copyBtn.setStyleSheet("border: 0px")
        copyBtn.setToolTip("copy")
        self.toolbar.addWidget(copyBtn)
        # tool purposes not decided.
        t1Btn = QToolButton(self)
        t1Btn.setIcon(FigIcon("scratchpad/blade.gif"))
        t1Btn.setStyleSheet("border: 0px")
        t1Btn.setToolTip("blade")
        self.toolbar.addWidget(t1Btn)   

        t2Btn = QToolButton(self)
        t2Btn.setIcon(FigIcon("scratchpad/ink.gif"))
        t2Btn.setStyleSheet("border: 0px")
        t2Btn.setToolTip("ink")
        self.toolbar.addWidget(t2Btn)   

        t3Btn = QToolButton(self)
        t3Btn.setIcon(FigIcon("scratchpad/highlight.gif"))
        t3Btn.setStyleSheet("border: 0px")
        t3Btn.setToolTip("highlight")
        self.toolbar.addWidget(t3Btn)   

        t4Btn = QToolButton(self)
        t4Btn.setIcon(FigIcon("scratchpad/postit1.gif"))
        t4Btn.setStyleSheet("border: 0px")
        t4Btn.setToolTip("Post it")
        self.toolbar.addWidget(t4Btn)   

        t5Btn = QToolButton(self)
        t5Btn.setIcon(FigIcon("scratchpad/postit2.gif"))
        t5Btn.setStyleSheet("border: 0px")
        t5Btn.setToolTip("Post it")
        self.toolbar.addWidget(t5Btn)   

        t6Btn = QToolButton(self)
        t6Btn.setIcon(FigIcon("scratchpad/rubberband.gif"))
        t6Btn.setStyleSheet("border: 0px")
        t6Btn.setToolTip("Rubber Band")
        self.toolbar.addWidget(t6Btn) 

        t7Btn = QToolButton(self)
        t7Btn.setIcon(FigIcon("scratchpad/pin-red.gif"))
        t7Btn.setStyleSheet("border: 0px")
        t7Btn.setToolTip("Pin red")
        self.toolbar.addWidget(t7Btn) 

        t8Btn = QToolButton(self)
        t8Btn.setIcon(FigIcon("scratchpad/pin-white.gif"))
        t8Btn.setStyleSheet("border: 0px")
        t8Btn.setToolTip("Pin white")
        self.toolbar.addWidget(t8Btn) 

        t9Btn = QToolButton(self)
        t9Btn.setIcon(FigIcon("scratchpad/clipcase.gif"))
        t9Btn.setStyleSheet("border: 0px")
        t9Btn.setToolTip("clip case")
        self.toolbar.addWidget(t9Btn) 

        t10Btn = QToolButton(self)
        t10Btn.setIcon(FigIcon("scratchpad/eraser2.gif"))
        t10Btn.setStyleSheet("border: 0px")
        t10Btn.setToolTip("Eraser 2")
        self.toolbar.addWidget(t10Btn)  

        t11Btn = QToolButton(self)
        t11Btn.setIcon(FigIcon("scratchpad/stapler.gif"))
        t11Btn.setStyleSheet("border: 0px")
        t11Btn.setToolTip("Stapler")
        self.toolbar.addWidget(t11Btn)  

        t12Btn = QToolButton(self)
        t12Btn.setIcon(FigIcon("scratchpad/staples.gif"))
        t12Btn.setStyleSheet("border: 0px")
        t12Btn.setToolTip("Staples")
        self.toolbar.addWidget(t12Btn)  

        t13Btn = QToolButton(self)
        t13Btn.setIcon(FigIcon("scratchpad/staple-remover.gif"))
        t13Btn.setStyleSheet("border: 0px")
        t13Btn.setToolTip("Staple remover")
        self.toolbar.addWidget(t13Btn)  

        t14Btn = QToolButton(self)
        t14Btn.setIcon(FigIcon("scratchpad/ruler.gif"))
        t14Btn.setStyleSheet("border: 0px")
        t14Btn.setToolTip("Ruler")
        self.toolbar.addWidget(t14Btn)  

        t15Btn = QToolButton(self)
        t15Btn.setIcon(FigIcon("scratchpad/triangle.gif"))
        t15Btn.setStyleSheet("border: 0px")
        t15Btn.setToolTip("Triangle")
        self.toolbar.addWidget(t15Btn)   

        t16Btn = QToolButton(self)
        t16Btn.setIcon(FigIcon("scratchpad/tapestand.gif"))
        t16Btn.setStyleSheet("border: 0px")
        t16Btn.setToolTip("Tape Stand")
        self.toolbar.addWidget(t16Btn)   

        t17Btn = QToolButton(self)
        t17Btn.setIcon(FigIcon("scratchpad/sharpner.gif"))
        t17Btn.setStyleSheet("border: 0px")
        t17Btn.setToolTip("Sharpner")
        self.toolbar.addWidget(t17Btn)   
        # text editing area.

        # custom cursor fot text area.
        pixmap = QPixmap(__icon__("scratchpad/Pencil.gif"))
        cursor = QCursor(pixmap, 32, 32)

        self.textEdit = QTextEditor()
        self.textEdit.setStyleSheet(f"color: black")
        if path == "Untitled.txt":
            self.textEdit.setPlainText("type your text here")
        else:
            try:
                with open(path) as f:
                    self.textEdit.setPlainText(f.read())
            except UnicodeDecodeError:
                self.textEdit.setReadOnly(True)
                with open(path, 'rb') as f:
                    Bytes = f.read()
                    bits = "".join([str(bin(byte)) for byte in Bytes])
                    self.textEdit.setPlainText(bits)
        self.textEdit.viewport().setCursor(cursor)
        self.textEdit.lineNumberArea.setStyleSheet("background: #292929; color: #fff")

        toolbar = QWidget()
        toolbar.setLayout(self.toolbar)
        toolbar.setStyleSheet("background-color: rgba(100,100,100,100)")

        label = QLabel()
        label.setFont(QFont('HomemadeApple', 15))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"padding: 0px; margin: 0px; color: #700c0c; font-weight: bold")
        label.setText("Scratch    PAD")
        
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(label)
        layout.addWidget(toolbar)
        layout.addWidget(self.textEdit)
        self.setStyleSheet(f"background: url({__icon__('scratchpad/w.jpg')}); color: #000")
        self.setLayout(layout)
        self.textEdit.cursorPositionChanged.connect(self.updateCursorPos)
        self._parent = parent

    def updateCursorPos(self):
        if self._parent:
            cursor = self.textEdit.textCursor()
            line = cursor.blockNumber()+1
            col = cursor.columnNumber()+1
            self._parent.cursorBtn.setText(f"Ln {line}, Col {col}") 