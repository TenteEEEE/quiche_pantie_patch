import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_corona.png', **options):
        super().__init__('コロナ', body=body, pantie_position=[2448, 24], **options)
        self.inner_position = [2371, 1005]
        self.ribbon_position = [3009, 189]
        self.mask = io.imread('./mask/mask_corona.png')
        self.mask_inner = io.imread('./mask/mask_corona_inner.png')
        try:
            self.use_ribbon_mesh = self.options['use_ribbon_mesh']
        except:
            self.use_ribbon_mesh = self.ask(question='Use Corona ribbon mesh?', default=False)
        if self.use_ribbon_mesh:
            self.ribbon_base = io.imread('./material/corona_ribbon.png')[:, :, :3] / 255
            self.ribbon_shade = io.imread('./material/corona_ribbon_shade.png')[:, :, 3] / 255

    def convert(self, image):
        pantie = np.array(image)
        if self.use_ribbon_mesh:
            pantie = ribbon_inpaint(pantie)
        front = pantie[:116, :300]
        back = pantie[:-8, 300:][::-1,::-1]
        front = np.pad(front, [(0, 0), (0, back.shape[1] - front.shape[1]), (0, 0)], mode='constant')
        pantie = np.concatenate((front, back), axis=0)
        pantie = np.uint8(resize(pantie,[1.57, 1.57])*255)
        pantie = np.bitwise_and(pantie, self.mask)[:,12:]
        pantie = np.concatenate((pantie[:,::-1], pantie), axis=1)
        return Image.fromarray(pantie)
        
    def convert_inner(self, image):
        pantie = np.array(image)
        pantie = ribbon_inpaint(pantie)
        front = pantie[:, :300]
        arrx = 200*np.linspace(0,1,25)**2
        arrx[6:] += 50*np.sin(np.linspace(0,np.pi,19))
        arrx -= 200
        arry = np.zeros(25)
        front = affine_transform_by_arr(front, arrx, arry)
        front = np.uint8(front[:-80]*255)

        back = pantie[:-8, 300:][::-1,::-1]
        back = np.pad(back, [(0, 300), (0,0), (0,0)], mode='constant')
        arrx = -200*np.linspace(0,1,25)
        back = affine_transform_by_arr(back, arrx, arry)
        back = np.uint8(back[70:-100]*255)
        
        front = np.pad(front, [(0, 0), (0, back.shape[1] - front.shape[1]), (0, 0)], mode='constant')
        pantie = np.concatenate((front, back), axis=0)[:,16:]
        pantie = np.uint8(resize(pantie,[1.50, 1.50])*255)
        pantie = np.bitwise_and(pantie, self.mask_inner)
        pantie = np.concatenate((pantie[:,::-1], pantie), axis=1)
        return Image.fromarray(pantie)
    
    def gen_ribbon(self, image):
        image = np.array(image)
        ribbon = image[19:58, 5:35, :3]
        base_color = np.mean(np.mean(ribbon[5:12, 16:20], axis=0), axis=0) / 255
        shade_color = np.mean(np.mean(ribbon[8:14, 7:15], axis=0), axis=0) / 255
        ribbon_base = (self.ribbon_base > 0) * base_color
        ribbon_shade = self.ribbon_shade[:, :, None] * (1 - shade_color)
        ribbon = ribbon_base - ribbon_shade
        ribbon = np.dstack((ribbon, ribbon[:, :, 0] > 0))
        ribbon = np.clip(ribbon, 0, 1)
        return Image.fromarray(np.uint8(ribbon * 255))
        
    def patch(self, image, transparent=False):
        pantie = self.convert(image)
        inner = self.convert_inner(image)
        if transparent:
            patched = Image.new("RGBA", self.body_size)
        else:
            patched = self.body.copy()
        if self.use_ribbon_mesh:
            ribbon = self.gen_ribbon(image)
            self.paste(patched, ribbon, self.ribbon_position)
        self.paste(patched, inner, self.inner_position)
        self.paste(patched, pantie, self.pantie_position)
        return patched
        
