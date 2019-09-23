import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *

class patcher(patcher):
    def __init__(self, body='./body/body_firina.png', **options):
        super().__init__('Firina', body=body, pantie_position=[31, 54], **options)
        self.mask = io.imread('./mask/mask_firina.png')
        try:
            self.is_frill = self.options['is_frill']
        except:
            self.is_frill = self.ask(question='Is there a frill on the hip?', default=False)

    def convert(self, image):
        pantie = np.array(image)

        # prepare for moving from hip to front
        if self.is_frill:
            patch = np.copy(pantie[-230:-5, 485:, :])
            patch = np.pad(patch, [(0, 0), (100, 100), (0, 0)], mode='constant')
            patch = skt.rotate(patch, 90)
        else:
            patch = np.copy(pantie[-212:-5, 485:, :])
            patch = np.pad(patch, [(0, 0), (100, 100), (0, 0)], mode='constant')
            patch = skt.rotate(patch, 90)
        # Affine transform matrix for patch
        [r, c, d] = patch.shape
        arry = np.zeros(100)
        arrx = np.sin(np.linspace(0, 1 * np.pi, 100) + np.pi / 8) * 60 + 25
        patch = affine_transform_by_arr(patch, arrx, arry)
        pantie[-250:, 485:, :] = 0

        # Affine transform matrix for whole image
        pantie = np.pad(pantie, [(50, 0), (50, 0), (0, 0)], mode='constant')
        arrx = (np.sin(np.linspace(0, 1 * np.pi, 100) - np.pi / 2) * 94)
        arrx[30:60] += (np.sin(np.linspace(0, 1 * np.pi, 100) - np.pi / 8) * 45)[30:60]
        arrx[:30] += (np.sin(np.linspace(0, 1 * np.pi, 100) + np.pi / 2) * 65)[:30]
        arrx[:20] += 14
        # arrx[22] -= 20
        arrx[21] -= 20
        arrx[23] += 100
        arrx[32] -= 80
        # arrx[20:22] -= 8
        arrx[30:45] += 7
        arrx -= 20
        arry = np.sin(np.linspace(0, 1 * np.pi, 100) + np.pi / 2) * 135
        arry[-50:] -= (np.sin(np.linspace(0, 1 * np.pi, 100) - np.pi / 3) * 150)[-50:]
        arry = abs(arry)
        arry[:20] += 15
        arry -= 100
        pantie = affine_transform_by_arr(pantie, arrx, arry, smoothx=True, mvx=30, smoothy=True, mvy=20)
        pantie = pantie[10:,25:-120]
        
        # paste patch
        if self.is_frill:
            patch = skt.rotate(patch, 90)[:, 59:160]
            patch = skt.resize(patch[:, :, :], (220, 86), anti_aliasing=True, mode='reflect')
        else:
            patch = skt.rotate(patch, 90)[:, 68:155]
            patch = skt.resize(patch[:, :, :], (220, 130), anti_aliasing=True, mode='reflect')
        pantie[215:215 + patch.shape[0], :patch.shape[1], :] = patch
        pantie = np.uint8(pantie*255)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = skt.resize(pantie, (np.int(pantie.shape[0] * 3.8), np.int(pantie.shape[1] * 3.8)), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie[:,7:]*255)
        pantie = np.concatenate((pantie[:,::-1],pantie),axis=1)
        return Image.fromarray(pantie)
