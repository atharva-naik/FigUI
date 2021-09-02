import os, platform, webbrowser, subprocess
import screen_brightness_control as sbc


class BrightnessController:
    def __init__(self):
        self.platform = platform.system()
        self.xdotool_installed = False
        if self.platform == "Linux":
            if subprocess.getoutput("xdotool") != "/bin/sh: 1: xdotool: not found": 
                self.xdotool_installed = True
        #     os.system('''zenity --error --text="For using brightness control on Linux, you will need to install one of these programs: 'xrandr, ddcutil, light or xbacklight'"''')
        #     webbrowser.open("https://pypi.org/project/screen-brightness-control/#description")
        # webbrowser.open("https://www.freebsd.org/cgi/man.cgi?query=xdotool&apropos=0&sektion=1&manpath=FreeBSD+8.1-RELEASE+and+Ports&format=html")
        
        self.all_brightness = sbc.get_brightness()
        if isinstance(self.all_brightness, int):
            self.all_brightness = [self.all_brightness]
        self.primary_brightness = sbc.get_brightness(display=0)

    def _xdotool_install_msg(self):
        os.system('''zenity --error --text="For using brightness control on Linux, you will need to install xdotool, using appropriate package managers."''')
        # webbrowser.open("https://pypi.org/project/screen-brightness-control/#description")
        webbrowser.open("https://www.freebsd.org/cgi/man.cgi?query=xdotool&apropos=0&sektion=1&manpath=FreeBSD+8.1-RELEASE+and+Ports&format=html")

    def inc_brightness(self):
        if self.platform == "Linux":
            if self.xdotool_installed == False:
                if subprocess.getoutput("xdotool") != "/bin/sh: 1: xdotool: not found": 
                    self.xdotool_installed = True
                else:
                    self._xdotool_install_msg()
                    subprocess.getoutput("xdotool key XF86MonBrightnessUp")
            else:
                subprocess.getoutput("xdotool key XF86MonBrightnessUp")

    def dec_brightness(self):
       if self.platform == "Linux":
            if self.xdotool_installed == False:
                if subprocess.getoutput("xdotool") != "/bin/sh: 1: xdotool: not found": 
                    self.xdotool_installed = True
                else:
                    self._xdotool_install_msg()
                    subprocess.getoutput("xdotool key XF86MonBrightnessDown")
            else:
                subprocess.getoutput("xdotool key XF86MonBrightnessDown")

    def __str__(self):
        return f"{len(self.all_brightness)} displays found. Primary display has brightness of {self.primary_brightness}%"

    def __repr__(self):
        return "FigUI.subSystem.system.brightness.BrightnessController"