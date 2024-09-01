from .base import BaseWidget
import base64

class ImageWidget(BaseWidget):
    def __init__(
        self,
        name: str,
        title: str,
        author: str,
        *,
        width: int = 1,
        height: int = 1,
        background: str = "#e3e3e3",
        order: int = 10,
    ):
        super().__init__(name, title, author, width, height, background, order)
        self.type = "image"
        self.content = ImageContent()

    def set_image(self, data: bytes, fit: str = "cover"):
        """contain, cover, fill"""
        self.content.data = base64.b64encode(data).decode()
        self.content.fit = fit


class ImageContent(object):
    def __init__(self):
        self.data = ""
        self.fit = "cover"
