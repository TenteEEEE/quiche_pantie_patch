import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_lopolykon.png', **options):
        super().__init__('ロポリこん', body=body, pantie_position=[5, 662], **options)
        self.skin = Image.open('./material/lopolykon_skin.png')

    def convert(self, image):
        pantie = np.array(image)
        arrx = np.zeros(100)
        arrx[:50] = np.sin(np.linspace(0, np.pi, 50)) * -50
        arry = np.zeros(100)
        arry[12:-10] = np.sin(np.linspace(0, np.pi, 78)) * 350
        pantie = affine_transform_by_arr(pantie, arrx, arry)[:140,:300]
        pantie = np.uint8(resize(pantie, [0.84, 0.84])*255)
        return Image.fromarray(pantie)
        
    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        patched = self.paste(patched, self.skin, [0, 0])
        patched = self.paste(patched, pantie, self.pantie_position)
        return patched
