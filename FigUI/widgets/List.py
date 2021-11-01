import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QApplication


class FigVListWidget(QWidget):
    def __init__(self, parent=None):
        super(FigVListWidget, self).__init__(parent)
        # scroll area and widget
        self.scrollArea = QScrollArea()
        self.scrollWidget = QWidget()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # the main layout.
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.scrollWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.scrollWidget)
        # wrapper layout.
        self.wrapper = QVBoxLayout()
        self.wrapper.setContentsMargins(0,0,0,0)
        self.wrapper.setSpacing(0)
        self.wrapper.addWidget(self.scrollArea)
        self.setLayout(self.wrapper)

    def addWidget(self, widget: QWidget):
        self.layout.addWidget(widget)

    def clear(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            # elif child.layout() is not None:
            #     clearLayout(child.layout())
def test1(argv):
    app = QApplication(argv)
    # the main vertical list (with scroll bar)
    figVList = FigVListWidget()
    # first textarea
    text1 = QTextEdit()
    text1.setHtml('''
<h1>Header</h1>
<p>This is a paragraph.</p>
<ol>
<li>First list item</li>
<li>Second list item</li>
<li>Third list item</li>
</ol>
''')
    text2 = QTextEdit()
    text2.setText('''
It turned out that I was lead down a wrong path by putting the layout as the layout of a widget. The actual way to do this is as simple as:

scrollarea = QScrollArea(parent.widget())
layout = QVBoxLayout(scrollarea)
realmScroll.setWidget(layout.widget())

layout.addWidget(QLabel("Test"))
Which I'm pretty sure I tried originally, but hey it's working.

However this adds an issue that the layout's items are shrunk vertically instead of causing the scrollarea to add a scrollbar.
''')
    # second textarea
    figVList.addWidget(text1)
    figVList.addWidget(text2)
    figVList.show()
    app.exec()

def main(argv):
    app = QApplication(argv)
    figVList = FigVListWidget()
    line_edits = []
    for i in range(100):
        line_edit = QTextEdit()
        line_edit.setText(f"{i+1} "*(i+1))
        figVList.addWidget(line_edit)
        line_edits.append(line_edit)
    figVList.resize(400,200)
    figVList.show()    
    app.exec() 


if __name__ == "__main__":
    main(sys.argv)