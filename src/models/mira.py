import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_mira.png', **options):
        super().__init__('ミラ', body=body, pantie_position=[1268, 10], **options)
        self.mask = io.imread('./mask/mask_mira.png')

    def convert(self, image):
        pantie = np.array(image)
        arrx = np.zeros(25)
        arry = np.zeros(25)
        arry[:10] -= np.sin(np.linspace(0, 1, 10)) * 30
        pantie_ = affine_transform_by_arr(pantie, arrx, arry)

        patch = np.copy(pantie[-190:, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] + 25, patch.shape[1]), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie_[125:125 + pr, 3:3+pc, :] = patch
        io.imshow(pantie_[:340])
        pantie = pantie_[:340]
        pantie = np.uint8(resize(pantie, [0.9, 1.25]) * 255)
        io.imsave('test.png', pantie)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
