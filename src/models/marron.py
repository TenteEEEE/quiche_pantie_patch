import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_marron.png', **options):
        super().__init__('マロン', body=body, pantie_position=[3160, 257], **options)
        self.mask = io.imread('./mask/mask_marron.png')

    def convert(self, image):
        pantie = np.array(image)
        
        front = pantie[:250, :330]
        arrx = (np.linspace(0, 1, 36)**3) * 117
        arrx[16:30] += np.sin(np.linspace(0, np.pi, 14)) * 7
        arrx -= 80
        arry = np.linspace(0, 1, 36)**2 * 40
        arry[:8] += np.sin(np.linspace(0, np.pi, 8)) * 20
        arry -= 15
        front = affine_transform_by_arr(front, arrx, arry)

        back = pantie[:-7, 330:][:, ::-1]
        back = np.pad(back, [(0, 100), (0, 0), (0, 0)], mode='constant')
        arrx = (np.linspace(0, 1, 36)**2) * 115
        arrx -= np.sin(np.linspace(0, np.pi, 36) + np.pi / 2.5) * 2
        arrx[:3] += 8
        arrx -= 100
        arry = np.linspace(0, 1, 36)**2 * 40
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.rot90(back)[::-1, ]
        arrx = np.zeros(25)
        arry = np.linspace(0, 1, 25)**2 * 120
        arry += np.sin(np.linspace(0, np.pi, 25)) * 50
        back = np.rot90(affine_transform_by_arr(back, arrx, arry))[90:]

        fr, fc, d = front.shape
        br, bc, d = back.shape
        shy = 56
        pantie = np.zeros((fr + br - shy, fc, d), dtype=np.float32)
        pantie[:fr, :fc, :] = front
        pantie[fr - shy:fr - shy + 80, :bc, :] = alpha_brend(pantie[fr - shy:fr - shy + 80, :bc, :], back[:80], back[:80, :, -1] < 0.99)
        pantie[fr - shy + 80:fr - shy + br, :bc, :] = alpha_brend(pantie[fr - shy + 80:fr - shy + br, :bc, :], back[80:], back[80:, :, -1] < 0)
        pantie = np.uint8(resize(pantie, [2.92, 2.92]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
