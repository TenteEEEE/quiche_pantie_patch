import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_lunauff.png', **options):
        super().__init__('転生ルナーフ', body=body, pantie_position=[-18, 59], **options)
        self.mask = io.imread('./mask/mask_lunauff.png')

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:200, :300]
        back = pantie[:-8, 300:][::-1, ::-1]
        back = np.pad(back, [(70, 0), (0, 0), (0, 0)], mode='constant')

        arrx = np.zeros(25)
        arrx -= np.cos(np.linspace(0, np.pi, 25)) * 20 + 20
        arry = np.linspace(0, 1, 25) * 40
        front = affine_transform_by_arr(front, arrx, arry)

        arrx = np.linspace(0, 1, 49)**2 * -68 + 70
        arrx[15:20] -= 5
        arrx[25:34] -= 8
        arrx[34:] -= 2
        arry = np.linspace(0, 1, 49) * 120
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.rot90(back, 3)

        arrx = np.zeros(25)
        arry = np.zeros(25)
        arry[7:] += np.linspace(0, 1, 18)**2 * 3000
        arry[9:] -= np.linspace(0, 1, 16)**2 * 3000
        back = affine_transform_by_arr(back, arrx, arry)[:250, 14:-160]
        back = np.rot90(back, 1)

        back = np.pad(back, [(0, 0), (0, front.shape[1] - back.shape[1]), (0, 0)], mode='constant')
        pantie = resize(np.concatenate([front[:-60], back], axis=0), [1.58, 1.16])
        pantie = np.uint8(pantie * 255)[:, 5:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)
