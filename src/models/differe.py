import skimage.io as io
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher


class patcher(patcher):
    def __init__(self, body='./body/body_differe.png', **options):
        super().__init__('Differe', body=body, pantie_position=[1337, 14], **options)
        self.mask = io.imread('./mask/mask_differe.png')

    def convert(self, image):
        pantie = np.array(image)
        pantie = np.bitwise_and(pantie, self.mask)
        image = Image.fromarray(pantie).resize((683, 660))
        return image
