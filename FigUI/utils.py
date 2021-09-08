import os
from PyQt5.QtGui import QFont, QIcon


def truncateString(string):
    if len(string) > 20:
        return string[:10]+"..."+string[-6:]
    else:
        return string

def FigIcon(name, w=None, h=None):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "assets/icons")
    path = os.path.join(__icons__, name)

    return QIcon(path)

def FigFont(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "assets/fonts")
    path = os.path.join(__icons__, name)

    return QFont(path)

def __icon__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "assets/icons")
    path = os.path.join(__icons__, name)

    return path

def __font__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "assets/fonts")
    path = os.path.join(__icons__, name)

    return path

def getThumbnail(path):
    import pathlib, subprocess
    name = pathlib.Path(path).name 
    _,ext = os.path.splitext(name)
    stem = pathlib.Path(path).stem
    print("thumbnail:", ext)
    # print(self.name, self.stem, ext, os.path.isfile(self.path))
    ext = ext[1:]
    if name.lower() == "todo": return "launcher/todo.png"
    # elif ext in ["png","jpg"]: # display standard thumbnail for png/jpg.
    #     return path
    elif stem == "README": return "launcher/README.png"
    elif stem == "requirements": return "launcher/requirements.png"
    elif stem.lower() == "license": return "launcher/license.png"
    elif stem == ".gitignore": return "launcher/gitignore.png"
    elif ext == "":
        if subprocess.getoutput(f"file --mime-encoding {path}").endswith("binary"):
            return "launcher/bin.png"
        else:
            return "launcher/txt.png"
    if os.path.exists(__icon__(f"launcher/{ext}.png")): # check if png file for the ext
        return f"launcher/{ext}.png"
    else:
        if os.path.exists(__icon__(f"launcher/{ext}.svg")): 
            return f"launcher/{ext}.svg"
        else: 
            return f"launcher/txt.png" # if ext is not recognized set it to txt