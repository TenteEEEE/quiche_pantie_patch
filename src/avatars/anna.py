import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image

import sys
sys.path.append('./src/avatars')
from class_patcher import patcher


class patcher(patcher):
    def __init__(self):
        super().__init__('Anna', body='./body/body_anna.png', pantie_position=[31, 1115])
        self.mask = io.imread('./mask/mask_anna.png')

    def convert(self, image):
        pantie = np.array(image)
        pantie = np.bitwise_and(pantie, self.mask)
        [r, c, d] = pantie.shape

        # move from hip to front
        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-100:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 40), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[157:157 + pr, :pc, :] = np.uint8(patch * 255)

        # Affine transform matrix
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row = -(np.sin(np.linspace(0, 1 * np.pi, src.shape[0]) - np.pi / 8) * 60)
        shifter_row[-30:] += (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]))[-30:] * 50)
        shifter_row = np.convolve(shifter_row, np.ones(30) / 30, mode='same')
        dst_rows = src[:, 1] + shifter_row - 20
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = np.uint8(skt.warp(pantie, affin) * 255)
        pantie = pantie[:, 6:-35, :]

        # Finalize
        pantie = skt.resize(pantie, (np.int(pantie.shape[0] * 1.25), np.int(pantie.shape[1] * 1.56)), anti_aliasing=True, mode='reflect')
        pantie = np.uint8(pantie * 255)
        return Image.fromarray(pantie)
