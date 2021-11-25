#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# global variables
ICONS_ROOTS = ["/usr/share/icons", "/usr/share/pixmaps", "~/.local/share/icons", "~/.local/share/pixmaps"]
APPS_ROOTS = ["/usr/share/applications", "~/.local/share/applications"]

import os
# import xdg
import pathlib
import subprocess
from typing import Union
for i in range(len(ICONS_ROOTS)):
    ICONS_ROOTS[i] = os.path.expanduser(ICONS_ROOTS[i])
for i in range(len(APPS_ROOTS)):
    APPS_ROOTS[i] = os.path.expanduser(APPS_ROOTS[i])
CACHED_ICON_PATHS = []

def _locate_icon(query, root, verbose=False):
    '''recursively locate icon!'''
    hits = []
    global CACHED_ICON_PATHS
    # check edge case when root doesn't exist!
    if not os.path.exists(root): 
        return []
    for entry in os.scandir(root):
        if entry.is_file():
            CACHED_ICON_PATHS.append(entry.path)
            if verbose:
                try: print(entry.name)
                except UnicodeEncodeError: 
                    print("\x1b[31;1municode encode error\x1b[0m")
            if query == entry.name: 
                hits.append(entry.path)
        else:
            hits += _locate_icon(query, root=entry.path, verbose=verbose)
    
    return hits

def _locate_icon_loop(query, roots, verbose=False):
    hits = []
    for root in roots:
        hits += _locate_icon(query, root=root, verbose=verbose)

    return hits

def locate_icon(query, roots=ICONS_ROOTS, refresh=False, verbose=False):
    '''check CACHE first, if not found then recursively locate!'''
    hits = []
    global CACHED_ICON_PATHS 
    if refresh == False:
        for path in CACHED_ICON_PATHS:
            if path.endswith(query):
                # verify if icon still exists at the cached up path.
                if os.path.exists(path):
                    if verbose: print(f"found in cache: {path}")
                    hits.append(path)
        if len(hits) == 0:
            if verbose: print("failed to locate entries in cache!")
            CACHED_ICON_PATHS = []
            return _locate_icon_loop(query, roots=roots, verbose=verbose)
        else: 
            return hits
    else:
        CACHED_ICON_PATHS = []
        print("ignoring cache, conducting full search!")
        return _locate_icon_loop(query, roots=roots, verbose=verbose)

def parse_desktop(path):
    # import argparse
    # ns = argparse.Namespace()
    ns = {}
    with open(path) as f:
        for line in f:
            line = line.strip("\n").strip()
            try:
                name = line.split("=")[0].strip()
                value = line.split("=")[1].strip()
                if name not in ns:
                    ns[name] = value
            except IndexError: pass
    
    return ns


class Application:
    def __init__(self, path: Union[str, pathlib.Path]):
        # private shit
        self.path = os.path.expanduser(str(path))
        self.attr_dict = parse_desktop(path)
        if os.path.exists(self["Icon"]):
            self.icon_paths = [self["Icon"]]
        else:
            self.icon_paths = locate_icon(self["Icon"])
        self.installed = True
        # if self["Exec"] != "NOT_FOUND":
        #     self.installed = os.path.exists(self["Exec"])
        # else:  # assume that app is installed even when Exec is not present.
        #     self.installed = True
    def __getitem__(self, key: str):
        return self.attr_dict.get(key, "NOT_FOUND")

    def __repr__(self):
        return self.Name

    @property
    def Name(self):
        return self["Name"]

    @property
    def Path(self):
        return self.path

    @Path.setter
    def Path(self, v):
        pass

    @property
    def Type(self):
        return self["Type"]

    @Type.setter
    def Type(self, v):
        pass

    @property
    def Icons(self):
        '''
        List of all icon paths.
        uneditable accesser for icon paths.
        '''
        return self.icon_paths

    @Icons.setter
    def Icons(self, v):
        pass

    @property
    def Icon(self):
        '''
        Most high resolution icon's path
        uneditable accesser for icon path
        '''
        try:
            return self.icon_paths[0]
        except IndexError: return None

    @Icon.setter
    def Icon(self, v):
        pass

    def Exec(self):
        name = pathlib.Path(self.Path).name
        subprocess.call(["gtk-launch", name], shell=False)
        
    def __str__(self):
        '''print application!'''
        op = ''
        for k,v in self.attr_dict.items():
            op += f'{k}: {v}\n'
        
        return op

    def OpenIcon(self):
        subprocess.call(["xdg-open", self.Icon])


class XdgOpen:
    def __init__(self):
        pass
# def Ls(roots=APPS_ROOTS, is_installed=True):
#     apps = []
#     for root in roots:
#         for entry in os.scandir(root):
#             if entry.is_file() and entry.name.endswith(".desktop"):
#                 try: 
#                     app = Application(entry.path)
#                     if app.Type != "Application": continue
#                 except UnicodeDecodeError: continue
#                 if is_installed:
#                     if app.installed == True:
#                         apps.append(app)
#                 else:
#                     apps.append(app)

#     return apps
def Ls(roots=APPS_ROOTS, is_installed=True):
    apps = []
    for root in roots:
        for entry in os.scandir(root):
            if entry.is_file() and entry.name.endswith(".desktop"):
                try: 
                    app = Application(entry.path)
                    if app.Type != "Application": continue
                except UnicodeDecodeError: continue
                if is_installed:
                    if app.installed == True:
                        yield app
                else:
                    yield app

    return apps


if  __name__ == "__main__":
    pass