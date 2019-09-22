import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_noy.png', **options):
        super().__init__('Noy', body=body, pantie_position=[147, 133], **options)
        self.mask = io.imread('./mask/mask_noy.png')

    def convert(self, image):
        pantie = np.array(image)

        # prepare for moving from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (240, 60), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape

        # Affine transform matrix
        pantie = np.pad(pantie, [(0, 0), (100, 0), (0, 0)], mode='constant')
        arrx = np.zeros(100)
        arry = np.zeros(100)
        arry[:30] += np.linspace(70,0,30)
        arry[30:] += np.linspace(0,200,70)
        arry[65:] -= np.linspace(0,170,35)
        pantie = affine_transform_by_arr(pantie, arrx, arry)[:,53:-65]
        pantie[147:147 + pr, :pc, :] = patch
        pantie = np.bitwise_and(np.uint8(pantie*255), self.mask)
        pantie = skt.resize(pantie, (int(pantie.shape[0]*3.65), int(pantie.shape[1]*3.13)), anti_aliasing=True, mode='reflect')[:,8:]
        pantie = np.concatenate((pantie[:,::-1],pantie),axis=1)

        return Image.fromarray(np.uint8(pantie*255))
