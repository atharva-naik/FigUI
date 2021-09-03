import json, inspect, html
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout, QLineEdit


UNABLE_TO_LOAD = "There was an issue in unpickling the .pkl archive"
class PickleViewer(QWidget):
    pass


class PickleHandler:
    def __init__(self, parent=None):
        self.parent = parent

    def getUI(self, path):
        import pickle as pkl
        try:
            self.data = pkl.load(open(path, "rb"))
            widget = QWidget()
            layout = QVBoxLayout()
            searchBar = QLineEdit()
            searchBar.setStyleSheet("background: white; color: black")
            layout.addWidget(searchBar)
            textEdit = QTextEdit()
            if isinstance(self.data, dict):
                # print("\x1b[31;1mfound dict\x1b[0m")
                try:
                    string = json.dumps(self.data, indent=4)
                except:
                    string = str(self.data)
                textEdit.setText(string)
            else:
                string = ""
                string += f"data is an instance of <span style='color: green; font-weight: bold'>"+html.escape(f"{type(self.data)}")+"</span><br>"
                i = 0
                for name,func in inspect.getmembers(self.data):
                    try:
                        args = inspect.getfullargspec(func)
                        args = str(inspect.signature(func))
                        space = "&nbsp;"*4
                        args = "("+f",{space}".join(["<span style='color: yellow; font-style: italic'>"+arg+"</span>" for 
                        arg in args[1:-1].split(",")])+")"
                        # print(args)
                        tab = "&nbsp;"*8
                        string += f"{i}. <span style='color: orange; font-weight: bold'>method:</span>"+f"<span style='color: blue; font-weight: bold'>{name}</span>" + args + f":<br>{tab}{func.__doc__}<br>" 
                    except:
                        string += f"{i}. <span style='color: red; font-weight: bold'>attr:</span> {name}<br>"
                    i += 1
                textEdit.setHtml(string)
            layout.addWidget(textEdit)
            widget.setLayout(layout)
        except ImportError:
            self.data = UNABLE_TO_LOAD
            widget = QTextEdit(self.parent) 
            widget.setText(self.data)

        return widget