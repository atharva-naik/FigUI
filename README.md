# FigUI: The pythonic file UI

The aim of FigUI is to provide a single desktop application to view, edit, process and convert various file types - images, videos, audio files, 3D model files, binary files, log files, code files, pdf, excel, ppt files etc. You get the picture :P . This is just a passion project and don't expect this to be a replacement for gnome apps, VSCode or VLC :|

## File formats to be supported:

1) Text: (txt, md, rst, log)
2) Code: (most coding languages: think python, Javascript, C, C++, Java, Perl, Ruby, anything code mirror can highlight :P, JSON, JSONL, pickle files, github flavored markdown, html, css, scss, less etc.)
3) Audio: (mp3, wav, ogg etc.)
4) Document: ppt/ CSVs
5) Image: (still images formats such as png, jpg, svg (technically they are more like html files though :P), ico, bmp etc. as well as more dynamic formats such as gif)
6) Video: (mp4, mov, webm etc.)
7) Archives: (zip, 7zip etc)

<!-- ## Package Structure
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
```
.
├── basic.ics
├── datetime.pkl
├── example.feature
├── FigUI
│   ├── assets
│   │   ├── attributions.md
│   │   ├── fonts
│   │   │   ├── OMORI_GAME2.ttf
│   │   │   └── OMORI_GAME.ttf
│   │   ├── icons
│   │   │   ├── back.svg
│   │   │   ├── blockview.svg
│   │   │   ├── bookmark.svg
│   │   │   ├── bottombar
│   │   │   ├── browser
│   │   │   ├── case-sensitive.svg
│   │   │   ├── close.svg
│   │   │   ├── copy.svg
│   │   │   ├── cut.svg
│   │   │   ├── decrypt.svg
│   │   │   ├── delete.svg
│   │   │   ├── email.svg
│   │   │   ├── encrypt.svg
│   │   │   ├── file_share.svg
│   │   │   ├── forward.svg
│   │   │   ├── hide.svg
│   │   │   ├── launcher
│   │   │   ├── launcher.png
│   │   │   ├── listview.svg
│   │   │   ├── logo.png
│   │   │   ├── maximize.svg
│   │   │   ├── minimize.svg
│   │   │   ├── new_file.svg
│   │   │   ├── new_folder.svg
│   │   │   ├── open_in_terminal.svg
│   │   │   ├── open.svg
│   │   │   ├── paste.svg
│   │   │   ├── permissions.svg
│   │   │   ├── pizza.gif
│   │   │   ├── properties.svg
│   │   │   ├── redo.svg
│   │   │   ├── regex_search.svg
│   │   │   ├── rename.svg
│   │   │   ├── search.svg
│   │   │   ├── sidebar
│   │   │   ├── sort_ascending.svg
│   │   │   ├── sort_descending.svg
│   │   │   ├── stepback.svg
│   │   │   ├── sysbar
│   │   │   ├── undo.svg
│   │   │   ├── unhide.svg
│   │   │   ├── user_permissions.svg
│   │   │   ├── whole-word.svg
│   │   │   └── zip.svg
│   │   └── icons_license.pdf
│   ├── conf
│   │   └── theme.json
│   ├── handler
│   │   ├── Archives
│   │   │   ├── pkl.py
│   │   │   ├── pt.py
│   │   │   ├── __pycache__
│   │   │   └── zip.py
│   │   ├── Audio
│   │   │   ├── aiff
│   │   │   ├── mp3
│   │   │   ├── ogg
│   │   │   └── wav
│   │   ├── Code
│   │   │   ├── bashrc.py
│   │   │   ├── c
│   │   │   ├── cpp
│   │   │   ├── css
│   │   │   ├── html
│   │   │   ├── __init__.py
│   │   │   ├── java
│   │   │   ├── js
│   │   │   ├── LICENSE
│   │   │   ├── py
│   │   │   ├── __pycache__
│   │   │   ├── QtColorPicker
│   │   │   ├── scala
│   │   │   └── static
│   │   ├── Document
│   │   │   ├── csv
│   │   │   ├── doc
│   │   │   ├── pdf
│   │   │   ├── ppt
│   │   │   └── xls
│   │   ├── Image
│   │   │   ├── bmp
│   │   │   ├── convert.py
│   │   │   ├── gif
│   │   │   ├── ico
│   │   │   ├── __init__.py
│   │   │   ├── jpg
│   │   │   ├── png
│   │   │   ├── __pycache__
│   │   │   ├── static
│   │   │   ├── svg
│   │   │   └── tiff
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── __init__.cpython-37.pyc
│   │   ├── Text
│   │   │   ├── log
│   │   │   ├── md
│   │   │   ├── rst
│   │   │   └── txt
│   │   └── Video
│   │       ├── __init__.py
│   │       ├── mov
│   │       ├── mp4
│   │       ├── __pycache__
│   │       ├── static
│   │       └── webm
│   ├── __pycache__
│   │   └── utils.cpython-37.pyc
│   ├── subSystem
│   │   ├── Calendar
│   │   │   ├── __init__.py
│   │   │   └── static
│   │   ├── Chat
│   │   ├── Email
│   │   ├── News
│   │   ├── PassMan
│   │   ├── __pycache__
│   │   │   └── Shell.cpython-37.pyc
│   │   ├── Scrape
│   │   ├── Shell.py
│   │   ├── system
│   │   │   ├── brightness.py
│   │   │   └── __pycache__
│   │   └── Weather
│   ├── utils.py
│   └── widgets
│       ├── DELETE.py
│       ├── FileViewer.py
│       ├── Launcher.py
│       ├── __pycache__
│       │   ├── FileViewer.cpython-37.pyc
│       │   ├── Launcher.cpython-37.pyc
│       │   ├── Tab.cpython-37.pyc
│       │   ├── Tabs.cpython-37.pyc
│       │   ├── Theme.cpython-37.pyc
│       │   └── Window.cpython-37.pyc
│       ├── Tab.py
│       ├── Theme.py
│       ├── Toolbar.py
│       └── Window.py
├── FigUI.desktop
├── figui_wallpaper_1631225129.6073387.jpg
├── gay.sass
├── hello.ts
├── LICENSE
├── logo.png
├── logs
│   └── 10_Sep_2021_04_41_53.log
├── main.py
├── pickle.pkl
├── pom.xml
├── README.md
├── requirements.txt
└── TODO

74 directories, 90 files
``` -->