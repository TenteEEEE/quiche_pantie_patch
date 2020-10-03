from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from skimage.color import rgb2hsv, hsv2rgb


class patcher(patcher):
    def __init__(self, body='./body/body_yuu.png', **options):
        super().__init__('ユウ', body=body, pantie_position=[634, 7], **options)
        self.mask = io.imread('./mask/mask_yuu.png')

    def convert(self, image):
        pantie = np.array(image)
        patch = np.copy(pantie[-170:-5, 546:, :])
        [pr, pc, d] = patch.shape
        pantie[115:115 + pr, :pc, :] = patch[::-1, ::-1]
        arrx = np.zeros(25)
        arry = np.zeros(25)
        arry[5:20] = np.sin(np.linspace(0,np.pi,15))*75
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie = perspective_transform(pantie, np.array([[1,0,0],[-0.001,1,0],[-0.0002,0,1]]))[:,:550]
        pantie = np.uint8(resize(pantie[:275], [1.,1.29])*255)[:,8:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:,::-1], pantie), axis=1)
        return Image.fromarray(pantie)
