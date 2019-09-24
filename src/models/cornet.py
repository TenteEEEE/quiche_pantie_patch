from PIL import Image, ImageOps
from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_cornet.png', **options):
        super().__init__(name='コルネット', body=body, pantie_position=[2035, 1656], **options)
    
    def convert(self, image):
        image = image.resize((image.width*2, image.height*2), Image.LANCZOS)
        return image
