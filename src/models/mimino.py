import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_mimino.png', **options):
        super().__init__('みみの', body=body, pantie_position=[3, 772], **options)

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-100:-5, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] + 90, patch.shape[1]), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[114:114 + pr, :pc, :] = np.uint8(patch * 255)
        pantie = np.uint8(resize(pantie, [0.82, 0.82]) * 255)
        pantie = pantie[:-70, 5:]
        pantie = np.concatenate([pantie[:, ::-1], pantie], axis=1)
        return Image.fromarray(pantie)
