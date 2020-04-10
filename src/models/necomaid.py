import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_necomaid.png', **options):
        super().__init__('スピカ', body=body, pantie_position=[0, 0], **options)
        self.mask = io.imread('./mask/mask_necomaid.png')

    def convert(self, image):
        image = Image.open('./dream/0101.png')
        pantie = np.array(image)
        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-150:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0]-50, 60), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[120:120 + pr, :pc, :] = np.uint8(patch * 255)
        
        arrx = np.zeros(100)
        arry = np.zeros(100)
        arry[10:] += np.sin(np.linspace(0,np.pi,90))*120
        # arry[3:13] += np.sin(np.linspace(0,np.pi,10))*-50
        import matplotlib.pyplot as plt
        pantie_ = affine_transform_by_arr(pantie, arrx, arry)
        
        io.imshow(pantie_)
        io.imsave('test.png', pantie_)
        
        # pantie = np.uint8(resize(pantie, [1.38, 1.62]) * 255)[:, 11:]
        # pantie = np.bitwise_and(pantie, self.mask)[:, 1:]
        # pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        # components = self.gen_components(image)
        return Image.fromarray(pantie)
