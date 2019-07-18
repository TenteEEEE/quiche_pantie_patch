from PIL import Image, ImageOps
from src.avatars.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_quiche_nbody.png'):
        super().__init__('Quiche-Nbody', body=body, pantie_position=[403, 836])

    def convert(self, image):
        cut = 7
        right_pantie = image.crop((cut, 0, image.size[0], image.size[1]))
        left_pantie = ImageOps.mirror(right_pantie)
        npantie = Image.new("RGBA", (right_pantie.size[0] * 2, right_pantie.size[1]))
        npantie.paste(right_pantie, (right_pantie.size[0], 0))
        npantie.paste(left_pantie, (0, 0))
        return npantie
