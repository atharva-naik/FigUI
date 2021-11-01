import psutil
import getpass
# from pathlib import Path
from jinja2 import Template
import os, sys, logging, datetime, pathlib
from PyQt5.QtWebChannel import QWebChannel
from typing import Union, Dict, List, Tuple
from PyQt5.QtCore import QUrl, QVariant, QObject, pyqtSlot, pyqtSignal, Qt, QThread
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QTransform, QTextCharFormat, QRegExpValidator, QSyntaxHighlighter, QFontDatabase
from PyQt5.QtWidgets import QApplication, QAction, QDialog, QPushButton, QTabWidget, QStatusBar, QToolBar, QToolButton, QWidget, QLineEdit, QTextEdit, QMainWindow, QHBoxLayout, QLabel, QVBoxLayout, QPlainTextEdit, QToolBar, QSplitter, QFrame, QSizePolicy#, QListView, QListWidget, QListWidgetItem
try:
    from FigUI.utils import *
    from FigUI.assets.Linker import FigLinker
    from FigUI.widgets.List import FigVListWidget
except ImportError:
    from ...utils import *
    from ...assets.Linker import FigLinker
    from ...widgets.List import FigVListWidget
def trunc(string: str, limit: int=100):
    if len(string) > limit:
        return string[:limit-3]+"..."
    return string
def RJust(string: str, margin: int):
    '''rjust for html.'''
    return str(string).rjust(margin, "`").replace("`", "&nbsp;")
def LJust(string: str, margin: int):
    '''ljust for html.'''
    return str(string).ljust(margin, "`").replace("`", "&nbsp;")


class ProcessItem(QTextEdit):
    def __init__(self, proc_dict: dict, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # item.setLineWrapMode(QTextEdit.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMaximumHeight(30)
        self.setReadOnly(True)
        self.setStyleSheet('''
        QTextEdit {
            background: #484848; 
            color: #fff
        }
        QTextEdit:hover {
            background: #94d0f2;
            color: #484848;
        }''')
        self.populate(proc_dict)
        # self.clicked.connect(self.onClick)
        self._parent_widget = parent

    def populate(self, proc_dict):
        # template for user created processes.
        usr_temp = Template('''<span style="font-family='Calibri'">{{ pid }}</span><span style="color: red; font-weight: bold;">{{ username }}</span>{{ name }}{{ num_threads }}{{ cpu_percent }}{{ memory_percent }}''')
        # template for root processes.
        root_temp = Template('''<span style="font-family='Monospace'">{{ pid }}</span> <span style="color: #92bf7c; font-weight: bold;">{{ username }}</span>{{ name }}{{ num_threads }}{{ cpu_percent }}{{ memory_percent }}''')
        # template for other processes.
        other_temp = Template('''<span style="font-family='Monospace'">{{ pid }}</span> <span style="color: #ffda73; font-weight: bold;">{{ username }}</span>{{ name }}{{ num_threads }}{{ cpu_percent }}{{ memory_percent }}''')
        # tab = "&nbsp;"*4
        ROOT = LJust("root", 20+2)
        USERNAME = LJust(str(getpass.getuser()), 20+2)
        proc_dict["pid"] = LJust(proc_dict["pid"], 5+4)
        proc_dict["name"] = LJust(trunc(proc_dict["name"], 30), 35+2)
        proc_dict["username"] = LJust(proc_dict["username"], 20+2)
        proc_dict["num_threads"] = LJust(proc_dict["num_threads"], 15)
        proc_dict["cpu_percent"] = LJust(f'{proc_dict["cpu_percent"]:.2f}%', 15)
        proc_dict["memory_percent"] = LJust(f'{proc_dict["memory_percent"]:.2f}%', 15)
        if proc_dict["username"] == ROOT:
            proc_html = root_temp.render(**proc_dict)
        elif proc_dict["username"] == USERNAME:
            proc_html = usr_temp.render(**proc_dict)
        else:
            proc_html = other_temp.render(**proc_dict)
        self.setHtml(proc_html)

    def onClick(self):
        if self._parent_widget:
            print()
            pass

    # def 
class ProcessDetails(QTextEdit):
    def __init__(self, parent=None, clipboard=None):
        super(ProcessDetails, self).__init__(parent)
        layout = QVBoxLayout()
        self.clipboard = clipboard
        # process object returned by psutil.
        self.procPtr = None
        self.controls = self.initControls()
        self.detailsArea = QTextEdit()
        layout.addWidget(self.detailsArea)
        layout.addWidget(self.controls)

    def initControls(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        controls = QWidget()
        copyEnvBtn = QToolButton(self)
        copyEnvBtn.setIcon(QIcon(""))
        copyEnvBtn.setText("copy env")
        copyEnvBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        copyEnvBtn.clicked.connect(self.copyEnv)
        controls.setLayout(layout)

        return controls

    def copyEnv(self):
        if self.procPtr and self.clipboard is not None:
            environ = self.procPtr.as_dict()["environ"]
            print(environ)

    def update(self, pid: int):
        self.procPtr = psutil.Process(pid)
        self.procPtr 

    def updateDetails(self):
        pass


class ProcListWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    
    def run(self, widget):
        '''for the fileviewer ui loading task.'''
        import time
        title = widget.initTitle()
        widget.procList.addWidget(title)
        while True:
            s1 = time.time()
            processes = widget.backend.list_proc("dict", k=100)
            s2 = time.time()
            # print("psutil took:", s2-s1, "s")
            for proc_dict in processes:
                item = ProcessItem(proc_dict, parent=widget)
                # add to list widget and store in process list items list.
                widget.procListItems.append(item)
                widget.procList.addWidget(widget.procListItems[-1])
            s3 = time.time()
            # print(f"PyQt5 took:", s3-s2, "s")
            # pause for a minute.
            pyqtSleep(1*1000)
            widget.procList.clear()
            title = widget.initTitle()
            widget.procList.addWidget(title)
        self.finished.emit()


class DiskUsageGraph(QWidget):
    def __init__(self, parent=None):
        pass


def default_sort(processes: list):
    return processes


class SysMonitorBackend:
    def __init__(self):
        self.process_html = Template('''{{ pid }} <b>{{ username }}</b> {{ name }}''')
        self.process_text = Template('''{{ pid }} {{ username }} {{ name }}''')
        self.process_attrs = ['cmdline', 'connections', 'cpu_affinity', 'cpu_num', 'cpu_percent', 'cpu_times', 'create_time', 'cwd', 'environ', 'exe', 'gids', 'io_counters', 'ionice', 'memory_full_info', 'memory_info', 'memory_maps', 'memory_percent', 'name', 'nice', 'num_ctx_switches', 'num_fds', 'num_threads', 'open_files', 'pid', 'ppid', 'status', 'terminal', 'threads', 'uids', 'username']
        self.process_list_attrs = ["num_threads", "cpu_percent", "memory_percent", "pid", "name", "username"]

    def list_proc(self, *args, k=10, **kwargs):
        processes = [proc for proc in self.ls_proc(*args, **kwargs)]
        processes = self.sort_proc(processes, *args, **kwargs)[:k]
        return processes

    def sort_proc(self, proceses, fmt):
        # print(fmt)
        if fmt == 'dict':
            # print("sorting")
            return sorted(proceses, key=lambda x: x["cpu_percent"]+x["memory_percent"], reverse=True)
        else:
            return proceses

    def ls_proc(self, fmt="raw"):
        for process in psutil.process_iter(self.process_list_attrs):
            if fmt == 'html':
                yield self.process_html.render(**process.info)
            elif fmt == 'dict':
                yield process.info
            elif fmt == "raw":
                yield process
            elif fmt == "text":
                yield self.process_text.render(**process.info)
            # info = {k: str(v).rjust(5) for k,v in process.info.items()}
            # info["name"]  = info["name"].rjust(12)
class FigSysDashboard(QSplitter):
    def __init__(self, parent=None):
        super(FigSysDashboard, self).__init__(Qt.Vertical, parent=parent)
        # system monitor backend.
        self.backend = SysMonitorBackend()
        # process details widget.
        procWidget = QWidget()
        procLayout = QHBoxLayout()
        procLayout.setSpacing(0)
        procLayout.setContentsMargins(0,0,0,0)
        self.procList = self.initProcList()
        # self.procDet = self.initProcDetail()
        self.procListItems = []
        procLayout.addWidget(self.procList)
        procWidget.setLayout(procLayout)
        self.addWidget(procWidget)
        # fig linker.
        self.linker = FigLinker(__file__, rel_path="../../../assets") 
        # start workers.
        import time
        start = time.time()
        # create all threads.
        # thread to list processes.
        self.process_list_thread = QThread()
        # self.network_thread = QThread()
        
        # create all workers.
        # worker to list processes
        self.process_list_worker = ProcListWorker()
        # self.network_worker = QThread()
        
        # connect slots and stuff.
        self.process_list_thread.started.connect(lambda: self.process_list_worker.run(self))
        self.process_list_worker.finished.connect(self.process_list_thread.quit)
        self.process_list_worker.finished.connect(self.process_list_worker.deleteLater)
        self.process_list_thread.finished.connect(self.process_list_thread.deleteLater)

        # move workers to threads and start.
        print(f"starting workers t={start}")
        self.process_list_worker.moveToThread(self.process_list_thread)
        self.process_list_thread.start()

        print(f"Δt={time.time()-start}")

    def initProcDetail(self):
        print(self.parent())
        procDet = ProcessDetails(parent=self.parent())
        return procDet

    def initProcTools(self):
        '''tools for filtering, search, deleting elements from proclist.
        1. search process name.
        2. username dropdown.
        '''
        widget = QWidget()
        layout = QHBoxLayout()
        searchBar = QLineEdit()
        layout.addWidget(searchBar)
        widget.setLayout(layout)

        return widget

    def initTitle(self):
        title = QTextEdit()
        title.setHtml(f'''
        <b>{LJust("PID", 5+2)}{LJust("username", 20+2)}{LJust("name", 35+2)}{LJust("THREADS", 15)}{LJust("CPU(%)", 15)}{LJust("MEM(%)", 15)}</b>
        ''')
        title.setStyleSheet("background: #000; color: #fff")
        title.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        title.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        title.setMaximumHeight(30)
        title.setReadOnly(True)

        return title

    def initProcList(self):
        '''create widget to display list of active processes.'''
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Process List"))
        procTools = self.initProcTools()
        layout.addWidget(procTools)
        procList = FigVListWidget()
        # procListItems = []
        # # template for user created processes.
        # usr_temp = Template('''<span style="font-family='Calibri'"> {{ pid }} </span> <span style="color: red; font-weight: bold;"> {{ username }} </span> {{ name }}''')
        # # template for root processes.
        # root_temp = Template('''<span style="font-family='Monospace'"> {{ pid }} </span> <span style="color: blue; font-weight: bold;"> {{ username }} </span> {{ name }}''')
        # # template for other processes.
        # other_temp = Template('''<span style="font-family='Monospace'"> {{ pid }} </span> <span style="color: yellow; font-weight: bold;"> {{ username }} </span> {{ name }}''')
        # for proc_dict in self.backend.ls_proc("dict"):
        #     item = QTextEdit()
        #     if proc_dict["username"] == "root":
        #         proc_html = root_temp.render(**proc_dict)
        #     elif proc_dict["username"] == str(getpass.getuser()):
        #         proc_html = usr_temp.render(**proc_dict)
        #     else:
        #         proc_html = other_temp.render(**proc_dict)
        #     item.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #     # item.setLineWrapMode(QTextEdit.NoWrap)
        #     item.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #     item.setMaximumHeight(30)
        #     item.setHtml(proc_html)
        #     procListItems.append(item)
        #     procList.addWidget(procListItems[-1])
        return procList

def test_dashboard(argv):
    app = QApplication(argv)
    # create system dashboard.
    dashboard = FigSysDashboard()
    # create main window.
    window = QMainWindow()
    window.setCentralWidget(dashboard)
    window.setWindowIcon(
        dashboard.linker.FigIcon("sidebar/hardware.svg")
    )
    # show window.
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    window.show()
    window.setWindowTitle("System Dashboard")
    window.setGeometry(100, 100, 800, 450)
    # window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    # window.setWindowFlags(Qt.Window)
    app.exec_()


if __name__ == '__main__':
    test_dashboard(sys.argv)