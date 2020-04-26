import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image, ImageOps
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_leeme.png', **options):
        super().__init__('リーメ(下着)', body=body, pantie_position=[-9, 475], **options)
        self.mask = io.imread('./mask/mask_leeme.png')

    def convert(self, image):
        pantie = np.array(image)
        front = pantie[:116, :260]
        arrx = np.zeros(25)
        arry = np.linspace(0,1,25)**2*15
        front = affine_transform_by_arr(front, arrx, arry)[:-1,:]
        
        back = pantie[:-8, 260:][::-1, ::-1]
        arry = np.linspace(0,1,25)**2*15
        back = affine_transform_by_arr(back, arrx, arry)[1:,:]
        
        front = np.pad(front, [(0, 0), (0, back.shape[1] - front.shape[1]), (0, 0)], mode='constant')
        pantie = np.concatenate((front, back), axis=0)
        pantie = np.uint8(resize(pantie, [2.87,2.862])*255)[:,20:]
        pantie = np.bitwise_and(pantie, self.mask)
        pantie = np.concatenate((pantie[:, ::-1], pantie), axis=1)
        return Image.fromarray(pantie)

    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
