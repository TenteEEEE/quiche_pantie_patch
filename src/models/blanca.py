import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_blanca.png', **options):
        super().__init__('ブランカ', body=body, pantie_position=[2534, 1521], **options)
        self.mask = io.imread('./mask/mask_blanca.png')
        self.ribbon_mask = io.imread('./mask/ribbon_blanca.png') / 255.0
        self.ribbon_shade = io.imread('./material/ribbon_blanca.png')[:, :, -1] / 255.0

    def convert(self, image):
        pantie = np.array(image)

        # make ribbon
        front = pantie[20:100, 30:80, :3] / 255.0
        front_shade = pantie[130:150, 0:40, :3] / 255.0
        front_color = np.mean(np.mean(front, axis=0), axis=0)
        shade_color = np.mean(np.mean(front_shade, axis=0), axis=0)
        ribbon = self.ribbon_mask[:, :, :3] * front_color
        shade = self.ribbon_mask[:, :, :3] * shade_color
        ribbon = shade * self.ribbon_shade[:, :, None] + ribbon * (1 - self.ribbon_shade)[:, :, None]
        ribbon = np.uint8(ribbon * 255)

        # make pantie
        div = -110
        patch = np.copy(pantie[div:, 546:, :])
        pantie[div:, 546:, :] = 0
        [pr, pc, d] = patch.shape
        pantie[157:157 + pr, :pc, :] = patch
        pantie = pantie[:300]

        front = pantie[:, :300]
        arrx = np.linspace(0, 40, 100)
        arry = np.zeros(100)
        arrx -= 40
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(resize(front, [2, 2.78]) * 255)

        back = pantie[:, 300:][:, ::-1]
        arrx = np.linspace(0, 40, 100)
        arrx += np.sin(np.linspace(0, np.pi, 100))**2 * 12
        arrx -= 40
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(resize(back, [2, 2]) * 255)[::-1, :]

        [fr, fc, _] = front.shape
        [br, bc, _] = back.shape
        shx = 10
        shy = 44
        pantie = np.zeros((fr + br - shy, np.max([fc, bc]) + shx, 4), dtype=np.uint8)
        pantie[:fr, shx:shx + fc] = front
        pantie[-br - shy:-shy, :bc] = back
        pantie = np.bitwise_and(pantie, self.mask)
        pantie[119:119 + ribbon.shape[0], 441:441 + ribbon.shape[1], :3] = ribbon
        pantie[119:119 + ribbon.shape[0], 441:441 + ribbon.shape[1], 3] = 255
        return Image.fromarray(pantie)
