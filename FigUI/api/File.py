try:
    import magic
    magic = magic.Magic()
except: # import error/platform error.
    magic = None
import os
import re
import pathlib
import argparse
import datetime
import platform

STDLinuxFolders = ["/bin", "/home", "/boot", "/etc", "/opt", "/cdrom", "/proc", "/root", "/sbin", "/usr", "/dev", "/lost+found", "/var", "/tmp", "/snap", "/media", "/lib", "/lib32", "/lib64", "/mnt"]
ThumbPhrases = ["android", "gnome", "nano", "eclipse", "cache", "java", "cargo", "compiz", "aiml", "kivy", "mozilla"]
# map for getting filenames for thumbnails given the folder name.
ThumbMap = {
            "cuda": "cu.png",
            ".sbt": "scala.png",
            ".cmake": "cmake.svg",
        }

for folder in ["openoffice", "ssh", "npm", "wine", "dbus", "thunderbird", "gradle"]:
    ThumbMap["."+folder] = folder + '.png'
for folder in ["Videos", "Desktop", "Documents", "Downloads", "Pictures"]:
    ThumbMap[folder] = folder + ".png"
ThumbMap["Music"] = "Music.svg"
ThumbMap[".rstudio-desktop"] = "R.png"
ThumbMap[".python-eggs"] = "python-eggs.png"
StemMap = {
    "requirements": "requirements.png",
    ".cling_history": "cling.png",
    ".scala_history": "scala.png",
    ".gitignore": "gitignore.png", 
    ".gitconfig": "gitignore.png",
    ".python_history": "py.png",
    ".julia_history": "jl.png",
    "README": "README.png",
    ".gdbinit": "gnu.png",
    ".Rhistory": "R.png",
    ".pypirc": "py.png", 
}
PrefixMap = {
    ".python_history": "py.png",
    ".conda": "anaconda3.png",
    ".bash": "bashrc.png",
    "rstudio-": "R.png",
    ".nvidia": "cu.png",
    "nvidia-": "cu.png",
    "zsh": "bashrc.png",
}
PLATFORM = platform.system()

def __icon__(name):
    __current_dir__ = os.path.dirname(os.path.realpath(__file__))
    __icons__ = os.path.join(__current_dir__, "../assets/icons")
    path = os.path.join(__icons__, name)

    return path

def sizeof_fmt(num, suffix="B"):
    '''convert bytes to human readable format'''
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    
    return f"{num:.1f}Y{suffix}"

class FigFile:
    def __init__(self, path):
        self.path = path
        self.pathlibObj = pathlib.Path(path)
        self.name = self.pathlibObj.name
        self.stem = self.pathlibObj.stem
        self.parent = self.pathlibObj.parent
        self.isdir = os.path.isdir(self.path)
        self.isfile = os.path.isfile(self.path)
        if magic:
            self.mimetype = magic.from_file(self.path)
        else:
            self.mimetype = "libmagic not installed"
        self.thumbnail = self.getThumbnail()
        self.getProperties()

    def getProperties(self):
        try:
            stat = os.stat(self.path)
        except (PermissionError, FileNotFoundError) as e: 
            self.props = argparse.Namespace()
            self.props.access_time = datetime.datetime.now().strftime("%b,%b %d %Y %H:%M:%S")
            self.props.modified_time = datetime.datetime.now().strftime("%b,%b %d %Y %H:%M:%S")
            self.props.size = "0B"
            return 
        self.props = argparse.Namespace()
        if PLATFORM == "Linux":
            self.props.access_time = datetime.datetime.fromtimestamp(stat.st_atime).strftime("%b,%b %d %Y %H:%M:%S")
            self.props.modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%b,%b %d %Y %H:%M:%S")
            self.props.size = sizeof_fmt(stat.st_size)
        elif PLATFORM == "Windows":
            pass
        elif PLATFORM == "Darwin":
            pass
        else:
            pass

    def __str__(self):
        properties = f'''
Name: {self.name}
Type: {self.mimetype}
Size: {self.props.size}

Location: {self.path}

Accessed: {self.props.access_time} 
Modified: {self.props.modified_time}
Thumbnail: {self.thumbnail}
'''
        return properties

    def getThumbnail(self):
        _,ext = os.path.splitext(self.name)
        # print(self.name, self.stem, ext, os.path.isfile(self.path))
        ext = ext[1:]
        if self.name == ".git":
            return "launcher/git.png"
        elif self.name == "pom.xml":
            return "launcher/pom.png"
        elif self.name.lower() == "todo":
            return "launcher/todo.png"
        elif not self.isfile:            
            # phrase contained case.
            for phrase in ThumbPhrases:
                if phrase in self.name.lower():
                    return f"launcher/{phrase}.png"
            if self.name in ThumbMap:
                filename = ThumbMap[self.name]
                return f"launcher/{filename}"
            # elif self.name == ".sbt":
            #     "launcher/scala.png"
            elif self.name.startswith(".git"):
                return "launcher/git.png"
            elif "julia" in self.name.lower():
                return "launcher/jl.png"
            elif "netbeans" in self.name.lower():
                return "launcher/netbeans.svg"
            elif "vscode" in self.name.lower():
                return "launcher/notvscode.png"
            elif self.stem == ".gconf":
                return "launcher/gnome.png"
            elif self.stem == ".fontconfig":
                return "launcher/ttf.svg"
            elif "anaconda" in self.name.lower() or self.name.startswith(".conda"):
                return "launcher/anaconda3.png"
            elif "jupyter" in self.name.lower() or "ipython" in self.name.lower() or "ipynb" in self.name.lower():
                return "launcher/ipynb.png"
            elif "tor" in re.split("_| |-", self.name.lower()) or self.name == ".tor":
                return "launcher/tor.png"
            elif self.name == ".linuxbrew" or self.name == "Homebrew":
                return "launcher/brew.png"
            elif self.name in [".gnupg"]:
                return "launcher/gnu.png"
            elif self.path in STDLinuxFolders:
                return f"dir/{self.name}.png"
            else:    
                return "launcher/fileviewer.png"
        elif ext in ["STL", "OBJ"]:
            return f"launcher/{ext.lower()}.png"
        elif ext in ["png","jpg","svg"]:
            return self.path
        elif self.name == ".profile":
            return "launcher/bashrc.png" 
        elif self.stem.lower() == "license":
            return "launcher/license.png"             
        # REMOVE #
        elif self.stem.startswith(".bash"):
            return "launcher/bashrc.png" 
        elif self.stem.startswith("zsh"):
            return "launcher/bashrc.png" 
        elif self.stem.startswith(".conda"):
            return "launcher/anaconda3.png"
        elif self.stem.startswith("nvidia-"):
            return "launcher/cu.png"
        elif self.name.startswith(".nvidia"):
            return "launcher/cu.png"
        # REMOVE #
        elif self.name.startswith(".") and "cookie" in self.name:
            return "launcher/cookie.png"
        elif self.stem in StemMap:
            filename = StemMap[self.stem]
            return f"launcher/{filename}"   
        elif self.stem.endswith("_history"):
            return "launcher/history.png"
        # txt/bin classification.
        elif ext == "":
            if self.mimetype.endswith("binary"):
                return "launcher/bin.png"    
            else:
                return "launcher/txt.png"
        for prefix in PrefixMap:
            if self.stem.startswith(prefix):
                filename = PrefixMap[prefix]
                return f"launcher/{filename}" 
        # check for .ext kind of files.
        if os.path.exists(__icon__(f"launcher/{ext}.png")): # check if png file for the ext
            return f"launcher/{ext}.png"
        else:
            if os.path.exists(__icon__(f"launcher/{ext}.svg")): 
                return f"launcher/{ext}.svg" 
                # check if svg file exists for the ext
            else: 
                # print(self.name)
                return f"launcher/txt.png" 
                # if ext is not recognized set it to txt

def listdir(path, reverse=False, filter_hidden=True, key=lambda x: x.lower()):
    path = os.path.expanduser(path)
    files, folders = [], []
    for file in os.listdir(path):
        abs_path = os.path.join(path, file)
        if file.startswith(".") and filter_hidden:
            continue
        if os.path.isfile(abs_path):
            files.append(file)
        else:
            folders.append(file)
    files = sorted(files, key=lambda x: x.lower(), reverse=reverse)
    folders = sorted(folders, key=lambda x: x.lower(), reverse=reverse)
    paths = []
    for file in folders:
        paths.append(os.path.join(path, file))
    for file in files:
        paths.append(os.path.join(path, file))

    return paths