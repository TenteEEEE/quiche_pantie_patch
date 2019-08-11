import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *

import matplotlib.pyplot as plt

class patcher(patcher):
    def __init__(self, body='./body/body_yuko.png', **options):
            super().__init__('Yuko', body=body, pantie_position=[0, 0], **options)
            
    # def inpaint(self, image, mask):
    def ribbon_inpaint(image):
        mask = io.imread('./mask/ribbon4inpaint.png')
        ribbon = image[19:58, 5:35, :3]
        ribbon_mask = (mask[19:58, 5:35, 1]>0)[:,:,None]
        removed = ribbon*(mask[19:58, 5:35, 1]<1)[:,:,None].astype(np.float)
        search_area = image[60:100-1,:40,:3].astype(np.float)
        [r,c,d] = ribbon_mask.shape
        dx = search_area.shape[1] - ribbon.shape[1]
        score = np.zeros(dx)
        for x in range(dx):
            inpainter = search_area[:,x:x+c,:]*ribbon_mask
            inpainted = removed + inpainter
            for vx in range(dx):
                score[x] += np.mean((inpainted-search_area[:,vx:vx+c])**2)
        optimum = np.argmin(score)
        inpainter = search_area[:,optimum:optimum+c,:]*ribbon_mask
        inpainted = removed + inpainter
        image[19:58, 5:35, :3] = np.uint8(inpainted)
        return image

    def convert(self, image):
        image = Image.open('./dream/0200.png')
        pantie = np.array(image)
        [r,c,d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (270, 60), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = np.uint8(patch * 255)
        
        # Inpainting ribbon
        # pantie = ribbon_inpaint(pantie)
        # pantie = resize(pantie,[2.62,2.62])
        # io.imshow(pantie)
        
        # Front transform
        front = pantie[:390, :250, :]
        front = front.transpose(1,0,2)
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[30:] -= (np.linspace(0, 1 * np.pi, 70)**2)*5
        front = affine_transform_by_arr(front,arrx,arry,smooth=True)
        front = np.uint8(front.transpose(1,0,2)*255)
        
        # Back transform
        back = pantie[:350, 250:, :]
        back = (np.pad(back, [(0, 0), (0, 100), (0, 0)], mode='constant'))
        back = back.transpose(1,0,2)
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[10:] -= (np.linspace(0, 1 * np.pi, 90)**3)*14
        back = affine_transform_by_arr(back,arrx,arry,smooth=True)
        back = np.uint8(back.transpose(1,0,2)*255.0)[:,1:]
        
        pantie = np.zeros((r,c+99,d),dtype=np.uint8)
        pantie[:front.shape[0],:front.shape[1]]=front
        pantie[:back.shape[0],front.shape[1]:]=back
        io.imshow(pantie)
        
        # main transform
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[35:] += (np.cos(np.linspace(0, 1 * np.pi, 100) - np.pi) * -75)[35:]-30
        arrx[:30] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi) * 15)[:30]
        arrx[5:20] += (np.sin(np.linspace(0, 6 * np.pi, 100) - np.pi) * -10)[:15]
        # arry += np.sin(np.linspace(0, 1 * np.pi, 100) + np.pi/2) * 40
        plt.plot(arrx)
        pantie_ = affine_transform_by_arr(pantie,arrx,arry, smooth=True)
        pantie_ = skt.rotate(pantie_, 8.1, resize=True)
        io.imsave('test.png',pantie_)
        io.imshow(affine_transform_by_arr(pantie,arrx,arry,smooth=True))
        

        # front = pantie[:390, :250, :]
        # back = pantie[:350, 250:, :]
        io.imshow(front)
        
        io.imshow(front_)
        io.imsave('test.png',front)

        # Finalize
        pantie_ = skt.resize(pantie, (np.int(pantie.shape[0] * 2.05), np.int(pantie.shape[1] * 2.05)), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie_ * 255)
        return Image.fromarray(pantie)
