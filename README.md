# FigUI: The pythonic file UI
The aim of FigUI is to provide a single package to view, edit, process and convert code, text, audio, document, image and video files of major popular formats.

## File formats to be supported:
1) Text: (txt, md, rst)
2) Code: (most coding langs)
3) Audio:
4) Document: (ppt/pdf/doc/font/spreadsheet)
5) Image: (stills/gifs)
6) Video: 

## Package Structure
handler -> Modality -> ext -> [formatter, highlighter, linter, parser, processor, AI, editor, widgets] 
subSystem -> storage // storage management APIs (for files and databases)
subSystem -> system -> [camera, gpu, cpu, battery, display, time, logging]
utils 
subSystem -> Auth
subSystem -> Email
subSystem -> [Chat, VidCall]
subSystem -> Browser
subsystem -> PassMan
subsystem -> WinMan
subSystem -> Scrape
subSystem -> API
FigUI

├── assets
│   ├── icons
│   │   ├── fix.png
│   │   ├── idea.png
│   │   ├── launcher
│   │   │   ├── bash.png
│   │   │   ├── bmp.png
│   │   │   ├── browser.png
│   │   │   ├── css.png
│   │   │   ├── html.png
│   │   │   ├── jpg.png
│   │   │   ├── json.png
│   │   │   ├── pdf.png
│   │   │   ├── png.png
│   │   │   ├── svg.png
│   │   │   └── vscode.png
│   │   ├── launcher.png
│   │   └── tips.png
│   └── icons_license.pdf
├── conf
│   └── theme.json
├── handler
│   ├── Audio
│   │   ├── aiff
│   │   ├── mp3
│   │   ├── ogg
│   │   └── wav
│   ├── Code
│   │   ├── c
│   │   ├── cpp
│   │   ├── css
│   │   ├── html
│   │   ├── java
│   │   ├── js
│   │   ├── py
│   │   └── scala
│   ├── Document
│   │   ├── csv
│   │   ├── doc
│   │   ├── pdf
│   │   ├── ppt
│   │   └── xls
│   ├── Image
│   │   ├── bmp
│   │   ├── convert.py
│   │   ├── gif
│   │   ├── ico
│   │   ├── __init__.py
│   │   ├── jpg
│   │   ├── png
│   │   ├── svg
│   │   ├── tiff
│   │   └── ui.py
│   ├── Text
│   │   ├── log
│   │   ├── md
│   │   ├── rst
│   │   └── txt
│   └── Video
│       ├── mov
│       ├── mp4
│       └── webm
├── subSystem
│   ├── API
│   ├── Auth
│   ├── Browser
│   ├── Chat
│   ├── Email
│   ├── News
│   ├── PassMan
│   ├── __pycache__
│   │   └── Shell.cpython-37.pyc
│   ├── Scrape
│   ├── Shell.py
│   ├── Storage
│   ├── system
│   ├── Weather
│   └── WinMan
├── utils.py
└── widgets
    ├── Launcher.py
    ├── Minimap.py
    ├── __pycache__
    │   ├── Launcher.cpython-37.pyc
    │   ├── Tab.cpython-37.pyc
    │   ├── Tabs.cpython-37.pyc
    │   ├── Theme.cpython-37.pyc
    │   └── Window.cpython-37.pyc
    ├── Tab.py
    ├── Theme.py
    ├── Toolbar.py
    └── Window.py

58 directories, 34 files