import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_anna_light.png', **options):
        super().__init__('Anna-Light', body=body, pantie_position=[0, 15], **options)

    def convert(self, image):
        pantie = np.array(image)

        # move from hip to front
        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 50), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[137:137 + pr, :pc, :] = np.uint8(patch * 255)
        pantie = pantie[:-165, :, :]

        # Finalize
        pantie = skt.resize(pantie, (np.int(pantie.shape[0] * 0.405), np.int(pantie.shape[1] * 0.405)), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie * 255)[:, 2:, :]
        return Image.fromarray(pantie)
