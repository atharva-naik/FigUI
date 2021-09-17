#!/home/atharva/anaconda3/envs/figui/bin/python
# -*- coding: utf-8 -*-
import os, sys
import FigUI.widgets.Window 


if __name__ == "__main__":
    os.system("notify-send 'launching FIG'")
    app = FigUI.widgets.Window.FigApp(argv=sys.argv)
    app.run()
