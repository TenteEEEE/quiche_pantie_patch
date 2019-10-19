import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_chronos.png', **options):
        super().__init__('クロノス', body=body, pantie_position=[0, 2], **options)
        self.mask = io.imread('./mask/mask_chronos.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-100:-5, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] + 30, patch.shape[1]), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)

        front = pantie[:350, :300]
        arrx = (np.linspace(0, 1, 25)**2) * 43
        arrx[5:20] += np.sin(np.linspace(0, np.pi, 15)) * 4
        arrx[5:10] += np.sin(np.linspace(0, np.pi, 5)) * 13
        arry = np.zeros(25)
        arrx -= 30
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(front[::-1, 7:][88:] * 255)

        back = pantie[:350, 300:-10][:, ::-1]
        arrx = (np.linspace(0, 1, 25)**2) * 115
        arrx[2:14] += np.sin(np.linspace(0, np.pi, 12)) * 7
        arry = np.zeros(25)
        arrx -= 70
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(back[3:, 10:10 + front.shape[1]] * 255)

        pantie = np.concatenate((back, front), axis=0)
        pantie = np.uint8(resize(pantie, [1.55, 1.745]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)
