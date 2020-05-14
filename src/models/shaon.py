import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_shaon.png', **options):
        super().__init__('シャオン', body=body, pantie_position=[1312, 1435], **options)
        self.mask = io.imread('./mask/mask_shaon.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-60:-5, 546:, :])
        pantie[-60:, 546:, :] = 0
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = patch[::-1, ::-1]
        arrx = np.linspace(0, 1, 100)**2 * 100
        arry = np.sin(np.linspace(0, np.pi, 100) + np.pi / 4) * -100
        pantie = affine_transform_by_arr(pantie, arrx - 110, arry)[30:-60, 95:-30]
        pantie = np.uint8(resize(pantie, [2.5, 2.5]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
