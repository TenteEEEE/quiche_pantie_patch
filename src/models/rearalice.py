import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_rearalice.png', **options):
        super().__init__('リアアリス', body=body, pantie_position=[2162, 2320], **options)
        self.mask = io.imread('./mask/mask_rearalice.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch[::-1, ::-1]

        front = pantie[:250, :330]
        arrx = (np.linspace(0, 1, 36)**0.5) * 45
        arrx[:10] += np.cos(np.linspace(0, np.pi / 2, 10))**2 * 12
        arrx -= 50
        arry = np.zeros(36)
        front = affine_transform_by_arr(front, arrx, arry)[:-50]
        front = np.uint8(resize(front, [1.55, 1.57]) * 255)

        back = pantie[:-15, 330:][:, ::-1]
        back = np.pad(back, [(0, 200), (0, 0), (0, 0)], mode='constant')
        arrx = (np.linspace(0, 1, 36)**1.5) * 270
        arrx -= np.sin(np.linspace(0, np.pi, 36) - np.pi / 6) * 14
        arrx -= 200
        arry = np.zeros(36)
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.rot90(back)[::-1]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 40
        arry += np.sin(np.linspace(0, np.pi, 25)) * 110
        arry -= 50
        back = np.rot90(affine_transform_by_arr(back, arrx, arry))[50:]
        back = np.uint8(resize(back, [1.55, 1.57]) * 255)

        front = front[:-40]
        back = back[60:]
        fr, fc, d = front.shape
        br, bc, d = back.shape
        pantie = np.zeros((fr + br, fc, d), dtype=np.uint8)
        pantie[:fr, :fc, :] = front
        pantie[fr:, :bc, :] = back
        pantie = pantie[:, 11:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)
