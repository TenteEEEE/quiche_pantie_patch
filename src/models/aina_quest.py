from PIL import Image, ImageOps
from src.models.aina import patcher

class patcher(patcher):
    def __init__(self, body='./body/body_aina_quest.png', **options):
        super().__init__(**options)
        self.name = "愛奈(クエスト)"
        self.body = Image.open(body)
        self.body_size = self.body.size
        self.pantie_position = [768, 269]
