import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_necomaid.png', **options):
        super().__init__('NecoMaid', body=body, pantie_position=[104, 2482], **options)
        self.mask = io.imread('./mask/mask_necomaid.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-150:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] - 50, 60), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = np.uint8(patch * 255)

        arrx = np.zeros(100)
        arry = np.zeros(100)
        arry[10:] += np.sin(np.linspace(0, np.pi, 90)) * 300
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie = np.uint8(resize(pantie[:130, :330], [3.21, 3.21]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)[4:]
        return Image.fromarray(pantie)
