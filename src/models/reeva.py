from PIL import Image
from src.models.leeme import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_reeva.png', **options):
        super().__init__(**options)
        self.name = 'リーバ(下着)'
        self.body = Image.open(body)
        self.body_size = self.body.size
