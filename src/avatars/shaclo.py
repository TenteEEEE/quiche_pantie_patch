import skimage.io as io
import skimage.transform as skt
import numpy as np
from PIL import Image
from src.avatars.class_patcher import patcher
from src.utils.imgproc import *


class patcher(patcher):
    def __init__(self, body='./body/body_shaclo.png', stitch_correction=None):
        super().__init__('Shaclo', body=body, pantie_position=[62, 16])
        if stitch_correction is None:
            ans = input('Apply stitch correction? [default:no] (y/n):')
            if ans is 'y':
                self.stitch_correction = True
            else:
                self.stitch_correction = False
        else:
            self.stitch_correction = stitch_correction
    def convert(self, image):
        pantie = np.array(image)
        [r, c, d] = pantie.shape
        # move from hip to front
        patch = np.copy(pantie[-170:, 546:, :])
        pantie[-80:, 546:, :] = 0
        patch = skt.resize(patch[::-1, ::-1, :], (patch.shape[0], 40), anti_aliasing=True, mode='reflect')
        [pr, pc, d] = patch.shape
        pantie[157:157 + pr, :pc, :] = np.uint8(patch * 255)

        # cut intermediate pantie (for acculate stitch on hip)
        pantie[260:, 546:, :] = 0
        pantie = pantie[:365, :, :]
        pantie = pantie[:, :-10, :]

        if self.stitch_correction:
            pantie = np.delete(pantie, [np.arange(200, 275)], 1)
            pantie = np.pad(pantie[:, :, :], ((0, 0), (0, 40), (0, 0)), mode='reflect')
            pantie = np.pad(pantie[:, :, :], ((0, 0), (0, 50), (0, 0)), mode='reflect')

        # Afine transform matrix
        src_cols = np.linspace(0, c, 10)
        src_rows = np.linspace(0, r, 10)
        src_rows, src_cols = np.meshgrid(src_rows, src_cols)
        src = np.dstack([src_cols.flat, src_rows.flat])[0]
        shifter_row = np.zeros(src.shape[0])
        shifter_col = np.zeros(src.shape[0])
        shifter_row[10:50] = (np.sin(np.linspace(0, 1 * np.pi, src.shape[0]))[20:60] * 40)
        shifter_row[00:20] = -(np.sin(np.linspace(0, 1 * np.pi, src.shape[0]))[50:70] * 15)
        shifter_row[50:] = -(np.sin(np.linspace(0, 1 * np.pi, src.shape[0]))[0:50] * 10)
        shifter_row = np.convolve(shifter_row, np.ones(30) / 30, mode='same')
        dst_rows = src[:, 1] + shifter_row - 50
        dst_cols = src[:, 0] + shifter_col
        dst = np.vstack([dst_cols, dst_rows]).T
        affin = skt.PiecewiseAffineTransform()
        affin.estimate(src, dst)
        pantie = np.uint8(skt.warp(pantie, affin) * 255)

        # mirroring and finalize
        overlap = 6
        [r, c, d] = pantie.shape
        pantie_new = np.zeros((r, c * 2 - overlap * 2, d), dtype=np.uint8)
        pantie_inv = pantie[:, ::-1, :]
        pantie_new[:r, :c, :] = pantie_inv
        pantie_new[:r, c - overlap:c * 2 - overlap, :] = pantie[:, overlap:, :]
        if self.stitch_correction:
            mag_c = 1.7
        else:
            mag_c = 1.72
        mag_r = 1.8
        out = skt.resize(pantie_new, (np.int(pantie_new.shape[0] * mag_r), np.int(pantie_new.shape[1] * mag_c)), anti_aliasing=True, mode='reflect')
        out = np.uint8(out * 255)
        return Image.fromarray(out)
