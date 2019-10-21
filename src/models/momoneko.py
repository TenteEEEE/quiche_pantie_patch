from PIL import Image
from src.models.cc0 import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_momoneko.png', **options):
        super().__init__(**options)
        self.name = "ももねこ"
        self.body = Image.open(body)
        self.body_size = self.body.size
