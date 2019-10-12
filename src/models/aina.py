import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_aina.png', **options):
        super().__init__('愛奈', body=body, pantie_position=[0, 269], **options)
        self.mask = io.imread('./mask/mask_aina.png')

    def convert(self, image):
        pantie = np.array(image)
        pantie = np.bitwise_and(pantie, self.mask)

        front = pantie[:158, 1:200]
        back = pantie[:200, 460:]
        front = np.uint8(resize(front, [0.55, 0.57]) * 255)
        back = np.uint8(resize(back, [0.55, 0.57]) * 255)
        back = np.rot90(back, -1)

        out = np.zeros((115, 115, 4),  dtype=np.uint8)
        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        out[:fr, :fc] = front
        out[-br:, -bc:] = out[-br:, -bc:] * (back[:, :, -1] <= 20)[:, :, None] + back * (back[:, :, -1] > 20)[:, :, None]
        return Image.fromarray(out)
