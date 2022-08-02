import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_karin.png', **options):
        super().__init__('カリン', body=body, pantie_position=[1030, 2393], **options)
        self.mask = io.imread('./mask/mask_karin.png')

    def convert(self, image):
        # image = Image.open('./dream/0101.png')
        pantie = np.array(image)
        pantie = ribbon_inpaint(pantie)
        patch = np.copy(pantie[-160:-5, 548:, :])[::-1, ::-1, :]
        [pr, pc, d] = patch.shape
        pantie[105:105 + pr, :pc, :] = patch
        div = 49
        arrx = np.zeros(div) - 150
        arrx += np.linspace(0, 1, div)**2.1 * 210
        arrx += np.sin(np.linspace(0, np.pi, div))**1.5 * 4
        arrx[7:17] -= np.sin(np.linspace(0, np.pi, 10)) * 6
        arry = np.linspace(0, 1, div)**2 * 50
        pantie = affine_transform_by_arr(pantie, arrx, arry)[:400, 7:-70]
        pantie = np.uint8(resize(pantie, [2.04, 1.85])*255)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)