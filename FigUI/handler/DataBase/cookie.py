import os
import typing
import pathlib


class Cookie:
    def __init__(self, app: str):
        self.home = pathlib.Path.home().__str__()
        self.path = os.path.join(self.home, f'.config/{app}/Default/Cookies')

    @classmethod
    def fromPath(self, path: typing.Union[pathlib.Path, str]):
        if isinstance(path, pathlib.Path):
            path = str(path)
        self = Cookie("")
        self.path = path # os.path.join(self.home, path)

        return self

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"FigUI.handler.DataBase.cookie.Cookie.fromPath(path='{self.path}')"
# LINUX_CHROMIUM_COOKIES = os.path.join(HOME_DIR, '.config/chromium/Default/Cookies')
LINUX_CHROMIUM_COOKIES = Cookie("chromium")
LINUX_GOOGLE_CHROME_COOKIES = Cookie("google-chrome")
# LINUX_GOOGLE_CHROME_COOKIES = os.path.join(HOME_DIR, '.config/google-chrome/Default/Cookies')
if __name__ == '__main__':
    # import pprint
    # cookies = [LINUX_CHROMIUM_COOKIES, LINUX_GOOGLE_CHROME_COOKIES]
    print(LINUX_CHROMIUM_COOKIES)
    # pprint.pprint(cookies)
    # exec(f"DaCookie = {repr(cookies)}")
    # print("DaCookie:", DaCookie)
    print(repr(LINUX_CHROMIUM_COOKIES))