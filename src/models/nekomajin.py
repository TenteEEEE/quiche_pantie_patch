import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.models.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_nekomajin.png', **options):
        super().__init__(name='ねこまじん', body=body, pantie_position=[-20,0], **options)
        self.mask = io.imread('./mask/mask_nekomajin.png')

    def convert(self, image):
        pantie = np.array(image)
        [r, c, d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-200:, 546:, :])
        pantie[-200:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (247, 40), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[160:160 + pr, :pc, :] = np.uint8(patch * 255)
        
        # Affine transform matrix
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        dst_rows = src[:, 1]
        dst_cols = src[:, 0]
        dst = np.vstack([dst_cols, dst_rows]).T
        dst[2:9,1] = dst[1,1] + (dst[2:9,1]-dst[1,1]) * 0.7
        dst[12:19,1] = dst[11,1] + (dst[12:19,1]-dst[11,1]) * 0.7
        dst[22:29,1] = dst[21,1] + (dst[22:29,1]-dst[21,1]) * 0.8
        dst[32:39,1] = dst[31,1] + (dst[32:39,1]-dst[31,1]) * 0.9
        dst[42:49,1] = dst[41,1] + (dst[42:49,1]-dst[41,1]) * 1.0
        dst[52:59,1] = dst[51,1] + (dst[52:59,1]-dst[51,1]) * 1.1
        dst[62:69,1] = dst[61,1] + (dst[62:69,1]-dst[61,1]) * 1.2
        dst[72:79,1] = dst[71,1] + (dst[72:79,1]-dst[71,1]) * 1.3
        dst[82:89,1] = dst[81,1] + (dst[82:89,1]-dst[81,1]) * 1.3
        dst[92:99,1] = dst[91,1] + (dst[92:99,1]-dst[91,1]) * 1.35
        dst[15:20,0] -= np.linspace(0, 20, 5)

        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = np.uint8(skt.warp(pantie, affin) * 255)

        # Finalize
        pantie = skt.resize(pantie, (866,1813), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie * 255)
        pantie = np.bitwise_and(pantie, self.mask)
        return Image.fromarray(pantie)
