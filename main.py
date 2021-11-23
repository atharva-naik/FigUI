#!/home/atharva/anaconda3/envs/figui/bin/python
# -*- coding: utf-8 -*-
import sys
import FigUI.utils
import FigUI.widgets.Window 


if __name__ == "__main__":
    FigUI.utils.notify() # works only for Linux.
    app = FigUI.widgets.Window.FigApp(argv=sys.argv,
                                      # x=200, y=200, w=1920, h=1080, 
                                      background='/home/atharva/GUI/background.jpg')
    app.window.smartPhoneTaskBar.rePos()
    app.run()
