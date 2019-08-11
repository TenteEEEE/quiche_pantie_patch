import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_yuko.png', **options):
        super().__init__('Yuko', body=body, pantie_position=[1, 1130], **options)
        self.mask = io.imread('./mask/mask_yuko.png')
        try:
            self.use_ribbon_mesh = self.options['use_ribbon_mesh']
        except:
            self.use_ribbon_mesh = self.ask(question='Use Yuko ribbon mesh?', default=False)

    def convert(self, image):
        pantie = np.array(image)
        [r, c, d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (270, 60), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[125:125 + pr, :pc, :] = np.uint8(patch * 255)

        # Inpainting ribbon
        if self.use_ribbon_mesh:
            pantie = ribbon_inpaint(pantie)

        # Front transform
        front = pantie[:390, :250, :]
        front = np.pad(front, [(0, 0), (50, 0), (0, 0)], mode='constant')
        front = front.transpose(1, 0, 2)
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[40:] -= (np.linspace(0, 1 * np.pi, 60)**2) * 4
        arrx[28:70] += (np.sin(np.linspace(0, 1 * np.pi, 100)) * 10)[28:70]
        front = affine_transform_by_arr(front, arrx, arry, smooth=False)
        front = np.uint8(front.transpose(1, 0, 2) * 255)[:, 38:]

        # Back transform
        back = pantie[:350, 250:, :]
        back = np.pad(back, [(0, 0), (0, 100), (0, 0)], mode='constant')
        back = back.transpose(1, 0, 2)
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[10:] -= (np.linspace(0, 1 * np.pi, 90)**3) * 14
        back = affine_transform_by_arr(back, arrx, arry, smooth=True)
        back = np.uint8(back.transpose(1, 0, 2) * 255.0)[:, 1:]

        # Merge front and back
        pantie = np.zeros((np.max((front.shape[0], back.shape[0])), front.shape[1] + back.shape[1], d), dtype=np.uint8)
        pantie[:front.shape[0], :front.shape[1]] = front
        pantie[:back.shape[0], front.shape[1]:] = back

        # main transform
        arrx = np.zeros((100))
        arry = np.zeros((100))
        arrx[35:] += (np.cos(np.linspace(0, 1 * np.pi, 100) - np.pi) * -75)[35:] - 30
        arrx[:30] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi / 0.9) * 10)[:30]
        arrx[50:80] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi) * 11)[:30]
        arry += np.linspace(0, 1, 100) * -50
        arry[:30] += (np.sin(np.linspace(0, 3 * np.pi, 100) - np.pi) * 35)[:30]
        pantie = affine_transform_by_arr(pantie, arrx, arry, smooth=True)
        pantie = skt.rotate(pantie, 8.1, resize=True)
        pantie = resize(pantie, [2.31, 2.31])
        pantie = pantie[140:-80, 72:]

        # Finalize
        pantie = np.uint8(pantie * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
