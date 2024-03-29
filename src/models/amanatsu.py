import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_amanatsu.png', **options):
        super().__init__(name='あまなつ', body=body, pantie_position=[402, 835], **options)
        self.mask = io.imread('./mask/mask_amanatsu.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-110:-5, 546:, :])
        pantie[-110:, 546:, :] = 0
        [pr, pc, d] = patch.shape
        pantie[105:105 + pr, :pc, :] = patch[::-1, ::-1]

        arrx = np.zeros(100) - 40
        arrx += np.cos(np.linspace(0, np.pi, 100)) * -30
        arry = np.linspace(0, 1, 100)**2 * 10
        pantie = affine_transform_by_arr(pantie, arrx, arry)[:, 7:]
        pantie = perspective_transform(pantie, np.matrix('1, 0.01, 0; 0, 1, 0; -0.0008,0,1'))
        pantie = np.uint8(resize(pantie[:300, :415], [1.5, 1.5]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate([pantie[:, ::-1], pantie], axis=1)
        return Image.fromarray(pantie)
