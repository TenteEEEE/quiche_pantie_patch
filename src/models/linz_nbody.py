from PIL import Image, ImageOps
from src.models.quiche_nbody import patcher

class patcher(patcher):
    def __init__(self, body='./body/body_linz_nbody.png', **options):
        super().__init__(**options)
        self.name = "リンツ(素体)"
        self.body = Image.open(body)
