import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_ququkimono.png', **options):
        super().__init__('着物(QuQu)', body=body, pantie_position=[1001, 20], **options)

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-100:-5, 546:, :])
        pantie[-50:, 546:, :] = 0
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = patch[::-1, ::-1]
        pantie = np.uint8(resize(pantie, [0.4, 0.392]) * 255)
        pantie = np.rot90(pantie, 1)
        return Image.fromarray(pantie)
