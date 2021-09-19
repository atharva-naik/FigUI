import os
import json
import pathlib
import datetime
from typing import Union
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl


class HistoryLogger:
    '''
    Class for logging and reading history
    '''
    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # get path of history directory.
        self.dir = os.path.join(current_dir, "../assets/history/")
        # create history folder.
        os.makedirs(self.dir, exist_ok=True)
        # file for storing a days history. 
        self.file = datetime.datetime.now().strftime("%Y-%b-%d.history")
        self.path = os.path.join(self.dir, self.file)
        # create the file.
        open(self.path, "a")
        self.title = datetime.datetime.now().strftime("%d %b %Y")

    def log(self, handler: str, path: Union[str, QUrl]) -> None:
        ''' path can be a file path or a url '''
        if isinstance(path, QUrl):
            path = path.toString() # convert QUrl to string.
        now = datetime.datetime.now().strftime("%-I:%M:%S %p %a %b %d %Y")
        record = {"handler": handler, "path": path, "time": now}
        # log info.
        with open(self.path, "a") as f:
            f.write("\n"+json.dumps(record))

    def __iter__(self):
        ''' iterator that yields each record line by line '''
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                try:
                    record = json.loads(line)
                except:
                    record = {"handler": None, "path":"ERROR in fetching record", "time": "[MISSING]"}

                yield record