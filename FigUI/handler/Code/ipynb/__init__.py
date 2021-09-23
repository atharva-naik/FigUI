# source code for jupyter notebooks.
import sys, subprocess, signal, logging, threading
from PyQt5.QtCore import pyqtSlot, QSettings, QTimer, QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication, QWidget
# logfileformat = '[%(levelname)s] (%(threadName)-10s) %(message)s'
# logging.basicConfig(level=logging.DEBUG, format=logfileformat)

# def log(message):
#     logging.debug(message)
class CustomWebView(QWebEngineView):
    def __init__(self, mainwindow, main=False):
        super(CustomWebView, self).__init__(None)
        self.parent = mainwindow
        self.main = main
        self.loadedPage = None
        self.setZoomFactor(1.25)

    @pyqtSlot(bool)
    def onpagechange(self, ok):
        # log("on page change: %s, %s" % (self.url(), ok))
        if self.loadedPage is not None:
            # log("disconnecting on close signal")
            self.loadedPage.windowCloseRequested.disconnect(self.close)
        self.loadedPage = self.page()
        # log("connecting on close signal")
        self.loadedPage.windowCloseRequested.connect(self.close)

    def createWindow(self, windowtype):
        v = CustomWebView(self.parent)
        windows = self.parent.windows
        windows.append(v)
        v.show()
        return v

    def closeEvent(self, event):
        if self.loadedPage is not None:
            # log("disconnecting on close signal")
            self.loadedPage.windowCloseRequested.disconnect(self.close)
        
        if not self.main:
            if self in self.parent.windows:
                self.parent.windows.remove(self)
            # log("Window count: %s" % (len(self.parent.windows)+1))
        event.accept()


class FigJupyterNB(QWidget):
    def __init__(self, parent=None, homepage=None):
        super(FigJupyterNB, self).__init__(parent)
        self.homepage = homepage
        self.windows = []

        # settings = QSettings()
        # val = settings.value("net.fishandwhistle/JupyterQt/geometry", None)
        # if val is not None:
        #     self.restoreGeometry(val)
        self.setGeometry(300, 300, 1050, 850)
        self.basewebview = CustomWebView(self, main=True)
        self.setCentralWidget(self.basewebview)
        QTimer.singleShot(0, self.initialload)

    @pyqtSlot()
    def initialload(self):
        if self.homepage:
            self.basewebview.load(QUrl(self.homepage))
        self.show()

    def closeEvent(self, event):
        if self.windows:
            for i in reversed(range(len(self.windows))):
                w = self.windows.pop(i)
                w.close()
            event.accept()
        else:
            event.accept()

        #save geometry
        settings = QSettings()
        settings.setValue("net.fishandwhistle/JupyterQt/geometry", self.saveGeometry())


def startnotebook(notebook_executable="jupyter-notebook", port=8888, directory=QDir.homePath()):
    # --ip='*' --NotebookApp.token='' --NotebookApp.password=''
    return subprocess.Popen([notebook_executable,
                            "--port=%s" % port, 
                            "--ip='*'", 
                            "--NotebookApp.token=''", 
                            "--NotebookApp.password=''", 
                            "--browser=n", "-y",
                            "--notebook-dir=%s" % directory], bufsize=1,
                            stderr=subprocess.PIPE)


#start jupyter notebook and wait for line with the web address
# log("Starting Jupyter notebook process")
notebookp = startnotebook()

# log("Waiting for server to start...")
webaddr = None
while webaddr is None:
    line = str(notebookp.stderr.readline())
    # log(line)
    if "http://" in line:
        start = line.find("http://")
        end = line.find("/", start+len("http://"))
        webaddr = line[start:end]
# log("Server found at %s, migrating monitoring to listener thread" % webaddr)
#pass monitoring over to child thread
def process_thread_pipe(process):
    while process.poll() is None: #while process is still alive
        pass
        # log(str(process.stderr.readline()))

notebookmonitor = threading.Thread(name="Notebook Monitor", target=process_thread_pipe, args=(notebookp,))
notebookmonitor.start()

#setup application
# log("Setting up GUI")
app = QApplication(sys.argv)
app.setApplicationName("JupyterQt")
app.setOrganizationDomain("fishandwhistle.net")

#setup webview
view = MainWindow(None, homepage=webaddr)

# log("Starting Qt Event Loop")
result = app.exec_()
