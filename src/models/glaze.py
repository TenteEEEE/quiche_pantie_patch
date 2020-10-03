from PIL import Image, ImageOps
import numpy as np
import skimage.io as io
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_glaze.png', **options):
        super().__init__('ぐれーず', body=body, pantie_position=[0, 0], **options)
        self.mask = io.imread('./mask/mask_glaze.png')

    def convert(self, image):
        # image = Image.open('./dream/0101.png')
        pantie = np.array(image)
        patch = np.copy(pantie[-140:-5, 546:, :])
        [pr, pc, d] = patch.shape
        
        arrx = np.zeros(25)-10
        arry = np.zeros(25)-5
        arrx[6:-10] += np.sin(np.linspace(0,np.pi,9))*4
        arrx[-15:] -= np.sin(np.linspace(0,np.pi/2,15))*5
        arry[1:5] -= np.sin(np.linspace(0,np.pi,4))*25
        arry[5:] += np.sin(np.linspace(0,np.pi/2,20))*40
        pantie = affine_transform_by_arr(pantie, arrx, arry)
        pantie[125:125 + pr, :pc, :] = np.float32(patch[::-1, ::-1]/255)
        pantie = np.uint8(resize(pantie[:320,:-50], [3.25,3.15])*255)[:,38:]
        io.imsave('tmp.png', pantie)
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:,::-1], pantie), axis=1)
        return Image.fromarray(pantie)
