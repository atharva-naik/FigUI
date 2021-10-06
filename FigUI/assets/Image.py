# blurring images.
import tempfile
from pathlib import Path
from typing import Union, List 
from PyQt5.QtGui import QIcon, QPixmap
from PIL import Image, ImageFilter, ImageQt


class ImageAsset:
    def __init__(self, path: Union[str, Path, None]):
        self.path = path
        if path:
            self._image = Image.open(self.path)

    def gaussBlur(self, radius: int=5) -> Image:
        '''apply gaussian blur on the image.'''
        gaussFilter = ImageFilter.GaussianBlur(radius)

        return self._image.filter(gaussFilter)  

    @classmethod
    def fromPIL(cls, image: Image):
        '''create asset from PIL Image object.'''
        obj = cls(None)
        obj._image = image

        return obj

    def show(self):
        '''show image.'''
        self._image.show()

    def save(self, path: Union[str, Path]):
        '''save image at a given path.'''
        self._image.save(path)

    def backgroundURL(self, path='tmp'):
        '''save the image at a given path and return that path.'''
        tmp = tempfile.NamedTemporaryFile(suffix=".png")
        self._image.save(tmp.name)

        return tmp.name

    def QIcon(self):
        '''convert to QIcon.'''
        img_qt = ImageQt.ImageQt(self._image)
        pixmap = QPixmap.fromImage(img_qt)
        q_icon = QIcon(pixmap)

        return q_icon


if __name__ == "__main__":
    figImg = ImageAsset("/home/atharva/Pictures/Wallpapers/anime/shop.png")
    figImg.gaussBlur(5).show()
    # print(ImageAsset.fromPIL(figImg.gaussBlur(5)).QIcon())
    print(ImageAsset.fromPIL(figImg.gaussBlur(5)).backgroundURL())