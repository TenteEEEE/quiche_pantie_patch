import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_caronauff.png', **options):
        super().__init__('カロナーフ', body=body, pantie_position=[1635, 1032], **options)
        self.mask = io.imread('./mask/mask_caronauff.png')
            
    def convert(self, image):
        pantie = np.array(image)

        # prepare for moving from hip to front
        patch = np.copy(pantie[-212:-5, 485:, :])
        patch = np.pad(patch, [(0, 0), (100, 100), (0, 0)], mode='constant')
        patch = skt.rotate(patch, 90)
            
        # Affine transform matrix for patch
        arry = np.zeros(100)
        arrx = np.sin(np.linspace(0, 1 * np.pi, 100) + np.pi / 8) * 60 + 25
        patch = affine_transform_by_arr(patch, arrx, arry)
        pantie[-250:, 485:, :] = 0

        # Affine transform matrix for whole image
        arrx = np.zeros(100)
        arrx[10:] += np.linspace(0, 1, 90)**2 * 195
        arrx[50:80] += np.sin(np.linspace(0, 1 * np.pi, 30)) * -20
        arry = np.zeros(100)
        arry[20:80] += np.sin(np.linspace(0, 1 * np.pi, 60) + np.pi / 2) * -70
        arrx -= 110
        pantie = affine_transform_by_arr(pantie, arrx, arry, smoothx=True, mvx=20, smoothy=True, mvy=20)
        pantie = pantie[10:,27:-30]
        
        # paste patch
        patch = skt.rotate(patch, 90)[:, 68:155]
        patch = skt.resize(patch[:, :, :], (150, 80), anti_aliasing=True, mode='reflect')
        pantie[240:240 + patch.shape[0], :patch.shape[1], :] = patch
        pantie = resize(pantie, [1.04, 0.77])
        pantie = np.rot90(pantie, -1)
        pantie = np.uint8(pantie*255)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[::-1],pantie),axis=0)
        return Image.fromarray(pantie)
