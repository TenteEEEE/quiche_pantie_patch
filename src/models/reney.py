import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_reney.png', **options):
        super().__init__(name='リネィ', body=body, pantie_position=[15, -36], **options)
        self.mask = io.imread('./mask/mask_reney.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-170:-7, 546:, :])
        pantie[-100:, 546:, :] = 0
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = patch[::-1, ::-1]

        pantie = np.pad(pantie, [(0, 0), (0, 200), (0, 0)], mode='constant')
        arrx = np.zeros(100) - 20
        arry = np.zeros(100)
        arry[10:85] += np.sin(np.linspace(0, np.pi, 75))**2 * -80
        arry[60:] += np.sin(np.linspace(0, np.pi, 40))**2 * -80
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie = perspective_transform(pantie, np.matrix('1, 0.0, 0; -0.01, 1, 0; -0.0004,0,1'))[:310, :550]
        pantie = np.uint8(resize(pantie, [4.48, 6.15]) * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
