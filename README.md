# FigUI: The pythonic file UI
The aim of FigUI is to provide a single package to view, edit, process and convert code, text, audio, document, image and video files of major popular formats.

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

## File formats to be supported:
1) Text: (txt, md, rst)
2) Code: (most coding langs)
3) Audio:
4) Document: (ppt/pdf/doc/font/spreadsheet)
5) Image: (stills/gifs)
6) Video: 