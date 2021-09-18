#!/home/atharva/anaconda3/envs/figui/bin/python
# -*- coding: utf-8 -*-
import sys
import FigUI.utils
import FigUI.widgets.Window 


if __name__ == "__main__":
    FigUI.utils.notify() # works only for Linux.
    app = FigUI.widgets.Window.FigApp(argv=sys.argv)
    app.run()
