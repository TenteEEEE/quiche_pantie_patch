import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_hati.png', **options):
        super().__init__('ハティ', body=body, pantie_position=[1591, 2080], **options)
        self.mask = io.imread('./mask/mask_hati.png')

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:115, :230][::-1]
        back = pantie[:, -230:][:, ::-1]
        pantie = np.concatenate((back, front), axis=0)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
