import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_liqu.png', **options):
        super().__init__('リク', body=body, pantie_position=[620, 769], **options)
        self.mask = io.imread('./mask/mask_liqu.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-100:-5, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0] + 30, patch.shape[1]), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[114:114 + pr, :pc, :] = np.uint8(patch * 255)

        front = pantie[:, :300]
        arrx = np.zeros(25)
        arry = np.zeros(25)
        arry[5:10] = np.sin(np.linspace(0, np.pi, 5)) * -40
        arry[8:] += np.linspace(0, 1, 17)**2 * 500
        front = affine_transform_by_arr(front, arrx, arry)[:, :-70]
        front = np.uint8(resize(front, [1.1, 1]) * 255)

        back = pantie[:, 300:]
        arrx = np.zeros(25)
        arry = np.linspace(1, 0, 25)**2 * -280
        back = affine_transform_by_arr(back, arrx, arry)[:, 110:]
        back = np.uint8(resize(back, [1.1, 1]) * 255)

        [fr, fc, d] = front.shape
        [br, bc, d] = back.shape
        shift_x = 36
        pantie = np.zeros((fr, fc + bc - shift_x, d), dtype=np.uint8)
        pantie[:, :fc] = front
        pantie[:, fc - shift_x:fc - shift_x + bc] = alpha_brend(back, pantie[:, fc - shift_x:fc - shift_x + bc], back[:, :, -1] > 254)
        pantie = pantie[:270, 8:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:-16, ::-1], pantie[:-16]), axis=1)
        return Image.fromarray(pantie)
