import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_ukon.png', **options):
        super().__init__('右近', body=body, pantie_position=[616, 686], **options)
        self.mask = io.imread('./mask/mask_ukon.png')

    def convert(self, image):
        pantie = np.array(image)
        pantie = np.bitwise_and(pantie, self.mask)

        front = pantie[:159, :185, :]
        front = resize(front, [0.592, 0.72])[:, :, :]
        back = pantie[:355, 410:, :]
        back = skt.rotate(back, 180)
        back = resize(back, [0.47, 0.59])

        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        pantie = np.zeros((fr + br, np.max([fc, bc]), 4))
        pantie[:fr, :fc, :] = front
        pantie[fr:, :bc, :] = back

        # Finalize
        pantie = np.uint8(pantie * 255)
        return Image.fromarray(pantie)
