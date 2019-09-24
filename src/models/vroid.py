import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_vroid.png', **options):
        super().__init__('VRoid', body=body, pantie_position=[482, 944], **options)
        self.mask = io.imread('./mask/mask_vroid.png')

    def convert(self, image):
        pantie = np.array(image)

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (180, 40), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[157:157 + pr, :pc, :] = np.uint8(patch * 255)

        # Affine transform matrix
        pantie = np.pad(pantie, [(100, 0), (10, 0), (0, 0)], mode='constant')
        arrx = np.zeros(100)
        arrx[10:50] = (np.sin(np.linspace(0, 1 * np.pi, 100))[20:60] * 30)
        arrx[50:] = -(np.sin(np.linspace(0, 1 * np.pi, 100))[50:] * 15)
        arrx[40:60] += (np.sin(np.linspace(0, 1 * np.pi, 100))[40:60] * 15)
        arrx[00:10] -= (np.sin(np.linspace(0, 1 * np.pi, 100))[50:60] * 35)
        arry = (np.sin(np.linspace(0, 0.5 * np.pi, 100)) * 70)
        arry[10:30] -= (np.sin(np.linspace(0, 1 * np.pi, 100)) * 20)[50:70]
        pantie = affine_transform_by_arr(pantie, arrx, arry, smoothx=True, mvx=30)
        pantie = np.uint8(pantie * 255)[60:430, 16:-80]
        pantie = np.bitwise_and(pantie, self.mask)

        # mirroring and finalize
        [r, c, d] = pantie.shape
        npantie = np.zeros((r, c * 2, d), dtype=np.uint8)
        npantie[:, c:, ] = pantie
        npantie[:, :c, ] = pantie[:, ::-1]
        return Image.fromarray(npantie)
