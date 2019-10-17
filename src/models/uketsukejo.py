import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *
from scipy.interpolate import interp1d


class patcher(patcher):
    def __init__(self, body='./body/body_uketsukejo.png', **options):
        super().__init__('受付嬢', body=body, pantie_position=[860, 1671], **options)
        self.mask = io.imread('./mask/mask_uketsukejo.png')

    def convert(self, image):
        pantie = np.array(image)

        patch = np.copy(pantie[-140:-5, 546:, :])
        patch = skt.resize(patch[::-1, ::-1, :], (230, 65), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[127 - 5:127 - 5 + pr, :pc, :] = np.uint8(patch * 255)
        front = pantie[:, :300]
        back = pantie[:, 300:-10]
        back[380:] = 0
        front = front[::-1, ::-1]
        back = back[::-1, ::-1]

        def mesh_transform(img, arr):
            [r, c, d] = img.shape
            src_cols = np.linspace(0, c, int(np.sqrt(arr.shape[0])))
            src_rows = np.linspace(0, r, int(np.sqrt(arr.shape[0])))
            src_rows, src_cols = np.meshgrid(src_rows, src_cols)
            src = np.dstack([src_cols.flat, src_rows.flat])[0]
            affin = skt.PiecewiseAffineTransform()
            affin.estimate(arr, src)
            return skt.warp(img, affin)
            
        front_arr = np.array([
            [280, 144],
            [305, 171],
            [314, 203],
            [314, 241],
            [314, 365],

            [286, 124],
            [330, 141],
            [346, 181],
            [355, 222],
            [427, 350],

            [284, 88],
            [351, 108],
            [378, 131],
            [391, 183],
            [512, 283],

            [263, 74],
            [351, 69],
            [421, 97],
            [454, 135],
            [569, 190],

            [216, -2],
            [406, 0],
            [475, 12],
            [532, 26],
            [623, 88],
        ])
        front_arr[:, 0] -= back.shape[1]

        back_arr = np.array([
            [348, 0],
            [249, 0],
            [158, 11],
            [78, 27],
            [5, 54],

            [348, 72],
            [260, 73],
            [186, 89],
            [118, 111],
            [40, 156],

            [342, 96],
            [290, 124],
            [223, 140],
            [174, 187],
            [100, 250],

            [354, 113],
            [310, 155],
            [274, 189],
            [238, 245],
            [200, 334],

            [378, 146],
            [346, 176],
            [324, 212],
            [320, 245],
            [320, 365],
        ])
        front = np.uint8(mesh_transform(front, front_arr)[:, :-2] * 255)
        back = np.uint8(mesh_transform(back, back_arr)[:, 2:] * 255)
        pantie = np.concatenate((back, front), axis=1)[:-30]
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
